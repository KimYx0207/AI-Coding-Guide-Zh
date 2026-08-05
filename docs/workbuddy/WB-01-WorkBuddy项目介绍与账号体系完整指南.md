# WB-01 WorkBuddy 项目介绍：给中国用户的 AI 办公助手

定位说明：本篇只解决一件事——让你 15 分钟内判断，WorkBuddy 是不是给你准备的。后续桌面工作流、深度研究、Coding Mode、集成、计划任务、企业安全，都建立在这个判断上。

主要来源：腾讯 WorkBuddy 官方站点（workbuddy.ai / codebuddy.cn/work）、Tencent Cloud Techpedia、WorkBuddy App 内帮助页。本篇按 2026-08-06 可查官方资料修订；WorkBuddy 没有 semver，菜单名、价格、套餐一律以本机 App 关于页和官网为准。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：30-60 分钟
> - **难度等级**：⭐ 零基础入门
> - **更新日期**：2026年8月6日
> - **信息来源**：[workbuddy.ai](https://www.workbuddy.ai/) / [codebuddy.cn/work](https://www.codebuddy.cn/work) / [Tencent Cloud Techpedia](https://www.tencentcloud.com/techpedia/144314)
> - **前置要求**：已完成 [WB-00 阅读指南](./WB-00-阅读指南.md)

---

## 这篇解决什么问题

如果你符合下面任意一条，WorkBuddy 大概率适合你：

```text
✅ 会用 Word / Excel / 企业微信，但不会命令行
✅ 想用 AI 办公，但被 Claude Code / Codex 的英文 CLI、API Key 劝退过
✅ 团队在国内，主要沟通工具是企业微信 / 微信 / 钉钉
✅ 不想折腾代理、海外信用卡、英文文档
✅ 想要一个下载就能用、像用微信一样简单的 AI 助手
```

如果你符合下面任意一条，**WorkBuddy 可能不是首选**，去看同仓库的其他主线：

```text
❌ 你是开发者，要写 Hooks / Subagent / Agent SDK 做深度定制 → 看 Claude Code 系列
❌ 你要 App + CLI + Cloud 多入口分层协作 → 看 Codex 系列
❌ 你要本地完全可控的开源助手框架 → 看 OpenClaw 系列
```

这两类需求没有优劣，只是工具重心不同。本仓库四条主线就是按"不同人不同工具"组织的。

---

## 0. WorkBuddy 是什么（一段话版）

腾讯云出品的 AI 办公助手桌面 App。下载、用微信扫码登录、用一句话下任务，AI 帮你产出 Word / Excel / PPT / 代码。**不用学命令行、不用配 API Key、不用懂英文、不用代理**。

一句话总结：**Claude Code 和 Codex 是给开发者的专业工具，WorkBuddy 是给中国普通办公人的开箱即用助手**。

---

## 1. 为什么是 WorkBuddy，不是 Claude Code / Codex

老金在这节把 WorkBuddy 的独特价值讲清楚，因为新手最容易问的就是"我已经在用 Claude Code/Codex 了，为什么还要 WorkBuddy"或者"我老婆/同事不是程序员，能用哪个 AI"。

WorkBuddy 的核心优势就两个词：**更简单、更中国**。

### 1.1 更简单

| 维度 | Claude Code / Codex | WorkBuddy |
|---|---|---|
| **形态** | CLI（终端）/ App + CLI + Cloud 分层 | 一个桌面 App |
| **登录** | API Key / ChatGPT 账号 / Anthropic Console | 微信 / QQ 扫码 |
| **语言** | 英文命令为主 | 全中文界面 |
| **配置** | 要写 AGENTS.md、配 MCP、设 Hooks | 下载就用，没有配置文件 |
| **学习成本** | 要学 Commands、Skills、Subagent、MCP 这些概念 | 像用微信一样，打字就能用 |
| **出成品** | 写代码、改代码、做架构 | 直接出 Word / Excel / PPT |

> 💡 **关键理解**：Claude Code 和 Codex 强在"**深度可控**"——你能精确干预每一步、写脚本、做自动化。WorkBuddy 强在"**开箱即用**"——你不用知道任何技术细节，下完 App 就能用。**两者解决的不是同一个问题**。

### 1.2 适合中国用户

| 维度 | Claude Code / Codex | WorkBuddy |
|---|---|---|
| **服务器** | 海外，部分用户要代理 | 国内，直连不用代理 |
| **IM 集成** | GitHub / Slack / Discord（海外工具） | 企业微信 / 微信 / QQ / 小程序（国内工具） |
| **支付** | 海外信用卡 / PayPal | 微信支付 / 支付宝（人民币） |
| **合规** | 海外服务条款 | 国内合规、企业版可私有部署 |
| **客服** | 英文社区 / GitHub Issue | 中文客服 / 腾讯支持体系 |
| **生态** | 开发者工具链 | 腾讯办公生态（企业微信、腾讯会议、腾讯文档） |

> 💡 **关键理解**：如果你的团队在国内、用企业微信沟通、用人民币结算、要符合国内数据合规——WorkBuddy 几乎是唯一一个原生贴合这条链路的 AI 助手。这不是"哪个更好"的问题，是"哪个更贴你的实际环境"的问题。

### 1.3 什么时候别选 WorkBuddy

老金也把"不该用 WorkBuddy"的场景列出来，避免你选错工具：

```text
🚫 你是开发者，要做 CI/CD 集成、写 Hooks、定制 Subagent → Claude Code
🚫 你要 App + CLI + Web + Cloud 多入口协作 → Codex
🚫 你团队在海外、用 Slack/Notion/Stripe → Codex / Claude Code
🚫 你想完全本地部署、零云依赖 → OpenClaw
🚫 你要做复杂代码重构、大型代码库架构 → Claude Code（WorkBuddy 的 Coding Mode 适合小改和 demo，不适合大型重构）
```

> ⚠️ **注意**：选错工具比不选工具更糟。如果你是开发者，本仓库的 Claude Code 系列和 Codex 系列才是你的主线，WorkBuddy 是给你"非技术同事"或"办公场景"用的辅助工具。

---

## 2. 课堂工坊：30 分钟体验"简单"和"中国"两个优势

这个工坊用三个小场景，让你 30 分钟内亲自感受到 WorkBuddy 相对 Claude Code / Codex 的两个核心优势。建议拿一台日常办公电脑跟练。

### 2.1 工坊准备

你需要：

```text
- 一台 Windows 11 或 macOS 电脑
- 一个微信或 QQ 账号（用来扫码登录）
- 30 分钟时间
- 一份非敏感的本地文件（比如一份旧周报、一份公开 PDF）
```

> 🚫 **危险**：第一次实验**不要用**生产数据、客户信息、未公开财务数据。先用公开或脱敏素材，确认 App 行为可靠后再扩大范围。

### 2.2 场景 A：5 分钟出一份周报 Word（体现"简单"）

**目标**：感受"下完 App 就能用、不用配任何东西"。

打开 WorkBuddy App，用微信扫码登录，在任务输入框粘贴：

```text
帮我把这份文件整理成一份周报 Word 文档：
- 提炼 3 个本周核心进展
- 列出 2-3 个下周计划
- 用一段话总结整体进度
格式：标题 + 三个小节，方便直接发给领导。
```

然后把你的文件拖进任务输入框，回车发送。

**你应该看到**：

```text
- 几秒到几十秒后，Artifacts 面板出现一份 Word 文档
- 文档包含标题、三个进展、两三个计划、一段总结
- 可以直接复制到企业微信、导出 .docx、或贴到飞书/钉钉文档
```

**停下条件**：

```text
- 如果 App 提示"无法读取文件"：检查文件格式和路径，避免中文乱码或被其他程序锁定
- 如果产出明显跑偏（比如把下周计划写成本周总结）：不要直接用，回到原文对照后再发
- 如果长时间无响应（>2 分钟）：取消任务、检查网络、换个小文件重试
```

**这一步想让你体会的**：整个过程**没有任何配置**——没装 Node.js、没配 API Key、没写 .mcp.json、没设 Hooks。下完 App、扫码、下任务，完事。这就是"更简单"。

### 2.3 场景 B：把汇报推到企业微信（体现"中国"）

**目标**：感受"原生贴合国内办公链路"。

完成场景 A 后，在 Artifacts 面板里找到刚才那份周报 Word，找到"分享到企业微信"或类似入口（**具体按钮名以本机 App 为准**），把它推给你自己的企业微信"文件传输助手"或一个测试群。

**你应该看到**：

```text
- 文档出现在企业微信里，可以正常打开、转发、@同事
- 整个链路不用代理、不用第三方中转、不用配 Webhook
- 推送速度很快（国内服务器）
```

**停下条件**：

```text
- 如果推送失败：先检查企业微信账号是否在 WorkBuddy 里授权过
- 如果推到错误群聊：立刻在企业微信里撤回，并在 WorkBuddy 里关闭该集成
- 第一次测试只推给"文件传输助手"或自己建的测试群，不要直接推工作群
```

**这一步想让你体会的**：Claude Code / Codex 要把成果推到企业微信，需要自己写脚本、配 Webhook、走代理；**WorkBuddy 这一步是原生功能**，点一下就行。这就是"适合中国用户"。

### 2.4 场景 C：用中文问它一个原本要英文的问题（体现"中文友好"）

**目标**：感受"不用切英文也能把事办成"。

在任务输入框粘贴下面这段（这是一个典型的"换 Claude Code 要用英文问"的技术问题）：

```text
我要在一个 Python 项目里加日志，用 logging 模块。
要求：
1. 同时输出到控制台和文件
2. 文件按天切割
3. 控制台用 INFO 级别，文件用 DEBUG 级别
4. 给我完整的代码示例和怎么调用的说明
```

**你应该看到**：

```text
- WorkBuddy 用中文回复
- 给出一段完整的 Python 代码
- 解释每行关键参数
- 说明如何调用、如何验证日志生效
- 如果切到 Coding Mode，还能直接帮你在本地项目里加这段代码
```

**停下条件**：

```text
- 如果代码运行报错：先看是否缺依赖、Python 版本是否匹配，再让 AI 修
- 不要第一次就让它改生产代码，先在一个 demo 项目里验证
```

**这一步想让你体会的**：同样的问题，用 Claude Code / Codex 时多数人会本能地切英文（"Add logging to a Python project with..."），因为英文 Prompt 在那些工具上往往效果更好。**WorkBuddy 的中文优化让你不用切换语言**——这对非技术用户、对"想用母语思考"的人，是真实的体验差距。

### 2.5 工坊收尾：你应该留下的产物

```text
- 一份 AI 整理的周报 Word（场景 A 产出）
- 一条企业微信里的推送记录（场景 B 证据）
- 一段中文 Prompt 拿到的 Python 日志代码（场景 C 产出）
- 一份你自己的核对记录：哪些对了、哪些错了、下次怎么调
```

这四样东西比任何功能介绍都更能告诉你 WorkBuddy 是什么。

---

## 3. 常见问题

### Q1：我已经订阅了 Claude Code / Codex，还要再用 WorkBuddy 吗？

看场景。如果你是开发者、主要写代码、要深度定制——Claude Code / Codex 已经够用，WorkBuddy 不是必需。如果你有大量**非代码的办公任务**（周报、调研、PPT、企业微信分发），或者要给非技术同事一个 AI 工具——WorkBuddy 互补。

### Q2：WorkBuddy 和 CodeBuddy 是什么关系？

同团队同账号。"CodeBuddy 管开发，WorkBuddy 管办公"。一个腾讯账号两边通用，订阅关系以官网当前说明为准。

### Q3：WorkBuddy 真的不用代理吗？

国内服务器直连，正常办公网络不用代理。具体网络环境以你本机实测为准——少数企业内网可能有自己的出口策略，跟 WorkBuddy 本身无关。

### Q4：企业微信集成需要管理员权限吗？

部分能力需要企业管理员在腾讯后台开通授权。个人测试场景通常不需要。**具体权限要求以企业微信管理后台和 WorkBuddy App 提示为准**。

### Q5：WorkBuddy 能替代 Claude Code 写代码吗？

不能完全替代。WorkBuddy 的 Coding Mode 适合**小改、demo、原型、改 bug、写测试**——也就是"办公场景里偶尔要写点代码"。大型代码库重构、复杂架构、CI/CD 集成，仍然是 Claude Code / Codex 的主场。

### Q6：我要给整个团队部署，怎么算账号？

团队场景看 WB-09 企业安全章节，按席位计费、集中管理。本篇先解决"个人能不能用起来"的问题。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 能用一句话向同事解释 WorkBuddy 是什么
- [ ] 能说清它和 Claude Code / Codex 的核心差别（更简单 + 更中国）
- [ ] 知道自己属不属于它的目标用户
- [ ] 跑通了工坊三个场景（周报 Word / 企业微信推送 / 中文技术问答）
- [ ] 手上有四样产物（周报 / 推送记录 / 日志代码 / 核对笔记）
- [ ] 知道哪些场景**不该**用 WorkBuddy

**全部勾选后，你已经具备判断 WorkBuddy 是否值得你或你团队投入时间的能力。**

---

## 附录

### A. WorkBuddy 适合 / 不适合速查

| 场景 | 用 WorkBuddy | 改用其他工具 |
|---|---|---|
| 写周报、做汇报 PPT | ✅ | |
| 整理 PDF、汇总资料 | ✅ | |
| 企业微信分发、定时推送 | ✅ | |
| 中文办公场景、非技术同事 | ✅ | |
| 大型代码库重构 | | Claude Code |
| 写 Hooks / Subagent / SDK | | Claude Code |
| App + CLI + Cloud 多入口 | | Codex |
| 海外团队、用 Slack/Notion | | Codex / Claude Code |
| 本地完全控制、零云依赖 | | OpenClaw |

### B. 官方来源速查

- **产品主页（国际）**：https://www.workbuddy.ai/
- **产品主页（国内）**：https://www.codebuddy.cn/work
- **Tencent Cloud Techpedia（Coding Mode）**：https://www.tencentcloud.com/techpedia/144314
- **计费公告**：https://cloud.tencent.com/announce/detail/2270（以最新公告为准）

### C. 推荐学习资源

- **本系列上一篇**：[WB-00 阅读指南](./WB-00-阅读指南.md)
- **本系列下一篇**：[WB-02 WorkBuddy 安装与登录完整指南](./WB-02-WorkBuddy安装与登录完整指南.md)
- **本仓库兄弟主线**：
  - [Claude Code 系列](../claude-code/01-Claude-Code完整安装指南.md)（开发者深度定制）
  - [Codex 系列](../codex/CX-01-Codex-App安装与认证完整指南.md)（多入口协作）
  - [OpenClaw 系列](../openclaw/01-OpenClaw项目介绍.md)（本地开源）

---

**课程制作**：老金
**最后更新**：2026年8月6日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[WB-02 WorkBuddy 安装与登录完整指南](./WB-02-WorkBuddy安装与登录完整指南.md)。
