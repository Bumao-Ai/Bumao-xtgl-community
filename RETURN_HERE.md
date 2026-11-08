# RETURN_HERE — resume here

Status: maintenance pause · 状态：维护暂停，稳定可用

Iteration is paused; the current release is stable and usable as-is. When work resumes, start from this file.
迭代已暂停；当前版本稳定可用。恢复迭代时，从这份文件开始。

## Look at these three first · 先看这三样

1. **Which version you are on, and whether the tree is clean**
   `git tag --sort=-v:refname | head -3` and `git status --short`.
   If the tree is dirty, stop and decide what to keep before touching anything.
   先确认当前 tag 与工作区是否干净；工作区不干净就先决定留什么，再动手。

2. **The last verdict, then the current one**
   Read `30_taizhang/check_last.json` (`finished_at`, `nfail`, `managed_sha`), then run `check --strict` twice.
   Two identical conclusions are the baseline; one run alone is not evidence.
   先读上一轮凭据，再连跑两次 `check --strict`；两次结论一致才算基线。

3. **What was in flight**
   Read the top entry of `CHANGELOG.md` and `ROADMAP.md`. The top entry lists what the last release actually changed; the roadmap marks what was still in progress.
   读 `CHANGELOG.md` 最上面一条与 `ROADMAP.md`：前者是上一版真实改动，后者标着当时未完成项。

## Touch this file first · 先动这个文件

`CHANGELOG.md` — open the new version entry before editing any code, so the change is recorded before it exists.
先开 `CHANGELOG.md` 的新版本条目，再改代码；先有记录，后有改动。

Then run `check --strict` twice and compare the two conclusions before committing.
然后连跑两次 `check --strict`，两次一致再提交。
