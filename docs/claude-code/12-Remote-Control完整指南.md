# Claude Code Remote Control完整指南：手机、浏览器继续本地会话

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：1-2小时
> - **难度等级**：⭐⭐ 进阶
> - **更新日期**：2026年4月
> - **适用版本**：Claude Code v2.1.150（验证于 2026-05-25）
> - **信息来源**：[Claude Code 官方文档 - Remote Control](https://code.claude.com/docs/en/remote-control)

---

## 本课学习目标

<p align="center"><img src="../../images/official/claude-code-agent-view-dark.png" alt="Claude Code 官方 Agent View 深色界面：Needs input、Working、Completed 分组" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-agent-view.png" alt="Claude Code 官方 Agent View：多后台会话状态" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-product-ui.jpg" alt="Claude Code 官方 CLI 任务界面：任务执行、文件变更与终端状态" width="720"/></p>

完成本课后，你将能：

1. 理解 Remote Control 和 Claude Code on the Web 的区别
2. 正确启动 Remote Control 的三种模式
3. 从手机、平板或浏览器继续本地 Claude Code 会话
4. 理解并发模式、worktree、sandbox 与权限边界
5. 解决 Team / Enterprise 下最常见的启用问题

---

## 1. 先说结论

Remote Control 不是“把你的本地项目同步到云端”，而是：

> 让 `claude.ai/code` 或 Claude 手机 App 变成你本地 Claude Code 会话的远程窗口。

核心特点：

- **会话继续在你的机器上跑**
- **本地文件系统、MCP、配置仍然可用**
- **手机 / 浏览器 / 终端可以同时连同一会话**
- **适合中途离开工位但不想中断当前任务**

---

## 2. 它和 Claude Code on the Web 有什么区别

这是最容易混淆的一点。

| 功能 | Remote Control | Claude Code on the Web |
|------|----------------|------------------------|
| 运行位置 | 你的本地机器 | Anthropic 云端 |
| 文件系统 | 本地真实项目 | 云端克隆 / 沙箱 |
| MCP / 本地工具 | 可直接复用本地环境 | 取决于云端环境 |
| 是否能离开终端继续 | 可以 | 可以，但其实是另一种会话形态 |
| 典型场景 | 我已在本地做了一半，想在手机上继续 | 我想远程开一个新的云端任务 |

如果你已经在终端里干了一半活，想躺沙发继续看、继续发指令，用 **Remote Control**。

如果你想新开一个云端任务，不依赖本地运行环境，用 **Claude Code on the Web**。

---

## 3. 使用前提

> **v2.1.139+ 登录方式限制**：如果当前会话通过 `ANTHROPIC_API_KEY`、`apiKeyHelper` 或 `ANTHROPIC_AUTH_TOKEN` 走 API key / helper 登录，Remote Control、`/schedule`、claude.ai MCP connectors 和 notification preferences 会被禁用。要使用远控和计划能力，优先使用支持这些能力的 Claude.ai 登录路径。

官方当前要求：

- Claude Code **v2.1.51+**
- 使用 **claude.ai 登录**
- 不是 API key 模式
- Team / Enterprise 需要管理员先在后台启用 Remote Control

支持 Remote Control 的订阅计划：**Pro、Max、Team、Enterprise**。

### 3.1 推荐先检查这三件事

```bash
claude --version
```

```text
/login
```

确认你已经至少在项目目录里启动过一次 `claude`，并接受过 workspace trust。

---

## 4. 三种启动方式

## 4.1 方式一：独立服务器模式

这是最纯粹的 Remote Control 方式。

```bash
claude remote-control
```

它会：

- 在当前终端进入 server mode
- 显示一个会话 URL
- 可以按空格显示二维码
- 等待你从别的设备连接

适合：

- 本地不需要继续敲终端
- 就想把这个会话“挂出来”

### 常用参数

```bash
claude remote-control --name "My Project"
```

```bash
claude remote-control --verbose
```

```bash
claude remote-control --sandbox
```

```bash
claude remote-control --spawn worktree
```

这些参数里最值得理解的是：

- `--name`：远端会话标题
- `--spawn same-dir|worktree|session`：并发会话如何创建（默认 `same-dir`）
- `--sandbox / --no-sandbox`：是否启用沙箱
- `--capacity <N>`：最多允许多少个并发会话

在 server mode 运行时，可以按 `w` 键在 `same-dir` 和 `worktree` 之间实时切换。

---

## 4.2 方式二：本地交互会话 + Remote Control

如果你既想保留终端交互，也想让手机或浏览器接入，用这个：

```bash
claude --remote-control
```

或者：

```bash
claude --rc
```

它和 `claude remote-control` 的区别是：

- 你还能继续在本地终端里正常聊天
- 同时又能从远端设备控制同一个会话

---

## 4.3 方式三：在已运行会话里临时开启

如果你已经在 Claude Code 里工作了，不想重启：

```text
/remote-control
```

也可以直接命名：

```text
/remote-control Auth Fix Session
```

这会把当前会话历史一起带过去，并展示：

- 会话 URL
- QR 码

适合：

- 正在做一半才决定“我要换设备继续”

---

## 5. 怎么从别的设备连接

Remote Control 启动后，官方支持三种常见连接方式：

1. **直接打开终端里显示的 URL**
2. **扫 QR 码**
3. **在 `claude.ai/code` 或手机 App 的会话列表中找到它**

### 会话标题来自哪里

官方当前的优先级是：

1. `--name` / `--remote-control` / `/remote-control` 传入的名字
2. `/rename` 设置的名字
3. 最近一条有意义的消息
4. 自动生成的名字

**v2.1.92（[GitHub Release v2.1.92](https://github.com/anthropics/claude-code/releases/tag/v2.1.92)）对 Remote Control 默认名的补充**（以下为 release **英文原文**，便于与官方逐字核对）：

> Remote Control session names now use your hostname as the default prefix (e.g. `myhost-graceful-unicorn`), overridable with `--remote-control-session-name-prefix`

也就是说：在未手动命名时，默认名会带 **hostname 前缀**；也可用 CLI 参数 **`--remote-control-session-name-prefix`** 覆盖该前缀行为。具体与上述 1～4 条优先级如何叠加，以你当前 CLI 行为为准。

所以如果你想让手机上更容易认出来，最实用的是：

```text
/rename monorepo-auth-fix
```

---

## 6. 并发模式：`same-dir` 还是 `worktree`

如果 Remote Control 会衍生出多个并发会话，你要先选好隔离方式。

### `same-dir`

- 所有会话都在同一目录工作
- 配置简单
- 但容易互相改同一批文件

### `worktree`

- 每个并发会话单独一个 git worktree
- 更适合并行任务
- 需要 git 仓库

如果你准备用 Remote Control 做”多设备继续”而非”多人并发”，`same-dir` 足够。

如果你打算把它当作多线程工作台，优先用 `worktree`。

### `session`

- 每个并发会话独立隔离
- 不依赖 git
- 适合不在 git 仓库中的项目

### 运行时切换

在 server mode 下，按 `w` 可以在 `same-dir` 和 `worktree` 之间实时切换。

---

## 7. 远端可用命令 vs 仅本地命令

不是所有 Claude Code 命令都能在远端界面执行。官方当前清单：

**远端可用**（手机 / 浏览器都能执行）：

`/compact`、`/clear`、`/context`、`/usage`、`/exit`、`/usage-credits`、`/recap`、`/reload-plugins`、`/autocompact`

**仅本地**（必须在终端操作）：

`/mcp`、`/plugin`、`/resume`（涉及交互式选择器的命令）

这意味着你不能在手机上装插件或恢复旧会话，但日常的上下文管理和监控都能远程完成。

---

## 8. Sandbox、权限和安全边界

Remote Control 的一个关键误区是：

> 远端只是入口，真正执行操作的还是你本地机器。

所以安全问题本质上仍是**本地 Claude Code 权限问题**。

### 8.1 官方口径下要注意的点

- Remote Control 仍继承本地会话的文件、工具和 MCP 能力
- 允许谁连入，比“界面在哪”更重要
- 如果本地会话权限很宽，远端也会继承

### 8.2 传输安全

官方当前的安全架构：

- 所有流量走 **HTTPS/TLS**，经由 Anthropic API 中转
- 你的机器**不会打开任何入站端口**
- 使用**多个短期、单一用途、独立过期**的凭据

### 8.3 建议做法

- 涉及高风险仓库时，优先配合 sandbox
- 高风险任务不要顺手开 `bypassPermissions`
- 给 Remote Control 会话显式命名，避免误连错会话

---

## 9. Team / Enterprise 常见阻塞

Team 和 Enterprise 下，Remote Control 默认可能是关闭的。

你可能看到这类报错：

- Remote Control requires a claude.ai subscription
- Remote Control is disabled by your organization’s policy
- Unable to determine your organization for Remote Control eligibility
- Remote Control requires a full-scope login token
- Remote Control is not yet enabled for your account

### 9.1 排查顺序

1. 先确认你不是 API key 登录
2. 再确认管理员已经打开 Claude Code 后台里的 Remote Control 开关
3. 确认当前项目已接受 workspace trust
4. 检查是否设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 或 `DISABLE_TELEMETRY` 环境变量（会干扰 RC 连接）
5. 用 `/status` 确认当前登录方式和订阅状态

### 9.2 托管策略：`forceRemoteSettingsRefresh`（v2.1.92）

若组织使用 **remote managed settings**，请关注 **v2.1.92** 引入的策略项（以下为 [v2.1.92 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.92) **英文原文**）：

> Added `forceRemoteSettingsRefresh` policy setting: when set, the CLI blocks startup until remote managed settings are freshly fetched, and exits if the fetch fails (fail-closed)

**含义**：开启后，CLI **在成功拉取到最新远程托管设置之前不会启动**；若拉取失败则 **直接退出**（fail-closed）。具体在项目/企业配置中的写法，以官方托管设置文档与你方管理员下发的 schema 为准，本教程不臆造 JSON 示例。

### 9.3 更高版本增强（v2.1.93 → v2.1.150）

v2.1.92 之后的版本对 Remote Control 做了一系列增强和修复（以下版本号经 GitHub Release Notes 逐条核实）：

| 版本 | 增强 |
|------|------|
| v2.1.98 | 修复 Remote Control 权限处理器中的内存泄漏 |
| v2.1.101 | 修复 worktree 在会话崩溃时被删除、SSH 环境下 `/remote-control` 失败等问题 |
| v2.1.110 | 远端支持 `/autocompact`、`/context`、`/exit`、`/reload-plugins` 命令 |
| v2.1.110 | Push notifications：Claude 可向手机推送通知（需在 `/config` 中启用 "Push when Claude decides"） |
| v2.1.113 | 修复子智能体执行过程不在远端实时显示的问题（subagent streaming） |
| v2.1.113 | 修复会话退出时未正确归档导致重启后丢失的问题 |
| v2.1.116 | 远端支持 `@`-file 自动补全和 `/usage-credits` 命令 |
| v2.1.118-119 | 修复 JWT 刷新期间会话被意外归档的稳定性问题 |
| v2.1.121+ | `effort.level` 在远端会话中可用；`worktree.baseRef` 控制并发 worktree 分叉来源 |
| v2.1.133 | `parentSettingsBehavior` 影响企业环境下的 RC 启用策略（参见 09-企业实战指南） |

其中 **Push notifications** 需要额外配置：

1. 手机安装 Claude App（iOS / Android）
2. 在 Claude Code 中执行 `/config`
3. 启用 "Push when Claude decides"
4. 确保手机和 CLI 使用同一账号

启用后，Claude 在 Remote Control 会话中有重要输出时会主动推送通知到手机。

---

## 10. 典型使用场景

## 场景 1：离开工位继续盯一个长任务

你在终端里：

```bash
claude --remote-control "deploy-watch"
```

然后去手机上继续：

- 看 Claude 跑到哪一步
- 补一句新的指令
- 在沙发上继续盯结果

## 场景 2：本地项目必须在线，但你要换设备

比如：

- 本地已有浏览器登录态
- 本地挂着 MCP
- 本地项目环境复杂

这时用 Web 新开会话就会丢环境，用 Remote Control 就不会。

---

## 11. 常见问题

### Q1：Remote Control 会把我的代码上传到云端吗？

不会按“云端沙箱执行”的方式迁移过去。会话仍运行在你的本地机器上，远端界面只是连接窗口。

### Q2：API key 登录能用吗？

不能。当前官方要求是 `claude.ai` 登录。

### Q3：Remote Control 和 `/mobile` 是什么关系？

`/mobile` 只是帮助你下载 Claude 手机 App；真正开启远程接管的是 `/remote-control` 或对应 CLI 入口。

### Q4：我已经在会话里了，还能临时开吗？

可以，直接：

```text
/remote-control
```

### Q5：它能替代 Cloud / Desktop scheduled tasks 吗？

不能。Remote Control 适合”继续一个正在运行的本地会话”，不是长期持久调度系统。

### Q6：Ultraplan 模式下能用 Remote Control 吗？

不能。官方文档明确说明 **Ultraplan 会断开 Remote Control**。如果你需要远程监控，避免在 Remote Control 会话中使用 Ultraplan。

### Q7：网络不稳定会怎样？

短暂断网会自动重连（包括笔记本合盖/休眠）。但如果**网络中断超过约 10 分钟**，会话会超时断开。

### Q8：能同时开多个 Remote Control 会话吗？

在 server mode（`claude remote-control`）下可以，受 `--capacity` 限制（默认 32）。但在交互模式（`claude --remote-control`）下，**每个交互进程只能有一个 remote session**。

---

## 12. 实用速查

```bash
# 独立 server mode
claude remote-control

# 交互模式直接开 Remote Control
claude --remote-control

# 交互中临时开启
/remote-control

# 给会话命名
/remote-control release-monitor

# v2.1.92+：默认会话名带 hostname 前缀；可用 --remote-control-session-name-prefix 覆盖（参数挂载在哪个子命令上以 claude --help 为准）

# 所有会话自动开启 Remote Control（在 /config 中设置）
/config

# 查看登录状态和订阅信息
/status

# 手机 App 下载二维码
/mobile
```

---

## 13. 下一步建议

- 想把外部消息直接推到会话中：继续看 [Channels与计划任务完整指南](./13-Channels与计划任务完整指南.md)
- 想理解模型切换、1M context 和 `opusplan`：继续看 [安装指南中的模型配置章节](./01-Claude-Code完整安装指南.md#85部分模型配置安装后的进阶配置)

---

> **最后更新**：2026年5月25日 | **适用版本**：Claude Code v2.1.150
