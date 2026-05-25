# 01. OpenClaw 项目介绍

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **难度等级**：🟢 入门
> - **阅读时间**：15 分钟
> - **前置知识**：无
>
> **本篇你将了解：** OpenClaw 是什么、能做什么、跟其他框架有什么区别、核心架构长什么样
>
> **小白速通：** 只看前 3 节（"一句话说清楚"、"发展历史"、"与其他 AI 助手框架的对比"），其余章节可以等需要时再回来看

## 一句话说清楚

<p align="center"><img src="../../images/official/openclaw-model-picker.png" alt="OpenClaw 官方模型选择与配置界面" width="720"/></p>

<p align="center"><img src="../../images/official/openclaw-agents-ui.jpg" alt="OpenClaw 官方 Agent 与技能管理界面" width="720"/></p>

<p align="center"><img src="../../images/official/openclaw-quick-settings-browser-tools.png" alt="OpenClaw 官方 Control UI 设置与浏览器工具界面" width="720"/></p>

OpenClaw 是一个**开源的 AI 私人助手框架**，跑在你自己的电脑或服务器上，能连接 WhatsApp、Telegram、Discord 等消息平台，让 AI 帮你处理消息、执行任务、管理日程。

你可以把它理解为：**一个 7x24 小时在线的 AI 员工，通过你常用的聊天软件跟你沟通。**

跟那些云端 AI 助手不同，OpenClaw 的所有数据都在你自己的设备上。你的聊天记录、偏好设置、工作文件，全部本地存储。没有第三方服务器偷看你的数据，没有月费订阅锁定你的工作流。

## 发展历史

OpenClaw 的故事可以简单理解成：一个从个人实验起步、很快获得开发者社区关注、经历过名称演化，最终稳定为 OpenClaw 的开源 AI 助手项目。

```
2025年11月    Peter Steinberger 从个人实验出发，把 AI 模型接入消息应用
                      ↓
2025年11月    项目以早期名称开源发布，快速获得社区关注
                      ↓
2026年1月     因名称与 Claude 过近，项目进入更名过程
                      ↓
2026年1月末   社区投票后，最终定名为 OpenClaw
                      ↓
2026年4月     Control UI 多语言、插件懒加载优化、Google Meet 集成等密集发布
                      ↓
2026年        持续快速迭代，围绕 Gateway、Channels、Skills、Plugins 等能力扩展
```

为什么增长这么快？因为它解决了一个真实痛点：**每个人都想要一个私人 AI 助手，但没人想把所有数据交给云端。** OpenClaw 让你在自己的设备上跑 AI，通过你已经在用的聊天软件交互，零学习成本。

### 关键里程碑

| 时间 | 事件 | 意义 |
|------|------|------|
| 2025.11 | 项目创建 | 从个人 AI 实验起步 |
| 2025.11 | 开源发布 | 快速进入开发者社区视野 |
| 2026.01 | 完成更名 | 统一到 OpenClaw 品牌 |
| 2026.04.05 | Control UI 多语言 | 新增 12 种界面语言 |
| 2026.04.22 | 插件懒加载优化 | 内置插件加载时间缩短 82-90% |
| 2026.04.24 | Google Meet 集成 | 首个内置会议类插件；DeepSeek V4 Flash 成为引导默认模型 |
| 2026 年后 | 持续高频迭代 | 版本号采用 `YYYY.M.D` 风格 |

## 与其他 AI 助手框架的对比

市面上做 AI 助手/聊天机器人的框架不少，OpenClaw 的定位跟它们有本质区别。

### OpenClaw vs Botpress

| 维度 | OpenClaw | Botpress |
|------|----------|----------|
| 定位 | 个人 AI 助手 | 企业级聊天机器人平台 |
| 部署 | 本地优先，跑在你自己设备上 | 云端 SaaS 为主 |
| 数据 | 全部本地存储 | 存在 Botpress 云端 |
| AI 模型 | 支持多个主流模型提供商，具体目录以当前版本为准 | 主要绑定自家模型 |
| 目标用户 | 开发者、技术爱好者 | 企业客服团队 |
| 对话设计 | 自然语言驱动，无需流程图 | 可视化流程编辑器 |
| 价格 | 完全免费开源（MIT） | 免费层有限，企业版收费 |

Botpress 适合做客服机器人，有可视化的对话流程编辑器，适合非技术人员。OpenClaw 不做客服，它是你的私人助手 -- 帮你管邮件、写代码、控制智能家居。

### OpenClaw vs Rasa

| 维度 | OpenClaw | Rasa |
|------|----------|------|
| 架构 | Gateway（核心服务进程，负责接收和分发消息） + Agent（独立的 AI 助手实例） 循环 | NLU + 对话管理 + 动作服务器 |
| 学习曲线 | `npm install -g openclaw` 就能跑 | 需要理解 NLU 管道、训练数据格式 |
| AI 能力 | 直接调用大语言模型 | 传统 NLU + 可选 LLM |
| 消息平台 | 内置 15+ 平台支持 | 需要自己写 Connector |
| 工具调用 | 内置浏览器控制、文件操作等 | 需要自己实现 Action Server |
| 适用场景 | 个人助手、开发者工具 | 企业级对话系统 |

Rasa 是传统 NLU 路线的代表，需要标注训练数据、定义意图和实体。OpenClaw 直接站在大语言模型的肩膀上，不需要训练数据，开箱即用。

### OpenClaw vs 自建方案

很多开发者会想：我直接调 OpenAI API + 写个 Telegram Bot 不就行了？

当然可以，但你很快会遇到这些问题：

```
自建方案需要解决的问题：
├── 消息平台适配（每个平台 API 都不一样）
├── 会话管理（多轮对话、上下文窗口）
├── 流式输出（实时显示 AI 回复）
├── 工具调用（让 AI 执行实际操作）
├── 记忆系统（AI 记住你的偏好）
├── 安全控制（防止未授权访问）
├── 多模型切换（不同任务用不同模型）
├── 模型故障转移（主模型挂了自动切备用）
├── 媒体处理（图片、音频、视频）
├── 守护进程管理（7x24 小时运行）
└── 更新维护（持续跟进 API 变更）
```

OpenClaw 把这些基础设施大部分都预先做好了。现在官方更推荐的上手方式是运行安装脚本，再进入 `openclaw onboard` 完成初始化；如果你更习惯 Node 生态，也仍然可以用 npm / pnpm / bun 安装 CLI。

### 选择建议

| 你的需求 | 推荐方案 |
|----------|----------|
| 个人 AI 助手，隐私优先 | OpenClaw |
| 企业客服机器人，需要可视化 | Botpress |
| 企业级对话系统，需要精确控制 | Rasa |
| 简单的单平台 Bot | 自建方案 |
| 多平台 + 多模型 + 工具调用 | OpenClaw |

## 核心架构

OpenClaw 的架构设计非常优雅。官方的自我定义是：**Multi-channel AI gateway with extensible messaging integrations**（多通道 AI 网关，带可扩展的消息集成）。

核心就三层：

```
┌─────────────────────────────────────────────────────────────────┐
│                        消息平台层 (Channels)                      │
│                                                                   │
│  WhatsApp │ Telegram │ Discord │ Slack │ Signal │ iMessage       │
│  BlueBubbles │ Google Chat │ Teams │ LINE │ Zalo │ WebChat │ ... │
└──────────────────────────────┬────────────────────────────────────┘
                               │
┌──────────────────────────────▼────────────────────────────────────┐
│                    Gateway（网关控制平面）                          │
│                    ws://127.0.0.1:18789                           │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ 路由引擎  │  │ 会话管理  │  │ 安全控制  │  │ WebSocket API  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ 技能系统  │  │ 记忆系统  │  │ 工具系统  │  │ 插件系统       │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Cron 调度 │  │ Webhook  │  │ 媒体管道  │  │ Control UI     │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Pi Agent Runtime   │
                    │  (RPC 模式)          │
                    └──────────┬──────────┘
                               │
┌──────────────────────────────▼────────────────────────────────────┐
│                     AI 模型提供商层 (Models)                       │
│                                                                   │
│  OpenAI │ Anthropic │ Google │ Ollama │ Mistral │ xAI            │
│  AWS Bedrock │ 通义千问 │ 智谱 │ DeepSeek │ OpenRouter │ ...    │
└───────────────────────────────────────────────────────────────────┘
```

### 数据流：一条消息的旅程

当你在 WhatsApp 上给 OpenClaw 发一条消息，背后发生了什么？

```
1. WhatsApp 消息到达
   │
2. Baileys 库接收消息，转换为统一格式
   │
3. Gateway 路由引擎判断：
   ├── 这条消息属于哪个 Agent？
   ├── 发送者是否已授权？（DM 配对检查）
   └── 是否在群聊中被 @提及？
   │
4. 会话管理器加载/创建会话：
   ├── 加载历史上下文
   ├── 加载记忆文件（MEMORY.md + 今日日志）
   └── 加载技能指令
   │
5. Pi Agent 执行推理循环：
   ├── 组装完整 Prompt（系统指令 + 记忆 + 历史 + 用户消息）
   ├── 调用 AI 模型（如 Claude Opus 4.6）
   ├── 模型返回文本或工具调用请求
   ├── 如果是工具调用 → 执行工具 → 把结果喂回模型
   └── 循环直到模型给出最终回复
   │
6. 流式输出：
   ├── AI 的回复实时推送到 WhatsApp
   ├── 同时推送到 WebChat UI（如果打开了的话）
   └── 打字指示器让对方知道 AI 在"思考"
   │
7. 状态持久化：
   ├── 会话历史写入磁盘
   ├── 如果 AI 决定记住什么 → 写入记忆文件
   └── 使用统计更新
```

这个流程的关键设计决策：

- **每个会话串行执行** — 同一个会话里的消息排队处理，防止竞态条件
- **流式输出** — 不用等 AI 想完再发，实时看到回复
- **工具调用循环** — AI 可以连续调用多个工具，直到任务完成

> ⏭️ **小白可跳过** — 这部分是技术深入分析，新手可以先跳过

## 核心概念详解

### Gateway（网关）

Gateway 是 OpenClaw 的心脏，一个长期运行的守护进程（daemon）。它不是一个简单的 HTTP 服务器，而是一个完整的控制平面（control plane）。

Gateway 的职责：

```
Gateway 核心职责：
├── 连接管理
│   ├── 管理所有消息平台的长连接
│   ├── WhatsApp 用 Baileys，Telegram 用 grammY，Discord 用 @buape/carbon
│   ├── 自动重连、心跳保活
│   └── 统一消息格式转换
│
├── 会话管理
│   ├── main 会话（直接聊天）
│   ├── 群聊隔离（每个群独立会话）
│   ├── 激活模式（@提及、关键词触发等）
│   └── 队列模式（消息排队处理）
│
├── Agent 调度
│   ├── 多 Agent 路由（不同平台/联系人 → 不同 Agent）
│   ├── 每个 Agent 独立工作空间
│   └── 独立的认证和配置
│
├── 安全控制
│   ├── DM 配对机制（未知发送者需要验证码）
│   ├── 允许列表（allowFrom）
│   └── 权限隔离
│
├── API 暴露
│   ├── WebSocket API（默认 127.0.0.1:18789）
│   ├── Control UI（Web 控制面板）
│   └── WebChat（浏览器聊天界面）
│
└── 自动化
    ├── Cron 定时任务
    ├── Webhook 接收
    └── Gmail Pub/Sub 推送
```

Gateway 的安装方式是注册为系统服务：macOS 用 launchd，Linux 用 systemd。这样它会开机自启，7x24 小时运行。

```bash
# 安装 Gateway 守护进程
openclaw onboard --install-daemon

# 手动启动（调试用）
openclaw gateway --port 18789 --verbose

# 检查 Gateway 健康状态
openclaw doctor
```

### Channel（消息平台抽象层）

Channel 是 OpenClaw 对消息平台的统一抽象。不管你用的是 WhatsApp 还是 Telegram，对 Gateway 来说都是一个 Channel。

每个 Channel 需要处理的事情：

| 能力 | 说明 |
|------|------|
| 消息收发 | 文本、图片、音频、视频、文件 |
| 群聊支持 | @提及检测、回复引用、群成员信息 |
| 打字指示器 | 让对方看到"正在输入..." |
| 消息分块 | 长消息自动拆分（不同平台限制不同） |
| 媒体处理 | 图片压缩、音频转码、视频帧提取 |
| 认证管理 | 每个平台的认证方式不同 |

目前支持的 Channel 分为两类：

**核心 Channel（src/ 目录下有独立实现）：**

| 平台 | 集成库 | 认证方式 |
|------|--------|----------|
| WhatsApp | Baileys (Web 协议) | 扫码配对 |
| Telegram | grammY | Bot Token |
| Discord | @buape/carbon | Bot Token |
| Slack | Bolt | OAuth App |
| Signal | signal-cli | 手机号注册 |
| BlueBubbles | BlueBubbles API | iMessage（推荐） |
| iMessage | imsg CLI | macOS 原生（旧版） |
| WebChat | 内置 | 无需认证 |

**扩展 Channel（通过 extensions 加载）：**

| 平台 | 说明 |
|------|------|
| Google Chat | Google Workspace 集成 |
| Google Meet | 会议参与者插件（v2026.4.24 新增） |
| Microsoft Teams | 企业通信平台 |
| Matrix | 去中心化通信协议 |
| Zalo | 越南主流通信应用 |
| Zalo Personal | Zalo 个人账号 |
| LINE | 日本/东南亚主流 |
| 飞书 (Feishu) | 字节跳动企业通信平台 |

Channel 的安全默认值很重要。OpenClaw 连接的是真实的消息平台，所以对陌生人的 DM 默认采用**配对模式**（pairing）：

```
陌生人发消息 → OpenClaw 返回一个配对码 → 你在终端确认
                                          ↓
                              openclaw pairing approve telegram ABC123
                                          ↓
                              该用户被加入允许列表，后续消息正常处理
```

### Skills（技能系统）

如果说工具（Tools）是 AI 的双手，那技能（Skills）就是教 AI 如何组合使用这些工具的教科书。

技能的本质是一组**系统指令 + 工具定义**，告诉 AI 在特定场景下应该怎么做。

```
工具 (Tools) = 单个原子操作
    例：读文件、发 HTTP 请求、执行 Shell 命令

技能 (Skills) = 组合工具完成复杂任务的知识
    例：管理 GitHub Issue = 搜索 Issue + 读取详情 + 添加评论 + 修改标签
```

技能分三个层级：

| 层级 | 说明 | 来源 |
|------|------|------|
| Bundled Skills | 内置技能，随 OpenClaw 一起安装 | 核心仓库 |
| Managed Skills | 通过 ClawHub 安装的社区技能 | clawhub.com |
| Workspace Skills | 你自己写的本地技能 | 工作空间目录 |

内置技能一览（示意）：

| 类别 | 技能 | 功能 |
|------|------|------|
| 办公效率 | `gog` | Google Workspace（邮件、日历、文档） |
| | `notion` | Notion 页面和数据库管理 |
| | `trello` | Trello 看板和任务管理 |
| | `slack` | Slack 工作区消息管理 |
| | `1password` | 1Password 密码查询（只读） |
| 笔记管理 | `obsidian` | Obsidian 笔记搜索和管理 |
| | `apple-notes` | Apple 备忘录 |
| | `bear-notes` | Bear 笔记 |
| 开发工具 | `coding-agent` | 编程助手（写代码、调试、重构） |
| | `github` | GitHub 仓库管理、PR、Issue |
| | `gh-issues` | GitHub Issues 专项管理 |
| | `tmux` | 终端会话管理 |
| 任务管理 | `apple-reminders` | Apple 提醒事项 |
| | `things-mac` | Things 任务管理 |
| 多媒体 | `spotify-player` | Spotify 音乐控制 |
| | `voice-call` | 语音通话（ElevenLabs） |
| | `peekaboo` | 屏幕截图 |
| | `camsnap` | 摄像头拍照 |
| | `video-frames` | 视频帧提取 |
| 实用工具 | `weather` | 天气查询 |
| | `summarize` | 内容摘要 |
| | `nano-pdf` | PDF 处理 |
| | `skill-creator` | 创建自定义技能 |
| 系统管理 | `healthcheck` | 系统健康检查 |
| | `session-logs` | 会话日志查看 |
| | `model-usage` | 模型使用统计 |

### Memory（记忆系统）

OpenClaw 的记忆系统设计哲学是：**简单到极致**。

没有向量数据库，没有 RAG 管道，没有 Embedding 索引。AI 的记忆就是写在磁盘上的 Markdown 文件。

```
~/.openclaw/workspace/
├── MEMORY.md              # 长期记忆（精选的重要信息）
└── memory/
    ├── 2026-02-25.md      # 今天的日志
    ├── 2026-02-24.md      # 昨天的日志
    └── ...                # 更早的日志
```

两层记忆架构：

| 层级 | 文件 | 内容 | 加载时机 |
|------|------|------|----------|
| 长期记忆 | `MEMORY.md` | 你的偏好、重要决策、关键事实 | 每次会话启动 |
| 每日日志 | `memory/YYYY-MM-DD.md` | 当天的笔记和上下文 | 加载今天 + 昨天 |

AI 有两个记忆工具：
- `memory_search` — 语义搜索所有记忆文件
- `memory_get` — 精确读取特定记忆内容

这个设计的好处：
- **可读** — 你随时可以打开 Markdown 文件看 AI 记住了什么
- **可编辑** — 你可以直接修改记忆文件，删掉不想让 AI 记住的东西
- **可版本控制** — 放进 Git 就能追踪记忆变化
- **零依赖** — 不需要额外的数据库服务

记忆系统是一个插件槽位（plugin slot），同一时间只能有一个记忆插件激活。官方计划未来收敛到一个推荐的默认方案。

### Tools（工具系统）

工具是 AI 执行实际操作的能力。OpenClaw 内置了一套强大的工具集：

| 工具类别 | 能力 | 说明 |
|----------|------|------|
| 浏览器控制 | 打开网页、截图、点击、填表 | 基于 Playwright，有专用的 Chrome 实例 |
| Canvas | 可视化工作区 | Agent 驱动的 UI，支持 A2UI 推送 |
| 节点操作 | 摄像头、屏幕录制、位置获取 | 通过 macOS/iOS/Android 节点 |
| 文件操作 | 读写文件、目录管理 | 在工作空间内操作 |
| Shell 执行 | 运行命令行命令 | 安全沙箱内执行 |
| 消息发送 | 通过任意 Channel 发消息 | 跨平台消息推送 |
| 定时任务 | Cron 表达式调度 | 定时提醒、自动化任务 |
| Webhook | 接收外部事件 | 与第三方服务集成 |

工具调用的安全模型：AI 请求调用工具 → Gateway 检查权限 → 执行工具 → 返回结果给 AI。

### Plugin（插件系统）

OpenClaw 的核心保持精简，可选功能通过插件扩展。

自 v2026.4.22 起，内置插件采用懒加载和 manifest 驱动的激活方式，**实测加载时间缩短 82-90%**，显著改善了 CLI 和 Gateway 的启动速度。

插件的分发方式：
- **npm 包** — 通过 npm 安装，标准的 Node.js 包管理
- **本地扩展** — 开发时直接加载本地目录
- **社区插件** — 通过 ClawHub（clawhub.com）发现和安装

插件 API 提供了 SDK：

```typescript
// 插件 SDK 导入
import { ... } from 'openclaw/plugin-sdk'
```

官方对插件的态度是：**核心仓库的门槛很高**。大部分新功能应该作为独立插件发布到 ClawHub，而不是合并到核心代码。

### MCP 支持

OpenClaw 通过 `mcporter` 桥接支持 MCP（Model Context Protocol）：

```
OpenClaw Gateway ←→ mcporter ←→ MCP Servers
```

这种桥接模式的好处：
- 添加或更换 MCP 服务器不需要重启 Gateway
- 核心工具/上下文保持精简
- MCP 生态的变动不影响核心稳定性

> ⏭️ **小白可跳过** — 这部分是技术深入分析，新手可以先跳过

## 技术栈详解

### 为什么选 TypeScript？

官方的回答很直接：OpenClaw 本质上是一个**编排系统**（orchestration system）—— 处理 Prompt、工具、协议和集成。TypeScript 被选中是因为：

- **广泛使用** — 大多数开发者都能读懂和修改
- **迭代快** — 动态类型 + 类型检查的平衡
- **生态丰富** — npm 上有几乎所有消息平台的 SDK
- **易于扩展** — 插件开发门槛低

### 核心依赖

从 `package.json` 可以看到 OpenClaw 的技术选型：

| 类别 | 库 | 用途 |
|------|-----|------|
| 运行时 | Node.js 24.x 推荐，22.19+ 兼容 | 服务端 JavaScript 运行时 |
| 语言 | TypeScript 5.9+ | 类型安全 |
| 构建 | tsdown | TypeScript 打包工具 |
| 测试 | Vitest 4.x | 单元测试 + E2E 测试 |
| 代码质量 | oxlint + oxfmt | Lint + 格式化（Rust 写的，极快） |
| Web 框架 | Express 5.x | HTTP/WebSocket 服务 |
| WebSocket | ws | WebSocket 通信 |
| Schema | Zod 4.x + TypeBox | 运行时类型验证 |
| 数据库 | sqlite-vec | 向量搜索（记忆系统） |
| 图像处理 | Sharp | 图片压缩和转换 |
| 浏览器 | Playwright | 浏览器自动化控制 |
| PDF | pdfjs-dist | PDF 解析 |
| 配置 | JSON5（一种支持注释的配置文件格式） + dotenv | 主配置文件为 JSON5 格式（~/.openclaw/openclaw.json） |

**消息平台 SDK：**

| 平台 | 库 |
|------|-----|
| WhatsApp | @whiskeysockets/baileys |
| Telegram | grammy |
| Discord | @buape/carbon |
| Slack | @slack/bolt + @slack/web-api |
| 飞书 | @larksuiteoapi/node-sdk |
| LINE | @line/bot-sdk |
| AWS Bedrock | @aws-sdk/client-bedrock |

**AI Agent 核心：**

| 库 | 用途 |
|-----|------|
| @mariozechner/pi-agent-core | Agent 运行时核心 |
| @mariozechner/pi-ai | AI 模型抽象层 |
| @mariozechner/pi-coding-agent | 编程 Agent |
| @mariozechner/pi-tui | 终端 UI |

> ⏭️ **小白可跳过** — 这部分是技术深入分析，新手可以先跳过

### 项目结构

```
openclaw/
├── src/                    # 核心实现（TypeScript 等）
├── extensions/             # 扩展 Channel 和插件
├── skills/                 # 内置技能定义
├── apps/
│   ├── macos/             # macOS 菜单栏应用（Swift）
│   ├── ios/               # iOS 应用（Swift）
│   └── android/           # Android 应用（Kotlin）
├── ui/                     # Control UI（Web 前端）
├── docs/                   # 官方文档（Mintlify）
├── scripts/                # 构建和工具脚本
├── test/                   # 测试文件
├── dist/                   # 构建产物
├── openclaw.mjs            # CLI 入口
├── package.json            # 依赖和脚本
├── tsconfig.json           # TypeScript 配置
├── vitest.unit.config.ts   # 单元测试配置
├── vitest.e2e.config.ts    # E2E 测试配置
└── vitest.live.config.ts   # 实时测试配置
```

> ⏭️ **小白可跳过** — 这部分是技术深入分析，新手可以先跳过

### 开发工具链

```bash
# 从 Git 仓库本地构建
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build

# 开发模式（文件变更自动重载）
pnpm gateway:watch

# 运行测试
pnpm test              # 并行单元测试
pnpm test:e2e          # E2E 测试
pnpm test:live         # 实时模型测试

# 代码质量
pnpm check             # 格式 + 类型 + Lint
pnpm lint:fix          # 自动修复
```

### 版本策略

OpenClaw 采用日期版本号：`vYYYY.M.D`，例如 `v2026.2.24`。

三个发布通道：

| 通道 | npm 标签 | 说明 |
|------|----------|------|
| stable | `latest` | 正式发布，推荐使用 |
| beta | `beta` | 预发布版本，可能缺少 macOS 应用 |
| dev | `dev` | main 分支最新代码 |

```bash
# 切换通道
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

## 支持的 AI 模型提供商

OpenClaw 支持多个主流 AI 模型提供商，这是它的核心竞争力之一。官方模型目录变化很快，教程不再写死“最强模型”或固定数量，实际以当前安装版本、Onboarding 和官方 Models 文档为准。

### 推荐配置

官方强烈推荐 **Anthropic Claude Opus 4.6**，理由是：
- 长上下文处理能力强
- 更好的 Prompt 注入防御
- 工具调用准确率高

### 完整提供商列表

**国际主流：**

| 提供商 | 代表模型 | 特点 |
|--------|----------|------|
| OpenAI | GPT-5.4 | 最强通用能力，OpenClaw 赞助商 |
| Anthropic | Claude Opus 4.6, Sonnet 4.6 | 官方推荐，编程和安全最强 |
| Google | Gemini 3.1 | 多模态能力强 |
| Mistral | Mistral Large | 欧洲开源模型 |
| xAI | Grok | 实时信息能力 |

**本地/自托管：**

| 提供商 | 代表模型 | 特点 |
|--------|----------|------|
| Ollama | Llama, Qwen, Mistral | 本地运行，隐私优先 |
| vLLM | 各种开源模型 | 高性能本地推理 |
| node-llama-cpp | GGUF 模型 | 直接在 Node.js 中运行 |

**中国大陆：**

| 提供商 | 代表模型 | 特点 |
|--------|----------|------|
| 通义千问 (Qwen) | Qwen-Max | 阿里巴巴，中文能力强 |
| 百度千帆 (Qianfan) | ERNIE | 百度，中文优化 |
| 智谱 (GLM) | GLM-4 | 清华系，学术能力强 |
| Moonshot/Kimi | Moonshot 视觉 | 中文优化，视觉能力 |
| 小米 (Xiaomi) | MiLM | 小米 AI |
| MiniMax | abab6 | 多模态 |
| DeepSeek | DeepSeek V4 Flash / V4 Pro | 编程能力强，引导向导默认 |

**代理/路由服务：**

| 提供商 | 特点 |
|--------|------|
| OpenRouter | 一个 API Key 用所有模型 |
| LiteLLM | 统一接口代理层 |
| AWS Bedrock | 企业级，支持 Claude 和 Titan |
| Vercel AI Gateway | Vercel 生态集成 |
| Cloudflare AI Gateway | CDN 加速 |
| Together AI | 开源模型托管，性价比高 |
| NVIDIA NIM | GPU 加速推理 |
| Venice AI | 隐私优先，不记录数据 |
| HuggingFace | 社区开源模型 |

### 模型故障转移

OpenClaw 支持配置多个模型的优先级和故障转移策略。主模型不可用时自动切换到备用模型，保证助手始终在线。

详见 [04. 模型配置指南](04-模型配置指南.md)。

## 客户端生态

连接 Gateway 的方式有很多，覆盖了主流平台：

### 原生应用

| 平台 | 类型 | 技术栈 | 功能 |
|------|------|--------|------|
| macOS | 菜单栏应用 | Swift | 控制面板、Voice Wake、Talk Mode、Canvas |
| iOS | 移动应用 | Swift | Canvas、Voice Wake、Talk Mode、摄像头 |
| Android | 移动应用 | Kotlin | Canvas、Talk Mode、摄像头、屏幕录制 |

### 命令行

```bash
# 直接跟 AI 对话
openclaw agent --message "帮我查一下明天的天气"

# 发送消息到指定平台
openclaw message send --to +1234567890 --message "Hello"

# 交互式 TUI
openclaw tui
```

### Web 界面

- **Control UI** — 浏览器控制面板，管理 Gateway 配置。自 v2026.4.5 起支持 12 种界面语言（简/繁中文、日/韩/法/德/西/葡/土/印尼/波兰/乌克兰语）
- **WebChat** — 浏览器聊天界面，直接跟 AI 对话
- **Live Canvas** — Agent 驱动的可视化工作区

### 语音能力

- **Voice Wake** — 语音唤醒，类似 "Hey Siri"（macOS/iOS/Android）
- **Talk Mode** — 实时语音对话，基于 ElevenLabs TTS
- **PTT（Push to Talk）** — 按键说话模式

## 社区生态

### 项目数据（截至 2026 年 2 月）

| 指标 | 数据 |
|------|------|
| GitHub Stars | 227,000+ |
| Forks | 43,000+ |
| 贡献者 | 30+（核心仓库，GitHub API 分页限制） |
| 开放 Issues | 7,500+ |
| 许可证 | MIT |
| 发布频率 | 几乎每天 |
| 赞助商 | OpenAI, Vercel, Blacksmith, Convex |

### 社区渠道

| 渠道 | 链接 | 用途 |
|------|------|------|
| Discord | discord.gg/clawd | 主要社区，实时讨论 |
| GitHub Discussions | github.com/openclaw/openclaw | 功能请求、技术讨论 |
| GitHub Issues | github.com/openclaw/openclaw/issues | Bug 报告 |
| 官方文档 | docs.openclaw.ai | 完整文档 |
| 官方网站 | openclaw.ai | 项目主页 |
| DeepWiki | deepwiki.com/openclaw/openclaw | AI 生成的代码文档 |

### ClawHub（技能市场）

ClawHub（clawhub.com）是 OpenClaw 的技能和插件市场。社区开发者可以发布自己的技能，其他用户可以一键安装。

官方鼓励新技能优先发布到 ClawHub，而不是提交到核心仓库。核心仓库的合并门槛很高。

### 贡献指南

如果你想给 OpenClaw 贡献代码：

- **一个 PR = 一个问题** — 不要把多个不相关的修复打包在一起
- **PR 不超过 5000 行** — 超大 PR 只在特殊情况下审查
- **不要批量提交小 PR** — 每个 PR 都有审查成本
- **小修复可以合并** — 相关的小修复可以放在一个 PR 里

## 适用场景和不适用场景

### 适合用 OpenClaw 的场景

**个人效率助手：**
- 通过 WhatsApp/Telegram 管理日程和待办
- 让 AI 帮你整理邮件、回复消息
- 语音控制智能家居设备
- 定时提醒和自动化工作流

**开发者工具：**
- 通过聊天软件管理 GitHub Issue 和 PR
- AI 编程助手，直接在聊天中写代码
- 监控服务器状态，异常时自动通知
- 自动化 DevOps 任务

**知识管理：**
- 连接 Obsidian/Notion，AI 帮你整理笔记
- 自动摘要长文档和网页
- 跨平台信息聚合

**多平台统一入口：**
- 一个 AI 助手，通过所有你常用的聊天软件都能访问
- 在 WhatsApp 上开始的对话，可以在 Telegram 上继续
- 统一的记忆系统，AI 在所有平台都"认识"你

### 不适合用 OpenClaw 的场景

| 场景 | 原因 | 替代方案 |
|------|------|----------|
| 企业客服机器人 | OpenClaw 是单用户设计 | Botpress, Intercom |
| 多用户 SaaS 产品 | 没有多租户架构 | 自建方案 |
| 不想碰终端的用户 | 目前安装和配置需要命令行 | ChatGPT, Claude.ai |
| 低配设备 | 需要 Node.js 22+，内存占用不小 | 轻量级 Bot 框架 |
| 需要 100% 可用性 | 个人设备可能关机/断网 | 云端 AI 服务 |

OpenClaw 的设计哲学很明确：**它是一个个人助手，不是企业平台。** 单用户、本地优先、隐私至上。

## 版本历史和路线图

### 当前优先级（来自官方 VISION.md）

**最高优先级：**
- 安全和安全默认值
- Bug 修复和稳定性
- 安装可靠性和首次使用体验

**下一步优先级：**
- 支持所有主流模型提供商
- 改进主流消息平台支持（并添加高需求平台）
- 性能和测试基础设施
- 更好的 Computer Use 和 Agent 能力
- CLI 和 Web 前端的易用性
- macOS、iOS、Android、Windows、Linux 伴侣应用

### 不会合并的功能（目前）

官方明确列出了暂时不会接受的 PR 类型：

- 可以放在 ClawHub 上的新核心技能
- 全套文档翻译（计划用 AI 自动翻译）
- 不明确属于模型提供商类别的商业服务集成
- 已有 Channel 的包装器（除非有明确的能力或安全差距）
- 核心中的一等 MCP 运行时（mcporter 已经提供了集成路径）
- Agent 层级框架（管理者的管理者/嵌套规划树）
- 重复现有 Agent 和工具基础设施的重型编排层

官方说这是路线图护栏，不是铁律。强烈的用户需求和技术理由可以改变它。

## 学习路径建议

### 新手路线（1-2 小时）

```
第 1 步：安装 OpenClaw
         → 阅读 02-安装部署指南.md
         → 运行 openclaw onboard

第 2 步：连接第一个消息平台
         → 阅读 05-消息平台接入指南.md
         → 推荐从 Telegram 开始（最简单）

第 3 步：配置 AI 模型
         → 阅读 04-模型配置指南.md
         → 推荐从 OpenAI 或 Anthropic 开始

第 4 步：试用内置技能
         → 阅读 06-技能系统指南.md
         → 试试 weather、summarize 等简单技能
```

### 进阶路线（1 周）

```
第 5 步：理解记忆系统
         → 阅读 07-记忆系统指南.md
         → 教 AI 记住你的偏好

第 6 步：多 Agent 配置
         → 阅读 08-多Agent协作指南.md
         → 为不同场景创建专用 Agent

第 7 步：Docker 部署
         → 阅读 09-Docker部署指南.md
         → 在服务器上 7x24 运行

第 8 步：安全加固
         → 阅读 10-安全配置指南.md
         → 配置 DM 策略和权限
```

### 高级路线（持续学习）

```
第 9 步：开发自定义技能
         → 学习 Workspace Skills 开发
         → 发布到 ClawHub

第 10 步：插件开发
          → 学习 Plugin SDK
          → 开发自定义 Channel 或工具

第 11 步：向上游贡献
          → Fork 仓库，从仓库本地构建
          → 修复 Bug 或添加功能
          → 提交 PR
```

### 推荐学习资源

| 资源 | 链接 | 说明 |
|------|------|------|
| 官方文档 | docs.openclaw.ai | 最权威的参考 |
| Install | docs.openclaw.ai/install/index | 官方安装指南 |
| CLI Reference | docs.openclaw.ai/cli | 官方 CLI 参考 |
| Discord 社区 | discord.gg/clawd | 实时问答 |
| DeepWiki | deepwiki.com/openclaw/openclaw | AI 生成的代码文档 |
| SkillClaw | https://github.com/AMAP-ML/SkillClaw | 长期 skill 库治理与集体演化框架，适合研究多用户、多设备场景下的 skill 去重、合并、提质和共享；论文见 https://arxiv.org/abs/2604.08377 |
| 本系列教程 | 你正在读的这个 | 中文完整指南 |

## 快速体验

如果你等不及了，这是最快的上手方式：

```bash
# 1. 安装（官方推荐，适用于 macOS / Linux / WSL2）
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. 运行安装向导（会引导你配置模型和平台）
openclaw onboard --install-daemon

# 3. 启动 Gateway（调试模式）
openclaw gateway --port 18789 --verbose

# 4. 跑一次诊断，确认 Gateway 和配置已就绪
openclaw doctor
```

5 分钟后，你就有了一个跑在自己电脑上的 AI 私人助手。

## 下一步

准备好了吗？去 [02. 安装部署指南](02-安装部署指南.md) 开始安装 OpenClaw！
