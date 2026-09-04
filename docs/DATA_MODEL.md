# Problem Episode 数据契约

`schemas/problem-episode.schema.json` 是 M0 阶段的结构原型。它把仓库已经写下的方法约束变成可检查的数据契约，但**不替历史研究者裁决史实或问题同一性**。

当前版本：`0.1.0`，使用 JSON Schema Draft 2020-12。

## 它检查什么

每个 episode 必须显式记录：

| 区域 | 最低要求 |
|---|---|
| 时间 | 起止年份、精度、证据和分期说明 |
| 问题表述 | `actor_explicit`、`actor_reconstructed` 或 `researcher_analytic`；后两者必须解释重建/分析行为 |
| 语境 | actors、institutions、vocabulary、stakes、presuppositions 均与 evidence id 相连 |
| 回答空间 | accepted / marginal / unthinkable-or-impossible 分开；没有证据时保留空数组而不是猜测 |
| 来源 | 可找回的 citation + locator；引用片段再以 evidence 记录定位 |
| 竞争框架 | 与主 formulation 分开保存，不能静默合并 |
| 关系 | source/target 明确，正反证据同时存在，六维矩阵和三个 identity tests 完整 |
| 风险 | hindsight risk 与一般 uncertainty 分开 |
| 审核 | draft / provisional / reviewed 状态和 reviewer 可见 |

`additionalProperties: false` 用于尽早发现拼写错误和未经讨论的字段漂移。Schema 版本升级时应同步迁移数据，不能让不同 agent 各自发明相似字段。

## 三种 formulation 不能混同

```text
actor_explicit       历史行动者明确提出
actor_reconstructed  由多条同时代证据重建
researcher_analytic  研究者为比较而提出
```

`actor_reconstructed` 至少需要两条 evidence，并写 `reconstruction_note`；`researcher_analytic` 必须写 `researcher_note`。这不是把后两者判成“较差材料”，而是阻止它们被偷偷升级成行动者原话。

`actor_explicit` 的 formulation 与 answer 必须至少引用一条 `quotation` 或 `paraphrase`。`context` 与 `silence` 可以限制解释，但不能单独证明行动者明确提出了某个问题或回答。

词汇也必须写 `term_source_type`，区分行动者明确用词、由材料重建的用词、后来研究术语和研究者分析标签。后三者必须用 `provenance_note` 解释来源，不能因为一个现代术语很方便，就把它倒灌成历史行动者自己的分类。

## 来源与证据的最小规范

一个 source 至少包含：

- `source_id`：episode corpus 内可引用的稳定 slug；
- `source_type`：一手文本、制度记录、同时代观察、专业二手研究或参考资料；
- `citation`：作者/机构、标题、日期或版本等足以识别材料的信息；
- `locator`：页、章、段、folio、档案号或表格等可回到原位置的定位；
- `retrievable`：当前是否可找回；不可找回不等于删除，但必须显式暴露。

每个 evidence 再保存该 source 内更细的 locator、excerpt 和 interpretation。`excerpt` 可以是原文引句，也可以在 `evidence_type: paraphrase/context/silence` 时如实说明观察到的内容；不能把释义伪装成引号内原话。

URL 只是可选的获取路径，不代替 citation 和 locator。

## Relation 是一等对象

关系类型以 [`IDENTITY-CHECK.md`](./IDENTITY-CHECK.md) 为准：

```text
continuous / reformulated / transformed_successor / split / merged
displaced / revived / analogy_only / unrelated / undetermined
```

每条关系都必须保存：

1. 历史行动者、后来的行动者、观察者、历史学者或 agent 各自提出的 identity claim；
2. 至少一条 continuity evidence 和一条 discontinuity evidence；
3. target/object、stakes、presuppositions、answer space、historical recognition、askability 六维矩阵；
4. Answer Transfer、Presupposition Removal、Historical Recognition 三项测试的材料和理由；
5. repository 当前的 provisional / contested / reviewed 裁决、confidence 和 decision note。

`confidence: high` 可以与 `relation: undetermined` 并存：它表示有充分理由相信“当前证据不足以裁决”，不是把不确定伪装成确定关系。

## Fixture 只校准表达能力

[`fixtures/problem-episodes/`](../fixtures/problem-episodes/) 的三个 harbor 案例完全虚构，所有记录都设置：

```json
"is_fixture": true
```

它们依次覆盖：

- 行动者明确提出的问题；
- 需要两份材料重建的问题；
- 研究者为比较而提出的分析问题；
- actor continuity claim 与 repository relation 不同；
- `transformed_successor` 不等于 same problem；
- 有理由保留 `undetermined` 的跨 episode 关系。

Fixture 不能被引用为历史事实，也不能因为通过 schema 就升级成正式 episode。

## 验证

安装开发依赖后运行：

```bash
python -m pip install --requirement requirements-dev.txt
python scripts/validate_problem_episodes.py
python -m unittest discover -s tests -v
```

CLI 默认把三个 fixture 当作一个 corpus 校验。也可以传入一个或多个 JSON 文件/目录：

```bash
python scripts/validate_problem_episodes.py problems/example/episodes-json
```

JSON Schema 检查字段、枚举和条件要求；validator 另外检查：

- schema 与 episode 是否为严格 UTF-8 JSON（拒绝重复 object key 与 `NaN` / `±Infinity`）；
- schema 自身是否为有效 Draft 2020-12；
- corpus 内 episode/source/evidence/relation id 是否重复；
- evidence → source、claim → evidence、relation → target 是否能解析；
- relation source 是否就是包含它的 episode；
- relation evidence 是否只属于 source / target 两端；
- relation 两端的 `is_fixture` 是否一致（fixture 与正式 episode 不得建立关系）；
- `actor_explicit` formulation / answer 是否至少有一条 quotation 或 paraphrase；
- 起始年份是否晚于结束年份；
- reviewed 状态是否真的写了 reviewer；
- `fixtures/` 下的记录是否明确标成 fixture。

GitHub Actions 使用只读 `contents` 权限运行同一组命令。

## 自动化边界

验证通过只证明：

```text
论证结构完整 + 引用关系可解析
```

它不证明：

```text
引文真实 / 来源具有代表性 / 推断成立 / relation 裁决正确
```

特别禁止把 schema 验证、关键词相似度或模型输出直接当成 `reviewed` 的历史结论。正式 episode 仍须回到原始材料、主动寻找竞争框架，并由 reviewer 检查解释是否越过证据。
