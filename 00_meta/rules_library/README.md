# rules_library —— 规则库预留槽位（默认不生效、不自动启用）

落点：每端 `00_meta/rules_library/`（宿主层）。端根目录受结构闸 B5b 约束（子目录名必须匹配两位编号），
所以库挂在 00_meta 下面、与运行期声明件同层；生效规则目录（`web_config.json` 的 `rules` 段所指）另在别处，两者分开。

一句话：这里只放「槽位」和「模板」，不放任何人的私有规则。本目录里的包全部 `enabled=false`。

## 目录
- `schema.json` —— 包格式定义，`module_check.py` 按它校验；
- `packs/` —— 五类预置空包，规则数组一律为空；
- `examples/` —— 示例模板，永不自动启用；照着改成自己的包再放进 `packs/`。

## 五类包
| 包 | 管什么 |
|---|---|
| `backup` | 备份与保留 |
| `audit` | 留痕与台账 |
| `credential` | 凭据与闸门 |
| `rollback` | 回滚与证据 |
| `logging` | 日志与复审 |

## 怎么从规则库挂一条规则（六步）
1. 复制 `examples/example-template.json`，改名放进 `packs/`；
2. 按 `schema.json` 填自己的规则——只写自己的动作与范围，**不写真身条款的标题／编号／正文**；
   阈值、天数、份数一律留空由自己填，仓库和代码里不预置任何数值；
3. 把该包的 `enabled` 改成 `true`（不改就永远不生效）；
4. 跑 `python 20_view/web/module_check.py`：包格式错必须 FAIL，格式对才继续；
5. 跑闸门 `check --strict`：必须全绿；
6. 打开前端「能力挂载」里的规则库行看现场计数——未启用的包不进快照，启用了才出现。

## 红线（违反任一条即视为破坏预留）
① 不含任何真身条款标题／编号／正文；② 不写死天数、份数、条数、版本；
③ 不预设行为、不自动启用；④ 空库时三端启动不崩（缺目录只提示，不报错）；
⑤ 只有 `enabled=true` 且规则非空的包才允许出现在快照里。

## 反向用例（自己造，验证拦得住拦不住）
- 把 `packs/` 里任一包改成坏 JSON → `module_check` 必须 FAIL；
- 删掉 `depends_on`，或把 `applies_to` 写成不存在的端，或依赖定义表里没有的能力 → 必须 FAIL；
- 删掉五类槽位中的任意一个 → 必须 FAIL；
- 把整个 `rules_library` 目录改名 → 不许崩：只提示「未建库」，快照该行显示「未建库（不影响启动）」。

---

## English

# rules_library — reserved slots for the rules library (inactive by default, never auto-enabled)

Location: `00_meta/rules_library/` in every edition (host layer). The edition root directory is constrained by structural gate B5b (subdirectory names must match a two-digit number),
so the library hangs under 00_meta, on the same level as the runtime declaration files; the active rules directory (the one pointed to by the `rules` section of `web_config.json`) is elsewhere, and the two are kept separate.

In one sentence: only "slots" and "templates" live here; nobody's private rules do. Every package in this directory has `enabled=false`.

## Contents
- `schema.json` — the package format definition; `module_check.py` validates against it;
- `packs/` — five preset empty packages, with rule arrays always empty;
- `examples/` — example templates that are never auto-enabled; copy one, turn it into your own package, and put it into `packs/`.

## The five package types
| Package | What it governs |
|---|---|
| `backup` | Backup and retention |
| `audit` | Trace records and ledgers |
| `credential` | Credentials and gates |
| `rollback` | Rollback and evidence |
| `logging` | Logs and review |

## How to mount a rule from the rules library (six steps)
1. Copy `examples/example-template.json`, rename it, and put it into `packs/`;
2. Fill in your own rules according to `schema.json` — write only your own actions and scope, **do not write the titles / numbers / text of the canonical clauses**;
   leave thresholds, days and counts blank for you to fill in yourself; neither the repository nor the code presets any values;
3. Set the package's `enabled` to `true` (leave it unchanged and it will never take effect);
4. Run `python 20_view/web/module_check.py`: a malformed package must FAIL; continue only when the format is correct;
5. Run the gate `check --strict`: it must be all green;
6. Open the rules library row under "Capability Mounting" in the front end and check the live count — packages that are not enabled do not enter the snapshot; only enabled ones appear.

## Red lines (violating any one of them is considered breaking the reservation)
① Contain no titles / numbers / text of any canonical clause; ② do not hard-code days, counts, clause counts or versions;
③ do not preset behaviour and do not auto-enable; ④ with an empty library, all three editions start without crashing (a missing directory only produces a notice, not an error);
⑤ only packages with `enabled=true` and non-empty rules are allowed to appear in the snapshot.

## Negative test cases (build them yourself to verify the blocks hold)
- Change any package in `packs/` into bad JSON → `module_check` must FAIL;
- Delete `depends_on`, or set `applies_to` to a non-existent edition, or depend on a capability absent from the definition table → must FAIL;
- Delete any one of the five slot types → must FAIL;
- Rename the whole `rules_library` directory → it must not crash: only notice "library not created", and that snapshot row displays "library not created (does not affect startup)".
