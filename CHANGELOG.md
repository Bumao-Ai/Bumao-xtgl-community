# Changelog

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
