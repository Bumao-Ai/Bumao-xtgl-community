# Bumao XTGL Community — 开源发布教程

> 面向「不太会开源」的第一次发布者。按顺序做，就能安全地把 Community 版公开到 GitHub。
> 许可证：Apache-2.0（官方全文随包置于根 LICENSE，勿另选模板）。

---

## 0. 一句话说明

Community 版是「AI 助手治理引擎」的开源发行版——把「助手该怎么干活」写成可检查的条款，别人 clone 下来就能用。发布前唯一要做的严肃事：**确认没有把你的本机路径 / 用户名 / 密钥漏出去**。

---

## 1. 发布前隐私自查（最重要，逐条过）

在发布目录下打开终端，逐条执行下面命令，**每条都应输出 0 命中**：

### ① 本机盘符与用户目录
```bash
grep -rn "<本机根>\|用户目录\|<用户>" . --include="*.py" --include="*.json" --include="*.html" --include="*.md"
```
预期：无结果。若有 → 定位文件逐行删改。

### ② 密钥与令牌
```bash
grep -rn "sk-\|api[_-]key\|token\|password" . --include="*.json" --include="*.py" --include="*.html"
```
预期：只命中「字段名」，不命中「真实值」。若出现 `sk-` 开头的长串 → 立刻删。

### ③ 旧项目代号（历史改名残留）
```bash
grep -rn "<旧项目代号>" . --include="*.py" --include="*.json" --include="*.md"
```
预期：无结果（本目录已改名为 community）。

### ④ 本地配置值是否已清空
检查 `20_view/web/web_config.json` 里这三项**必须是空串**：
```json
{ "daiban": "", "defects": "", "check_log_dir": "" }
```
你的个人真实路径只许留在 `web_config.local.json`（该文件必须被 .gitignore 排除，绝不提交）。

### ⑤ 备份文件与缓存
```bash
find . -name "*.bak*" -o -name "__pycache__" -o -name "*.pyc"
```
预期：无结果。`.bak` 文件常含改动前的敏感内容，**发布前删掉**，别图省事留着。

---

## 2. 写 .gitignore（防止以后手滑）

在发布目录根新建 `.gitignore`，内容至少包含：

```
__pycache__/
*.pyc
*.bak
*.bak.*
web_config.local.json
*.log
```

---

## 3. 打一个干净包（可选：先本地验证）

```bash
python 10_rac/engine.py check --strict
```
末行必须 `ALL PASS` 才继续。若不 PASS，先把红项修好，别带故障发布。

---

## 4. 推送到 GitHub（第一次发布）

```bash
# 0）在 GitHub 网页端先「New repository」建好空仓库，名字如 bumao-xtgl-community

# 1）进目录、初始化
cd <你的 community 目录>
git init
git add .
git commit -m "feat: Bumao XTGL Community 首次开源"

# 2）连远程并推送
git branch -M main
git remote add origin https://github.com/<你的用户名>/bumao-xtgl-community.git
git push -u origin main
```

如果 push 时提示要先登录，用 GitHub 的个人访问令牌（Settings → Developer settings → Personal access tokens）当密码。

---

## 5. 发布后补三样东西

1. **README**：一句话说清「这是什么、怎么装、怎么跑 check」
2. **LICENSE**：Apache-2.0 官方全文（三条公开仓已随包提供，直接上传，勿换模板）
3. **CONTRIBUTING.md**（可选）：说明别人怎么提规则修改建议

---

## 6. 常见问题

**Q：我不确定某文件该不该提交，怎么办？**
A：私有的 → 进 .gitignore。拿不准的 → 先不提交，宁可少交不要漏。

**Q：已经 push 了敏感信息怎么办？**
A：立即删仓库重建（历史会留痕，清不干净）。这就是为什么第 1 步的自查必须做在前面。

**Q：engine.py check 一直 FAIL，能先发吗？**
A：不能。这是本引擎的铁律——不 ALL PASS 不开工、不发布。

---

## 怎么从零加一个功能

以「加一个只读的新面板」为例，按五步走；少一步就会出现「开关打开却空白」。

### 1. 加能力位
在 `20_view/web/modules.json` 的 `modules` 数组里加一条，字段照现有条目抄齐：`id`、`name`、`name_en`、`version`、`core`、`min_core`、`kind`、`status`、`group`、`source`、`permission`、`write`、`credential`、`evidence`、`review_by`、`desc`。这张表是全端共用定义，改完要与上游一致；某个发行版要不要开，不写在这里，写到该版 `web_config.json` 的 `capabilities`。`applies_to` 是包用的，不是能力位用的。

### 2. 接后端
只读数据先加进 `snapshot`，在 `xtgl_core.py` 的 `/api/overview` 返回里多一个字段；需要独立查询就加一条 `/api/` 路由。读用 `GET`，写用 `POST`，两者都要过同源校验与 `permission` 权限位。路由里不许写死本机绝对路径，路径一律从配置解析；返回结构固定为状态码与数据两段，出错给可读原因。

### 3. 挂前端
卡片编号以 `s-` 开头，写进 `index.html` 的 `CAP_MAP`，映射到第一步的能力位 `id`；页签不用手工显隐，`applyCaps()` 会按 `capabilities` 自动收起未开启的卡片。词条加在 `i18n.js` 的中英成对条目里，中文句子不拼英文短语，英文句子不夹中文。没有数据时补一句空态文案。

### 4. 加规则包与功能包
规则包放 `00_meta/rules_library/packs/`，功能包放 `00_meta/feature_packs/`；一个文件一个包，`id` 必须与文件名一致。`enabled` 默认 `false`，改成 `true` 才生效。`applies_to` 只填 `community`、`minimal` 这类发行版名；`depends_on` 只能引用 `modules.json` 里已有的能力 `id`。加载顺序固定：先读能力定义，再按本版 `capabilities` 开关，最后叠加 `enabled` 的包。包不能改真身条款，也不能预置天数、份数这类数值。

### 5. 加完怎么自证
在本版跑 `BumaoXTGL_Community_v01.py check --strict`（不带 `--out`）；改动核心件后跑 `kernelsync.py --manifest` 重算清单。对账点：能力定义与上游字节一致、能力关闭时不出现新面板、打开后能取到真数据、检查结论全绿。任何一项不过，就不要把 `enabled` 改成 `true`。

---

【索引尾开始】
- 维护者：Bumao XTGL
- 时间戳：2026-11-03
- 说明：本教程只覆盖 Community 版；Minimal 版见其 00_meta 下的简化版
【索引尾结束】
---

## English

# Bumao XTGL Community — Open Source Release Tutorial

> For first-time publishers who are "not very good at open source". Follow the order and you can safely make the Community edition public on GitHub.
> License: Apache-2.0 (the official full text ships with the package in the root LICENSE; do not choose another template).

---

## 0. In one sentence

The Community edition is the open-source release of the "AI assistant governance engine" — it writes "how the assistant should work" as checkable clauses, and anyone who clones it can use it. The only serious thing to do before publishing: **confirm that you have not leaked your local machine paths / user name / keys**.

---

## 1. Pre-publication privacy self-check (most important, go through item by item)

Open a terminal in the release directory and run the commands below one by one; **each of them should output 0 hits**:

### ① Local drive letters and user directories
```bash
grep -rn "<本机根>\|用户目录\|<用户>" . --include="*.py" --include="*.json" --include="*.html" --include="*.md"
```
Expected: no results. If there are any → locate the files and delete or edit them line by line.

### ② Keys and tokens
```bash
grep -rn "sk-\|api[_-]key\|token\|password" . --include="*.json" --include="*.py" --include="*.html"
```
Expected: only "field names" are hit, not "real values". If a long string starting with `sk-` appears → delete it immediately.

### ③ Old project code name (residue from the historical rename)
```bash
grep -rn "<旧项目代号>" . --include="*.py" --include="*.json" --include="*.md"
```
Expected: no results (this directory has already been renamed to community).

### ④ Whether local configuration values have been cleared
Check that these three items in `20_view/web/web_config.json` **must be empty strings**:
```json
{ "daiban": "", "defects": "", "check_log_dir": "" }
```
Your real personal paths may only stay in `web_config.local.json` (that file must be excluded by .gitignore and never committed).

### ⑤ Backup files and caches
```bash
find . -name "*.bak*" -o -name "__pycache__" -o -name "*.pyc"
```
Expected: no results. `.bak` files often contain sensitive content from before the change, **delete them before publishing**; do not keep them just for convenience.

---

## 2. Write .gitignore (to prevent slips later)

Create a new `.gitignore` in the root of the release directory, containing at least:

```
__pycache__/
*.pyc
*.bak
*.bak.*
web_config.local.json
*.log
```

---

## 3. Build a clean package (optional: verify locally first)

```bash
python 10_rac/engine.py check --strict
```
The last line must be `ALL PASS` before you continue. If it does not PASS, fix the red items first; do not publish with failures.

---

## 4. Push to GitHub (first release)

```bash
# 0）在 GitHub 网页端先「New repository」建好空仓库，名字如 bumao-xtgl-community

# 1）进目录、初始化
cd <你的 community 目录>
git init
git add .
git commit -m "feat: Bumao XTGL Community 首次开源"

# 2）连远程并推送
git branch -M main
git remote add origin https://github.com/<你的用户名>/bumao-xtgl-community.git
git push -u origin main
```

If push asks you to log in first, use a GitHub personal access token (Settings → Developer settings → Personal access tokens) as the password.

---

## 5. Three things to add after publishing

1. **README**: state in one sentence "what this is, how to install it, how to run check"
2. **LICENSE**: the official full text of Apache-2.0 (the three public repositories already ship it with the package; upload it directly, do not swap in another template)
3. **CONTRIBUTING.md** (optional): explain how others can propose rule changes

---

## 6. FAQ

**Q: I am not sure whether a file should be committed. What should I do?**
A: Private → put it into .gitignore. Unsure → do not commit it for now; better to commit less than to leak.

**Q: What if sensitive information has already been pushed?**
A: Delete the repository immediately and rebuild it (history leaves traces and cannot be cleaned out). That is why the self-check in step 1 must be done first.

**Q: engine.py check keeps failing. Can I publish first?**
A: No. This is the iron rule of this engine — no work starts and nothing is published without ALL PASS.

---

## How to add a feature from scratch

Take "add a new read-only panel" as an example and follow five steps; skip one and you get "the switch is on but the panel is blank".

### 1. Add the capability entry
Add an item to the `modules` array in `20_view/web/modules.json`, copying all fields from an existing entry: `id`, `name`, `name_en`, `version`, `core`, `min_core`, `kind`, `status`, `group`, `source`, `permission`, `write`, `credential`, `evidence`, `review_by`, `desc`. This table is the definition shared by all editions, and after changing it you must keep it consistent with upstream; whether a particular edition should enable it is not written here but in that edition's `web_config.json` `capabilities`. `applies_to` is used by packages, not by capability entries.

### 2. Wire up the backend
Add read-only data to `snapshot` first, adding one more field to the `/api/overview` response in `xtgl_core.py`; if an independent query is needed, add an `/api/` route. Use `GET` for reads and `POST` for writes; both must pass the same-origin check and the `permission` bit. Routes must not hard-code local absolute paths; resolve paths from configuration every time. The return structure is fixed as two parts, status code and data; on error, give a readable reason.

### 3. Mount the front end
Card numbers start with `s-`, are written into `CAP_MAP` in `index.html`, and map to the capability entry `id` from step one; tabs do not need manual show/hide, `applyCaps()` automatically collapses cards that are not enabled according to `capabilities`. Add entries to the paired Chinese-English items in `i18n.js`; Chinese sentences do not mix English phrases and English sentences do not mix Chinese. Add an empty-state message for when there is no data.

### 4. Add rule packages and feature packages
Rule packages go into `00_meta/rules_library/packs/`, feature packages go into `00_meta/feature_packs/`; one file is one package, and `id` must match the file name. `enabled` defaults to `false`; set it to `true` to take effect. `applies_to` only takes edition names such as `community` and `minimal`; `depends_on` may only reference capability `id`s that already exist in `modules.json`. The load order is fixed: first read the capability definitions, then switch according to this edition's `capabilities`, and finally stack the `enabled` packages. Packages must not modify canonical clauses, nor preset values such as days or counts.

### 5. How to prove it after adding
Run `BumaoXTGL_Community_v01.py check --strict` in this edition (without `--out`); after changing core files, run `kernelsync.py --manifest` to recompute the manifest. Reconciliation points: capability definitions are byte-identical to upstream, no new panel appears while the capability is off, real data can be fetched once it is on, and the check verdict is all green. If any item fails, do not set `enabled` to `true`.

---

【Index tail start】
- Maintainer: Bumao XTGL
- Timestamp: 2026-11-03
- Note: this tutorial covers only the Community edition; for the Minimal edition see the simplified version under its 00_meta
【Index tail end】
