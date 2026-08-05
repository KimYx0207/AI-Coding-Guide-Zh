# CX-04 项目指令、配置、权限与沙盒：让 App 知道怎么安全工作

本篇是 App 主线中的项目指令、权限与安全配置篇。

主要来源：OpenAI Codex Config、Rules、Hooks、Settings、CLI 官方文档。

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
> - **信息来源**：OpenAI Codex Config、Rules、Hooks、Settings、CLI 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md) 和 [CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

> **2026-06-18 配置口径**：Codex App 26.609 增加 composer `/init` 和 Migrate to Codex，适合把已有项目规则落成 `AGENTS.md`；CLI 0.141 强化 code mode hooks、PostToolUse blocking、插件路由和 Windows sandbox 修复。App 用户仍优先在 Settings / Review 中收口，CLI 只用于配置排查、CI 和高级权限验证。

1. **编写AGENTS.md**：用项目级指令文件告诉Codex项目规则、命令、风格和禁止事项
2. **掌握多层指令结构**：理解根目录和子目录AGENTS.md的层级关系
3. **理解App权限入口**：通过Settings、审批提示、`/`命令列表管理权限
4. **区分沙盒模式**：清楚read-only、workspace-write、danger-full-access各自的含义
5. **了解config.toml的作用**：知道什么时候需要它，什么时候App Settings就够了
6. **理解Rules和Hooks**：区分命令策略（Rules）和事件脚本（Hooks），知道各自适合什么
7. **建立项目安全基线**：为个人和团队项目配置最小权限基线
8. **核对配置改动**：每次改完配置后能确认当前 App / 线程是否已读到新规则

---

## 术语表（小白必读）

这一章同时出现 `AGENTS.md`、Settings、sandbox、approval、profile、Rules、Hooks、`config.toml`。如果不先分层，后面很容易把“项目说明”“权限开关”“命令策略”“事件脚本”混成一团。

| 术语 | 本质 | 放什么 | 不放什么 |
|---|---|---|---|
| `AGENTS.md` | 给 Codex 看的项目说明和协作规则 | 项目事实、命令、风格、验证、安全边界 | 密钥、临时任务、个人机器路径 |
| App Settings | 当前 App 的用户配置入口 | 模型、终端、审批、沙盒、连接器、外观等 | 团队强制规则的唯一来源 |
| Sandbox | 技术边界 | 能读写哪些目录、命令是否能联网 | 业务规则和代码风格 |
| Approval | 人工确认边界 | 什么动作需要停下来问你 | 替代 Review 或测试 |
| Permission profile | 一组权限和沙盒配置 | 只读、日常开发、应急等场景化配置 | 项目 README 内容 |
| `config.toml` | Codex 持久配置文件 | MCP、profiles、feature flags、hooks 等高级配置 | 未确认字段、公司密钥 |
| Rules | 命令策略 | 允许、提示或禁止特定命令前缀 | 长流程、代码审查 SOP |
| Hooks | 生命周期事件脚本 | 命令前检查、日志、审计、自动校验 | 没审查过的危险脚本 |
| Managed requirements | 企业强制配置 | 组织最低安全要求、允许的 sandbox / approval | 个人临时偏好 |

一句话：`AGENTS.md` 教 Codex “怎么理解项目”，Settings / profiles 决定“能做多大动作”，Rules 决定“哪些命令该拦”，Hooks 决定“事件发生时跑什么脚本”。

## 0. 配置系统的四层心智模型

老金，我写项目指令时最关心的是让 Codex 少猜；项目规则越清楚，后面的修改越不容易跑偏。

你可以把 Codex 配置想成四层，从软到硬：

```text
项目说明层：AGENTS.md
  -> 告诉 Codex 项目事实、命令、规范和安全边界

用户偏好层：App Settings / config.toml
  -> 设置模型、终端、审批、沙盒、MCP、插件等

命令策略层：Rules / permission profiles
  -> 对命令、目录、网络和危险动作建立可执行边界

事件脚本层：Hooks
  -> 在特定时机运行真实脚本，做审计、检查或自动化
```

新手只需要先掌握前两层：`AGENTS.md` 和 App Settings。团队和企业再逐步引入 profiles、Rules、managed requirements 和 Hooks。

### 0.1 为什么不能只靠提示词

提示词适合当前任务，但它有三个问题：

1. **不持久**：换线程后你可能忘了重复说。
2. **不够硬**：你说“不要推 main”，但没有命令策略时仍可能需要靠人工盯。
3. **不可审计**：团队很难知道每个人临时说了什么。

所以长期项目规则写进 `AGENTS.md`；高风险命令用 Rules；团队最低权限用 managed requirements；复杂事件处理才考虑 Hooks。

### 0.2 配置读取的实操顺序

当 Codex 行为不符合预期时，按这个顺序排查：

1. **当前项目是否打开对了目录**：工作区错了，`AGENTS.md` 再好也读不到。
2. **新线程是否读到 `AGENTS.md`**：旧线程可能仍停留在旧上下文。
3. **App Settings 是否和任务风险匹配**：只读、日常写入、危险模式不能混用。
4. **项目 `.codex/` 是否被信任**：未信任项目不会加载项目级 `.codex/` 配置层。
5. **Rules 是否匹配了真实命令前缀**：用 `match` / `not_match` 和 `execpolicy check` 测。
6. **Hooks 是否需要信任或是否失败**：未信任、超时、路径错都会影响执行。

这就是 Claude Code 配置篇常见的“机制解释”在 Codex 里的对应写法：不是只贴配置，而是讲清楚配置为什么生效、什么时候不生效。

## 先做一个15分钟实操：写出第一份 `AGENTS.md`

这一章会讲权限、沙盒、Rules 和 Hooks，但 App 用户最先应该做的是 `AGENTS.md`。它决定 Codex 打开项目后先理解哪些规则。

### 第一步：让 Codex 只读分析项目

在 Codex App 当前项目线程里输入：

```text
Read this project. Report:
1. what this project does
2. the install command
3. the test command
4. the main source and docs directories
5. files or directories that should not be changed casually

Do not modify files.
```

这一步只收集项目事实，不让 Codex 写文件。

### 第二步：创建最小可用的 `AGENTS.md`

在项目根目录创建 `AGENTS.md`：

```markdown
# AGENTS.md

这份文件约束 Codex 在本项目里的工作方式，用来减少常见的 AI 编程失误。你可以在此基础上继续补充项目专属规则。

参考来源：https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md

取舍说明：这些规则更偏向谨慎和可验证，而不是最快完成。遇到很小的简单任务时，可以按实际情况简化流程。

## 项目背景

开始修改前，先阅读 README、配置文件和目录结构，确认项目目标、技术栈和关键目录；不要凭经验猜。

## 常用命令

在 Codex App 终端里只运行项目已经证明存在的命令。优先从 README、脚本清单、构建配置、CI workflow 和上一轮 Review 记录里确认；找不到就先只读检查，不要让 Codex 现场编一个。

不要把示例命令写成项目事实；没有确认过的命令不要写进本文件，也不要留下占位文本。

## 1. 写代码前先想清楚

不要假装已经理解，也不要把不确定性藏起来。该说清楚的地方先说清楚。

开始实现前：

- 先在当前 thread 里写出任务边界、将要读取的文件和不会碰的目录。
- 需求可能有多种解释时，先用 `/plan` 或自然语言列出分支，再让用户选。
- 发现更小的 App 工作流能解决问题时，优先提出，例如只读 Review、只改文档、只跑测试。
- 当请求会扩大权限、绕过 Review 或触碰敏感文件时，先停下来说明风险。

## 2. 简单优先

只写解决当前问题所需的最少代码，不做猜测式扩展。

- 不把一次 App thread 做成“顺手重构全项目”。
- 不因为 Codex 能开 worktree，就把小修拆成复杂分支流程。
- 不新增 Settings、Rules、Hooks 或 profile 字段，除非本任务确实需要。
- 不替未来想象场景写大段配置；先让当前 diff 可读、可审、可回滚。
- 如果 Review 面板里出现无关文件，先收窄而不是继续解释。

自检问题：资深工程师看到这段实现，会不会觉得过度设计？如果会，就删减。

## 3. 外科手术式修改

只碰必须修改的地方。只清理自己造成的问题。

编辑已有代码时：

- Codex 每次改动都要能在 Review 面板里解释给人看。
- 不把格式化、重命名、目录移动混进业务修复。
- 沿用项目已有风格、脚本和测试入口；不要把别的仓库习惯搬进来。
- 看到无关问题，放到后续任务建议里，不在当前 thread 直接处理。

如果你的改动制造了无用内容：

- 删除由本次改动造成的无用 import、变量、函数。
- 不删除本来就存在的死代码，除非任务明确要求。

检查标准：每一行改动都应该能追溯到用户这次请求。

## 4. 目标驱动执行

把任务转成可验证的目标，然后循环到验证完成。

示例：

- “加校验” -> “先在 App 里确认输入路径和失败用例，再改最小文件”
- “修 bug” -> “先复现或写出复现条件，再让 Review 只显示相关 diff”
- “重构 X” -> “先说明为什么必须重构，再用测试和 Review 证明行为没变”

多步骤任务先写简短计划：

```text
1. [步骤] -> 验证：[检查方式]
2. [步骤] -> 验证：[检查方式]
3. [步骤] -> 验证：[检查方式]
```

清晰的成功标准能让你独立推进；含糊的标准，比如“让它能用”，会导致反复追问。

## 安全边界

- 不读取、打印或提交 `.env*`、密钥、Token、证书等敏感信息。
- 不编辑生成文件、构建产物、锁文件，除非任务明确要求。
- 涉及依赖、权限、脚本、部署配置的变化，先说明理由再改。

## 验证要求

- 改源码后运行相关测试、lint 或 build。
- 如果验证命令不存在、失败或耗时过长，要写清楚原因和已做的替代检查。
- 最终回复说明改了哪些文件、验证了什么、还剩什么风险。

## 这些规则生效时应该看到

- diff 里无关改动更少。
- 因为过度复杂而返工的次数更少。
- 澄清问题发生在动手前，而不是出错之后。
- 每次修改都有明确验证方式。
```

创建正式 `AGENTS.md` 前，先让 Codex 根据第一步的分析输出完整版本。命令必须来自项目文件或你亲自确认；没有确认的命令整行删除，不要留空、不要写占位。

### 第三步：验证 Codex 是否读到了规则

开启一个新线程，输入：

```text
Summarize the project rules from AGENTS.md.
Then tell me how you would verify a source-code change in this project.
Do not modify files.
```

如果 Codex 能复述项目规则、测试命令和禁止事项，说明 `AGENTS.md` 已经成为项目上下文的一部分。

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想让Codex知道项目规则

**只看这些章节**：

```
✅ 先做一个15分钟实操：写出第一份 AGENTS.md
✅ 第1部分：App用户先写AGENTS.md（5分钟）
✅ 第4部分：App中的权限入口（5分钟）
✅ 第5部分：沙盒模式（5分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握权限和安全配置

**学习顺序**：从头到尾所有章节

---

### 路径C：企业配置（⏱️ 20分钟）

**适合人群**：需要给团队设统一安全边界

**直接跳到**：

```
🔧 第6-7部分：config.toml + Rules
🔧 第10部分：App项目基线
```

---

## 1. App 用户先写 `AGENTS.md`

`AGENTS.md` 是项目级指令文件。App 打开项目后，会把它作为重要上下文。

它应该回答：

- 项目是什么。
- 技术栈是什么。
- 常用命令是什么。
- 代码风格是什么。
- 修改后如何验证。
- 哪些文件或动作禁止。

推荐模板：

```markdown
# Project Instructions

## Overview
这是一个 Next.js 应用，主代码在 `src/`，测试在 `tests/`。

## Commands
- 安装依赖：`npm install`
- 开发服务：`npm run dev`
- 类型检查：`npm run typecheck`
- 单元测试：`npm test`
- 格式检查：`npm run lint`

## Code Style
- 使用 TypeScript strict mode。
- 不新增 `any`。
- 复用现有组件和工具函数。

## Testing
- 修改业务逻辑时补充或更新测试。
- 提交前至少运行相关测试。

## Safety
- 不读取或修改 `.env*`。
- 不提交真实密钥。
- 不直接改数据库迁移，除非任务明确要求。
```

## 2. `AGENTS.md` 不该写什么

不要写：

- API Key、token、cookie。
- 只针对本次任务的临时要求。
- 个人机器路径。
- 不稳定的模型名称或价格。
- “写高质量代码”这种无法验证的口号。

临时要求写在 App 当前线程里；长期规则才写进 `AGENTS.md`。

## 3. 多层 `AGENTS.md`

Monorepo 可以在根目录和子目录放不同的 `AGENTS.md`：

```text
repo/
  AGENTS.md
  apps/web/AGENTS.md
  packages/api/AGENTS.md
```

理解方式：

- 根目录写全局规则。
- 子目录写局部规则。
- 越靠近当前文件的指令越能补充具体上下文。
- 不要依赖“同名标题自动覆盖”这种想象，写规则时要尽量避免冲突。

### 3.1 `AGENTS.md` 写作结构：从事实到约束

一份好 `AGENTS.md` 不应该像口号墙，而应该像项目交接文档。推荐结构：

| 模块 | 要回答的问题 | 示例 |
|---|---|---|
| 项目概览 | 这个项目是什么，主要目录在哪里 | `src/` 是应用代码，`tests/` 是测试 |
| 常用命令 | 安装、测试、lint、build 怎么跑 | 命令必须来自 README / package.json / CI |
| 修改边界 | 哪些文件可以改，哪些要谨慎 | 不直接改迁移文件，不碰 `.env*` |
| 代码风格 | 当前项目已有写法是什么 | TypeScript strict，不新增 `any` |
| 验证方式 | 改完怎么证明 | 跑相关测试，失败要解释 |
| 安全规则 | 哪些动作默认禁止 | 不提交密钥，不自动 push |
| 交付格式 | 最终回复要说明什么 | 改了什么、验证了什么、风险是什么 |

写作顺序是：先写项目事实，再写操作规则，最后写禁止事项。不要一上来写“你必须写高质量代码”，这种句子对 Codex 和新人都没有足够信息。

### 3.2 多层文件的冲突处理

Monorepo 里常见冲突：

```text
根 AGENTS.md：所有包都用 npm test
apps/mobile/AGENTS.md：移动端包使用 pnpm test
```

正确写法不是互相打架，而是让子目录文件明确说明适用范围：

```markdown
# apps/mobile/AGENTS.md

本文件只适用于 apps/mobile 下的 React Native 包。
在本目录内，测试命令使用 pnpm test；不要套用根目录 npm test 示例。
```

如果你发现根目录和子目录规则冲突，不要让 Codex 猜。先让它报告冲突，再由人决定哪条规则适用。

## 4. App 中的权限入口


App 用户优先通过这几处理解权限：

- App Settings。
- 当前线程的审批提示。
- 当前 App 的 `/` 命令列表中显示的权限入口。
- Review 面板中的 diff。

常见策略：

| 场景 | 建议 |
|---|---|
| 陌生项目 | 保守审批，先只读 |
| 日常小改 | 允许常见读写和安全命令 |
| 大规模重构 | 使用 worktree，严格 review |
| CI / 自动化 | 外部沙箱 + 最小权限 |
| 涉及密钥 / 生产数据 | 默认拒绝，人工确认 |

> **v0.133.0→v0.141.0 权限口径**：permission profiles 不再只是单个 approval mode。新版已支持 profile 列表、继承、managed `requirements.toml`、运行时刷新、named profiles 和更强的 Windows sandbox 集成；后续又补强了 cloud-managed config、remote-control grants、personal access token v2、plugin JSON 输出、配置错误展示、加密凭证、PostToolUse blocking、远程执行权限路径保留和 Windows sandbox stale credentials 修复。`--profile` 已成为 CLI / TUI permissions / sandbox flows 的主选择器，旧 profile 配置会走迁移提示；个人项目可以继续先用 App Settings，团队项目要把 profile、`AGENTS.md`、Rules、Plugins、MCP 和 sandbox 一起看。

实操时按这个顺序确认：

1. 在 App Settings 里选默认 profile 和 sandbox。
2. 用当前 App 的 `/` 列表、线程权限提示或 Settings 查看实际生效的审批策略；`/permissions` 属于 CLI 常见入口，App 是否显示以当前版本为准。
3. 如果团队下发 managed `requirements.toml`，先读它规定的工具、网络和目录边界。
4. 修改 profile 后开一个新任务验证；如果当前版本支持 runtime refresh，再确认旧线程是否已刷新。

## 5. 沙盒模式怎么理解


Codex 的沙盒是为了限制命令和文件访问范围。CLI 中常见模式包括：

| 模式 | 含义 |
|---|---|
| `read-only` | 只读，适合审计和探索 |
| `workspace-write` | 可写工作区，适合日常开发 |
| `danger-full-access` | 无沙盒限制，只能在外部可信沙箱中使用 |

App 用户不需要一开始背 CLI 参数，但要理解：权限越大，越需要 Review、Git 和备份。

## 6. `config.toml` 是什么


`config.toml` 是 Codex 的配置文件。它适合团队或高级用户管理：

- 默认 profile。
- 审批和沙盒默认值。
- MCP server。
- feature flags。
- 终端和环境策略。

v0.133.0 以后，团队不要把权限只散落在 `config.toml`。更稳的结构是：

| 配置层 | 放什么 | 不放什么 |
|---|---|---|
| `AGENTS.md` | 项目事实、测试命令、修改边界 | 密钥、临时版本号、个人偏好 |
| permission profile | 审批模式、沙盒、工具边界 | 业务说明 |
| managed `requirements.toml` | 团队强制要求、最低安全基线 | 本地一次性调试选项 |
| App Settings | 个人机器上的默认模型、终端和连接器 | 团队必须遵守的规则 |

App 主线中，普通读者不需要先手写它。推荐顺序：

1. 先在 App Settings 里完成模型、权限、终端、插件和 MCP 的基础设置。
2. 团队需要统一策略时，再查官方 Config Reference。
3. 只复制官方当前支持的字段。
4. 改完后重启或刷新 App，再用 `/status`、Settings、MCP 列表等入口核对。

如果教程需要展示配置，优先展示“要查官方 schema”而不是写死字段。比如 `/goal` 不显示时，官方 App Commands 文档说明可以使用 `[features] goals = true` 或 `codex features enable goals`；其他字段也要以当前官方 Config Reference 为准。

```toml
# 只作为结构提示，实际字段以官方 Config Reference 和当前 App 为准。
# 不要把模型名、实验开关或公司密钥硬写进教程示例。
```

注意：字段会随版本变化，写教程时应链接官方 Config Reference，不要复制过时字段。

## 7. Rules：比 prompt 更硬的命令边界

Rules 用来限制或允许命令执行。官方 Rules 是放在 `rules/` 目录下的 `.rules` 文件，语法是 Starlark 风格的 `prefix_rule()`。适合团队把危险命令拦住。

示例：对 `gh pr view` 这类读取 PR 的命令要求提示确认。

```python
# ~/.codex/rules/default.rules 或受信任项目里的 .codex/rules/default.rules
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "prompt",
    justification = "查看 PR 可以，但需要确认目标仓库和输出字段。",
    match = [
        "gh pr view 123",
        "gh pr view --repo owner/repo 123",
    ],
    not_match = [
        "gh pr checkout 123",
    ],
)
```

危险命令可以用 `decision = "forbidden"` 拦住，但要先写 `match` / `not_match` 样例，确认规则匹配的是你想拦的命令。

Rules 适合：

- 禁止危险命令。
- 要求高风险命令人工审批。
- 给团队设置统一安全边界。

Rules 不适合：

- 写代码风格。
- 写长工作流。
- 替代测试。

## 8. Hooks：事件脚本

Hooks 是事件触发脚本，适合做：

- 命令执行前检查。
- 工具执行后记录日志。
- 自动格式化。
- 外部审计。

App 用户应先理解它的配置入口和风险：

- Hook 配置通常放在 `.codex/hooks.json` 或 `.codex/config.toml` 的 `[hooks]` 表中。
- 脚本可以放在 `.codex/hooks/` 等目录，但目录本身不是 hook 配置入口。
- Hook 会运行真实脚本。
- Hook 可能读取敏感上下文。
- Hook 写错会阻塞工作流。

学习阶段不要急着写 Hook。先用 `AGENTS.md`、Settings、Rules。

### 8.1 Hooks 的执行机制

Hooks 厚度不在“能写脚本”，而在你理解它进入了 agentic loop。它不是 Markdown 规则，而是真实命令：

```text
某个事件发生
  -> Codex 找到匹配的 hook 配置
  -> 需要信任的 hook 先走 trust review
  -> hook 命令在当前 session cwd 里运行
  -> 输出、失败、超时都会影响体验
```

常见事件包括 `SessionStart`、`PreToolUse`、`PermissionRequest`、`PostToolUse`、`PreCompact`、`PostCompact`、`UserPromptSubmit`、`SubagentStart`、`SubagentStop`、`Stop`。并不是每个事件都适合新手使用；团队最常见的是命令前检查、权限请求检查、命令后审计和停止时校验。

示例：只在 Bash 命令前做策略检查：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .codex/hooks/pre_tool_use_policy.py",
            "timeout": 30,
            "statusMessage": "Checking command policy"
          }
        ]
      }
    ]
  }
}
```

这个例子只说明形状。真实项目里不要直接用相对路径上线，优先从 git root 或绝对路径解析，避免从子目录启动 Codex 时找不到脚本。

### 8.2 Rules 和 Hooks 的选择表

| 需求 | 优先用 | 理由 |
|---|---|---|
| 禁止 `rm -rf`、`gh pr merge` 等命令 | Rules | 简单、可预测、可用 match / not_match 测 |
| 命令前做复杂上下文判断 | Hook | 需要脚本逻辑 |
| 写文件后跑格式化 | Hook | 事件触发更合适 |
| 记录审计日志 | Hook | 需要把事件写到日志系统 |
| 统一代码风格 | `AGENTS.md` + 测试 / lint | Rules 不适合写风格 |
| 发布流程 SOP | Skill | 长流程应该沉淀为 Skill |

能用 Rules 解决的命令边界，不要先写 Hook。Hook 的自由度更高，维护成本和安全风险也更高。

### 8.3 Hooks 排障表

| 症状 | 可能原因 | 处理 |
|---|---|---|
| Hook 没运行 | 配置位置不在 active config layer，项目 `.codex/` 未信任，feature 被关闭 | 先看启动警告和 `/hooks`（CLI） |
| Hook 需要信任 | 非 managed hook 新增或 hash 变化 | 审查命令内容后再 trust |
| Hook 找不到脚本 | 相对路径依赖启动目录 | 用 git root 或绝对路径 |
| Hook 卡住 | 脚本等待交互或 timeout 太长 | 改成非交互脚本，设置合理 timeout |
| 多个 Hook 都跑了 | 多来源 Hook 会合并运行 | 检查用户、项目、插件、managed 来源 |
| Windows 上失败 | 路径和解释器不同 | 使用 Windows 专用命令字段或跨平台脚本 |

Hook 是企业治理的强工具，但不适合用来弥补项目说明不清。先把 `AGENTS.md` 写清，再决定是否需要 Hook。

## 9. 改完配置后怎么核对


每次改 `AGENTS.md`、Settings、Rules、Hooks 或 `config.toml` 后，都按这张表自查：

| 改动 | App 中怎么核对 |
|---|---|
| `AGENTS.md` | 新线程里让 Codex 总结项目规则，看是否读到正确内容 |
| 权限 / 沙盒 | `/status` 或 Settings 显示符合预期 |
| MCP 配置 | `/mcp` 能看到 server 和工具 |
| Rules | 试一个应被拦截的无害模拟命令，确认提示正确 |
| Hooks | 在测试仓库里触发一次，看日志和副作用 |

配置改完不核对，很容易以为规则生效了，实际线程仍在旧状态。

## 9.1 配置变更的安全流程

团队项目改配置，建议像改代码一样走小步流程：

1. **先说明目的**：这次是为了减少误删、限制网络、统一 MCP，还是修复 Hook 误报。
2. **只改一类配置**：不要同一 PR 同时改 `AGENTS.md`、Rules、Hooks、MCP 和 profiles。
3. **用只读任务验证读取**：先让 Codex 复述新规则。
4. **用无害命令验证 Rules**：例如检查 `gh pr merge 123` 是否命中 prompt，而不是直接合并 PR。
5. **在测试仓库验证 Hooks**：确认脚本路径、输出、失败行为和 Windows / macOS 差异。
6. **更新团队说明**：告诉成员哪里变了，怎么排查。

配置变更最怕“看起来是文档，实际改变了工具行为”。尤其 Rules 和 Hooks，一定要当成可执行系统的一部分来 Review。

## 9.2 常见故障排查

| 问题 | 先看哪里 | 常见修复 |
|---|---|---|
| Codex 没读到 `AGENTS.md` | 当前工作目录、新线程、文件位置 | 把文件放到项目根或当前目录链路上 |
| Codex 忽略子目录规则 | 当前任务文件路径、子目录 `AGENTS.md` | 让 Codex 明确说明当前文件适用哪些规则 |
| Rules 没拦住命令 | `pattern` 是否是真实命令前缀 | 增加 `match` / `not_match` 样例后测试 |
| App 和 CLI 表现不同 | 当前界面、版本、配置层 | 以各自官方入口核对，不互相假设 |
| 项目 `.codex/` 不生效 | 项目是否被信任 | 在可信项目里再加载项目级配置 |
| 团队成员表现不一致 | 版本、Settings、managed requirements | 统一版本说明和 profile 名称 |

### 9.3 个人、团队、企业三种落地方式

| 场景 | 推荐组合 | 不建议 |
|---|---|---|
| 个人学习 | `AGENTS.md` + App Settings + Review | 一上来写 Hook |
| 小团队 | 根 `AGENTS.md` + `.codex/rules/default.rules` + 少量 MCP | 每个人手动复制配置 |
| 企业 | managed requirements + profiles + Rules + reviewed Hooks + 插件/MCP 白名单 | 只靠口头约定和聊天提示 |

配置的目标不是把 Codex 绑死，而是让它在正确边界里大胆工作。

## 10. App 项目基线

个人项目的最小基线：

```text
AGENTS.md
  写清项目命令、测试、禁止事项

App Settings
  使用默认或保守审批

Review
  每次改动都看 diff

Git
  小步提交，不混 unrelated changes
```

团队项目再增加：

```text
.codex/config.toml
.codex/rules/default.rules
.codex/hooks.json 或 .codex/config.toml 中的 [hooks]
CI 中的 codex review 或测试任务
```

## 11. 课堂工坊：配置一份能约束 Codex 的项目基线

### 案例一：写一份最小 `AGENTS.md`

目标：让 Codex 先知道项目事实和安全边界。

```markdown
# Project Instructions

## Overview
这是一个 Web 项目，主要代码在 src/，测试在 tests/。

## Commands
- Install: npm ci
- Test: npm test
- Lint: npm run lint

## Safety
- 不读取或修改 .env*。
- 不自动提交、推送或创建 PR。
- 大范围改动前先给计划。
```

新线程发送：

```text
阅读 AGENTS.md，复述本项目的命令和安全边界。不要修改文件。
```

你应该看到：Codex 能读到项目命令和禁止事项；如果它没读到，先确认文件位置和线程工作目录。

### 案例二：用 Rules 拦一个 GitHub 写操作

目标：理解 Rules 是命令策略，不是代码风格文档。

```python
# .codex/rules/default.rules
prefix_rule(
    pattern = ["gh", "pr", "merge"],
    decision = "prompt",
    justification = "合并 PR 前需要人工确认目标仓库、分支和 CI 状态。",
    match = [
        "gh pr merge 123",
        "gh pr merge 123 --squash",
    ],
)
```

用下面命令检查规则：

```bash
codex execpolicy check --pretty --rules .codex/rules/default.rules -- gh pr merge 123
```

你应该看到：命令命中 prompt。若没有命中，先改 `match` / `not_match` 样例，不要直接上线。

### 案例三：多层 `AGENTS.md` 的局部规则

目标：让测试目录有更具体的本地规则。

```text
AGENTS.md
tests/AGENTS.md
```

根目录写全局命令，`tests/AGENTS.md` 写测试命名和 fixture 规则。让 Codex 只读总结 `tests/` 下规则时，你应该看到：它同时理解根目录规则和测试目录补充规则，不把测试局部规则误用到整个项目。

## 12. 配置 Cookbook：从个人仓库到团队基线

这一节给你几种常见情境的组合方式。每个组合都先说明目的，再说明用哪些层解决。

### 12.1 个人学习仓库

目标：降低误操作，练习 App 主线。

```text
AGENTS.md
  - 项目是什么
  - 常用命令
  - 不读取 .env*
  - 改完展示 diff，不自动提交

App Settings
  - 默认或保守权限
  - 陌生项目先只读

Review
  - 每次改完看文件列表和 diff
```

不需要先写 Rules 和 Hooks。个人学习阶段最重要的是建立只读、写入、Review 的节奏。

### 12.2 小团队共享仓库

目标：让所有成员用同一套项目事实和危险命令边界。

```text
AGENTS.md
  - 项目结构
  - package manager
  - test / lint / build 命令
  - 代码风格
  - 安全边界

.codex/rules/default.rules
  - prompt: gh pr merge
  - forbidden: 递归删除高风险目录
  - prompt: 部署命令

团队文档
  - App Settings 推荐 profile
  - MCP / Connector / Plugin 登记表
```

这个阶段 Rules 的价值很高，因为它把“不要随便合并/删除/部署”变成更硬的命令策略。

### 12.3 Monorepo

目标：不同子项目有不同命令和边界。

```text
repo/AGENTS.md
  - 仓库总体结构
  - 全局安全规则
  - 不要跨包乱改

apps/web/AGENTS.md
  - Web 应用命令
  - 前端测试和构建

packages/api/AGENTS.md
  - API 包命令
  - 数据库和迁移边界
```

提示词要明确当前任务在哪个包里：

```text
目标：修复 apps/web 登录页样式。
范围：只改 apps/web 下文件。
请先总结当前目录适用哪些 AGENTS.md 规则，再给计划。
不要修改 packages/api。
```

### 12.4 企业受管环境

目标：让个人偏好不能绕过组织最低安全要求。

```text
managed requirements
  - allowed sandbox modes
  - allowed approval policies
  - managed hooks
  - restrictive rules
  - MCP server allowlist

项目 AGENTS.md
  - 项目事实和验证命令

团队 profiles
  - read-only
  - daily-dev
  - ci
  - emergency
```

企业环境里，`AGENTS.md` 负责项目事实，managed requirements 负责组织底线。不要把组织底线只写进项目 README。

### 12.5 配置变更 PR 模板

```markdown
## Summary
- 改了哪一类 Codex 配置
- 目的是什么

## Scope
- 涉及 AGENTS.md / Rules / Hooks / config / MCP 中哪一层
- 不涉及哪些层

## Verification
- 新线程是否读到 AGENTS.md
- Rules 是否用 execpolicy check 验证
- Hooks 是否在测试仓库触发
- MCP 是否只读试跑

## Risk
- 可能阻塞哪些命令
- Windows / macOS 是否有差异
- 如何回滚
```

这个模板能避免“顺手改配置”变成团队级故障。

## 常见问题

### Q1：可以在 `AGENTS.md` 里指定模型吗？

不建议。模型选择属于运行配置，不是项目事实。

### Q2：Rules 和 Hooks 有什么区别？

Rules 更像命令策略；Hooks 是事件脚本。能用 Rules 解决的，不要先写 Hook。

### Q3：App 用户必须学 `config.toml` 吗？

不必须。单人使用先掌握 App Settings 和 `AGENTS.md`。

### Q4：`AGENTS.md` 写得越长越好吗？

不是。越长越容易过期，也会挤占上下文注意力。好文件应该短、准、可验证。大段参考资料可以放到单独文档，让 `AGENTS.md` 指向它。

### Q5：Rules 能不能替代审批？

不能完全替代。Rules 控制特定命令前缀的决策，审批仍然是当前会话或组织策略的一部分。你可以用 Rules 减少重复确认，也可以强制危险命令 prompt / forbidden，但仍要看 sandbox 和 approval 设置。

### Q6：Hooks 能不能自动修所有问题？

不建议。Hooks 适合检查、记录、阻断或做很小的机械动作。复杂修复应该回到线程、Skill、Review 和测试流程里。

### Q7：团队应该先上 Rules 还是 Hooks？

先 Rules。把危险命令边界固定下来，再考虑少量 Hook 做审计和复杂检查。Hook 是强能力，越强越需要审查。

---

## 13. `AGENTS.md` 深度写作：让 Codex 读到“项目真实习惯”

很多团队写 `AGENTS.md` 时会犯两个极端：要么写成口号，要么写成百科。好 `AGENTS.md` 让 Codex 在关键决策点不猜。

### 13.1 `AGENTS.md` 的五类内容

| 内容 | 作用 | 例子 |
|------|------|------|
| 项目事实 | 让 Codex 知道项目是什么 | 技术栈、目录结构、主要模块 |
| 常用命令 | 让 Codex 会验证 | test、lint、typecheck、build |
| 修改边界 | 让 Codex 不乱动 | 不改 generated、不碰 migrations |
| 风格约定 | 让 Codex 融入代码 | 命名、错误处理、组件模式 |
| 安全提醒 | 让 Codex 避免事故 | 不提交 secrets、不访问生产数据 |

### 13.2 事实优先于口号

差写法：

```md
请写高质量代码，像世界顶级工程师一样认真。
```

好写法：

```md
Run `pnpm test -- --runInBand` for targeted Jest checks.
Generated API clients live under `src/generated/`; do not edit them manually.
Use `src/lib/errors.ts` helpers instead of throwing plain strings.
```

事实越具体，Codex 越少猜。

### 13.3 单仓库模板

```md
# Project Instructions

## Overview

This is a TypeScript web app with a Next.js frontend and API routes.

## Common Commands

- Install: `pnpm install`
- Lint: `pnpm lint`
- Test: `pnpm test`
- Typecheck: `pnpm typecheck`

## Code Style

- Prefer small functions near their call sites.
- Use existing error helpers from `src/lib/errors.ts`.
- Do not introduce new state libraries without discussion.

## Editing Boundaries

- Do not edit generated files under `src/generated/`.
- Do not change database migrations unless the task explicitly asks.
- Keep unrelated formatting changes out of functional patches.

## Security

- Never commit secrets.
- Treat `.env*` files as sensitive.
- Do not call production services from local tests.
```

### 13.4 Monorepo 模板

```md
# Repository Instructions

## Workspace

This repository contains multiple packages:

- `apps/web`: customer-facing web app
- `apps/admin`: internal admin app
- `packages/ui`: shared UI components
- `packages/api`: shared API clients

## Commands

- Root install: `pnpm install`
- Web test: `pnpm --filter web test`
- Admin test: `pnpm --filter admin test`
- UI lint: `pnpm --filter ui lint`

## Boundaries

- When working in one package, avoid changing sibling packages unless needed.
- Shared package changes require checking at least one downstream app.
- Do not update lockfiles unless dependency changes are part of the task.
```

### 13.5 子目录 `AGENTS.md`

```md
# apps/admin Instructions

This app is internal-only.

Use existing table components from `packages/ui`.
Do not add new chart libraries.
When changing permissions UI, read `docs/admin-permissions.md` first.
```

子目录说明应该补充局部规则，不要重复根目录所有内容。

## 14. 配置优先级：为什么同一个 Codex 在不同项目表现不同

Codex 会受到多层配置影响：系统、管理员、用户、项目、当前会话。学习时不用背完每个细节，但要理解“近的规则和高优先级配置会改变行为”。

### 14.1 排查配置时的顺序

```text
1. 当前 App 线程的权限和 sandbox。
2. 当前项目里的 AGENTS.md。
3. 当前项目的 .codex/config.toml。
4. 用户级 ~/.codex/config.toml。
5. 管理员或企业受管要求。
6. CLI 启动参数或 profile override。
```

### 14.2 同一个任务表现不同的常见原因

| 表现 | 可能原因 |
|------|----------|
| A 项目能写，B 项目不能写 | sandbox 或 trusted project 不同 |
| CLI 能看到 MCP，App 没看到 | 配置刷新或项目作用域不同 |
| 某个 Skill 不触发 | skill scope、description 或禁用配置 |
| Rules 在一个项目生效 | 项目规则文件或信任状态不同 |
| Hooks 被跳过 | hook trust 或 feature setting |

### 14.3 配置排查 prompt

```text
当前 Codex 行为和我预期不一致。
请先不要修改文件。
请帮我按层排查：
1. App 当前权限和 sandbox
2. AGENTS.md 指令
3. 项目级 config
4. 用户级 config
5. MCP / Skills / Plugins 是否可见
6. 是否有企业受管策略影响
```

## 15. 权限 Profile：把“能做什么”写成可复用方案

Codex 支持内置权限 profile，也支持自定义 profile。新手先记三类：

| Profile | 含义 |
|---------|------|
| `:read-only` | 本地命令保持只读 |
| `:workspace` | 允许在工作区范围内写 |
| `:danger-full-access` | 移除本地沙盒限制，谨慎使用 |

### 15.1 自定义 profile 示例

```toml
default_permissions = "project-edit"

[permissions.project-edit]
description = "Project editing with narrow network access."
extends = ":workspace"

[permissions.project-edit.filesystem.":workspace_roots"]
"**/*.env" = "deny"
"src/generated/**" = "read"

[permissions.project-edit.network]
enabled = true

[permissions.project-edit.network.domains]
"api.openai.com" = "allow"
"*.github.com" = "allow"
"tracking.example.com" = "deny"
```

这个示例表达的是：

- 从 `:workspace` 继承基本工作区权限。
- 环境文件始终拒绝。
- 生成目录只读。
- 网络只开放需要的域。

### 15.2 什么时候不用 full access

```text
- 不知道任务会运行什么命令。
- 项目里有生产密钥或客户数据。
- 自动化后台运行。
- 子代理会并行执行。
- 外部插件或 MCP 会参与。
```

如果你只是为了少点弹窗就开 full access，后面排查事故会更难。

## 16. Rules 深入：把危险命令拦在执行前

Rules 适合约束命令执行边界。它比 `AGENTS.md` 更硬，因为它参与工具执行策略。

### 16.1 Rules 适合做什么

| 用途 | 例子 |
|------|------|
| 拦危险删除 | 阻止 `rm -rf` 或跨目录删除 |
| 拦外部发布 | 阻止未经确认的 publish |
| 拦 Git 写操作 | 对 push、tag、force push 要求人工确认 |
| 限制包管理器 | 只允许项目指定命令 |
| 允许只读命令 | git status、rg、ls |

### 16.2 Rules 不适合做什么

```text
- 写复杂业务流程。
- 替代测试。
- 替代 Review。
- 判断产品取舍。
- 管理外部账号授权。
```

### 16.3 课程示例：拦截高风险 Git 操作

```python
# .codex/rules/default.rules

def prefix_rule(argv):
    if len(argv) >= 2 and argv[0] == "git" and argv[1] == "push":
        return "prompt"
    if len(argv) >= 3 and argv[0] == "git" and argv[1] == "push" and "--force" in argv:
        return "deny"
    return None
```

课程里不要把 Rules 写成 TOML 表。它使用 rules 文件和 Starlark 风格函数来表达命令策略。

### 16.4 允许只读命令

```python
def prefix_rule(argv):
    readonly = [
        ["git", "status"],
        ["git", "diff"],
        ["git", "log"],
        ["rg"],
        ["ls"],
    ]
    for prefix in readonly:
        if argv[:len(prefix)] == prefix:
            return "allow"
    return None
```

这类规则适合教学：先让新人安全探索，再逐步开放写操作。

## 17. Hooks 深入：事件脚本不是万能自动化

Hooks 可以在 Codex 的事件点运行脚本，例如 session start、tool use 前后、用户提交 prompt、subagent lifecycle 或 stop。它很强，但不应该一开始就上。

### 17.1 Hooks 的适用场景

| 场景 | 适合吗 |
|------|--------|
| 记录会话摘要 | 适合 |
| 检查 prompt 是否粘贴密钥 | 适合 |
| 工具执行前做命令策略补充 | 适合 |
| 自动修复所有错误 | 不适合 |
| 替代人类审批 | 不适合 |
| 每次都运行很慢的脚本 | 不适合 |

### 17.2 Hooks 与 Rules 的区别

| 机制 | 更像什么 | 重点 |
|------|----------|------|
| Rules | 命令执行策略 | allow / prompt / deny |
| Hooks | 事件脚本 | 在事件发生时运行检查或记录 |

### 17.3 Hook 配置示例

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .codex/hooks/check_prompt_for_secrets.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .codex/hooks/log_bash_use.py",
            "statusMessage": "Recording command use"
          }
        ]
      }
    ]
  }
}
```

### 17.4 Hook 信任

非受管 hooks 需要被 review 和信任。不要在团队仓库里随手加入会执行外部脚本的 hook。课程里要教学生看三点：

```text
1. 这个 hook 在什么事件触发？
2. 它会运行什么命令？
3. 它能读取或写入哪些数据？
```

## 18. 配置变更工作流：像改代码一样改配置

配置不是随便贴一段就完事。推荐流程：

```text
1. 先描述配置目标。
2. 只读当前配置和 AGENTS.md。
3. 生成最小变更计划。
4. 修改配置。
5. 新开线程或重启 Codex 验证是否生效。
6. 记录给团队看的变更说明。
```

### 18.1 配置变更 prompt

```text
我想收窄 Codex 在这个项目里的权限。
请先只读查看 AGENTS.md、.codex/config.toml 和相关 rules 文件。
给我一个最小变更方案。
不要直接修改，直到我确认。
```

### 18.2 配置 PR 描述

```md
## Summary

- Add a project-level Codex permission profile.
- Deny `.env*` files.
- Keep generated files read-only.

## Why

- Reduce accidental edits to sensitive and generated files.

## How To Use

- Restart Codex after pulling this change.
- Open a new thread in the project.
```

## 19. 企业受管配置：让默认行为可预期

企业团队不应该靠每个成员手动记住所有安全边界。受管配置可以把一些要求放到组织层。

### 19.1 企业最先管的 6 件事

```text
1. 默认 sandbox 模式。
2. 是否允许 approval_policy = "never"。
3. 哪些 MCP server 可以启用。
4. 插件共享是否允许。
5. Hooks 是否启用或受管。
6. 是否限制 full access。
```

### 19.2 管理员视角的沟通模板

```md
# Codex Managed Config Notice

## What changed

The workspace now uses a managed Codex baseline for permissions and external tools.

## What developers will notice

- Some commands may ask for approval more often.
- Unapproved MCP servers may be disabled.
- Project hooks may need review before running.

## What to do

- Keep project commands in AGENTS.md.
- Request new MCP or plugin access through the team process.
- Do not bypass sandbox settings for convenience.
```

## 20. 配置案例：从个人到团队

### 20.1 个人学习仓库

```text
目标：降低风险，先学会 App。
做法：
- `AGENTS.md` 写项目命令。
- 默认 workspace 权限。
- 不配置复杂 hooks。
- 不接生产 MCP。
```

### 20.2 小团队业务仓库

```text
目标：让每个人用同一套边界。
做法：
- 根目录 `AGENTS.md`。
- 关键子目录补局部 `AGENTS.md`。
- Rules 拦 git push、publish、危险删除。
- MCP 只接只读文档和 PR 上下文。
```

### 20.3 企业平台仓库

```text
目标：可审计、可回滚、可解释。
做法：
- 受管配置约束 sandbox 和审批。
- MCP allowlist。
- Hook trust 流程。
- 插件登记和共享策略。
- 自动化默认只读或 worktree。
```

## 21. 综合工坊：给一个真实项目建立 Codex 基线

这个工坊适合团队一起做。目标是在一个仓库里建立最小但有效的 Codex 使用基线。

### 21.1 第一步：只读盘点

```text
请只读盘点当前项目，为建立 Codex 项目基线做准备。
读取：
- README
- package.json 或项目构建配置
- docs/ 中的开发说明
- 现有 AGENTS.md 或 CLAUDE.md
- .codex/ 目录如果存在

输出：
1. 项目事实
2. 常用命令候选
3. 敏感目录或文件
4. 适合写进 AGENTS.md 的规则
5. 适合用 Rules 管的命令风险
不要修改文件。
```

### 21.2 第二步：生成 `AGENTS.md` 草稿

```text
请根据刚才的盘点生成 AGENTS.md 草稿。
要求：
- 只写当前项目能支持的事实
- 不确定的命令标注为候选
- 不写空泛口号
- 不覆盖现有文件，先输出草稿
```

### 21.3 第三步：写入并 Review

```text
请把确认后的 AGENTS.md 写入项目根目录。
只创建或修改 AGENTS.md。
完成后说明：
- 哪些内容来自 README
- 哪些内容来自 package.json
- 哪些内容是安全边界
```

然后运行：

```text
/review
请审查 AGENTS.md 是否有过度承诺、过期命令或不清楚的安全边界。
```

### 21.4 第四步：增加 Rules

```text
请为这个项目设计最小 rules 策略。
目标：
- git push 需要确认
- force push 拒绝
- publish 需要确认
- 只读 Git 命令允许

先给规则草稿和解释，不要写文件。
```

### 21.5 第五步：复盘

```text
请总结这个项目的 Codex 基线：
1. AGENTS.md 解决了什么
2. Rules 解决了什么
3. 哪些风险还需要权限 profile 或企业配置
4. 新人使用这个项目时第一条 prompt 应该怎么写
```

## 22. 配置冲突案例库

### 22.1 `AGENTS.md` 和实际命令冲突

现象：

```text
AGENTS.md 写 `npm test`，但项目实际使用 `pnpm test`。
```

修复 prompt：

```text
请核对 AGENTS.md 中的命令是否和 package.json、lockfile、README 一致。
只修改 AGENTS.md 中明显过期的命令。
不改 package.json。
```

### 22.2 Rules 太宽导致误拦

现象：

```text
所有 git 命令都被 prompt，连 git status 都很烦。
```

修复思路：

```python
def prefix_rule(argv):
    if argv[:2] in [["git", "status"], ["git", "diff"], ["git", "log"]]:
        return "allow"
    if len(argv) >= 2 and argv[0] == "git" and argv[1] == "push":
        return "prompt"
    return None
```

### 22.3 Hooks 太慢

现象：

```text
每次工具调用后都要等很久。
```

排查 prompt：

```text
请只读检查 Codex hooks 配置。
帮我找出：
1. 哪些 hooks 触发太频繁
2. 哪些脚本可能耗时过长
3. 哪些检查应该改到 Stop 或人工命令里
4. 哪些 hook 可以先禁用
```

### 22.4 项目级配置和用户级配置冲突

现象：

```text
同事能用 MCP，我这里看不到。
```

排查 prompt：

```text
请帮我比较项目级和用户级 Codex 配置可能的差异。
重点看：
- MCP server 是否配置在不同层
- 当前项目是否 trusted
- CODEX_HOME 是否不同
- App 和 WSL CLI 是否使用不同 home
```

## 23. 权限设计练习

### 23.1 文档仓库

```toml
[permissions.docs-edit]
extends = ":workspace"

[permissions.docs-edit.filesystem.":workspace_roots"]
"docs/**" = "write"
"README.md" = "write"
"src/**" = "read"
"**/.env*" = "deny"
```

适合：课程、文档、知识库。

### 23.2 应用仓库

```toml
[permissions.app-edit]
extends = ":workspace"

[permissions.app-edit.filesystem.":workspace_roots"]
"src/**" = "write"
"tests/**" = "write"
"docs/**" = "write"
"migrations/**" = "read"
"**/.env*" = "deny"
```

适合：普通业务开发，迁移默认只读。

### 23.3 高敏仓库

```toml
default_permissions = ":read-only"
```

适合：生产配置、基础设施、敏感系统。需要修改时，通过明确流程临时扩大，而不是默认开放。

## 24. 配置进阶常见问题

### Q1：`AGENTS.md` 能不能写“每次都先问我”？

可以，但不要滥用。所有任务都先问会降低效率。更好的写法是：遇到扩大范围、权限提升、外部写操作、删除文件或产品取舍时先问。

### Q2：Rules 会不会让 Codex 变笨？

Rules 不影响推理能力，它影响命令执行策略。好的 Rules 会减少危险动作，坏的 Rules 会制造很多无意义 prompt。

### Q3：Hooks 和 Automations 有什么区别？

Hooks 是 Codex 执行过程中的事件脚本。Automations 是按时间运行的后台任务。一个是事件触发，一个是时间触发。

### Q4：配置改了为什么没生效？

常见原因：需要重启、新线程没刷新、配置层级不对、项目未 trusted、App 和 CLI 使用不同 home、文件路径写错。

### Q5：企业应该让每个项目都写很长的 `AGENTS.md` 吗？

不需要。根基线写通用要求，项目写项目事实，子目录写局部差异。越靠近代码的指令越具体，越上层越稳定。

## 25. 配置基线会议：把口头偏好翻译成规则

团队讨论 Codex 配置时，大家说出来的往往是口头偏好：有人担心命令跑不对，有人担心改动太大，有人担心敏感文件，有人担心文档失真。配置课的重点，是把这些偏好翻译成项目规则。

可以这样收集需求：

```text
- Codex 必须知道哪些命令？
- 哪些目录可以默认修改？
- 哪些目录只能读？
- 哪些操作必须先问人？
- 哪些外部能力需要登记？
- 哪些文档或课程内容需要核对事实？
```

再把它们合并成配置语言：

```md
# Project Instructions

## Commands

- Test:
- Lint:
- Build:

## Scope

- Codex may edit `src/`, `tests/`, and `docs/` when the task asks.
- Do not edit generated files.
- Ask before changing migrations.

## Safety

- Do not read or modify `.env*`.
- Ask before running publish, deploy, or push commands.
- Keep bug fixes small unless the user asks for refactoring.
```

这个过程比直接复制一份模板更重要。模板只能给起点，团队自己的风险和工作方式才决定最终写法。

这个剧本能让课程从“配置字段讲解”升级为“团队协商过程”。

## 26. 配置演进路线

### 26.1 第一天

```text
- 根目录 AGENTS.md。
- 写项目命令。
- 写敏感文件提醒。
- 不上复杂 Hooks。
```

### 26.2 第一周

```text
- 根据真实任务补充 AGENTS.md。
- 加 Rules 拦 push、publish、危险删除。
- 记录常见 prompt。
- 修正过期命令。
```

### 26.3 第一个月

```text
- 拆子目录 AGENTS.md。
- 设计权限 profile。
- 引入只读 MCP。
- 建立 Plugin 和 Automation 登记。
```

### 26.4 企业化

```text
- 受管配置。
- MCP allowlist。
- Hook trust 流程。
- 月度配置复盘。
```

## 27. 配置审查 prompt 库

### 27.1 审查 `AGENTS.md`

```text
请审查 AGENTS.md。
重点看：
1. 命令是否能从项目文件找到依据
2. 是否有空泛口号
3. 安全边界是否清楚
4. 是否把一次性任务写成长期规则
5. 是否遗漏 generated、migrations、env 文件说明
```

### 27.2 审查 Rules

```text
请审查 rules 文件。
重点看：
1. 是否误拦只读命令
2. 是否漏掉 push、publish、force push
3. 是否有过宽 allow
4. 是否容易让正常开发频繁 prompt
```

### 27.3 审查 Hooks

```text
请审查 hooks 配置。
重点看：
1. 触发事件是否合理
2. 命令是否可信
3. 是否会读取敏感文件
4. 是否会拖慢每次工具调用
5. 是否需要 trust review
```

### 27.4 审查 permissions

```text
请审查权限 profile。
重点看：
1. workspace roots 是否正确
2. deny 规则是否覆盖敏感文件
3. generated 是否只读
4. network domains 是否过宽
5. 是否使用了不适合默认的 full access
```

## 28. 配置长案例：把一句“别乱改”翻译成可执行边界

团队常说“让 Codex 别乱改”。这句话本身没有用，因为 Codex 不知道什么叫乱。要把它翻译成三层内容：项目说明、任务边界、硬性限制。

口头规则：

```text
别乱改支付相关代码。
```

第一层，写进 `AGENTS.md`：

```md
## Payment Area

Payment code is high risk.

Before editing files under `src/payment/`, Codex should:
- Explain why the payment area is relevant to the task.
- Prefer read-only analysis first.
- Ask before changing payment flow, billing logic, or migration files.

Do not include payment refactors in unrelated PRs.
```

第二层，在具体 prompt 里收窄：

```text
本次只修 auth redirect。
不要修改 `src/payment/`、billing、checkout 或 migration 文件。
如果你认为这些文件相关，请先停下来说明原因。
```

第三层，用权限或 Rules 管住危险动作：

```text
目标：
- 普通任务默认不碰 payment。
- 需要 payment 修改时，人要明确确认。
- 发布、迁移、push 仍由人执行。
```

这样，“别乱改”就从情绪变成了可执行边界。

再看一句口头规则：

```text
每次都要跑测试。
```

也要翻译：

```md
## Testing

Use the narrowest relevant test first.

Common commands:
- `npm test -- auth`
- `npm test -- checkout`
- `npm run lint`

If tests are not run, explain why and what should be run manually.
Do not claim tests passed without command output.
```

prompt 里可以写：

```text
修完后运行 auth redirect 相关测试。
如果不能运行，请说明原因和人工验证方式。
不要写“已验证”，除非你真的看到命令结果。
```

配置课程要训练的不是"多写规则"，而是把含糊偏好翻译成 Codex 能执行、团队能检查的语言。

## 29. 配置冲突长案例：AGENTS.md、Rules、prompt 谁说了算

真实项目里经常出现这种冲突：

```text
AGENTS.md：修改 generated 文件前必须确认。
当前 prompt：帮我更新所有生成文件。
Rules：禁止运行 broad formatter。
Codex 计划：运行 format all 并更新 generated。
```

这时不要让 Codex 猜。先让它解释冲突：

```text
请只读分析当前指令冲突。

已知：
1. AGENTS.md 要求修改 generated 文件前确认。
2. 当前 prompt 要更新所有生成文件。
3. Rules 限制 broad formatter。

请输出：
1. 哪些动作可以直接做。
2. 哪些动作需要确认。
3. 哪些动作被规则限制。
4. 推荐的安全下一步。

不要修改文件。
```

安全下一步通常是：

```text
- 先只读列出 generated 文件。
- 说明为什么需要更新。
- 请求用户确认具体文件范围。
- 不运行 broad formatter，只运行 narrow command。
```

然后改 prompt：

```text
只更新以下 generated 文件：
- src/generated/api-types.ts

不要运行全项目 formatter。
不要更新其他 generated 文件。
修改后说明生成来源和验证方式。
```

配置冲突不是坏事，它暴露了团队边界。课程里要让读者学会停下来处理冲突，而不是把所有规则都塞进更长的 prompt。

## 30. 配置复盘：一次失误之后怎样改规则

假设 Codex 在一次 README 更新中顺手改了 `package.json` scripts。团队不应该只说“下次注意”。应该复盘它为什么发生。

复盘 prompt：

```text
请只读复盘这次 Codex 改动越界。

背景：
- 目标是更新 README 安装说明。
- 实际 diff 包含 package.json scripts 修改。

输出：
1. prompt 里哪里没有限制清楚。
2. AGENTS.md 是否缺少边界。
3. 是否需要 Rules 或权限限制。
4. 下次同类任务应该怎么写 prompt。
5. 不要修改文件。
```

可能的规则补充：

```md
## Documentation-Only Tasks

When the user asks for documentation-only edits:
- Do not modify package files.
- Do not modify source code.
- If a doc command appears wrong, report it first instead of changing scripts.
```

下次 prompt：

```text
只更新 README 安装说明。
不要修改 package.json、lockfile、源码或配置。
如果发现 README 命令和 package scripts 不一致，只报告不修改。
```

这就是配置演进：不是预先写一本巨大的规则书，而是从真实失误里提炼短规则。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 已为当前项目编写AGENTS.md（项目说明、命令、风格、禁止事项）
- [ ] 知道App Settings、当前线程权限提示和当前 `/` 列表是权限管理入口
- [ ] 理解read-only、workspace-write、danger-full-access三种沙盒模式
- [ ] 知道config.toml适合团队统一配置，新手先不需要
- [ ] 能区分Rules（命令策略）和Hooks（事件脚本）
- [ ] 每次改完配置都做过核对

**全部勾选后即掌握 Codex 权限与配置。**

---

## 附录

### A. 配置层级速查

| 配置项 | 适合谁 | 入口 |
|--------|--------|------|
| `AGENTS.md` | 所有用户 | 项目根目录/子目录 |
| App Settings | 所有用户 | App界面 |
| 权限入口 | 所有用户 | App Settings、线程权限提示或当前 `/` 列表 |
| `config.toml` | 团队/高级 | `.codex/config.toml` |
| Rules | 团队 | `.codex/rules/*.rules` |
| Hooks | 高级/企业 | `.codex/hooks.json` 或 `.codex/config.toml` 中的 `[hooks]` |

### B. AGENTS.md最小模板

```markdown
# AGENTS.md

这份文件约束 Codex 在本项目里的工作方式。

参考来源：https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md

## 项目背景

开始修改前，先阅读 README、配置文件和目录结构，确认项目目标、技术栈和关键目录；不要凭经验猜。

## 常用命令

只写本项目已经确认过的真实命令。不要保留示例命令或占位文本。

## 1. 写代码前先想清楚

- 先确认需求、影响范围和验证方式。
- 信息不足时先问，不根据经验猜项目规则。
- 有多种方案时，先说明权衡，再选择适合当前任务的方案。

## 2. 简单优先

- 只实现当前任务需要的内容。
- 不主动新增框架、依赖、配置项或抽象层。
- 能用小改动解决，就不用大改动。

## 3. 外科手术式修改

- 保持改动集中，不顺手重构无关代码。
- 优先使用项目已有写法。
- 不统一格式化无关文件。
- 发现无关问题可以说明，不直接处理。

## 4. 目标驱动执行

- 复杂任务先拆成可检查的小步骤。
- 每一步都写清楚验证方式。
- 计划不成立时先说明原因，再调整。

## 安全边界

- 不读取 `.env*`。
- 不提交密钥、Token、证书。
- 不编辑生成文件，除非任务明确要求。

## 验证要求

- 改源码后运行相关测试；无法运行时说明原因。
- 最终回复说明改了什么、验证了什么、还剩什么风险。

## 这些规则生效时应该看到

- diff 能清楚对应本次需求。
- 无关改动少。
- 结果有测试或检查步骤支撑。
```

### C. 推荐学习资源

- **Codex App Settings 官方文档**：https://developers.openai.com/codex/app/settings
- **Codex CLI Reference 官方文档**：https://developers.openai.com/codex/cli/reference
- **本系列上一篇**：[CX-03 Commands](./CX-03-Codex-Commands工作流入口完整指南.md)
- **本系列下一篇**：[CX-05 MCP 外部工具](./CX-05-Codex-MCP外部工具完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-05 MCP：在 App 中连接外部工具](./CX-05-Codex-MCP外部工具完整指南.md)。
