# CX-03 Commands 完整指南：App 里的 slash commands 与工作流入口

本篇以 Codex App 的 slash commands 为主线。CLI slash commands 只作为核对和排查补充。

主要来源：OpenAI Codex App Commands、Codex CLI Slash Commands、Codex Follow Goals 与 Plugins 官方文档。本篇按 2026-06-18 可查官方文档与 Codex App 26.609 修订；CLI slash commands 只作为辅助核对，命令会随 App 版本、实验开关、插件和权限变化，最终以你当前 App 输入 `/` 后看到的列表为准。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时
> - **难度等级**：⭐⭐ 入门级
> - **更新日期**：2026年6月18日
> - **信息来源**：OpenAI Codex App Commands、CLI Slash Commands、Follow Goals 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md) 和 [CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

> **2026-06-18 App 口径**：App composer 新增 `/init`，适合在新仓库里快速建立项目指令和初始化上下文；Migrate to Codex 用来把 Claude Code / Claude Cowork 既有设置迁移到 Codex 工作流。课程里不要把迁移讲成“照搬文件”，要讲成“把项目事实、权限边界和验证命令迁移成 Codex 能读懂的形态”。

1. **理解Commands的本质**：掌握slash命令是App的快速工作流入口，不是高级玩具
2. **学会发现命令**：在App中输入`/`查看当前可用命令，不依赖死记硬背
3. **掌握核心稳定命令**：熟练使用`/status`、`/plan`、`/review`、`/mcp`、`/feedback`
4. **理解计划模式**：知道什么时候该先规划再执行，用`/plan`进入
5. **区分命令层级**：分清App命令、CLI命令、版本相关命令、Skills各自的位置
6. **理解命令边界**：知道 App 稳定命令、CLI 命令、实验能力和 Skill 入口各自怎么核对
7. **理解命令的变化性**：知道命令会随版本、插件、权限变化，以当前App显示为准
8. **避免常见命令陷阱**：不把CLI命令当App主线，不把版本相关命令写成确定功能

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想快速知道App里有哪些命令可以用

**只看这些章节**：

```
✅ 第2部分：先学会在App里发现命令（3分钟）
✅ 第3部分：App用户优先掌握的稳定命令（5分钟）
✅ 第4部分：/plan 先规划（7分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握所有Commands用法

**学习顺序**：从头到尾所有章节

---

### 路径C：问题排查（⏱️ 5分钟）

**适合人群**：某个命令用不了或效果不对

**直接跳到**：

```
🔧 最后的常见问题FAQ部分
```

---

## 术语表（小白必读）

Commands 这一章要先分清“入口”和“能力”。很多人学 slash commands 会犯一个错误：以为命令越多，能力越强。实际上，命令只是把某类工作流快速切出来，真正的能力仍然来自 App 当前线程、权限、工具、项目上下文和你的任务描述。

| 术语 | 一句话解释 | 在 Codex App 里怎么理解 |
|---|---|---|
| Slash command | 在输入框用 `/` 调出的工作流入口 | 快速切换状态、计划、审查、工具面板 |
| Composer | 你输入任务的地方 | `/`、`$skill`、自然语言都从这里进入 |
| Plan mode | 先规划、暂不执行的模式 | 大任务先降低风险 |
| Goal mode | 持续推进到完成、暂停或需要更多输入 | 适合长目标，但必须有停止条件 |
| Review mode | 让 Codex 审查当前 diff 或分支差异 | 不是人工 Review 的替代品 |
| MCP status | 查看外部工具 server 是否连接 | 工具可见不等于可以随便用 |
| Skill invocation | 用 `$skill-name` 或自然语言触发 Skill | Skill 是流程，不是普通 slash command |
| CLI slash command | 终端 TUI 里的 `/` 命令 | 可辅助理解，不等于 App 一定有同名命令 |

一句话：Command 是“入口”，Skill 是“方法”，MCP 是“工具”，Automation 是“时间触发”，Review 是“收口”。学清边界，比背完整命令表更重要。

## 0. Commands 的心智模型：入口、状态、动作

老金我讲 Commands 时不会把命令背诵当目标，真正要学的是什么时候该规划、什么时候该审查、什么时候该看状态。

Codex App 里的 slash commands 可以分成三层：

```text
入口层：/status、/mcp、/feedback
  -> 帮你打开状态、工具、反馈等面板或信息

状态层：/plan、/goal
  -> 改变 Codex 接下来怎么推进任务

审查层：/review
  -> 围绕当前 Git diff 或分支差异做检查
```

这三层的使用顺序通常是：

1. **先看状态**：用 `/status` 或当前 App 界面确认线程、权限、上下文。
2. **再定推进方式**：任务复杂就 `/plan`，长期目标才 `/goal`。
3. **执行后收口**：用 `/review` 和 Review 面板检查结果。
4. **工具问题单独查**：外部工具不可见时用 `/mcp`，插件和连接器去对应入口。

不要把 command 当成魔法咒语。它只是让你更快进入一种工作模式。模式不对，命令反而会制造混乱。例如，模糊目标直接 `/goal`，会让 Codex 长时间围绕一个不清楚的目标打转；没有 diff 时 `/review`，只会得到“当前没有可审查内容”的结果。

### 0.1 用不用 Command 的判断树

| 你现在想做什么 | 首选方式 | 为什么 |
|---|---|---|
| 看当前线程状态 | `/status` | 快速确认上下文、限制和配额信息 |
| 让 Codex 先别动手 | `/plan` | 把执行前移到方案讨论 |
| 长时间推进一个清楚目标 | `/goal` | 让目标跨多个 turn 持续存在 |
| 检查当前改动 | `/review` | 直接进入代码审查口径 |
| 查 MCP 是否连接 | `/mcp` | 看工具 server 和状态 |
| 触发团队 SOP | `$skill-name` 或自然语言 | Skill 比 command 更适合复用流程 |
| 定期重复检查 | Automation | Command 是手动入口，不负责调度 |
| 当前 App 没这个命令 | 自然语言 + 官方文档核对 | 不要硬套 CLI 命令 |

### 0.2 命令变化为什么正常

命令列表会随这些因素变化：

- App 版本。
- 账号或组织权限。
- 实验开关，例如 `features.goals`。
- 已安装插件和 Skills。
- 当前线程类型、项目状态和连接器。
- CLI / App / IDE extension 的不同界面。

所以教程要教你"怎么发现和核对命令"，免去背表的负担。Claude Code 的 Commands 章节之所以厚，是因为它讲命令系统、作用域、开发方式、故障排查和 FAQ；Codex 这里也要用同样的思路：先理解命令背后的工作流。

## 1. Commands 在 App 里解决什么问题


Commands 不是"高级玩具"，而是 App 的快速入口：

| 你想做什么 | 直接说也可以 | Command 更适合 |
|---|---|---|
| 查看当前状态 | “现在是什么模型和权限？” | `/status` |
| 进入计划模式 | “先给计划别执行” | `/plan` |
| 长目标持续推进 | “一直做直到验证通过” | `/goal`；如果当前 App 没显示，按官方方式启用或改用分阶段提示 |
| 审查改动 | “review 当前 diff” | `/review` |
| 管理外部工具 | “看看 MCP” | `/mcp` |
| 反馈问题 | “这个 App 行为不符合预期” | `/feedback` |

学习方式：在 App 输入框输入 `/`，看当前版本展示什么。不要背死命令表，也不要把别人机器上出现的命令直接当成你这台机器一定有。

## 2. 先学会在 App 里发现命令


每次换版本、换账号、换项目或安装插件后，先做这四步：

1. 打开 Codex App 的任意项目线程。
2. 在输入框输入 `/`。
3. 看弹出的命令列表、命令说明和是否有实验标记。
4. 如果不确定某个命令能做什么，先输入 `/help` 或用自然语言问“解释当前可用 slash commands，不要执行任何改动”。

判断一个命令能不能写进教程，按这个顺序：

| 来源 | 教程写法 |
|---|---|
| 官方 App Commands 明确列出 | 可以作为稳定入口写 |
| 当前 App 弹窗显示但官方页未列出 | 写成“当前版本可能出现，以你的 App 为准” |
| 只在 CLI 出现 | 放到 CX-12，不能写成 App 主线 |
| 只听别人说过 | 不写成确定命令 |

## 3. App 用户优先掌握的稳定命令


| 命令 | App 主线用途 | 使用建议 |
|---|---|---|
| `/feedback` | 发送产品反馈 | 反馈 App 或命令问题 |
| `/status` | 查看模型、工作区、审批、上下文状态 | 任务前后都可用 |
| `/plan` | 切换计划模式 | 大任务先规划，不急着改 |
| `/review` | 审查当前改动 | 合并前使用 |
| `/mcp` | 查看 MCP 工具 | 接外部工具后检查 |
| `/goal` | 设置持续目标 | 长任务要写清范围和停止条件 |
| `/help` 或 `/` 列表 | 查看当前可用命令 | 以当前 App 显示为准 |

官方 App Commands 页面当前明确列出的命令很少，所以本篇不再把 CLI 的完整 slash command 表硬搬成 App 表。

### 3.1 三个 App 命令工作流配方

**配方一：大任务先计划**

```text
/plan

目标：把登录逻辑从旧 auth helper 迁到新 auth client。
范围：先只读 src/auth、tests/auth 和相关 README。
约束：先不要修改文件，不要安装依赖。
交付：列出方案、风险、要改的文件和验证命令。
```

你应该看到：Codex 只输出计划，不直接写文件；计划里能说明为什么读这些文件。

**配方二：改完立刻审查**

```text
/review 重点检查：是否改了范围外文件、是否缺少测试、是否引入权限或网络行为变化。
```

你应该看到：Review 结论能对应当前 diff，不是泛泛而谈。

**配方三：命令不确定时先问状态**

```text
/status
```

然后再问：

```text
解释当前线程的模型、工作区、权限/审批状态和可用工具。不要修改文件。
```

你应该看到：你能判断当前任务适合只读、可写、worktree 还是 Cloud。

## 4. `/plan`：先规划，不急着写

适合：

- 多文件改动。
- 架构调整。
- 不确定影响面的 bug。
- 需要先比较方案。

示例：

```text
/plan

修复登录页移动端布局问题。先读相关文件，列出可能方案、风险和验证命令，不要改文件。
```

好的计划应该包括：

- 要读哪些文件。
- 要改哪些文件。
- 可能方案和取舍。
- 验证命令。
- 不做什么。
- 什么时候退出计划模式进入执行。

如果你的 App 里仍显示旧口径 `/plan-mode` 而不是 `/plan`，按当前 App 弹窗为准；但教程中不要把两者写成永远等价。

## 5. `/goal`：长目标入口

当前官方 App Commands 与 Prompting 文档都把 `/goal` 作为长目标入口。它适合“比一次普通提示更长、但有明确结束条件”的任务。

如果当前 App 的 slash 列表里看不到 `/goal`，先按官方说明启用：

```toml
[features]
goals = true
```

也可以在 CLI 中运行：

```bash
codex features enable goals
```

适合：

- 长迁移。
- 长重构。
- 部署重试直到成功。
- 原型持续打磨直到测试通过。

不要这样写：

```text
/goal 优化项目
```

应该这样写：

```text
/goal Complete the migration from legacy auth helpers to the new auth client. Scope: src/auth and tests/auth only. Stop when npm test -- auth passes or when a blocker requires human decision. Do not commit or push.
```

长目标必须包含：

- 任务范围。
- 允许读写的文件。
- 验证命令。
- 失败时怎么停。
- 最长运行边界。
- 是否允许提交、推送或调用外部服务。

周期性或后台重复检查优先放到 CX-09 Automations，不要把未在当前 App 显示的命令写成固定能力。

## 6. `/review`：把审查放进 App 工作流

`/review` 用来审查当前工作区改动。App 用户可以把它放在每次合并前：

```text
/review
```

你也可以自然语言补充审查重点：

```text
/review 重点看：是否改了范围外文件、是否缺测试、是否引入安全问题。
```

注意：

- `/review` 不替代人工确认。
- 高风险改动仍要读 diff。
- 安全专项可以另用安全审查提示或专门 skill。

### 6.1 `/review` 不是一句“帮我看看”

好的 `/review` 要带检查维度：

| 维度 | 适合提示 |
|---|---|
| 范围 | 是否只改了任务指定文件 |
| 正确性 | 是否有边界条件、空值、异步竞态 |
| 安全 | 是否触碰 secret、权限、网络、外部服务 |
| 测试 | 是否覆盖新增行为，是否只跑了无关测试 |
| 可维护 | 是否引入重复逻辑、过度抽象或隐式依赖 |

示例：

```text
/review 重点检查 auth migration 的边界条件、token 处理、测试覆盖，以及是否误改了非 auth 模块。
```

## 7. 权限命令与安全边界

权限入口的名称可能随 App 版本变化。你应该通过 `/` 列表或 Settings 找到当前会话的权限设置，用来理解或调整 Codex 能自动做什么。

学习阶段建议：

- 不要开无限制自动执行。
- 让 Codex 在写文件和运行危险命令前解释。
- 对陌生项目使用更保守权限。

当任务涉及删除、移动、大量写入、联网或外部服务时，先看权限。若当前 App 没有 `/permissions`，就去 Settings 或当前线程权限提示里看，不要假设命令一定存在。

## 8. `/mcp`、Apps、Plugins

这三个命令常被混淆：

| 命令 | 管什么 | 例子 |
|---|---|---|
| `/mcp` | 外部工具 server 暴露的工具 | 浏览器、数据库、内部 API |
| Apps / Connectors 入口 | 连接器 / 外部服务上下文 | GitHub、Drive、Gmail、Slack |
| Plugins 入口 | 能力包 | 携带 skills、MCP、apps、配置 |

使用顺序：

1. 先确认要解决的问题。
2. 看 App 是否已有连接器或插件。
3. 用 `/mcp`、Apps 入口或 Plugins 入口确认工具是否可见。
4. 再让 Codex 使用它。

## 9. CLI slash commands：只作为补充

在终端里运行 `codex` 也有 slash commands。CLI 表只能帮助你理解概念，不能反推 App 一定支持同名命令。终端里输入 `/help` 查看当前 CLI 支持项。

| 类型 | 例子 | App 用户怎么用 |
|---|---|---|
| 状态 / 配置 | `/status`、`/model`、`/permissions` | 理解概念，App 里按 Settings 和 `/` 列表找对应入口 |
| 工作流 | `/review`、计划模式、目标模式 | App 优先用 Review 面板和当前命令 |
| 工具 | `/mcp`、Apps、Plugins | App 优先看工具/连接器入口 |
| 会话管理 | `/compact`、`/resume`、`/new` 等 | CLI 辅助或当前 App 可见时使用，不写成 App 必备 |

如果你需要完整 CLI 命令表，去 CX-12 或直接运行 `codex` 后输入 `/help`。本篇只保留 App 主线。

## 10. Commands、Skills、Automations 的边界

| 类型 | 适合什么 | 例子 |
|---|---|---|
| Command | 当前会话里的快速动作 | `/review`、`/plan`、`/mcp` |
| Skill | 可复用流程或领域规范 | 代码审查 SOP、发布检查 |
| Automation | 定时或后台重复任务 | 每天检查测试、每周依赖摘要 |

不要把所有东西都做成 command。长期流程优先沉淀为 Skill；周期任务用 Automation。

## 10.1 App Commands 与 CLI Commands 的差异模型

App 和 CLI 都有 slash commands，但它们服务的界面不同。

| 维度 | App commands | CLI commands |
|---|---|---|
| 主要对象 | 桌面线程、Review 面板、App 工具入口 | 终端 TUI、命令行权限、模型、会话 |
| 发现方式 | App 输入框输入 `/` | CLI TUI 输入 `/help` 或 `/` |
| 适合读者 | 桌面 App 用户 | 终端用户、CI / 远程环境用户 |
| 教程写法 | 以 App 当前显示和官方 App Commands 为准 | 放到 CX-12，按本机 `--help` 核对 |
| 风险 | 把 CLI 命令误写成 App 主线 | 把 App 面板能力误以为 CLI 自动具备 |

如果你正在写课程、团队文档或 onboarding 文档，建议这样表述：

```text
在 Codex App 中，先输入 `/` 查看当前可用 commands。
如果你在 CLI TUI 中工作，输入 `/help` 查看终端可用 commands。
两者不保证完全一致；以当前界面显示为准。
```

这句话能避免很多学习者卡在“教程写了，但我的界面没有”的挫败感。

## 10.2 命令排障表

| 症状 | 可能原因 | 排查顺序 |
|---|---|---|
| 输入 `/goal` 没出现 | goals feature 未启用、版本未支持、账号/环境差异 | 先看 `/` 列表，再查 `features.goals`，最后用分阶段普通提示替代 |
| `/review` 没有发现问题 | 当前没有 Git diff，或 Review 范围不对 | 先看 Review 面板文件列表，再确认是否有 uncommitted changes |
| `/mcp` 看不到工具 | MCP 未配置、App 未刷新、server 启动失败、项目未信任 | 先看 App Settings，再用 CLI `codex mcp list` 辅助 |
| `/plan` 后仍想执行 | 任务描述里让它直接改了，或你后续批准执行 | 明确写“先只读计划，不修改文件” |
| 命令列表和教程不同 | 版本、插件、界面、实验开关不同 | 以当前 App 列表和官方文档为准 |
| CLI 有命令 App 没有 | 两个界面能力不同 | 不要强行照搬，用自然语言或 App 对应入口 |

排障的原则是：先看当前界面，再查官方文档，再用 CLI 辅助。不要把别人截图里的命令当作你的机器一定应该出现。

## 10.3 团队应该怎么教 Commands

团队培训时，不要从“命令大全”开始，而是用四个场景带着学：

1. **状态场景**：每个人输入 `/status`，说明当前线程、上下文和限制。
2. **计划场景**：给一个两文件改动，让大家用 `/plan` 只出方案。
3. **审查场景**：制造一个小 diff，用 `/review` 做定向检查。
4. **工具场景**：连接一个只读 MCP，用 `/mcp` 看工具是否可见。

这样学完，团队真正掌握的是“什么时候切换工作模式”，而不是机械背命令名。

## 11. 课堂工坊：三种命令场景连起来练

### 案例一：用 `/plan` 把模糊任务变成可执行计划

目标：让 Codex 先读证据、出计划，不直接改文件。

```text
/plan

目标：修复登录页移动端按钮文字溢出。
范围：先只读 src/pages/login.tsx、src/styles/login.css、相关测试文件。
约束：不要修改文件，不要安装依赖。
交付：列出可能方案、影响文件、验证命令和不做事项。
```

你应该看到：计划里有要读的文件、要改的文件、验证命令和风险；当前 Review 面板没有新增改动。

### 案例二：用 `/goal` 做有边界的长任务

目标：学习长目标不是"无限优化"，而是带停止条件的持续任务。

```text
/goal Fix the docs link drift in docs/codex only. Scope: markdown links inside docs/codex. Stop when every broken local link is either fixed or listed with a reason. Do not commit or push.
```

如果当前 App 看不到 `/goal`，先按官方方式启用，或改用普通提示分阶段执行。你应该看到：目标进度出现在 composer 附近；Codex 在完成、暂停或遇到阻塞时能说明状态。

### 案例三：用 `/review` 做定向审查

目标：让审查指向真实 diff，而不是泛泛评价。

```text
/review 重点检查：是否改了范围外文件、是否引入错误命令、是否缺少验证步骤、是否触碰密钥或权限配置。
```

你应该看到：Review 结果能引用具体文件或 diff 片段；如果没有改动，Codex 会说明当前没有可审查 diff。

## 常见问题

### Q1：App 和 CLI 的命令完全一样吗？

不保证。以当前 App 的 `/` 列表、命令说明和官方 App Commands 文档为准。CLI 表只能辅助理解。

### Q2：`/goal` 会不会无限跑？

有风险。所以必须写清楚停止条件、范围和验证方式。

### Q3：我应该背完整命令表吗？

不用。掌握“输入 `/` 看当前命令”、`/status`、`/plan`、`/review`、`/mcp`、`/goal`，再理解 Apps / Plugins / 权限入口，就足够开始。周期任务去 CX-09 Automations。

### Q4：为什么 Claude Code 的 Commands 能自定义很多文件，Codex 这里没有照搬？

因为两个工具的命令系统不一样。Claude Code 有自己的命令文件体系；Codex App 的 App commands 是产品内置工作流入口，Codex 的可复用流程主要用 Skills、Plugins、Automations、MCP 和项目指令来组织。不要把 Claude Code 的命令开发方式硬套到 Codex App。

### Q5：我能不能把常用提示做成一个 command？

在 Codex 里，重复提示优先做成 Skill。Command 负责进入当前界面的工作模式，Skill 负责沉淀可复用工作流。如果这个流程还要定时跑，再让 Automation 调用 Skill。

### Q6：命令能绕过权限吗？

不能这样理解。Command 只是入口，真正执行文件写入、命令、MCP 或外部服务动作时，仍受当前 Settings、sandbox、approval、rules、hooks、connector 权限影响。

---

## 12. Commands 的分类学习法

新手不要把 Commands 当成一张需要背诵的命令表。更好的学习法是按“改变什么”来分类。

| 类别 | 改变什么 | 代表场景 |
|------|----------|----------|
| 计划类 | 改变任务推进方式 | `/plan`、长任务拆解 |
| 目标类 | 改变持续执行状态 | `/goal` |
| 审查类 | 改变当前姿态 | `/review` |
| 能力类 | 查看或选择外部能力 | `/mcp`、App Plugins 页面、CLI TUI `/plugins`、Skills mention |
| 权限类 | 改变能做什么 | permissions 相关入口 |
| 会话类 | 改变上下文和线程 | resume、status、agent 相关入口 |

Commands 的本质是“告诉 Codex 现在进入哪种工作模式”。它不是魔法，也不会绕过项目规则、审批或沙盒。

### 12.1 什么时候不用 command

很多任务普通自然语言就够：

```text
请只读解释当前项目结构。
```

不需要强行写成：

```text
/plan 请只读解释当前项目结构
```

如果任务很小、风险很低、边界清楚，普通 prompt 更自然。

### 12.2 什么时候应该用 command

| 情况 | 推荐 |
|------|------|
| 任务有多个阶段 | `/plan` |
| 需要长时间推进 | `/goal` |
| 当前 diff 需要审查 | `/review` |
| 要检查 MCP 是否可见 | `/mcp` |
| 要浏览插件 | App 里打开 Plugins 页面；CLI 里运行 `codex` 后输入 `/plugins` |
| 要管理子代理线程 | agent 相关入口 |

## 13. `/plan` 深入：让 Codex 先站住脚

`/plan` 最适合模糊、较大、会改多个文件的任务。它的价值是把执行前的思考显性化。

### 13.1 差的 `/plan`

```text
/plan 做一个完整优化。
```

问题是没有对象和边界。

### 13.2 好的 `/plan`

```text
/plan
我想把 README 的安装部分改得更适合 Windows 新手。
请先只读分析 README、package.json 和 docs/setup.md。
计划里请说明：
1. 哪些内容可能过期
2. 建议改哪些文件
3. 哪些内容不要碰
4. 是否需要先运行命令
不要直接修改文件。
```

### 13.3 plan 后的确认话术

```text
按方案 A 执行。
只改 README 和 docs/setup.md。
不要改 package.json。
完成后告诉我 Review 面板里应该检查哪些 diff。
```

不要只说“可以”。要把你接受的方案和边界再说一遍。

## 14. `/goal` 深入：长任务也要有边界

`/goal` 适合目标持续、步骤较多、需要 Codex 长时间推进的任务。但长任务更需要边界。

### 14.1 适合 `/goal` 的任务

```text
/goal
把 docs/codex 目录的课程文档补厚到可以作为完整自学课程。
边界：
- 只改 docs/codex
- 不加入空白素材提示
- 不写课程外的内部评审文字
- 不虚构 Codex 功能
每完成一批请做禁词和 diff 检查。
```

### 14.2 不适合 `/goal` 的任务

```text
/goal
帮我把公司所有项目都弄好。
```

这个目标没有范围，没有结束条件，也没有权限边界。

### 14.3 长任务的中途控制

```text
先暂停扩大范围。
请汇报：
1. 已经改了哪些文件
2. 当前统计变化
3. 还差哪些部分
4. 下一批准备改什么
```

长任务不是交出去就不管。你可以随时收窄、改变优先级或要求复盘。

## 15. `/review` 深入：把 Codex 切到审查姿态

`/review` 的价值是让 Codex 按 review 方式看改动，而不是继续实现。

### 15.1 宽泛 review

```text
/review
请审查当前 diff。
```

适合快速扫一眼，但可能输出泛。

### 15.2 定向 review

```text
/review
请只看以下风险：
1. 行为回归
2. 安全或权限问题
3. 缺失测试
4. 破坏兼容性的改动

不要评论纯格式问题，除非它会造成真实维护风险。
```

### 15.3 Review 后不急着全修

```text
请把 `/review` findings 分成：
- 需要马上处理
- 可以稍后处理
- 需要我判断

先不要改文件。
```

这一步能避免 Codex 把 review 中的每个点都当成同等重要的修复任务。

## 16. `/mcp` 与 Plugins：能力发现入口

`/mcp` 是 App slash command；Plugins 在 App 里主要通过 Plugins 页面和插件深链进入，CLI 里才是运行 `codex` 后输入 `/plugins`。两者都是能力发现入口，但看的是不同层。

| 入口 | 看什么 |
|------|--------|
| `/mcp` | 当前 MCP server 是否可用、工具是否暴露 |
| App Plugins / CLI `/plugins` | 已安装和可发现的插件、marketplace 来源 |

### 16.1 MCP 排查 prompt

```text
我在 App 里想使用文档查询 MCP，但 Codex 没有调用它。
请先帮我判断：
1. MCP server 是否在当前配置中可见
2. 当前任务是否真的需要 MCP
3. prompt 是否没有明确要求查外部文档
4. 是否应该改用普通 Web search 或本地文件
```

### 16.2 Plugins 排查 prompt

```text
我安装了一个插件，但当前线程里没有按预期使用。
请帮我判断：
1. 插件是否需要新线程才能被发现
2. 是否需要外部账号授权
3. 是否应该用 @ 显式调用
4. 是否应该用普通 Skill 或 MCP 而不是插件
```

## 17. Commands 与 Skills 的组合

Command 负责“切换入口”，Skill 负责“执行工作法”。

### 17.1 组合示例：先 plan，再 skill

```text
/plan
我想用 $docs-drift 检查文档是否过期。
请先分析这个项目是否适合运行该 skill。
不要修改文件。
```

确认后：

```text
$docs-drift
只读检查 README 和 docs/。
输出可能过期的段落、证据和建议更新位置。
```

### 17.2 组合示例：先 review，再 skill

```text
/review
请审查当前文档改动是否引入事实不一致。
```

再用：

```text
$writing-humanizer-zh
请只润色刚才改动中的课程表达。
不要改变事实和命令。
```

## 18. Commands 与 Automations 的组合

Automations 里也可以用 Skill，但不应该依赖需要人工交互的 command。你要把“定期醒来要做什么”写清楚。

```text
$pr-review
每天上午 10 点检查当前项目关联 PR 的新评论。
只读读取评论。
把需要我处理的事项放进 Triage。
不要回复评论，不要推送代码。
```

如果任务需要 `/review`，更好的做法是让自动化生成报告，然后人打开线程手动运行 review。

## 19. Commands 排障：命令不存在不等于功能不存在

Codex 的不同界面和版本中，commands 的入口可能不同。不要把某个命令不存在直接理解为功能不存在。

| 症状 | 判断方式 |
|------|----------|
| App 里找不到某命令 | 看当前 App 命令列表或 command palette |
| CLI TUI 命令不同 | 在 CLI 里看帮助或 slash 列表 |
| 插件入口没出现 | 打开 App Plugins 页面；CLI 里进入 `codex` TUI 后再输入 `/plugins` |
| Skill 没被触发 | 检查 `$skill` mention 和 description |
| MCP 工具没出现 | 用 `/mcp` 或配置检查 |

### 19.1 通用排查 prompt

```text
我想使用一个 Codex command，但当前界面里找不到。
请不要猜命令一定存在。
请帮我：
1. 判断这个能力在 App、CLI、Skill、Plugin、MCP 中哪个层面
2. 给出当前界面可用的替代入口
3. 避免使用不存在的命令名称
```

## 20. 团队 Commands 教学脚本

团队培训时，可以按 4 个 15 分钟模块讲。

### 20.1 第一段：不用 command

练普通 prompt：

```text
请只读总结当前项目。
```

目标：先学会写清任务。

### 20.2 第二段：用 `/plan`

```text
/plan
请帮我规划如何更新 README 的快速开始部分。
只读分析，不改文件。
```

目标：学会执行前拆解。

### 20.3 第三段：用 `/review`

```text
/review
请审查 README 改动是否和 package.json 一致。
```

目标：学会切换到审查姿态。

### 20.4 第四段：用能力入口

```text
/mcp
```

App 里打开 Plugins 页面；如果在 CLI 里练习，则先运行：

```text
codex
/plugins
```

目标：知道外部能力在哪里看，不把所有事情都归到 slash command。

## 21. Commands 综合工坊：一个任务从 `/plan` 到 `/review`

本工坊用一个文档修复任务串起常用 command。

### 21.1 任务背景

README 里的安装命令和 package.json 不一致。你要先规划，再执行，再 review。

### 21.2 第一步：`/plan`

```text
/plan
README 的安装命令可能和 package.json 不一致。
请先只读分析 README、package.json 和 docs/setup.md。
输出：
1. 可能不一致的地方
2. 建议修改文件
3. 不应该修改的文件
4. 建议执行顺序
不要改文件。
```

### 21.3 第二步：执行计划

```text
执行计划中的最小方案。
只改 README。
不要改 docs/setup.md、package.json 或 lockfile。
```

### 21.4 第三步：`/review`

```text
/review
请审查刚才的 README 改动是否：
1. 和 package.json 一致
2. 没有扩大范围
3. 没有改变其它说明
4. 没有引入过期命令
```

### 21.5 第四步：修 review findings

```text
请只处理 review 结果里和 README 命令一致性有关的问题。
其它建议先列出，不要修改。
```

这个工坊让学习者理解：Commands 不是孤立用，而是组成任务节奏。

## 22. Command prompt 语法库

### 22.1 只读规划

```text
/plan
请先只读分析这个任务。
计划里列出：
- 目标
- 可改文件
- 不改文件
- 需要运行的命令
- 风险
不要修改文件。
```

### 22.2 小范围执行

```text
按刚才计划执行。
只改以下文件：
- docs/setup.md
- README.md

如果你认为需要改其它文件，先停下来说明原因。
```

### 22.3 长任务目标

```text
/goal
目标：把 docs/codex 中某一篇课程补成完整自学章节。
边界：
- 只改目标文件
- 不虚构功能
- 不加入课程外内容
- 每批修改后汇报新增章节和检查结果
```

### 22.4 定向 review

```text
/review
只看：
- 行为是否偏离目标
- 命令是否正确
- 是否有不必要改动
- 是否缺少必要解释

不要评价纯文风。
```

### 22.5 能力发现

```text
请帮我判断这个任务应该使用 command、Skill、MCP、Plugin、Automation 还是普通 prompt。
先给理由，不要执行。
```

## 23. Commands 与团队规范

团队里使用 commands，不能只靠个人习惯。建议统一三类模板。

### 23.1 规划模板

```text
/plan
Task:

Scope:

Do not:

Evidence to read:

Expected output:
```

### 23.2 审查模板

```text
/review
Review lens:
- correctness
- security
- tests
- scope control

Ignore:
- style-only comments
- unrelated refactor ideas
```

### 23.3 长目标模板

```text
/goal
Outcome:

Allowed files:

Not allowed:

Batch size:

Progress report:
```

把这些模板放进团队文档，而不是让每个人临场发挥。

## 24. Commands 版本意识

Codex App、CLI、IDE Extension 的命令入口会随版本变化。课程写法要避免“把当前界面当永恒事实”。

### 24.1 课程里应该怎么说

```text
- 在当前界面查看可用 commands。
- App 和 CLI 的入口可能不同。
- CLI 用 `--help` 和 TUI 内列表确认。
- 插件用 App Plugins 页面；CLI 里用 `codex` TUI 内的 `/plugins`。
- MCP 用 App settings、CLI `codex mcp` 或 TUI `/mcp`。
```

### 24.2 学生遇到命令差异时

```text
我在当前 Codex 界面找不到教程里的命令入口。
请帮我按能力寻找替代路径：
1. 这个命令想完成什么事
2. 当前 App 有没有对应按钮或 command palette
3. CLI 有没有对应子命令
4. 是否应该用 Skill、Plugin 或普通 prompt
```

## 25. Commands 进阶常见问题

### Q1：Commands 是不是越多越高级？

不是。高手往往先用普通 prompt 把任务说清楚，只有在需要切换模式、调用能力或管理状态时才用 command。

### Q2：`/plan` 之后一定要照计划执行吗？

不用。计划是为了暴露路线。你可以选择其中一部分执行，也可以要求 Codex 改计划。

### Q3：`/goal` 适合所有长任务吗？

适合目标明确、边界清楚的长任务。不适合“帮我把一切弄好”这类开放目标。

### Q4：`/review` 发现的问题都要修吗？

不一定。Review 是发现风险，不是自动排期。先分级，再决定处理哪些。

### Q5：找不到命令是不是课程错了？

不一定。可能是界面不同、版本不同、功能入口变了，或者这个能力在当前客户端不可用。按能力寻找替代路径。

## 26. 命令选择案例库：同一句需求，入口不同结果不同

### 26.1 需求：帮我改 README

普通 prompt：

```text
请只改 README 的安装命令，使它和 package.json 一致。
```

适合：范围小、风险低、目标明确。

`/plan`：

```text
/plan
README 的安装部分可能过期。
请先只读分析 README、package.json、docs/setup.md。
不要修改文件。
```

适合：不确定改哪里。

`/review`：

```text
/review
请审查 README 改动是否和 package.json 一致。
```

适合：已经有 diff，需要检查。

### 26.2 需求：处理 PR 评论

普通 prompt：

```text
请读取当前 PR 评论并分类。
不要修改文件。
```

`/review`：

```text
/review
请审查当前 diff 是否已经处理 PR 评论中的 bug 和测试问题。
```

Skill：

```text
$pr-risk-review
请按团队 PR review 流程审查当前分支。
```

Automation：

```text
每天 17:00 只读检查当前 PR 新评论，输出到 Triage。
不要回复评论。
```

同一个需求从“临时处理”到“周期跟进”，入口会变化。

### 26.3 需求：查官方文档

普通 prompt：

```text
请根据你知道的信息解释 Codex MCP。
```

风险：可能过期。

MCP：

```text
请使用官方文档 MCP 核对 Codex MCP 配置字段。
输出来源和需要改写的地方。
```

适合：事实可能变化，需要来源。

### 26.4 需求：长期补课程

`/goal`：

```text
/goal
把 docs/codex 的课程按 App-first 主线补厚。
边界：
- 只改 docs/codex
- 不虚构功能
- 保持课程内容面向学习者
- 每批修改后运行扫描
```

适合：多文件、长时间、需要阶段复盘。

## 27. Command 错误恢复

### 27.1 `/plan` 计划太大

```text
这个计划太大。
请收缩成第一批最小可执行任务：
- 最多 2 个文件
- 不改配置
- 不涉及外部系统
```

### 27.2 `/goal` 跑偏

```text
先暂停继续执行。
请只汇报：
1. 当前目标
2. 已经改了什么
3. 哪些动作可能偏离目标
4. 如何回到原边界
```

### 27.3 `/review` 输出太散

```text
请重写 review 输出。
只保留：
- confirmed bug
- security risk
- missing test
- scope creep
其它建议放到低优先级。
```

### 27.4 能力入口找不到

```text
请不要继续假设某个 command 存在。
请按能力目标寻找入口：
- App UI
- CLI subcommand
- slash command
- Skill
- Plugin
- MCP
- ordinary prompt
```

## 28. Commands 教学作业

### 作业一：改写模糊任务

原句：

```text
帮我优化项目。
```

要求：分别改写成普通 prompt、`/plan` prompt、`/review` prompt。

### 作业二：判断入口

给出 10 个任务，让学生选择入口：

```text
1. 看当前 MCP 是否可用。
2. 审查当前 diff。
3. 长期补完整课程。
4. 每周检查 docs 漂移。
5. 把 PR 评论分类。
6. 生成发布说明。
7. 打开插件目录。
8. 修一个明确 bug。
9. 设计项目 AGENTS.md。
10. 查官方最新配置字段。
```

参考方向：

```text
1 `/mcp`
2 `/review`
3 `/goal`
4 Automation + Skill
5普通 prompt 或 GitHub connector
6 Skill
7 App Plugins 或 CLI TUI `/plugins`
8普通 prompt 或 `/plan`
9 `/plan`
10 MCP 或 Web search
```

### 作业三：写团队 command 模板

```md
# Team Command Templates

## Planning

...

## Review

...

## Long Goal

...

## Capability Discovery

...
```

这个作业让团队把个人经验沉淀成共享语言。

## 29. Commands 长案例：同一个需求，入口选错会怎样

需求：

```text
帮我把结账页的错误处理做得更好。
```

这是一个典型的入口选择题。如果直接普通 prompt：

```text
帮我优化 checkout 错误处理。
```

风险是 Codex 可能立刻改代码，而且“优化”范围很大。更稳的第一步是 `/plan`：

```text
/plan
我想改善 checkout 页的错误处理。

请先只读分析：
1. checkout 页当前有哪些错误路径。
2. 哪些错误用户可见。
3. 哪些测试覆盖了错误路径。
4. 哪个最适合做成一个小 PR。

不要修改文件。
```

如果已经有 diff，入口就换成 `/review`：

```text
/review
请审查当前 checkout 错误处理改动。

重点看：
1. 是否覆盖网络失败、库存不足、支付失败。
2. 是否有未测试路径。
3. 是否引入无关 UI 改动。
4. 是否需要拆 PR。
```

如果这是一个长目标，比如“未来两周持续改善 checkout 稳定性”，入口才是 `/goal`：

```text
/goal
在接下来两周逐步改善 checkout 稳定性。

目标：
1. 先建立错误路径清单。
2. 每次只处理一个高价值错误。
3. 每个改动都要有测试或手测路径。
4. 每次结束都总结剩余风险。
```

如果你怀疑需要外部工具或插件：

```text
/mcp
请帮我确认当前有没有可用工具能读取错误监控、PR 评论或内部文档。
只做能力发现，不修改文件。
```

这个案例说明：Commands 不是魔法词，而是任务阶段的入口。阶段不同，入口不同；入口错了，Codex 的行为就容易错。

## 30. Commands 反例库：这些命令习惯会拖慢你

### 30.1 一上来就 `/goal`

坏例子：

```text
/goal
把整个项目质量提升一下。
```

问题：

```text
- 目标过宽。
- 没有边界。
- 很难判断什么时候完成。
- 容易把多个 PR 混成一个长线程。
```

改法：

```text
/plan
请只读分析项目中最适合先改善的一个质量问题。
限制：必须能在一个小 PR 内完成。
```

### 30.2 用 `/review` 要求实现

坏例子：

```text
/review
帮我审查并修复所有问题。
```

问题：

```text
- review 和 implementation 混在一起。
- finding 还没确认就开始改。
- 容易扩大 diff。
```

改法：

```text
/review
只读审查当前 diff。
输出 findings，不要修改文件。
```

等确认后再普通 prompt：

```text
只修第 1 条 finding。
边界：只改 auth redirect 和对应测试。
```

### 30.3 把 `/mcp` 当搜索按钮

坏例子：

```text
/mcp
帮我查一下最新最佳实践。
```

问题：

```text
- `/mcp` 更适合发现和管理当前可用外部工具。
- 不是所有“查资料”都应该走 MCP。
- 如果资料是官方网页，可能需要 web 或文档来源，而不是项目 MCP。
```

改法：

```text
请先说明当前任务需要哪类外部资料：
1. 项目内部文档。
2. GitHub PR/issue。
3. 官方公开文档。
4. 本地代码即可。

再建议使用 MCP、Plugin、Web 还是普通本地分析。
```

### 30.4 把命令当成课程主线

坏习惯：

```text
先教所有 slash command，再教 App。
```

更好的顺序：

```text
1. 先教 App 任务闭环。
2. 在真实任务里插入 `/plan`。
3. 在 diff 出现后插入 `/review`。
4. 需要能力发现时再讲 `/mcp`、App Plugins 和 CLI TUI `/plugins` 的边界。
5. 长任务出现时再讲 `/goal`。
```

读者不是因为背会命令而会用 Codex，而是在每个任务阶段知道该用哪个入口。

## 31. Commands 与团队语言：把口头习惯变成 prompt 入口

团队里常见的口头话：

```text
- 先别写，先看看。
- 这个 PR 太大了，拆一下。
- 先把风险说清楚。
- 别碰支付逻辑。
- 这事儿做成每周检查。
```

这些话可以翻译成 Commands 入口。

```text
“先别写，先看看”
=> `/plan` + 只读分析 + 不修改文件。

“这个 PR 太大了，拆一下”
=> `/review` + scope creep + 拆分建议。

“先把风险说清楚”
=> `/review` 或普通只读风险分析。

“别碰支付逻辑”
=> 当前 prompt 边界 + AGENTS.md 或 Rules。

“这事儿做成每周检查”
=> Automation + Skill。
```

团队可以沉淀一份入口词典：

```md
# Codex Entry Phrases

## Planning

Use when someone says:
- 先看看
- 先别改
- 帮我拆一下

Prompt:
`/plan ... 不要修改文件`

## Review

Use when someone says:
- 这个 diff 看一下
- 会不会有风险
- 这个 PR 能不能合

Prompt:
`/review ... 只读审查当前 diff`

## Automation

Use when someone says:
- 每周都要检查
- 每次发版前都要看
- 这个提醒能不能自动化

Prompt:
普通线程中描述 schedule、scope、output、archive condition。
```

这份词典看起来简单，但很能提升团队协作。大家不需要争论“该用哪个功能”，只要把日常语言映射到稳定入口。

## 32. Commands 收口：命令结束后要留下下一步

很多命令使用失败，不是开始错了，而是结束时没有收口。`/plan` 给出计划后，用户不知道下一步该执行哪一小块；`/review` 给出 findings 后，作者不知道先修哪条；`/goal` 运行一阵后，线程不知道当前阶段是否完成。

每次命令结束，都可以要求 Codex 输出下一步。

`/plan` 收口：

```text
请把这个 plan 收口成一个最小下一步。

输出：
1. 现在先做哪一件事。
2. 允许修改哪些文件。
3. 不允许碰哪些文件。
4. 完成后跑什么检查。
5. 如果遇到不确定，要停在哪里。
```

`/review` 收口：

```text
请把 review findings 收口成修复顺序。

分类：
1. blocking
2. should fix
3. follow-up
4. ignore for this PR

然后只推荐第一条要修的问题。
```

`/goal` 收口：

```text
请总结当前 goal 的阶段状态。

输出：
1. 已完成什么。
2. 当前卡在哪一步。
3. 下一次醒来或继续时应该先看什么。
4. 是否应该拆新线程。
5. 哪些内容已经不再相关。
```

命令不是流程的终点。命令的好坏，要看它是否让下一步更窄、更清楚、更容易 Review。

## 33. Commands 练习：把一段混乱对话整理成入口序列

混乱对话：

```text
用户：帮我优化 checkout。
Codex：我可以开始修改。
用户：等等，先看看哪里问题最大。
Codex：发现测试失败。
用户：那你修一下。
Codex：改了 checkout、payment、toast。
用户：这个 PR 太大了。
```

要求学生整理成正确入口序列：

```text
1. `/plan`：只读分析 checkout 问题。
2. 普通 prompt：只修一个明确失败。
3. `/review`：检查 diff 是否越界。
4. 普通 prompt：只处理 blocking finding。
5. Review 面板：人工决定 stage。
```

可用 prompt：

```text
请把下面这段混乱 Codex 对话整理成正确 Commands 使用顺序。

要求：
1. 标出哪里应该用 `/plan`。
2. 哪里应该用普通 prompt。
3. 哪里应该用 `/review`。
4. 哪一步不应该继续写代码。
5. 给出改写后的 prompt。
```

这个练习能让读者看到：Commands 不只是功能入口，还是节奏控制器。会用命令的人，能在任务快要跑偏时把它拉回正确阶段。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 知道在App输入框输入`/`可以查看当前可用命令
- [ ] 掌握核心稳定命令：`/status`、`/plan`、`/review`、`/mcp`、`/feedback`
- [ ] 理解`/plan`适合多文件改动、架构调整等场景
- [ ] 知道命令会随版本、插件、权限变化，以当前App显示为准
- [ ] 不把CLI命令表硬搬成App命令表
- [ ] 知道周期任务优先使用 Automations，长目标使用 `/goal`

**全部勾选后即掌握 Codex Commands。**

---

## 附录

### A. 命令速查

| 命令 | 用途 | 稳定性 |
|------|------|--------|
| `/` 或 `/help` | 查看当前可用命令 | 稳定 |
| `/status` | 查看模型、工作区、审批状态 | 稳定 |
| `/plan` | 切换计划模式（先规划不执行） | 稳定 |
| `/review` | 审查当前改动 | 稳定 |
| `/mcp` | 查看/管理MCP工具 | 稳定 |
| `/goal` | 设置持续目标 | 稳定 |
| `/feedback` | 发送产品反馈 | 稳定 |

### B. 推荐学习资源

- **Codex App Commands 官方文档**：https://developers.openai.com/codex/app/commands
- **本系列上一篇**：[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)
- **本系列下一篇**：[CX-04 项目指令与权限](./CX-04-Codex项目指令权限配置完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-04 项目指令、配置、权限与沙盒](./CX-04-Codex项目指令权限配置完整指南.md)。
