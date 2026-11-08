# Changelog

## Unreleased — 2026-11-08

本版为口径与结构对齐（无新增界面功能）。This release aligns naming and structure; it adds no UI feature.

- Before: README opened with gate IDs and ledger paths. Now: first screen answers what/who/problem, English first, Chinese below.
- Before: no screenshots. Now: two real captures in `docs/screens/` — console overview and `check --strict` output.
- Before: install command followed `main`. Now: pinned to the release tag and verified with `SHA256SUMS`.
- Numbers corrected: `56 rules / 13 chapters` → `59 rules / 15 chapters / 44 checks`, with an explicit note that rules and checks are two dimensions (`check --strict` A1 line reports `15 ch / 59 cls`).
- No rule, gate or kernel change: `git diff v0.13..HEAD -- 10_rac/ 20_view/ kernel/` is empty.

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
