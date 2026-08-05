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

老金在这篇里不会把 OpenClaw 讲成万能助手，因为真正要学的是它适合接哪些消息流和工作流。

OpenClaw 是一个**开源的 AI 私人助手框架**，跑在你自己的电脑或服务器上，能连接 WhatsApp、Telegram、Discord 等消息平台，让 AI 帮你处理消息、执行任务、管理日程。

你可以把它理解为：**一个 7x24 小时在线的 AI 员工，通过你常用的聊天软件跟你沟通。**

跟只在云端运行的 AI 助手不同，OpenClaw 的配置、记忆、聊天记录和工作文件默认由你自己的电脑或服务器保存。但只要你接入 OpenAI、Anthropic、Google、OpenRouter 等云端模型，消息内容仍会发给对应模型提供商处理；只有使用 Ollama / vLLM 等本地模型时，模型推理才可以不出本机。课程里讲“隐私优先”，指的是你能控制运行位置、数据目录、模型 provider 和通道边界，而不是承诺所有数据天然不离开设备。

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
| 2026.04.24 | Google Meet 集成 | 首个内置会议类插件；模型目录和 provider 元数据继续扩展 |
| 2026 年后 | 持续高频迭代 | 版本号采用 `YYYY.M.D` 风格 |

## 与其他 AI 助手框架的对比

市面上做 AI 助手/聊天机器人的框架不少，OpenClaw 的定位跟它们有本质区别。

### OpenClaw vs Botpress

| 维度 | OpenClaw | Botpress |
|------|----------|----------|
| 定位 | 个人 AI 助手 | 企业级聊天机器人平台 |
| 部署 | 本地优先，跑在你自己设备上 | 云端 SaaS 为主 |
| 数据 | 配置、记忆和聊天记录默认本地保存；云端模型调用另看 provider | 存在 Botpress 云端 |
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
   ├── 调用已配置的 AI 模型
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

### 选型原则

不要把某个固定模型写成永久推荐。OpenClaw 的模型目录、provider 元数据和 fallback 规则更新很快，课堂上应先运行当前版本的 onboarding / models 命令，确认本机能看到哪些 provider 和模型，再按下面的维度选择：

- 长上下文任务：优先选当前目录里上下文窗口更大的模型。
- 多工具 / 多 Agent：优先选工具调用稳定、延迟可接受的模型。
- 隐私敏感任务：优先本地模型或企业受控 provider。
- 成本敏感任务：把日常问答、摘要和高价值复杂任务分开配。

### 完整提供商列表

**国际主流：**

| 提供商 | 代表模型 | 特点 |
|--------|----------|------|
| OpenAI | 以当前 OpenClaw Models 目录为准 | 通用、代码、多模态等能力随账号和模型版本变化 |
| Anthropic | 以当前 OpenClaw Models 目录为准 | 长上下文、工具调用、代码任务常用 |
| Google / Vertex | 以当前 OpenClaw Models 目录为准 | 多模态、长上下文和企业云路径常见 |
| Mistral | 以当前 OpenClaw Models 目录为准 | 欧洲模型生态和自托管场景常见 |
| xAI | 以当前 OpenClaw Models 目录为准 | 是否可用取决于 provider 配置和地区 |

**本地/自托管：**

| 提供商 | 代表模型 | 特点 |
|--------|----------|------|
| Ollama | Llama, Qwen, Mistral | 本地运行，隐私优先 |
| vLLM | 各种开源模型 | 高性能本地推理 |
| node-llama-cpp | GGUF 模型 | 直接在 Node.js 中运行 |

**中国大陆：**

| 提供商 | 代表模型 | 特点 |
|--------|----------|------|
| 通义千问 (Qwen) | 以当前 provider 目录为准 | 中文和本地化生态常见 |
| 百度千帆 (Qianfan) | 以当前 provider 目录为准 | 百度云路径和中文场景常见 |
| 智谱 (GLM) | 以当前 provider 目录为准 | 中文、工具和企业场景常见 |
| Moonshot / Kimi | 以当前 provider 目录为准 | 长文本和中文场景常见 |
| 小米 (Xiaomi) | 以当前 provider 目录为准 | 是否可用取决于当前版本目录 |
| MiniMax | 以当前 provider 目录为准；v2026.6.x release 已补充 MiniMax M3 元数据 | 多模态和中文生态场景常见 |
| DeepSeek | 以当前 provider 目录为准 | 编程和中文场景常见 |

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

## 从概念到真实系统：一条消息背后的责任链

读完项目介绍后，最重要的是能把概念串起来。下面用一条 Telegram 私聊消息做例子。

```text
用户发消息
  ↓
Telegram Channel 收到事件
  ↓
Gateway 接收并标准化消息
  ↓
路由规则判断交给哪个 Agent
  ↓
Agent 加载 SOUL.md、记忆和可用技能
  ↓
模型生成计划或回复
  ↓
必要时调用工具或技能
  ↓
Gateway 把回复发回 Telegram
```

这条链路里，每一层都有不同的排障方法。

```text
平台没收到：
查 Channel 配置和平台权限。

Gateway 没日志：
查 Gateway 是否启动、端口、Webhook / Polling。

Agent 没处理：
查路由、绑定、session 和 Agent 状态。

模型失败：
查 provider、API Key、模型 ID、限流和网络。

工具失败：
查技能依赖、权限、沙箱和日志。

回复没发出：
查平台 token、出站权限和 rate limit。
```

OpenClaw 的学习顺序也应该按这条链路来：先 Gateway，再 Agent，再模型，再 Channel，再技能、记忆和多 Agent。顺序反了，排障会非常痛苦。

## OpenClaw 适合做什么样的产品

如果你把 OpenClaw 当成“多平台聊天机器人脚手架”，会低估它。更准确的定位是：它适合做长期在线、跨平台、有记忆、有工具、有安全边界的 AI 助手。

适合做：

```text
- 个人手机 AI 助手。
- 团队内部知识问答机器人。
- 项目运维提醒助手。
- 会议和消息摘要助手。
- 多平台客服辅助。
- 带工具和记忆的工作流入口。
```

不适合做：

```text
- 完全无人工边界的生产操作机器人。
- 高并发商业客服系统的唯一核心。
- 不保存配置、不看日志的一次性聊天网页。
- 没有 token、TLS、Pairing 就暴露公网的服务。
```

判断一个场景适不适合 OpenClaw，可以问四个问题：

```text
1. 是否需要长期运行？
2. 是否需要接多个消息入口？
3. 是否需要记忆、技能或工具？
4. 是否有人愿意维护配置、安全和日志？
```

如果四个答案都是否，普通 ChatGPT 或一次性脚本可能更合适。如果前三个是，第四个没人负责，那先不要上生产。

## 项目介绍课的实战练习

练习目标：不安装新东西，只用项目介绍判断一个需求应该怎么落地。

需求：

```text
我想做一个团队 AI 助手，接 Slack，能回答项目文档问题，也能记住团队常用流程。
```

请按下面模板拆解：

```md
# OpenClaw Solution Sketch

## Message Entry

Platform:
Channel:
Who can talk:

## Agent

Default agent:
Need multiple agents:

## Model

Default model:
Heavy task model:

## Skills

Needed skills:
Not needed yet:

## Memory

Should remember:
Should not remember:

## Security

Pairing / allowlist:
Gateway token:
Logs:

## First milestone

What to test in day 1:
```

参考拆解：

```text
第一天只接 Slack 测试频道，默认 Agent 回答项目文档问题。
先不启用多 Agent。
先不让它写外部系统。
记忆只保存团队术语，不保存客户数据。
安全上先限制频道和用户，再考虑更多技能。
```

这类练习能让读者看到：OpenClaw 的每个概念都不是孤立名词，而是一个真实系统里的责任点。

## 选型判断：什么时候该用 OpenClaw

很多读者第一次看到 OpenClaw，会把它放进三个熟悉分类里：聊天机器人、Agent 框架、自动化工具。它确实都沾一点，但又不完全等同。

更准确的判断方式，是看你的需求是不是同时具备下面几个特征：

```text
1. 需要长期在线，而不是一次性脚本。
2. 需要从消息平台进入，而不是只在终端里运行。
3. 需要本地文件、记忆、技能或工具参与。
4. 需要安全边界，而不是完全开放给所有人。
5. 需要以后能迁移、备份、排错和升级。
```

如果你的需求只是一问一答，用普通聊天产品就够。如果只是跑代码任务，专门的编程 Agent 更直接。如果你要把 AI 放到 Telegram、Discord、Slack、WebChat 里，让它带着记忆和技能长期服务，OpenClaw 的价值才会明显。

下面用几个场景做判断。

### 场景一：个人手机助手

需求：

```text
我希望在手机上发消息给 AI，让它帮我总结想法、记住偏好、偶尔整理文件。
```

适合 OpenClaw，因为：

- Telegram / WhatsApp / WebChat 可以作为入口。
- `USER.md` 和 `MEMORY.md` 能保存长期偏好。
- Skill 可以把“整理读书笔记”“生成周报”这类动作固化。
- DM Pairing 可以限制只有你本人能触发。

第一阶段不要做：

- 不要马上开放到群聊。
- 不要让它自动发送外部消息。
- 不要让它拥有高风险 shell 权限。

最小架构：

```text
Telegram 私聊
  -> Gateway
  -> main Agent
  -> 默认模型
  -> USER.md / MEMORY.md
```

### 场景二：开源项目社区助手

需求：

```text
我有一个 Discord 社区，希望 AI 回答安装问题、引导用户看文档、整理反馈。
```

适合 OpenClaw，但要分阶段：

```text
第 1 阶段：
只接一个测试频道，回答 FAQ。

第 2 阶段：
接 #support，增加技术支持 Skill。

第 3 阶段：
增加反馈整理 Skill，把高频问题沉淀到 FAQ 草稿，并由人工 Review 后再发布。

第 4 阶段：
拆 community 和 tech-support 两个 Agent。
```

关键边界：

- 社区 Agent 不应该直接关闭 issue。
- 技术支持 Agent 不应该执行用户发来的脚本。
- 反馈整理可以生成草稿，不自动发布公告。

最小架构：

```text
Discord #support
  -> Gateway
  -> tech-support Agent
  -> docs / FAQ Skill
  -> 手动确认后再创建 issue 或更新文档
```

### 场景三：内部运维助手

需求：

```text
团队希望在 Slack 里问部署状态、查运行手册、整理告警。
```

OpenClaw 可以做入口和工作流协调，但不能无边界接管生产。

适合做：

- 解释告警。
- 整理日志摘要。
- 生成排查步骤。
- 查运行手册。
- 提醒值班人。

谨慎做：

- 自动重启服务。
- 自动改配置。
- 自动执行数据库操作。
- 自动发布生产变更。

最小架构：

```text
Slack 运维频道
  -> Gateway
  -> ops Agent
  -> runbook Skill
  -> 只读日志或人工提供日志
  -> 输出排查建议
```

如果后续要让它触发真实运维动作，应该单独设计审批、沙箱、日志、回滚和权限，而不是把一个聊天 Agent 直接接到生产命令上。

## 从需求到配置：一张设计草图

OpenClaw 的配置不是孤立字段。每个字段背后都对应一个产品决策。可以用下面这张草图把需求翻译成系统结构。

```text
谁会发消息？
  -> 决定 Channel、Pairing、allowlist。

消息进来给谁处理？
  -> 决定 Agent、bindings、workspace。

需要什么智能水平？
  -> 决定 provider、model、fallback。

需要记住什么？
  -> 决定 USER.md、MEMORY.md、每日记忆。

需要做哪些固定动作？
  -> 决定 Skill、Tool、权限。

有没有外部风险？
  -> 决定 sandbox、token、日志、反向代理。
```

例如“团队文档问答机器人”可以拆成：

| 决策 | 示例 |
|---|---|
| Channel | Slack 测试频道 |
| Agent | `docs-helper` |
| Model | 默认中等成本模型，长文档总结用强模型 |
| Memory | 记住团队术语，不记客户数据 |
| Skills | 文档搜索、反馈整理 |
| Security | 只允许内部频道，DM Pairing 开启 |
| Deployment | 先本地，稳定后 Docker |

对应的第一版配置不需要复杂：

```json5
{
  "agents": {
    "list": [
      {
        "id": "docs-helper",
        "workspace": "~/.openclaw/workspace-docs-helper",
        "model": "openai/gpt-5.2-mini",
        "skills": ["summarize"]
      }
    ]
  },
  "bindings": [
    {
      "agent": "docs-helper",
      "channel": "slack",
      "channelId": "C0123456789"
    }
  ]
}
```

这只是草图，不是最终配置。它的作用是让你先看清“入口、处理者、模型、记忆、技能、安全”之间的关系。

## 故障地图：看症状就知道先查哪一层

OpenClaw 的错误通常不是"整个系统坏了"，而是某一层没有接上。下面这张地图适合排障时快速定位。

| 症状 | 先查 | 常见原因 |
|---|---|---|
| `openclaw` 命令不存在 | 安装层 | npm 全局路径、shell 没刷新、Node 版本 |
| Gateway 启动失败 | Gateway 层 | 端口占用、配置语法错误、权限问题 |
| Control UI 打不开 | Gateway / 网络 | 端口不对、防火墙、监听地址 |
| UI 能聊，平台不回复 | Channel 层 | token、Webhook、Pairing、平台权限 |
| 平台进来但 AI 不答 | Agent / 模型 | 路由错误、模型 Key 错、限流 |
| AI 答非所问 | Agent / Skill / Memory | SOUL.md 模糊、技能误触发、记忆污染 |
| 工具调用失败 | Tool / Sandbox | 依赖缺失、权限不足、路径不对 |
| Docker 更新后丢数据 | 部署层 | volume 未挂载、备份未恢复 |

排障时每次只动一层。比如平台不回复，先不要改模型；模型报错，先不要重写 SOUL.md；Docker 丢数据，先查 volume，不要反复重装 CLI。

## OpenClaw 的学习心智模型

把 OpenClaw 当成一个小系统，而不是一个 App。你学它时可以用四层心智模型：

```text
入口层：
Channel、Webhook、Polling、WebChat、CLI。

调度层：
Gateway、bindings、sessions、Agent routing。

智能层：
Model、SOUL.md、Skills、Memory、Tools。

运行层：
config、logs、sandbox、Docker、security、backup。
```

新手常常只看智能层，因为那里最像“AI”。但真正决定系统稳定性的，往往是入口层和运行层。只要入口不稳、配置不清、日志不会看，再强的模型也救不了体验。

建议学习时每一层都至少做一个动作：

```text
入口层：
用 CLI 或 WebChat 发第一条消息。

调度层：
看一次 Gateway 日志，确认消息进了哪个 Agent。

智能层：
写一个最小 Skill 或整理一次 MEMORY.md。

运行层：
跑一次 openclaw doctor，记录配置和日志位置。
```

这样你学到的不是零散功能，而是一套能维护的系统。

## 案例：把“AI 客服”需求改写成 OpenClaw 方案

很多需求一开始都很大，比如：

```text
我想做一个 AI 客服，接到 WhatsApp 和 Discord，能回答问题、处理退款、创建工单、自动升级给人工。
```

这句话不能直接变成配置。先拆边界。

### 第一步：拆消息入口

```text
WhatsApp：
更像私域客服，用户身份更具体，消息可能包含订单、手机号、售后信息。

Discord：
更像社区支持，公开频道更多，适合安装、使用、bug、FAQ。
```

所以不要让两个平台共用同一个 Agent。可以这样拆：

```text
WhatsApp -> customer-support Agent
Discord #support -> community-support Agent
Discord #bugs -> issue-triage Agent
```

### 第二步：拆能力边界

AI 可以做：

```text
- 回答公开 FAQ。
- 收集问题信息。
- 生成工单草稿。
- 判断是否需要人工。
- 总结用户问题。
```

AI 不应该直接做：

```text
- 承诺退款。
- 修改订单。
- 发送法律或财务承诺。
- 访问完整客户隐私。
- 自动关闭投诉。
```

### 第三步：拆记忆和知识

```text
FAQ、产品手册、安装文档：
放知识库或文档检索。

客服流程、升级条件：
放 Agent 的 SOUL.md 或 MEMORY.md。

用户个人信息：
尽量不进入长期记忆，只在必要时临时处理，并做脱敏。
```

### 第四步：拆第一期目标

第一期不要做“完整 AI 客服”。第一期可以是：

```text
Discord #support 中，Bot 回答安装和配置 FAQ。
遇到无法判断的问题，生成 issue 草稿。
不接触退款、订单、支付。
```

对应 OpenClaw 结构：

```text
Discord #support
  -> Gateway
  -> community-support Agent
  -> FAQ / docs Skill
  -> issue-triage Skill
  -> 人工确认后创建 issue
```

这样做的好处是上线快、风险低、可观察。等公开支持跑稳，再考虑 WhatsApp 私域客服。

## 案例：把“团队 AI 助手”需求改写成 OpenClaw 方案

需求：

```text
我们想在 Slack 里问项目问题、查部署流程、总结会议，还想让它记住团队习惯。
```

先拆成三类 Agent：

```text
docs-helper：
回答文档和项目问题。

ops-helper：
解释部署流程和告警。

meeting-helper：
整理会议 transcript 和待办。
```

再拆频道：

```text
Slack #ai-help -> docs-helper
Slack #ops-alerts -> ops-helper
Slack #meetings -> meeting-helper
```

安全边界：

```text
docs-helper：
只读文档，不执行命令。

ops-helper：
可以解释 runbook，但不直接操作生产。

meeting-helper：
可以整理会议纪要，但不自动发布结论。
```

记忆边界：

```text
团队术语：
可以进入共享项目事实。

个人偏好：
不要放进团队共享记忆。

会议原文：
按保留策略归档，不默认写长期记忆。
```

第一期目标：

```text
只接 Slack #ai-help，一个 docs-helper Agent，只回答项目文档问题。
```

等第一期稳定后，再把 ops 和 meeting 拆出来。多 Agent 不是为了显得复杂，而是为了让入口、权限、记忆和工具边界更清楚。

## 从 MVP 到长期系统：OpenClaw 的阶段路线

OpenClaw 很适合渐进式搭建。你不需要第一天就把模型、平台、技能、记忆、多 Agent、Docker、安全全部配完。更稳的做法是分阶段。

### 阶段一：MVP，只证明一条链路

目标：

```text
用户能在一个入口发消息，默认 Agent 能用一个模型回复。
```

结构：

```text
WebChat / CLI
  -> Gateway
  -> main Agent
  -> default model
```

这个阶段只关心：

- Gateway 是否能启动。
- 模型是否能返回。
- 日志是否能看懂。
- 配置文件在哪里。

暂时不要关心：

- 多 Agent。
- 群聊。
- 自动任务。
- 外部工具写入。

MVP 阶段的产物是一份 Quickstart Runbook，而不是一套复杂配置。

### 阶段二：接入真实入口

目标：

```text
把 OpenClaw 放进你真正会使用的消息入口。
```

结构：

```text
Telegram / Discord / Slack
  -> Channel
  -> Gateway
  -> main Agent
  -> default model
```

这个阶段开始关注：

- 谁可以发消息。
- 消息是否需要 Pairing。
- 公开频道和私聊是否不同。
- 平台 token 存在哪里。
- 平台日志怎么看。

这时 OpenClaw 已经从“本地工具”变成“外部入口”。外部入口一旦出现，安全和费用就开始重要。

### 阶段三：增加可复用能力

目标：

```text
让 Agent 能稳定做一类重复工作。
```

结构：

```text
Message
  -> Agent
  -> Skill
  -> Memory
  -> reply / draft / file
```

这个阶段的重点是把“临时提示词”固化成 Skill，把“长期事实”整理进记忆。比如：

```text
- 整理反馈。
- 总结会议。
- 生成周报。
- 分拣 issue。
- 根据团队流程回答问题。
```

不要把所有能力都写进一个 Skill。一个 Skill 做一件事，触发条件清楚，边界清楚，例子清楚。

### 阶段四：拆分 Agent 和权限

目标：

```text
不同入口、不同任务、不同权限交给不同 Agent。
```

结构：

```text
Discord #general -> community Agent
Discord #support -> tech-support Agent
Slack #ops -> ops Agent
Telegram DM -> personal Agent
```

这个阶段的核心：

- 不同 Agent 有不同 workspace。
- 不同 Agent 有不同模型。
- 不同 Agent 有不同技能和工具。
- 不同 Agent 有不同记忆和安全边界。

当一个 Agent 的 SOUL.md 里出现太多“同时负责”，就是拆分信号。

### 阶段五：长期部署和治理

目标：

```text
OpenClaw 能稳定运行、能更新、能备份、能恢复、能解释事故。
```

结构：

```text
Reverse proxy / VPN
  -> Gateway
  -> Docker volume
  -> logs
  -> backup
  -> security runbook
```

这个阶段开始关注：

- Docker volume 是否持久化。
- Gateway 是否只监听本机。
- 反向代理是否正确处理 WebSocket。
- token 如何轮换。
- 日志是否脱敏。
- 更新前是否备份。
- 出事时如何关闭入口。

长期系统的关键不是"功能更多"，而是“出了问题能恢复”。这也是 OpenClaw 和一次性聊天脚本最大的区别。

## OpenClaw 的边界：它不是万能自动员工

OpenClaw 能把 AI 放进真实消息入口，也能连接技能、记忆和工具。正因为它有这些能力，边界更重要。

适合自动化的：

```text
- 总结。
- 分类。
- 起草。
- 提醒。
- 查找公开文档。
- 生成排查步骤。
- 整理用户反馈。
```

适合人工确认后再执行的：

```text
- 创建 issue。
- 发布公告。
- 回复客户。
- 修改配置。
- 写入共享文档。
- 调用外部系统。
```

不建议交给 AI 直接做的：

```text
- 生产数据库修改。
- 付款和退款。
- 法律承诺。
- 安全漏洞披露判断。
- 删除大量文件。
- 泄露、复制或转发凭证。
```

这不是保守，而是产品边界。AI 最适合提升信息处理和草稿生成效率，不应该在缺少确认和回滚机制时直接掌握高风险动作。

## 下一步

准备好了吗？去 [02. 安装部署指南](02-安装部署指南.md) 开始安装 OpenClaw！
