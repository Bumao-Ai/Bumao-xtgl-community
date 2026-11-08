# Changelog

## 0.18 — 2026-11-09

本版只做内核同步，不新增规则、不放宽任何判定；**是本阶段的最后一个版本**，未来一个月不再主动迭代（只做维护与修复）。Kernel sync only; this is the last release of this phase.

- **内核随 core `v0.2.0-beta.5` 同步** — `kernel/bumao_core/engine.py`、`gate_registry.py`、`bumao_core_rules.py`、`gate_count.py`、`test_equivalence.py` 与 `HOST_CONTRACT.md` 按整目录口径覆盖到 core 同版本。内核以 core 为唯一源头，这里是同一份字节。
- **`build_parser()` 重复注册修复** — 旧代码连续两次 `sub.add_parser("check")`，调用 `build_parser()` 即抛 `argparse.ArgumentError: conflicting subparser: check`；`main()` 过去另建一份解析器，文档里的参数因此从未真正注册。现在只有一份解析器，`main()` 复用同一份。
- **三个参数由文档承诺改为真实实现** — `check --quick`（只跑 A 段结构闸，结论行明说不能替代 `--strict`）、`whoami --full`（追加 4 行诊断，不带时逐字不变）、`selftest --kernel`（6 项宿主无关自检）。随包新增 `kernel/bumao_core/test_build_parser.py` 锁定回归（4/4）。
- **两种加载方式并存** — 新增 `kernel/bumao_core/__init__.py`，`pip install -e .` 后 `from bumao_core import engine` 与历史 `sys.path.insert` + `import engine` 都可用；`gate_count.py`／`test_equivalence.py` 在单仓 clone 下改为打印「需要三端同级检出」并退出 2，不再假绿或误报红。
- **留痕** — 三件改前件同哈希随包（`*.261109_v018.bak`），两件新增件登 `30_taizhang/shouci_ruku_dengji.txt`；审批册第 18 号记录本轮授权原话。
- **未变** — 规则 59 条／15 章、闸门总数 44、应用内版本 `0.10`、目录结构未改；`A10`／`A13` 判定逻辑未动，无当日授权条目时仍判 `DENY`。
- **已知红项（设计行为）** — 已存在基线的本机工作树里，当日改动内核件会让 `A13` 判红（`改而未授权`），`A10` 因随包审批册零条目恒判 `DENY`。下载件解出后首跑无基线，`A13` 先纳基线后通过，只剩 `A10`。

## 0.17 — 2026-11-09

本版修的是判据取件与一条空闸，不放宽任何判定。This release fixes where the gates look for the approval ledger and repairs one vacuous gate; no verdict was relaxed.

- **`B15` 空闸修复（真缺陷）** — `gate_b15()` 的前缀原是 `community/20_view/web/`，而基线键是 `20_view/web/…`（`REPO` 已指向端根），前缀永不匹配，于是恒报「0 件改动」，正反两向都放行。改为相对端根的前缀后，`test_qiangzhi.py` 的两条 `B15` 反向用例（未审批改核心件、审批未点名该件）才真正被拦。`B15` 的前缀 bug made the gate always report “0 files changed”, so both directions passed; the prefix is now relative to the edition root and both reverse cases are caught.
- **反向套件补齐** — `10_rac/test_qiangzhi.py` 新增 1 条反向用例（当日有审批条目但点名另一件，`B15` 必须仍拦），套件由 16 条增至 17 条，实跑 **17 caught / 0 missed**。One reverse case added (same-day approval naming a different file); suite 17 cases, all caught.
- **A10／A13 判据取件修正** — 单仓 clone 下「区根」原被取成仓外上一级，`A10` 读不到 `30_taizhang/shenpi_jilu.txt`；现在本仓根带 `30_taizhang/` 时以本仓根为区根。`find_approval_ledger()` 不再扫描兄弟目录（旧实现会读到别仓审批册，结论对但理由错）。随包新增 `30_taizhang/shenpi_jilu.txt` **结构模板（零条目）**，`A10` 因此输出 `A10 判定=DENY ｜ 判拒（DENY · 策略 deny）：审批册里没有可解析的【第 N 号】条目`。`A10`/`A13` now resolve the area root correctly and no longer read a sibling repo's ledger; the shipped template has zero entries, so `A10` prints an explicit DENY with the policy name.
- **改前件随包** — 本轮改动的两件内核改前件（`engine.py.261108_deny.bak`、`gate_registry.py.261108_deny.bak`）随包放进 `90_lishi/gongkai_weihu_261107/`。`*.bak` 默认不入库；本次特意随包，是为了让**下载件解出后** `B16` 也能对到同哈希改前件——否则干净解包只有本机才有的备份区，`B16` 会判红。The two pre-change kernel copies ship in `90_lishi/gongkai_weihu_261107/`, so a downloaded extract satisfies `B16` without any local backup.
- **未变** — 规则 59 条／15 章、闸门总数 44、应用内版本 `0.10`、目录结构未改。Rules, gate count, in-app version and layout unchanged.
- **已知红项** — 解出即跑：首跑 `3/44`（`A10` 按设计 DENY，`B19`／`B22` 因检查凭据要到该轮结束才写），第二次 `1/44`（仅 `A10`）。`B16` 因改前件已随包而绿。Extracted artifact: first run `3/44` (`A10` by design, `B19`/`B22` because the credential is written at the end of that run), second run `1/44` (only `A10`). `B16` is green because the pre-change copies ship.

## 0.16 — 2026-11-08

本版是功能版：`B29` 预告闸判据收紧，核心件预告必须逐件点名，`*` 不再是通配符。This release ships a real gate change: `B29` notices must name each core file, and `*` no longer matches as a wildcard.

- **`B29` 判据收紧** — `10_rac/qiangzhi.py` 的 `_yugao_covers()` 由 `fnmatch` 通配改为逐字精确匹配；`10_rac/zhunze/z11.json` 的 11.6 正文同步写明「0.16 起 `*` 不再作通配」。改前：一条 `*.html` 预告能覆盖全部核心件，等于没有点名；改后：预告行必须写出被改件的文件名，未点名的核心件仍判 FAIL。Before: one `*.html` notice covered every core file. Now: the file name must match literally; unlisted files still fail.
- **回归用例** — `10_rac/test_qiangzhi.py` 新增 2 条反向用例（`*.html` 通配、预告点名别的文件）与 1 条放行对照（精确点名仍然通过）；反向套件由 14 条增至 16 条，实跑 15 caught / 1 missed（`B15` 为既有缺口，未在本版改动）。Two reverse cases and one positive control added; 16 cases, 15 caught / 1 missed (`B15`, pre-existing).
- **派生视图** — `python render.py write` 重渲染 17 个视图，`B1` 视图漂移归零。
- **未变** — 规则 59 条／15 章、闸门总数 44、应用内版本 `0.10`、目录结构、三页样式与生成视图格式均未改动。Rules, gate count, in-app version and layout unchanged.
- **已知红项** — 干净克隆首跑 `4/44`（`A10`、`A13`、`B19`、`B22`），第二次 `2/44`（`A10`、`A13`，公开仓不发审批册，按设计红）。Clean clone: first run `4/44`, second `2/44` (`A10`/`A13` by design).

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
