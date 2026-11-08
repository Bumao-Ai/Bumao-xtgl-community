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

"""lock.py —— 单实例运行锁（Bumao XTGL Community）
用途：防止同一脚本被并行跑两遍导致视图互相覆盖。
自清理：超过 STALE 秒数的锁视为残留，自动接管，避免异常退出后永久卡死。
"""
import os, io, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK_FILE = os.path.join(HERE, ".run.lock")
STALE = 900


def _read():
    if not os.path.exists(LOCK_FILE):
        return {}
    try:
        return json.loads(io.open(LOCK_FILE, encoding="utf-8").read())
    except Exception:
        return {}


def _write(d):
    with io.open(LOCK_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(d, ensure_ascii=False))


def stale():
    """返回残留锁信息（None 表示无残留）"""
    d = _read()
    if not d:
        return None
    if time.time() - d.get("ts", 0) > STALE:
        return d
    return None


def acquire(tag):
    d = stale()
    if d is None and _read():
        raise RuntimeError("已有实例在运行：%s" % _read().get("tag"))
    rid = "%s-%d" % (tag, int(time.time()))
    _write({"tag": tag, "rid": rid, "ts": time.time()})
    return rid


def release(rid):
    d = _read()
    if d.get("rid") == rid:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        return True
    return False


def clear():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        return True
    return False
