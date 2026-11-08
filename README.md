# Bumao XTGL Community（规则版）

一句话：把「你想守的规矩」写成机器能检查的条目，每次动手前得到一个唯一的 `ALL PASS / FAIL` 结论。本仓自带 56 条通用规则、13 章结构和一个 Web 控制台。

- 运行时依赖：**纯 Python 标准库**，要求 **Python 3.12 或更高**，不需要 `pip install`。
- 本仓是四个独立仓库之一，**已内置内核**（`kernel/bumao_core/`），克隆后可直接运行。

## 内核已内置

入口脚本按 `10_rac/../kernel/bumao_core` 查找内核，内核随本仓一起分发，克隆后无需另装：

```
bumao-xtgl-community/
├── kernel/
│   └── bumao_core/            ← 已随本仓内置（源头为 bumao-core 仓）
├── 10_rac/
│   └── BumaoXTGL_Community_v01.py
└── 20_view/
```

内核只有一份源头：`bumao-core` 仓。内核更新时，用 `bumao-core` 的 `bumao_core/` **整目录覆盖**本仓 `kernel/bumao_core/`，不做逐文件合并；覆盖后比对哈希是否一致即可。

## 30 秒跑起来

```bash
cd 10_rac
python BumaoXTGL_Community_v01.py whoami
python BumaoXTGL_Community_v01.py check --strict
```

`check --strict` 输出唯一结论：功能类闸门应全绿；A10／A13／B15／B16／B24／B29 等「审批与留痕」闸门在没有团队内部台账时会如实报缺件——公开仓不携带内部审批与备份记录，这是预期差异，不是安装失败。首次 clone 的第一轮还会报 B19（尚无检查凭据）与 B22（无有效检查完成时刻），本轮结束时会写出 `30_taizhang/check_last.json`，第二轮起转为通过。

Web 控制台：

```bash
cd 20_view/web
python serve.py
```

默认端口 8802（见 `web_config.json`，端口被占用时会自动向后寻找并打印真实地址）。Windows 也可以直接双击 `20_view/web/qidong_kongzhitai.bat`。

## 六层结构

```
00_meta/       元信息、接入协议、版本单点、规则库与功能包
10_rac/        执行器与规则真身：入口脚本、render.py、rules_db.py、rules/
20_view/       只读视图区：渲染产物与 Web 控制台
30_taizhang/   变更与治理台账（只追加）
40_renwu/      任务执行区（交付物与过程稿）
90_lishi/      历史归档（只读）
```

规则真身在 `10_rac/rules/`，视图由 `render.py` 生成；**只改真身，不改视图**，否则下一轮渲染会覆盖你的改动。

## 常用命令（在 `10_rac/` 下执行）

| 命令 | 作用 |
|---|---|
| `python BumaoXTGL_Community_v01.py check --strict` | 全量闸门校验，唯一的放行结论 |
| `python BumaoXTGL_Community_v01.py whoami` | 接入自检与检查项体检 |
| `python BumaoXTGL_Community_v01.py audit` | 结构与条款统计 |
| `python BumaoXTGL_Community_v01.py show <条款id>` | 打印某条条款正文 |
| `python render.py write` | 真身 → 视图 |
| `python rules_db.py` | 重建派生索引 |

## 它不做什么

- 不做权限控制：它只能说「你违规了」，不能拦住你的手。
- 不做代码审查：它管行为纪律，不管代码写得好不好。
- 不保证规则内容本身正确：它只查自相矛盾、编号重复、视图漂移。

## 许可

Copyright 2026 Bumao

Licensed under the Apache License, Version 2.0. 全文见 [`LICENSE`](LICENSE)。
商标与品牌使用边界见 [`TRADEMARK.md`](TRADEMARK.md)。
贡献流程与 DCO 要求见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
安全问题请按 [`SECURITY.md`](SECURITY.md) 的私密渠道报告。
