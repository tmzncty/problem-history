# Hartmann → Gadamer：Problemgeschichte 与“问题同一性”

> 状态：method-lineage source packet  
> 目的：补足仓库关于 Nicolai Hartmann 与 Hans-Georg Gadamer 的一手文本证据，并把争点转成可执行的 Problem Identity 约束。  
> 注意：这不是“错误的 Hartmann → 正确的 Gadamer”的进步史。

## 1. 本轮新增发现

仓库此前已经知道：Hartmann 式 Problemgeschichte 倾向于把跨时代问题同一性当作方法前提，而本项目要求 identity 必须由历史证据证明。

这轮把差异精确化：

- Hartmann 1909/1910 不只是建议“按问题而不是按人物写哲学史”。他的方案把哲学问题赋予相对独立、可跨历史重新识别的地位，历史变化主要落在 problem situation 与具体 formulation。
- Gadamer 1924 已经直接攻击“永恒问题库”模型。他认为历史处境不只改变问题的措辞，也参与规定什么会成为问题、问题的内容如何形成。
- Gadamer 1960 在 Truth and Method 中把这一批评接到 question-and-answer logic：抽离真实提问动机的 problem 只是抽象物，不能从一个超历史立场直接判定跨时代 identity。

因此本项目最安全的规则是：

~~~text
cross-temporal problem identity
= evidence-constrained historical verdict
not preloaded problem_content_id
~~~

## 2. Source boundary

### Hartmann 1909/1910

Nicolai Hartmann, “Zur Methode der Philosophiegeschichte,” Kant-Studien 15 (1909/1910), 459–485；1958 重印于 Kleinere Schriften III, pp. 1–22.

书目与 DOI：
https://philpapers.org/rec/HARZMD-5
https://doi.org/10.1515/9783110855203.1

本轮没有取得可公开逐页翻阅的 Hartmann 原刊扫描。因此论文身份、刊物、页码为 high；论证结构为 medium-high；具体页码判断由多份学术研究交叉支持，仍待 direct page-image audit。

主要控制材料：

- “Reason’s genuine historicity: the establishment of a history of philosophy as a philosophical sub-discipline in Marburg Neo-Kantianism,” BJHP (2021): https://www.tandfonline.com/doi/full/10.1080/09608788.2021.1932410
- Martin Morgenstern, “Vom Idealismus zur realistischen Ontologie. Das Frühwerk Nicolai Hartmanns”: https://philosophia-bg.com/archive/philosophia-5-2013/vom-idealismus-zur-realistischen-ontologie-das-fruhwerk-nicolai-hartmanns/
- Hannes Kerber, “Der Begriff der Problemgeschichte und das Problem der Begriffsgeschichte,” International Yearbook for Hermeneutics 15 (2016), 294–314: https://bc.academia.edu/HannesKerber

### Gadamer 1924

Hans-Georg Gadamer, “Zur Systemidee in der Philosophie,” Festschrift für Paul Natorp (1924), 55–75.

首次完整英译与研究导言：

Haley Burke / Fridolin Neumann, “Hans-Georg Gadamer’s ‘On the idea of a system in philosophy’ (1924),” BJHP 33.4 (2025), 930–956:
https://www.tandfonline.com/doi/abs/10.1080/09608788.2024.2393239
https://philarchive.org/rec/BURHGQ

译文保留原始 “System” 页码；涉及德语词级含义时仍应回原文。

### Gadamer 1960

Hans-Georg Gadamer, Truth and Method, printed pp. 368–369。本轮直接核过页面：

https://blogs.ubc.ca/nfriesen/files/2015/01/Pages-from-Hans-Georg_Gadamer_-_Truth_And_Method_.pdf

## 3. Hartmann：Problemgehalt / Problemlage / Problemstellung 不是中性 schema

Hartmann 的方法困难可以安全重建为：

> 哲学史怎样在思想家与时代不断变化的情况下，仍保存一种属于哲学本身的内在连续性，而不退化为思想家传记或一般文化史？

2021 年的 Marburg Neo-Kantian historiography 研究表明，Hartmann 的方案同时承认哲学家作为个人具有历史规定性，并把哲学问题赋予一种相对独立的 reality；在此结构里，是 philosopher 被 problem 塑造，而不只是 philosopher 创造 problem。

Kerber 对 Hartmann 文本的恢复区分：

- Problemgehalt：problem content；
- Problemlage：某时代中的 problem situation；
- Problemstellung / Problemfassung：某个思想家或体系里的具体 formulation。

关键在于：后两层发生历史变化，同时保留可重新识别的 problem content。

因此下面这个结构本身已经包含 identity 前提：

~~~text
stable Problemgehalt
    ↓
historically varying Problemlage
    ↓
thinker-specific Problemstellung
~~~

本项目不能直接复制它，否则“它们是不是同一个问题”已经在建模时被提前回答。

但也不能把 Hartmann caricature 成“不关心历史”。他仍要求恢复 historical problem situation，并反对研究者用自己的系统立场先验地改写过去。真正的分歧较窄：

~~~text
Hartmann:
history mediates how a problem appears

Gadamer:
historicity can participate in
what the problem itself is
~~~

## 4. Gadamer 1924：历史性进入 problem content

1924 “Zur Systemidee” 的关键论证并非“问题的表达会变化”。

Gadamer 质疑：曾经被哲学清楚看见的 problems 是否真的会作为同一个问题永久保存给后来时代。他以古希腊问题在现代变得难以理解为例，反对这样一种模型：

~~~text
identical supra-historical problem stock
        ↓
historical formulations are partial presentations
        ↓
modern historian strips away old clothing
        ↓
recovers the same problem we ask today
~~~

他特别指出：把 Plato 的 problems 直接读成现代 problems 的早期版本，会把 Plato 变成我们现在的无差别 predecessor，而错过只有在其历史世界中才成立的概念邻接与 problem content。

更重要的是原始 “System” pp. 61–62 的结构：

- problem 必须实际对某个历史中的 questioner 成为问题；
- world-experience / existential experience 参与规定什么会成为 problem、什么根本能成为 problem；
- formulation 不是包在固定 content 外面的历史外壳；
- historical basic attitude 同时影响 formulation 与 content。

这可以转写成仓库规则：

~~~text
historical conditions
do not merely affect wording

they can affect
target classification
stakes
presuppositions
answer possibilities
and therefore the question itself
~~~

但 Gadamer 并不因此走向“每个人都有不可比较的私人问题”。1924 文本仍坚持 problem 的 objectivity；他反对的是把历史性当成可以从客观问题中剥离的偶然噪声。所以也不能写成 different context → automatically different problem。

## 5. Gadamer 1960：从 permanent problem 回到 motivated question

Truth and Method printed pp. 368–369 把 1924 的问题推进到成熟的 question-and-answer 语言。

Gadamer 先说历史理解必须恢复某个 question 在哪些 presuppositions 下被提出，随后借 Collingwood 的 question-and-answer logic 反对 permanent problems：不存在一个真正站在历史之外、可以直接读取 problem true identity 的位置。

他又把抽象 problem 理解为从实际 question 中抽离出来的内容。离开使 question 真正被提出的 motivation，problem 会失去具体的 sense。

对本项目而言，这支持一个强而窄的规则：

~~~text
topic label / modern research title
!=
motivated historical question
~~~

例如“技术会不会替代人”可以作为跨年代检索 umbrella，但不能因为 1848、1930s、1960s、AI-era 都能被今天放进这个标题，就先判定共享 problem identity。

1924 → 1960 可以说存在明显的方法连续性：1924 反对把 historical problems objectify 成 eternal stock；1960 把 detached problem 重新放回 motivated questioning。但不要把 1924 当作 1960 mature hermeneutics 的缩写。

## 6. 对当前 Problem History schema 的直接影响

### 6.1 不新增 invariant Problemgehalt

episode 内可以记录 target、formulation、stakes、presuppositions、answer space、responsibility、askability。跨 episode 的 identity 必须在比较这些结构后得到。

不能先设置：

~~~text
problem_content_id: X
A = formulation of X
B = formulation of X
~~~

### 6.2 motivated context 应成为 identity evidence

至少追问：

- 什么具体困难使 question 在此时发生；
- 谁需要回答；
- 谁承担失败成本；
- 哪些 presuppositions 使它可问；
- 什么观察算证据；
- 什么 answer 会被承认为回答；
- 哪些 distinctions 当时尚不存在或已失效。

所以 same wording + same referent 仍不足以抵消 different motivation + different presuppositions + different answer criteria。

### 6.3 候选 Test D — Historical Motivation Test

现有 IDENTITY-CHECK 已有 Answer Transfer、Presupposition Removal、Historical Recognition。可新增一个候选：

> A 与 B 中，是什么具体压力、异常或实践困难使问题必须被问？如果移除这一 motivation，formulation 是否仍以相同意义成立？

可能读法：

- same / traceably inherited motivation → continuity evidence；
- motivation broadened / reallocated → reformulation evidence；
- different motivation but explicit uptake → transformed-successor candidate；
- only researcher sees a shared topic → analogy_only candidate。

先在非哲学史 case 回测，不应直接做 validator 硬规则。

## 7. 不能从 Gadamer 推出的过强结论

1. 跨时代 comparison 不可能：错误。Gadamer攻击的是 supra-historical identity guarantee，不是 genealogy / comparison 本身。
2. 只要语境变了就是新问题：错误。历史语境总会变化；仍需 actor recognition、institutional continuity、transmission、presupposition survival 等证据。
3. 所有 Neo-Kantians 都等于 Hartmann：未证。Natorp、Windelband 等需分开恢复。
4. Gadamer 已经发明本仓 schema：错误。relation enum、episode fields、evidence contract 都是本项目的 researcher-side operationalization。

## 8. 三层严格分离

Historical actor problem：

- Hartmann：如何写出一种仍然是“哲学的”哲学史，使历史差异没有把哲学分解成互不相干的文化事实？
- Gadamer 1924：如果历史 problem formulations 的成立依赖具体存在处境，把它们还原为同一 eternal problem stock 是否已经错过其问题性？
- Gadamer 1960：历史理解如何把抽象化的 problem 重新放回使它获得意义的真实 questioning relation？

Later reconstruction：

- Kerber 2016 把 Gadamer 的 Neo-Kantian Problemgeschichte 批判恢复为其处理 historicism 的长期线索；
- Burke / Neumann 2025 把 1924 essay 恢复为 mature Gadamer 的重要早期节点；
- 2021 Marburg historiography study 把 Hartmann 1909 放回 Marburg history-of-philosophy 形成史。

Researcher rule：

> problem identity is an output of historical comparison, not an input key.

这是本项目的设计原则，不是历史行动者自己的 schema。

## 9. 证据强度与尚未解决

高置信：

- Gadamer 1924 反对 supra-temporal identical problem stock；
- Gadamer 1924 让历史存在参与规定 formulation 与 problem content；
- Gadamer 1960 明确反对 permanent-problem identity；
- Gadamer 1960 强调 problem 必须回到 motivated questioning；
- 1924 与 1960 在此争点上有明显连续性。

中高置信、待 direct scan：

- Hartmann 1909 的 problem-history hierarchy；
- Problemgehalt / Problemlage / Problemstellung 的精确页级用法。

尚未解决：

1. Hartmann 1909 原刊或 1958 重印 direct page images；
2. Hartmann 1936 是否修正 / 强化 1909；
3. Natorp 的具体位置，避免 “Neo-Kantianism = Hartmann”；
4. Gadamer 1924 德文词级复核；
5. Historical Motivation Test 在非哲学史 cases 上是否真有区分力。

## 10. 下一步候选

1. 恢复 Hartmann 1909 Kant-Studien pp. 459–485 或 1958 pp. 1–22 的页影像。
2. 精读 Hartmann 1936 Der philosophische Gedanke und seine Geschichte。
3. 单独恢复 Natorp 的 history-of-problems 立场。
4. 用 technology–labour 现有链回测 Historical Motivation Test：1930s technological unemployment → 1964 cybernation → 1974–76 employment right → 2000 monetary-range disappearance。
5. 回测后再决定是否更新 IDENTITY-CHECK 的强制测试。
6. 继续 PROBLEMGESCHICHTE 尚未完成的 Rudolf Unger、Oexle/Weber、Werle case audit。

## 11. 本轮方法结论

这次真正新增的不是一句“Gadamer 反对 Hartmann”，而是一个可以约束仓库设计的边界：

~~~text
Hartmann-style danger:
historically varying formulation
can be treated as clothing around
re-identifiable problem content

        ↓

Gadamer 1924:
historicity can enter
what becomes problematic
and what the problem contains

        ↓

Gadamer 1960:
detached problem
must return to motivated questioning

        ↓

Problem History:
cross-temporal identity
must be produced by evidence,
never preloaded into the record
~~~

长时段 problem-line 仍然可以做；但必须先允许“这些材料也许不是同一个问题”，再去证明 continuous / reformulated / transformed-successor / analogy_only。
