# Bumao XTGL Community · 运行说明

这是**社区版控制台**：基础规则版，开箱即用，只读。不 mock、不联网、不需要数据库，也不需要 `pip install`。

- 本端：**Bumao XTGL Community v0.10**，规则真身在 `10_rac/zhunze/z00–z10.json`
- 端口：**8802**（以 `web_config.json` 的 `port` 为准）
- 内核：`xtgl_core.py`（本端自带，不依赖外部服务）
- 默认打开能力：`overview`、`gate`、`rules`、`log_day`、`rules_library`

---

## 30 秒启动

```bash
cd 20_view/web
python serve.py
```

前置只有 Python 3.8+。启动后终端打印地址，浏览器自动打开。

| 启动方式 | 命令 |
|---|---|
| 按配置启动 | `python serve.py` |
| 临时指定项目 | `python serve.py --root "/path/to/another-project"` |
| 演示数据 | `python serve.py --demo` |
| 换端口 | `python serve.py --port 8802` |
| 不开浏览器 | `python serve.py --no-browser` |

> 直接双击 `index.html` 不行：页面要调 `/api/*`，必须经 `serve.py`。

---

## 打开后你会看到什么

只有 **3 个页签、4 张卡**，这就是社区版的全部：

| 页签 | 卡片 | 数据来源 |
|---|---|---|
| 总览 | 闸门红绿 | `check --strict` 实跑 |
| 规则与模块 | 规则条款清单、条款检索 | `10_rac/zhunze/` 三层合并 |
| 运行与日志 | 工作日志（四层：当天 → 时间 → 项目 → 客户端） | `90_lishi/` 留档与日志 |

没有的（本端未开放，一律不显示、不采数）：AI 诊断、缺陷台账、接入名册、三端取数、路径地图、落盘导出、日志日历、备份归档。

想看更多功能，不要改代码——放包，见下面两节。

---

## 三层规则

优先级固定：**core > default > user**。

```json
"rules": {
  "core":    {"dir": "core_rules", "enabled": false},
  "default": {"dir": "zhunze",     "enabled": true},
  "user":    {"dir": "rules_user", "enabled": false}
}
```

- 用户层可新增条款，也可覆盖默认层；
- 用户层与内核层同编号时，用户条被拒绝，页面显示冲突，不静默覆盖；
- 相对目录先找 `10_rac/<目录>`，再找项目根 `<目录>`。

---

## 规则包：放一个，才多一条规则

规则包目录：`00_meta/rules_library/packs/`，格式见同目录 `schema.json`。

现成两个包，直接可用：

| 包 | 管什么 | 默认 |
|---|---|---|
| `packs/logging.json` | 日志与复审 | `enabled=false` |
| `packs/backup.json` | 备份与保留 | `enabled=false` |

启用只改一个字段：

```json
{ "id": "logging", "name": "日志与复审", "enabled": true, "rules": [ ... ] }
```

然后跑：

```bash
python 20_view/web/module_check.py
python 10_rac/BumaoXTGL_Community_v01.py check --strict
```

两条都过，包才算生效。`enabled=false` 的包不进快照、不生效、不显示。

红线：包里不写真身条款的标题／编号／正文，不写死天数、份数、条数，不自动启用。

---

## 功能包：放一个，才多一块面板

功能包目录：`00_meta/feature_packs/`。一个包一个 JSON：

```json
{
  "schema": 1,
  "id": "f01_jieru",
  "name": "接入名册",
  "name_en": "Client roster",
  "enabled": false,
  "capabilities": ["clients"],
  "applies_to": ["community", "minimal"],
  "note": "把日志 who 列汇总成接入名册"
}
```

- `capabilities` 只能写 `modules.json` 定义表里已有的 id；
- `enabled=true` 的包在启动时并入本端能力表，对应面板才出现；
- `enabled=false` 的包连数都不采，页签也不会多出来；
- 两个现成功能包：`f01_jieru.json`（接入名册）、`f02_lishi.json`（日志日历）。

启用方式同上：改 `enabled` 为 `true`，重启 `serve.py`。不想用就改回 `false`，面板立即消失，数据不动。

查看当前加载了哪些包：`GET /api/packages`。

---

## 日志四层

日志按 **天 → 时间 → 项目 → 客户端** 四层展示，缺一层就不完整：

1. **天**：`YYYY-MM-DD`，只认当天；
2. **时间**：`HH:MM:SS`，同一天内按时间排；
3. **项目**：`40_renwu/` 下一级目录名，wrapper 自动填；
4. **客户端**：日志 `who` 列，没登记就不算接入。

每次更新必须登记一条：

```bash
python 10_rac/BumaoXTGL_Community_v01.py log --file <本次留档> --what "..."
```

---

## 接口

| 接口 | 用途 |
|---|---|
| `GET /api/overview` | 元信息、规则层、条款、闸门 |
| `GET /api/clauses` | 某文件的条款 id 与首行 |
| `GET /api/tasks` | 任务目录与留档 |
| `GET /api/modules` | 能力定义表 |
| `GET /api/packages` | 规则包／功能包加载情况 |
| `GET /api/config` | 本端能力表 |
| `POST /api/setup/save` | 写 `web_config.json`（原子写 + `.bak` + 回读） |

除向导四个写接口外，控制台不修改项目文件。

---

## 边界

- 只监听 `127.0.0.1`，不做鉴权，不要暴露到局域网或公网；
- 必须经 `serve.py` 打开；
- 闸门是真实执行，项目大时会跑十几秒，不是卡死；
- 子进程统一 UTF-8，使用启动控制台的同一个解释器；
- 演示数据是合成的，页面会标「演示数据」。

---

## 自检

```bash
python module_check.py
python kernelsync.py --check
python -m unittest discover -s tests -v
```
