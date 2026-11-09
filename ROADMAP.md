# Roadmap

问题史先做方法实验，再谈平台、图谱或大规模语料。

## M0 — 方法校准

- [x] `docs/METHOD.md`：Problem Episode 定义与执行流程；
- [x] `docs/IDENTITY-CHECK.md`：问题同一性、连续性与后继关系的裁决规则；
- [x] `docs/FAILURE-MODES.md`：后见之明、永恒问题幻觉、同词=同问题等错误；
- [x] `schemas/problem-episode.schema.json`（Draft 2020-12 原型、虚构 fixtures 与 validator）；
- [x] 设计边类型：`continuous / reformulated / transformed_successor / split / merged / displaced / revived / analogy_only / unrelated / undetermined`；
- [x] 建立 source citation 最小规范：`docs/SOURCE-CITATION.md`；数据合同细节见 `docs/DATA_MODEL.md`。

### M0 验收

找 5 段历史文本，让两个 Agent 独立判断：文本中“明确问题”“隐含前提”“研究者推断”分别是什么。若无法稳定区分，先改方法，不做图谱。

另外准备至少 7 组 `identity fixtures`，覆盖：

- 同词但问题断裂；
- 换词但问题连续；
- 行动者宣称连续、研究者判断断裂；
- 后人制造传统谱系；
- 问题失去 askability；
- A 导致 B 但 A ≠ B；
- 只能保留 `undetermined` 的证据冲突案例。

两个 Agent 必须分别给出 continuity evidence 与 discontinuity evidence。若只能输出标签、不能解释裁决，则 identity 模型不通过。

---

## M1 — 候选问题选择，而不是拍脑袋开题

对以下方向做小型 literature survey：

- 文学有什么用？
- 知识与身份的关系；
- 机器能否思考？
- 技术是否替代劳动？
- 现代国家/现代化问题。

每个候选都必须回答：

- 已有概念史/思想史研究多不多？
- 是否能获得跨至少 50 年的一手材料？
- 是否真的能看到 formulation 变化？
- 是否容易被今天的问题倒灌？

选一个最适合做 pilot 的，不求最宏大。

产物：`research/pilot-selection.md`。

---

## M2 — 单问题、三情境 pilot

选择一个问题，至少建立 3 个 Problem Episodes。

每个 episode 必须有：

- [ ] 时间与社会/制度语境；
- [ ] 历史行动者自己的问题表述；
- [ ] presuppositions；
- [ ] 同时期竞争表述；
- [ ] 可接受答案空间；
- [ ] 至少 3 条一手证据；
- [ ] 与前后 episode 的关系说明；
- [ ] 通过 `docs/IDENTITY-CHECK.md` 的 episode relation 检查；
- [ ] “为什么不是同一个问题换了个人说”论证。

### 验收

最终 synthesis 中至少出现一次：

> “旧问题没有被回答，而是被另一个问题框架取代。”

但只有证据真的支持时才能这样写；不能为了满足验收硬凑。

---

## M3 — 反例与失败案例

主动找会破坏方法的材料：

- 同一个词，问题完全不同；
- 不同词，问题结构高度连续；
- 历史行动者互相不承认对方问题；
- 后人把一个实践性困境重写成理论问题；
- 一个问题突然消失，却没有“解决方案”。

产物：`studies/failure-cases/`。

目标：证明数据模型能表达历史歧义，而不是逼所有材料进入线性演化链。

---

## M4 — 计算辅助发现

只有 M2/M3 稳定后才引入计算方法。

候选：

- 关键词/搭配变化；
- topic/context neighborhood；
- lexical semantic shift；
- citation/co-occurrence network；
- LLM 生成“候选 problem formulation”。

### 强制边界

计算输出只能标为：

```text
candidate / lead / anomaly
```

不能自动升级为历史结论。

所有重要变化仍需人工/Agent 回到原始文本核验。

特别禁止：

```text
semantic similarity → problem identity
```

任何自动建议的 episode relation 都必须经过 `IDENTITY-CHECK`，并显式保存正反证据。

---

## M5 — 多问题交叉

成熟后研究问题之间的关系：

```text
Problem A
   ├─ produces → Problem B
   ├─ blocks   → Problem C
   └─ reframes → Problem D
```

例如某种“知识身份”变化是否使新的“文学功能”问题成为可能。

这一步才值得做图谱/UI。

---

## AI 可直接领取的第一批任务

### Task A — 方法谱系阅读

基于 `docs/PRIOR_ART.md`，分别写 1–2 页：Collingwood、Skinner、Koselleck、Foucault 对本项目的“可借用部分”和“不能混同部分”。要求引用一手/权威资料，不写泛泛人物介绍。

### Task B — Pilot 候选调查

对 README 中 5 个问题做已有研究查重。每个问题找至少：

- 2 本/篇重要学术研究；
- 3 个可能的历史断点；
- 一手材料可得性；
- 最严重的后见之明风险。

### Task C — Schema 原型

创建 `schemas/problem-episode.schema.json` 和 3 个虚构 fixture，只测试数据表达能力；不要把虚构 fixture 当历史事实。

### Task D — Failure Modes

建立 `docs/FAILURE-MODES.md`，至少写 10 种常见错误，并为每种设计“AI 自检问题”。

### Task E — Identity Fixtures

基于 `docs/IDENTITY-CHECK.md`，建立至少 7 组 pair fixtures。第一轮可以全部虚构，只测试：

- relation 是否足够表达歧义；
- Agent 能否区分 lexical continuity 与 problem continuity；
- Agent 是否会主动寻找 counterevidence；
- `analogy_only` / `undetermined` 是否真的会被使用，而不是所有东西都被连成演化链。

通过后再换成真实历史材料。

## Stop conditions

出现以下情况时先停：

- 只有今天的研究者使用该问题表述，找不到历史行动者证据；
- 研究其实已经是成熟概念史，只是换名叫问题史；
- 分期完全依赖政治年代而非问题结构变化；
- LLM 相似度成为唯一证据；
- 为了画漂亮图强迫复杂争论变成一条线；
- 为了维持一个既定 problem lineage，忽略核心 presupposition 已经崩塌的证据。

问题史的价值首先来自**问题本身被历史化**，不是来自数据库规模。
