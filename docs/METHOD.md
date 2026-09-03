# METHOD.md — Problem History operational method

> **状态：M0 core method / working normative protocol**  
> 本文件定义仓库当前实际使用的 Problem Episode 研究流程。它不是一套声称来自某位理论家的完整学说，而是从 Collingwood、Skinner、Koselleck、Foucault，以及本仓已经完成的 identity / negative-evidence / source-provenance 工作中抽取出来的**可执行研究约束**。
>
> 深入依据见：
>
> - `docs/method-lineage/COLLINGWOOD.md`
> - `docs/method-lineage/SKINNER.md`
> - `docs/method-lineage/KOSELLECK.md`
> - `docs/method-lineage/FOUCAULT.md`
> - `docs/IDENTITY-CHECK.md`
> - `docs/NEGATIVE-EVIDENCE.md`
> - `docs/SOURCE-CITATION.md`

---

## 0. 本仓到底研究什么

Problem History 研究的不是“伟大人物如何回答永恒问题”，而是：

```text
某种困难 / 对象 / 实践 / 争论
        ↓
在特定历史条件下变得可见、可问、值得问
        ↓
行动者形成一个或多个 problem formulations
        ↓
不同群体争夺问题的定义、前提与答案空间
        ↓
问题持续、改写、分裂、合并、被替代、休眠、复活
        ↓
有时最终不再按原来的结构可问
```

因此研究对象不是孤立命题，而是**历史上可定位的问题情境**。

本仓最核心的研究纪律是：

> **先证明历史行动者确实在面对某种问题，再讨论他们给出了什么答案。**

---

## 1. Working definition：什么是一个 Problem Episode

一个 **Problem Episode** 是：

> 在一个可界定的历史情境中，一组行动者围绕某个被他们显式提出、或能够由同时代证据可靠重建的问题，形成了可辨认的 stakes、presuppositions、answer space 与竞争性表述；这些结构足以与前后时期的问题情境做历史比较。

它不是：

- 一个现代研究标题；
- 一个关键词的出现期；
- 一个思想家的“观点条目”；
- 一项客观困难本身；
- 某个理论概念的全部历史；
- 一个后人为了叙事方便制造的永恒问题。

### 1.1 Episode 的粒度

一个 episode 应小到可以回答：

- 谁在问？
- 在什么 forum / institution / practice 中？
- 为什么现在值得问？
- 什么说法当时算一个可能答案？

同时又应大到允许：

- 至少一组竞争 formulation；
- 多条一手材料互证；
- 与前后 episode 做 relation 判断。

如果只能写成“18 世纪的人讨论自由”，粒度过大。

如果只能写成“某作者某页出现一个问号”，粒度过小。

---

## 2. 四个必须分开的认识层

任何写作都必须区分下列层次；它们不得在 prose 中悄悄滑动。

### 2.1 `actor_explicit`

历史行动者明确提出、命名或以可识别方式表述的问题。

证据例：

- 明确疑问句；
- “当前的问题是……”；
- “我们必须解决……”；
- 对方明确回应某一被提出的问题；
- 会议议题、制度问题单、正式争论题目。

这是最强的 formulation evidence，但仍需检查体裁、修辞、受众与版本。

### 2.2 `actor_reconstructed`

历史行动者未必留下一个整齐的问句，但同时代材料足以支持：

> 这组言论 / 行动可合理理解为在处理 Q。

这是**历史重建假说**，不是原文内容。

它必须通过本文件第 5 节的 reconstruction gates。

### 2.3 `later_reconstruction`

后来的参与者、官方叙事、学者或传统把早期材料重新组织成某个问题。

例如：

- 后人说“他们当时真正争论的是 X”；
- 某学科史把更早材料编入自己的前史；
- 政治/机构纪念叙事把旧争论重新命名。

这类材料可以非常重要，但它首先证明的是**后来的人如何重构过去**。

除非有独立证据，不得倒推成早期行动者自己的 formulation。

### 2.4 `researcher_analytic`

今天研究者为了比较、解释或建模而提出的问题。

它完全合法，例如：

> “这些材料是否都涉及知识与身份的关系？”

但必须标成研究者层，不得写成：

> “从古代开始，人们一直在问‘知识与身份是什么关系’。”

### 2.5 一个简单自检

每次出现一句类似：

> “当时真正的问题是……”

必须立刻追问：

```text
谁这样说？
原文在哪里？
如果不是明确说的，重建依赖哪些独立证据？
这个表述中的关键词当时可用吗？
是否其实只是今天的便利改写？
```

---

## 3. Problem Episode 的核心组成

正式 episode 至少处理以下字段。字段未必立即进入 JSON Schema，但研究笔记必须能回答这些问题。

### 3.1 Period / scope

记录：

- 起止时间；
- 地区；
- relevant institutions / forums；
- 主要行动者与受众；
- 为什么选择这个边界。

禁止只因为王朝、战争、政权更替或十年整数而切 episode。

时间边界应尽量由 problem structure 的变化支持。

### 3.2 Formulation evidence

至少保存：

```yaml
formulation:
  type: actor_explicit | actor_reconstructed | researcher_analytic
  text: "..."
  source_links: []
  confidence: high | medium | low | undetermined
```

若是 `actor_reconstructed`，还必须保存 reconstruction rationale 与 counterevidence。

### 3.3 Stakes

问题为什么值得问？

检查：

- 理论困难；
- 制度风险；
- 职业/身份利益；
- 道德或宗教后果；
- 政策/技术后果；
- 谁承担“不解决”的代价。

同一句话在 stakes 根本不同的历史情境中，可能已经不是同一个问题。

### 3.4 Presuppositions

问题成立所依赖的前提，例如：

- 对象分类；
- 人的类型；
- 制度角色；
- 权威来源；
- 技术能力；
- 因果观念；
- 正常/异常标准；
- 哪些事实被当作理所当然。

Presupposition 不能因为“逻辑上好像需要”就直接写成 actor belief。

至少区分：

```text
explicitly stated
contextually supported
researcher inferred
```

### 3.5 Answer space

研究的不只是已经出现过的答案，还要尽可能恢复：

```text
accepted / mainstream
contested / marginal
possible but disfavored
unthinkable / category error
unknown
```

只有证据支持时才写 `unthinkable`。

“没有看到某答案”通常不足以证明它不可想象。

### 3.6 Competing formulations

不要假定一个时期只存在一个统一问题。

至少问：

- 不同群体是否把“同一困难”定义成不同问题？
- 某群体是否拒绝对方的问题前提？
- 是否存在 rival framing？
- 是否有人试图把问题从一个 domain 移到另一个 domain？

竞争 formulation 往往比“主流答案列表”更能显示问题如何变形。

### 3.7 Askability

Askability 不是“能不能用语法造出一句问句”，而是：

> 在当时的语言、分类、制度、知识、技术与实践条件下，这个问题为什么能够成为一个有意义、可讨论、需要回应的问题？

可检查：

- available vocabulary；
- relevant classifications；
- institutional jurisdiction；
- measurement / recording practices；
- recognized roles；
- accepted authorities；
- practical pressures；
- public / private forums。

---

## 4. 方法谱系如何转成仓库规则

这部分只说明“借什么”，不把几位作者混成一套 doctrine。

### 4.1 Collingwood：从答案恢复问题，但 reconstruction 必须受证据约束

Collingwood 的 question-and-answer 路线支持：

```text
statement 的历史意义
不能脱离它被当作什么问题的回答
```

但本仓额外增加两条限制：

1. 不能只从同一段 answer 循环推出 Q，再拿 Q 回头证明 answer 的意义；
2. `actor_reconstructed` 必须有独立同时代证据。

参考：R. G. Collingwood, *An Autobiography* (1939), esp. ch. 5；现代 question-logic 讨论可参见 SEP “Questions”。

### 4.2 Skinner：actor-available language 与 speech act

Skinner 对“fundamental concepts / abiding questions”的批评直接约束本仓：

> 不得先设定一组跨时代恒定问题，再把历史作者排成答题者。

同时必须区分：

```text
what is being said
what problem it addresses
what the actor is doing by saying it
```

一段话可能是在反驳、辩护、讽刺、合法化、重新命名或划界。

因此 `actor_reconstructed` 还要通过 actor-language admissibility：研究者重建的描述必须能在当时可用语言/概念/惯例中得到支持，或者明确标记为现代 paraphrase。

参考：Quentin Skinner, “Meaning and Understanding in the History of Ideas” (1969; revised in *Visions of Politics*, 2002)。

### 4.3 Koselleck：词汇、语义、概念、问题连续性分层

本仓强制区分：

```text
lexical continuity
semantic continuity
conceptual continuity
problem continuity
```

它们不能自动升级。

同一词可以承担不同历史功能；不同词也可能服务于高度连续的问题结构。

概念史 evidence 对 problem history 很重要，但不能替代 stakes / presuppositions / answer space / askability 的判断。

参考：Reinhart Koselleck, “Begriffsgeschichte and Social History”。

### 4.4 Foucault：difficulty 不等于 problem；problematization 是历史过程

最重要的硬边界：

```text
historical difficulty
≠
historical problem
```

某个贫困、疾病、制度失灵或技术限制可以长期存在，却尚未按后来熟悉的方式成为 thought / policy / ethics 的问题。

研究 emergence 时必须寻找：

- familiar practice 失去当然性；
- questioning / contestation；
- object formation；
- competing responses；
- institutions / practices 开始围绕它重组。

参考：Michel Foucault, “Polemics, Politics and Problematizations,” interview with Paul Rabinow (May 1984)。

### 4.5 Negative evidence：silence 必须解释它在哪一层产生

见 `docs/NEGATIVE-EVIDENCE.md`。

至少区分：

- actor silence；
- source silence；
- archive silence；
- retrieval silence；
- later narrative silence。

因此：

```text
search result = 0
```

从来不能自动升级成：

```text
actor did not ask Q
Q disappeared
Q became unaskable
```

### 4.6 Source provenance：citation 必须绑定 claim

见 `docs/SOURCE-CITATION.md`。

一个来源不是“高/低证据”单轴对象。

必须问：

- 哪个 version？
- 哪个 locator？
- 是 facsimile、OCR 还是编辑文本？
- 它和历史行动的 temporal / participant relation 是什么？
- 它究竟支持哪条 claim？

---

## 5. `actor_reconstructed` 的七道 gate

只有通过下面的门，研究者才可以把一个现代重述升级为 `actor_reconstructed`。

### Gate 1 — Source identity / locator

至少有一条可重新定位的 source，符合 `SOURCE-CITATION.md`。

如果关键依据只是搜索摘要、无页码摘录、二次转载或 OCR hit，不能进入高置信 reconstruction。

### Gate 2 — Independent support

不能只用“看起来像答案”的同一段文本倒推出问题。

至少寻找一种独立支持，例如：

- 前后文明确提问；
- 对手文本；
- 同一争论中的回应；
- 会议/制度议程；
- 作者其他文本；
- 同时期术语和分类；
- audience uptake。

### Gate 3 — Actor-language admissibility

问：

> 如果把研究者的 Q 翻回当时，这个描述在行动者的概念与语言空间中是否可理解？

可能状态：

```text
supported
contested
unsupported
undetermined
```

现代分析术语可以使用，但必须标成 modern paraphrase。

### Gate 4 — Speech-act / interaction context

确认文本在当时是在：

- 回答；
- 反驳；
- 规避；
- 讽刺；
- 合法化；
- 转移问题；
- 改写对手问题；
- 或进行其他行动。

不要把一句修辞话语机械当作字面问题陈述。

### Gate 5 — Difficulty / problematization distinction

如果依据只是“客观上发生了困难”，不能升级。

还需 actor-side evidence 证明该困难已经被问题化：质疑、争论、分类、改革、诊断、制定 response field 等。

### Gate 6 — Rival formulations / counterevidence

主动找至少一种 competing reading。

例如：

- 另一群体是否定义成别的问题？
- 有材料显示行动者并不接受我们重建的前提吗？
- 同一句话是否可解释为另一 speech act？

如果 rival explanation 同样强，保留 `undetermined`。

### Gate 7 — Hindsight audit

最后问：

```text
这个 formulation 中哪些词来自今天？
哪些分类是后来才稳定的？
如果删掉现代术语，行动者的问题还剩什么？
我们是不是因为已经知道后来结局，才把早期资料组织成这一问？
```

未通过时降级为 `researcher_analytic`。

---

## 6. 问题如何“出现”

### 6.1 禁止把 first mention 当 birth date

```text
first surviving use of word X
≠
first historical emergence of problem X
```

真正的 emergence claim 应尽量同时找到以下证据中的多项：

- underlying difficulty / anomaly；
- loss of familiarity；
- actor questioning；
- new classification / diagnostic practice；
- forum / institution 开始处理它；
- competing responses 出现；
- answer space 形成；
- contemporaries 识别为新问题或新争论。

### 6.2 Emergence 可以有 lag

某种困难可能存在几十年后才成为问题。

记录时允许：

```yaml
underlying_condition_since: "..."
problematization_visible_since: "..."
explicit_formulation_since: "..."
```

不要为了一个整齐年份把三者压成同一点。

---

## 7. 问题如何“消失”

### 7.1 disappearance 不等于 solution

一个问题后来不再出现，至少可能是：

- 被回答；
- 被制度化成 routine；
- displaced；
- split / merged；
- vocabulary changed；
- forum disappeared；
- archive / source gap；
- censorship / strategic silence；
- became unaskable。

### 7.2 `became_unaskable` 是强的 modal claim

它不是：

> “后来没人问了。”

而更接近：

> “支撑旧问题的关键对象、分类、制度、角色、前提或答案空间已经变化，使旧 Q 按原结构不再成立。”

因此最好有积极 transition evidence，例如：

- old category 被废除；
- institution 失去 jurisdiction；
- actor 明确说旧问题不再适用；
- 原标准答案变成 category error；
- 新 frame 明确接管旧争论；
- 支撑问题的技术 / practice / role 消失。

### 7.3 不知道就是不知道

如果材料不足，允许：

```text
evidence_gap
undetermined
```

不要把 source limitation 写成 historical disappearance。

---

## 8. Episode 之间的 relation

正式 relation 以 `docs/IDENTITY-CHECK.md` 为准，目前至少允许：

```text
continuous
reformulated
transformed_successor
split
merged
displaced
revived
analogy_only
unrelated
undetermined
```

### 8.1 默认不是 continuity

两个 episode 看起来相似时，默认：

```text
undetermined
```

研究者必须同时提交：

```yaml
continuity_evidence: []
discontinuity_evidence: []
```

### 8.2 最低 relation 检查

至少比较：

- target / object；
- stakes；
- presuppositions；
- answer space；
- actor recognition / transmission；
- askability。

并执行 `IDENTITY-CHECK.md` 的：

- Answer Transfer Test；
- Presupposition Removal Test；
- Historical Recognition Test。

### 8.3 `transformed_successor` 很重要

本仓明确允许：

```text
A historically helps generate B
```

但同时：

```text
A ≠ B
```

因果或谱系联系不等于 problem identity。

---

## 9. Evidence 不做单轴排行榜

禁止：

```text
primary = strong
secondary = weak
```

应做 claim-relative 评价。

例如一份政府会议记录可能：

- 很强地证明“该机构正式使用 formulation F”；
- 中等地证明“参与者共享某 presupposition”；
- 很弱地证明“整个社会都这样理解”。

### 9.1 每条关键 claim 最少写清

```yaml
claim:
  text: "..."
  layer: actor_explicit | actor_reconstructed | researcher_analytic
  status: supported | provisional | contested | undetermined

source_links:
  - source_id: src-...
    locator: "..."
    relation: supports | contradicts | complicates | contextualizes | dates | locates | later_reinterprets
```

### 9.2 OCR / 搜索结果只是入口

```text
OCR hit
keyword match
embedding neighbor
LLM extraction
```

只能作为 lead。

凡关键措辞影响 formulation、identity、emergence 或 disappearance，能回 facsimile 就应回 facsimile。

---

## 10. 计算辅助的边界

M0–M3 没稳定前，计算方法不得替代历史判断。

允许输出：

```text
candidate
lead
anomaly
```

禁止自动输出：

```text
same problem
problem emerged in YEAR
problem disappeared in YEAR
actor intended Q
```

尤其禁止：

```text
semantic similarity → problem identity
semantic shift → problem transformation
zero search result → unaskability
```

---

## 11. 标准研究循环

每次推进一个 episode 或 evidence chain 时，按以下顺序：

1. **Read state**：读 README / ROADMAP / RESEARCH_PLAN / METHOD / FAILURE-MODES（若存在）与当前 study；
2. **Define claim**：明确今天要证明/推翻哪一个历史判断；
3. **Source audit**：先看仓库已有材料，避免重复；
4. **Find actor evidence**：优先寻找可定位的一手材料；
5. **Separate layers**：标 actor explicit / reconstructed / later reconstruction / researcher analytic；
6. **Recover context**：语言、speech act、institution、audience、stakes；
7. **Presupposition / answer-space check**；
8. **Search rivals**：找竞争 formulation 和反证；
9. **Askability check**：解释为什么当时可问；
10. **Negative-evidence check**：若使用 silence，执行 `NEGATIVE-EVIDENCE.md`；
11. **Identity check**：若连接前后 episode，执行 `IDENTITY-CHECK.md`；
12. **Provenance check**：执行 `SOURCE-CITATION.md`；
13. **Write uncertainty**：明确不知道什么；
14. **Only then synthesize**。

---

## 12. 一个可直接使用的 Episode research packet

```yaml
episode_id: "..."
working_title: "..."

period:
  start: "..."
  end: "..."
  boundary_rationale: "..."

scope:
  place: []
  institutions: []
  forums: []
  actors: []
  audiences: []

formulations:
  - type: actor_explicit | actor_reconstructed | researcher_analytic
    text: "..."
    source_links: []
    confidence: high | medium | low | undetermined
    reconstruction_rationale: null
    counterevidence: []

later_reconstructions:
  - actor_or_scholar: "..."
    date: "..."
    formulation: "..."
    source_links: []

stakes:
  - claim: "..."
    source_links: []

presuppositions:
  - claim: "..."
    status: explicit | contextually_supported | researcher_inferred | undetermined
    source_links: []

answer_space:
  accepted: []
  contested: []
  marginal: []
  excluded_or_category_error: []
  unknowns: []

competing_formulations:
  - formulation: "..."
    actors: []
    source_links: []

askability:
  enabling_language: []
  classifications: []
  institutional_conditions: []
  knowledge_or_technical_conditions: []
  pressures_or_triggers: []
  status: supported | provisional | undetermined

emergence:
  claim: null
  positive_evidence: []
  alternative_dates_or_explanations: []

disappearance_or_transition:
  claim: null
  positive_evidence: []
  negative_evidence: []
  rival_explanations: []

relations:
  - other_episode: "..."
    proposed_relation: continuous | reformulated | transformed_successor | split | merged | displaced | revived | analogy_only | unrelated | undetermined
    continuity_evidence: []
    discontinuity_evidence: []
    status: provisional | supported | contested | undetermined

hindsight_risks: []
uncertainties: []
next_source_targets: []
```

这只是 research packet，不等同于最终 schema。Schema 应在 fixture 测试后再冻结。

---

## 13. 证据强度怎样写

不要只写 `strong / medium / weak` 而没有理由。

建议说明强弱来自哪一方面：

```text
source identity / version certainty
exact locator
actor proximity
genre fit
independent corroboration
explicitness
representativeness
rival explanation pressure
archive / survival coverage
```

一个 claim 的总体判断可以是：

```yaml
evidence_assessment:
  status: supported | provisional | contested | undetermined
  strengths:
    - "..."
  weaknesses:
    - "..."
  what_would_change_the_judgment:
    - "..."
```

---

## 14. 后见之明风险的最低自检

每个正式 episode 至少回答一次：

1. 我是否先有现代问题标题，再向过去搜“答案”？
2. 我是否把一个后来才稳定的概念倒灌给早期行动者？
3. 我是否因为同词出现就假定同问题？
4. 我是否因为换词就假定问题断裂？
5. 我是否把客观困难当成已经被问题化？
6. 我是否用一个 actor / institution 代表整个时期？
7. 我是否把后来的 official / scholarly reconstruction 当成 simultaneous actor evidence？
8. 我是否因为材料沉默就宣称问题消失？
9. 我是否因为知道后来结果，才把 earlier ambiguity 写成“通向结果的步骤”？
10. 我是否为了保持 lineage 而忽略 presupposition 已崩塌的证据？

完整 failure catalogue 应进入 `docs/FAILURE-MODES.md`。

---

## 15. Stop / downgrade conditions

出现以下情况，应停止升级结论：

- 找不到 actor-side formulation / problematization evidence；
- 只有现代研究者使用该问题表述；
- 关键原文无法可靠定位；
- actor-language admissibility 明显失败；
- competing reading 与当前 reconstruction 同样强；
- problem identity 主要靠同词或 embedding；
- disappearance 主要靠 search silence；
- 分期只靠外部政治年代；
- 为了漂亮谱系忽略 discontinuity evidence。

正确动作可以是：

```text
researcher_analytic only
evidence_gap
analogy_only
undetermined
candidate rejected
```

这些都不是失败，而是研究诚实。

---

## 16. M0 calibration：METHOD 还没有“冻结”

本文件完成后，M0 仍需要实测。

### 16.1 双-Agent 5 段文本测试

两个 Agent 对同一批历史文本独立输出：

- actor-explicit formulation；
- actor-reconstructed formulation；
- presuppositions；
- researcher inference；
- competing interpretation；
- confidence / uncertainty。

如果两者经常把研究者重述写成 actor formulation，METHOD 必须继续修改。

### 16.2 Identity adversarial fixtures

至少覆盖：

- same word / different problem；
- different words / high continuity；
- actor claims continuity but evidence shows break；
- later invented lineage；
- genuine askability loss；
- A causes B but A ≠ B；
- evidence conflict requiring `undetermined`。

### 16.3 Negative-evidence fixtures

至少覆盖：

- public silence + hidden/private evidence；
- keyword disappearance + vocabulary replacement；
- archive destruction / digitization gap；
- positive institutional evidence for real displacement。

Schema 只有在这些测试暴露出实际字段需求后才应冻结。

---

## 17. 方法来源与版本说明

以下仅列本 METHOD 直接依赖的公开可核验入口；完整文献图见 method-lineage notes。

### Collingwood

- R. G. Collingwood, *An Autobiography* (Oxford University Press, 1939), ch. 5.
- Stanford Encyclopedia of Philosophy, “Questions”: https://plato.stanford.edu/entries/questions/
- Fernando Leal, “Collingwood’s Logic of Question and Answer,” in *Interpreting R. G. Collingwood* (Cambridge University Press, 2024), DOI 10.1017/9781009337021.008.

### Skinner

- Quentin Skinner, “Meaning and Understanding in the History of Ideas,” *History and Theory* 8.1 (1969), 3–53.
- Revised version in *Visions of Politics*, vol. I (Cambridge University Press, 2002), 57–89, DOI 10.1017/CBO9780511790812.007.
- Cambridge chapter: https://www.cambridge.org/core/books/abs/visions-of-politics/meaning-and-understanding-in-the-history-of-ideas/96B251BDAB60C0E570F014E340F70EDD
- Adrian Blau (ed.), *Meaning and Understanding in the History of Ideas and Beyond*, Proceedings of the British Academy 281 (2026), open-access record: https://www.jstor.org/stable/jj.31510298

### Koselleck

- Reinhart Koselleck, “Begriffsgeschichte and Social History,” English trans. in *Futures Past* (Columbia University Press, 2004), 73–77 excerpt reproduced by German History Intersections: https://germanhistory-intersections.org/en/knowledge-and-education/ghis:document-129

### Foucault

- Michel Foucault, “Polemics, Politics and Problematizations,” interview with Paul Rabinow, May 1984; later in *Essential Works of Foucault*, vol. 1 (1998). Public text: https://www.foucault.info/documents/foucault.interview/

### Negative evidence

- Charles-Victor Langlois & Charles Seignobos, *Introduction to the Study of History*, public-domain text: https://www.gutenberg.org/ebooks/29637
- Timothy McGrew, “The Argument from Silence,” *Acta Analytica* 29.2 (2014), 215–228, DOI 10.1007/s12136-013-0205-5.

### Source provenance

- Library of Congress, “Getting Started with Primary Sources”: https://www.loc.gov/programs/teachers/getting-started-with-primary-sources/
- `docs/SOURCE-CITATION.md` contains the repository’s operational minimum.

Access check for the above public web entry points: 2026-09-04.

---

## 18. 一句话版本

如果只能记住一条：

> **不要问“历史上谁回答过我今天的问题”；先问“这些行动者当时究竟把什么变成了问题，以及我们凭什么知道”。**
