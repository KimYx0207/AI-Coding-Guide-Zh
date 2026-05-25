# 08. 多 Agent 协作指南

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **难度等级**：🔴 高级
> - **阅读时间**：35 分钟
> - **前置知识**：已熟悉基本使用（[03-快速开始](03-快速开始指南.md)）+ 了解技能系统（[06-技能系统](06-技能系统指南.md)）
>
> **本篇你将学会：** 创建多个 AI 助手、配置分工协作、设置消息路由、管理 Agent 间通信
>
> **大多数人不需要这篇！** 如果你只是个人使用，一个默认的 main Agent 就够了。只有当你需要"不同平台用不同 AI 性格"或"团队多人使用"时才需要看这篇

## 什么是 Agent？

<p align="center"><img src="../../images/official/openclaw-model-picker.png" alt="OpenClaw 官方模型选择与配置界面" width="720"/></p>

<p align="center"><img src="../../images/official/openclaw-quick-settings-browser-tools.png" alt="OpenClaw 官方 Control UI 设置与浏览器工具界面" width="720"/></p>

在 OpenClaw 的世界里，Agent 就是一个独立的 AI 助手实例。每个 Agent 有自己的"大脑"（系统指令）、"记忆"（记忆文件）、"技能"（技能集）和"身份"（认证凭证）。

你可以把 Agent 想象成公司里的员工：

```
Agent = 一个独立的 AI 员工

它有：
├── 自己的工位（工作空间目录）
├── 自己的工牌（认证凭证）
├── 自己的笔记本（记忆文件）
├── 自己的技能证书（技能集）
├── 自己的性格（SOUL.md 人格设定）
└── 自己的工作日志（会话历史）
```

> 💡 **术语说明：** 上面提到的 `SOUL.md` 是 Agent 的人格设定文件，定义 AI 的性格和行为风格，后面会详细介绍。

默认情况下，OpenClaw 只有一个 `main` Agent。对大多数人来说，一个 Agent 就够了 -- 它能处理你所有的消息、执行所有的任务。

## 为什么需要多个 Agent？

一个 Agent 什么都干，听起来很方便，但实际用起来会遇到问题：

**问题一：上下文污染**

当你让同一个 Agent 既写代码又管日程，它的系统提示词会变得很长。写代码时加载了一堆日历相关的技能指令，管日程时又带着一堆编程工具的描述。这些无关信息会：
- 浪费 token（花更多钱）
- 降低 AI 的专注度（回答质量下降）
- 增加误触发的概率（该用 A 技能时用了 B）

**问题二：人格冲突**

你希望编程助手严谨、精确、代码优先；但你希望社交助手轻松、幽默、善于闲聊。一个 Agent 很难同时扮演两种截然不同的角色。

**问题三：安全隔离**

编程 Agent 需要访问 GitHub、执行 Shell 命令；但你不希望社交 Agent 也有这些权限。万一有人通过社交平台发了一条恶意消息，触发了 Shell 命令执行，后果不堪设想。

**问题四：消息路由**

你可能希望 Discord 的 #coding 频道由编程 Agent 处理，Telegram 的家庭群由生活 Agent 处理。一个 Agent 没法根据消息来源自动切换行为模式。

多 Agent 架构就是为了解决这些问题：

```
单 Agent 模式：
┌─────────────────────────────────────┐
│  所有消息 → main Agent → 所有技能    │
│  （上下文臃肿，角色混乱）             │
└─────────────────────────────────────┘

多 Agent 模式：
┌─────────────────────────────────────┐
│  Discord #coding → coding Agent     │
│                    （只加载开发技能）  │
│                                     │
│  Telegram 家庭群 → home Agent       │
│                    （只加载生活技能）  │
│                                     │
│  WhatsApp 私聊 → main Agent         │
│                  （通用技能）         │
└─────────────────────────────────────┘
```

## OpenClaw 的 Agent 架构

### 架构总览

<p align="center"><img src="../../images/official/openclaw-agents-ui.jpg" alt="OpenClaw 官方多 Agent UI 图" width="720"/></p>

> **v2026.5.22 子代理注意**：默认子 Agent bootstrap context 已收窄到 `AGENTS.md` 与 `TOOLS.md`，不会自动把 persona、identity、user、memory、heartbeat、setup 等文件全部带入 delegated workers。多 Agent 教程里的“自动继承上下文”应按最小必要上下文理解。

> ⏭️ **小白可跳过** — 这是底层运行时细节

OpenClaw 的多 Agent 架构基于 Pi agent runtime（RPC 模式）运行，采用**扁平路由模型**，不是层级管理模型。没有"管理者 Agent"来调度其他 Agent，而是由 Gateway 根据消息来源直接路由到对应的 Agent。每个 Agent 通过 channel routing（消息路由，决定哪条消息由哪个 Agent 处理）配置绑定到不同的频道或账号。

```
┌─────────────────────────────────────────────────────────────┐
│                     消息平台层                                │
│  WhatsApp │ Telegram │ Discord │ Slack │ Signal │ WebChat   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   Gateway 路由引擎                             │
│                                                              │
│  消息进来 → 检查 bindings 配置 → 匹配 Agent                   │
│                                                              │
│  路由规则：                                                    │
│  ├── Discord #coding 频道 → coding Agent                     │
│  ├── Telegram 群 -100xxxxx → social Agent                    │
│  ├── Slack #team 频道 → work Agent                           │
│  └── 其他所有消息 → main Agent（默认）                         │
└──────┬──────────┬──────────┬──────────┬─────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│  main    ││  coding  ││  social  ││  work    │
│  Agent   ││  Agent   ││  Agent   ││  Agent   │
│          ││          ││          ││          │
│ 工作空间  ││ 工作空间  ││ 工作空间  ││ 工作空间  │
│ 记忆文件  ││ 记忆文件  ││ 记忆文件  ││ 记忆文件  │
│ 技能集   ││ 技能集   ││ 技能集   ││ 技能集   │
│ 认证凭证  ││ 认证凭证  ││ 认证凭证  ││ 认证凭证  │
│ SOUL.md  ││ SOUL.md  ││ SOUL.md  ││ SOUL.md  │
└──────────┘└──────────┘└──────────┘└──────────┘
```

### 关键设计决策

**为什么是扁平路由而不是层级管理？**

OpenClaw 官方明确表示不会合并"Agent 层级框架（管理者的管理者/嵌套规划树）"。原因很实际：

1. 层级管理增加延迟 -- 消息要先经过管理者 Agent 判断，再转发给工作 Agent
2. 管理者 Agent 本身也消耗 token -- 每条消息多一次 AI 调用
3. 路由规则是确定性的 -- 不需要 AI 来判断消息该给谁，配置文件就能搞定
4. 简单可靠 -- 越少的中间环节，越少的出错机会

**每个 Agent 是完全独立的**

Agent 之间默认没有任何共享：

| 资源 | 是否共享 | 说明 |
|------|----------|------|
| 工作空间 | 否 | 每个 Agent 有独立的工作目录 |
| 记忆文件 | 否 | 每个 Agent 有独立的 MEMORY.md 和日志 |
| 记忆后端 | 可选 | 可配置 Builtin(SQLite)、QMD、Honcho 等后端 |
| 会话历史 | 否 | 每个 Agent 的对话记录完全隔离 |
| 认证凭证 | 否 | 每个 Agent 的 auth-profiles.json 独立 |
| 技能配置 | 可选 | 可以配置 Agent 级别的技能白名单 |
| AI 模型 | 可选 | 可以为每个 Agent 指定不同的模型 |

### 目录结构详解

```
~/.openclaw/
├── openclaw.json              # 主配置文件（包含 Agent 列表和路由规则）
│
├── agents/                    # Agent 状态目录
│   ├── main/                  # 默认 Agent
│   │   ├── agent/
│   │   │   └── auth-profiles.json    # main 的认证凭证
│   │   └── sessions/                  # main 的会话历史
│   │       ├── session-abc123.json
│   │       └── session-def456.json
│   │
│   ├── coding/                # 编程 Agent
│   │   ├── agent/
│   │   │   └── auth-profiles.json    # coding 的认证凭证
│   │   └── sessions/                  # coding 的会话历史
│   │
│   └── social/                # 社交 Agent
│       ├── agent/
│       │   └── auth-profiles.json    # social 的认证凭证
│       └── sessions/                  # social 的会话历史
│
├── workspace/                 # main Agent 的工作空间
│   ├── SOUL.md               # main 的人格设定
│   ├── AGENTS.md             # Agent 协作说明
│   ├── USER.md               # 用户信息
│   ├── MEMORY.md             # main 的长期记忆
│   ├── memory/               # main 的每日日志
│   └── skills/               # main 的工作空间技能
│
├── workspace-coding/          # coding Agent 的工作空间
│   ├── SOUL.md               # coding 的人格设定
│   ├── MEMORY.md             # coding 的长期记忆
│   ├── memory/               # coding 的每日日志
│   └── skills/               # coding 的工作空间技能
│
└── workspace-social/          # social Agent 的工作空间
    ├── SOUL.md               # social 的人格设定
    ├── MEMORY.md             # social 的长期记忆
    ├── memory/               # social 的每日日志
    └── skills/               # social 的工作空间技能
```

每个 Agent 的工作空间是它的"家"。AI 的文件操作默认在这个目录下进行，记忆文件也存在这里。其中 `AGENTS.md`（Agent 的系统指令文件）定义了 Agent 之间的协作规则。

## Agent 角色定义和配置

### 创建新 Agent

```bash
# 使用向导创建（推荐）
openclaw agents add coding
openclaw agents add social
openclaw agents add work

# 每个 Agent 会自动创建：
# - 独立的工作空间（SOUL.md, AGENTS.md, USER.md）
# - 独立的 agentDir 和会话存储
# - 独立的 auth-profiles.json
```

### 查看和管理 Agent

```bash
# 列出所有 Agent
openclaw agents list

# 更新 Agent 的身份设定
openclaw agents set-identity
```

### 在 openclaw.json（JSON5）中配置 Agent

Agent 的核心配置在 `~/.openclaw/openclaw.json`（JSON5 格式）的 `agents` 字段中：

```json5
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-6",
      "sandbox": {
        // 非主会话在 Docker 沙箱中运行
        "mode": "non-main",
      },
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "model": "anthropic/claude-opus-4-6",
      },
      {
        "id": "coding",
        "workspace": "~/.openclaw/workspace-coding",
        "model": "anthropic/claude-opus-4-6",
        // Agent 级别的 skills 是简单的字符串数组
        "skills": ["coding-agent", "github", "gh-issues", "tmux"],
      },
      {
        "id": "social",
        "workspace": "~/.openclaw/workspace-social",
        "model": "openai/gpt-5.2",
        "skills": ["summarize", "weather", "goplaces"],
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "model": "anthropic/claude-sonnet-4-6",
        "skills": ["gog", "slack", "notion", "trello", "summarize"],
      },
    ],
  },

  // bindings 是顶层配置，不嵌套在 agent 内部
  "bindings": [
    {
      "agent": "coding",
      "channel": "discord",
      "guildId": "123456789",
      "channelId": "987654321",
    },
    {
      "agent": "social",
      "channel": "telegram",
      "chatId": "-100123456789",
    },
    {
      "agent": "work",
      "channel": "slack",
      "teamId": "T01234567",
      "channelId": "C01234567",
    },
  ],
}
```

### Agent 配置字段详解

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `string` | 是 | Agent 唯一标识符，只能用字母、数字、连字符 |
| `workspace` | `string` | 是 | 工作空间目录路径 |
| `model` | `string` 或 `object` | 否 | AI 模型，可以是字符串或 `{ primary, fallbacks }` 对象 |
| `skills` | `string[]` | 否 | Agent 可用的技能列表（简单字符串数组） |
| `sandbox` | `object` | 否 | 沙箱配置 |

> **注意：** `bindings`（消息路由绑定）是顶层配置，不嵌套在 Agent 内部。`temperature`、`maxTokens` 等参数不是 Agent 级别的直接配置字段。

### Agent 人格设定（SOUL.md）

每个 Agent 的工作空间里有一个 `SOUL.md` 文件，这是 Agent 的"灵魂"。AI 在每次会话启动时都会读取这个文件，作为系统指令的一部分。

**编程 Agent 的 SOUL.md 示例：**

```markdown
# coding Agent

你是一个专业的编程助手，专注于帮助用户写代码、调试和架构设计。

## 性格
- 严谨、精确、逻辑清晰
- 代码优先，少说废话
- 遇到不确定的问题会主动说"我不确定"
- 喜欢用代码示例来解释概念

## 专长
- TypeScript / Python / Go / Rust
- 系统架构设计和代码审查
- 性能优化和安全分析
- DevOps 和 CI/CD

## 工作规则
- 所有代码必须有类型注解
- 遵循 SOLID 原则和 DRY 原则
- 不写没有测试的代码
- 代码变更前先解释方案，等用户确认再执行
- 遇到安全相关的代码要特别谨慎

## 沟通风格
- 用中文沟通，代码注释用英文
- 回复简洁，不要长篇大论
- 给出代码时附带简短解释
- 如果用户的需求不明确，先问清楚再动手
```

**社交 Agent 的 SOUL.md 示例：**

```markdown
# social Agent

你是一个轻松有趣的聊天伙伴，帮助用户管理社交消息和日常生活。

## 性格
- 幽默、随和、善于倾听
- 说话像朋友，不像机器人
- 适当使用 emoji 让对话更生动
- 遇到敏感话题会委婉回避

## 专长
- 日常闲聊和情感支持
- 天气查询和出行建议
- 内容摘要和信息整理
- 简单的翻译和语言帮助

## 工作规则
- 不执行任何代码或 Shell 命令
- 不访问文件系统（除了记忆文件）
- 回复要简短，适合手机阅读
- 群聊中只在被 @提及时回复

## 沟通风格
- 轻松口语化，像朋友聊天
- 适当使用表情符号
- 回复控制在 3-5 句话以内
- 如果不知道答案，诚实说不知道
```

**办公 Agent 的 SOUL.md 示例：**

```markdown
# work Agent

你是一个高效的办公助手，帮助用户管理邮件、日程、项目和文档。

## 性格
- 专业、高效、条理清晰
- 主动提醒重要事项
- 善于整理和归纳信息
- 注重时间管理

## 专长
- Gmail 邮件管理和回复
- Google Calendar 日程安排
- Notion/Trello 项目管理
- Slack 消息管理
- 会议纪要和周报生成

## 工作规则
- 处理邮件前先确认用户意图
- 发送邮件/消息前必须让用户确认内容
- 日程冲突时主动提醒
- 重要操作（删除、发送）需要二次确认

## 沟通风格
- 专业但不生硬
- 用列表和要点来组织信息
- 时间相关的信息要明确时区
- 涉及金额时要标明货币单位
```

### 为不同 Agent 配置不同的 AI 模型

这是多 Agent 架构的一个隐藏优势：你可以根据任务复杂度为不同 Agent 选择不同的模型，优化成本。

```json5
{
  "agents": {
    "list": [
      {
        "id": "coding",
        "model": "anthropic/claude-opus-4-6",
        // 编程需要最强的推理能力，用最好的模型
      },
      {
        "id": "social",
        "model": "openai/gpt-5.2-mini",
        // 闲聊不需要太强的模型，用便宜的就行
      },
      {
        "id": "work",
        "model": "anthropic/claude-sonnet-4-6",
        // 办公任务中等复杂度，用性价比最高的
      },
    ],
  },
}
```

成本对比（假设每天处理 100 条消息）：

| 方案 | 模型 | 估算日成本 |
|------|------|-----------|
| 全部用 Opus | claude-opus-4-6 | ~$5-10 |
| 按需分配 | Opus + Sonnet + Mini | ~$2-4 |
| 全部用 Mini | gpt-5.2-mini | ~$0.5-1 |

按需分配能在保证关键任务质量的同时，大幅降低成本。

## Agent 间通信机制

> ⏭️ **小白可跳过** — 这是 Agent 间通信的底层机制，了解概念即可

### Sessions 工具：Agent 直接通信

OpenClaw 提供了一组 Sessions 工具，让 Agent 之间可以直接通信。这些工具基于 Pi agent runtime 的 RPC 模式运行，每个 Agent 可以发现、查看和向其他会话发送消息。

**四个核心工具：**

| 工具 | 功能 | 说明 |
|------|------|------|
| `sessions_list` | 发现活跃会话 | 列出当前所有活跃的 Agent 会话 |
| `sessions_history` | 获取会话日志 | 查看指定会话的历史消息 |
| `sessions_send` | 向另一个会话发消息 | 支持 reply-back ping-pong 和 announce step 模式 |
| `sessions_spawn` | 生成新会话 | 动态创建一个新的 Agent 会话 |

**sessions_send 的两种模式：**

- **reply-back ping-pong** -- 发送消息并等待对方回复，适合需要来回协商的场景
- **announce step** -- 单向通知，不等待回复，适合流水线式的任务传递

**使用示例：**

```
coding Agent 完成代码审查
    │
    ├── sessions_list → 发现 writer Agent 的活跃会话
    │
    ├── sessions_send → 向 writer Agent 发送审查结果
    │   （announce step 模式，不等待回复）
    │
    └── writer Agent 收到消息，开始生成审查报告
```

**Sessions CLI 命令：**

```bash
# 列出所有活跃会话
openclaw sessions list

# 清理过期会话
openclaw sessions cleanup
```

### 间接通信方式

除了 Sessions 工具的直接通信，还有几种间接通信的方式：

**方式一：共享文件**

把需要共享的数据放在一个公共目录：

```json5
{
  "agents": {
    "list": [
      {
        "id": "research",
        "workspace": "~/.openclaw/workspace-research",
      },
      {
        "id": "writer",
        "workspace": "~/.openclaw/workspace-writer",
      },
    ],
  },
}
```

在两个 Agent 的 SOUL.md 中都指向同一个共享目录：

```markdown
## 共享数据

当需要与其他 Agent 共享数据时，把文件写入 ~/.openclaw/shared/ 目录。
读取其他 Agent 的输出也从这个目录读取。
```

**方式二：通过用户中转**

最简单的方式 -- 你从一个 Agent 那里得到结果，然后手动发给另一个 Agent：

```
你 → coding Agent：帮我分析这段代码的性能问题
coding Agent → 你：发现 3 个性能瓶颈：1. N+1 查询 2. 未缓存 3. 同步阻塞

你 → work Agent：帮我创建 3 个 Jira Issue，分别是...
work Agent → 你：已创建 PROJ-101, PROJ-102, PROJ-103
```

**方式三：通过定时任务串联**

用 Cron 定时任务让 Agent 按顺序执行：

```json5
{
  "cron": {
    "enabled": true,
    "store": "file",
    "maxConcurrentRuns": 2,
  },
}
```

> **注意：** `cron` 是一个配置对象（包含 `enabled`、`store`、`maxConcurrentRuns` 等字段），不是任务数组。具体的定时任务通过 CLI 管理：

```bash
# 添加定时任务
openclaw cron add --name "research-phase" --schedule "0 9 * * 1-5" \
  --agent research --prompt "搜索今天的行业新闻，整理成摘要，保存到 ~/.openclaw/shared/daily-news.md"

openclaw cron add --name "writing-phase" --schedule "30 9 * * 1-5" \
  --agent writer --prompt "读取 ~/.openclaw/shared/daily-news.md，基于今天的新闻写一篇简报，发送到 Slack #news 频道"

# 列出所有定时任务
openclaw cron list

# 删除定时任务
openclaw cron rm research-phase
```

**方式四：通过 HTTP 请求触发**

一个 Agent 完成任务后，可以通过 Gateway 的 HTTP API 触发另一个 Agent。在 coding Agent 的技能中，完成审查后通过 HTTP 请求触发 writer Agent：

```markdown
## 审查完成后

1. 把审查结果保存到 ~/.openclaw/shared/review-result.json
2. 通过 HTTP 请求通知 Gateway: POST http://localhost:18789/api/message
   发送消息给 writer Agent，提示它读取审查结果并生成报告
```

## 消息路由和绑定配置

### 路由规则详解

Gateway 收到消息后，按以下顺序匹配 Agent：

```
消息进来
    │
    ▼
1. 检查 bindings 配置
   ├── 匹配到 → 路由到对应 Agent
   └── 未匹配 → 继续
    │
    ▼
2. 检查是否是私聊
   ├── 是 → 路由到 main Agent（默认）
   └── 否 → 继续
    │
    ▼
3. 回退到默认 Agent（main）
```

### 绑定类型

**Discord 绑定：**

```json5
// 顶层 bindings 数组
{
  "bindings": [
    {
      "agent": "coding",
      "channel": "discord",
      "guildId": "123456789",
      "channelId": "987654321",
    },
  ],
}
```

- `guildId` -- Discord 服务器 ID
- `channelId` -- Discord 频道 ID
- 可以只指定 `guildId`，这样整个服务器的消息都路由到这个 Agent

**Telegram 绑定：**

```json5
{
  "bindings": [
    {
      "agent": "social",
      "channel": "telegram",
      "chatId": "-100123456789",
    },
  ],
}
```

- `chatId` -- Telegram 群组 ID（负数开头）
- 私聊默认走 main Agent，不需要绑定

**Slack 绑定：**

```json5
{
  "bindings": [
    {
      "agent": "work",
      "channel": "slack",
      "teamId": "T01234567",
      "channelId": "C01234567",
    },
  ],
}
```

**WhatsApp 绑定：**

```json5
{
  "bindings": [
    {
      "agent": "social",
      "channel": "whatsapp",
      "groupId": "120363xxx@g.us",
    },
  ],
}
```

**多平台绑定：**

一个 Agent 可以绑定多个平台的多个频道：

```json5
// 顶层 bindings 数组中，同一个 agent 可以有多条绑定
{
  "bindings": [
    {
      "agent": "coding",
      "channel": "discord",
      "guildId": "111111",
      "channelId": "222222",
    },
    {
      "agent": "coding",
      "channel": "discord",
      "guildId": "111111",
      "channelId": "333333",
    },
    {
      "agent": "coding",
      "channel": "telegram",
      "chatId": "-100999888777",
    },
    {
      "agent": "coding",
      "channel": "slack",
      "teamId": "T01234567",
      "channelId": "C09876543",
    },
  ],
}
```

### 查看路由状态

```bash
# 查看所有 Agent
openclaw agents list

# 输出示例：
# Agent: main (default)
#   No specific bindings (handles unmatched messages)
#
# Agent: coding
#   discord: guild=111111 channel=222222
#   discord: guild=111111 channel=333333
#   telegram: chat=-100999888777
#
# Agent: social
#   telegram: chat=-100123456789
```

## 任务分发和协调策略

### 策略一：按职能分工

最常见的策略，每个 Agent 负责一个领域：

```
┌──────────────────────────────────────────────────┐
│                  按职能分工                        │
│                                                  │
│  coding Agent    → 写代码、调试、GitHub 管理       │
│  office Agent    → 邮件、日历、项目管理            │
│  social Agent    → 社交消息、闲聊、生活助手        │
│  research Agent  → 信息搜索、内容摘要、分析        │
└──────────────────────────────────────────────────┘
```

配置示例：

```json5
{
  "agents": {
    "list": [
      {
        "id": "coding",
        "skills": ["coding-agent", "github", "gh-issues", "tmux"],
        "model": "anthropic/claude-opus-4-6",
      },
      {
        "id": "office",
        "skills": ["gog", "slack", "notion", "trello", "summarize"],
        "model": "anthropic/claude-sonnet-4-6",
      },
      {
        "id": "social",
        "skills": ["weather", "goplaces", "summarize"],
        "model": "openai/gpt-5.2-mini",
      },
    ],
  },
}
```

### 策略二：按平台分工

每个 Agent 负责一个消息平台：

```
┌──────────────────────────────────────────────────┐
│                  按平台分工                        │
│                                                  │
│  whatsapp Agent  → 处理所有 WhatsApp 消息         │
│  telegram Agent  → 处理所有 Telegram 消息         │
│  discord Agent   → 处理所有 Discord 消息          │
│  slack Agent     → 处理所有 Slack 消息            │
└──────────────────────────────────────────────────┘
```

这种策略适合不同平台有不同用途的场景。比如你用 WhatsApp 跟家人聊天，用 Slack 工作，用 Discord 参与开源社区。

### 策略三：按安全等级分工

根据操作的风险等级来分配 Agent：

```
┌──────────────────────────────────────────────────┐
│                按安全等级分工                       │
│                                                  │
│  trusted Agent   → 有完整权限，只接受你的私聊      │
│  limited Agent   → 有限权限，处理群聊消息          │
│  readonly Agent  → 只读权限，处理公开频道          │
└──────────────────────────────────────────────────┘
```

配置示例：

```json5
{
  "agents": {
    "defaults": {
      "sandbox": {
        // 非主会话在 Docker 沙箱中运行
        "mode": "non-main",
      },
    },
    "list": [
      {
        "id": "trusted",
        "skills": ["coding-agent", "github", "gog", "slack"],
        // 完整权限，只处理私聊
      },
      {
        "id": "limited",
        "skills": ["summarize", "weather", "goplaces"],
        // 有限权限，处理群聊
      },
      {
        "id": "readonly",
        "skills": ["summarize"],
        // 只读权限，处理公开频道
      },
    ],
  },
  "bindings": [
    {
      "agent": "limited",
      "channel": "telegram",
      "chatId": "-100111222333",
    },
    {
      "agent": "readonly",
      "channel": "discord",
      "guildId": "444555666",
    },
  ],
}
```

### 策略四：流水线协作

多个 Agent 按顺序处理同一个任务，每个 Agent 负责一个阶段：

```
研究 Agent → 写作 Agent → 审核 Agent
   │              │              │
   ▼              ▼              ▼
 收集资料      撰写内容       审核质量
 整理要点      格式排版       修改建议
 保存到共享    读取资料       最终发布
```

这种策略可以通过 `sessions_send` 工具直接传递、定时任务或 HTTP API 来串联（详见上面的"Agent 间通信机制"章节）。

## 实战案例

### 案例一：客服 + 技术支持双 Agent

**场景：** 你运营一个开源项目，Discord 服务器里有 #general 频道（闲聊）和 #support 频道（技术支持）。你希望闲聊频道由一个友好的社区 Agent 处理，技术支持频道由一个专业的技术 Agent 处理。

**第一步：创建 Agent**

```bash
openclaw agents add community
openclaw agents add tech-support
```

**第二步：配置 SOUL.md**

`~/.openclaw/workspace-community/SOUL.md`：

```markdown
# Community Agent

你是开源项目 MyProject 的社区助手。

## 性格
- 热情友好，欢迎新成员
- 熟悉项目的基本功能和使用方法
- 会引导用户去正确的频道提问

## 规则
- 不回答深度技术问题，引导用户去 #support 频道
- 不执行任何代码或命令
- 回复简短，适合 Discord 阅读
- 遇到 Bug 报告，引导用户创建 GitHub Issue

## 常用回复模板
- 欢迎新人："欢迎加入！建议先看看我们的文档：https://docs.myproject.dev"
- 技术问题："这个问题建议到 #support 频道提问，那边有专门的技术支持"
- Bug 报告："感谢反馈！请到 GitHub 创建一个 Issue：https://github.com/myproject/issues/new"
```

`~/.openclaw/workspace-tech-support/SOUL.md`：

```markdown
# Tech Support Agent

你是开源项目 MyProject 的技术支持助手。

## 性格
- 专业、耐心、善于解释
- 会一步步引导用户排查问题
- 给出的解决方案要附带代码示例

## 专长
- MyProject 的安装和配置
- API 使用和集成
- 常见错误排查
- 性能优化建议

## 规则
- 只回答跟 MyProject 相关的技术问题
- 不确定的答案要标注"我不确定，建议查看官方文档"
- 复杂问题建议用户创建 GitHub Issue
- 涉及安全漏洞的问题，私信通知项目维护者

## 排查流程
1. 先确认用户的版本号和运行环境
2. 让用户提供错误日志
3. 根据日志定位问题
4. 给出解决方案
5. 确认问题是否解决
```

**第三步：配置路由**

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
      },
      {
        "id": "community",
        "workspace": "~/.openclaw/workspace-community",
        "model": "openai/gpt-5.2-mini",
        "skills": ["summarize"],
      },
      {
        "id": "tech-support",
        "workspace": "~/.openclaw/workspace-tech-support",
        "model": "anthropic/claude-sonnet-4-6",
        "skills": ["coding-agent", "github", "summarize"],
      },
    ],
  },
  "bindings": [
    {
      "agent": "community",
      "channel": "discord",
      "guildId": "111222333",
      "channelId": "444555666",
    },
    {
      "agent": "tech-support",
      "channel": "discord",
      "guildId": "111222333",
      "channelId": "777888999",
    },
  ],
}
```

**效果：**

- #general 频道的消息由 community Agent 处理，用便宜的 GPT-5.2-mini，回复轻松友好
- #support 频道的消息由 tech-support Agent 处理，用更强的 Claude Sonnet，回复专业精准
- 私聊消息由 main Agent 处理

### 案例二：翻译 + 内容创作多 Agent

**场景：** 你是一个内容创作者，需要把中文内容翻译成英文，然后润色发布。你希望有一个翻译 Agent 和一个写作 Agent 协作完成。

**第一步：创建 Agent**

```bash
openclaw agents add translator
openclaw agents add writer
```

**第二步：配置 SOUL.md**

`~/.openclaw/workspace-translator/SOUL.md`：

```markdown
# Translator Agent

你是一个专业的中英翻译助手。

## 翻译原则
- 信、达、雅 -- 准确、通顺、优美
- 技术术语保留英文原文
- 保持原文的语气和风格
- 不添加原文没有的内容

## 输出格式
- 翻译结果保存到 ~/.openclaw/shared/translations/ 目录
- 文件名格式：YYYY-MM-DD-原标题-en.md
- 文件开头标注原文来源和翻译日期

## 工作流程
1. 接收用户的中文内容
2. 分析内容类型（技术文章/博客/社交媒体）
3. 根据类型调整翻译风格
4. 输出翻译结果
5. 标注不确定的翻译，等待用户确认
```

`~/.openclaw/workspace-writer/SOUL.md`：

```markdown
# Writer Agent

你是一个英文内容润色和创作助手。

## 写作风格
- 清晰、简洁、有节奏感
- 适合英文读者的表达习惯
- 避免中式英语
- 善用短句和主动语态

## 工作流程
1. 读取 ~/.openclaw/shared/translations/ 目录中的翻译稿
2. 润色英文表达，使其更地道
3. 调整段落结构，适合目标平台
4. 添加 SEO 友好的标题和摘要
5. 保存到 ~/.openclaw/shared/published/ 目录

## 输出格式
- 博客文章：Markdown 格式，包含 frontmatter
- 社交媒体：纯文本，控制字数
- 技术文档：保持代码块和格式
```

**第三步：配置定时任务串联**

通过 CLI 添加定时任务来串联两个 Agent：

```bash
openclaw cron add --name "translate-new-content" --schedule "0 10 * * *" \
  --agent translator \
  --prompt "检查 ~/.openclaw/shared/drafts/ 目录，翻译所有新的中文稿件，保存到 ~/.openclaw/shared/translations/"

openclaw cron add --name "polish-translations" --schedule "0 11 * * *" \
  --agent writer \
  --prompt "检查 ~/.openclaw/shared/translations/ 目录，润色所有新的翻译稿，保存到 ~/.openclaw/shared/published/"
```

**手动触发的工作流：**

```
你 → translator Agent：帮我翻译这篇文章（粘贴中文内容）
translator Agent → 翻译完成，保存到 shared/translations/2026-02-25-article-en.md

你 → writer Agent：帮我润色 shared/translations/2026-02-25-article-en.md
writer Agent → 润色完成，保存到 shared/published/2026-02-25-article-en.md
```

### 案例三：研究 + 写作 + 审核流水线

**场景：** 你需要定期生成行业研究报告。流程是：研究 Agent 收集资料 → 写作 Agent 撰写报告 → 审核 Agent 检查质量。

**第一步：创建三个 Agent**

```bash
openclaw agents add researcher
openclaw agents add report-writer
openclaw agents add reviewer
```

**第二步：配置各 Agent 的 SOUL.md**

`~/.openclaw/workspace-researcher/SOUL.md`：

```markdown
# Researcher Agent

你是一个专业的行业研究员。

## 研究方法
- 从多个来源收集信息
- 交叉验证关键数据
- 标注信息来源和可信度
- 区分事实和观点

## 输出格式
把研究结果保存到 ~/.openclaw/shared/research/ 目录：

文件结构：
- summary.md -- 研究摘要（500 字以内）
- data.json -- 结构化数据（数字、统计）
- sources.md -- 信息来源列表
- raw-notes.md -- 原始笔记

## 研究模板

### summary.md
- 行业概况（3-5 句话）
- 关键趋势（3-5 个要点）
- 重要数据（表格形式）
- 风险提示
```

`~/.openclaw/workspace-report-writer/SOUL.md`：

```markdown
# Report Writer Agent

你是一个专业的报告撰写者。

## 写作原则
- 数据驱动，每个观点都有数据支撑
- 结构清晰，使用标题和小标题
- 图表优先，能用图表说明的不用文字
- 结论明确，给出可操作的建议

## 工作流程
1. 读取 ~/.openclaw/shared/research/ 目录中的研究资料
2. 根据研究摘要确定报告结构
3. 撰写完整报告
4. 保存到 ~/.openclaw/shared/reports/draft-YYYY-MM-DD.md

## 报告模板
1. 执行摘要
2. 行业背景
3. 关键发现
4. 数据分析
5. 趋势预测
6. 建议和行动项
7. 附录（数据来源）
```

`~/.openclaw/workspace-reviewer/SOUL.md`：

```markdown
# Reviewer Agent

你是一个严格的内容审核员。

## 审核标准
- 事实准确性：数据是否有来源支撑？
- 逻辑一致性：论点和论据是否匹配？
- 完整性：是否遗漏了重要信息？
- 可读性：表达是否清晰易懂？
- 格式规范：标题、图表、引用是否规范？

## 审核流程
1. 读取 ~/.openclaw/shared/reports/ 目录中的报告草稿
2. 逐节审核，标注问题
3. 生成审核报告，保存到 ~/.openclaw/shared/reviews/
4. 审核报告包含：
   - 总体评分（1-10）
   - 问题列表（按严重程度排序）
   - 修改建议
   - 通过/需修改/拒绝 的结论

## 输出格式
审核报告保存为 review-YYYY-MM-DD.md，格式：

### 总体评分：X/10

### 问题列表
1. [严重] 第 3 节的数据来源缺失
2. [中等] 第 5 节的预测缺乏依据
3. [轻微] 第 2 节有一个错别字

### 修改建议
- ...

### 结论：需修改
```

**第三步：配置流水线**

通过 CLI 添加定时任务来串联三个 Agent：

```bash
openclaw cron add --name "weekly-research" --schedule "0 9 * * 1" \
  --agent researcher \
  --prompt "进行本周的 AI 行业研究，收集最新动态、融资信息、产品发布，保存到 shared/research/"

openclaw cron add --name "weekly-report" --schedule "0 14 * * 1" \
  --agent report-writer \
  --prompt "基于 shared/research/ 中的资料，撰写本周 AI 行业研究报告，保存到 shared/reports/"

openclaw cron add --name "weekly-review" --schedule "0 16 * * 1" \
  --agent reviewer \
  --prompt "审核 shared/reports/ 中最新的报告草稿，生成审核报告保存到 shared/reviews/"
```

每周一的流程：
- 9:00 -- researcher Agent 收集资料
- 14:00 -- report-writer Agent 撰写报告
- 16:00 -- reviewer Agent 审核报告

你只需要在周一下午查看审核结果，根据修改建议做最终调整。

## Agent 的工具和权限分配

### 为什么要限制 Agent 的工具？

默认情况下，每个 Agent 可以使用所有已安装的技能和工具。但这不是最佳实践：

1. **安全风险** -- 社交 Agent 不应该有执行 Shell 命令的能力
2. **上下文浪费** -- 加载不需要的技能会浪费 token
3. **误触发** -- 技能越多，误触发的概率越高

### 技能白名单配置

为每个 Agent 配置只需要的技能：

```json5
{
  "agents": {
    "list": [
      {
        "id": "coding",
        // Agent 级别的 skills 是简单的字符串数组
        "skills": ["coding-agent", "github", "gh-issues", "tmux"],
      },
      {
        "id": "office",
        "skills": ["gog", "slack", "notion", "trello", "summarize"],
      },
      {
        "id": "social",
        "skills": ["weather", "goplaces", "summarize"],
      },
    ],
  },

  // 技能的详细配置放在顶层 skills.entries 中
  "skills": {
    "entries": {
      "coding-agent": {
        "config": {
          "workDir": "~/projects",
          "allowedCommands": ["npm", "node", "git", "tsc", "pnpm"],
          "autoApprove": false,
        },
      },
      "gog": {
        "config": {
          "timezone": "Asia/Shanghai",
          "language": "zh-CN",
        },
      },
    },
  },
}
```

> ⏭️ **小白可跳过** — 默认的沙箱配置已经足够安全

### 沙箱隔离

对于处理不可信消息的 Agent（比如公开频道的 Agent），建议启用沙箱。OpenClaw 使用 `mode: "non-main"` 模式，让非主会话在 Docker 沙箱中运行：

```json5
{
  "agents": {
    "defaults": {
      "sandbox": {
        // 非主会话自动在 Docker 沙箱中运行
        "mode": "non-main",
      },
    },
  },
}
```

**工具 allowlist 和 denylist：**

沙箱环境中，Agent 可用的工具受到严格限制：

| 类型 | 工具列表 |
|------|----------|
| allowlist（允许使用） | `bash`, `process`, `read`, `write`, `edit`, `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn` |
| denylist（禁止使用） | `browser`, `canvas`, `nodes`, `cron`, `discord`, `gateway` |

allowlist 中的工具是 Agent 在沙箱中可以调用的全部工具。denylist 中的工具即使在 allowlist 中也会被阻止，确保沙箱内的 Agent 无法访问浏览器、管理 Gateway 或操作 Discord 等外部服务。

### 认证隔离

每个 Agent 的认证凭证是独立的：

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

main Agent 的 Google 凭证不会自动共享给 coding Agent。如果 coding Agent 也需要访问 Google，需要单独认证：

```bash
# 为 coding Agent 认证 Google
openclaw models auth login --provider google --agent coding

# 为 coding Agent 认证 GitHub
openclaw models auth login --provider github --agent coding
```

如果你确实需要共享凭证，可以手动复制：

```bash
cp ~/.openclaw/agents/main/agent/auth-profiles.json \
   ~/.openclaw/agents/coding/agent/auth-profiles.json
```

但不推荐这样做 -- 独立认证更安全，而且可以为不同 Agent 使用不同的账号。

## Agent 性能监控

### 查看 Agent 使用统计

```bash
# 查看所有 Agent
openclaw agents list

# 查看活跃会话
openclaw sessions list

# 清理过期会话
openclaw sessions cleanup
```

### 监控关键指标

| 指标 | 说明 | 健康范围 | 异常处理 |
|------|------|----------|----------|
| 响应时间 | 从收到消息到发出回复 | < 10s | 检查模型选择和网络 |
| Token 消耗 | 每条消息的平均 token 数 | < 5000 | 检查技能加载是否过多 |
| 错误率 | 工具调用失败的比例 | < 5% | 检查工具配置和权限 |
| 会话长度 | 平均每个会话的消息数 | 因场景而异 | 检查是否需要优化 SOUL.md |

### 成本优化建议

**1. 为低复杂度任务使用便宜的模型**

```json5
{
  "agents": {
    "list": [
      {
        "id": "social",
        "model": "openai/gpt-5.2-mini",
        // 闲聊用便宜模型
      },
    ],
  },
}
```

**2. 限制技能加载数量**

每个加载的技能都会增加系统提示词的长度，消耗更多 input token。只启用真正需要的技能。

**3. 调整会话压缩阈值**

```json5
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 15000,
        // 更早压缩会话，减少 token 消耗
      },
    },
  },
}
```

**4. 使用模型故障转移降低成本**

Agent 的 `model` 字段支持故障转移配置：

```json5
{
  "agents": {
    "list": [
      {
        "id": "work",
        // model 可以是对象形式，指定主模型和备用模型
        "model": {
          "primary": "anthropic/claude-sonnet-4-6",
          "fallbacks": [
            "openai/gpt-5.2-mini",
            "ollama/llama3.1",
          ],
        },
      },
    ],
  },
}
```

主模型不可用时自动切换到备用模型列表中的下一个。注意字段名是 `fallbacks`（复数形式）。

## 自定义 Agent 开发

### 从零创建一个专业 Agent

下面我们从零开始创建一个"DevOps 监控 Agent"，它能监控服务器状态、处理告警、执行简单的运维操作。

**第一步：创建 Agent**

```bash
openclaw agents add devops
```

**第二步：编写 SOUL.md**

`~/.openclaw/workspace-devops/SOUL.md`：

```markdown
# DevOps Agent

你是一个专业的 DevOps 运维助手，负责监控服务器状态和处理告警。

## 性格
- 冷静、精确、注重细节
- 遇到紧急情况会立即通知用户
- 操作前会确认，操作后会验证

## 专长
- 服务器状态监控
- 日志分析和错误排查
- Docker 容器管理
- 简单的运维操作（重启服务、清理磁盘等）

## 安全规则（最重要）
- 永远不要执行 rm -rf 或类似的危险命令
- 重启服务前必须确认用户意图
- 不修改防火墙规则
- 不修改 SSH 配置
- 所有操作都要记录到日志

## 告警处理流程
1. 收到告警 → 分析告警内容
2. 判断严重程度（P0/P1/P2/P3）
3. P0/P1 → 立即通知用户 + 尝试自动修复
4. P2/P3 → 记录到日志 + 下次汇报时提及

## 自动修复策略
- 磁盘空间不足 → 清理 Docker 无用镜像和日志
- 服务无响应 → 尝试重启服务（最多 3 次）
- 内存使用过高 → 识别占用最多的进程并报告
- CPU 持续高负载 → 收集 top 信息并报告

## 日报格式
每天 18:00 生成运维日报：
- 服务器健康状态概览
- 今日告警统计
- 资源使用趋势
- 需要关注的问题
```

**第三步：创建工作空间技能**

```bash
mkdir -p ~/.openclaw/workspace-devops/skills/server-monitor
```

`~/.openclaw/workspace-devops/skills/server-monitor/skill.md`：

````markdown
---
name: server-monitor
description: 服务器监控和运维操作
triggers:
  - 服务器状态
  - 检查服务
  - 磁盘空间
  - 内存使用
  - 重启服务
tools:
  - shell_exec
  - file_write
  - file_read
permissions:
  - shell_exec
  - file_write
  - file_read
category: system
---

# 服务器监控技能

## 健康检查

当用户要求检查服务器状态时，执行以下命令并整理结果：

```bash
# CPU 和内存
top -bn1 | head -20

# 磁盘空间
df -h

# Docker 容器状态
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 最近的错误日志
journalctl --since "1 hour ago" --priority err --no-pager | tail -20
```

## 服务管理

当用户要求重启服务时：
1. 确认服务名称
2. 检查服务当前状态：`systemctl status <service>`
3. 确认用户意图："确定要重启 <service> 吗？"
4. 执行重启：`systemctl restart <service>`
5. 验证重启结果：`systemctl status <service>`
6. 记录操作到日志
````

**第四步：配置路由和定时任务**

```json5
{
  "agents": {
    "list": [
      {
        "id": "devops",
        "workspace": "~/.openclaw/workspace-devops",
        "model": "anthropic/claude-sonnet-4-6",
        "skills": ["server-monitor", "summarize"],
      },
    ],
  },
  "bindings": [
    {
      "agent": "devops",
      "channel": "slack",
      "teamId": "T01234567",
      "channelId": "C-ops-channel",
    },
  ],
  "cron": {
    "enabled": true,
  },
}
```

通过 CLI 添加定时任务：

```bash
openclaw cron add --name "health-check" --schedule "*/30 * * * *" \
  --agent devops \
  --prompt "执行服务器健康检查，如果发现异常，通过 Slack 通知 #ops 频道"

openclaw cron add --name "daily-report" --schedule "0 18 * * *" \
  --agent devops \
  --prompt "生成今日运维日报，发送到 Slack #ops 频道"
```

### Agent 开发最佳实践

**1. SOUL.md 要具体，不要模糊**

```markdown
# 差的写法
你是一个助手，帮用户做事。

# 好的写法
你是一个 TypeScript 编程助手。
- 所有代码使用 TypeScript 严格模式
- 遵循 Airbnb 代码风格
- 函数必须有 JSDoc 注释
- 不使用 any 类型
```

**2. 明确定义边界**

在 SOUL.md 中明确说明 Agent 不应该做什么：

```markdown
## 不要做的事
- 不要执行任何 Shell 命令
- 不要修改系统文件
- 不要回答跟你职责无关的问题
- 不要泄露其他用户的信息
```

**3. 提供错误处理指引**

```markdown
## 异常处理
- 如果工具调用失败，告诉用户具体的错误信息
- 如果不确定答案，说"我不确定"而不是编造
- 如果用户的请求超出你的能力范围，建议他们联系人工支持
```

**4. 定期审查和优化**

每周检查一次：
- Agent 的响应质量是否符合预期？
- 有没有误触发或漏触发的情况？
- Token 消耗是否合理？
- SOUL.md 是否需要更新？

## Agent 调试技巧

### 开启详细日志

```bash
# 启动 Gateway 时开启 Agent 调试
openclaw gateway --verbose --agent-debug

# 或者在配置中开启
```

```json5
{
  "logging": {
    "level": "debug",
  },
}
```

开启后，你会在日志中看到：

```
[AGENT] Message received from telegram:chat=-100123456789
[AGENT] Routing: matched binding → agent=social
[AGENT] Loading workspace: ~/.openclaw/workspace-social
[AGENT] Loading SOUL.md (tokens: 320)
[AGENT] Loading MEMORY.md (tokens: 150)
[AGENT] Loading skills: weather, goplaces, summarize
[AGENT] Total system prompt tokens: 1,850
[AGENT] Calling model: openai/gpt-5.2-mini
[AGENT] Model response received (tokens: 120, time: 1.2s)
[AGENT] Sending response to telegram:chat=-100123456789
```

### 常见问题排查

**问题：消息没有路由到正确的 Agent**

排查步骤：

1. 检查 bindings 配置是否正确：
```bash
openclaw agents list
```

2. 确认频道 ID 是否正确（Discord 和 Telegram 的 ID 格式不同）

3. 检查是否有多个 Agent 绑定了同一个频道（先匹配的会生效）

4. 查看路由日志：
```bash
openclaw gateway --verbose 2>&1 | grep "AGENT.*Routing"
```

**问题：Agent 的回复不符合 SOUL.md 的设定**

排查步骤：

1. 确认 SOUL.md 文件路径正确（在 Agent 的工作空间根目录下）

2. 检查 SOUL.md 是否被正确加载：
```bash
openclaw gateway --verbose 2>&1 | grep "Loading SOUL"
```

3. SOUL.md 的指令是否太模糊？尝试用更具体的语言

4. 是否有其他技能的指令覆盖了 SOUL.md 的设定？检查技能优先级

**问题：Agent 的工具调用失败**

排查步骤：

1. 检查技能是否正确启用（查看 `openclaw.json` 中对应 Agent 的 `skills` 数组配置）

2. 检查工具依赖是否安装（如 `gh`、`ffmpeg`）

3. 检查权限配置（确认工具在沙箱 allowlist 中）

4. 查看工具调用日志：
```bash
openclaw gateway --verbose 2>&1 | grep "Tool call"
```

**问题：Agent 之间的共享文件不同步**

排查步骤：

1. 确认共享目录存在且两个 Agent 都有读写权限

2. 检查定时任务的执行顺序（写入 Agent 必须先于读取 Agent 执行）

3. 查看会话日志（使用 sessions_history 工具或检查 Gateway 日志）

### 使用 WebChat 调试

WebChat 是调试 Agent 最方便的工具。你可以在浏览器中直接跟任意 Agent 对话：

```bash
# 启动 Gateway（如果还没启动）
openclaw gateway --port 18789

# 打开浏览器访问
# http://localhost:18789/chat?agent=coding
# http://localhost:18789/chat?agent=social
```

通过 URL 参数 `?agent=<agentId>` 可以指定跟哪个 Agent 对话，方便逐个测试。

## 常见问题

### 最多能创建多少个 Agent？

没有硬性限制，但每个 Agent 都会占用一些磁盘空间（工作空间、会话历史、记忆文件）。实际使用中，3-5 个 Agent 是比较常见的配置。超过 10 个 Agent 可能会让管理变得复杂。

### Agent 之间能共享记忆吗？

默认不能。每个 Agent 有独立的 MEMORY.md 和每日日志。如果你需要共享某些信息，可以：

1. 把共享信息写入公共目录（如 `~/.openclaw/shared/`）
2. 在每个 Agent 的 SOUL.md 中指示它读取公共目录
3. 手动复制记忆文件（不推荐，容易冲突）
4. 使用 Memory Wiki 插件（`memory-wiki`，v2026.4.12+ 可用）-- 提供结构化的知识页面层，支持确定性的页面组织和跨 Agent 共享查询。详见官方文档 [memory-wiki](https://docs.openclaw.ai/concepts/memory)
5. 使用 Honcho 后端 -- 支持跨会话、多 Agent 感知的记忆系统

### 能不能让一个 Agent 调用另一个 Agent？

可以。OpenClaw 提供了 Sessions 工具来实现 Agent 间的直接通信：

- `sessions_list` -- 发现活跃会话
- `sessions_send` -- 向另一个会话发消息（支持 reply-back ping-pong 和 announce step 模式）
- `sessions_spawn` -- 生成新的 Agent 会话

如果不需要实时通信，也可以使用定时任务 + 共享文件的方式（参见"Agent 间通信机制"章节）。

### 删除 Agent 会丢失数据吗？

删除 Agent 会移除 Agent 的状态目录（`~/.openclaw/agents/<agentId>/`），但不会删除工作空间目录。你的 SOUL.md、记忆文件、技能文件都还在。如果要彻底清理，需要手动删除工作空间目录。

### 多个 Agent 绑定同一个频道会怎样？

只有第一个匹配的 Agent 会处理消息。如果你不小心把两个 Agent 绑定到了同一个频道，检查 `openclaw.json` 中 `agents.list` 的顺序 -- 排在前面的 Agent 优先匹配。

### Agent 的会话是独立的吗？

是的，完全独立。coding Agent 的对话历史不会出现在 social Agent 的上下文中。这是设计如此 -- 保证每个 Agent 的上下文干净、专注。

### 如何迁移 Agent 到另一台机器？

复制以下目录到新机器：

```bash
# Agent 状态（认证凭证、会话历史）
~/.openclaw/agents/<agentId>/

# Agent 工作空间（SOUL.md、记忆、技能）
~/.openclaw/workspace-<agentId>/
```

然后在新机器的 `openclaw.json` 中添加对应的 Agent 配置。

### 多 Agent 模式下 Gateway 的资源消耗会增加吗？

Gateway 本身的资源消耗不会显著增加。Agent 是按需加载的 -- 只有收到消息时才会激活对应的 Agent。空闲的 Agent 不占用 CPU 和内存。主要的额外消耗来自：

- 磁盘空间：每个 Agent 的工作空间和会话历史
- AI API 调用：每个 Agent 独立计费

> v2026.4.20+ 优化了插件启动性能（冷启动时间降低约 74%，依赖加载时间降低 82-90%），多 Agent 场景下 Gateway 的首次响应速度明显改善。

### 能不能动态创建和销毁 Agent？

Agent 的创建需要通过 CLI 命令（`openclaw agents add`）。但在运行时，Agent 可以通过 `sessions_spawn` 工具动态生成新的会话，实现临时任务的分发。

## 下一步

多 Agent 协作搞定！去 [09. Docker 部署](09-Docker部署指南.md) 学习如何把 OpenClaw 容器化部署到服务器上！
