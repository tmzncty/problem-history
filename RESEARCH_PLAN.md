# RESEARCH_PLAN.md — Problem History

## Phase 0 — Method calibration

- [ ] `docs/METHOD.md`：Problem Episode、formulation、presupposition、answer-space、competition；
- [ ] `docs/FAILURE-MODES.md`：至少 10 类后见之明/同词同问题/线性进步等错误，并配 AI 自检问题；
- [x] `schemas/problem-episode.schema.json`（Draft 2020-12 原型、虚构 fixtures 与 validator）；
- [x] 关系类型：continuous / reformulated / transformed_successor / split / merged / displaced / revived / analogy_only / unrelated / undetermined；
- [x] source citation 最小规范（见 `docs/DATA_MODEL.md`）；
- [ ] 5 段历史文本的双-agent 校准 fixture。

验收：能稳定区分“明确问题 / 可支持前提 / 研究者推断”。若做不到，先改方法。

## Phase 1 — Pilot selection

对五个候选做小型查重：

1. 文学有什么用；
2. 知识与身份；
3. 机器能否思考；
4. 技术是否替代劳动；
5. 现代国家/现代化。

每个候选至少记录：重要研究 ≥2、可能历史断点 ≥3、一手材料可得性、跨 50 年可能性、最严重后见之明风险、与概念史/思想史重叠程度。

产物：`research/pilot-selection.md`。选择最适合验证方法的 pilot，而不是最宏大的题目。

## Phase 2 — Source pack

为选定 pilot 建立可定位的一手材料包：

- [ ] 不同时点的历史文本；
- [ ] 制度/教育/出版/技术语境材料（按题目需要）；
- [ ] edition/page/date metadata；
- [ ] 竞争群体材料；
- [ ] 明确记录缺失与代表性偏差。

此阶段只证明材料基础，不急着写总论。

## Phase 3 — Three Problem Episodes

至少建立 3 个真正可区分的 episode。每个包含：

- context；
- actor formulation；
- vocabulary/institutions；
- presuppositions；
- competing formulations；
- answer space；
- ≥3 条一手证据；
- predecessor/successor relation；
- hindsight risk；
- 为什么它不是“同一永恒问题换个人回答”的论证。

## Phase 4 — Synthesis

写 `synthesis.md`，重点解释 formulation 和可问范围如何改变。不得预设一定存在“旧问题被新问题取代”；只有材料支持时才这样判断。

同时生成一张问题变形图，允许分叉、竞争、断裂和 dormant，不强迫线性链。

## Phase 5 — Failure cases

建立 `studies/failure-cases/`，至少覆盖：

- 同词异问题；
- 异词近连续；
- 不同群体互不承认对方问题；
- 后人理论化实践困境；
- 问题无答案地消失。

用这些反例检验 schema 和 METHOD。

## Phase 6 — Computational assistance

只有 Phase 3–5 稳定后才做：关键词/搭配、semantic shift、context neighborhood、citation/co-occurrence、LLM candidate extraction。

所有结果只能标记 candidate/lead/anomaly，并附回到原文的核验链。

## Phase 7 — Multi-problem relations

成熟后才探索多个问题如何产生、阻塞、重构彼此。此阶段才值得做图谱/UI；可视化不得先于研究模型。

## 每阶段门禁

- 一手文本可定位；
- inference 显式；
- 主动找竞争框架和反例；
- 不按今天的问题强迫过去；
- 不以算法输出代替史料判断；
- checkpoint 后继续。
