# 2025–2026 PostgreSQL：AI 缺陷发现与维护者判断瓶颈

> Status: **contemporary lead / episode candidate**  
> Problem family: technology–labour / automation and expert work  
> Relation to existing lineage: **undetermined**  
> Evidence status: strong for the PostgreSQL case; insufficient for software development as a whole

## 1. 为什么把这个案例收进来

2026 年 PostgreSQL 19 的发布时间明显晚于近十年的常态。PostgreSQL committer Robert Haas 将这次延迟的一部分直接归因于一个新的维护负荷：LLM 让缺陷发现显著加速，但修复、审查、back-patch、提交和发布判断仍主要依赖有限的人类 committer。

这个案例值得进入“技术—劳动”问题线，不是因为它已经证明“AI 替代程序员”，恰恰相反：它显示了一种不同的自动化问题结构——**自动化提升了某个上游环节的吞吐量，却把稀缺性转移到下游的人类判断、责任与治理能力上。**

因此，本条目暂时不把它接入传统的“机器是否替代劳动”线性叙事，而把它作为一个可能的新 problem episode 候选：

> 当机器能够比维护者更快地产生“需要判断的问题”时，软件维护如何维持质量、发布节奏与创新能力？

这是对 Haas 2026 年陈述的研究性归纳，不应反投射为整个软件行业在此前已经共享的问题表述。

---

## 2. 当时行动者明确面对了什么问题

### 2.1 Robert Haas 的 formulation

2026-10-21，PostgreSQL committer Robert Haas 在 Neon 博客发表《Postgres 19 is late, and it's AI's fault》。他的核心判断非常直接：

- LLM 正在更快地发现 PostgreSQL 中原本长期潜伏的缺陷；
- 修复也变容易了，但没有像“发现”那样变得同等容易；
- AI 草拟的修复仍可能不正确或不符合 PostgreSQL 标准；
- 因而补丁仍需要人类 review 和 commit；
- back-branch 的安全问题与 bug 修复占用了原本可用于审查 PostgreSQL 19 的时间；
- 这与 late reverts 和 PostgreSQL 19 延迟有关。

Haas 用一句高度凝练的话概括这种不对称：**“LLMs are finding bugs faster than committers can fix them.”**

这里的历史行动者问题并不是抽象的“AI 是否会取代程序员”，而是一个具体的维护能力问题：**缺陷发现吞吐量已经超过了项目对这些发现进行可信验证、修复和吸收的能力。**

### 2.2 release team 的 formulation

PostgreSQL release team 在 2026-10-10 更新 v19 的 RC/GA 日期时，没有把原因表述成“AI 导致延期”，但明确指出：back branches 中累积了大量 fixes，因此决定增加 RC2，把这些修复带入 PostgreSQL 19，再进行 GA。

这提供了与 Haas 解释相独立的一层制度证据：release team 的实际决策确实围绕“修复量、稳定性和发布节奏”发生变化。

### 2.3 Beta 4 的 late reverts

PostgreSQL 19 Beta 4（2026-09-24）官方公告列出多项被撤回的大功能，包括：

- SQL/PGQ property graph query support；
- `FOR PORTION OF` temporal update/delete；
- `ALTER TABLE ... MERGE PARTITIONS` / `SPLIT PARTITIONS`；
- online enable/disable data checksums；
- 若干 DDL retrieval functions 等。

官方理由强调 reliability、predictable release schedule，以及需要更多时间完成 community development and review process。

这并不能单独证明这些 revert “由 AI 导致”，但它与 Haas 所说的审查资源被 bug/security work 分流形成时间上的相互印证。

---

## 3. 可量化的负荷变化

Haas 给出的提交数据提供了一个重要但需要谨慎解释的代理指标：

| 时间窗口 | branch | commits |
|---|---|---:|
| 2025-04-08 → 2025-09-25 | master | 1037 |
| 2025-04-08 → 2025-09-25 | REL_18_STABLE | 724 |
| 2026-04-08 → 2026-09-25 | master | 1443 |
| 2026-04-08 → 2026-09-25 | REL_19_STABLE | 1169 |
| 2025 同期 | REL_17_STABLE | 248 |
| 2026 同期 | REL_18_STABLE | 433 |

Haas 强调的是 back-patched commits 的跃升：

- 当年 release branch 同期 back-patch 数量增长超过 60%；
- 前一稳定版本的同期 back-patch 数量增长超过 74%。

这些数字本身只证明维护活动显著增加；“其中多大比例可归因于 LLM”是 Haas 基于项目经验提出的解释，而不是由 commit count 自动推出的因果结论。

因此证据层级应分开记录：

1. **强事实**：2026 release/back-branch 修复提交显著增多；
2. **行动者解释**：Haas 认为主要原因是大量使用 LLM 发现并报告的 bug；
3. **研究者推断**：这种不对称吞吐量可能构成一种新的维护治理瓶颈。

---

## 4. Problem Episode 草案

```yaml
problem_id: ai-assisted-maintenance-throughput
period: 2025-2026
context:
  - PostgreSQL 19 release cycle
  - rapid diffusion of LLM-assisted bug discovery and patch drafting
actors:
  - Robert Haas
  - PostgreSQL committers
  - PostgreSQL release team
formulation:
  - defect discovery is accelerating faster than trusted human review/fix/commit capacity
  - release work is displaced by security and back-branch maintenance work
vocabulary:
  - LLM
  - bug reports
  - back-patch
  - review
  - committers
  - late reverts
  - release delay
institutions:
  - PostgreSQL Global Development Group
  - PostgreSQL commit/review process
  - stable branches and release team
presuppositions:
  - AI-generated findings and patches cannot be trusted merely because they are machine-produced
  - PostgreSQL quality standards require accountable human review
  - maintainer attention is finite
  - old mature code can contain a large reservoir of latent defects
status: active
relation_to_technology_replaces_labour: undetermined
```

目前还不应填写完整的 accepted/marginal/unthinkable answer space，因为现有材料主要在描述负荷与原因，还没有足够证据恢复 PostgreSQL 社区内部对“应该怎样制度化应对 AI 报告洪流”的稳定分歧结构。

---

## 5. 与“技术会不会替代劳动？”的关系

这是本案例最值得保留的地方。

传统技术—劳动问题常被组织为：

```text
机器能力上升
    ↓
某类人的劳动是否减少 / 消失？
```

PostgreSQL 2026 案例出现的却是：

```text
机器的发现能力上升
    ↓
待验证、待修复、待审查的问题数量上升
    ↓
有限的人类判断能力成为瓶颈
    ↓
维护劳动被强化 / 重组 / 挤占其他工作
```

因此它可能不是“替代劳动”问题的简单延续，而是一个 **split** 或 **transformed successor** 的候选：

- 一条线继续问 AI 是否能替代编码、测试、review；
- 另一条线开始问 AI 是否会制造比组织能够吸收的更多候选缺陷、补丁与决策事项。

当前证据还不足以裁定 relation。仓库中应保持 `undetermined`，避免因为主题相似就把它强行接成一个从机械化到生成式 AI 的线性故事。

---

## 6. 一个可能的重要结构变化：从“生产瓶颈”到“判断瓶颈”

这个案例支持提出一个研究假设，但还不能把它当成普遍历史结论：

> 当自动化首先提高发现、生成和候选方案生产速度时，稀缺劳动可能从“产出内容”转移到“验证、责任归属和最终判断”。

在 PostgreSQL 这里，这个假设有相当具体的制度形态：

- bug report 可以被快速制造；
- patch 可以被快速草拟；
- 但 merge/back-patch/release 仍要经过项目规范与有权限、有信誉的维护者；
- 因而“AI 产能”不能直接等价为“项目吞吐量”。

若未来在 Linux kernel、LLVM、Rust、Python、OpenSSL 等高可靠开源项目中反复出现相同的行动者 formulation，才有理由讨论更广泛的软件工程问题结构转型。

---

## 7. 后见之明风险

### 风险 A：把 PostgreSQL 个案写成整个软件业的事实

目前只能确定 PostgreSQL 社区有强烈的一手表述。不同项目的 maintainer 数量、权限结构、自动化测试、代码规模和安全要求差异很大。

### 风险 B：把“bug 更多被发现”误写成“软件质量下降”

Haas 明确反对这种简单解释。他认为 PostgreSQL 代码质量并没有因此变差；变化在于过去不可见的 bug 更容易被发现。

### 风险 C：把 commit 数量直接当成 AI 因果证明

commit/back-patch 数量只能证明维护活动增加。AI 的因果角色来自行动者解释和 bug-report 经验，而不是计数本身。

### 风险 D：把“AI 加重维护负担”写成“AI 没有提高效率”

两者并不等价。Haas 同时承认修复也变容易，只是改善幅度小于发现端。

### 风险 E：把它提前纳入“AI 取代程序员”的答案

这个案例恰好说明“替代”不是唯一问题形式。AI 可能同时减少某些劳动、增加另一些劳动，并改变项目治理的稀缺资源。

---

## 8. 下一步证据任务

若要把本 lead 升格为正式 Problem Episode，至少补以下材料：

1. PostgreSQL mailing list 中关于 2026 AI-assisted bug reports 的原始 thread，确认不同 committer 是否共享 Haas 的判断；
2. 抽样若干明确由 LLM 辅助发现的 bug report，记录报告质量、修复过程与 maintainer 反馈；
3. 核验 2025/2026 back-patch commit 的类别分布，区分 security、regression、old latent bug、new-feature bug；
4. 查找 PostgreSQL 项目对 AI-generated patches/reports 的正式或非正式规范；
5. 与至少两个其他成熟基础设施项目做同期对照，避免单项目特殊性；
6. 追踪 PostgreSQL 19 最终 GA 后，release team 是否回顾这一周期并改变 workflow。

在上述证据补齐前，本文件保持 **lead / episode candidate**，不纳入已经确认的跨期 problem lineage。

---

## 9. Sources

### Primary / actor-level

- Robert Haas, “Postgres 19 is late, and it's AI's fault,” Neon, 2026-10-21.  
  https://neon.com/blog/postgres-19-is-late-and-its-ais-fault

- Jonathan S. Katz, “Updated PostgreSQL RC / GA dates,” `pgsql-hackers`, 2026-10-10.  
  https://www.postgresql.org/message-id/f161fbb7-e193-42eb-bec7-4cfc1af74a50%40postgresql.org

- PostgreSQL Global Development Group, “PostgreSQL 19 Beta 4 Released!”, 2026-09-24.  
  https://www.postgresql.org/about/news/postgresql-19-beta-4-released-3386/

- PostgreSQL Global Development Group, “PostgreSQL 19 RC 1 Released!”, 2026-10-15.  
  https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/

### Secondary pointer

- Michael Larabel, “PostgreSQL 19 Running Behind Schedule Due To AI/LLM Burden,” Phoronix, 2026-10-30.  
  https://www.phoronix.com/news/PostgreSQL-19-Late

---

## 10. 当前判断

**可确认：** PostgreSQL 19 周期中，维护与 back-patch 负荷显著上升；核心 committer 明确把 LLM-assisted bug discovery 视为重要原因，并认为这种负荷参与造成了 late reverts 和 release delay。

**可以提出但尚未证明为普遍现象：** AI 使软件工程的稀缺资源从代码/缺陷“生产”向可信 review、判断、责任与治理迁移。

**暂不能声称：** 2026 年整个软件行业已经从“自动化替代劳动”进入“自动化制造判断负荷”的新阶段。
