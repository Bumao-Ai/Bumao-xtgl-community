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

"""验证日志筛选器数据可用性。"""
import json
import os
import sys
import urllib.request

_here = os.path.dirname(os.path.abspath(__file__))


def _port():
    """端口只从 web_config.json 读；读不到就报错退出，不静默兜底。"""
    cfg = os.path.join(_here, "web_config.json")
    try:
        with open(cfg, "r", encoding="utf-8-sig") as f:
            port = json.load(f).get("port")
    except (OSError, ValueError) as e:
        sys.exit("读不到 %s 的 port：%s（本脚本不猜端口）" % (cfg, e))
    if isinstance(port, bool) or not isinstance(port, int) or port <= 0:
        sys.exit("web_config.json 缺有效 port（本脚本不猜端口）")
    return port


url = "http://127.0.0.1:%d/api/overview?fast=1" % _port()
with urllib.request.urlopen(url, timeout=20) as resp:
    data = json.loads(resp.read().decode("utf-8"))

logs = (data.get("logs") or {}).get("list") or []
if not logs:
    print("没有日志数据")
    exit(1)

days, whos, projs = set(), set(), set()
for r in logs:
    days.add(r.get("date", "—"))
    who = (r.get("who") or "").strip()
    who = who.split("（")[0].strip() or "未标注"
    whos.add(who)
    detail = (r.get("detail") or "").replace("\\", "/")
    import re
    m = re.search(r"/40_renwu/([^/]+)/", detail)
    projs.add(m.group(1) if m else "其他记录")

print("=== 筛选器数据摘要 ===")
print("日期 (%d 个): %s" % (len(days), ", ".join(sorted(days))))
print("客户端 (%d 个): %s" % (len(whos), ", ".join(sorted(whos))))
print("工程 (%d 个): %s" % (len(projs), ", ".join(sorted(projs))))
print("\n各筛选条件计数:")
for d in sorted(days):
    cnt = len([r for r in logs if r.get("date") == d])
    print("  %s: %d 条" % (d, cnt))
for w in sorted(whos):
    cnt = len([r for r in logs if ((r.get("who") or "").split("(")[0].strip() or "未标注") == w])
    print("  %s: %d 条" % (w, cnt))
for p in sorted(projs):
    cnt = len([r for r in logs if (lambda d: (re.search(r"/40_renwu/([^/]+)/", d.replace("\\", "/")) or type("", (), {"group": lambda _, x: "其他记录"})()).group(1) if re.search(r"/40_renwu/([^/]+)/", d.replace("\\", "/")) else "其他记录")(r.get("detail", "")) == p])
    print("  %s: %d 条" % (p, cnt))
