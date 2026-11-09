README-HX.txt · Bumao XTGL Community 工作区导航（唯一入口）

【品牌定位 · 2026-11-03】本产品 = **Bumao XTGL Community（开源基础版）** = Bumao Core + 通用规则。
只含 Bumao Core 极小内核与通用规则；发行差异只在发行配置与预置内容，**规则不进内核**。
============================================================
本文件是本产品的唯一入口，位于产品目录之内、随产品一起流动。
新会话第一件事是全文读本文件；未读即视为未接入，不得执行任何写操作。
上级目录中的同名文件或指针不属于本产品，不参与任何闸门校验。

一、这是什么
------------------------------------------------------------
AI 治理引擎，内核是「多 Agent 角色与路由治理」。
只保留通用治理机制：工作区分层、真身／视图／台账三层、闸门与审计、版本规则。
当前版本 0.33（2026-11-09）。版本号只认 00_meta\meta.json 的 version 字段，
本文件任何文字与 meta 冲突时以 meta 为准。

二、版本与条款
------------------------------------------------------------
版本独立维护；条款变更在本产品 30_taizhang 登记「已落地／未落地＋原因」。

三、六层结构（00_meta / 10_rac / 20_view / 30_taizhang / 40_renwu / 90_lishi）
------------------------------------------------------------
00_meta       元信息、接入协议、版本单点、私域词表、检查项登记表、新手指导
10_rac        执行器与唯一真身 zhunze\
20_view       唯一视图区，render.py 独占写入
30_taizhang   变更与治理台账（只追加）
40_renwu      任务执行区（交付物与过程稿）
90_lishi      历史归档，只读

四、三层资产
------------------------------------------------------------
真身 zhunze\z00..z10.json  唯一可改的数据源
视图 20_view\               真身渲染出的只读产物，可随时重建
台账 30_taizhang\           只记事实与流程留痕，不复制条款正文
流向单向：真身 → 视图。

五、接入三步（顺序不可颠倒）
------------------------------------------------------------
① 读本文件，取得产品名、版本与真身位置；
② 按需读 20_view\ 下的对应分章或全文归档；
③ python BumaoXTGL_Community_v01.py check --strict   ← 必须 ALL PASS 才允许动手
改法四步：① 改 zhunze\z*.json → ② render.py write → ③ check --strict →
④ 记账到 30_taizhang\biangeng_zhang.txt。缺失任一步，改动视为未生效。

新手请先读 00_meta\XINSHOU-ZHINAN.txt（十分钟上手，含三个最常犯的错）。

六、0.8 新增的四条（都是「怎么算干完」）
------------------------------------------------------------
4.3  交付完成度五档（S0 立项 / S1 在研 / S2 可运行 / S3 已验收 / S4 已归档），
     百分比只由档位换算，不许手填；允许降档且必须降。
4.4  两条健康分开判：宿主健康（A）与规则系统健康（B）各给结束判据，
     不许合成一个总分；两者都结束才叫「闭环」。
5.3  状态可人工覆盖：系统判定只是基线，人工勾的写覆盖文件并留 by/at，
     但覆盖不得绕过闸门。
8.3  每日工作登记：一行一条六列，详细指向必须真实存在，滚动保留只迁不删。

七、产品化红线
------------------------------------------------------------
· 任何文件不得出现盘符、用户目录、机器名等部署信息，路径由脚本运行时溯源。
· 整个工作区可整体拷贝至任意机器直接运行。
· 凭据一律走环境变量，产品内不允许出现密钥字面值。
· 上述三条由闸门 B6 / B6b / B7 逐轮机器校验，不由人眼保证。

八、常用命令（在 10_rac\ 下执行）
------------------------------------------------------------
python BumaoXTGL_Community_v01.py check --strict   闸门全量校验
python BumaoXTGL_Community_v01.py whoami           接入自检与检查项体检
python BumaoXTGL_Community_v01.py audit            结构与条款统计
python BumaoXTGL_Community_v01.py show <条款id>    打印某条正文
python render.py write            真身 → 视图
python rules_db.py                重建派生索引 rules.json
============================================================
【本文件结束】

---

## English

README-HX.txt · Bumao XTGL Community Workspace Navigation (Single Entry Point)

[Brand Positioning · 2026-11-03] This product = **Bumao XTGL Community (open-source base edition)** = Bumao Core + generic rules.
It contains only the minimal Bumao Core kernel and generic rules; edition differences lie only in distribution configuration and preset content, and **rules do not enter the kernel**.
============================================================
This file is the single entry point of this product. It lives inside the product directory and travels with the product.
The first thing in a new session is to read this file in full; not having read it counts as not connected, and no write operation may be executed.
A file of the same name or a pointer in the parent directory does not belong to this product and does not take part in any gate check.

1. What this is
------------------------------------------------------------
An AI governance engine whose kernel is "multi-agent roles and routing governance".
It retains only the generic governance mechanisms: workspace layering, the true-body/view/ledger three layers, gates and audit, and version rules.
Current version 0.33 (2026-11-09). The version number is recognized only from the `version` field of 00_meta\meta.json;
if any text in this file conflicts with meta, meta prevails.

2. Versions and clauses
------------------------------------------------------------
Versions are maintained independently; clause changes are registered in this product's 30_taizhang as "landed / not landed + reason".

3. Six-layer structure (00_meta / 10_rac / 20_view / 30_taizhang / 40_renwu / 90_lishi)
------------------------------------------------------------
00_meta       metadata, onboarding protocol, single version point, private vocabulary, check-item registry, newcomer guide
10_rac        executor and the sole true body zhunze\
20_view       the sole view area, written exclusively by render.py
30_taizhang   change and governance ledger (append-only)
40_renwu      task execution area (deliverables and working drafts)
90_lishi      historical archive, read-only

4. Three-layer assets
------------------------------------------------------------
True body zhunze\z00..z10.json   the only editable data source
Views 20_view\                   read-only products rendered from the true body, rebuildable at any time
Ledger 30_taizhang\              records only facts and process traces; does not copy clause bodies
Flow is one-directional: true body → views.

5. Three onboarding steps (order must not be reversed)
------------------------------------------------------------
① Read this file to obtain the product name, version, and true-body location;
② Read the corresponding chapters or the full-text archive under 20_view\ as needed;
③ python BumaoXTGL_Community_v01.py check --strict   ← must be ALL PASS before you may act
Four steps to make a change: ① edit zhunze\z*.json → ② render.py write → ③ check --strict →
④ record in 30_taizhang\biangeng_zhang.txt. If any step is missing, the change is considered not in effect.

Newcomers should first read 00_meta\XINSHOU-ZHINAN.txt (ten minutes to get started, including the three most common mistakes).

6. The four items added in 0.8 (all about "what counts as done")
------------------------------------------------------------
4.3  Five levels of delivery completeness (S0 initiated / S1 in progress / S2 runnable / S3 accepted / S4 archived);
     the percentage is converted only from the level and may not be filled in by hand; downgrading is allowed and, when required, mandatory.
4.4  Two kinds of health are judged separately: host health (A) and rule-system health (B) each have their own end criteria;
     they may not be merged into a single score; only when both have ended is it called a "closed loop".
5.3  Status may be manually overridden: the system verdict is only a baseline; manual ticks write an override file and retain by/at,
     but an override must not bypass a gate.
8.3  Daily work log: one line per entry with six columns; the detailed pointer must really exist; rolling retention only moves entries and never deletes them.

7. Productization red lines
------------------------------------------------------------
· No file may contain drive letters, user directories, machine names, or other deployment information; paths are resolved by scripts at runtime.
· The entire workspace can be copied as a whole to any machine and run directly.
· Credentials always go through environment variables; literal secret values are not allowed inside the product.
· The three items above are machine-checked each round by gates B6 / B6b / B7; they are not guaranteed by human eyes.

8. Common commands (run under 10_rac\)
------------------------------------------------------------
python BumaoXTGL_Community_v01.py check --strict   full gate check
python BumaoXTGL_Community_v01.py whoami           onboarding self-check and check-item physical exam
python BumaoXTGL_Community_v01.py audit            structure and clause statistics
python BumaoXTGL_Community_v01.py show <clause id> print the body of a clause
python render.py write            true body → views
python rules_db.py                rebuild the derived index rules.json
============================================================
[End of this file]
