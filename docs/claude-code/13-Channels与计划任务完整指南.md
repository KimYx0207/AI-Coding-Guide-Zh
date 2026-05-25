# Claude Code Channels与计划任务完整指南：把外部事件推入会话

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时
> - **难度等级**：⭐⭐⭐ 进阶
> - **更新日期**：2026年4月
> - **适用版本**：Claude Code v2.1.150（验证于 2026-05-25）
> - **信息来源**：
>   - [Claude Code 官方文档 - Channels](https://code.claude.com/docs/en/channels)
>   - [Claude Code 官方文档 - Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
>   - [GitHub Releases v2.1.128+](https://github.com/anthropics/claude-code/releases)

---

## 本课学习目标

<p align="center"><img src="../../images/official/claude-code-agent-view-dark.png" alt="Claude Code 官方 Agent View 深色界面：Needs input、Working、Completed 分组" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-agent-view.png" alt="Claude Code 官方 Agent View：多后台会话状态" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-product-ui.jpg" alt="Claude Code 官方 CLI 任务界面：任务执行、文件变更与终端状态" width="720"/></p>

完成本课后，你将能：

1. 理解 Channels、Remote Control、MCP、Cloud Tasks 之间的区别
2. 正确安装并启用官方 channel plugin
3. 用 `--channels` 把 Telegram / Discord / iMessage / fakechat 推入当前会话
4. 正确使用 `/schedule`、`/loop`、`CronCreate / CronList / CronDelete`
5. 避开“用 polling 解决 push 问题”这种常见设计误区

---

## 1. 先说结论

Channels 和计划任务，解决的是两类不同问题：

- **Channels**：外部事件主动推给 Claude
- **计划任务**：Claude 按时间轮询或提醒

如果你只记一句话：

> 有事件就用 Channels，没有事件源才考虑 `/loop` 或 `/schedule`。

---

## 2. Channels 是什么

官方当前定义里，Channels 是：

> 通过 MCP server 把消息、提醒、Webhook 直接推入你已经打开的 Claude Code 会话。

它不是新开云端会话，也不是轮询。

它的核心价值是：

- CI 失败了，直接把结果推进当前会话
- Telegram / Discord / iMessage 上给 Claude 发消息
- 你不在终端前时，也能让外部事件进到当前 session

### 2.1 当前官方状态

- **research preview**
- 需要 **Claude Code v2.1.80+**
- 需要 **claude.ai 登录**
- Team / Enterprise 默认可能关闭，需要管理员启用

**v2.1.128 变更**：`--channels` 现在也支持 **Console auth（API key）登录**，不再仅限 claude.ai 登录。如果你之前因为 API key 模式无法使用 Channels，可以重新尝试。

---

## 3. Channels、Remote Control、普通 MCP 的区别

| 功能 | 解决什么问题 | 最适合场景 |
|------|--------------|------------|
| Channels | 外部事件主动推进来 | CI、聊天桥、Webhook |
| Remote Control | 你自己从别的设备继续控制会话 | 手机继续本地会话 |
| 普通 MCP | Claude 在任务中主动调用外部工具 | 按需查数据 / 操作系统 |
| `/loop` / `Cron*` | 按时间轮询或提醒 | 没有事件推送源时 |

一个特别重要的判断标准：

- **外部系统会主动发事件**：优先 Channels
- **只能自己定时检查**：才用 `/loop`

---

## 4. 开始前准备

> **v2.1.139+ 注意**：当环境中设置 `ANTHROPIC_API_KEY`、`apiKeyHelper` 或 `ANTHROPIC_AUTH_TOKEN` 时，`/schedule`、Remote Control、claude.ai MCP connectors 和通知偏好会被禁用。Channels / 计划任务教程默认按 Claude.ai 登录路径讲解；企业 API key 环境请先核对当前 `/status`。

### 4.1 基础条件

- Claude Code 已安装并登录 claude.ai
- 能看到 `/plugin`
- 若要跑官方 channel plugin，**必须安装 Bun**（所有官方 channel plugin 都依赖 Bun 运行时）

### 4.2 当前官方支持的典型 channel plugin

- Telegram
- Discord
- iMessage
- fakechat（官方 demo）

---

## 5. 最推荐的入门方式：fakechat

如果你第一次接触 Channels，别一上来就配 Telegram。

先用官方 demo `fakechat` 最稳。

### 5.1 安装插件

在 Claude Code 里：

```text
/plugin install fakechat@claude-plugins-official
```

如果提示 marketplace 不存在或未更新，先执行：

```text
/plugin marketplace update claude-plugins-official
```

或：

```text
/plugin marketplace add anthropics/claude-plugins-official
```

### 5.2 启动 channels

退出当前会话后重新启动：

```bash
claude --channels plugin:fakechat@claude-plugins-official
```

如果要同时启动多个 channel，用空格分隔：

```bash
claude --channels plugin:telegram@claude-plugins-official plugin:discord@claude-plugins-official
```

### 5.3 打开本地界面

浏览器打开：

```text
http://localhost:8787
```

在页面输入消息，它会作为 `<channel source="fakechat">` 事件进入你当前 Claude Code 会话。

这就是理解 Channels 最快的方法。

---

## 6. Telegram / Discord / iMessage 的核心模式

它们虽然接法不同，但逻辑一致：

1. 装 plugin
2. 配 token 或权限
3. 用 `--channels` 启动
4. 做 pairing / allowlist
5. 之后该平台的消息会直接推入当前 session

### 6.1 Telegram

官方主路径大致是：

```text
/plugin install telegram@claude-plugins-official
/reload-plugins
/telegram:configure <token>
```

然后重启：

```bash
claude --channels plugin:telegram@claude-plugins-official
```

再做配对：

```text
/telegram:access pair <code>
/telegram:access policy allowlist
```

### 6.2 Discord

同理：

```text
/plugin install discord@claude-plugins-official
/reload-plugins
/discord:configure <token>
```

然后：

```bash
claude --channels plugin:discord@claude-plugins-official
```

最后：

```text
/discord:access pair <code>
/discord:access policy allowlist
```

**Discord Bot 必须开启的权限：**

- **Message Content Intent**（在 Developer Portal 的 Bot 设置中开启）
- View Channels
- Send Messages
- Send Messages in Threads
- Read Message History
- Attach Files
- Add Reactions

### 6.3 iMessage

iMessage 逻辑不同：

- 只支持 macOS
- 直接读本机 Messages 数据库
- 需要 Full Disk Access
- 回复靠 AppleScript

启动方式：

```text
/plugin install imessage@claude-plugins-official
```

```bash
claude --channels plugin:imessage@claude-plugins-official
```

默认给自己发消息即可打通；允许其他联系人则用：

```text
/imessage:access allow +15551234567
```

### 6.4 Token 存储位置

各 channel 的 token 默认存储在：

- Telegram：`~/.claude/channels/telegram/.env`（包含 `TELEGRAM_BOT_TOKEN`）
- Discord：`~/.claude/channels/discord/.env`（包含 `DISCORD_BOT_TOKEN`）

如果你需要迁移配置或排查连接问题，直接检查这些文件。

---

## 7. Channels 的安全边界

官方当前强调的几个点很关键：

### 7.1 allowlist 是核心

所有 approved channel plugin 都有 sender allowlist。

也就是说：

- 不是“谁知道 bot 就能发”
- 而是“只有被允许的 sender 才能推消息进来”

### 7.2 `--channels` 只是本会话启用

即便 `.mcp.json` 里有 server，也不代表它能推送消息。

必须当前会话显式用：

```bash
claude --channels plugin:xxx@marketplace
```

### 7.3 Team / Enterprise 还能再控一层

管理员可以通过：

- `channelsEnabled`
- `allowedChannelPlugins`

控制：

- 组织是否允许 Channels
- 哪些 plugin 可以注册成 channel

另外，如果你在开发自定义 channel plugin，需要加：

```bash
claude --channels plugin:my-channel --dangerously-load-development-channels
```

该参数绕过 marketplace 验证，仅用于本地开发调试。

### 7.4 Permission Relay：远端审批权限请求

从 v2.1.81 起（v2.1.100 完全实现），Channels 支持**权限中继**（Permission Relay）：

当 Claude 需要执行需要审批的操作时（如写文件、执行命令），权限确认请求会被转发到你的 Channel（如 Telegram / Discord），你可以直接在手机上批准或拒绝。

这意味着你不需要守在终端前也能让 Claude 继续有权限地工作。

### 7.5 事件只在会话打开时到达

Channel 消息**只会在 Claude Code 会话运行时被接收**。如果你关掉了终端，消息就丢了。

如果你需要 always-on 的 Channel 接收：

- 在后台进程中运行 Claude Code
- 或使用持久终端（如 tmux / screen）

---

## 8. 什么时候该用 `/loop`

`/loop` 不是 Channels 的替代品，它是：

> 当前会话仍然开着时，用最低成本做“定时轮询”。

官方当前把 `/loop` 归为 **bundled skill**，不是固定逻辑 built-in command。

### 8.1 最基础用法

```text
/loop 5m check if the deployment finished and tell me what happened
```

### 8.2 `/loop` 不带 prompt 时的默认行为

如果你只打 `/loop` 不带任何参数，Claude 会使用内置的维护提示词，按以下优先级自动工作：

1. **继续未完成的工作**
2. **维护当前 PR**（查看 review comments、CI 失败、merge conflicts）
3. **运行清理**（bug 排查、代码简化）

你也可以自定义默认提示词：在项目目录创建 `.claude/loop.md`，或在用户目录创建 `~/.claude/loop.md`。项目级优先于用户级。修改后下一次迭代自动生效。

### 8.3 它支持几种写法

```text
/loop 30m check the build
/loop check the build every 2 hours
/loop check the build
```

如果你不写间隔且带了自定义 prompt，Claude 会**动态选择间隔**（1 分钟到 1 小时之间），根据观察到的情况自行调整。不带 prompt 的纯 `/loop` 也是动态间隔。

### 8.4 支持单位

- `s`
- `m`
- `h`
- `d`

但底层 cron 只有分钟粒度，所以秒会向上取整到分钟。

### 8.5 还能循环执行另一个命令

```text
/loop 20m /sync-inbox
```

### 8.6 取消正在等待的 `/loop`

在 `/loop` 等待下一次迭代时，按 **Esc** 即可取消（v2.1.111+）。

### 8.7 `/proactive` 别名

从 v2.1.105 起，`/proactive` 是 `/loop` 的别名，功能完全相同。如果你觉得 "loop" 不够语义化，可以用 `/proactive`。

---

## 9. `/schedule`、`CronCreate`、`CronList`、`CronDelete`

除了 `/loop`，Claude Code 现在还有更底层的 cron 调度能力。

### 9.1 当前官方工具

| 工具 | 作用 |
|------|------|
| `CronCreate` | 创建任务 |
| `CronList` | 列出任务 |
| `CronDelete` | 删除任务 |

计划任务功能（`/loop`、`CronCreate` 等）从 **v2.1.72+** 开始可用，比 Channels（v2.1.80+）更早。

### 9.2 Cron 表达式参考

如果 Claude 直接使用 `CronCreate`，底层走的是标准 cron 表达式：

| 表达式 | 含义 |
|--------|------|
| `*/5 * * * *` | 每 5 分钟 |
| `0 * * * *` | 每小时整点 |
| `0 9 * * *` | 每天早上 9 点 |
| `0 9 * * 1-5` | 工作日早上 9 点 |
| `30 14 15 3 *` | 3 月 15 日下午 2:30 |

所有时间均为**本地时区**，不是 UTC。

### 9.3 `/schedule` 是什么

`/schedule` 是当前用户入口，用来创建、更新、列出和运行 **Cloud scheduled tasks**。

但在**本地 session 里**，Claude 也会借助 `CronCreate / CronList / CronDelete` 做 session-scoped 的计划任务和提醒。

### 9.4 一次性提醒

你甚至不一定非得手打 `/schedule`。

自然语言也可以：

```text
remind me at 3pm to push the release branch
```

```text
in 45 minutes, check whether the integration tests passed
```

---

## 10. 当前本地计划任务的关键限制

官方当前明确写了几个限制，必须知道：

### 10.1 任务是 session-scoped

只要当前 Claude Code 会话结束，任务就没了。

### 10.2 不跨重启持久化（v2.1.110 部分改善）

重启 Claude Code 后，本地 cron 任务默认不会继续。

但从 **v2.1.110** 起，如果用 `--resume` 或 `--continue` 恢复之前的会话，**未过期的计划任务会一起恢复**。也就是说：

- 正常重启 → 任务丢失
- `claude --resume` / `claude --continue` → 未过期任务自动恢复

### 10.3 Claude 忙的时候不会插队

定时任务会在 turn 之间触发，不会在 Claude 正在回答时硬插进去。

### 10.4 recurring task 7 天自动过期

官方当前默认策略是：

- 循环任务 7 天后自动过期
- 最后再触发一次，然后删除

这是为了防止遗忘的轮询长期跑下去。

### 10.5 退出确认会提示剩余任务（v2.1.113+）

从 **v2.1.113** 起，当你退出会话时，如果还有未完成的计划任务，Claude Code 会显示确认提示并展示倒计时：

- 一次性任务：显示距离触发还有多久
- 循环任务：显示下一次触发时间

这样你就不会不小心退出然后丢掉还没跑的任务。

### 10.6 每个会话最多 50 个计划任务

官方当前限制：单个会话最多 50 个计划任务。超过后需要先删除旧的才能创建新的。

### 10.7 `--resume` 不会恢复所有任务

v2.1.110 的 `--resume` 恢复策略有细节：

- **循环任务**：创建后 7 天内的会恢复
- **一次性任务**：计划时间未过的会恢复
- **后台 Bash 和监控任务**：永远不恢复

### 10.8 Jitter 策略

为了避免大规模部署时所有 Claude 实例在同一时刻触发：

- **循环任务**：最多延迟周期的 10%（上限 15 分钟）
- **一次性任务**：整点/半点前后最多提前 90 秒

这是确定性偏移，不是随机的。

### 10.9 Bedrock / Vertex / Foundry 限制

在 Bedrock、Vertex 或 Foundry 环境下，`/loop <prompt>` 固定为 **10 分钟间隔**，不支持动态调整。

### 10.10 禁用调度器

如果你完全不需要计划任务功能：

```bash
CLAUDE_CODE_DISABLE_CRON=1 claude
```

---

## 11. 什么时候该用 Cloud / Desktop scheduled tasks

如果你需要：

- 关掉终端后也继续
- 重启后依然在
- 不依赖当前 session 持续存活

那就别靠 `/loop`。

官方建议：

- 要可靠、无需你机器在线：用 **Cloud scheduled tasks**
- 要跑在你本机且跨重启：用 **Desktop scheduled tasks**
- 只是在当前 session 临时盯一件事：用 **`/loop`**

---

## 12. 常见误区

### 误区 1：Channels = Remote Control

不是。

- Remote Control 是你自己远程接管
- Channels 是外部系统把消息推过来

### 误区 2：有 `/loop` 就不用 Channels

不对。

如果外部系统本来就能发事件，轮询只是更慢、更贵、更脆。

### 误区 3：计划任务会一直留着

不会。当前本地计划任务是 session-scoped，循环任务还有 7 天自动过期。

---

## 13. 实用速查

```text
/plugin install fakechat@claude-plugins-official
/reload-plugins
```

```bash
claude --channels plugin:fakechat@claude-plugins-official
```

```bash
# 同时启动多个 channel
claude --channels plugin:telegram@claude-plugins-official plugin:discord@claude-plugins-official
```

```text
/loop 5m check if the deployment finished
```

```text
# 按 Esc 取消正在等待的 /loop
```

```text
what scheduled tasks do I have?
cancel the deploy check job
```

```text
# 自定义 /loop 默认提示词
# 创建 .claude/loop.md 或 ~/.claude/loop.md
```

```bash
# 恢复会话时自动恢复未过期任务
claude --resume
```

---

## 14. 下一步建议

- 想跨设备继续本地会话：继续看 [Remote Control完整指南](./12-Remote-Control完整指南.md)
- 想控制模型、1M 上下文和 `opusplan`：继续看 [安装指南中的模型配置章节](./01-Claude-Code完整安装指南.md#85部分模型配置安装后的进阶配置)

---

> **最后更新**：2026年5月25日 | **适用版本**：Claude Code v2.1.150
