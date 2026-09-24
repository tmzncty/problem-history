# Problem History · 问题史

> 不以“谁提出了什么答案”为中心，而追踪：一个问题何时出现、如何被表述、为什么在当时成为问题、后来又怎样变形或消失。

## 核心想法

通常的思想史容易写成：

```text
人物 A → 理论 A
人物 B → 理论 B
人物 C → 理论 C
```

问题史试图换一个主语：

```text
某个时代的人为什么会开始问 X？
        ↓
X 当时到底是什么意思？
        ↓
有哪些可接受/不可接受的回答？
        ↓
什么变化使 X 被重新表述成 X'？
        ↓
旧问题是真的解决了，还是失去了被提问的条件？
```

因此，本项目的基本单位不是“思想家”或“概念”，而是 **Problem Episode（问题情境）**。

## Problem Episode 建议模型

```yaml
problem_id: knowledge-and-identity
period: 1895-1919
formulation:
  - "..."
actors:
  - "..."
presuppositions:
  - "..."
vocabulary:
  - "..."
institutions:
  - "..."
answer_space:
  accepted: []
  marginal: []
  impossible_or_unthinkable: []
evidence: []
predecessors: []
successors: []
status: transformed   # emerged / active / transformed / displaced / dormant
```

## 和邻近方法的区别

### 不是普通“思想史”

不先设定一组永恒的大问题，再找历代名人回答。

### 不是单纯“概念史”

概念史非常重要，但“词义变化”不等于“问题结构变化”。同一个词可以服务于完全不同的问题；同一个问题也可能改用另一套词汇表达。

### 不是“某问题研究综述”

综述关心今天的研究者怎么回答；问题史首先问历史行动者当时究竟把什么视为问题。

### 不追求最后答案

一个问题可能被解决，也可能被制度变化、知识分类变化、语言变化或关注点转移直接取消。

## 方法约束

1. **先证明问题存在，再讨论答案。** 不允许用后见之明替历史人物发问。
2. **恢复当时的可问范围。** 什么能问、不能问、无需问，本身就是历史事实。
3. **表述变化不是装饰。** 问题从 A 变成 B，可能意味着前提已经变化。
4. **区分问题、症状、答案。** 后人认为的“问题”未必是当事人自觉的问题。
5. **反对目的论。** 不能把过去写成通往今天正确答案的预备阶段。
6. **保留竞争问题框架。** 同一时期不同群体可能根本不承认对方的问题设定。

## 第一批适合试做的题目

这些只是测试题，不预设结论：

- “文学有什么用？”如何在不同制度环境中被重新提出；
- “知识如何成为一种身份？”从士、学者、专家到职业知识人的变化；
- “机器能否思考？”在计算机、控制论、AI 不同时期的提问结构；
- “中国如何成为现代国家？”不同阶段的问题前提如何变化；
- “技术会不会替代人？”机械化、自动化、计算机化、AI 化是否真是同一个问题。

## 推荐目录

```text
problems/
└── <problem-id>/
    ├── README.md
    ├── episodes/
    │   ├── 01_<period>.md
    │   └── 02_<period>.md
    ├── sources.md
    ├── formulations.csv
    └── synthesis.md

docs/
├── PRIOR_ART.md
├── METHOD.md
└── DATA_MODEL.md

schemas/
└── problem-episode.schema.json

fixtures/problem-episodes/
└── 纯虚构的 schema 校准案例
```

数据字段、最小引用规范、虚构 fixture 和本地验证命令见 [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)。Schema 只检查论证结构与引用关系，不自动裁决历史结论。

## 第一阶段验收

- [ ] 建立方法文献地图，明确与 Collingwood、Skinner、Koselleck、Foucault 等路径的关系；
- [ ] 选择一个跨度至少 50 年的问题；
- [ ] 找出至少 3 次问题表述真正发生变化的节点；
- [ ] 每个节点给出原始文本证据；
- [ ] 单独列出“后见之明风险”；
- [ ] 最后形成一张“问题如何变形”的图，而不是人物观点排行榜。

## 一个最重要的提醒

**不要因为今天可以用一句话提出某个问题，就假定过去的人也在问同一句话。**

问题本身需要被历史化。
