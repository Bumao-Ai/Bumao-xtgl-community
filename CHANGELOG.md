# Changelog

## 0.15 — 2026-11-08

本版是功能版：编码修复、启动器兼容、`B22` 改按内容哈希划界。This release ships real behaviour changes: encoding-safe entry points, a portable launcher, and a content-hash boundary for `B22`.

- **编码修复** — `10_rac/BumaoXTGL_Community_v01.py`、`20_view/web/serve.py`、`20_view/web/xtgl_core.py` 的 `__main__` 现在对 `stdout`／`stderr` 都做 `reconfigure(encoding="utf-8", errors="replace")`，与内核 `serve.py`／`xtgl_core.py` 同款。改前：控制台在 cp936 或缺少字形时遇到罕见字符会抛 `UnicodeEncodeError` 中断检查；改后：降级为替换字符，继续跑完。Before: a rare glyph could abort the run with `UnicodeEncodeError`. Now: it is replaced instead of raising.
- **启动器** — `20_view/web/qidong_kongzhitai.bat` 在调用任何解释器之前设置 `PYTHONUTF8=1`／`PYTHONIOENCODING=utf-8`；位置探测顺序改为 `py -3 → python3 → python → python_path.txt`（本地覆盖放在最后），每个候选都用 `-c "import sys"` 实跑，Windows Store 的假 `python.exe`（退出码 9009）被跳过。The launcher probes `py -3 → python3 → python → python_path.txt`, runs each candidate, and rejects the Store stub.
- **R6：`B22` 划界依据换成内容哈希** — 每轮完成的检查把受管件内容哈希清单写进 `30_taizhang/check_last.json`；`B22` 下一轮逐件比对内容，不再看 mtime。本仓受管件 36 件（12 件 web 核心 + 9 件内核 + 15 条规则）。改前：把时间戳往回拨就能绕过闸门；改后：内容一变即需当日点名审批。Before: backdating `mtime` could bypass `B22`. Now: the boundary is the hash list of 36 managed files.
- **未变** — 规则 59 条／15 章、闸门总数 44、应用内版本 `0.10`、发布口径与目录结构均未改动。Rules, gate count, in-app version and layout are unchanged.
- **文档与维护状态** — README 顶部加 `Status: maintenance pause`／「状态：维护暂停，稳定可用」；新增 `RETURN_HERE.md` 作为恢复迭代的冷启动入口（先看三样、先动 `CHANGELOG.md`），并把它列入根下平铺白名单，`B3` 仍绿。README status line added; resume path documented in `RETURN_HERE.md`, allowlisted so `B3` stays green.
- **已知红项** — `check --strict` 第二次运行 `2/44`（`A10`、`A13`，公开仓不发审批册，按设计红）。干净克隆的首次运行另加 `B19`／`B22`，因为凭据在该轮结束才写入；第二次即 `2/44`。Known reds: `A10`/`A13` by design; a clean clone's first run adds `B19`/`B22` until the credential is written.

## 0.14 — 2026-11-08

本版为口径与结构对齐，并补上内核契约（无新增界面功能）。This release aligns naming and structure and ships the kernel contract; it adds no UI feature.

- Before: gate `A10` threw `FileNotFoundError` on a fresh clone, because `kernel_contract.json` was not in the repository. Now: `kernel/kernel_contract.json` and `kernel/contract_test.py` ship at the path `engine.py` reads (`kernel/`, one level above `kernel/bumao_core/`), so `A10` reports the missing approval ledger instead of crashing.
- Before: README opened with gate IDs and ledger paths. Now: first screen answers what/who/problem, English first, Chinese below.
- Before: no screenshots. Now: two real captures in `20_view/screens/` — console overview and `check --strict` output. Screenshots cannot sit in a top-level `docs/` directory because gate `B4` only allows numbered layer directories; moving them keeps `B4` green without changing the gate.
- Before: install command followed `main`. Now: pinned to `v0.14` and verified with `SHA256SUMS`.
- Numbers corrected: `56 rules / 13 chapters` → `59 rules / 15 chapters / 44 checks`, with an explicit note that rules and checks are two dimensions (`check --strict` A1 line reports `15 ch / 59 cls`).
- No rule or gate change: `git diff v0.13..HEAD -- 10_rac/` is empty; `20_view/` only gains the screenshot folder, and the only `kernel/` additions are the contract pair above. On a clean clone, run `check --strict` twice: the first run is `4/44` red (`A10`, `A13`, `B19`, `B22`), the second is `2/44` red, because `check_last.json` is written at the end of the first run.

## 0.1.1 — 2026-11-08

内置内核。

- 本仓新增 `kernel/bumao_core/`，克隆后无需外部 `bumao-core` 即可运行。
- 入口脚本内核查找路径由 `../../kernel/bumao_core` 改为 `../kernel/bumao_core`。
- 内核维护方式：以 `bumao-core` 为唯一源头，整目录覆盖本仓副本。

## 0.1 — 2026-11-08

首次公开发布。

- 自带 56 条通用规则、13 章结构。
- 统一内核闸门全量执行，`check --strict` 给出唯一结论。
- 六层工作区结构与真身／视图／台账三层资产。
- Web 控制台（默认 8802），按能力开关裁剪页签。
