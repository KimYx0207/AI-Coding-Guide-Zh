# CX-14 Codex 与 Claude Code 对比：从 App 主线出发做工具选择

主要来源：OpenAI Codex App / CLI / Web 官方文档，以及 Claude Code 官方命令、插件、MCP、Hooks、Skills 文档。模型、价格和开放范围变化快，本篇不写固定数值结论。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：1-2小时
> - **难度等级**：⭐⭐ 入门级
> - **更新日期**：2026年6月18日
> - **信息来源**：OpenAI Codex App/CLI/Web 官方文档、Claude Code 官方命令/插件/MCP/Hooks/Skills 文档
> - **前置要求**：已完成CX-01至CX-13，或已熟悉Claude Code基本使用

---

## 📚 本课学习目标

完成本课学习后，你将能够：

> **2026-06-18 迁移口径**：Codex App 26.609 的 Migrate to Codex 适合把 Claude Code / Claude Cowork 的项目经验迁移成 Codex 工作流，但迁移对象是“项目事实、权限边界、验证命令和可复用流程”，不是把 `.claude` 目录原样复制到 Codex。

1. **理解两个工具的定位差异**：Codex App是桌面开发主控台，Claude Code是覆盖 terminal、IDE、desktop app 和 browser 的多端 coding agent
2. **判断何时优先Codex**：桌面多线程、Review面板、Automations、连接器、Cloud handoff
3. **判断何时优先Claude Code**：CLI 深度协作、Hooks、Skills、MCP、Agent Teams、IDE / Desktop / Browser 多端接力
4. **设计双工具共存策略**：按任务类型分工，不让他们同时改同一批文件
5. **管理双工具配置**：AGENTS.md服务Codex，CLAUDE.md服务Claude Code，两边写相同项目事实
6. **安全共享MCP**：MCP server可复用但配置方式不同，权限分别管理
7. **避免常见选择错误**：不按模型名判断、不按价格下结论、看工作流重心
8. **落地团队工具选择**：先选一个主力，另一个作补充，不一开始双主线培训

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速选型（⏱️ 10分钟）

**适合人群**：想快速知道选Codex还是Claude Code

**只看这些章节**：

```
✅ 第1部分：一句话对比（2分钟）
✅ 第2-3部分：什么时候优先Codex / Claude Code（5分钟）
✅ 第7部分：选择标准（3分钟）
```

---

### 路径B：完整学习（⏱️ 1-2小时）

**适合人群**：想设计双工具共存策略

**学习顺序**：从头到尾所有章节

---

## 术语表（选型必读）

工具对比最怕变成“谁更强”的口水战。先把对比维度固定住。

| 术语 | 含义 | 为什么重要 |
|---|---|---|
| Surface | 用户主要在哪个界面工作 | App、CLI、Web、IDE 会改变学习路径 |
| Workflow center | 工作流中心 | Codex App 偏桌面控制台，Claude Code 偏终端工具链 |
| Governance | 权限、审计、团队配置 | 企业落地看这里，不只看模型 |
| Extensibility | 扩展能力 | Skills、MCP、Plugins、Hooks、Subagents |
| Handoff | 任务在本地、云端、PR 之间接力 | 决定长任务和团队协作体验 |
| Review loop | 修改、审查、反馈、再修的闭环 | 决定日常开发效率 |
| Migration cost | 从一种工具切到另一种的成本 | 配置、习惯、培训、自动化都算 |

## 0. 正确对比方法

老金我写 Codex 与 Claude Code 对比，不是为了站队，而是帮读者按任务、团队和风险选择主工具。

不要按“模型名、跑分、价格、谁更新快”来做长期选型。更稳的比较顺序是：

```text
团队工作界面
  -> 常见任务类型
  -> 权限和审计要求
  -> 外部系统连接
  -> 自动化和并行需求
  -> 培训成本
  -> 迁移和共存策略
```

这也是为什么 Claude Code 的课程厚：它不是只列功能，而是讲概念、机制、边界、排障、企业落地。Codex 课程也应该按这个标准写，所以前面 13 篇分别覆盖 App 主线、Commands、配置权限、MCP、Skills、Plugins、Subagents、Automations、Review、Cloud、CLI 和安全。

### 0.1 两个工具的“重心”不同

| 维度 | Codex App 更强的学习重心 | Claude Code 更强的学习重心 |
|---|---|---|
| 第一入口 | 桌面 App、线程、Review、Settings | 终端、命令、项目上下文、shell |
| 可视化收口 | Review 面板、diff、inline feedback | 终端 diff、Git 命令、PR / hooks |
| 后台体验 | App Automations、Triage、Cloud handoff | 计划任务、hooks、CLI / SDK 自动化 |
| 扩展方式 | Skills、Plugins、Connectors、MCP | Skills、commands、hooks、MCP、agents |
| 团队培训 | 先教 App 工作流和 Review | 先教终端习惯和项目规则 |
| 风险控制 | Settings、sandbox、approval、Rules、Review | permissions、hooks、settings、shell discipline |

这不是优劣表，而是训练路径表。团队选错重心，教程再厚也会学歪。

### 0.2 迁移时不要硬搬

| Claude Code 习惯 | 迁移到 Codex 时怎么处理 |
|---|---|
| `CLAUDE.md` 项目规则 | 写成 `AGENTS.md`，保留项目事实和安全边界 |
| 自定义 commands | 优先评估是否应改成 Codex Skill |
| Hooks 深度治理 | Codex 也有 Hooks，但事件、信任和配置口径按 Codex 官方文档 |
| MCP server | 可复用思路，但配置和权限分别验证 |
| Subagent / Agent Teams | 按 Codex 当前 Subagents / multi-agent 能力重设边界 |
| 终端工作流 | App 用户先用 Review / Settings / Commands，再看 CLI |

不要把 `.claude/commands`、Claude hooks 配置或 Claude 专属命令直接贴进 Codex 教程。迁移的核心是“意图迁移”，不是“文件结构照搬”。

## 1. 一句话对比


| 工具 | 更像什么 | 适合 |
|---|---|---|
| Codex App | 桌面开发主控台 | 本地多线程、Review、Automations、连接器、Cloud handoff |
| Claude Code | 多端 coding agent 工具链，CLI 仍是强主线 | CLI 深度协作、Hooks、Skills、MCP、Agent Teams、IDE / Desktop / Browser 接力 |

这不是谁替代谁的问题，而是工作流重心不同。

## 2. 什么时候优先 Codex App


优先 Codex App：

- 你希望用桌面线程管理多个任务。
- 你重视 Review 面板和可视化 diff。
- 你想把 Commands、Skills、Plugins、Connectors、Automations 放在一个 App 里。
- 你需要从本地 App 接力到 Cloud / GitHub。
- 团队成员不想先学终端。

## 3. 什么时候优先 Claude Code


优先 Claude Code：

- 团队主要在终端中工作。
- 已经有 `.claude/`、Hooks、Skills、插件生态。
- 需要深度自定义 CLI / SDK / Agent Teams。
- 需要在 SSH、服务器、tmux 等终端环境中长时间运行。

## 4. 双工具共存

推荐分工：

| 任务 | Codex App | Claude Code |
|---|---|---|
| 桌面多线程开发 | 主力 | 辅助 |
| 本地 Review | 主力 | 辅助 |
| 终端自动化 | 辅助 | 主力 |
| Hooks 深度定制 | 辅助 | 主力 |
| App Automations | 主力 | 另建计划任务 |
| Cloud / GitHub handoff | 主力 | 视插件能力 |
| 复杂 Agent Teams | 视当前 App 能力 | 主力 |

## 5. 配置共存

同一仓库可以同时存在：

```text
AGENTS.md
CLAUDE.md
.codex/
.claude/
```

规则：

- `AGENTS.md` 服务 Codex。
- `CLAUDE.md` 服务 Claude Code。
- 两边都要写相同项目事实，但不要互相假设。
- 敏感规则要同步。
- 不要让两个工具同时改同一批文件。

## 6. MCP 共享

MCP server 可以在两个工具中复用，但配置方式不同。

注意：

- 不要复制过期配置。
- 分别验证工具列表。
- 权限和 token 要按工具分别管理。
- 生产系统默认只读。

## 7. 选择标准

不要问“哪个更强”，问这些：

- 团队主要在 App 还是终端？
- 是否需要桌面 Review 和 Automations？
- 是否需要终端 hooks 和 agent teams？
- 外部连接器在哪边更完整？
- 企业权限和审计哪边更容易落地？
- 当前项目是否适合云端 handoff？

### 7.1 选型评分表（给团队会议用）

| 问题 | Codex App 倾向 | Claude Code 倾向 |
|---|---|---|
| 团队成员是否熟终端？ | 不熟，App 更易培训 | 熟，终端效率更高 |
| 是否高度依赖可视化 Review？ | 是 | 一般 |
| 是否已有大量 `.claude/` 资产？ | 需要迁移成本 | 可继续复用 |
| 是否需要桌面多项目并行？ | 是 | 取决于终端和工作区管理 |
| 是否需要深度 shell / SSH / tmux？ | 一般 | 是 |
| 是否需要 App Automations / Triage？ | 是 | 需另建自动化方式 |
| 是否要企业统一权限配置？ | 两边都要评估 | 两边都要评估 |

### 7.2 单人、创业团队、企业的默认建议

| 场景 | 推荐 |
|---|---|
| 单人开发者 | 先用 Codex App 建立 Review 和任务纪律，CLI 作为排查 |
| 终端高手 | Claude Code 或 Codex CLI 都可主线，按生态和团队选择 |
| 非工程背景团队成员 | Codex App 更容易教学 |
| 已有 Claude Code 重资产团队 | 不要立刻切主线，先做 Codex 试点 |
| 企业 | 先选一个主力工具，再把另一个作为补充；不要双主线同时培训 |

## 8. 常见错误

| 错误 | 修正 |
|---|---|
| 按模型名判断工具 | 看工作流 |
| 两个工具同时改同文件 | 分支 / worktree 隔离 |
| 配置只写一边 | AGENTS.md 和 CLAUDE.md 分别维护 |
| MCP 权限复制粘贴 | 分别验证 |
| 用固定价格和跑分下结论 | 写成会变化的信息 |

## 8.1 共存的工作区纪律

双工具共存时，最大的风险不是"两个工具冲突"，而是人让它们同时改同一批文件。

推荐规则：

```text
同一任务只指定一个主力工具。
同一文件同一时间只归一个工具处理。
不同工具用不同分支或 worktree。
AGENTS.md 和 CLAUDE.md 保持项目事实一致。
提交前统一用 Git diff / PR Review 收口。
```

如果 Codex App 改了文件，又让 Claude Code 在同一工作区继续大改，很容易出现上下文错位。更稳的是：Codex 做 App Review 主线，Claude Code 做终端专项；或反过来，但不要同时抢方向盘。

## 9. 课堂工坊：同一个任务分别用两种工具判断

### 案例一：同一个小修任务怎么分配

目标：不要抽象争“谁更强”，而是看工作流。

任务：

```text
修复 README 中一个过时启动命令。只改 README.md，展示 diff，不提交。
```

Codex App 路线：

1. Local thread 打开项目。
2. 发送任务。
3. Review 面板看 README diff。
4. 让 Codex 草拟 commit message。

Claude Code 路线：

1. 在终端进入项目。
2. 用项目上下文发同样任务。
3. 通过终端 diff / git 命令检查。
4. 由人决定提交。

你应该看到：小文档修复两边都能做；如果团队成员不熟终端，Codex App 的 Review 主线更容易教学。

### 案例二：配置共存检查

目标：让 `AGENTS.md` 和 `CLAUDE.md` 讲同一个项目事实，但不互相替代。

```text
阅读 AGENTS.md 和 CLAUDE.md，只输出二者关于安装命令、测试命令、安全边界是否一致。不要修改文件。
```

你应该看到：Codex 能指出事实差异；如果要改，只改对应文件，不把 Claude Code 专属 hooks 写进 Codex App 主线。

### 案例三：团队选型会议的三问题

目标：把工具选择落到团队流程。

```text
基于当前团队情况，帮我判断 Codex App 和 Claude Code 谁做主力：
1. 团队主要在 App 还是终端工作？
2. 我们最常见任务是本地 Review、多线程、自动化，还是终端 hooks / SSH / agent teams？
3. 哪些外部连接器、MCP、权限审计必须先落地？
只给选择建议和理由，不写固定价格或模型结论。
```

你应该看到：建议围绕流程、权限和团队习惯，而不是围绕短期模型名、跑分或价格。

## 10. 综合实战：30 天 Codex App 落地计划

如果团队决定把 Codex App 作为主线，不要要求大家“下周全部用 AI 开发”。更稳的方式是 30 天分阶段落地。

### 第 1 周：建立控制感

目标：每个人能安全打开项目、只读理解、小范围修改、看 Review。

任务：

1. 安装 Codex App，登录账号。
2. 打开一个非生产仓库。
3. 用只读提示总结项目。
4. 改 README 一行。
5. 用 Review 面板确认 diff。
6. 让 Codex 草拟 commit message，但不自动提交。

本周不要引入 MCP、插件、自动化和 Cloud。先让团队知道“Codex 做了什么，我能在哪里检查”。

### 第 2 周：建立项目规则

目标：让 Codex 不再靠每个人临时口头约束。

任务：

1. 为主仓库写根 `AGENTS.md`。
2. 明确安装、测试、lint、build 命令来源。
3. 写清 `.env*`、生产数据、迁移文件、部署命令边界。
4. 新线程验证 Codex 是否读到规则。
5. 对一个真实小 bug 使用 `/plan`，只出计划不执行。
6. 完成一次 `/review` 定向审查。

本周重点是“项目事实一致”。没有这一步，后续 MCP、Subagents、Automations 都容易放大混乱。

### 第 3 周：接入外部能力

目标：只读接入 GitHub / 文档 / MCP / Plugin，建立权限纪律。

任务：

1. 连接 GitHub，只读读取一个 issue 或 PR。
2. 配置一个文档类 MCP，只读核对 README。
3. 安装一个可信插件，先读能力和权限。
4. 写插件 / MCP 登记表。
5. 用 Skill 沉淀一次 code review SOP。
6. 让 Automation 调用只读 Skill 生成一次报告。

本周仍然不自动评论、不自动推送、不自动合并。先让外部上下文进入工作流，再决定哪些写操作值得开放。

### 第 4 周：并行、后台和云端

目标：把 Codex App 放进真实团队协作。

任务：

1. 用 worktree 做一个多文件小功能。
2. 用 Subagents 做三路只读分析。
3. 创建一个只读 Automation，每天总结测试失败。
4. 把一个 PR 评论修复交给 Cloud。
5. Cloud 回流后在 App Review 里检查 diff。
6. 团队复盘：哪些任务适合 Codex，哪些仍然手工或 Claude Code 更合适。

本周重点是“分工和收口”。多 agent、后台和 Cloud 都不能替代主线程判断和人工 Review。

### 30 天后团队应该留下什么

| 产物 | 用途 |
|---|---|
| `AGENTS.md` | 项目事实和安全边界 |
| 常用任务模板 | 减少模糊 prompt |
| Code Review Skill | 统一审查口径 |
| MCP / Plugin 登记表 | 外部能力可追踪 |
| Automation 登记表 | 后台任务有人负责 |
| PR 描述模板 | Summary / Verification / Risk 稳定 |
| 双工具分工规则 | Codex 与 Claude Code 不抢同一批文件 |

这才是一套工具真正落地的样子：不是人人会喊"帮我优化"，而是团队有共同的上下文、边界、工具、审查和复盘方式。

## 11. 课程内容地图：从功能到能力

把本系列 14 篇看成四层能力：

| 层级 | 课程 | 你获得的能力 |
|---|---|---|
| 基础环境 | CX-01、CX-02 | 安装、线程、任务描述、Review 主线 |
| 工作流控制 | CX-03、CX-04、CX-10、CX-12 | Commands、权限、配置、PR、CLI 排障 |
| 能力扩展 | CX-05、CX-06、CX-07、CX-08、CX-09 | MCP、Skills、Plugins、Subagents、Automations |
| 团队治理 | CX-11、CX-13、CX-14 | Cloud handoff、安全企业、工具选型和共存 |

学习顺序也可以按角色调整：

| 角色 | 先学 |
|---|---|
| 普通开发者 | CX-01、CX-02、CX-03、CX-10 |
| Tech Lead | CX-02、CX-04、CX-06、CX-10、CX-13 |
| 平台 / DevEx | CX-04、CX-05、CX-07、CX-09、CX-12、CX-13 |
| 安全 / 合规 | CX-04、CX-05、CX-09、CX-11、CX-13 |
| 从 Claude Code 迁移者 | CX-02、CX-04、CX-06、CX-12、CX-14 |

## 常见问题

### Q1：只学 Codex App 可以吗？

可以。本系列就是 Codex App 主线。CLI、Web、Claude Code 都是辅助对照。

### Q2：两个工具能一起用吗？

能，但不要让它们同时改同一工作区。用分支、worktree 或明确文件范围隔离。

### Q3：团队怎么落地？

先选一个主力工具。另一个作为补充，不要一开始双主线培训。

### Q4：Codex 课程要不要照 Claude Code 的章节写？

可以借鉴厚度结构，不能照搬功能结构。Claude Code 的命令、hooks、skills 和 Codex 的 App commands、Rules、Hooks、Skills 有相似问题域，但官方机制不同。课程应该学它的“讲概念、讲机制、讲排障、讲企业落地”，而不是复制命令文件体系。

### Q5：两个工具的配置文件要不要内容完全一样？

项目事实、安全边界、测试命令应该一致；工具专属配置不要互相复制。`AGENTS.md` 服务 Codex，`CLAUDE.md` 服务 Claude Code。

### Q6：什么时候应该从 Claude Code 迁到 Codex？

当团队更需要桌面 App、Review 面板、App Automations、连接器和 Cloud handoff，且愿意维护 `AGENTS.md` 和 Codex 配置时，可以逐步迁移。已有成熟 Claude Code hooks / commands 的团队应先做小范围试点。

### Q7：什么时候不该强推 Codex？

如果团队完全在 SSH / tmux / 终端里工作，现有 Claude Code 流程成熟，且没有桌面 App Review 和 Automations 需求，强行切换会制造培训成本。

## 系列回顾

本系列现在的主线是：

1. App 安装与登录。
2. App 桌面工作流。
3. Commands。
4. 项目指令、权限与沙盒。
5. MCP。
6. Skills。
7. Plugins / Connectors。
8. Subagents。
9. Automations。
10. Review / GitHub / PR。
11. Web / Cloud 辅助。
12. CLI 辅助。
13. 安全与企业。
14. Claude Code 对比。

---

## 12. 对比的正确姿势：不是谁更强，而是谁更适合哪种操作系统

Codex App 和 Claude Code 的差异不是简单的模型差异，也不是“一个新一个旧”。它们更像两种不同的工作操作系统。

| 维度 | Codex App | Claude Code |
|------|-----------|-------------|
| 主交互 | 桌面 App、线程、Review、Automations | CLI、IDE、Desktop、Browser、commands、hooks、subagents |
| 学习入口 | 项目 + App 工作台 | CLI 会话 + 配置文件；也可从 Desktop / IDE / Web 进入 |
| 强项 | 桌面可视化、Review 面板、App automations、Cloud handoff | CLI 深度、hooks、commands、自定义自动化、多端接力 |
| 适合人群 | 想把 AI 编程纳入桌面工作流的人 | 习惯终端和脚本化，或需要 Claude Code 多端接力的人 |
| 团队落地 | App 培训、项目说明、权限配置 | CLI 规范、hooks、commands、agent teams |
| 风险 | 误以为 App 能自动处理所有流程 | 误以为脚本化越多越好 |

所以这门 Codex 课不能照抄 Claude Code 的目录。它应该学习 Claude Code 课程的厚度和教学逻辑，但内容要围绕 Codex 自己的 App、Review、Cloud、Automations、Plugins、Skills 和权限模型。

## 13. Claude Code 内容厚在哪里

Claude Code 课程厚，不只是因为字多。它厚在几个方面：

```text
1. 每个功能都有学习路径。
2. 每个概念都有术语解释。
3. 每个入口都有快速上手。
4. 每个系统都有工作原理。
5. 每个高风险功能都有安全提醒。
6. 每个功能都有案例、命令、模板和 FAQ。
7. 企业场景有单独章节。
8. 排障按症状拆，而不是简单一句“重启试试”。
```

Codex 课程要对齐的是这种“教学密度”，不是把 Claude Code 的命令照搬。

### 13.1 Codex 课程应该补的厚度

| Claude Code 厚度来源 | Codex 对应补法 |
|----------------------|----------------|
| 安装路径多 | Windows/macOS/App/CLI/工具链排障 |
| Commands 体系 | App commands、CLI slash、Skills、Automations 边界 |
| Hooks 深讲 | Codex Rules、Hooks、permissions 分层 |
| MCP 深讲 | Codex MCP config、tool approval、plugin-provided MCP |
| Skills 深讲 | `.agents/skills`、progressive disclosure、openai.yaml |
| Plugins 生态 | App Plugins、marketplace、sharing、governance |
| Subagents | 显式触发、文件所有权、main thread merge |
| Enterprise | 受管配置、MCP allowlist、Automation 分级 |

## 14. 功能映射表：迁移时不要硬搬

| Claude Code 习惯 | Codex 里的对应思路 |
|------------------|-------------------|
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/commands` | App/CLI commands + Skills，不是等价目录照搬 |
| Hooks 自动化 | Codex Hooks + Rules + Automations 分工 |
| Claude subagents | Codex 显式 subagent workflows |
| Terminal-first review | App Review pane + `/review` |
| CLI scheduled tasks | Codex App Automations |
| Remote control | Codex remote-control / app-server 高级辅助 |
| MCP 配置 | Codex `config.toml` MCP servers |
| Plugin loading | Codex App Plugins + marketplace |

迁移时最重要的一句话：**保留工作意图，重写实现入口。**

## 15. 从 Claude Code 迁到 Codex 的 5 步

### 第 1 步：盘点 Claude Code 资产

```text
- CLAUDE.md
- commands
- hooks
- skills
- MCP config
- subagent templates
- CI scripts
- team docs
```

### 第 2 步：按用途分类

| 资产 | 迁移方向 |
|------|----------|
| 项目说明 | `AGENTS.md` |
| 可复用流程 | Codex Skill |
| 命令入口 | App command / prompt template / Skill |
| 命令拦截 | Rules |
| 事件脚本 | Hooks |
| 外部工具 | MCP 或 Plugin |
| 周期任务 | Automations |
| 并行角色 | Subagents / `.codex/agents` |

### 第 3 步：先迁低风险流程

```text
1. 文档审查。
2. PR 摘要。
3. README 更新。
4. 只读 MCP 文档查询。
5. Review prompt。
```

不要第一天就迁移发布、生产配置、密钥轮换或自动推送流程。

### 第 4 步：在 App 中重建工作流

```text
打开项目
  ↓
写 AGENTS.md
  ↓
验证 Review 面板
  ↓
迁移一个 Skill
  ↓
接一个只读 MCP
  ↓
做一个只读 Automation
  ↓
再考虑 Plugin 和 Cloud
```

### 第 5 步：逐步替换，而不是一次切断

```text
Claude Code 保留终端重自动化流程。
Codex App 承担可视化 Review、桌面多线程、Cloud handoff 和 Automations。
等 Codex 流程稳定后，再决定是否迁移更多。
```

## 16. 双工具共存的工程纪律

如果团队同时用 Codex 和 Claude Code，最大风险不是工具冲突，而是文件状态和规则冲突。

### 16.1 配置文件分工

| 文件 | 服务谁 | 内容 |
|------|--------|------|
| `AGENTS.md` | Codex | 项目指令 |
| `CLAUDE.md` | Claude Code | Claude Code 指令 |
| `.codex/config.toml` | Codex | MCP、permissions、features |
| `.mcp.json` 或 Claude 配置 | Claude Code | Claude 侧 MCP |
| `.agents/skills` | Codex | Codex Skills |
| `.claude/skills` | Claude Code | Claude Skills |

不要为了省事把一个工具专属字段复制到另一个工具里。

### 16.2 工作区纪律

```text
- 同一时间同一文件最好只让一个工具写。
- 大任务用分支或 worktree 隔离。
- 提交前统一看 Git diff。
- 不要让两个工具同时跑自动写入。
- PR 描述里说明主要由哪个工具辅助。
```

### 16.3 共存 prompt

```text
这个仓库同时使用 Codex 和 Claude Code。
请只修改 Codex 相关文件：
- AGENTS.md
- .codex/**
- docs/codex/**

不要修改 CLAUDE.md、.claude/** 或 Claude Code 课程文件。
如果发现两边规则冲突，先报告，不要自动合并。
```

## 17. 选型决策：按工作流，不按情绪

### 17.1 个人开发者

优先 Codex App，如果：

```text
- 你喜欢桌面工作台。
- 你需要 Review 面板。
- 你想用 Automations 做提醒和周期检查。
- 你经常在本地项目、Web/Cloud 之间切换。
```

优先 Claude Code，如果：

```text
- 你长期在终端里工作。
- 你有成熟 hooks 和 commands。
- 你需要很强的 CLI 自动化。
- 你不需要桌面 Review 体验。
```

### 17.2 创业团队

推荐组合：

```text
Codex App:
- 新人上手
- PR Review
- 文档和产品协作
- Cloud 修明确任务

Claude Code:
- 终端强自动化
- hooks 深度流程
- 已有 agent team 流程
```

### 17.3 企业团队

选型要看治理：

```text
- 是否有桌面 App 管理策略？
- 是否能统一 AGENTS.md？
- 是否需要受管配置？
- 是否已有 Claude Code hooks 资产？
- 是否能管理 MCP 和 Plugin 风险？
- 是否需要 Cloud 环境和 PR 回流？
```

企业不应该为了“更潮”切工具。要看已有流程和新收益。

## 18. Codex 的独特课程主线

这套 Codex 课程应该形成自己的主线：

```text
App 安装
  ↓
桌面线程和 Review
  ↓
Commands 作为入口
  ↓
AGENTS.md、permissions、Rules、Hooks
  ↓
MCP 接外部上下文
  ↓
Skills 沉淀流程
  ↓
Plugins 分发能力
  ↓
Subagents 并行
  ↓
Automations 后台
  ↓
Review + GitHub + PR
  ↓
Cloud handoff
  ↓
CLI 辅助
  ↓
企业治理
  ↓
与 Claude Code 共存和迁移
```

这个顺序不是功能罗列，而是学习者能力升级路径。

## 19. 30 / 60 / 90 天落地计划

### 30 天：让团队安全用起来

```text
- 安装 Codex App。
- 每人完成只读项目分析和 README 小改。
- 每个试点仓库写 AGENTS.md。
- 训练 Review 面板和 inline comments。
- 禁止默认 full access。
```

### 60 天：让团队形成复用流程

```text
- 引入 2-3 个 repo skills。
- 配置只读 MCP。
- 建立 PR review prompt。
- 试点 Automations，只读或 worktree。
- 建立 Plugin/MCP 登记表。
```

### 90 天：让团队形成治理能力

```text
- 受管配置或团队 baseline。
- Codex + Claude Code 共存规则。
- Cloud 环境模板。
- Subagent 分工模板。
- 月度复盘和事故响应流程。
```

## 20. 按任务入口选择阅读路径

| 当前任务 | 最小路径 | 进阶路径 |
|------|----------|----------|
| 第一次把 Codex 跑起来 | CX-01、CX-02、CX-10 | CX-04、CX-06 |
| 处理一个真实 PR | CX-02、CX-10、CX-14 | CX-05、CX-08、CX-12 |
| 拆复杂任务给多个 agent | CX-02、CX-08、CX-10 | CX-04、CX-13 |
| 把会议、评论或需求变成可执行改动 | CX-02、CX-10、CX-14 | CX-09 |
| 沉淀团队可复用流程 | CX-06、CX-09、CX-14 | CX-05、CX-07 |
| 接外部工具但控制风险 | CX-04、CX-05、CX-13 | CX-07、CX-09、CX-11 |
| 做团队推广和企业基线 | CX-01、CX-04、CX-13 | CX-07、CX-11 |

这样学习者不用 14 篇从头硬啃，也能按自己当前要解决的问题找到入口。

## 21. 同一个任务如何选择工具

任务：修复一个 PR 里 reviewer 提到的认证错误。

### 用 Codex App

```text
1. 打开 PR 分支。
2. 读取 PR context。
3. 用 Review 面板看 diff。
4. 让 Codex 分类评论。
5. 只处理第一条认证 bug。
6. 看 last turn changes。
7. 人工 stage、commit、push。
```

### 用 Claude Code

```text
1. 在终端进入项目。
2. 读取 PR 评论或 issue。
3. 用 commands / hooks / tests 推进。
4. 通过 CLI 查看 diff。
5. 手动提交。
```

### 选择判断

```text
如果你重视 PR context、Review 面板和 inline comments，Codex App 更顺。
如果你已有终端命令和 hooks 自动化，Claude Code 更顺。
```

## 22. 怎么使用这套 Codex 课程

不要把 14 篇当成必须顺序读完的书。更实用的方式是先按当前任务查对应章节，再把高频流程沉淀成团队自己的 prompt、Skill、Automation 或配置基线。

如果你今天只是想把 Codex 用起来，读法是：

```text
1. CX-01 完成安装、登录和项目打开。
2. CX-02 学会 App 主界面、权限和 Review 入口。
3. CX-10 跑完一次从 diff 到 PR 的闭环。
```

如果你已经在团队里推广，读法是：

```text
1. CX-04 写清项目指令和权限边界。
2. CX-05 决定哪些外部工具可以接入。
3. CX-06 把重复流程做成 Skill。
4. CX-07 把可共享能力做成 Plugin。
5. CX-13 写成团队使用基线。
```

如果你正在从 Claude Code 迁移，读法是：

```text
1. 先用本章判断哪些流程继续留在 Claude Code。
2. 把需要 App Review、PR context、Automations、Cloud 的流程迁到 Codex。
3. 不要把 Claude Code hooks/commands 的习惯原样搬过来。
4. 用 Codex 自己的 App-first 逻辑重新设计任务入口。
```

这样用课，读者不是"看完很多文章"，而是能在安装、改代码、审 PR、接工具、做治理时马上找到可复制的流程。

## 23. 最终建议：把 Codex 作为 App-first AI 编程课来设计

Codex 的课程定位应该是：

```text
以 App 为主控台，
以 Review 为安全闭环，
以 AGENTS.md 和 permissions 建立边界，
以 MCP / Skills / Plugins 扩展能力，
以 Automations / Cloud / CLI 做辅助，
以企业治理保证可持续。
```

这样它不是 Claude Code 课程的缩小版，而是一套围绕 Codex 自己优势建立的完整课程。

## 24. 综合工坊：把一个 Claude Code 流程迁移到 Codex

### 24.1 原流程

Claude Code 里有：

```text
- CLAUDE.md：项目命令和安全规则
- /review-command：PR 审查命令
- Hook：拦截 git push
- Skill：发布说明生成
- MCP：GitHub 和文档
```

### 24.2 迁移分析

| 原资产 | Codex 目标 |
|--------|------------|
| `CLAUDE.md` 项目事实 | `AGENTS.md` |
| PR 审查命令 | Skill + `/review` prompt |
| git push hook | Rules prompt 或 Hook |
| 发布说明 Skill | `.agents/skills/release-notes` |
| GitHub MCP | Codex MCP 或 GitHub connector |
| 文档 MCP | Codex MCP config |

### 24.3 迁移 prompt

```text
请帮我把这个 Claude Code 工作流迁移成 Codex App 工作流。
要求：
- 不照搬 Claude Code 专属目录
- 保留原工作意图
- 映射到 AGENTS.md、Skills、Rules、MCP、Plugins、Automations
- 标出哪些暂时不迁移
```

### 24.4 迁移后试跑

```text
请用新的 Codex 工作流处理一个低风险 PR。
先只读分类评论。
再运行 Codex review。
最后建议是否需要修改。
不要提交，不要推送。
```

## 25. 双工具团队会议模板

```md
# Codex / Claude Code Workflow Decision

## Task Type

What are we trying to improve?

## Current Claude Code Flow

- Commands:
- Hooks:
- Skills:
- MCP:

## Proposed Codex Flow

- App:
- AGENTS.md:
- Review:
- Skills:
- MCP:
- Automations:
- Cloud:

## Keep in Claude Code

- ...

## Move to Codex

- ...

## Trial Project

- ...
```

## 26. 对比进阶常见问题

### Q1：Codex 课程要不要和 Claude Code 一样长？

不必机械一样长，但要在学习密度上有得比：机制、案例、排障、团队落地和真实模板都要够。

### Q2：Claude Code 的 hooks 更强，是不是 Codex 就不适合企业？

不是。Codex 企业路线更强调 App、permissions、Rules、Hooks、Review、MCP/Plugin governance、Cloud 和 Automations 的组合。两者治理方式不同。

### Q3：已有 Claude Code 资产要不要全部迁移？

不要。先迁低风险、高复用的流程。成熟、稳定、终端依赖强的 Claude Code 流程可以继续保留。

### Q4：团队能不能同时要求所有人用两个工具？

可以，但要有工作区纪律和配置分工。否则最容易出现两个工具同时改文件、规则互相冲突、PR 难 review。

### Q5：Codex 最应该打出的差异化是什么？

App-first。用桌面线程、Review 面板、Automations、Cloud handoff、Plugins/Skills 形成可视化、可培训、可治理的 AI 编程工作台。

## 27. 对比作业：给团队写一页选型建议

```md
# Codex vs Claude Code Recommendation

## Team Context

- Current workflow:
- Existing Claude Code assets:
- Desired Codex benefits:

## Recommended Split

Use Codex for:
- ...

Use Claude Code for:
- ...

## First 30 Days

- ...

## Risks

- ...

## Decision

- ...
```

### 示例结论

```md
Use Codex App as the default onboarding and review interface for new AI-assisted engineering workflows.
Keep Claude Code for existing terminal-heavy automation and mature hooks.
Revisit after 60 days with PR cycle time, review quality, and developer feedback.
```

## 28. 对比课程的最终落点

学完这 14 篇，学习者应该不是简单知道 Codex 有哪些功能，而是能回答：

```text
- 我该从 App 还是 CLI 开始？
- 一个任务要用 prompt、command、Skill、MCP、Plugin、Automation、Cloud 还是 Subagent？
- 我怎样看 diff，怎样让 Codex 修，怎样决定是否提交？
- 团队怎样写 AGENTS.md 和权限边界？
- 哪些 Claude Code 资产应该迁移，哪些应该保留？
- 企业怎样在效率和风险之间建立可执行规则？
```

这才是 Codex 课程真正能和 Claude Code 课程站在同一张桌上的地方：不是功能数量一样，而是学习者完成课程后能独立做判断。

## 29. 迁移长案例：把 Claude Code 的 hooks-first 流程改成 Codex 的 App-first 流程

很多团队原来在 Claude Code 里习惯这样工作：

```text
1. 进入终端。
2. 运行自定义 command。
3. hooks 在提交前检查危险命令、格式和测试。
4. 通过终端 diff 看结果。
5. 手动提交。
```

如果直接搬到 Codex，会出现两个问题：第一，Codex 的优势不在“把所有东西都塞进终端”；第二，Codex 的 App Review、PR context、Automations、Cloud 和 Plugins 如果不进入流程，课程就会变成 Claude Code 的弱化版。

迁移时不要问“这个 hook 在 Codex 里对应哪个按钮”。先问原流程解决的真实问题。

```text
原流程要解决：
- 任务开始前明确边界。
- 写代码前知道项目规则。
- 改完后看 diff。
- 提交前不漏测试。
- 高风险动作有人确认。
```

在 Codex 里可以改成：

```text
1. 用 App 线程描述任务目标、范围和禁止事项。
2. 让 `AGENTS.md` 承接项目规则。
3. 用 Rules 或权限 profile 收窄危险命令。
4. 修改完成后在 Review 面板看 last turn 和 full diff。
5. 用 `/review` 或 Review prompt 找风险。
6. 需要远端并行时再用 Cloud。
7. 稳定重复任务再沉淀成 Skill 或 Automation。
```

迁移 prompt：

```text
我有一套 Claude Code 工作流，流程如下：

1. 运行 /fix-auth command。
2. hooks 阻止危险 shell 命令。
3. hooks 在提交前跑 tests。
4. 人工看 git diff。

请帮我改写成 Codex App-first 工作流。

要求：
1. 哪些放进 AGENTS.md。
2. 哪些用 App prompt。
3. 哪些用 Review 面板。
4. 哪些适合 Rules 或权限。
5. 哪些不应该迁到 Codex。

不要假设 Codex 拥有 Claude Code 的同名 hooks 或 commands。
```

一个迁移后的流程示例：

```text
任务入口：
在 App 新线程中说明“只修 auth redirect bug，不重构 auth 模块”。

持久规则：
AGENTS.md 写清测试命令、代码风格、安全边界。

执行方式：
Codex 本地修改最小文件集；如果要改新文件，先说明原因。

审查方式：
Review 面板看 last turn changes，再看 full diff。

风险补充：
用 `/review` 检查认证、授权、redirect 和敏感日志。

收口：
人工 stage、commit、push；PR 描述写 Summary、Verification、Risk。
```

这才是迁移，不是翻译。翻译会问“Claude Code 的 A 在 Codex 里叫什么”；迁移会问“这个流程要保护什么结果，Codex 哪个能力最适合承担”。

## 30. 双工具冲突处理：当两个工具都改了同一个项目

双工具共存最常见的事故不是模型犯错，而是人没有管理工作区。Claude Code 在终端里改一批文件，Codex App 也在本地线程里改同一批文件，最后 Review 面板看到一团混合 diff。

先建立三条纪律：

```text
1. 同一时间只让一个工具拥有某一组文件的写权限。
2. 另一个工具如果参与，只做只读 review 或分析。
3. 每次切换工具前先看 Git 状态。
```

如果冲突已经发生，先不要让任何一个工具继续修。用 Codex App 做只读整理：

```text
请只读分析当前 Git diff。

背景：
- 一部分改动来自 Claude Code。
- 一部分改动来自 Codex App。
- 我需要先分清哪些改动属于哪个任务。

输出：
1. 按文件列出可能属于任务 A 的改动。
2. 按文件列出可能属于任务 B 的改动。
3. 无法判断来源的改动。
4. 哪些文件不应该继续同时编辑。
5. 建议的收口顺序。

不要修改文件，不要执行 git 操作。
```

如果项目很大，可以把任务拆开：

```text
任务 A：auth redirect bug。
任务 B：toast 样式整理。

请判断当前 diff 中哪些文件更像任务 A，哪些更像任务 B。
如果某个文件同时包含两类改动，请标记为需要人工逐行处理。
```

然后选择一个工具收口一个任务。比如 auth bug 交给 Codex App：

```text
现在只处理任务 A：auth redirect bug。

请基于当前 diff 设计收口步骤：
1. 哪些文件保留在任务 A。
2. 哪些文件应该从任务 A 排除。
3. 哪些测试先跑。
4. PR 描述怎么写。

不要执行 git 操作。
```

双工具共存的原则很朴素：工具可以多，写入责任不能乱。Codex 课程要把这件事讲透，否则读者学会了两个强工具，却没有学会管理一个清楚的 diff。

## 31. 选型案例：同一个需求，为什么答案会变

需求：把一个“导出报表失败”的问题修掉。

如果背景是“本地能复现，失败在 UI 操作后出现”，优先 Codex App：

```text
原因：
- 需要本地项目和 Review 面板。
- 可能要看 UI 相关文件、测试和 diff。
- 修完后要人工检查用户路径。
```

App prompt：

```text
我本地能复现导出报表失败。
请先只读分析 export/report 相关代码和测试。
输出最可能的原因和最小修复计划。
不要修改文件。
```

如果背景是“CI 里报表导出测试失败，本地暂时不方便跑”，可以先用 CLI 或 Cloud：

```text
原因：
- 失败材料主要是日志。
- 任务可复现且边界清楚。
- 可以先让 Codex 远端或无头分析，再回本地 Review。
```

CLI prompt：

```bash
cat ci-log.txt |
  codex exec --sandbox read-only "
  Summarize the report export failure.
  Identify failing tests, likely files, and smallest next action.
  "
```

如果背景是“团队每周都要检查报表文档和代码是否一致”，用 Automation + Skill：

```text
原因：
- 重复发生。
- 输出是报告或提醒。
- 可以让后台定期检查，但不应该自动发布。
```

Automation prompt：

```text
每周一检查报表导出相关文档是否和代码入口一致。
只读执行。
输出：必须修、可以排期、暂不处理。
不要修改文件。
```

同一个需求在不同背景下，工具选择完全不同。课程真正要训练的是“读场景”的能力：本地交互、日志分析、远端执行、周期性巡检，这四类任务不要混成一种万能 prompt。

## 32. 从 Claude Code 课程学写 Codex 课：学厚度，不学外壳

Claude Code 课程厚，不只是因为字数多。它通常会把一个能力讲成完整链条：为什么需要、怎么用、哪里会错、错了怎么恢复、团队怎么复用。Codex 课要学的是这种链条，不是把 Claude Code 的命令名换成 Codex。

Codex 章节也应该围绕自己的链条展开：

```text
App：
任务描述 -> 本地执行 -> Review 面板 -> PR context -> 人工提交。

Commands：
入口选择 -> plan/review/goal -> 能力发现 -> 错误恢复。

MCP：
工具边界 -> 只读试点 -> 授权 -> 排障 -> 团队 allowlist。

Skills：
重复 prompt -> SKILL.md -> references/scripts/assets -> reload -> plugin 分发。

Plugins：
个人安装 -> 小团队试点 -> workspace sharing -> 禁用/移除 -> 治理。

Automations：
稳定任务 -> prompt 设计 -> run 观察 -> 降噪 -> 停用。

Cloud：
handoff -> setup -> agent 执行 -> diff 回收 -> 本地 Review。
```

读者读完一个章节，应该能回答三件事：

```text
1. 今天我能用这个功能完成什么真实任务？
2. 出错时我按什么顺序排查？
3. 这个流程稳定后，团队如何复用？
```

只要这三件事讲清楚，Codex 课就不会像功能说明书；它会像一套能落地的工作法。

## 33. 课程迁移练习：把一个 Claude Code 章节改写成 Codex 章节

假设 Claude Code 课程里有一章讲“用 command 修复 PR 评论”。不要直接把标题改成“用 Codex command 修复 PR 评论”。Codex 的改写应该围绕 App 和 Review。

原章节骨架：

```text
1. 读取 PR 评论。
2. 运行自定义 command。
3. hooks 检查风险。
4. 终端查看 diff。
5. 提交。
```

Codex 章节骨架：

```text
1. 在 App 中读取或整理 PR context。
2. 把评论分类为阻塞、可顺手修、需要澄清、应拆出。
3. 只处理一条阻塞评论。
4. 用 Review 面板检查 last turn diff。
5. 用 `/review` 做只读风险审查。
6. 人工 stage、commit、push。
7. 更新 PR 描述和回复材料。
```

改写 prompt：

```text
请把下面这个 Claude Code 课程流程改写成 Codex App-first 课程。

要求：
1. 不假设 Codex 有 Claude Code 同名 command。
2. 把终端 diff 改成 App Review 面板。
3. 把 hooks 风险检查改成 AGENTS.md、Rules、Review prompt 或人工检查。
4. 加入 PR context 和 inline comments 的使用场景。
5. 输出一段读者可以直接练习的任务。
```

改写后的练习：

```text
练习：PR reviewer 指出 auth redirect 测试失败。

步骤：
1. 在 App 中打开 PR 分支。
2. 让 Codex 分类 reviewer 评论。
3. 只修 auth redirect 测试失败。
4. 在 Review 面板检查 diff。
5. 用 `/review` 检查认证和测试风险。
6. 写 PR 更新说明。
```

这个练习能训练课程作者一个判断：同样是“修 PR 评论”，Claude Code 的强主舞台仍是 CLI / hooks / commands，也可以接 IDE、Desktop 和 Web；Codex 的主舞台是 App、Review 和 PR context。课程改写必须换主舞台，否则内容会天然显得弱。

## 34. 双工具团队的边界文档

如果团队同时使用 Codex 和 Claude Code，最好写一页边界文档。它不需要复杂，但要避免同一个任务被两个工具同时推进。

```md
# AI Coding Tools Boundary

## Default

Use Codex App for:
- onboarding
- local diff review
- PR context
- App Review workflows
- automations and cloud handoff

Use Claude Code for:
- existing terminal-heavy workflows
- mature hook-based automation
- workflows already encoded as Claude commands

## Do Not

- Let both tools edit the same files at the same time.
- Copy CLAUDE.md rules into AGENTS.md without adapting them.
- Assume hooks, commands, skills, and plugins have identical behavior.
- Skip Review because another tool already checked the diff.

## Handoff

When moving a task from one tool to another, include:
- original goal
- files already changed
- tests already run
- remaining risk
- what the next tool must not touch
```

一个 handoff 示例：

```text
Moving from Claude Code to Codex App.

Goal:
Fix auth redirect regression.

Already changed:
- src/auth/redirect.ts
- tests/auth-redirect.test.ts

Already run:
- targeted auth redirect test failed once, then passed after fix.

Need Codex App for:
- Review panel diff check.
- PR description.
- Scope creep review.

Do not touch:
- toast styles
- payment
- dependencies
```

这份边界文档能让双工具共存从“看心情选择”变成“按任务选择”。它也让新人知道：两个工具都强，但强在不同工作流，不应该混成一个大杂烩。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解Codex App和Claude Code的定位差异
- [ ] 能根据团队工作方式选择主力工具
- [ ] 知道双工具共存时如何隔离（分支/worktree/文件范围）
- [ ] AGENTS.md和CLAUDE.md分别维护，不互相假设
- [ ] MCP配置分别验证，不复制粘贴
- [ ] 不用模型名、价格、跑分做硬结论

**全部勾选后即完成 Codex 全系列学习。**

---

## 附录

### A. 双工具分工速查

| 任务 | Codex App | Claude Code |
|------|-----------|-------------|
| 桌面多线程开发 | 主力 | 辅助 |
| 本地Review | 主力 | 辅助 |
| 终端自动化 | 辅助 | 主力 |
| Hooks深度定制 | 辅助 | 主力 |
| App Automations | 主力 | 另建计划任务 |
| 复杂Agent Teams | 视当前App能力 | 主力 |

### B. 推荐学习资源

- **Codex 官方文档**：https://developers.openai.com/codex
- **Claude Code 官方文档**：https://docs.anthropic.com/en/docs/claude-code
- **本系列第一篇**：[CX-01 Codex App 安装与认证](./CX-01-Codex-App安装与认证完整指南.md)
- **本系列上一篇**：[CX-13 安全与企业](./CX-13-Codex安全企业完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

回到 [Codex App 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)，从 App 实战任务开始练。
