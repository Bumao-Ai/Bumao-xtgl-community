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

"""render.py —— 真身 → 视图 渲染器（Bumao XTGL Community）
定位（1.2）：zhunze\\z*.json 是唯一真身；本模块把它渲染成人类可读视图。
去私人化改动：视图单源落在 <工程域>\\20_view\\，不再向任何域外目录写入，
因此整个工程域可整体拷贝至任意机器运行。
视图清单（全部由本模块生成，禁止手改）：
  <工程域>\\20_view\\di*.txt            人读分章
  <工程域>\\20_view\\mulu.txt           章节目录
  <工程域>\\20_view\\quanwen_<版本>.txt 全文归档
版本号只存在于 00_meta\\meta.json 一处，渲染时注入；视图里出现硬编码版本号即 FAIL。
"""
import os, io, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
HX = os.path.dirname(HERE)
META = os.path.join(HX, "00_meta", "meta.json")
ZH = os.path.join(HERE, "zhunze")
VIEW = os.path.join(HX, "20_view")


def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def meta_load():
    return json.loads(rd(META))


def zhang_load():
    fs = sorted([f for f in os.listdir(ZH) if re.match(r"^z\d{2}\.json$", f)])
    return [json.loads(rd(os.path.join(ZH, f))) for f in fs]


def mulu_load():
    p = os.path.join(ZH, "_mulu.json")
    return json.loads(rd(p)) if os.path.exists(p) else None


def head_of(z, meta):
    """分章首行由 meta 注入，数据里不存版本号"""
    return "来源：%s %s 第%d章" % (meta["name"], meta["version"], z["ch"])


def flat(z):
    out = [z["chapter_title"]] + list(z.get("pre", []))
    for c in z["clauses"]:
        out.append(c["title"])
        out.extend(c["body"])
    return out


def render_di(z, meta):
    body = flat(z)
    if not body or body[-1] != "":
        body = body + [""]
    return "\n".join([head_of(z, meta), ""] + body)


def render_quanwen(zs, meta):
    blocks = []
    for z in zs:
        b = flat(z)
        while b and b[-1] == "":
            b.pop()
        blocks.append("\n".join(b))
    return "\n\n".join(blocks) + "\n"


def render_mulu(zs, meta, m):
    rows = []
    for z in zs:
        k = m["rows"][str(z["ch"])] if m and str(z["ch"]) in m.get("rows", {}) else None
        if not k:
            k = {"name": z["chapter_title"], "keys": "", "sum": ""}
        rows.append("%d | %s | %s | %s | %s" % (
            z["ch"], k["name"], k["keys"], z["file"], k["sum"]))
    rows.append("当前版本：%s | 产品名：%s | 全文归档：quanwen_%s.txt"
                % (meta["version"], meta["name"], meta["version"]))
    return "\n".join(rows) + "\n"


def targets(meta, zs=None):
    zs = zs or zhang_load()
    t = []
    for z in zs:
        t.append((os.path.join(VIEW, z["file"]), render_di(z, meta)))
    t.append((os.path.join(VIEW, "mulu.txt"), render_mulu(zs, meta, mulu_load())))
    t.append((os.path.join(VIEW, "quanwen_%s.txt" % meta["version"]),
              render_quanwen(zs, meta)))
    return t


def write_all():
    import lock
    meta = meta_load()
    rid = lock.acquire("render")
    try:
        n = 0
        for p, s in targets(meta):
            wr(p, s)
            n += 1
        return n
    finally:
        lock.release(rid)


def check_drift():
    """返回不一致的视图路径列表（空 = 全部同步）"""
    meta = meta_load()
    bad = []
    for p, s in targets(meta):
        if not os.path.exists(p) or rd(p) != s:
            bad.append(p)
    return bad


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    m = meta_load()
    if len(sys.argv) > 1 and sys.argv[1] == "write":
        n = write_all()
        print("渲染写入 %d 个视图（%s %s）" % (n, m["name"], m["version"]))
    else:
        d = check_drift()
        print("视图漂移 %d 处" % len(d))
        for x in d[:10]:
            print("  - " + x)
