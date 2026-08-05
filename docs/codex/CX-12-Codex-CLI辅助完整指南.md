# CX-12 Codex CLI 辅助指南：App 用户什么时候需要终端

主要来源：OpenAI Codex CLI、CLI Slash Commands、Config、MCP、Review 官方文档。

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
> - **信息来源**：OpenAI Codex CLI、CLI Slash Commands、Config、MCP、Review 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **理解CLI的定位**：CLI是App的辅助工具，不是普通用户的第一入口
2. **掌握CLI常用命令**：`codex --help`、`codex exec`、`codex review`、`codex mcp list`
3. **理解审批与沙盒参数**：`--ask-for-approval`和`--sandbox`的组合使用
4. **使用`codex exec`无头执行**：在CI和脚本中运行一次性只读任务
5. **使用`codex review`终端审查**：快速检查当前diff，与App Review交叉验证
6. **掌握CLI slash commands**：`/status`、`/permissions`、`/plan`、`/compact`等常用命令
7. **用CLI排查MCP和Plugin marketplace**：排查工具配置、浏览插件目录、管理 marketplace 来源
8. **理解CI安全原则**：最小权限、外部沙箱、不输出密钥、明确范围、人工合并

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 10分钟）

**适合人群**：想知道CLI能干什么

**只看这些章节**：

```
✅ 第1-2部分：CLI定位 + 常用命令（5分钟）
✅ 第4部分：codex exec（5分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：需要用CLI做CI或排查

**学习顺序**：从头到尾所有章节

---

## 术语表（小白必读）

CLI 是 App 的辅助，不是“更高级才算会用”。先分清它的几个入口：

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| `codex` | 进入终端交互 TUI | slash commands 和 App 不完全一样 |
| `codex exec` | 无头执行一次任务 | 适合 CI、脚本和只读报告 |
| `codex review` | 终端审查当前 diff | 辅助 App Review，不替代面板 |
| `codex mcp` | 管理 MCP server | 配完仍要回 App 核对 |
| `/plugins` | CLI TUI 里的插件目录入口 | 不是 shell 子命令 |
| `plugin marketplace` | 管理 marketplace 来源 | 管来源，不是普通插件列表 |
| `--sandbox` | 指定命令执行边界 | 不知道就保守 |
| `--ask-for-approval` | 指定审批策略 | 不要默认 `never` |
| `--profile` | 选择 permission profile | 团队配置时很重要 |
| `codex doctor` | 诊断环境、Git、终端、app-server 等 | 排障优先跑 |

## 0. CLI 的三种使用模式

老金我讲 CLI 时会不断提醒：它是 App 主线的补充，不是让新手一开始就掉进终端细节。

```text
交互模式：codex
  -> 适合终端里长期协作、排查、使用 slash commands

无头模式：codex exec
  -> 适合 CI、脚本、一次性报告、结构化输出

专项命令：codex review / codex mcp / codex plugin marketplace
  -> 适合审查、工具配置和插件来源管理
```

App 用户不用一开始学完整 CLI。正确路径是：App 主线遇到“配置、CI、远程、排障”问题，再回到 CLI。

### 0.1 什么时候必须看 CLI

| 场景 | 为什么看 CLI |
|---|---|
| App 看不到 MCP | `codex mcp list` 可辅助确认配置 |
| CI 想跑一次性审查 | App 不适合无头运行 |
| 远程服务器或 Linux | 没有桌面 App 主线 |
| 权限 / profile 排障 | `codex doctor`、`--profile` 更直接 |
| 插件 marketplace 来源 | 需要 `codex plugin marketplace ...` |
| 自动化需要 JSON | `codex exec --output-schema` 适合脚本 |

### 0.2 CLI 安全心智模型

CLI 离 Git、shell、CI 更近，所以更要保守：

1. 默认只读或 workspace-write。
2. `danger-full-access` 只在外部隔离环境用。
3. CI token 只给必要仓库权限。
4. `codex exec` prompt 里写清“不要修改文件”。
5. 命令输出和日志不要打印 secret。

## 1. CLI 的定位


> **v0.141.0 CLI 辅助基线**：CLI 仍服务 Codex App 主线。v0.139.0 增强 code mode web search、MCP schema、doctor 诊断和 plugin marketplace；v0.140.0 增加 `/usage`、`/goal` 大文本 / 图片、`/import`、`codex delete` / `/delete`、统一 `@` mentions 和加密凭证；v0.141.0 强化远程执行 E2E relay、native cwd / shell / permission path 保留、executor plugin stdio MCP、PostToolUse blocking、插件路由、Windows sandbox stale credentials 与企业代理 TLS 修复。安装方式以官方 CLI 文档为准，不再只写 npm。

CLI 是 App 的辅助工具，适合：

- 排查配置。
- 管理 MCP。
- 在 CI 中无头执行。
- 终端中快速 review。
- 用脚本批处理。
- Linux 或远程服务器环境。

不适合：

- 作为普通 App 用户的第一入口。
- 替代 App Review 面板。
- 让新手先背所有参数。

## 2. 常用命令

```bash
codex --help
codex
codex app
codex exec "summarize this repo"
codex review
codex mcp list
codex features
codex plugin marketplace list
```

插件目录在 CLI 交互界面中打开：运行 `codex` 后输入 `/plugins`。

App 用户学习 CLI 的顺序：

1. 先会用 `codex --help` 看本机支持项。
2. 再会用 `codex app` 从终端打开或配合 App。
3. 需要无头任务时再学 `codex exec`。
4. 需要审查时再学 `codex review`。
5. 需要排查外部工具时再学 `codex mcp`、CLI `/plugins` 和 `codex plugin marketplace ...`。

不要先背参数表。CLI 版本变化快，本机 `--help` 比教程里的静态列表可靠。

### 2.1 v0.129.0 到 v0.141.0：先用本机命令确认差量

这几版变化集中在 CLI 可观测性、远程执行、权限配置和 SDK，而不是“多背几个参数”。升级后先做四个确认：

```bash
codex --version
codex doctor
codex remote-control --help
codex plugin marketplace list
codex --help
```

重点看这些能力是否已在你本机暴露：

| 版本段 | 你应该确认什么 | 教程里的使用方式 |
|---|---|---|
| v0.129.0 | `/vim` composer、默认 Vim mode、`/keymap debug`、workspace plugin sharing、`/hooks` 浏览与开关 | 输入体验、插件共享和 hooks 排查都先用内置入口确认 |
| v0.130.0 | `codex remote-control` 顶层入口、plugin share metadata / discoverability、live thread config refresh、thread pagination、Windows sandbox runtime cache | 远程控制、插件分享和 App server 排查时先看 readiness / config 是否刷新 |
| v0.131.0 | TUI session controls、`@` mentions 搜索文件 / 目录 / plugins / skills、`codex doctor` | 交互模式先用 `/help` 和 `@` 试搜索，不要手写路径 |
| v0.132.0 | Python SDK 认证、`codex exec` 结构化输出、remote executor 标准认证、图片 fidelity、session picker | 自动化任务需要结构化输出时优先查 `codex exec --help` 和 `--output-schema` |
| v0.133.0 | Goals 默认启用、permission profiles list / inheritance / managed `requirements.toml`、plugin discovery、extension lifecycle events | 把 `/goal`、权限 profiles、插件排查当成稳定教学入口 |
| v0.134.0 | 本地会话历史搜索、`--profile` 主选择器、MCP per-server environment / streamable HTTP OAuth、read-only MCP 并发、extension / hook 上下文增强 | 迁移旧 profile 配置，排查 MCP 时先看 server environment 和 OAuth 选项 |
| v0.135.0 | `codex doctor` 环境/Git/终端/app-server/thread 诊断、远程 `/status`、named permission profiles、Vim text object、Python SDK `Sandbox` presets、非交互安装 | 支持工单排查、CI 安装和 SDK 自动化时优先用新版诊断和 preset |
| v0.136.0 | TUI 链接和表格可读性、session archive、app-server stdio / MCP status、remote execution 注册、Windows sandbox setup alpha | 先用 `codex doctor`、archive 和 app-server 诊断收敛问题，不把远程执行当新手入口 |
| v0.137.0 | F13-F24 / paste / reasoning-only 状态、cloud-managed config、remote-control grants、plugin JSON、parallel web/image/code-mode、多 agent v2 元数据 | 企业配置、插件排查和远程控制要先看结构化输出和当前配置来源 |
| v0.138.0 | `/app` 交接到 Codex Desktop、图片文件路径暴露、personal access token v2、plugin add/remove / marketplace `--json`、goal/TUI/config/启动修复 | CLI 可以把排查线程带回 App；插件自动化和 CI 报告优先用 JSON 证据 |
| v0.139.0 | code mode web search、MCP schema oneOf / allOf 保留、doctor editor / pager 诊断、plugin marketplace JSON / cache | 排查 MCP、插件和终端体验时先用 doctor 和 marketplace 列表确认本机状态 |
| v0.140.0 | `/usage`、`/import`、`/delete` / `codex delete`、统一 `@` mentions、加密 Bedrock / API / MCP OAuth 凭证 | CLI 迁移、用量查看和敏感凭证管理进入辅助路径 |
| v0.141.0 | 远程执行 E2E relay、native cwd / shell / permission path 保留、executor plugin stdio MCP、PostToolUse blocking、Windows sandbox 修复 | 远程执行、code mode hooks、企业代理和 Windows 排障时优先核对本机版本 |

这些版本还补了很多“看起来小、实际影响学习体验”的 TUI 和启动修复：链接、表格、取消提示、目标续跑、配置错误展示、OAuth/MCP 刷新和 workspace instruction 加载都更稳。写教程和排障时，不需要让新手背每个变更，但要解释“为什么升级后终端界面、App handoff 和插件排查突然更稳了”。

## 3. 审批与沙盒


CLI 常见参数：

```bash
codex --ask-for-approval on-request --sandbox workspace-write
codex --ask-for-approval never --sandbox read-only
```

危险模式只用于外部已经隔离的一次性环境：

```bash
codex --dangerously-bypass-approvals-and-sandbox
```

不要把危险模式写成团队默认推荐。

如果你不知道该选什么，App 用户默认做法是：

| 场景 | 建议 |
|---|---|
| 只读分析 | read-only / 需要审批 |
| 小范围改 docs | workspace-write / 明确目录 |
| 跑测试 | 允许普通命令，危险命令仍审批 |
| CI runner | 只给 PR diff 或目标目录 |
| 一次性隔离环境 | 才考虑无审批无沙盒 |

## 4. `codex exec`

无头执行一次任务：

```bash
codex exec "read the repo and summarize test commands"
```

适合：

- CI。
- 脚本化只读分析。
- 生成报告。

不适合：

- 需要频繁交互的大改。

一个更清楚的无头任务示例：

```bash
codex exec "Read package.json and AGENTS.md. Report the install, test, lint, and build commands. Do not modify files."
```

### 4.1 结构化输出和恢复会话

需要让无头任务返回可校验 JSON 时，优先使用当前 `codex exec --help` 中显示的 `--output-schema` 能力：

```bash
codex exec \
  --output-schema ./schemas/audit-result.schema.json \
  "Read package.json and return only schema-valid JSON with scripts, packageManager, and risky lifecycle hooks."
```

`codex exec resume` 适合恢复旧的非交互任务上下文。是否能和 `--output-schema` 组合，以你本机 `codex exec resume --help` 为准；教程不要把组合参数写成所有版本都可用。

## 5. `codex review`


终端审查当前改动：

```bash
codex review
```

适合：

- CI PR 审查。
- 本地提交前快速检查。
- 与 App Review 交叉验证。

## 6. CLI slash commands

终端交互模式中可以输入 `/help` 查看当前 slash commands。不要把命令表写死；以当前 CLI 为准。

App 用户重点掌握：

- `/status`
- `/permissions`
- `/plan`
- `/goal`
- `/review`
- `/mcp`
- `/plugins`
- `/compact`
- `/resume`

如果这些命令没有出现在你本机 `/help`，以本机输出为准，不要按教程硬敲。

### 6.0 `/vim` 和键盘排查

v0.129.0 起，CLI TUI composer 支持 `/vim`。如果你习惯 Vim，可以在当前会话里开启 modal editing；团队教程不要默认要求所有人开 Vim mode，因为新手会被 Normal / Insert 模式卡住。

键盘快捷键异常时先用：

```text
/keymap debug
```

它适合排查终端是否正确上报组合键，不适合写进普通工作流步骤。

### 6.1 `/goal`、`@` mentions 和 session picker

v0.133.0 起 Goals 默认启用，并有专用存储追踪 active turns 之间的进度。写 `/goal` 时要给明确停止条件：

```text
/goal Finish the docs link audit. Stop when every broken local link has either been fixed or listed with a reason.
```

v0.131.0 起，`@` mentions 搜索范围更宽，能覆盖文件、目录、plugins 和 skills。路径不确定时，优先在 TUI 里输入 `@` 搜索，而不是复制一长串容易出错的路径。

session picker 在 v0.132.0 后更适合恢复旧线程：重命名线程会显示 `name (thread-id)`，粘贴文本也能用于搜索。找不到旧任务时，先用 picker 搜标题关键词，再决定是否用 `codex exec resume`。

## 7. CLI 管理 MCP / Plugins

当 App 中看不到工具或需要团队统一配置时：

```bash
codex mcp --help
codex
# 在交互界面输入 /plugins
```

排查插件时不要只问“装没装”，还要看它来自哪个 marketplace、当前 marketplace 是否可见、插件是否已在 App / CLI 插件目录里启用。marketplace 管理命令的完整清单见 CX-07，本篇只负责说明 CLI 在 App 主线里的辅助排障角色。

CLI 是管理和排查路径，不是普通用户调用外部工具的唯一方式。

CLI 改完 MCP 或插件 marketplace 后，仍要回 App 核对：

1. App 里能否看到工具或插件。
2. 线程中能否调用。
3. 权限提示是否符合预期。
4. 是否能撤销或禁用。

## 8. `codex remote-control` 最小排查流程

v0.130.0 新增顶层 `codex remote-control` 入口，v0.133.0 又把它前台化并增加 readiness 反馈。排查时不要只看“命令有没有返回”，按这个顺序：

```bash
codex remote-control --help
codex remote-control
```

启动后确认三件事：

1. 终端显示 ready 或 machine status。
2. App / 远端客户端能看到同一台机器。
3. 退出前明确停止前台进程，避免误以为它是后台 daemon。

如果你需要长期后台服务，优先查当前 App server / Remote Connections 官方文档，不要把 `remote-control` 当成无监督系统服务。

## 9. 课堂工坊：三个 CLI 辅助场景

### 案例一：只读诊断仓库命令

目标：用 CLI 快速读项目，不修改文件。

```bash
codex exec "Read package.json, README, and AGENTS.md. Report install, test, lint, and build commands. Do not modify files."
```

你应该看到：输出能说明命令来源；工作区没有新增 diff。适合 CI 或远程服务器上做一次性诊断。

### 案例二：结构化输出给脚本使用

目标：让 `codex exec` 输出机器可读 JSON。

```bash
codex exec \
  --output-schema ./schemas/repo-commands.schema.json \
  "Return install, test, lint, build commands as schema-valid JSON. Do not modify files."
```

如果当前 CLI 不支持 `--output-schema`，先用 `codex exec --help` 确认本机版本，不要硬套教程参数。

### 案例三：插件排查从 `/plugins` 到 marketplace

目标：确认插件目录和 marketplace 来源。

1. 运行 `codex` 进入 CLI 交互界面。
2. 输入 `/plugins` 浏览插件目录。
3. 如需管理 marketplace 来源，再退出或另开终端运行：

```bash
codex plugin marketplace list
codex plugin marketplace upgrade
```

你应该看到：插件目录用于安装、启用、查看插件；`codex plugin marketplace ...` 用于管理 marketplace 来源，不等于普通插件列表。

## 10. CI 安全原则

| 原则 | 说明 |
|---|---|
| 最小权限 | CI token 只给需要的仓库权限 |
| 外部沙箱 | 无沙盒模式只在 runner 自身可信时使用 |
| 不输出密钥 | 日志中不得打印 secret |
| 明确范围 | 只审查 PR diff 或指定路径 |
| 人工合并 | 自动评论可以，自动合并要慎重 |

### 10.1 CI 中的最小安全模板

```bash
codex exec \
  --sandbox read-only \
  --ask-for-approval never \
  "Review the current PR diff for correctness, security risks, and missing tests. Do not modify files. Return findings and verification gaps."
```

这只是形状示例。真实 CI 要结合 runner 权限、checkout 范围、token scope、日志脱敏和组织策略。

### 10.2 CLI 排障表

| 症状 | 先跑什么 | 常见原因 |
|---|---|---|
| CLI 命令不存在 | `codex --version`、`codex --help` | 版本过旧或未安装 |
| App 能用但 CLI 不行 | `codex doctor` | PATH、认证、终端、profile 差异 |
| MCP 配置不生效 | `codex mcp list`、`codex mcp --help` | 配置层、server 启动、token |
| `/plugins` 找不到 | 先进入 `codex` TUI | 它是交互命令，不是 shell 子命令 |
| 结构化输出失败 | `codex exec --help` | 当前版本或 schema 不支持 |
| 权限行为不对 | 查看 `--profile`、sandbox、approval | profile 继承或 managed requirements |
| CI 日志泄露信息 | 查 prompt、命令、环境变量 | 禁止 echo secret，轮换凭据 |

## 11. CLI Runbook：四个常用排障场景

### 11.1 App 看不到 MCP

```bash
codex mcp list
codex mcp --help
codex doctor
```

然后回到 App：

1. 重启或刷新 App。
2. 打开目标项目线程。
3. 输入 `/mcp`。
4. 做一个只读工具调用。

CLI 看到配置只是中间证据，App 线程能调用才算主线可用。

### 11.2 CI 里做只读 Review

```bash
codex exec \
  --sandbox read-only \
  --ask-for-approval never \
  "Review the current diff for bugs, security risks, and missing tests. Do not modify files."
```

CI 中不要默认让 Codex 写代码、提交或 push。先把它当成高信号 reviewer。

### 11.3 权限 profile 排查

```bash
codex doctor
codex --help
codex --profile read-only
```

如果团队使用 managed requirements，个人 CLI 参数可能会被组织策略限制。看到行为和本机参数不一致时，先查 managed 配置，而不是反复改命令。

### 11.4 插件 marketplace 排查

```bash
codex
# 在 TUI 输入 /plugins

codex plugin marketplace list
codex plugin marketplace upgrade
```

区分两件事：

- `/plugins` 用于浏览和管理插件体验。
- `codex plugin marketplace ...` 用于管理 marketplace 来源。

不要把 marketplace 来源管理当成普通插件调用。

## 常见问题

### Q1：App 用户不装 CLI 可以吗？

可以，但排查和 CI 会不方便。建议安装，但不先学。

### Q2：CLI 和 App 的配置完全共享吗？

不要做绝对假设。看当前版本和官方文档。能通过 App 设置解决的，优先用 App。

### Q3：CLI 能替代 Automations 吗？

不能完全替代。CLI 适合脚本和 CI；App Automations 是 App 内的后台/周期任务体验。

### Q4：为什么教程不把 CLI 作为第一课？

因为本系列目标是 Codex App 主线。CLI 很强，但新手更容易在终端权限、路径、shell、Git 状态里迷路。先学 App Review 和权限，再学 CLI 更稳。

### Q5：为什么不写一个普通的插件列表 shell 命令？

当前插件目录主入口是在 CLI 交互界面输入 `/plugins`，marketplace 来源管理使用 `codex plugin marketplace ...`。不要臆造不存在或过时的 shell 命令。

### Q6：`codex exec` 适合直接改代码吗？

可以，但新手不建议。无头任务缺少交互反馈，更适合只读分析、结构化报告、CI review。要改代码，优先 App 或交互模式。

### Q7：CLI 输出和 App Review 冲突时信哪个？

先回到 Git diff 和真实命令输出。CLI review 是一个审查视角，App Review 是本地 diff 工作台；最终以文件、测试、PR 和人工判断收口。

---

## 12. CLI 深入：App 用户为什么还要懂一点终端

本系列把 App 当主线，但 CLI 仍然重要。CLI 适合做三类事：

| 类型 | 例子 |
|------|------|
| 诊断 | `codex doctor`、版本、配置、MCP |
| 自动化 | `codex exec`、CI、脚本 |
| 远程/高级 | app-server、remote-control、sandbox |

App 用户学 CLI 的目标不是回到纯终端工作流，而是知道什么时候该从 App 切到命令行。

## 13. CLI 命令地图

常见命令可以按用途分：

| 命令 | 作用 |
|------|------|
| `codex` | 打开交互式 TUI |
| `codex app` | 启动桌面 App |
| `codex login` / `logout` | 认证 |
| `codex doctor` | 本地诊断 |
| `codex exec` | 非交互执行 |
| `codex review` | CLI review |
| `codex mcp` | MCP 管理 |
| `codex plugin marketplace` | marketplace 管理 |
| `codex remote-control` | 本地 app-server 远程控制辅助 |
| `codex sandbox` | 在 Codex sandbox 中跑命令 |
| `codex apply` | 应用 Cloud 任务 diff |

学习时不用一口气背完。先掌握 `doctor`、`exec`、`mcp`、`review` 四类。

## 14. `codex doctor`：先诊断，不先重装

遇到 App 或 CLI 异常时，`doctor` 比猜测更好。

```bash
codex doctor
```

它适合检查：

```text
- 本地安装。
- 配置。
- 认证。
- 运行时。
- Git。
- terminal。
- app-server。
- thread inventory。
```

### 14.1 doctor 后怎么问 Codex

```text
下面是 `codex doctor` 的输出。
请帮我判断：
1. 哪些是必须处理的问题
2. 哪些只是提示
3. 先修哪一个
4. 是否影响 App、CLI、MCP 或认证
不要让我粘贴任何密钥。
```

## 15. `codex exec`：脚本里的 Codex

`codex exec` 是非交互模式，适合 CI、脚本和一次性自动化。它默认更适合明确任务，不适合开放式聊天。

### 15.1 基本用法

```bash
codex exec "summarize the repository structure and list the top 5 risky areas"
```

### 15.2 管道输入

```bash
npm test 2>&1 |
  codex exec "summarize the failing tests and propose the smallest likely fix"
```

### 15.3 JSONL 输出

```bash
codex exec --json "summarize the repo structure" | jq
```

JSONL 适合脚本消费，因为你能看到 thread、turn、command execution、file changes、MCP tool calls 等事件。

### 15.4 结构化输出

```bash
codex exec "Extract project metadata" \
  --output-schema ./schema.json \
  -o ./project-metadata.json
```

这适合自动化报表、风险摘要、release metadata。不要把结构化输出当成“事实自动正确”，仍然要看输入质量和任务边界。

### 15.5 恢复非交互会话

```bash
codex exec "review the change for race conditions"
codex exec resume --last "fix the race conditions you found"
```

如果要指定 session：

```bash
codex exec resume SESSION_ID
```

## 16. `codex exec` 权限安全

官方文档强调，自动化里要显式设置最小权限。

```bash
codex exec --sandbox read-only "summarize this repo"
codex exec --sandbox workspace-write "update README install instructions"
codex exec --sandbox danger-full-access "run this in an isolated container only"
```

### 16.1 CI 里不要泄露 API Key

不要把 API key 作为 job-level 环境变量暴露给所有步骤。更安全的做法是：

```text
- 用 Codex GitHub Action。
- 或只在单次 `codex exec` 调用环境里提供。
- 不让 untrusted code 和 key 处在同一进程环境。
```

### 16.2 CI prompt 示例

```text
The CI workflow failed for this commit.
Run the targeted test command if available.
Identify the smallest likely fix.
Do not refactor unrelated files.
If the failure cannot be reproduced, summarize the missing evidence.
```

## 17. `codex mcp`：CLI 管理 MCP 的辅助入口

App 和 CLI 共享 MCP 配置。CLI 适合快速添加和排查。

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp --help
```

在 TUI 中：

```text
/mcp
```

### 17.1 MCP 排查命令思路

```text
1. 看 config.toml 是否有 server。
2. 看 server command 是否能本机启动。
3. 看 token 环境变量是否存在。
4. 看 App/CLI 是否同一 CODEX_HOME。
5. 新开线程确认能力是否刷新。
```

## 18. `codex plugin marketplace`：管理插件来源，不是列插件按钮

CLI 中 marketplace 管理命令的完整清单放在 [CX-07 Plugins / Connectors](./CX-07-Codex-Plugins连接器完整指南.md)。本篇只记住一句：这里管理的是 marketplace 来源，不是普通插件开关；排查时优先跑 `codex plugin marketplace list` 看当前来源。

浏览和启用插件的常规入口仍然是 App Plugins 页面或 CLI TUI 的：

```text
/plugins
```

### 18.1 本地 marketplace 排查

```text
请帮我排查本地 Codex plugin marketplace。
我会提供 marketplace.json 和目录结构。
请检查：
1. source.path 是否相对 marketplace root
2. 插件是否有 `.codex-plugin/plugin.json`
3. 是否需要重启 Codex
4. 是否应该从 App Plugins 页面或 `/plugins` 查看
```

## 19. `codex review`：终端里的审查入口

CLI review 适合在没有 App Review 面板时做快速审查，或者在 CI 里生成 review 摘要。

```bash
codex review
```

更好的任务描述：

```bash
codex review "Focus on correctness, security, behavior regressions, and missing tests."
```

App 用户要记住：CLI review 可以补充 App Review，但不能替代你在 App 里看 diff、stage、revert 和 inline comments。

## 20. `codex remote-control` 与 app-server

Remote control 和 app-server 属于高级辅助能力。课程里只需要建立概念：

```text
- app-server 是本地 App 相关的服务入口。
- remote-control 帮助确保本地 app-server daemon 以远程控制支持运行。
- 这不是新手第一天要用的功能。
- 涉及网络监听和 token 时，要格外注意安全边界。
```

排查 prompt：

```text
我在排查 Codex remote-control / app-server。
请先解释当前命令会打开什么本地服务、监听范围是什么、是否需要认证 token。
不要建议我暴露到公网。
```

## 21. Windows CLI 特别注意

Windows 上 CLI 和 App 可能面对两个世界：Windows 原生和 WSL。

### 21.1 CODEX_HOME 差异

Windows App 使用：

```text
%USERPROFILE%\.codex
```

WSL CLI 默认使用 Linux home 下的：

```bash
~/.codex
```

如果你想共享配置，可以设置：

```bash
export CODEX_HOME=/mnt/c/Users/<you>/.codex
```

不要盲目共享。先确认你确实需要 App 和 WSL CLI 共享 auth、config、sessions。

### 21.2 PowerShell 与 Bash 命令差异

```powershell
Get-ChildItem
where.exe git
$env:CODEX_HOME
```

```bash
ls
which git
echo "$CODEX_HOME"
```

课程里给命令时要标清 Windows PowerShell 还是 Bash，避免学生直接复制失败。

## 22. CLI 与 App 的配合案例

### 22.1 用 CLI 生成诊断，App 解释

```bash
codex doctor > codex-doctor.txt
```

App prompt：

```text
请读取 codex-doctor.txt。
帮我判断哪些问题会影响 Codex App 使用。
不要修改配置，先给排查顺序。
```

### 22.2 用 CLI 做结构化摘要

```bash
git log --oneline -20 |
  codex exec "group these commits into release note categories" \
  -o release-summary.md
```

App prompt：

```text
请审查 release-summary.md 是否夸大了用户影响。
只改措辞，不改变 commit 事实。
```

### 22.3 用 CLI 管 MCP，用 App 做任务

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

App prompt：

```text
请确认当前线程能否使用文档 MCP。
如果不能，帮我排查配置刷新、项目作用域和工具可见性。
```

## 23. CLI 反模式

| 反模式 | 风险 |
|--------|------|
| 为省事长期 `danger-full-access` | 破坏本地安全边界 |
| 在 CI job-level 暴露 API key | 被构建脚本或依赖读取 |
| 用 CLI 绕过 App Review | diff 没被认真看 |
| 把所有任务都塞进 `exec` | 缺少交互澄清 |
| Windows/Bash 命令混用 | 学生复制失败 |
| 不看 `codex --help` 和当前版本 | 课程命令过期 |

## 24. 综合工坊：用 CLI 做一次只读 CI 日志分析

### 24.1 准备日志

```bash
gh run view 123456 --log > ci.log
```

### 24.2 用 `codex exec` 分析

```bash
cat ci.log |
  codex exec "Summarize the CI failure. Identify the first failing job, likely root cause, and next three debugging steps. Do not propose broad refactors." \
  -o ci-summary.md
```

### 24.3 回到 App

```text
请读取 ci-summary.md。
帮我判断这个失败适合：
1. 本地 App 修
2. Cloud 修
3. 只在 CI 配置里修
4. 需要人工调查
不要修改文件。
```

这个工坊展示 CLI 的定位：处理管道输入，再回 App 做决策和 Review。

## 25. 综合工坊：CLI + App + Cloud 三段式

```text
CLI:
  抓取 CI 日志并生成摘要

App:
  判断任务范围，整理 handoff

Cloud:
  修复可复现失败

App:
  Review diff，准备 PR 描述
```

### 25.1 命令

```bash
gh run view 123456 --log |
  codex exec "Turn this CI log into a concise handoff for a repair task." \
  -o cloud-handoff.md
```

### 25.2 App prompt

```text
请读取 cloud-handoff.md。
把它改写成适合 Codex Cloud 的任务 prompt。
要求范围小、禁止无关重构、包含建议验证命令。
```

## 26. CLI 设计题

### 26.1 题目 A

```bash
codex exec --sandbox danger-full-access "fix everything"
```

判断：不合格。权限过大，任务过泛。

改写：

```bash
codex exec --sandbox read-only "summarize current repo risks and suggest three narrow tasks"
```

### 26.2 题目 B

```bash
npm test 2>&1 | codex exec "summarize failing tests"
```

判断：合格。输入明确，输出只读。

### 26.3 题目 C

```bash
OPENAI_API_KEY=... npm test && codex exec "fix CI"
```

判断：有风险。不要让密钥暴露给不需要它的命令或同一 job 的不可信代码。

## 27. CLI 进阶常见问题

### Q1：`codex exec` 会打开交互界面吗？

不会。它是非交互模式，适合脚本和 CI。

### Q2：`--json` 和 `--output-schema` 有什么区别？

`--json` 输出运行事件流。`--output-schema` 约束最终回答结构。一个偏过程事件，一个偏最终数据。

### Q3：App 用户什么时候必须用 CLI？

很少“必须”。常见需要 CLI 的场景是 CI、脚本、MCP 管理、doctor 诊断、非交互任务。

### Q4：Windows 上 CLI 和 App 配置不一致怎么办？

检查 `CODEX_HOME`，尤其是 Windows 原生和 WSL 是否各用一套 home。

### Q5：CLI 能不能替代 App Review？

不能完全替代。CLI 能审查和输出 diff 信息，但 App Review 的可视化 diff、inline comments、stage/revert 仍然更适合桌面工作流。

## 28. CLI 学习深度：不是每个人都要背完整参数表

CLI 的课程难点不在命令少，而在读者很容易把它学成一张孤立清单。更合理的学法是按使用深度分层：先会排障，再会自动化，最后才碰远程控制和平台集成。

第一层是 App 用户也应该会的命令。它们不替代桌面工作流，只用于诊断和补充。

```text
最低掌握：
- `codex doctor`
- `codex exec` 的只读用法
- `codex mcp` 的查看和诊断
- CLI TUI 里的 `/plugins`
```

练习 prompt：

```text
请用 CLI 辅助我诊断当前 Codex 环境。

目标：
1. 先运行 doctor。
2. 解释输出里哪些会影响 App 使用。
3. 不修改配置。
4. 给出下一步排查顺序。
```

第二层是把 CLI 接进脚本和 CI。这里最重要的不是"会跑"，而是输出可解析、权限可控、密钥不外泄。

```text
需要掌握：
- `codex exec --json`
- `--output-schema`
- sandbox 参数
- API key 暴露风险
- GitHub Action 里的最小权限模式
```

一个典型 CI 场景：

```bash
codex exec --sandbox read-only --json \
  "review this diff for regression risk and output JSON findings only"
```

第三层才是平台工程能力，例如 `app-server`、`remote-control`、`CODEX_HOME`、profile 和 config override。这些内容适合维护内部工具链的人学，不适合塞进每个新手的第一天课程。

课程里可以这样安排节奏：

```text
第 1 次接触 CLI：只讲 doctor 和只读 exec。
第 2 次接触 CLI：讲 mcp/plugin 诊断和 JSON 输出。
第 3 次接触 CLI：讲 CI、安全边界和 schema。
最后再讲 app-server、remote-control 和多环境配置。
```

这能避免一个常见误区：把 CLI 讲得越全，读者越不知道自己今天该用哪一小块。CLI 的好课程应该让读者先有“我能用它解决一个明确问题”的感觉，再逐步扩展到自动化和平台化。

## 29. CLI 作业：把命令改成安全版本

原命令：

```bash
codex exec --sandbox danger-full-access "fix project"
```

要求改成三种安全版本：

```bash
codex exec --sandbox read-only "summarize the project and suggest narrow fixes"
```

```bash
codex exec --sandbox workspace-write "update README install commands only"
```

```bash
npm test 2>&1 |
  codex exec --sandbox read-only "summarize the failing tests and likely root cause"
```

学生要解释每个版本适合的场景。

## 30. CLI 长案例：从 CI 失败日志到 App 里的最小修复

CLI 最适合做“把大量文本变成可执行判断”的工作。下面这个案例不要求 Codex 直接改代码，而是先把 CI 失败日志整理成 App 可以接手的任务。

第一步，把日志交给只读 `exec`。

```bash
npm test 2>&1 |
  codex exec --sandbox read-only "
  Summarize this test failure.
  Output:
  1. failing test names
  2. likely root cause
  3. files to inspect first
  4. smallest next local action
  Do not suggest broad refactors.
  "
```

这个命令的重点是 `--sandbox read-only`。你让它读日志、压缩信息、给下一步。这样即使日志很长，也不会把错误分析和文件写入混在一起。

第二步，把结果带回 App。

```text
我刚用 CLI 分析了 CI 日志，得到：

- failing test: auth redirect preserves callback URL
- likely root cause: redirect helper drops query params
- inspect first: src/auth/redirect.ts, tests/auth-redirect.test.ts

请在 App 里只读确认这些文件是否相关。
不要修改文件，先给我最小修复计划。
```

第三步，App 里再决定是否写代码。

```text
根据刚才的只读计划，执行最小修复。

边界：
1. 只修改 redirect helper 和对应测试。
2. 不改 auth UI。
3. 如果需要改其他文件，先暂停说明原因。
4. 修完后运行相关测试。
```

第四步，回到 CLI 做日志复盘。

```bash
npm test -- auth-redirect 2>&1 |
  codex exec --sandbox read-only "
  Compare this output with the earlier failure.
  Tell me whether the targeted test now passes.
  If it fails, summarize only the remaining failure.
  "
```

这个流程让 CLI 和 App 各做擅长的事：CLI 读长日志、压缩信息；App 承接本地 diff、Review 和人工决策。不要把 CLI 当成 App 的替代品，也不要把 App 当成日志处理器。

## 31. JSON 输出案例：让 `codex exec` 进入脚本，但别让脚本乱改项目

当你想把 Codex 接进脚本时，自然会想到结构化输出。结构化输出适合“判断、分类、摘要”，不适合“自动相信并执行”。

一个只读风险分类示例：

```bash
git diff --stat |
  codex exec --sandbox read-only --json "
  Classify this diff summary into one of:
  docs-only, tests-only, code-low-risk, code-needs-review.
  Return JSON with keys: category, reason, suggested_next_step.
  "
```

脚本可以读取这个 JSON，但不要直接根据 category 自动 push 或 merge。更稳的做法是把结果作为提示：

```text
如果 category 是 docs-only：
- 提示用户仍然打开 Review 面板看 diff。
- 可以建议运行 docs lint。

如果 category 是 code-needs-review：
- 不自动继续。
- 提醒用户回到 App 或 PR review 流程。
```

一个更接近团队使用的 prompt：

```text
Return JSON only.

Schema:
{
  "category": "docs-only | tests-only | code-low-risk | code-needs-review",
  "reason": "short explanation",
  "suggested_next_step": "one concrete next action",
  "needs_human_review": true
}

Rules:
1. If source code files changed, needs_human_review must be true.
2. If auth, payment, permissions, migrations, dependencies, or CI config changed, category must be code-needs-review.
3. Do not claim tests passed unless test output is provided.
```

这段不是为了让 Codex 做最后裁判，而是让脚本输出稳定、可读、可记录。CI 和脚本里的 Codex 越自动，权限越要窄；越想省人工，越要把“人工必须决定的点”写清楚。

## 32. CLI 排障案例：同一个错误，先判断是哪一层

很多 CLI 问题不是 Codex 本身坏了，而是路径、shell、登录、项目状态或配置层级出了问题。不要第一步就重装。

### 32.1 命令在 App 里能跑，CLI 里不能跑

先问：

```text
1. CLI 当前目录是不是同一个项目？
2. Windows 原生和 WSL 是否用了不同 home？
3. `CODEX_HOME` 是否不同？
4. CLI 是否能看到同一份 AGENTS.md？
5. App 的权限设置和 CLI sandbox 是否一致？
```

可用 prompt：

```text
我在 App 里能完成任务，但 CLI 里失败。
请帮我按层排查：
1. 当前目录和项目根目录。
2. 登录状态。
3. CODEX_HOME。
4. AGENTS.md 发现路径。
5. sandbox / approval 设置。

不要修改配置，先列出我应该检查的命令和原因。
```

### 32.2 CLI 能跑，但结果和 App 不一致

这通常是上下文不一致，不一定是模型不一致。先确认：

```text
- App 线程里有没有额外上下文？
- CLI prompt 是否漏了目标、范围、验证命令？
- CLI 是否运行在另一个分支或 worktree？
- 是否有不同的 config profile？
- 是否有项目-local 配置未被信任或未加载？
```

修正 prompt：

```text
请比较我在 App 和 CLI 中给 Codex 的上下文差异。
目标是找出为什么 CLI 输出和 App 不一致。
只分析可能原因，不修改文件。
```

### 32.3 CLI 卡在权限或沙盒

不要直接切到 full access。先把任务拆小：

```text
请把这个 CLI 任务拆成两步：
1. read-only 能完成的信息收集。
2. 需要写权限或外部访问的动作。

每一步说明需要的最低权限。
```

然后分别执行：

```bash
codex exec --sandbox read-only "inspect the project and suggest a narrow fix"
```

等范围清楚后再进入 App 或 workspace-write。课程里要让读者形成一个习惯：CLI 权限越大，prompt 越要具体；prompt 越模糊，sandbox 越要保守。

## 33. CLI 与 Cloud 的边界：远端任务不要从终端一键扔出去

CLI 可以帮助你启动或浏览 Cloud 任务，但 Cloud 任务是否适合远端执行，仍然要先判断。

适合：

```text
- CI 失败可复现。
- 仓库已推到 GitHub。
- setup script 能安装依赖。
- 任务范围能写成 5-10 行。
- 结果能通过 diff 和测试检查。
```

不适合：

```text
- 依赖本机未同步文件。
- 需要访问本地浏览器状态。
- 需要秘密信息在 agent 阶段使用。
- 需要人工不断选择方向。
- 任务描述只有“帮我优化一下”。
```

一个合格的 CLI 到 Cloud handoff：

```bash
codex cloud exec --env ENV_ID "
Fix the failing auth redirect test.

Context:
- Branch contains the failing test.
- Failure: redirect target drops query params after login.
- Relevant files likely include auth redirect helper and auth redirect test.

Constraints:
- Do not refactor auth module.
- Do not add dependencies.
- Return changed files and commands run.
"
```

Cloud 返回后，仍然回到 App 或本地 Review：

```text
请只读审查 Cloud 返回的 diff。
确认：
1. 是否只处理 auth redirect。
2. 是否有无关文件。
3. 测试证据是否足够。
4. 我本地应该再跑什么命令。
```

CLI 的高阶能力不是"更快把任务扔出去"，而是把任务边界写清楚、把结果带回来、把人工判断保留下来。

## 34. CLI 课程案例：把终端输出变成团队知识

CLI 经常出现在排障现场。一个人跑完 `doctor`、测试、lint、review，结果只在自己终端里闪过，团队没有任何沉淀。更好的做法是让 Codex 帮你把终端输出转成可复用知识。

场景：三个人都遇到 Windows 上 CLI 和 App 行为不一致。与其各自排查，不如整理一份团队排障条目。

先收集只读材料：

```text
我会提供几个终端输出摘要。
请帮我整理成团队排障条目。

要求：
1. 不包含 token、用户名、绝对私有路径。
2. 按症状 -> 可能原因 -> 检查步骤 -> 下一步写。
3. 区分 Windows 原生、WSL、PowerShell。
4. 不要建议重装作为第一步。
```

输入摘要示例：

```text
Symptom:
CLI reads different config than App.

Observed:
Windows App opens project under C:\Users\Kim\Projects\repo.
CLI was launched inside WSL path.

Likely:
Different home and config layers.
```

输出成文档：

```md
# Codex CLI/App Config Mismatch

## Symptom

Codex App and CLI behave differently in the same-looking project.

## Likely Cause

The App is using Windows-native paths, while CLI was launched from WSL. Each environment may have different home directories, config, credentials, and project trust state.

## Check

- Confirm exact project path in App.
- Confirm CLI current directory.
- Check whether `CODEX_HOME` differs.
- Confirm which shell is running commands.

## Next Step

Use one environment consistently for the exercise, then document when WSL is intentionally needed.
```

这个案例能把 CLI 从“个人高手工具”变成团队知识来源。每次排障结束，都可以问：

```text
请把这次 CLI 排障整理成一条团队 FAQ。
要求：
1. 一句话症状。
2. 三条检查步骤。
3. 一个不要做的误区。
4. 一个推荐下一步。
```

长期看，这比把所有人都训练成 CLI 专家更有效。团队需要的是可复用的排障路径，而不是每个人都记住所有参数。

## 35. CLI 安全练习：把危险命令拆成两段

很多危险 CLI 用法不是因为命令本身恶意，而是把“分析”和“执行”绑在了一起。

坏命令：

```bash
codex exec --sandbox danger-full-access "find and fix all security issues"
```

拆成第一段，只读：

```bash
codex exec --sandbox read-only "
Inspect the repository for security-sensitive areas.
Output likely risks, files to inspect, and suggested narrow next tasks.
Do not modify files.
"
```

第二段，限定写入：

```bash
codex exec --sandbox workspace-write "
Fix only the hardcoded debug log in src/auth/session.ts.
Do not modify auth flow, dependencies, config, or tests except the matching regression test.
"
```

第三段，再只读审查：

```bash
codex exec --sandbox read-only "
Review the current diff for security regression and scope creep.
Do not modify files.
"
```

课程练习可以让学生把下面的危险任务全部拆成“只读分析 -> 窄写入 -> 只读审查”：

```text
1. fix all tests
2. clean up the whole repo
3. improve auth security
4. update dependencies
5. prepare release
```

这套练习会训练一个核心习惯：CLI 越强，越要把阶段拆开。不要让一个高权限 prompt 同时决定问题、修改文件、证明自己正确。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解CLI是App的辅助，不是主线
- [ ] 掌握`codex exec`无头执行和`codex review`终端审查
- [ ] 知道审批和沙盒参数的组合使用
- [ ] 不把CLI教程写成Codex主线
- [ ] CI中遵循最小权限、不输出密钥、人工合并原则

**全部勾选后即掌握 Codex CLI 辅助。**

---

## 附录

### A. CLI命令速查

| 命令 | 用途 |
|------|------|
| `codex --help` | 查看帮助 |
| `codex` | 交互模式 |
| `codex app` | 打开或配合App |
| `codex exec "任务"` | 无头执行 |
| `codex review` | 审查当前改动 |
| `codex mcp list` | 列出MCP工具 |
| `/plugins` | CLI交互界面中浏览插件目录 |
| `codex plugin marketplace list` | 列出插件 marketplace 来源 |

### B. 推荐学习资源

- **Codex CLI 官方文档**：https://developers.openai.com/codex/cli
- **本系列上一篇**：[CX-11 Web / Cloud 辅助](./CX-11-Codex-Web-Cloud辅助指南.md)
- **本系列下一篇**：[CX-13 安全与企业](./CX-13-Codex安全企业完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-13 安全与企业基线](./CX-13-Codex安全企业完整指南.md)。
