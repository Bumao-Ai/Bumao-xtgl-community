# -*- coding: utf-8 -*-
# Copyright 2026 Bumao
#
# Licensed under the Apache License, Version 2.0.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Bumao XTGL Community · Engine Entry (v0.1)
Unified kernel v4.0 — ALL original gates restored (~24 gates).
No check is removed. Each gate is registered via core.register(gid, fn, label).
"""

import os, sys, re, json, io

HERE = os.path.dirname(os.path.abspath(__file__))
HX = os.path.dirname(HERE)  # HX/community/
VIEW_DIR = os.path.join(HX, "20_view")
LEDGER_DIR = os.path.join(HX, "30_taizhang")

# Insert kernel path for bumao_core import（内核已内嵌：本仓根目录 kernel/bumao_core）
_kernel_dir = os.path.abspath(os.path.join(HERE, "..", "kernel", "bumao_core"))
sys.path.insert(0, _kernel_dir)
sys.path.insert(0, HERE)

# --- Inject rules_db + local deps ---
import rules_db as R
import lock as LK
import render as RN
import qiangzhi as Q
import pprint

META = os.path.join(HX, "00_meta", "meta.json")
PII_WORDS = os.path.join(HX, "00_meta", "pii_words.json")
MAPF = os.path.join(HX, "00_meta", "jiancha_map.json")
ENTRY = os.path.join(HX, "README-HX.txt")
ZH = os.path.join(HERE, "zhunze")

# Compatibility shims
def _load_meta():
    return json.loads(R.rd(R.META)) if os.path.exists(R.META) else {}
R.load_meta = _load_meta
if not hasattr(R, 'load_db'): R.load_db = R.load

# Helper functions
def _rd(path):
    try: return open(path, encoding="utf-8").read()
    except: return ""

# 运行时拼装，免得本 wrapper 触发自己定义的 B6/B7（故不再整文件豁免）
_PII_KEYBEGIN = "-" * 5 + "BEGIN"

def pii_hits(text, extra_words=(), skip_unc=False):
    _P_DRIVE = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]")  # 排除 http:// 这类协议前缀，只认盘符
    _P_UNC = re.compile(r"\\\\[A-Za-z]")
    _P_KEYBEGIN = re.compile(_PII_KEYBEGIN)
    _P_SK = re.compile(r"\bsk-[A-Za-z0-9]{6,}")
    items = [("drive_path", _P_DRIVE), ("privkey_header", _P_KEYBEGIN), ("secret_key_pat", _P_SK)]
    if not skip_unc: items.append(("unc_path", _P_UNC))
    hits = []
    for tag, pat in items:
        if pat.search(text): hits.append(tag)
    for w in extra_words:
        if len(w) >= 4 and w in text: hits.append("env_id(%s)" % w)
    return hits

def env_identities():
    out = []
    for k in ("USERNAME", "USER", "COMPUTERNAME", "HOSTNAME", "USERPROFILE", "HOME"):
        v = os.environ.get(k)
        if v and len(v) >= 4: out.append(v)
    return sorted(set(out))

def load_pii_words():
    if not os.path.exists(PII_WORDS): return []
    j = json.loads(_rd(PII_WORDS))
    return [w for w in j.get("words", []) if len(w) >= 2]

def scan_targets():
    files = []
    for base, ext in ((ZH, ".json"), (os.path.join(HX, "00_meta"), ".json"),
                      (HERE, ".py"), (VIEW_DIR, ".txt"), (LEDGER_DIR, ".txt")):
        if os.path.isdir(base):
            files += [(base, f) for f in sorted(os.listdir(base))
                      if f.endswith(ext) and os.path.isfile(os.path.join(base, f))]
    for extra in (ENTRY,):
        if os.path.exists(extra): files.append((os.path.dirname(extra), os.path.basename(extra)))
    ex = {os.path.abspath(PII_WORDS)} if os.path.exists(PII_WORDS) else set()
    return [(b, f, os.path.splitext(f)[1] in (".json",))  # rel=abspath, t=content, skip_enc=json
            for b, f in files if os.path.abspath(os.path.join(b, f)) not in ex]

_EXCL = {"render.py", "rules_db.py"}  # 原六条中四条指向不存在的文件，engine.py 亦不在本端 10_rac（Q123）

# --- Configure unified core engine (one file, three products) ---
try:
    import engine as core
except ImportError:
    sys.stderr.write("[FATAL] missing gate kernel: no engine.py under ../kernel/bumao_core "
            "(relative to this file). This edition ships with the kernel inside the repo; "
            "restore kernel/bumao_core from the bumao-core repo (whole-directory overwrite), then re-run. exit=2" + chr(10))
    sys.exit(2)
core.configure(rules_db_module=R)

# =========================== B-GATES (restored from original community engine.py) ===========================

# B1: 视图漂移为 0
def b1_drift():
    drift = RN.check_drift() if os.path.exists(META) else ["<meta 缺失>"]
    return not drift, str(drift[:5])
core.register("B1", b1_drift, "视图漂移为 0")

# B2: 渲染幂等
def b2_idem():
    meta = R.load_meta()
    try:
        t1 = [s for _, s in RN.targets(meta)]
        t2 = [s for _, s in RN.targets(meta)]
        diff = sum(1 for a, b in zip(t1, t2) if a != b)
        return diff == 0, "两次渲染差异 %d" % diff
    except Exception as e:
        return False, "渲染异常：%s" % e
core.register("B2", b2_idem, "渲染幂等")

# B3: 工程域根下平铺文件 ≤ 1
def b3_root_flat():
    # 2026-11-07 改判据：令文要求对外门面件置仓库根，故根下平铺只允许
    # 「入口导航 + 门面白名单」，其余仍判 FAIL。白名单宁多不少，覆盖标准门面件。
    _ROOT_ALLOW = {"README-HX.txt", "README-HX.md", "README.md", "NOTICE", "TRADEMARK.md",
                   "CONTRIBUTING.md", "LICENSE", "DCO", "CHANGELOG.md", "COMPLIANCE.md",
                   "OPEN_SOURCE_NOTICE.md", "SECURITY.md", "CODE_OF_CONDUCT.md", ".gitignore"}
    flat = [f for f in sorted(os.listdir(HX)) if os.path.isfile(os.path.join(HX, f))]
    bad = [f for f in flat if f not in _ROOT_ALLOW]
    return not bad, ("根下平铺 %d 件（白名单内 %d，越界 %d）：%s"
                     % (len(flat), len(flat) - len(bad), len(bad), str(bad[:5])))
core.register("B3", b3_root_flat, "工程域根下平铺文件 ≤ 1")

# B4: 子目录名匹配格式（kernel/ 例外，但必须内含 bumao_core）
def b4_subdir_names():
    dirs = [f for f in sorted(os.listdir(HX))
            if os.path.isdir(os.path.join(HX, f)) and not f.startswith(".")]
    _DIR_ALLOW = {"kernel"}
    baddir = [x for x in dirs if not re.match(r"^\d{2}_[a-z]+$", x) and x not in _DIR_ALLOW]
    if "kernel" in dirs:
        kc = os.path.join(HX, "kernel", "bumao_core")
        if not (os.path.isdir(kc) and os.listdir(kc)):
            return False, "kernel/ 存在但缺少 bumao_core（内置内核不完整）"
    return not baddir, "bad dirs: %s" % str(baddir[:3])
core.register("B4", b4_subdir_names, r"子目录名匹配 ^\d{2}_[a-z]+$（kernel 需含 bumao_core）")

# B5: zhunze 文件数 = 章数
def b5_zcount():
    zf = R.zhang_files()
    db = R.load_db(); nc = len(db["chapters"])
    return len(zf) == nc, "%d / %d" % (len(zf), nc)
core.register("B5", b5_zcount, "zhunze 文件数 = 章数")

# --- Configuration complete ---
# All B-GATE definitions are above. Now we proceed with B6+ gates.

# B6: PII 扫描
def b6_pii_scan():
    words = env_identities()
    units = scan_targets()
    bad_pii = []
    for base, fname, skip_enc in units:
        # Exclude wrapper/engine files themselves from PII scan (they contain pattern strings)
        if fname in _EXCL: continue
        fpath = os.path.join(base, fname)
        try:
            t = open(fpath, encoding="utf-8", errors="replace").read() if skip_enc else _rd(fpath)
        except Exception:
            t = ""
        h = pii_hits(t, words, skip_unc=skip_enc)
        if h: bad_pii.append("%s:%s" % (fname, "/".join(h)))
    return not bad_pii, str(bad_pii[:5])
core.register("B6", b6_pii_scan, "去私人化扫描（路径/本机标识/密钥）")

# B6b: 私域词表扫描
def b6b_word_scan():
    words_cfg = load_pii_words()
    units = scan_targets()
    bad_word = []
    if words_cfg:
        for base, fname, skip_enc in units:
            fpath = os.path.join(base, fname)
            try:
                t = open(fpath, encoding="utf-8", errors="replace").read() if skip_enc else _rd(fpath)
            except Exception:
                t = ""
            for w in words_cfg:
                if w in t: bad_word.append("%s:%s" % (fname, w))
    ok = not bad_word
    msg = "词表 %d 条 / 命中 0" % len(words_cfg) if ok else str(bad_word[:5])
    return ok, msg
core.register("B6b", b6b_word_scan, "私域词表扫描（人设语料类·可配置）")

# B7: 交付物卫生
def b7_delivery_hygiene():
    bad_code = []
    for p in sorted(os.listdir(HERE)):
        if not p.endswith(".py"): continue
        if os.path.basename(p) in _EXCL: continue
        t = _rd(os.path.join(HERE, p))  # 不再剥离：旧剥离会丢掉真实私钥首行（Q123②）
        h = pii_hits(t, skip_unc=True)
        if h: bad_code.append("%s:%s" % (p, "/".join(h)))
    return not bad_code, str(bad_code[:5])
core.register("B7", b7_delivery_hygiene, "交付物卫生（脚本无盘符 / 无明文密钥）")

# B8a: 全文归档存在且文件名由 meta 注入
def b8a_archive():
    ver = R.load_meta().get("version", "")
    vtxt = os.path.join(VIEW_DIR, "quanwen_%s.txt" % ver)
    ok = os.path.exists(vtxt)
    return ok, os.path.basename(vtxt) if ok else "<归档缺失>"
core.register("B8a", b8a_archive, "全文归档存在且文件名由 meta 注入")

# B8b: 分章首行版本由 meta 注入
def b8b_chapter_head():
    meta = R.load_meta()
    ver = meta.get("version", ""); name = meta.get("name", "")
    bad = []
    for c in R.load_db()["chapters"]:
        p = os.path.join(VIEW_DIR, c["file"])
        if not os.path.exists(p): bad.append(c["ch"]); continue
        head = _rd(p).split("\n")[0]
        want = "来源：%s %s 第%d章" % (name, ver, c["ch"])
        if head != want: bad.append(c["ch"])
    return not bad, str(bad)
core.register("B8b", b8b_chapter_head, "分章首行版本由 meta 注入")

# B8c: 入口页版本与 meta 一致
def b8c_entry_version():
    ver = R.load_meta().get("version", "")
    if not os.path.exists(ENTRY):
        return False, "<入口缺失>"
    content = _rd(ENTRY)
    pattern = r"当前版本\s*%s(?![\d.])" % re.escape(ver)
    ok = bool(re.search(pattern, content))
    return ok, os.path.basename(ENTRY) if os.path.exists(ENTRY) else "<入口缺失>"
core.register("B8c", b8c_entry_version, "入口页版本与 meta 一致")

# B9: 检查项登记覆盖全部条款
def b9_coverage():
    ids = set(c["id"] for c in R.load_db()["clauses"])
    covered, entrymiss = set(), []
    if os.path.exists(MAPF):
        mj = json.loads(_rd(MAPF))
        for k, v in mj.get("map", {}).items():
            covered |= set(v.get("covers", []))
    else:
        entrymiss.append("<jiancha_map 缺失>")
    miss = sorted(ids - covered)
    return not miss and not entrymiss, str(miss + entrymiss[:5])
core.register("B9", b9_coverage, "检查项登记覆盖全部条款")

# B10: 无残留运行锁
def b10_stale_lock():
    st = LK.stale()
    return st is None, str(st)
core.register("B10", b10_stale_lock, "无残留运行锁")

# B11: 治理台账存在
def b11_ledger_exists():
    led = [f for f in sorted(os.listdir(LEDGER_DIR)) if os.path.isfile(os.path.join(LEDGER_DIR, f))] \
        if os.path.isdir(LEDGER_DIR) else []
    return len(led) > 0, str(led[:3])
core.register("B11", b11_ledger_exists, "治理台账存在")

# B12: 差错台账四列齐全且无残缺行
def b12_cz_fields():
    cz = os.path.join(LEDGER_DIR, "chacuo_zhang.txt")
    cols = ["现象", "根因", "正确做法", "累计次数"]
    cz_bad, cz_msg = [], "<台账缺失>"
    if os.path.exists(cz):
        tab = [l.strip() for l in _rd(cz).replace("\r\n", "\n").split("\n")
               if l.strip().startswith("|")]
        hi = -1
        for i, l in enumerate(tab):
            if all(c in l for c in cols):
                hi = i; break
        if hi < 0:
            cz_bad, cz_msg = ["<未找到四列表头>"], "有表格但缺必备列"
        else:
            nc = len(tab[hi].strip().strip("|").split("|"))
            for j, l in enumerate(tab[hi + 2:], start=1):
                cs = [x.strip() for x in l.strip().strip("|").split("|")]
                if len(cs) != nc or "" in cs:
                    cz_bad.append("数据行%d" % j)
            cz_msg = "列数 %d / 数据行 %d" % (nc, len(tab) - hi - 2)
    return not cz_bad, str(cz_bad) if cz_bad else cz_msg
core.register("B12", b12_cz_fields, "差错台账四列齐全且无残缺行")

# B14: 层目录与 meta.layers 登记一致
def b14_layer_dirs():
    lay = [d.get("dir") for d in R.load_meta().get("layers", [])]
    missdir = [d for d in lay if not os.path.isdir(os.path.join(HX, d))]
    realdir = sorted(f for f in os.listdir(HX)
                     if os.path.isdir(os.path.join(HX, f)) and re.match(r"^\d{2}_[a-z]+$", f))
    outdir = [d for d in realdir if d not in lay]
    return not missdir and not outdir, str(missdir + outdir[:3])
core.register("B14", b14_layer_dirs, "层目录与 meta.layers 登记一致")

# --- 第 11 章 强制类（必须做，前置不满足即阻断）---
core.register("B15", Q.gate_b15, "【强制11.0】改核心件前必须有审批记录")
core.register("B16", Q.gate_b16, "【强制11.1】每次改动必须留痕")
core.register("B17", Q.gate_b17, "【强制11.2】必须声明改动来源")
core.register("B18", Q.gate_b18, "【强制11.3】版本号必须来自单一来源")
core.register("B19", Q.gate_b19, "【强制11.4】必须跑完检查才准落盘")
core.register("B20", Q.gate_b20, "【强制11.5】必须台账登记")

# --- 第 12 章 限制类（不许做，越界即阻断）---
core.register("B21", Q.gate_b21, "【限制12.0】不得擅自改 CORE_VERSION")
core.register("B22", Q.gate_b22, "【限制12.1】不得绕过闸门直接改核心件")
core.register("B23", Q.gate_b23, "【限制12.2】不得把本机路径／执行者代号写进公开件")
core.register("B24", Q.gate_b24, "【限制12.3】不得未审批改动内核")
core.register("B25", Q.gate_b25, "【限制12.4】不得把私人端内容带进开源件")
core.register("B26", Q.gate_b26, "【限制12.5】不得自造许可条款")
core.register("B27", Q.gate_b27, "【强制13.0】整份工程必须可迁移")
core.register("B28", Q.gate_b28, "【强制14.0】前端只用既有 token")
core.register("B29", Q.gate_b29, "【强制11.6】核心件改动必须先落预告行")

# ============================================================
# GATE REGISTRY VERIFICATION (补充篇 §五 第2条)
# We can't patch before register() calls — they're already above.
# Instead pass expected gates to the engine; cmd_check verifies them.
# ============================================================
def _read_gates_decl():
    """期望集唯一来源＝宿主层 00_meta/gates_decl.json（用户 2026-11-06 裁定第 6 项：
    gates 不进真身，wrapper 只读不改）。缺文件／缺键／端名不符／空集合一律直接拒——
    不许退回 wrapper 里的写死清单，退回就等于把声明又塞回代码。"""
    _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "00_meta", "gates_decl.json")
    if not os.path.isfile(_p):
        print("[FATAL] 缺宿主层闸门声明件 %s —— 期望集不许退回 wrapper 字面量" % _p)
        sys.exit(2)
    with open(_p, "rb") as _f:
        _doc = json.loads(_f.read().decode("utf-8-sig"))
    if str(_doc.get("edition", "")).lower() != "community":
        print("[FATAL] 声明件端名与本品不符：%s 里是 %r" % (_p, _doc.get("edition")))
        sys.exit(2)
    _exp = _doc.get("expected")
    if not isinstance(_exp, list) or not _exp:
        print("[FATAL] 声明件 expected 缺失或为空：%s" % _p)
        sys.exit(2)
    return frozenset(_exp)


try:
    core.set_expected("Community", _read_gates_decl())
except Exception as e:
    print("[FATAL] Gate registry setup failed: %s" % e)
    sys.exit(1)

if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass
    sys.exit(core.main())
