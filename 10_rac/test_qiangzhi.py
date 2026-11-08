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

"""test_qiangzhi.py —— B15—B26 反向用例（每条至少一例「应当拦截」）

做法：把本端整体复制到临时目录，逐例只破坏一个判据，再调用同一条闸函数。
全部在副本里做，不碰实物审批册／基线／真身；正例另有 1 条「改动+审批+留痕」放行。
运行：python 10_rac/test_qiangzhi.py
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HX = os.path.dirname(HERE)
KCORE = os.path.join(HX, "kernel", "bumao_core")
TODAY = time.strftime("%Y-%m-%d", time.localtime())


def _copy_product(dst):
    shutil.copytree(HX, os.path.join(dst, "community"),
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    # 内核随仓内嵌，已由 copytree 一并复制到 community/kernel/bumao_core。
    for fn in ("LICENSE", "NOTICE", "TRADEMARK.md", "CONTRIBUTING.md",
               "README.md", "DCO", "README-HX.txt"):
        src = os.path.join(HX, fn)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(dst, fn))
    # 副本里的核心件带着只读锁（z11 的 attrib +R），夹具要能破坏判据，先只对副本解锁。
    for dp, _dn, fn in os.walk(dst):
        for n in fn:
            p = os.path.join(dp, n)
            try:
                os.chmod(p, os.stat(p).st_mode | 0o200)
            except OSError:
                pass


def _load(dst):
    kdir = os.path.join(dst, "community", "kernel", "bumao_core")
    if kdir not in sys.path:
        sys.path.insert(0, kdir)
    spec = importlib.util.spec_from_file_location(
        "qz_" + str(abs(hash(dst)))[:8],
        os.path.join(dst, "community", "10_rac", "qiangzhi.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _seed(dst, q):
    led = os.path.join(dst, "community", "30_taizhang")
    os.makedirs(led, exist_ok=True)
    with open(os.path.join(led, "qiangzhi_shenpi.txt"), "w", encoding="utf-8") as f:
        f.write("【第 1 号】%s 09:00:00｜测试夹具\n" % TODAY)
        f.write("性质：授权\n用户批准原文：「测试夹具授权」\n")
    with open(os.path.join(led, "biangeng_zhang.txt"), "w", encoding="utf-8") as f:
        f.write("%s | L2 | 来源：脚本 | 测试夹具\n" % TODAY)
    q.rebuild_baseline([])
    with open(os.path.join(led, "check_last.json"), "w", encoding="utf-8") as f:
        json.dump({"finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "rules_sha": q._rules_sha(), "a_items": 12, "b_items": 28,
                   "total": 40, "nfail": 0}, f)


def _write(p, text):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _append(p, text):
    with open(p, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _approve(dst, filename, day=None):
    p = os.path.join(dst, "community", "30_taizhang", "qiangzhi_shenpi.txt")
    with open(p, "a", encoding="utf-8") as f:
        f.write("\n【第 2 号】%s 10:00:00｜测试放行\n" % (day or TODAY))
        f.write("性质：授权\n范围：%s\n用户批准原文：「测试放行授权」\n" % filename)


def _case(name, mutate, gate):
    dst = tempfile.mkdtemp(prefix="qz_")
    try:
        _copy_product(dst)
        q = _load(dst)
        _seed(dst, q)
        mutate(dst, q)
        ok, detail = getattr(q, gate)()
        return name, (not ok), detail
    finally:
        shutil.rmtree(dst, ignore_errors=True)


def main():
    cases = [
        ("B15 未审批改核心件", lambda d, q: _append(
            os.path.join(d, "community", "20_view", "web", "xtgl_core.py"), "\n# drill\n"), "gate_b15"),
        ("B16 改动无改前件", lambda d, q: _append(
            os.path.join(d, "community", "10_rac", "zhunze", "z00.json"), "\n"), "gate_b16"),
        ("B16 老件不得走新增分支", lambda d, q: _b16_old_with_entry(d, q), "gate_b16"),
        ("B16 新增件登记缺字段", lambda d, q: _b16_new_missing_field(d, q), "gate_b16"),
        ("B17 缺来源声明", lambda d, q: _write(
            os.path.join(d, "community", "30_taizhang", "biangeng_zhang.txt"),
            "%s | L2 | 测试\n" % TODAY), "gate_b17"),
        ("B18 版本字面量外溢", lambda d, q: _append(
            os.path.join(d, "community", "10_rac", "lock.py"),
            "\n# v%s\n" % (json.loads(q._read(q.META)).get("version", ""))), "gate_b18"),
        ("B19 检查凭据过期", lambda d, q: _write(
            os.path.join(d, "community", "30_taizhang", "check_last.json"),
            json.dumps({"finished_at": "2026-01-01 00:00:00", "rules_sha": "0" * 64,
                        "a_items": 12, "b_items": 28})), "gate_b19"),
        ("B20 条款未登记", lambda d, q: _mutate_map(d), "gate_b20"),
        ("B21 擅改 CORE_VERSION", lambda d, q: _set_core_version(d), "gate_b21"),
        ("B22 mtime 晚于检查", lambda d, q: _touch_after_check(d), "gate_b22"),
        ("B23 公开件写本机标识", lambda d, q: _append(
            os.path.join(d, "community", "README.md"),
            "\n" + (os.environ.get("USERNAME") or "LOCALUSER") + "\n"), "gate_b23"),
        ("B24 未审批改内核", lambda d, q: _append(
            os.path.join(d, "community", "kernel", "bumao_core", "bumao_core_rules.py"), "\n# drill\n"), "gate_b24"),
        ("B25 私人端标识混入", lambda d, q: _append(
            os.path.join(d, "community", "README.md"), "\n" + "BUMA" + "OSI" + "\n"), "gate_b25"),
        ("B26 自造许可附加条款", lambda d, q: _append(
            os.path.join(d, "community", "NOTICE"), "\n禁止商用\n"), "gate_b26"),
    ]
    print("反向用例（每条应被拦截）：")
    bad = 0
    for name, mutate, gate in cases:
        try:
            label, caught, detail = _case(name, mutate, gate)
        except Exception as e:
            print("  ERROR %-22s %s: %r" % (name, gate, e))
            bad += 1
            continue
        print("  %s %-22s %s  %s" % ("CAUGHT" if caught else "MISSED", label, gate, detail[:70]))
        if not caught:
            bad += 1
    print("\n放行对照（改动＋审批＋留痕）：")
    try:
        dst = tempfile.mkdtemp(prefix="qz_ok_")
        try:
            _copy_product(dst)
            q = _load(dst)
            _seed(dst, q)
            core = os.path.join(dst, "community", "20_view", "web", "xtgl_core.py")
            old = q._sha(core)
            bak = os.path.join(dst, "community", "90_lishi", "gongkai_weihu_261107")
            os.makedirs(bak, exist_ok=True)
            shutil.copy2(core, os.path.join(bak, "xtgl_core.py.bak_drill"))
            _append(core, "\n# approved drill\n")
            assert q._sha(os.path.join(bak, "xtgl_core.py.bak_drill")) == old
            _approve(dst, "xtgl_core.py")
            newp = os.path.join(dst, "community", "kernel", "bumao_core", "new_ok.py")
            _write(newp, "# ok\n")
            _first_entry_fixture(dst, "new_ok.py", q._sha(newp), complete=True)
            _approve(dst, "new_ok.py")
            r15 = q.gate_b15()
            r16 = q.gate_b16()
            r22 = q.gate_b22()
            print("  %s B15 %s" % ("PASS" if r15[0] else "FAIL", r15[1][:80]))
            print("  %s B16 %s" % ("PASS" if r16[0] else "FAIL", r16[1][:80]))
            print("  %s B22 %s" % ("PASS" if r22[0] else "FAIL", r22[1][:80]))
            if not (r15[0] and r16[0] and r22[0]):
                bad += 1
        finally:
            shutil.rmtree(dst, ignore_errors=True)
    except Exception as e:
        print("  ERROR 放行对照：%r" % e)
        bad += 1
    print("\n结果：%s（%d 条反向用例 + 1 条放行对照）"
          % ("ALL PASS" if bad == 0 else "FAIL %d 项" % bad, len(cases)))
    return 0 if bad == 0 else 1


def _mutate_map(d):
    p = os.path.join(d, "community", "00_meta", "jiancha_map.json")
    doc = json.loads(open(p, encoding="utf-8-sig").read())
    doc["map"].pop("11.0", None)
    _write(p, json.dumps(doc, ensure_ascii=False, indent=1))


def _first_entry_fixture(d, name, sha, complete=True):
    p = os.path.join(d, "community", "30_taizhang", "shouci_ruku_dengji.txt")
    doc = {"_note": "测试夹具", "items": []}
    if os.path.isfile(p):
        doc = json.loads(open(p, encoding="utf-8").read())
    item = {"file": name, "path": name, "created_at": "2026-11-08 06:57:07",
            "first_sha256": sha, "registered_at": "2026-11-08 08:30:00",
            "handler": "测试夹具"}
    if not complete:
        item.pop("registered_at")
    doc["items"].append(item)
    _write(p, json.dumps(doc, ensure_ascii=False, indent=1))


def _b16_old_with_entry(d, q):
    """老件（基线里有旧哈希）即使有一条四要素齐的入库登记，也必须判红。"""
    p = os.path.join(d, "community", "10_rac", "zhunze", "z00.json")
    _append(p, "\n")
    _first_entry_fixture(d, "z00.json", q._sha(p), complete=True)


def _b16_new_missing_field(d, q):
    """新增件（基线里没有）登记缺「入库时间」，必须判红。"""
    p = os.path.join(d, "community", "kernel", "bumao_core", "new_drill.py")
    _write(p, "# drill\n")
    _first_entry_fixture(d, "new_drill.py", q._sha(p), complete=False)


def _set_core_version(d):
    p = os.path.join(d, "community", "20_view", "web", "xtgl_core.py")
    text = open(p, encoding="utf-8-sig").read()
    import re
    text = re.sub(r'(?m)^CORE_VERSION\s*=\s*"[^"]*"', 'CORE_VERSION = "9.9.9"', text, count=1)
    _write(p, text)


def _touch_after_check(d):
    p = os.path.join(d, "community", "10_rac", "zhunze", "z01.json")
    os.utime(p, (time.time() + 3, time.time() + 3))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
