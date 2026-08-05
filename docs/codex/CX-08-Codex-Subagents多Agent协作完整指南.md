# CX-08 Subagents 完整指南：App 中的多 Agent 协作

主要来源：OpenAI Codex Subagents、App Features、CLI Slash Commands 官方文档。

> **2026-08-06 多 Agent 口径**：CLI 0.145.0 起 **多 Agent V2 已稳定**——可配置 subagent 模型、推理等级、并发上限，并恢复 V1 时期部分被限制的角色。委派模式分三档（禁用 / 仅显式请求 / 主动），可在线程 + 回合级别切换；父拥有的 subagent 线程**只读**，agent 线程工作区相互隔离，Guardian reviewer 工具权限被收窄。agent 任务存储从 CSV 迁到 SQLite。App-server 能列出后代线程并通过某一轮 fork 历史。演示时先讲"单 agent 边界"，再讲 V2 的可配置并发；不要第一天就开高并发。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时
> - **难度等级**：⭐⭐⭐ 进阶级
> - **更新日期**：2026年5月30日
> - **信息来源**：OpenAI Codex Subagents、App Features、CLI Slash Commands 官方文档
> - **前置要求**：已完成CX-01至CX-07，熟悉App基本操作

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **判断何时需要Subagents**：任务可拆成独立子任务、多文件互不重叠时才用
2. **设计安全的分工方案**：写清总目标、子任务边界、文件所有权、是否允许写
3. **掌握文件所有权规则**：并行写代码时明确每个Agent负责的文件范围
4. **组合Worktree和Subagents**：用Worktree隔离工作区 + Subagents分工并行
5. **正确合并Subagents输出**：看证据、看冲突、看所有权、主线程整合
6. **避免常见失败模式**：多个agent改同一文件、主线程不知道进展、子任务太大
7. **理解Subagents与Skills的配合**：Subagent执行角色，Skill提供工作流方法
8. **建立Review纪律**：并行改动合并前统一Review，不直接相信总结

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想快速知道什么时候该用Subagents

**只看这些章节**：

```
✅ 第1部分：Subagents解决什么问题（3分钟）
✅ 第2部分：App中什么时候用（5分钟）
✅ 第4部分：推荐分工模板（7分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握多Agent协作

**学习顺序**：从头到尾所有章节

---

## 术语表（进阶必读）

Subagents 的重点不是"多开几个 agent"，而是把并行工作变成可管理的协作。

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| Main thread | 主线程，负责目标、分工、合并和最终决策 | 不要把主线程变成旁观者 |
| Subagent | 被派出去做具体子任务的执行单元 | 子任务要小而清楚 |
| Worker | 偏执行的子 agent | 必须有文件所有权 |
| Explorer | 偏只读调查的子 agent | 适合并行收集证据 |
| Reviewer | 偏审查的子 agent | 通常只读，不改文件 |
| File ownership | 每个 agent 可改哪些文件 | 并行写入的生命线 |
| Merge owner | 最终合并结果的人或主线程 | 防止多份输出互相打架 |
| Dependency | 子任务之间的先后关系 | 有依赖就不要假并行 |
| Worktree | 隔离 Git 工作区 | 大任务降低污染风险 |

## 0. 多 Agent 协作模型

老金我讲 Codex Subagents 时，会先问文件所有权和合并责任；并行不是目的，可靠收口才是目的。

一次健康的 Subagents 任务应该像这样：

```text
主线程确认目标
  -> 拆分独立子任务
  -> 指定 owner、文件范围、是否只读
  -> 并行执行互不依赖的部分
  -> 子 agent 返回证据和结果
  -> 主线程处理冲突和合并
  -> Review 面板统一检查 diff
```

如果主线程没有分工、没有文件边界、没有合并规则，Subagents 只会把混乱并行化。

### 0.1 并行不是越多越好

| 子任务关系 | 是否适合并行 |
|---|---|
| 读不同模块、互不依赖 | 适合 |
| 一个查文档，一个查代码 | 适合 |
| 前端和测试文件所有权分开 | 适合 |
| 后一步必须等前一步结论 | 不适合 |
| 多个 agent 都要改同一个核心文件 | 不适合 |
| 目标本身还不清楚 | 先主线程澄清 |

### 0.2 子任务卡片模板

```text
子任务名称：
目标：
允许读取：
允许修改：
禁止事项：
输出：
完成条件：
遇到阻塞时：
```

这张卡片比“你去做后端”更有效，因为它把边界和交付都写清楚了。

## 1. Subagents 解决什么问题

Subagents 适合把一个任务拆成多个相对独立的子任务：

- 并行读不同模块。
- 一个实现、一个审查。
- 一个查官方文档、一个查代码。
- 前端、后端、测试分开推进。

它不是扩大单个上下文窗口，也不是让任务自动变聪明。它的价值是并行和分工。

## 2. App 中什么时候用


适合用：

```text
这个重构涉及前端、API 和测试。请先制定分工计划，再并行处理互不重叠的部分。
```

不适合用：

```text
修一个拼写错误。
```

判断标准：

| 条件 | 是否适合 |
|---|---|
| 任务可拆成独立子任务 | 适合 |
| 多个文件/模块互不重叠 | 适合 |
| 需要独立审查 | 适合 |
| 下一步必须等一个结果 | 先主线程做 |
| 单文件小改 | 不适合 |

## 3. App 中启动前要写清的内容


让 App 调 subagents 前，提示词至少要包含：

| 内容 | 示例 |
|---|---|
| 总目标 | “把认证模块迁移到新 SDK” |
| 子任务边界 | “前端只读 `src/pages/login.tsx`，后端只读 `src/api/auth/*`” |
| 文件所有权 | “Agent A 只改 docs，Agent B 只改 tests” |
| 是否允许写 | “先只读分析，不改文件” |
| 汇总方式 | “每个 agent 输出结论、证据、风险和建议动作” |
| 停止条件 | “遇到权限/测试/依赖问题先汇报，不自行扩大范围” |

不写这些，subagent 很容易变成多个不受控的普通对话。

## 4. 推荐分工模板

```text
先给出 subagent 分工计划，不要立刻改文件。

目标：重构认证模块。
范围：src/auth、tests/auth。
约束：不要改数据库迁移，不要引入新依赖。
分工：
- Agent A：阅读现有 auth 代码，列出风险。
- Agent B：核对官方 SDK 文档。
- Agent C：审查测试覆盖缺口。
汇总后再决定是否执行。
```

## 5. 文件所有权

并行写代码时必须明确文件所有权：

| Agent | 负责范围 |
|---|---|
| Frontend agent | `src/pages/login.tsx`、`src/components/auth/*` |
| Backend agent | `src/api/auth/*` |
| Test agent | `tests/auth/*` |
| Review agent | 只读 diff，不改文件 |

没有文件边界的并行开发很容易互相覆盖。

## 6. Subagents 与 worktree

| 能力 | 作用 |
|---|---|
| Subagent | 分工和并行思考 / 执行 |
| Worktree | 隔离 Git 工作区 |
| Review | 合并前看 diff |

大任务建议组合：

```text
Worktree thread + Subagents + Review
```

这样既能分工，又能降低污染主工作区的风险。

## 7. Subagents 与 Skills

Subagent 可以执行一个明确角色，Skill 提供工作流方法。

例子：

```text
让一个只读 subagent 使用 $tutorial-verifier skill 核对这篇教程的官方来源。
```

注意：不要假设所有 subagent 都自动拥有所有工具或插件。以当前 App 暴露能力为准。

## 8. Review 与合并规则


Subagents 返回后，主线程不要直接相信总结。按这个顺序合并：

1. 看每个 subagent 的输出是否有证据。
2. 看是否有互相冲突的结论。
3. 看文件所有权是否被遵守。
4. 由主线程整合方案。
5. 执行或合并后用 App Review 看 diff。
6. 运行验证命令。

如果两个 agent 给出相反建议，不要让其中一个继续硬改；先让主线程整理冲突点，再决定下一步。

### 8.1 冲突处理流程

| 冲突类型 | 表现 | 处理 |
|---|---|---|
| 事实冲突 | 一个说 API 已弃用，一个说还能用 | 要求双方列来源，必要时再查官方文档 |
| 文件冲突 | 两个 agent 改同一文件 | 停止并由主线程决定 owner |
| 方案冲突 | 一个建议重构，一个建议小修 | 回到任务目标和风险选择 |
| 测试冲突 | 一个测试通过，一个环境失败 | 核对命令、环境和输出 |
| 安全冲突 | 实现 agent 要放宽权限，review agent 反对 | 按安全优先处理，人工确认 |

### 8.2 主线程合并提示

```text
请合并各 subagent 输出：
1. 先列共同结论
2. 再列冲突点和证据
3. 标出每个建议影响的文件
4. 只选择一个最小可执行方案
5. 不要继续修改文件，等我确认
```

主线程的价值是判断和整合，不是把所有子 agent 总结原样粘在一起。

## 9. 常见失败模式

| 失败模式 | 原因 | 修正 |
|---|---|---|
| 多个 agent 改同一文件 | 所有权不清 | 明确文件范围 |
| 主线程不知道进展 | 没有汇总点 | 要求阶段性汇报 |
| 子任务太大 | 拆分不够 | 缩小到模块级 |
| agent 自己发散 | 缺少目标和停止条件 | 写清边界和停下来的条件 |
| 没有 Review | 并行改动难合并 | 合并前统一 review |

## 10. 课堂工坊：一次多 Agent 任务从拆分到合并

### 案例一：只读三路分析

目标：先练“并行读证据”，不让多个 agent 同时写文件。

```text
这个项目登录模块要升级。请先制定 subagent 分工计划，然后并行只读分析：
- frontend：只读 src/pages/login.tsx 和 src/components/auth/*
- backend：只读 src/api/auth/* 和 src/lib/auth/*
- test：只读 tests/auth/* 和 package.json

每个 subagent 只输出证据、风险和建议修改点。不要修改文件。
```

你应该看到：每个子任务都有自己的文件范围；输出能说明证据来自哪个文件；主线程最后汇总冲突和共同结论。

### 案例二：前端、后端、测试分文件写入

目标：练习并行写入时的文件所有权。

```text
在 worktree 里处理登录错误提示优化。请按文件所有权拆分：
- frontend 只改 src/pages/login.tsx
- backend 只改 src/api/auth/errors.ts
- test 只改 tests/auth/login-errors.test.ts
任何 agent 发现需要改其他文件，先停下汇报。最后由主线程合并并运行 npm test -- auth。
```

你应该看到：没有两个 agent 同时改同一个文件；如果需要跨边界修改，主线程先做决策。

### 案例三：让只读 review agent 查合并风险

目标：用 subagent 做独立审查，而不是让实现者自己说自己没问题。

```text
当前 diff 已完成。请启动一个只读 review subagent，重点检查：文件所有权是否被遵守、是否有范围外改动、测试是否覆盖新增行为、是否触碰 secret 或权限配置。review agent 不要修改文件。
```

你应该看到：review 输出按问题严重度列出；主线程根据 review 决定修复、撤销或保留。

## 11. 多 Agent 运营手册

Subagents 一旦进入真实项目，最重要的是运营纪律。没有纪律的并行就是多个 AI 同时制造 diff。

### 11.1 任务拆分表

| 子任务类型 | 推荐 agent | 是否允许写 | 输出 |
|---|---|---|---|
| 查官方文档 | Explorer | 否 | 来源、结论、版本差异 |
| 查现有代码 | Explorer | 否 | 相关文件、调用链、风险 |
| 实现前端 | Worker | 是，限定文件 | diff、验证命令 |
| 补测试 | Worker | 是，限定测试目录 | 测试文件、运行结果 |
| 安全审查 | Reviewer | 否 | findings、严重度、证据 |
| 合并判断 | Main thread | 视情况 | 冲突处理和最终方案 |

### 11.2 并行写入的文件所有权协议

```text
每个 worker 只能修改自己拥有的文件。
如果发现必须修改其他文件，先停止并汇报。
任何共享文件由主线程统一修改。
Review agent 只读，不修改文件。
最终由主线程运行测试和看 Review。
```

共享文件包括路由表、公共类型、全局样式、配置文件、lockfile、迁移文件。这些文件很容易成为冲突中心，不要让多个 agent 同时改。

### 11.3 多 Agent 复盘问题

任务结束后问：

1. 哪些子任务真正并行节省了时间？
2. 哪些子任务其实有依赖，不该并行？
3. 是否出现文件所有权冲突？
4. review agent 是否发现实现 agent 没发现的问题？
5. 主线程合并时是否有足够证据？
6. 下次应该减少还是增加 agent 数量？

Subagents 的成熟标志不是"用了很多 agent"，而是团队知道什么时候少用。

## 常见问题

### Q1：Subagents 会自动更正确吗？

不会。它们只是并行执行单元。正确性来自清晰分工、约束和 Review。

### Q2：什么时候不用 Subagents？

单文件小改、一步任务、目标不清楚的任务，都不应该先拉 subagents。

### Q3：Subagents 能和 Automation 一起用吗？

可以，但自动化任务更要限制权限和范围。

### Q4：Subagent 越多结果越好吗？

不是。每个 subagent 都有上下文、合并和冲突成本。小任务用 1 个主线程更快；只有独立子任务足够多时才并行。

### Q5：Subagents 会共享同一个文件状态吗？

取决于当前 App / worktree / 任务方式。不要假设所有 agent 自动看到彼此最新改动。并行写入时必须用文件所有权和主线程合并收口。

### Q6：能不能让 subagent 自己决定下一步？

可以在明确边界内让它推进，但大方向、扩大范围、写权限、外部服务动作应回到主线程或人工确认。

---

## 12. 深入理解：Subagent 的价值是“隔离思考噪音”

Subagents 很容易被误解成“多开几个 AI 就更聪明”。真正的价值不是数量，而是隔离。复杂任务里最容易出问题的不是模型不会想，而是主线程被日志、临时尝试、失败输出、局部推理和无关细节淹没。Subagent 的作用是把这些噪音放到子线程里，让主线程保留决策、边界和最终合并判断。

可以用这张表给新人讲：

| 主线程负责 | Subagent 负责 |
|------------|---------------|
| 锁定目标和非目标 | 做一块明确的探索或执行 |
| 拆分任务和分配边界 | 在边界内读取、测试、修改或总结 |
| 决定是否接受结果 | 返回证据、结论和风险 |
| 合并不同结果 | 不擅自扩大范围 |
| 对用户交付最终说法 | 不替主线程做全局承诺 |

如果一个子任务无法用一句话说清楚输入、范围、输出和停止条件，就暂时不要交给 subagent。

### 12.1 三个适合并行的任务类型

| 类型 | 适合原因 | 示例 |
|------|----------|------|
| 读多写少 | 不容易产生文件冲突 | 三个 agent 分别看安全、测试、性能 |
| 分文件写入 | 可以明确文件所有权 | 一个改前端，一个改后端，一个补测试 |
| 长日志分析 | 主线程不需要吞完整输出 | 每个 agent 分析一个 CI job 日志 |

### 12.2 三个不适合并行的任务类型

| 类型 | 风险 | 更好的做法 |
|------|------|------------|
| 需求还不清楚 | 每个 agent 会按不同理解执行 | 主线程先澄清 |
| 多个 agent 改同一文件 | 冲突和重复修改很多 | 拆出文件所有权 |
| 需要连续人工判断 | 子线程会等或猜 | 主线程逐步推进 |

## 13. Subagent 任务卡：让每个子线程有清楚边界

好的 subagent prompt 像一个小合同。它不用长，但要有边界。

```text
Spawn one explorer agent for the test suite.

Scope:
- Read package.json, test config, and failing test output.
- Do not edit files.

Question:
- Which tests are most relevant to this change?
- Which command should I run locally before review?

Return:
- 5 bullet summary
- exact commands
- files inspected
```

这张卡的关键点：

- `Scope` 控制读写范围。
- `Question` 控制思考方向。
- `Return` 控制回传格式。
- `Do not edit files` 把风险压低。

### 13.1 写入型任务卡

写入型 subagent 需要更明确：

```text
Spawn one worker agent for the documentation update.

Ownership:
- Only edit docs/api-auth.md and docs/api-errors.md.
- Do not edit code, tests, config, or generated files.

Task:
- Update the docs to match the behavior described in src/auth/errors.ts.
- Preserve existing tone and headings.

Verification:
- Check markdown fences and links in the two edited files.

Return:
- Files changed
- Summary of edits
- Any behavior questions you could not answer from source
```

注意这里的 “Verification” 是给子线程自己的操作说明，不是文章里的外部评审标准。它的作用是让 worker 回来时带证据，而不是只说“改好了”。

### 13.2 Review 型任务卡

Review agent 不应该被要求“修掉所有问题”。它应该先找问题：

```text
Spawn one reviewer agent.

Scope:
- Review current branch diff against main.
- Read nearby code when needed.
- Do not edit files.

Lens:
- correctness
- security
- missing tests

Return:
- findings first
- file references
- severity labels: high, medium, low
- open questions
```

Review 型 subagent 的价值在于“独立视角”。如果主线程已经准备改代码，就不要让 reviewer 同时改同一批文件。

## 14. 主线程合并：不要把多个答案简单拼起来

Subagents 返回多个结果后，主线程最重要的动作不是复制粘贴，而是合并判断。

```text
Agent A: 认为主要风险是 auth redirect。
Agent B: 认为主要风险是 missing regression test。
Agent C: 没发现安全问题，但指出日志里有 flaky test。

主线程应该输出：
1. 共识：auth redirect 需要补测试。
2. 分歧：是否属于安全问题还需要看威胁模型。
3. 下一步：先补 regression test，再决定是否改 redirect 行为。
```

### 14.1 合并时看四件事

| 维度 | 问题 |
|------|------|
| 共识 | 多个 agent 是否指向同一风险 |
| 冲突 | 结论不一致是事实冲突还是视角不同 |
| 证据 | 哪个 agent 给了可复查文件、命令或日志 |
| 行动 | 哪个结论能转成下一步小改动 |

### 14.2 合并提示词

```text
请把三个 subagent 的结果合并成一个行动计划。
不要平均分配篇幅。
优先处理：
1. 有文件证据的问题
2. 多个 agent 都提到的问题
3. 会阻塞发布的问题

输出：
- 共同发现
- 分歧点
- 下一步最小行动
- 暂时不处理的内容和理由
```

这类提示词能防止主线程把所有意见平铺，最后看起来很厚但没有决策。

## 15. 多 Agent 写入工作流：文件所有权是核心

并行写文件不是不能做，但要像小型工程组织一样管理所有权。

### 15.1 文件所有权表

| Agent | 可写文件 | 只读文件 | 不碰 |
|-------|----------|----------|------|
| frontend-worker | `src/components/CheckoutForm.tsx` | `src/api/**` | `db/**` |
| backend-worker | `src/api/checkout.ts` | `src/components/**` | `db/migrations/**` |
| test-worker | `tests/checkout.spec.ts` | `src/**` | 生产配置 |
| reviewer | 无 | 全部 diff | 全部写入 |

如果无法写出这张表，就说明任务还没有拆清楚。

### 15.2 并行写入 prompt

```text
Use parallel subagents for this change.

Worker 1:
- owns src/components/CheckoutForm.tsx
- only updates UI state and error display

Worker 2:
- owns src/api/checkout.ts
- only updates request validation

Worker 3:
- owns tests/checkout.spec.ts
- only adds or updates tests

Shared merge contract:
- keep ownership boundaries from the plan
- report any file that was touched outside the assigned area
- include verification evidence with each worker result

Main thread:
- wait for all workers
- inspect diffs
- resolve conflicts before final answer
```

这个 prompt 的重点是：写入范围被拆成了互不重叠的文件集合。

### 15.3 冲突处理

如果两个 agent 都改了同一段逻辑，不要让其中一个“覆盖”另一个。主线程应该先暂停合并：

```text
两个 worker 都改到了 checkout validation。
请先不要继续写文件。
请分别说明：
1. 你为什么需要改这个位置
2. 你依赖的行为假设是什么
3. 你的改动和另一个 worker 的改动是否能合并
4. 最小保留方案是什么
```

这能把冲突从“文本冲突”还原成“设计冲突”。

## 16. 自定义 agents：什么时候值得写配置

Codex 有内置 agent 类型，例如通用、执行型和探索型。大多数人先学内置分工就够了。只有当团队反复需要某种稳定角色时，才考虑写自定义 agent。

适合自定义的信号：

| 信号 | 示例 |
|------|------|
| 同一种 review 反复出现 | 安全 reviewer、性能 reviewer |
| 需要固定模型或 reasoning 设置 | 深度架构分析 |
| 需要固定沙盒 | 只读 explorer |
| 需要固定技能开关 | 文档审查 agent 绑定 docs skill |
| 需要团队共用昵称和职责 | 多人协作时更容易识别 |

### 16.1 自定义 agent 文件示例

```toml
name = "security-reviewer"
description = "Review code changes for security risks, sensitive data exposure, and unsafe external interactions."
developer_instructions = """
Review as a security-focused owner.
Prioritize concrete, reproducible issues over broad advice.
Do not edit files.
Return findings with file references and uncertainty labels.
"""
nickname_candidates = ["Sentinel", "Audit", "Shield"]
```

自定义 agent 不是给一次性任务写的。一次性任务放在 prompt 里，长期角色才放进 agent 配置。

### 16.2 项目级和个人级 agents

| 位置 | 适合内容 |
|------|----------|
| `.codex/agents/` | 项目团队共享的角色 |
| `~/.codex/agents/` | 个人常用角色 |

项目级 agent 要更保守，因为它会影响团队成员的协作体验。个人级 agent 可以更贴近个人习惯。

### 16.3 不要把任务写进 agent 身份

不好的 agent：

```toml
name = "fix-checkout-bug"
description = "Fix today's checkout bug in src/api/checkout.ts."
developer_instructions = "Edit checkout files and make tests pass."
```

好的 agent：

```toml
name = "api-debugger"
description = "Investigate API behavior regressions and suggest minimal fixes."
developer_instructions = """
Investigate API failures by reading routes, tests, logs, and nearby code.
Prefer small fixes.
Ask the main thread before widening scope.
"""
```

角色应该长期有效，任务应该一次性明确。

## 17. Subagents 与权限、沙盒、审批

Subagent 不是权限绕过器。它会受到当前会话权限和沙盒的约束。课程里可以这样讲：

| 设置 | 对 subagent 的影响 |
|------|-------------------|
| 当前 sandbox | 子线程继承当前边界 |
| 当前审批策略 | 子线程遇到需要审批的动作也受限制 |
| 运行时 override | 主线程临时改过的权限会影响子线程 |
| 自定义 agent sandbox | 可以更窄，但不应该拿来偷偷扩大 |

如果一个子线程需要新权限，在交互环境里可能会出现来自子线程的审批请求。人要看清请求来自哪个线程，再决定是否允许。

### 17.1 权限安全 prompt

```text
Use subagents for read-only analysis only.
Do not run commands that modify files.
Do not request broader sandbox permissions.
If any agent believes broader access is needed, it should return the reason instead of asking for approval.
```

### 17.2 写入前收窄 prompt

```text
Before spawning writer agents, propose the file ownership split.
Do not start write agents until the split is clear in the main thread.
Prefer read-only explorer agents first if the code ownership is uncertain.
```

## 18. Subagents 与 Worktree：隔离的不只是上下文

Worktree 隔离文件状态，Subagent 隔离思考和执行线程。两者经常一起用，但不是同一个东西。

| 机制 | 隔离什么 | 解决什么问题 |
|------|----------|--------------|
| Subagent | 上下文、任务、角色 | 防止主线程被噪音污染 |
| Worktree | 文件、分支、未提交改动 | 防止并行任务互相覆盖 |

### 18.1 适合 Worktree + Subagent 的场景

```text
我想同时探索两个修复方向：
方向 A：保持现有 API，只修边界条件。
方向 B：重构 API，让调用方显式传入状态。

请用 worktree 隔离两个方向。
每个方向一个 worker agent。
每个 agent 只在自己的方向里实现最小改动并运行相关测试。
最后主线程比较两种方案的风险、改动范围和测试结果。
```

这个场景里，Worktree 防止两个方向互相覆盖；Subagent 让两个方向并行推进。

### 18.2 不适合 Worktree + Subagent 的场景

```text
请派 5 个 agent 一起把整个项目优化一下。
```

这个 prompt 没有边界、没有所有权、没有合并策略。它会制造大量不可比较的改动。

## 19. Subagent 失败模式大全

| 失败模式 | 表现 | 修复方式 |
|----------|------|----------|
| 任务卡太宽 | 每个 agent 都在做全局分析 | 缩小 scope |
| 输出格式不一致 | 主线程难合并 | 统一 return 格式 |
| 写入范围重叠 | diff 冲突多 | 建文件所有权表 |
| 等待策略不清 | 主线程不知道何时继续 | 写明 wait for all 或先返回谁 |
| 子线程自作主张 | 改了不该改的文件 | 加“不碰”列表 |
| 结论没证据 | 很多观点无法复查 | 要求文件、命令、日志 |
| agent 数过多 | token 和时间飙升 | 先 2-3 个高价值视角 |
| 嵌套委派失控 | 子线程继续开子线程 | 保持默认深度或明令不再委派 |

### 19.1 修复“输出太散”的 prompt

```text
The subagent results are too broad.
Please normalize them into this shape:
- finding
- evidence
- impacted files
- suggested next action
- confidence

Drop points that do not cite evidence.
```

### 19.2 修复“agent 做重复工作”的 prompt

```text
The agents overlapped too much.
Please redesign the split by ownership:
1. one agent for data model
2. one agent for API surface
3. one agent for tests

Each agent should list files it will read and files it may edit before starting.
```

### 19.3 修复“合并后逻辑断裂”的 prompt

```text
After merging subagent output, check for contradictions:
1. Are two agents assuming different behavior?
2. Did one agent change code that another agent's test does not cover?
3. Are there duplicate fixes?
4. Is any suggested action now obsolete?
```

## 20. 企业团队怎么训练 Subagents

团队训练不要从“开很多 agent”开始，而要从“拆任务”开始。

### 20.1 第一周：只读并行

练习：

```text
Spawn three read-only explorer agents:
1. one for architecture overview
2. one for test strategy
3. one for security-sensitive files

No edits.
Wait for all.
Return a merged onboarding map for a new engineer.
```

目标是让团队学会看不同视角，而不是追求产出 diff。

### 20.2 第二周：分文件写入

练习：

```text
Use two worker agents with disjoint file ownership:
- docs-worker edits docs/getting-started.md only
- tests-worker edits tests/onboarding.spec.ts only

Main thread reviews both diffs before final response.
```

目标是让团队学会所有权和合并。

### 20.3 第三周：Review agent 加入

练习：

```text
After the workers finish, spawn one read-only reviewer agent.
The reviewer should check:
- behavior regression
- missing tests
- docs/code mismatch
Do not edit files.
```

目标是让团队把“执行”和“审查”分开。

### 20.4 第四周：沉淀 agent 模板

团队可以沉淀三类模板：

```text
Explorer template: 只读探索，返回地图。
Worker template: 分文件写入，返回 diff 摘要和命令。
Reviewer template: 只读审查，返回 findings 和证据。
```

这些模板比随手喊“开几个 agent”更能提高稳定性。

## 21. 课堂综合案例：三路并行审查一个 PR

完整 prompt：

```text
Please review the current branch with parallel subagents.

Spawn three read-only agents:
1. Security reviewer
   - focus on auth, secrets, external calls, permission checks
2. Test reviewer
   - focus on missing regression tests and flaky test risk
3. Maintainability reviewer
   - focus on unnecessary complexity and coupling

All agents:
- read current branch diff against main
- inspect nearby code when needed
- do not edit files
- return findings with file references

Main thread:
- wait for all agents
- merge duplicate findings
- separate confirmed issues from open questions
- recommend the next smallest action
```

主线程最终应该输出类似：

```md
# PR Review Summary

## Confirmed Findings

1. Auth redirect can bypass the intended fallback path.
   Evidence: src/auth/redirect.ts and tests/auth.spec.ts.
   Next action: add regression test before changing behavior.

2. Error state is documented but not tested.
   Evidence: docs/auth.md and tests/auth.spec.ts.
   Next action: add one failing test, then fix implementation.

## Open Questions

- Whether legacy clients still depend on the old redirect behavior.

## Suggested Next Step

Make one small patch for the redirect behavior and run the auth test file only.
```

这个案例体现了 Subagents 的核心：并行收集证据，主线程负责判断。

## 22. 综合工坊：三路只读 review + 一路主线程合并

这个工坊是学习 Subagents 的最佳入口，因为它高价值、低冲突、不需要并行写文件。

### 22.1 任务背景

当前分支改了登录逻辑。你想从安全、测试、维护性三个角度看风险。

### 22.2 Prompt

```text
沿用上一节“三路并行审查一个 PR”的 prompt。
本节不再重复写 agent 分工，重点只训练主线程如何合并输出。

主线程合并时必须做三件事：
1. 合并重复发现。
2. 区分确认问题和开放问题。
3. 给出下一步最小行动。
```

### 22.3 主线程合并输出模板

```md
# Parallel Review Summary

## Confirmed Findings

1. ...

## Cross-Agent Agreement

- ...

## Disagreements

- ...

## Open Questions

- ...

## Next Smallest Action

- ...
```

### 22.4 学习重点

```text
- subagent 负责独立视角。
- main thread 负责合并和排序。
- 只读 review 是最适合第一次练习的 subagent 场景。
- 不要把 reviewer 变成 writer。
```

## 23. 综合工坊：分文件并行写入

这是进阶工坊。只有在文件所有权清楚时才做。

### 23.1 任务背景

你要修一个 checkout 错误状态：

```text
- UI 文案在 CheckoutForm。
- API validation 在 checkout route。
- 测试在 checkout spec。
```

### 23.2 文件所有权

```text
frontend-worker:
- may edit src/components/CheckoutForm.tsx
- may read src/api/checkout.ts

backend-worker:
- may edit src/api/checkout.ts
- may read src/components/CheckoutForm.tsx

test-worker:
- may edit tests/checkout.spec.ts
- may read src/components/CheckoutForm.tsx and src/api/checkout.ts

reviewer:
- read-only after workers finish
```

### 23.3 Prompt

```text
Use parallel subagents for this checkout fix.

Before starting, repeat the file ownership split.

Worker 1: frontend
- only edit src/components/CheckoutForm.tsx
- update the displayed error state

Worker 2: backend
- only edit src/api/checkout.ts
- tighten request validation

Worker 3: tests
- only edit tests/checkout.spec.ts
- add regression coverage

All workers:
- do not edit each other's files
- do not refactor unrelated code
- return changed files and commands run

Main thread:
- wait for all workers
- inspect combined diff
- ask before resolving conflicts
```

### 23.4 合并后 review

```text
Now spawn one read-only reviewer agent.
Review the combined diff for:
- behavior mismatch between UI and API
- missing tests
- accidental unrelated changes
Do not edit files.
```

这个工坊让学生理解：并行写入不是"同时乱改"，而是小型协作管理。

## 24. Subagent 设计题

### 24.1 题目 A

```text
请开 8 个 agent，把整个项目优化一遍。
```

判断：不合格。范围过大、没有所有权、没有合并策略。

改写：

```text
请先只读分析项目，提出最多 3 个适合并行处理的独立任务。
不要启动 subagents，直到任务边界清楚。
```

### 24.2 题目 B

```text
请派 3 个 read-only agent 分别看安全、测试和性能风险。
每个 agent 返回 5 条以内 findings 和文件证据。
主线程合并重复项。
```

判断：合格。读多写少，视角独立。

### 24.3 题目 C

```text
请让两个 agent 同时改 src/auth.ts。
一个修 bug，一个重构。
```

判断：不合格。写入同一文件且目标冲突。

改写：

```text
先用一个 read-only agent 分析 bug 根因。
主线程决定最小修复后，再让一个 worker 修改 src/auth.ts。
```

## 25. Subagent 进阶常见问题

### Q1：Codex 会自动开 subagents 吗？

不会默认自动开。你需要明确要求 subagents 或 parallel agent work。这样设计是为了避免无意增加 token、时间和协调风险。

### Q2：Subagent 会继承当前权限吗？

会受当前 sandbox 和审批策略约束。不要把 subagent 当成绕过权限的办法。

### Q3：Subagent 能不能再开 subagent？

配置上有深度限制，默认不鼓励递归委派。课程中建议主线程统一调度，避免 fan-out 失控。

### Q4：Subagent 越多越快吗？

不一定。并行能节省等待时间，但会增加 token、合并成本和冲突风险。先从 2-3 个独立视角开始。

### Q5：自定义 agent 文件适合新手吗？

新手先学内置 explorer、worker、reviewer 风格的分工。自定义 agent 适合团队反复使用的稳定角色。

### Q6：Subagent 和 Skill 怎么组合？

Skill 定义工作法，subagent 执行一块任务。比如三个 reviewer agent 都可以使用同一个 `pr-risk-review` Skill，但视角不同。

## 26. Subagent 调度案例：一次改动不要分成一锅粥

假设你要让 Codex 更新一个登录流程：按钮文案要改、错误提示要补、测试也要跟上。这个任务看起来不大，但如果直接让多个 agent 同时写代码，很容易出现两个问题：有人改了同一个文件，有人根据旧代码给出过期判断。

更稳的做法是先让主线程把任务拆成一条清楚的流水线。

```text
第一步：只读摸底
- 找登录流程涉及的组件、路由、测试和文档。
- 标出哪些文件可能要改，哪些文件只读参考。
- 不做任何代码修改。

第二步：窄范围修改
- 只允许改已经确认的组件和测试文件。
- 每个 worker 拿到独立文件范围。
- 返回改过的文件、运行过的命令、没有覆盖的风险。

第三步：只读复核
- 检查 diff 是否越界。
- 检查测试和实际行为是否一致。
- 把分歧交回主线程，不直接继续扩写。
```

这个案例里，“多 agent”不是为了显得热闹，而是为了把三种脑力分开：探索时不要动手，修改时不要越界，审查时不要顺手重构。你可以把它当成团队协作的缩小版：先对齐事实，再分工产出，最后统一收口。

一个可直接复制的调度 prompt：

```text
我想更新登录流程的错误提示和相关测试。

请先只读探索：
1. 找出登录流程相关的组件、路由、测试和文档。
2. 按“可能需要修改 / 只读参考 / 不相关”分类。
3. 给出建议拆分，不要修改文件。

探索完成后，再等我确认下一步。
```

确认范围后再进入执行：

```text
根据刚才确认的范围执行修改。

约束：
1. 只修改已列入“可能需要修改”的文件。
2. 每次修改后说明改了什么行为。
3. 运行与登录流程最相关的测试。
4. 如果发现需要改新文件，先停下来说明原因。
```

最后复核：

```text
请只读审查当前 diff。

重点检查：
1. 是否有超出登录错误提示目标的改动。
2. 测试是否覆盖新增提示。
3. 是否遗漏空状态、网络失败或国际化文案。
4. 哪些风险需要人工点开页面确认。
```

## 27. Subagent 作业：写任务拆分表

```md
# Subagent Task Split

## Goal

...

## Agents

| Agent | Role | May read | May edit | Return |
|-------|------|----------|----------|--------|
| A | explorer | | none | |
| B | worker | | | |
| C | reviewer | | none | |

## Merge Plan

...
```

要求：如果 `May edit` 出现重叠，学生必须说明为什么安全；说不清就要重拆。

## 28. Subagent 失败恢复：并行结果互相打架怎么办

Subagents 的难点不在“开几个 agent”，而在结果回来后怎么合并。最常见的失败是两个 agent 都给出看似合理、但彼此冲突的建议。

例子：

```text
Explorer A：
auth redirect bug 应该改 `redirect.ts`，因为 query params 在 helper 里丢失。

Explorer B：
auth redirect bug 应该改 `login.tsx`，因为 form submit 时没有传 callback URL。

Reviewer C：
当前测试只覆盖默认 redirect，不覆盖 callback URL。
```

不要让主线程直接任选一个。先让 Codex 做冲突整理：

```text
请合并三个 subagent 的结果。

要求：
1. 哪些结论一致。
2. 哪些结论冲突。
3. 每个结论依赖什么文件证据。
4. 下一步最小验证动作是什么。
5. 不要修改文件。
```

如果冲突来自事实不同，就先验证事实：

```text
请只读检查：
1. callback URL 是在哪里读取的。
2. callback URL 是在哪里写入 redirect helper 的。
3. 当前测试覆盖哪一段。

只回答文件和行为，不给修复方案。
```

如果冲突来自任务边界不同，就让主线程重新定边界：

```text
本次只修“登录后没有回到原页面”。
不处理表单文案、不处理 toast、不重构 auth。

请基于这个边界重新判断哪些 subagent 建议保留。
```

Subagent 输出不是投票。三个 agent 说三种方案时，主线程要回到证据、边界和下一步验证，而不是看哪个说得更自信。

## 29. Subagent 写入案例：分文件不等于安全

很多人以为“不同 agent 改不同文件”就一定安全。实际不一定，因为两个文件可能表达同一个行为。

例子：

```text
Worker A：修改 `redirect.ts`。
Worker B：修改 `login.tsx`。
Worker C：修改 `auth-redirect.test.ts`。
```

看似分文件，实际都在改 auth redirect。风险是 A 和 B 同时修同一个 bug，测试最后只证明其中一个路径。

更稳的拆法：

```text
阶段 1：Explorer 只读确认行为链。
阶段 2：主线程决定只改 helper 还是 form。
阶段 3：一个 worker 改实现，一个 worker 改测试。
阶段 4：reviewer 只读审查完整 diff。
```

执行 prompt：

```text
请不要并行写 auth redirect 的两个实现入口。

先只读确认行为链：
1. callback URL 从哪里进入系统。
2. 保存在哪里。
3. redirect helper 如何读取。
4. 测试应该覆盖哪一层。

确认后再决定一个实现修改点。
```

如果确实要并行写，文件所有权要更细：

```md
# Write Ownership

## Worker A

May edit:
- src/auth/redirect.ts

Must not edit:
- login component
- tests

Return:
- behavior changed
- edge cases

## Worker B

May edit:
- tests/auth-redirect.test.ts

Must not edit:
- source code

Return:
- covered behavior
- remaining untested paths
```

这个案例教的不是"不要并行"，而是不要把并行当成省脑子的办法。并行之前要先知道行为边界，否则只是更快制造冲突。

## 30. Subagent 任务卡模板：让结果能被主线程接住

一个好的 subagent 任务卡要短，但不能缺关键边界。

```md
# Subagent Task Card

## Goal

Find why auth redirect drops callback URL.

## Mode

Read-only exploration.

## May Read

- src/auth/**
- tests/auth/**
- docs/auth.md

## Must Not

- Edit files.
- Run broad formatters.
- Suggest unrelated auth refactors.

## Return

1. Files inspected.
2. Behavior chain.
3. Likely root cause.
4. Next smallest verification.
5. Uncertainties.
```

写入型任务卡：

```md
# Worker Task Card

## Goal

Implement the minimal redirect helper fix.

## May Edit

- src/auth/redirect.ts

## Must Not Edit

- src/auth/login.tsx
- tests/auth-redirect.test.ts
- package files

## Stop If

- The fix requires changing form submission.
- A new dependency seems necessary.
- Existing tests describe conflicting behavior.

## Return

- Changed files.
- Behavior changed.
- Commands run.
- Remaining risk.
```

审查型任务卡：

```md
# Review Task Card

## Goal

Review the combined auth redirect diff.

## Mode

Read-only review.

## Focus

- Scope creep
- Missing tests
- Auth/security regression
- Unrelated UI changes

## Return

- Findings with file evidence.
- Blocking vs follow-up.
- Suggested next prompt.
```

任务卡的价值在于让 subagent 的结果可合并。没有任务卡，subagent 往往会把“我觉得有用的信息”都带回来；有任务卡，主线程才能判断结果是否完成了它该完成的那一小块。

## 31. Subagent 合并报告：主线程最后要交付什么

Subagents 跑完以后，最终交付不应该是一堆 agent 原话。主线程要把结果合并成一个可行动报告。

合并报告模板：

```md
# Subagent Merge Report

## Original Goal

...

## Work Split

- Explorer:
- Worker:
- Reviewer:

## Results Accepted

- ...

## Results Rejected

- ...

## Conflicts

- ...

## Files Changed

- ...

## Commands Run

- ...

## Remaining Risk

- ...

## Next Action

- ...
```

合并 prompt：

```text
请把所有 subagent 返回结果合并成一份主线程报告。

要求：
1. 不逐字粘贴每个 agent 的长输出。
2. 标出哪些结论被采纳，哪些被拒绝。
3. 对冲突给出原因和下一步。
4. 列出最终改动文件和命令证据。
5. 给出用户下一步应该看的内容。
```

示例输出：

```md
# Subagent Merge Report

## Original Goal

Fix auth redirect callback URL loss.

## Results Accepted

- Explorer confirmed callback URL enters via login route.
- Worker changed redirect helper only.
- Reviewer confirmed no payment or toast files changed.

## Results Rejected

- Explorer suggestion to refactor auth form was out of scope.

## Conflicts

- Test location was disputed. Resolved by placing regression test with existing auth redirect tests.

## Remaining Risk

- Manual browser check still useful for SSO path.
```

这份报告很重要，因为用户没有义务阅读每个 subagent 的完整输出。多 agent 协作的最后一步不是"大家都说完了"，而是主线程把结果变成一个清楚的交付。

## 32. Subagent 课堂练习：三人小组模拟

即使没有真正开启多个 agent，也可以用课堂模拟训练分工。

任务：

```text
当前 PR 修改登录 redirect。
请模拟三个独立检查者：
1. 代码路径探索。
2. 测试覆盖审查。
3. scope creep 审查。

每个检查者只输出自己的结论。
最后由主线程合并。
```

主线程合并 prompt：

```text
请把三个检查者的结果合并。
输出：
1. 一致结论。
2. 冲突结论。
3. 需要继续查的事实。
4. 最小修复建议。
5. 不应该进入本 PR 的事项。
```

这类练习能让读者先学会“分视角”和“合并证据”，再使用真正的 subagents。工具使用之前先学协作模型，会让后面的并行执行更稳。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 知道什么时候该用Subagents（可拆分、多文件、独立子任务）
- [ ] 知道什么时候不该用（单文件小改、一步任务）
- [ ] 能写出包含总目标、边界、文件所有权、停止条件的分工提示词
- [ ] 理解Worktree + Subagents + Review的组合模式
- [ ] 知道合并前必须看证据、看冲突、看所有权
- [ ] 不为了让任务"看起来高级"而滥用Subagents

**全部勾选后即掌握 Codex Subagents。**

---

## 附录

### A. Subagents使用判断

| 条件 | 适合？ |
|------|--------|
| 任务可拆成独立子任务 | ✅ |
| 多个文件/模块互不重叠 | ✅ |
| 需要独立审查 | ✅ |
| 下一步必须等一个结果 | ❌ 先主线程 |
| 单文件小改 | ❌ |

### B. 分工提示词模板

```text
先给出 subagent 分工计划，不要立刻改文件。
目标：[总目标]
范围：[目录/文件]
约束：[不能做的事]
分工：
- Agent A：[任务A]
- Agent B：[任务B]
汇总后再决定是否执行。
```

### C. 推荐学习资源

- **Codex Subagents 官方文档**：https://developers.openai.com/codex/subagents
- **本系列上一篇**：[CX-07 Plugins 连接器](./CX-07-Codex-Plugins连接器完整指南.md)
- **本系列下一篇**：[CX-09 Automations 后台任务](./CX-09-Codex-Automations后台任务完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-09 Automations：App 里的后台任务和周期检查](./CX-09-Codex-Automations后台任务完整指南.md)。
