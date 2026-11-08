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

"""rules_db.py —— 真身装载与结构校验（Bumao XTGL Community）
定位（1.2）：zhunze\\z*.json 是唯一真身。本模块只读真身、只做校验与派生索引，
不定义规则、不持有第二份正文。
去私人化要求：所有路径由 __file__ 运行时溯源，不写字面绝对路径，产品可整体拷贝。
输出：rules.json（派生索引，可随时重建；真身一变它就该重建）
"""
import os, io, re, sys, json, hashlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
HX = os.path.dirname(HERE)
ZH = os.path.join(HERE, "zhunze")
META = os.path.join(HX, "00_meta", "meta.json")
VIEW = os.path.join(HX, "20_view")
LEDGER_DIR = os.path.join(HX, "30_taizhang")
DB = os.path.join(HERE, "rules.json")

REF = re.compile(r"(?:按|见|依|据|照|走|见第)\s*(\d{1,2}\.\d{1,2}(?:\.\d{1,2}){0,2})")
REF2 = re.compile(r"(?<![0-9.])（(\d{1,2}\.\d{1,2}(?:\.\d{1,2}){0,2})）")


def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def zhang_files():
    if not os.path.isdir(ZH):
        return []
    return sorted([f for f in os.listdir(ZH) if re.match(r"^z\d{2}\.json$", f)])


def load():
    meta = json.loads(rd(META)) if os.path.exists(META) else {}
    chapters, clauses = [], []
    for f in zhang_files():
        z = json.loads(rd(os.path.join(ZH, f)))
        chapters.append({"ch": z["ch"], "file": z["file"],
                         "chapter_title": z["chapter_title"],
                         "n": len(z["clauses"]), "json": f})
        for c in z["clauses"]:
            c2 = dict(c)
            c2["ch"] = z["ch"]
            clauses.append(c2)
    return {"meta": meta, "chapters": chapters, "clauses": clauses}


def index(db):
    """补 refs / broken_refs / nbody"""
    ids = set(c["id"] for c in db["clauses"])
    roots = set(c["root"] for c in db["clauses"])
    for c in db["clauses"]:
        text = c["title"] + "\n" + "\n".join(c["body"])
        refs = set(REF.findall(text)) | set(REF2.findall(text))
        c["refs"] = sorted(r for r in refs if r in ids or r in roots)
        c["broken_refs"] = sorted(r for r in refs if r not in ids and r not in roots)
        c["nbody"] = len([x for x in c["body"] if x.strip()])
    return db


def dup_ids(db):
    seen, dup = set(), []
    for c in db["clauses"]:
        if c["id"] in seen:
            dup.append(c["id"])
        seen.add(c["id"])
    return dup


def block_broken(clauses):
    """同一 root 的条款必须连续出现且主条在最前"""
    pos, bad = {}, []
    for i, c in enumerate(clauses):
        pos.setdefault(c["root"], []).append(i)
    for r, ps in pos.items():
        if ps != list(range(ps[0], ps[0] + len(ps))) or clauses[ps[0]]["id"] != r:
            bad.append(r)
    return sorted(bad)


def shell_clauses(db):
    """标题以「：」结尾、自身无正文、且没有任何子条款承接的条款。"""
    kids = [c["id"] for c in db["clauses"]]
    out = []
    for c in db["clauses"]:
        if c["nbody"] > 0 or not c["title"].rstrip().endswith("："):
            continue
        if any(k.startswith(c["id"] + "(") or k.startswith(c["id"] + ".") for k in kids):
            continue
        out.append(c["id"])
    return out


def build_index(db):
    qw = sorted([f for f in os.listdir(VIEW)
                 if f.startswith("quanwen_") and f.endswith(".txt")]) \
        if os.path.isdir(VIEW) else []
    return {
        "schema": 1,
        "product": "Bumao XTGL Community",
        "name": db["meta"].get("name", ""),
        "version": db["meta"].get("version", ""),
        "ssot_files": zhang_files(),
        "n_clauses": len(db["clauses"]),
        "n_chapters": len(db["chapters"]),
        "chapters": [{"ch": c["ch"], "file": c["file"], "n": c["n"]} for c in db["chapters"]],
        "ids": [c["id"] for c in db["clauses"]],
        "quanwen_files": qw,
    }


def save(db):
    idx = build_index(db)
    wr(DB, json.dumps(idx, ensure_ascii=False, indent=1))
    return "%s %s / 条款 %d / 分章 %d" % (idx["name"], idx["version"], idx["n_clauses"], idx["n_chapters"])


def rules_sha():
    """z 系真身合并哈希。B19 与 engine 的检查凭据共用这一算法，避免两套口径。"""
    h = hashlib.sha256()
    for f in zhang_files():
        with open(os.path.join(ZH, f), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()


def enforce_decl():
    """第 11／12 章逐条的「条款 id → 闸位」声明，供 engine 的 A12 接线核对。"""
    out = []
    for f in zhang_files():
        z = json.loads(rd(os.path.join(ZH, f)))
        for c in z.get("clauses") or []:
            g = c.get("gate")
            if g:
                out.append({"clause": c.get("id", ""), "gate": g,
                            "judge": c.get("judge", ""), "file": f})
    return out


def record_check_result(nfail, a_items, b_items, total):
    """每轮 check 结束写凭据；B19 下一轮据此判「跑完检查才准落盘」。

    第二批 R6：凭据同时落受管件内容哈希清单，B22 下一轮按内容划界，不再看 mtime。
    清单随每轮完成的检查落盘，与旧 mtime 划界同一时点，只是判据从时间换成内容。
    """
    doc = {
        "finished_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "rules_sha": rules_sha(),
        "a_items": int(a_items),
        "b_items": int(b_items),
        "total": int(total),
        "nfail": int(nfail),
        "version": json.loads(rd(META)).get("version", "") if os.path.exists(META) else "",
    }
    try:
        import qiangzhi as _qz
        _msha = _qz.managed_sha()
    except Exception:
        _msha = {}
    if _msha:
        doc["managed_sha"] = _msha
    wr(os.path.join(LEDGER_DIR, "check_last.json"),
       json.dumps(doc, ensure_ascii=False, indent=1))
    return doc


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    db = index(load())
    print("装载：" + save(db))
    print("  重复 id %d %s" % (len(dup_ids(db)), dup_ids(db)[:5]))
    bb = block_broken(db["clauses"])
    print("  块断裂 %d %s" % (len(bb), bb[:5]))
    bad = [(c["id"], c["broken_refs"]) for c in db["clauses"] if c["broken_refs"]]
    print("  断链 %d %s" % (len(bad), bad[:5]))
    print("  空壳 %d %s" % (len(shell_clauses(db)), shell_clauses(db)[:5]))
