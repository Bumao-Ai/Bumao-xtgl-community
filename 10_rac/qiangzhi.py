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

"""qiangzhi.py —— 社区版「强制类／限制类」闸门实现（B15—B28）

定位：第 11 章六条强制项、第 12 章六条限制项的机器判据。每条闸只做一件事：
读取本端实物 → 与基准／审批册／检查凭据比对 → 返回 (ok, 一句话证据)。
判据口径全部写在 z11／z12.json 的条款正文里，本文件只是执行端；
改判据必须先改条款并同轮改本文件，否则 B9／A12 的接线核对会先报红。

约定：
- 本端审批册固定为 30_taizhang/qiangzhi_shenpi.txt，不与任何他端审批册混读。
- 基线固定为 30_taizhang/core_baseline.json，由本文件 rebuild_baseline() 生成；
  生成时要求审批册当日条目点名每个 approved_files 成员。
- 检查凭据固定为 30_taizhang/check_last.json，只由 engine.py 调
  rules_db.record_check_result() 写入，本文件只读不写。
"""

import fnmatch
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PRODUCT = os.path.dirname(HERE)            # 本仓根目录
REPO = PRODUCT                             # 本仓根目录（kernel/ 与 10_rac/ 同级）
ZH = os.path.join(HERE, "zhunze")
META = os.path.join(PRODUCT, "00_meta", "meta.json")
MAPF = os.path.join(PRODUCT, "00_meta", "jiancha_map.json")
GATES_DECL = os.path.join(PRODUCT, "00_meta", "gates_decl.json")
LEDGER = os.path.join(PRODUCT, "30_taizhang")
VIEW = os.path.join(PRODUCT, "20_view")
WEB = os.path.join(VIEW, "web")
KROOT = os.path.join(REPO, "kernel")
KCORE = os.path.join(KROOT, "bumao_core")
CONTRACT = os.path.join(KROOT, "kernel_contract.json")
BASELINE = os.path.join(LEDGER, "core_baseline.json")
APPROVAL = os.path.join(LEDGER, "qiangzhi_shenpi.txt")
CHECK_LAST = os.path.join(LEDGER, "check_last.json")
TOKEN_BASELINE = os.path.join(PRODUCT, "00_meta", "frontend_token_baseline.json")
BIANGENG = os.path.join(LEDGER, "biangeng_zhang.txt")
BACKUP_DIR = os.path.join(REPO, "90_lishi", "gongkai_weihu_261107")
# B16 新增件分支：基线建立后新增件（old_sha 为空）改为验「首次入库登记」四要素。
FIRST_ENTRY = os.path.join(LEDGER, "shouci_ruku_dengji.txt")
# B29 读的预告文件（由 kernel/suoding.py unlock 自动追加，也可手写）。
YUGAO = os.path.join(WEB, "gaigai_yugao.txt")
# B29 豁免：运行期遥测文件，由检查自身写盘，不属「人改核心件」，天然没有预告行。
YUGAO_EXEMPT = ("check_last.json", "saojian_zuijin.json")

# B25 的私人端专属标识清单。改清单须同轮改 12.4 条款正文并登记检查项。
# 本文件自身参与公开件扫描，故 PUBLIC 集合显式排除本文件与测试件（否则自匹配）。
PRIVATE_TOKENS = ("BUMA" + "OSI", "Buma" + "go", "00_PRO" + "FILE", "zhiwo_" + "jinhua", "riji")

RE_SPDX = re.compile(r"SPDX-License-Identifier:\s*Apache-2\.0")
RE_CORE_VER = re.compile(r"^CORE_VERSION\s*=\s*[\"']([^\"']+)[\"']", re.M)
RE_CORE_ASSIGN = re.compile(r"^CORE_VERSION\s*=", re.M)
_SEP = chr(92) + chr(92)   # 正则里的字面反斜杠；拆开拼装避免本文件被 B6/B7 误判为盘符路径
RE_WINUSER = re.compile("C" + ":" + _SEP + "Users" + _SEP + r"([^\\/\s\"'）|]+)")
PLACEHOLDER_USERS = frozenset({"你", "用户", "用户名", "<user>", "<用户>", "<username>"})
SOURCE_VALUES = ("用户指令", "脚本", "上游同步", "人工")
NOTICE_FORBIDDEN = ("禁止商用", "仅限个人", "非商业", "附加条款")


def _sha(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return ""


def _read(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except OSError:
        return ""


def _json(path):
    try:
        return json.loads(_read(path))
    except Exception:
        return None


def _rel(path):
    return os.path.relpath(path, REPO).replace("\\", "/")


def _mdate(path):
    try:
        return time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))
    except OSError:
        return ""


def _today():
    return time.strftime("%Y-%m-%d", time.localtime())


def _clauses():
    out = []
    for fn in sorted(os.listdir(ZH)):
        if not re.match(r"^z\d{2}\.json$", fn):
            continue
        doc = _json(os.path.join(ZH, fn)) or {}
        for c in doc.get("clauses") or []:
            c = dict(c)
            c["_file"] = fn
            out.append(c)
    return out


def _rules_sha():
    h = hashlib.sha256()
    for fn in sorted(os.listdir(ZH)):
        if re.match(r"^z\d{2}\.json$", fn):
            with open(os.path.join(ZH, fn), "rb") as f:
                h.update(f.read())
    return h.hexdigest()


def _manifest_files():
    doc = _json(os.path.join(WEB, "core_manifest.json")) or {}
    return sorted((doc.get("files") or {}).keys())


def _kernel_files():
    fs = []
    if os.path.isdir(KCORE):
        fs += [os.path.join(KCORE, f) for f in sorted(os.listdir(KCORE))
               if f.endswith(".py")]
    for extra in (os.path.join(KROOT, "contract_test.py"), CONTRACT):
        if os.path.isfile(extra):
            fs.append(extra)
    return fs


def _tracked_files():
    fs = [os.path.join(WEB, f) for f in _manifest_files() if os.path.isfile(os.path.join(WEB, f))]
    fs += _kernel_files()
    fs += [os.path.join(ZH, f) for f in sorted(os.listdir(ZH)) if re.match(r"^z\d{2}\.json$", f)]
    return fs


def _baseline():
    doc = _json(BASELINE)
    if not isinstance(doc, dict) or not isinstance(doc.get("files"), dict):
        return None
    return doc


def _approval_text():
    return _read(APPROVAL)


def _approval_hits(filename, date):
    try:
        import gate_registry as _gr
    except ImportError:
        sys.path.insert(0, KCORE)
        import gate_registry as _gr
    return _gr.approval_covers_file(_approval_text(), date, filename)


def _changed(prefix=None):
    """相对基线的改动文件（缺失也算改动）。prefix 限定相对路径前缀。"""
    base = _baseline()
    if base is None:
        return None
    out = []
    for rel, old in sorted(base["files"].items()):
        if prefix and not rel.startswith(prefix):
            continue
        cur = _sha(os.path.join(REPO, rel.replace("/", os.sep)))
        if cur != old:
            out.append((rel, old, cur))
    for rel in _tracked_files():
        r = _rel(rel)
        if prefix and not r.startswith(prefix):
            continue
        if r not in base["files"]:
            out.append((r, "", _sha(rel)))
    return out


def _backup_with_sha(basename, want_sha):
    """90_lishi 备份区里是否有同名改前件且哈希等于基准值。"""
    if not os.path.isdir(BACKUP_DIR) or not want_sha:
        return ""
    stem = os.path.splitext(basename)[0]
    for name in sorted(os.listdir(BACKUP_DIR)):
        p = os.path.join(BACKUP_DIR, name)
        if not os.path.isfile(p):
            continue
        if stem not in name:
            continue
        if _sha(p) == want_sha:
            return name
    return ""


def _first_entry(basename):
    """新增件的「首次入库登记」：创建时间／首版 sha256／入库时间／经办人 四要素齐才算数。

    仅在 old_sha 为空（基线里根本没有该件）时使用。缺任一要素或哈希不符都返回 None，
    由调用方判红；old_sha 非空的件一律走同哈希改前件，不套用本分支。
    """
    doc = _json(FIRST_ENTRY)
    if not isinstance(doc, dict):
        return None
    for it in doc.get("items") or []:
        if not isinstance(it, dict):
            continue
        name = str(it.get("file") or "").strip()
        path = str(it.get("path") or "").replace("\\", "/")
        if name != basename and os.path.basename(path) != basename:
            continue
        if not all(str(it.get(k) or "").strip()
                   for k in ("created_at", "first_sha256", "registered_at", "handler")):
            continue
        return it
    return None


def _b16_bad(ch):
    """B16 判定：老件验同哈希改前件；基线后新增件验首次入库登记。"""
    bad = []
    for rel, old, cur in ch:
        fn = os.path.basename(rel)
        if old:
            if not _backup_with_sha(fn, old):
                bad.append(rel)
            continue
        rec = _first_entry(fn)
        if not rec or str(rec.get("first_sha256") or "").strip().lower() != cur:
            bad.append(rel)
    return bad


def _today_ledger_block():
    """取当日条目的整段（日期行＋其后的续行），而不是只看日期行。

    2026-11-07 修：台账把「来源：」写在日期行的续行里，只比对日期行会漏判。
    续行到空行或下一条日期行为止；跨条目拼接仍然禁止。
    """
    text = _read(BIANGENG)
    today = _today()
    lines = text.splitlines()
    blocks, cur = [], None
    for ln in lines:
        if re.match(r"^\d{4}-\d{2}-\d{2}\s*\|", ln):
            cur = [ln]
            blocks.append(cur)
        elif cur is not None:
            if not ln.strip():
                cur = None
            else:
                cur.append(ln)
    hits = [b for b in blocks if b[0].startswith(today)]
    flat = [ln.strip() for b in hits for ln in b]
    return today, flat, text


def _baseline_signature_ok():
    """基线自身的签字核对：approved_files 每个成员须在 updated_at 当日被点名授权。"""
    base = _baseline()
    if base is None:
        return False, "基线缺失或不可解析：%s" % BASELINE
    day = str(base.get("updated_at") or "")
    if not day:
        return False, "基线缺 updated_at"
    for fn in base.get("approved_files") or []:
        if not _approval_hits(fn, day):
            return False, "基线自签失败：%s 在 %s 的审批条目里未被点名授权" % (fn, day)
    return True, "基线自签 %d 个文件，审批册 %s" % (len(base.get("approved_files") or []), os.path.basename(APPROVAL))


# ── B15 强制-01 改核心件前必须有审批记录 ──────────────────────────────
def gate_b15():
    ch = _changed("community/20_view/web/")
    if ch is None:
        return False, "缺基线 %s，无法判定核心件是否被改动" % BASELINE
    bad = []
    for rel, old, cur in ch:
        fn = os.path.basename(rel)
        if not _approval_hits(fn, _mdate(os.path.join(REPO, rel.replace("/", os.sep)))):
            bad.append(rel)
    if bad:
        return False, "未审批改动核心件 %d 件：%s（审批册 %s）" % (
            len(bad), str([os.path.basename(x) for x in bad[:5]]), APPROVAL)
    return True, "20_view/web 核心件相对基线 %d 件改动，均有当日点名审批" % len(ch)


# ── B16 强制-02 每次改动必须留痕 ─────────────────────────────────────
def gate_b16():
    ch = _changed()
    if ch is None:
        return False, "缺基线 %s，无法判定留痕" % BASELINE
    bad = _b16_bad(ch)
    if bad:
        return False, "已改动但无同哈希改前件／新增件入库登记不合规 %d 件：%s（备份区 %s；登记 %s）" % (
            len(bad), str(bad[:5]), BACKUP_DIR, FIRST_ENTRY)
    return True, "相对基线改动 %d 件，改前件哈希全部可对上或新增件四要素齐且哈希一致" % len(ch)


# ── B17 强制-03 必须声明改动来源 ─────────────────────────────────────
def gate_b17():
    day, rows, _ = _today_ledger_block()
    src = [ln for ln in rows if "来源：" in ln]
    if not src:
        return False, "变更台账 %s 无当日（%s）条目或缺「来源：」字段" % (BIANGENG, day)
    vals = [ln.split("来源：", 1)[1].split("|")[0].strip() for ln in src]
    good = [v for v in vals if any(v.startswith(s) for s in SOURCE_VALUES)]
    if not good:
        return False, "当日「来源：」取值越界：%s（只认 %s）" % (str(vals[:3]), "/".join(SOURCE_VALUES))
    return True, "当日来源声明 %d 条：%s" % (len(good), good[0][:40])


# ── B18 强制-04 版本号必须来自单一来源 ───────────────────────────────
def gate_b18():
    meta = _json(META) or {}
    ver = str(meta.get("version") or "")
    if not ver:
        return False, "meta.json 缺 version，版本单点不成立"
    bad = []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith(".py"):
            continue
        text = _read(os.path.join(HERE, fn))
        if re.search(r"(?<![\d.])%s(?![\d.])" % re.escape(ver), text):
            bad.append("10_rac/" + fn)
    for c in _clauses():
        text = c.get("title", "") + "\n" + "\n".join(c.get("body") or [])
        if re.search(r"(?<![\d.])%s(?![\d.])" % re.escape(ver), text):
            bad.append("zhunze/%s:%s" % (c.get("_file", ""), c.get("id", "")))
    core = os.path.join(WEB, "xtgl_core.py")
    text = _read(core)
    if len(RE_CORE_ASSIGN.findall(text)) != 1:
        bad.append("xtgl_core.py:CORE_VERSION 赋值出现 %d 次（应 1 次）"
                   % len(RE_CORE_ASSIGN.findall(text)))
    m = RE_CORE_VER.search(text)
    man = str((_json(os.path.join(WEB, "core_manifest.json")) or {}).get("core_version") or "")
    if m and man and m.group(1) != man:
        bad.append("core_manifest.core_version=%s ≠ CORE_VERSION=%s" % (man, m.group(1)))
    if bad:
        return False, "版本单点被破坏：%s" % str(bad[:5])
    return True, "产品版本只在 meta.json；CORE_VERSION 赋值 1 次且清单镜像一致"


# ── B19 强制-05 必须跑完检查才准落盘 ────────────────────────────────
def gate_b19():
    rec = _json(CHECK_LAST)
    if not isinstance(rec, dict):
        return False, "缺检查凭据 %s（改动后尚未跑完整检查）" % CHECK_LAST
    if str(rec.get("rules_sha") or "") != _rules_sha():
        return False, "检查凭据过期：真身已改动，上一轮凭据 rules_sha 不匹配"
    try:
        a_items = int(rec.get("a_items") or 0)
        b_items = int(rec.get("b_items") or 0)
    except (TypeError, ValueError):
        a_items, b_items = 0, 0
    exp = (len((_json(GATES_DECL) or {}).get("expected") or []))
    if a_items < 11 or b_items != exp:
        return False, "检查项数不完整：A=%d（≥11）／B=%d（应 %d）" % (a_items, b_items, exp)
    if not str(rec.get("finished_at") or ""):
        return False, "检查凭据缺 finished_at"
    return True, "凭据与当前真身同哈希，A=%d／B=%d，完成于 %s" % (
        a_items, b_items, rec.get("finished_at"))


# ── B20 强制-06 必须台账登记 ────────────────────────────────────────
def gate_b20():
    ids = set(c.get("id") for c in _clauses())
    covered = set()
    for v in ((_json(MAPF) or {}).get("map") or {}).values():
        covered |= set(v.get("covers") or [])
    miss = sorted(ids - covered)
    day, rows, _ = _today_ledger_block()
    lvl = [ln for ln in rows if ("L2" in ln or "L3" in ln)]
    msg = []
    if miss:
        msg.append("未登记检查项的条款 %d 条：%s" % (len(miss), str(miss[:5])))
    if not lvl:
        msg.append("变更台账无当日（%s）L2／L3 记账" % day)
    if msg:
        return False, "；".join(msg)
    return True, "条款登记 %d／%d，当日 L2／L3 记账 %d 条" % (len(ids), len(ids), len(lvl))


# ── B21 限制-01 不得擅自改 CORE_VERSION ─────────────────────────────
def gate_b21():
    text = _read(os.path.join(WEB, "xtgl_core.py"))
    n = len(RE_CORE_ASSIGN.findall(text))
    m = RE_CORE_VER.search(text)
    if n != 1 or not m:
        return False, "xtgl_core.py 的 CORE_VERSION 赋值 %d 次（应 1 次且可取值）" % n
    val = m.group(1)
    man = str((_json(os.path.join(WEB, "core_manifest.json")) or {}).get("core_version") or "")
    con = str((((_json(CONTRACT) or {}).get("frozen_interfaces") or {}).get("core_version") or {})
              .get("current_value") or "")
    bad = []
    if not man or man != val:
        bad.append("清单=%s" % man)
    if con and con != val:
        bad.append("契约=%s" % con)
    if bad:
        return False, "CORE_VERSION=%s 与 %s 不一致" % (val, "／".join(bad))
    return True, "CORE_VERSION=%s：代码 1 处、清单与契约一致" % val


# ── B22 限制-02 不得绕过闸门直接改核心件 ────────────────────────────
def gate_b22():
    rec = _json(CHECK_LAST) or {}
    fin = str(rec.get("finished_at") or "")
    try:
        fin_ts = time.mktime(time.strptime(fin, "%Y-%m-%d %H:%M:%S"))
    except Exception:
        return False, "无有效检查完成时刻（凭据 %s），无法判定是否绕过闸门" % CHECK_LAST
    bad = []
    for p in _tracked_files():
        try:
            mt = os.path.getmtime(p)
        except OSError:
            continue
        if mt <= fin_ts:
            continue
        if _approval_hits(os.path.basename(p), _mdate(p)):
            continue
        bad.append(_rel(p))
    if bad:
        return False, "改动时间晚于上轮检查且无当日审批 %d 件：%s" % (len(bad), str(bad[:5]))
    return True, "受管文件 %d 件均不晚于检查完成时刻 %s" % (len(_tracked_files()), fin)


def _public_files():
    fs = []
    for root in (PRODUCT, REPO):
        for fn in ("LICENSE", "NOTICE", "TRADEMARK.md", "CONTRIBUTING.md",
                   "README.md", "DCO", "README-HX.txt"):
            p = os.path.join(root, fn)
            if os.path.isfile(p) and p not in fs:
                fs.append(p)
    for fn in sorted(os.listdir(os.path.dirname(META))):
        p = os.path.join(os.path.dirname(META), fn)
        if os.path.isfile(p) and fn.endswith((".md", ".txt", ".json")) and fn != "pii_words.json":
            fs.append(p)
    fs += [os.path.join(ZH, f) for f in sorted(os.listdir(ZH)) if f.endswith(".json")]
    fs += [os.path.join(HERE, f) for f in sorted(os.listdir(HERE))
           if f.endswith(".py") and f not in ("qiangzhi.py", "test_qiangzhi.py")]
    fs += [os.path.join(VIEW, f) for f in sorted(os.listdir(VIEW)) if f.endswith(".txt")]
    return fs


# ── B23 限制-03 不得把本机路径、执行者代号写进公开件 ─────────────────
def gate_b23():
    words = []
    for k in ("USERNAME", "USER", "COMPUTERNAME", "HOSTNAME", "USERPROFILE", "HOME"):
        v = os.environ.get(k) or ""
        if len(v) >= 4:
            words.append(v)
    words = sorted(set(words))
    bad = []
    for p in _public_files():
        text = _read(p)
        for w in words:
            if w in text:
                bad.append("%s:env_id(%s)" % (os.path.basename(p), w))
        for m in RE_WINUSER.finditer(text):
            if m.group(1) in PLACEHOLDER_USERS or m.group(1).startswith("<"):
                continue
            bad.append("%s:winuser(%s)" % (os.path.basename(p), m.group(1)))
    if bad:
        return False, "公开件命中本机标识 %d 处：%s" % (len(bad), str(bad[:5]))
    return True, "公开件 %d 件，本机标识零命中" % len(_public_files())


# ── B24 限制-04 不得未审批改动内核 ───────────────────────────────────
def gate_b24():
    ch = _changed("kernel/")
    if ch is None:
        return False, "缺基线 %s，无法判定内核改动" % BASELINE
    bad = []
    for rel, old, cur in ch:
        fn = os.path.basename(rel)
        if not _approval_hits(fn, _mdate(os.path.join(REPO, rel.replace("/", os.sep)))):
            bad.append(rel)
    if bad:
        return False, "未审批改动内核 %d 件：%s（审批册 %s）" % (
            len(bad), str([os.path.basename(x) for x in bad[:5]]), APPROVAL)
    return True, "内核相对基线改动 %d 件，均有当日点名审批" % len(ch)


# ── B25 限制-05 不得把私人端内容带进开源件 ──────────────────────────
def gate_b25():
    bad = []
    for p in _public_files():
        text = _read(p)
        for tok in PRIVATE_TOKENS:
            if tok in text:
                bad.append("%s:%s" % (os.path.basename(p), tok))
    if bad:
        return False, "公开件命中私人端标识 %d 处：%s" % (len(bad), str(bad[:5]))
    return True, "公开件 %d 件，私人端标识零命中" % len(_public_files())


# ── B26 限制-06 不得自造许可条款 ────────────────────────────────────
def gate_b26():
    root_lic = os.path.join(PRODUCT, "LICENSE")
    rac_lic = os.path.join(HERE, "LICENSE")
    bad = []
    if not os.path.isfile(root_lic):
        bad.append("仓根 LICENSE 缺失")
    else:
        t = _read(root_lic)
        if "Apache License" not in t or "Version 2.0" not in t:
            bad.append("仓根 LICENSE 非 Apache-2.0 原文")
        if os.path.isfile(rac_lic) and _sha(rac_lic) != _sha(root_lic):
            bad.append("10_rac/LICENSE 与仓根 LICENSE 字节不同")
    extra = [f for f in os.listdir(PRODUCT)
             if os.path.isfile(os.path.join(PRODUCT, f)) and f.upper().startswith("LICENSE")
             and f.upper() != "LICENSE"]
    if extra:
        bad.append("仓根出现自造许可文件：%s" % str(extra[:3]))
    notice = _read(os.path.join(PRODUCT, "NOTICE"))
    for w in NOTICE_FORBIDDEN:
        if w in notice:
            bad.append("NOTICE 含附加限制词：%s" % w)
    for p in [os.path.join(HERE, f) for f in sorted(os.listdir(HERE)) if f.endswith(".py")] + \
             [os.path.join(WEB, f) for f in sorted(os.listdir(WEB)) if f.endswith(".py")]:
        if not RE_SPDX.search(_read(p)):
            bad.append("%s 缺 SPDX Apache-2.0" % os.path.basename(p))
    if bad:
        return False, "；".join(bad[:5])
    return True, "LICENSE Apache-2.0 原文、双份同哈希、发布脚本 SPDX 齐全、NOTICE 无附加限制"


# ── B27 强制-07 整份工程可迁移（静态判据） ─────────────────────────────
RE_ABS_DRIVE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:\\")
RE_USERS = re.compile(r"[\\/]Users[\\/]")
RE_PYABS = re.compile(r"(?i)[A-Za-z]:\\[^\s\"']*python\.exe")


def _port_scope():
    files = []
    for root in (HERE, WEB):
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in ("__pycache__", "90_lishi", "assets")]
            for fn in fns:
                if ".bak" in fn or fn.startswith("test_"):
                    continue
                if fn.endswith((".py", ".md", ".bat", ".html", ".css", ".js")):
                    files.append(os.path.join(dp, fn))
    return files


def gate_b27():
    bad = []
    for p in _port_scope():
        for i, ln in enumerate(_read(p).splitlines(), 1):
            for tag, rx in (("盘符绝对路径", RE_ABS_DRIVE),
                            ("用户目录", RE_USERS),
                            ("解释器绝对路径", RE_PYABS)):
                m = rx.search(ln)
                if m:
                    bad.append("%s:%d %s %s" % (os.path.basename(p), i, tag, m.group(0)))
    if bad:
        return False, "写死路径 %d 处：%s" % (len(bad), "；".join(bad[:5]))
    return True, "发布件与活区无写死盘符／用户目录／解释器路径（扫 %d 件）" % len(_port_scope())


# ── B28 强制-08 前端只用既有 token（存量登记＋增量管控） ────────────────
RE_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RE_FONT = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", re.I)


def _token_sets():
    raw = json.dumps(_json(os.path.join(WEB, "design_tokens.json")), ensure_ascii=False)
    colors = set(c.lower() for c in RE_HEX.findall(raw))
    fonts = set(re.findall(r"(?i)\b(\d+(?:\.\d+)?)px", raw))
    base = _json(TOKEN_BASELINE) if os.path.isfile(TOKEN_BASELINE) else {}
    return colors, fonts, base


def token_violations():
    colors, fonts, base = _token_sets()
    bfiles = (base.get("files") or {})
    bad = []
    for fn in ("index.html", "setup.html", "tutorial.html"):
        p = os.path.join(WEB, fn)
        if not os.path.isfile(p):
            continue
        entry = bfiles.get(fn) or {}
        allow_c = colors | set(entry.get("colors") or [])
        allow_f = fonts | set(entry.get("font_px") or [])
        for i, ln in enumerate(_read(p).splitlines(), 1):
            for c in RE_HEX.findall(ln):
                if c.lower() not in allow_c:
                    bad.append("%s:%d 色值 %s 不在 token" % (fn, i, c))
            for v in RE_FONT.findall(ln):
                if v not in allow_f:
                    bad.append("%s:%d 字号 %spx 不在 token" % (fn, i, v))
    return bad


def gate_b28():
    bad = token_violations()
    if bad:
        return False, "字面值越界 %d 处：%s" % (len(bad), "；".join(bad[:5]))
    return True, "三页字面色值与 px 字号均在 tokens＋存量基线内"


# ── B29 强制-07 核心件改动必须先落预告行，且可被第三方复核 ─────────────
def _yugao_minutes(text):
    """把「预计多久」解析成分钟数。认 60／60m／1h／90分钟／2小时；解析不出按 60。"""
    t = str(text or "").strip().lower()
    m = re.search(r"(\d+(?:\.\d+)?)", t)
    if not m:
        return 60
    n = float(m.group(1))
    if "h" in t or "小时" in t or "钟头" in t:
        return int(n * 60)
    return int(n)


def _yugao_rows():
    """解析预告行：时间｜改哪几件｜为什么｜预计多久｜影响面｜执行方。

    只认六段齐全、首段可解析成时刻的行；# 开头与空行跳过。
    """
    rows = []
    for ln in _read(YUGAO).splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [p.strip() for p in s.split("|")]
        if len(parts) < 6:
            continue
        try:
            t = time.mktime(time.strptime(parts[0], "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            continue
        files = [f for f in re.split(r"[,，、\s]+", parts[1]) if f]
        rows.append({"t": t, "files": files, "minutes": _yugao_minutes(parts[3]),
                     "impact": parts[4], "who": parts[5], "raw": s})
    return rows


def _yugao_covers(fn, mtime, base_time, rows):
    """某核心件的 mtime 是否有「对应」预告行。

    对应＝三件事同时成立（判据写死，换人复跑结论一致）：
      ① 文件名出现在「改哪几件」字段（按逗号等分隔后精确匹配，允许 * 通配）；
      ② 预告时刻落在 [基线时刻, 文件 mtime] 之间（预告必须先于改动，允许 120 秒时钟偏差）；
      ③ 文件 mtime 不晚于「预告时刻＋预计时长＋10 分钟宽限」（防一条旧预告长期有效）。
    """
    for r in rows:
        if r["t"] < base_time - 120 or r["t"] > mtime + 120:
            continue
        if mtime > r["t"] + r["minutes"] * 60 + 600:
            continue
        if any(fnmatch.fnmatch(fn, pat) for pat in r["files"]):
            return True
    return False


def gate_b29():
    if not os.path.isfile(BASELINE):
        return False, "缺基线 %s，无法判定核心件是否晚于基线" % BASELINE
    base_time = os.path.getmtime(BASELINE)
    rows = _yugao_rows()
    bad = []
    for fn in _manifest_files():
        if fn in YUGAO_EXEMPT:
            continue
        p = os.path.join(WEB, fn)
        if not os.path.isfile(p):
            continue
        if os.path.getmtime(p) <= base_time:
            continue
        if _yugao_covers(fn, os.path.getmtime(p), base_time, rows):
            continue
        bad.append(fn)
    if bad:
        return False, "核心件 mtime 晚于基线且无对应预告行 %d 件：%s（预告文件 %s）" % (
            len(bad), str(bad[:5]), YUGAO)
    return True, "核心件均不晚于基线或有对应预告行（预告行 %d 条，基线 %s）" % (
        len(rows), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(base_time)))


def write_token_baseline():
    """把当前三页的存量字面值登记为基线（只登记存量，不放宽新增判据）。"""
    colors, fonts, base = _token_sets()
    files = {}
    for fn in ("index.html", "setup.html", "tutorial.html"):
        p = os.path.join(WEB, fn)
        if not os.path.isfile(p):
            continue
        s = _read(p)
        files[fn] = {
            "colors": sorted(set(c.lower() for c in RE_HEX.findall(s)) - colors),
            "font_px": sorted(set(RE_FONT.findall(s)) - fonts),
        }
    doc = {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
           "source": "design_tokens.json + 存量字面值登记",
           "rule": "新增色值／字号必须先进 design_tokens.json；本文件只记存量，不放宽新增",
           "files": files}
    with open(TOKEN_BASELINE, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    return TOKEN_BASELINE


# ── 基线重建（需当日审批点名每个 approved_files） ─────────────────────
def rebuild_baseline(approved_files=None, day=None):
    """重建基线。approved_files 指本次相对旧基线被批准改动的文件 basename。

    返回 (ok, msg)。没有审批点名就不写文件——基线刷新本身也是改核心件的入口，
    不能由执行端无凭据自助完成。
    """
    day = day or _today()
    approved_files = list(approved_files or [])
    missing = [fn for fn in approved_files if not _approval_hits(fn, day)]
    if missing:
        return False, "拒绝重建基线：%s 在 %s 审批条目中未被点名授权" % (str(missing), day)
    files = {}
    for p in _tracked_files():
        files[_rel(p)] = _sha(p)
    doc = {
        "updated_at": day,
        "approval": os.path.basename(APPROVAL),
        "approved_files": approved_files,
        "files": files,
    }
    with open(BASELINE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return True, "基线已重建：%d 件，签字文件 %d 件" % (len(files), len(approved_files))


def main(argv=None):
    argv = argv or sys.argv[1:]
    if argv and argv[0] == "baseline":
        ok, msg = rebuild_baseline(sys.argv[2:] if len(sys.argv) > 2 else [])
        print(msg)
        return 0 if ok else 1
    if argv and argv[0] == "token-baseline":
        print("已登记存量 token 基线：%s" % write_token_baseline())
        return 0
    print("qiangzhi.py: B15—B28 由 BumaoXTGL_Community_v01.py check --strict 调用")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
