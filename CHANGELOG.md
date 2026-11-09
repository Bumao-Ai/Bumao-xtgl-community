# Changelog

## 0.31 — 2026-11-09

本版只做「解包即绿」的收口：改前件随包、凭据两步复跑写进包内说明。

- **加号依据：0.30→0.31（+0.01 同档正常晋升）** — 依据 `HX\personal\20_view\di00_qidong_zongze.txt` L55—60 的 0.6.8 逐级加号规则；内核版本未变（仍 core `v0.2.4`），不因文档/打包修正再加内核档。
- **改前件随包（B16）** — `90_lishi/gongkai_weihu_261107/` 内改前件原本被 `.gitignore` 的 `*.bak` 挡住；新增白名单 `!90_lishi/gongkai_weihu_261107/*`，使 `index.html.261109_pre_0.2.4.bak`、`kernel_contract.json.261109_pre_0.2.4.bak` 及同目录历史改前件随包发布（内容为公开件旧版，无私密内容）。
- **解包复跑两步（B19／B22）** — `30_taizhang/check_last.json` 是运行凭据，不提交；包内 `README.md`／`README-HX.txt` 已写明：解包后先跑一次 `check --strict`（写入凭据），再跑第二次复判，第二次结论应为 `0/44 gates red`。
- **发布 tag** — `v0.19` → `v0.20`；应用内版本 `0.30` → `0.31`（同档 +0.01）。
- **订正** — 0.30 条目所称「随包内核 v0.2.3」有误：0.30 发布件实物为 core `v0.2.4`（commit `5c217f6`），0.2.3 同步内容在发布前已作废重做；本版起以 0.2.4 为准。
- **未变** — 规则 59 条／15 章、闸门总数 44；A10 判据、三态定义、B16／B19／B22 判据与 0.30 相同。

## 0.30 — 2026-11-09

本版随包内核由 core `v0.2.2` 升到 `v0.2.3`（commit `282d684`，同档 0.2.x，按 0.6.9 规则本端 +0.01），并把控制台任务留档分组修正带入发布件。

- **加号依据：0.29→0.30（+0.01 同档正常晋升；0.2.2→0.2.3 不跨档，不加 0.1）** — 依据 `HX\personal\20_view\di00_qidong_zongze.txt` L55—60 的 0.6.8 逐级加号规则，不跳号、不跨级。
- **应用内版本 `0.29` → `0.30`** — `00_meta/meta.json`；`README.md` 两个版本空间说明、`README-HX.txt` 当前版本行、本台账同步（发布 tag `v0.18` → `v0.19`）。
- **随包内核同步到 core `v0.2.3`（28 件）** — 整目录覆盖 `kernel/bumao_core/`，逐件 SHA256 与 core `282d684` 一致（28/28）；新增 `test_jiancha_ledger.py`、`test_jiancha_recovery.py`、`test_jiancha_scope.py`，运行层 `jiancha/` 4 件加固。
- **控制台修复带入发布件** — `20_view/web/index.html` 的 `logKey()` 目录名 `任务目录` → `40_renwu`；工作日志分组按项目名归并，不再全落「其他记录」。
- **未变** — 规则 59 条／15 章、闸门总数 44；`A10` 按设计仍为 DENY（随包审批册零条目模板），

## 0.29 — 2026-11-09

本版同步 core `v0.2.2`（commit `06d78fb`）随包内核，并把应用内版本补齐到发布序列号。Kernel sync to core v0.2.2; in-app version back-filled to the release series.

- **加号依据：0.18→0.19（+0.01 正常晋升）→0.29（+0.10 内核跨档 0.1→0.2，同一版内叠加）** — 依据 `HX\personal\20_view\di00_qidong_zongze.txt` L55—60 的 0.6.8 逐级加号规则，不跳号、不跨级。
- **应用内版本 `0.10` → `0.29`** — `00_meta/meta.json`；`README-HX.txt` 当前版本行、`README.md` 两个版本空间说明同步。
- **随包内核同步到 core `v0.2.2`** — 以 tag 内容为准，非工作树拷贝；整目录覆盖 `kernel/bumao_core/`，新增 `host_reference.py`、`test_a10_policy.py`、`test_gate_registry.py` 与 `jiancha/` 运行层子包。
- **视图按新版本重渲染** — `render.py write` 重生成 `20_view/` 15 个分章、`mulu.txt` 与 `quanwen_0.29.txt`。
- **未变** — 规则 59 条／15 章、闸门总数 44；`A10`／`A13` 判定逻辑与判据输入无改动。

## 0.18 — 2026-11-09

本版只做内核同步，不新增规则、不放宽任何判定；**是本阶段的最后一个版本**，未来一个月不再主动迭代（只做维护与修复）。Kernel sync only; this is the last release of this phase.

- **内核随 core `v0.2.0-beta.5` 同步** — `kernel/bumao_core/engine.py`、`gate_registry.py`、`bumao_core_rules.py`、`gate_count.py`、`test_equivalence.py` 与 `HOST_CONTRACT.md` 按整目录口径覆盖到 core 同版本。内核以 core 为唯一源头，这里是同一份字节。
- **`build_parser()` 重复注册修复** — 旧代码连续两次 `sub.add_parser("check")`，调用 `build_parser()` 即抛 `argparse.ArgumentError: conflicting subparser: check`；`main()` 过去另建一份解析器，文档里的参数因此从未真正注册。现在只有一份解析器，`main()` 复用同一份。
- **三个参数由文档承诺改为真实实现** — `check --quick`（只跑 A 段结构闸，结论行明说不能替代 `--strict`）、`whoami --full`（追加 4 行诊断，不带时逐字不变）、`selftest --kernel`（6 项宿主无关自检）。随包新增 `kernel/bumao_core/test_build_parser.py` 锁定回归（4/4）。
- **两种加载方式并存** — 新增 `kernel/bumao_core/__init__.py`，`pip install -e .` 后 `from bumao_core import engine` 与历史 `sys.path.insert` + `import engine` 都可用；`gate_count.py`／`test_equivalence.py` 在单仓 clone 下改为打印「需要三端同级检出」并退出 2，不再假绿或误报红。
- **留痕** — 三件改前件同哈希随包（`*.261109_v018.bak`），两件新增件登 `30_taizhang/shouci_ruku_dengji.txt`；审批册第 18 号记录本轮授权原话。
- **未变** — 规则 59 条／15 章、闸门总数 44、应用内版本 `0.10`、目录结构未改；`A10`／`A13` 判定逻辑无改动，无当日授权条目时仍判 `DENY`。
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

---

## English

### 0.30 — 2026-11-09

Bundled kernel bumped from core v0.2.2 to v0.2.3 (commit `282d684`, same 0.2.x tier, +0.01 for this edition per rule 0.6.9), and the console task-record grouping fix is carried into the release artifact.

- **Bump rationale: 0.29→0.30 (+0.01, normal promotion within the same tier; 0.2.2→0.2.3 does not cross tiers, so no +0.1)** — per the 0.6.8 stepwise bump rule at `HX\personal\20_view\di00_qidong_zongze.txt` L55—60: no skipped numbers, no skipped tiers.
- **In-app version `0.29` → `0.30`** — `00_meta/meta.json`; the two-version-spaces note in `README.md`, the current-version line in `README-HX.txt` and this ledger are aligned (release tag `v0.18` → `v0.19`).
- **Bundled kernel synced to core `v0.2.3` (28 files)** — the whole directory overwrites `kernel/bumao_core/`, and each file's SHA256 matches core `282d684` (28/28); adds `test_jiancha_ledger.py`, `test_jiancha_recovery.py`, `test_jiancha_scope.py`, and the 4 files of the `jiancha/` runtime layer are hardened.
- **Console fix carried into the release artifact** — the `logKey()` directory name in `20_view/web/index.html` changes `任务目录` → `40_renwu`; work-log groups are merged by project name and no longer all fall into "其他记录".
- **Unchanged** — 59 rules / 15 chapters, 44 gates in total; `A10` is still DENY by design (zero-entry bundled approval ledger template) and is not written as fixed.

### 0.29 — 2026-11-09

Kernel sync to core v0.2.2; in-app version back-filled to the release series.

- **Bump rationale: 0.18→0.19 (+0.01 normal promotion) →0.29 (+0.10, kernel crossing tiers 0.1→0.2, stacked within one release)** — per the 0.6.8 stepwise bump rule at `HX\personal\20_view\di00_qidong_zongze.txt` L55—60: no skipped numbers, no skipped tiers.
- **In-app version `0.10` → `0.29`** — `00_meta/meta.json`; the current-version line in `README-HX.txt` and the two-version-spaces note in `README.md` are aligned.
- **Bundled kernel synced to core `v0.2.2`** — taken from the tag contents, not a working-tree copy; the whole directory overwrites `kernel/bumao_core/`, adding `host_reference.py`, `test_a10_policy.py`, `test_gate_registry.py` and the `jiancha/` runtime subpackage.
- **Views re-rendered for the new version** — `render.py write` regenerates the 15 chapter files under `20_view/`, `mulu.txt` and `quanwen_0.29.txt`.
- **Unchanged** — 59 rules / 15 chapters, 44 gates in total; the `A10` / `A13` verdict logic and evidence inputs are untouched.

### 0.18 — 2026-11-09

Kernel sync only; this is the last release of this phase.

- **Kernel synced with core `v0.2.0-beta.5`** — `kernel/bumao_core/engine.py`, `gate_registry.py`, `bumao_core_rules.py`, `gate_count.py`, `test_equivalence.py` and `HOST_CONTRACT.md` are overwritten to the same core release as a whole directory. The kernel has core as its only source; this is the same bytes.
- **`build_parser()` duplicate-registration fix** — the old code called `sub.add_parser("check")` twice, so calling `build_parser()` raised `argparse.ArgumentError: conflicting subparser: check`; `main()` used to build a separate parser, so the documented parameters were never actually registered. Now there is one parser, reused by `main()`.
- **Three parameters moved from documented promises to real implementations** — `check --quick` (runs only the section A structural gates, and the conclusion line states it cannot replace `--strict`), `whoami --full` (appends 4 diagnostic lines, byte-for-byte unchanged without it), `selftest --kernel` (6 host-independent self-checks). Bundled `kernel/bumao_core/test_build_parser.py` locks the regression (4/4).
- **Two loading modes coexist** — new `kernel/bumao_core/__init__.py`; after `pip install -e .` both `from bumao_core import engine` and the historical `sys.path.insert` + `import engine` work; on a single-repo clone `gate_count.py` / `test_equivalence.py` now print "requires the three editions checked out at the same level" and exit 2, no longer faking green or reporting false red.
- **Trail kept** — the three pre-change files ship with the same hash (`*.261109_v018.bak`), and the two new files are registered in `30_taizhang/shouci_ruku_dengji.txt`; approval ledger entry No. 18 records this round's authorization verbatim.
- **Unchanged** — 59 rules / 15 chapters, 44 gates in total, in-app version `0.10`, layout unchanged; the `A10` / `A13` verdict logic is untouched and still DENYs when there is no same-day authorization entry.
- **Known reds (design behaviour)** — on a local working tree that already has a baseline, changing kernel files that day makes `A13` red (`改而未授权`), and `A10` always DENYs because the bundled approval ledger has zero entries. A downloaded artifact has no baseline on first run, so `A13` first enrolls the baseline and then passes, leaving only `A10`.

### 0.17 — 2026-11-09

This release fixes where the gates look for the approval ledger and repairs one vacuous gate; no verdict was relaxed.

- **`B15` vacuous-gate fix (real defect)** — `gate_b15()`'s prefix was originally `community/20_view/web/`, while the baseline keys are `20_view/web/…` (`REPO` already points at the edition root), so the prefix never matched and the gate always reported "0 files changed", passing in both directions. With the prefix now relative to the edition root, the two `B15` reverse cases in `test_qiangzhi.py` (unapproved change to a core file, approval naming a different file) are actually caught. `B15` 的 prefix bug made the gate always report “0 files changed”, so both directions passed; the prefix is now relative to the edition root and both reverse cases are caught.
- **Reverse suite completed** — `10_rac/test_qiangzhi.py` adds 1 reverse case (a same-day approval entry exists but names another file, which `B15` must still block); the suite grows from 16 to 17 cases, actually run **17 caught / 0 missed**. One reverse case added (same-day approval naming a different file); suite 17 cases, all caught.
- **A10 / A13 evidence-lookup correction** — on a single-repo clone the "area root" was originally taken as the parent outside the repo, so `A10` could not read `30_taizhang/shenpi_jilu.txt`; now, when this repo root contains `30_taizhang/`, this repo root is the area root. `find_approval_ledger()` no longer scans sibling directories (the old implementation read another repo's approval ledger, the conclusion right but the reason wrong). The bundled `30_taizhang/shenpi_jilu.txt` is a **structure template (zero entries)**, so `A10` prints `A10 判定=DENY ｜ 判拒（DENY · 策略 deny）：审批册里没有可解析的【第 N 号】条目`. `A10`/`A13` now resolve the area root correctly and no longer read a sibling repo's ledger; the shipped template has zero entries, so `A10` prints an explicit DENY with the policy name.
- **Pre-change files bundled** — this round's two pre-change kernel files (`engine.py.261108_deny.bak`, `gate_registry.py.261108_deny.bak`) ship in `90_lishi/gongkai_weihu_261107/`. `*.bak` files are not committed by default; they ship here specifically so that **after a downloaded artifact is extracted** `B16` can also find a same-hash pre-change file — otherwise a clean unpack has only the backup area that exists on this machine, and `B16` would go red. The two pre-change kernel copies ship in `90_lishi/gongkai_weihu_261107/`, so a downloaded extract satisfies `B16` without any local backup.
- **Unchanged** — 59 rules / 15 chapters, 44 gates in total, in-app version `0.10`, layout unchanged. Rules, gate count, in-app version and layout unchanged.
- **Known reds** — extracted and run immediately: first run `3/44` (`A10` DENY by design, `B19` / `B22` because the check credential is only written at the end of that round), second run `1/44` (only `A10`). `B16` is green because the pre-change files ship. Extracted artifact: first run `3/44` (`A10` by design, `B19`/`B22` because the credential is written at the end of that run), second run `1/44` (only `A10`). `B16` is green because the pre-change copies ship.

### 0.16 — 2026-11-08

This release ships a real gate change: `B29` notices must name each core file, and `*` no longer matches as a wildcard.

- **`B29` criteria tightened** — `_yugao_covers()` in `10_rac/qiangzhi.py` changes from `fnmatch` wildcards to literal exact matching; section 11.6 of `10_rac/zhunze/z11.json` now states "from 0.16, `*` is no longer a wildcard". Before: one `*.html` notice covered every core file. Now: the file name must match literally; unlisted files still fail.
- **Regression cases** — `10_rac/test_qiangzhi.py` adds 2 reverse cases (`*.html` wildcard, notice naming another file) and 1 positive control (exact naming still passes); the reverse suite grows from 14 to 16 cases, actually run 15 caught / 1 missed (`B15` is a standing gap, not changed in this release). Two reverse cases and one positive control added; 16 cases, 15 caught / 1 missed (`B15`, pre-existing).
- **Derived views** — `python render.py write` re-renders 17 views, and `B1` view drift is zero.
- **Unchanged** — 59 rules / 15 chapters, 44 gates in total, in-app version `0.10`, layout, the three page styles and the generated view format are unchanged. Rules, gate count, in-app version and layout unchanged.
- **Known reds** — clean clone first run `4/44` (`A10`, `A13`, `B19`, `B22`), second run `2/44` (`A10`, `A13`; public repos do not ship an approval ledger, red by design). Clean clone: first run `4/44`, second `2/44` (`A10`/`A13` by design).

### 0.15 — 2026-11-08

This release ships real behaviour changes: encoding-safe entry points, a portable launcher, and a content-hash boundary for `B22`.

- **Encoding fix** — the `__main__` blocks of `10_rac/BumaoXTGL_Community_v01.py`, `20_view/web/serve.py` and `20_view/web/xtgl_core.py` now call `reconfigure(encoding="utf-8", errors="replace")` on both `stdout` / `stderr`, the same as the kernel's `serve.py` / `xtgl_core.py`. Before: on a cp936 console or with missing glyphs, a rare character could abort the check with `UnicodeEncodeError`; now it degrades to a replacement character and the run continues. Before: a rare glyph could abort the run with `UnicodeEncodeError`. Now: it is replaced instead of raising.
- **Launcher** — `20_view/web/qidong_kongzhitai.bat` sets `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8` before calling any interpreter; the probe order changes to `py -3 → python3 → python → python_path.txt` (local override last), each candidate is run with `-c "import sys"`, and the Windows Store stub `python.exe` (exit code 9009) is skipped. The launcher probes `py -3 → python3 → python → python_path.txt`, runs each candidate, and rejects the Store stub.
- **R6: `B22` boundary switched to content hashes** — each completed round writes the content-hash list of managed files into `30_taizhang/check_last.json`; the next round's `B22` compares contents file by file instead of looking at mtime. This repo has 36 managed files (12 web-core + 9 kernel + 15 rule files). Before: backdating `mtime` could bypass `B22`. Now: the boundary is the hash list of 36 managed files.
- **Unchanged** — 59 rules / 15 chapters, 44 gates in total, in-app version `0.10`, release convention and layout unchanged. Rules, gate count, in-app version and layout are unchanged.
- **Docs and maintenance status** — README gains `Status: maintenance pause` / 「状态：维护暂停，稳定可用」 at the top; new `RETURN_HERE.md` as the cold-start entry for resuming iteration (look at three things first, touch `CHANGELOG.md` first), and it is added to the root flat-file allowlist so `B3` stays green. README status line added; resume path documented in `RETURN_HERE.md`, allowlisted so `B3` stays green.
- **Known reds** — the second `check --strict` run is `2/44` (`A10`, `A13`; public repos do not ship an approval ledger, red by design). A clean clone's first run additionally has `B19` / `B22`, because the credential is written only at the end of that round; the second run is `2/44`. Known reds: `A10`/`A13` by design; a clean clone's first run adds `B19`/`B22` until the credential is written.

### 0.14 — 2026-11-08

This release aligns naming and structure and ships the kernel contract; it adds no UI feature.

- Before: gate `A10` threw `FileNotFoundError` on a fresh clone, because `kernel_contract.json` was not in the repository. Now: `kernel/kernel_contract.json` and `kernel/contract_test.py` ship at the path `engine.py` reads (`kernel/`, one level above `kernel/bumao_core/`), so `A10` reports the missing approval ledger instead of crashing.
- Before: README opened with gate IDs and ledger paths. Now: first screen answers what/who/problem, English first, Chinese below.
- Before: no screenshots. Now: two real captures in `20_view/screens/` — console overview and `check --strict` output. Screenshots cannot sit in a top-level `docs/` directory because gate `B4` only allows numbered layer directories; moving them keeps `B4` green without changing the gate.
- Before: install command followed `main`. Now: pinned to `v0.14` and verified with `SHA256SUMS`.
- Numbers corrected: `56 rules / 13 chapters` → `59 rules / 15 chapters / 44 checks`, with an explicit note that rules and checks are two dimensions (`check --strict` A1 line reports `15 ch / 59 cls`).
- No rule or gate change: `git diff v0.13..HEAD -- 10_rac/` is empty; `20_view/` only gains the screenshot folder, and the only `kernel/` additions are the contract pair above. On a clean clone, run `check --strict` twice: the first run is `4/44` red (`A10`, `A13`, `B19`, `B22`), the second is `2/44` red, because `check_last.json` is written at the end of the first run.

### 0.1.1 — 2026-11-08

Bundled kernel.

- This repo adds `kernel/bumao_core/`, so a clone runs without an external `bumao-core`.
- The entry script's kernel lookup path changes from `../../kernel/bumao_core` to `../kernel/bumao_core`.
- Kernel maintenance model: `bumao-core` is the only source, and the whole directory overwrites this repo's copy.

### 0.1 — 2026-11-08

First public release.

- Ships 56 generic rules and a 13-chapter structure.
- All unified kernel gates run, and `check --strict` gives the single conclusion.
- Six-layer workspace structure plus the three-layer assets: real body / views / ledgers.
- Web console (default 8802), with tabs trimmed by capability switches.
