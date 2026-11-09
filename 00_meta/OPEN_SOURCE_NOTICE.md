# Bumao XTGL Community — 开源发行说明

核对日期：2026-11-07　核对方式：逐项对照仓库内实物

## 一、基本信息

| 项 | 值 | 实物依据 |
|---|---|---|
| 名称 | Bumao XTGL Community | `00_meta/meta.json` 的 `name` |
| 版本 | 0.10 | `20_view/web/xtgl_core.py` 的 `CORE_VERSION`；`20_view/web/core_manifest.json` 的 `core_version` |
| 规则体系 | 13 章 56 条（第 11 章 6 条强制、第 12 章 6 条限制） | 见本节末「规则数口径」，由 z 系真身逐条计数 |
| 许可证 | Apache License 2.0 | 仓根 `LICENSE` 与 `10_rac/LICENSE`，两份字节相同 |
| 版权行 | `Copyright 2026 Bumao` | `NOTICE` |
| 商标 | 名称与标识的使用边界见仓根 `TRADEMARK.md` | 实物文件 |
| 端口 | `127.0.0.1:8802` | `20_view/web/web_config.json` 的 `port` |
| 运行环境 | Python 3.12.14；功能代码仅使用标准库 | 入口脚本与核心件的导入清单 |
| 前端 | `20_view/web` 全量随仓库发布，不剥离、不压缩、不混淆 | 实物目录 |

**规则数口径（唯一权威）**：在 community 根执行

```
python -c "import json,glob; fs=sorted(glob.glob('10_rac/zhunze/z*.json')); print(len(fs),'章',sum(len(json.load(open(f,encoding='utf-8-sig')).get('clauses',[])) for f in fs),'条')"
```

本文件与 README、发布教程里的章数／条数都必须以这条命令的输出为准，不手抄。

## 二、核心件与清单口径

`20_view/web` 下 13 个核心件，清单登记在 `core_manifest.json`：

```
xtgl_core.py  serve.py  index.html  setup.html  tutorial.html
kernelsync.py  module_check.py  modules.json  snapshot.py
i18n.js  favicon.png  xtgl_clean.py  design_tokens.json
```

其中 `kernelsync.py`、`module_check.py` 为本地工具，不发布。

`core_manifest.json` 记录上述 13 件的 SHA256，本身也在仓库内。核对应以仓内实物为准：

- 清单内的文件必须都在仓库内，仓库内不得出现清单外的核心件；
- 任意核心件改动后，由维护者在本地重算清单（本地工具，不发布）；
- 版本号只认 `xtgl_core.py` 的 `CORE_VERSION` 与 `core_manifest.json` 的 `core_version`，本文件不另立版本口径。

## 三、前端随包与 SPDX 标注现状

前端源码与后端同许可、同脱敏标准：

- `index.html`、`setup.html`、`tutorial.html`、`i18n.js`、`design_tokens.json`、`favicon.png` 全部随仓库发布；
- 4 个随包 Python 核心件（`xtgl_core.py`、`serve.py`、`snapshot.py`、`xtgl_clean.py`）文件头均带 `SPDX-License-Identifier: Apache-2.0`；
- HTML 与 JS（`index.html`、`setup.html`、`tutorial.html`、`i18n.js`）目前**未带** SPDX 注释，此项待补；
- `modules.json` 与 `design_tokens.json` 为数据文件，不带 SPDX 注释；
- 前端不得出现内部路径、内部角色代号、私有端名称或引用；
- 构建产物、缓存、`node_modules`、`*.bak*`、`*.tmp` 一律不入包。

## 四、禁止入包

- `web_config.local.json`（本机私有配置）
- `__pycache__/`、`*.pyc`
- `*.bak*`、`*.tmp`、`*~`
- `node_modules/`
- 任何未列入本仓库的私有配置或他端文件
- 本机路径、机器名、用户名、内部角色代号、内网地址

## 五、发布前自检

1. 在 `10_rac` 下执行 `python BumaoXTGL_Community_v01.py check --strict`，结论须为 `ALL PASS`；
2. 在 `20_view/web` 下核对 13 件哈希与 `core_manifest.json` 一致（由维护者在本地用核验工具完成，本地工具，不发布）；
3. 隐私重扫：本机路径、机器名、用户名、内部角色代号、内网地址零命中；
4. 冷启动：在干净目录解包后直接起服务，首页可开、向导可走；
5. 确认包内无 `.bak`／`__pycache__`／`node_modules`。

## 六、许可义务

- 分发须保留仓根 `LICENSE` 与 `NOTICE`；
- 修改过的文件须标注改动；
- 名称与标识的使用受仓根 `TRADEMARK.md` 约束。

维护者：Bumao

本稿替代 2026-11-03 的旧稿（旧稿已移入 `90_lishi`）。本稿只写仓库内可核对的实物事实；与实物不符的旧表述已删除。

---

## English

# Bumao XTGL Community — Open Source Release Notice

Verification date: 2026-11-07  Verification method: item-by-item comparison against the physical files in the repository

## I. Basic information

| Item | Value | Physical evidence |
|---|---|---|
| Name | Bumao XTGL Community | `name` in `00_meta/meta.json` |
| Version | 0.10 | `CORE_VERSION` in `20_view/web/xtgl_core.py`; `core_version` in `20_view/web/core_manifest.json` |
| Rule system | 13 chapters, 56 clauses (chapter 11 has 6 mandatory clauses, chapter 12 has 6 restrictive clauses) | see "Rule count convention" at the end of this section; counted clause by clause from the canonical z-series |
| License | Apache License 2.0 | repository root `LICENSE` and `10_rac/LICENSE`; the two are byte-identical |
| Copyright line | `Copyright 2026 Bumao` | `NOTICE` |
| Trademark | for the boundaries of use of the name and the logo see `TRADEMARK.md` at the repository root | physical file |
| Port | `127.0.0.1:8802` | `port` in `20_view/web/web_config.json` |
| Runtime | Python 3.12.14; the functional code uses only the standard library | import lists of the entry script and the core files |
| Front end | all of `20_view/web` is released with the repository, not stripped, not compressed, not obfuscated | physical directory |

**Rule count convention (the single authority)**: run the following in the community root

```
python -c "import json,glob; fs=sorted(glob.glob('10_rac/zhunze/z*.json')); print(len(fs),'章',sum(len(json.load(open(f,encoding='utf-8-sig')).get('clauses',[])) for f in fs),'条')"
```

The chapter counts / clause counts in this file, in the README and in the release tutorial must all follow the output of this command; do not copy them by hand.

## II. Core files and manifest convention

There are 13 core files under `20_view/web`, registered in `core_manifest.json`:

```
xtgl_core.py  serve.py  index.html  setup.html  tutorial.html
kernelsync.py  module_check.py  modules.json  snapshot.py
i18n.js  favicon.png  xtgl_clean.py  design_tokens.json
```

Among them, `kernelsync.py` and `module_check.py` are local tools and are not released.

`core_manifest.json` records the SHA256 of the above 13 files and is itself in the repository. Verification must be based on the physical files in the repository:

- files listed in the manifest must all be in the repository, and no core file outside the manifest may appear in the repository;
- after any core file is changed, the maintainer recomputes the manifest locally (local tool, not released);
- the version number is recognized only from `CORE_VERSION` in `xtgl_core.py` and `core_version` in `core_manifest.json`; this file establishes no separate version convention.

## III. Front end shipped with the package and the current state of SPDX marking

The front-end source is under the same license and the same sanitization standard as the backend:

- `index.html`, `setup.html`, `tutorial.html`, `i18n.js`, `design_tokens.json`, `favicon.png` are all released with the repository;
- the 4 shipped Python core files (`xtgl_core.py`, `serve.py`, `snapshot.py`, `xtgl_clean.py`) all carry `SPDX-License-Identifier: Apache-2.0` in their file headers;
- HTML and JS (`index.html`, `setup.html`, `tutorial.html`, `i18n.js`) currently **do not carry** SPDX comments; this item is still to be added;
- `modules.json` and `design_tokens.json` are data files and do not carry SPDX comments;
- the front end must not contain internal paths, internal role code names, private edition names or references;
- build artifacts, caches, `node_modules`, `*.bak*` and `*.tmp` are never included in the package.

## IV. Excluded from the package

- `web_config.local.json` (local private configuration)
- `__pycache__/`, `*.pyc`
- `*.bak*`, `*.tmp`, `*~`
- `node_modules/`
- any private configuration or other-edition files not listed in this repository
- local paths, machine names, user names, internal role code names, intranet addresses

## V. Self-check before release

1. Under `10_rac`, run `python BumaoXTGL_Community_v01.py check --strict`; the verdict must be `ALL PASS`;
2. Under `20_view/web`, verify that the hashes of the 13 files match `core_manifest.json` (done by the maintainer locally with the verification tool; local tool, not released);
3. Privacy rescan: zero hits for local paths, machine names, user names, internal role code names and intranet addresses;
4. Cold start: after unpacking in a clean directory, start the service directly; the home page opens and the wizard can be walked through;
5. Confirm that the package contains no `.bak` / `__pycache__` / `node_modules`.

## VI. License obligations

- distribution must retain the repository root `LICENSE` and `NOTICE`;
- modified files must be marked as changed;
- use of the name and the logo is governed by `TRADEMARK.md` at the repository root.

Maintainer: Bumao

This draft replaces the old draft of 2026-11-03 (the old draft has been moved into `90_lishi`). This draft states only verifiable physical facts inside the repository; old statements that did not match the physical files have been removed.
