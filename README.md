# Claude Code & OpenClaw & Codex & WorkBuddy 中文教程

<div align="center">

<p>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/KimYx0207/AI-Coding-Guide-Zh?style=flat-square&amp;logo=github&amp;label=Stars"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh/forks"><img alt="Forks" src="https://img.shields.io/github/forks/KimYx0207/AI-Coding-Guide-Zh?style=flat-square&amp;logo=github&amp;label=Forks"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/KimYx0207/AI-Coding-Guide-Zh?style=flat-square&amp;label=License"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="Tutorial Version" src="https://img.shields.io/badge/教程版本-v5.3-blueviolet.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="Claude Code 参考版本" src="https://img.shields.io/badge/Claude_Code-2.1.270-green.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="OpenClaw 参考版本" src="https://img.shields.io/badge/OpenClaw-v2026.9.4-blue.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="Codex App 功能快照" src="https://img.shields.io/badge/Codex_App-26.908-orange.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="WorkBuddy 参考版本" src="https://img.shields.io/badge/WorkBuddy-5.5.6-purple.svg"></a>
</p>

**AI Coding / Agent 工作流中文实战教程**

</div>

> **先做出一个能检查的成果，再把方法用到自己的工作里。**
>
> 老金基于游戏研发、项目管理和数据分析经验，把四款工具放进日常任务里讲：修代码、写周报、处理表格、查资料、整理待办。每条入门路线都有材料和结果对照，做完再按需要深入。

## 把教程里的方法用进自己的项目

我还在维护 [Meta_Kim](https://github.com/KimYx0207/Meta_Kim)，把目标澄清、任务分工、结果复核和验证记录整理成可复用的 AI 工作流。它主要面向 Claude Code 和 Codex，也提供本地 Live 面板查看任务进展与证据。学完这套教程，想把这些做法带进自己的项目，可以先看 [Meta_Kim 中文说明](https://github.com/KimYx0207/Meta_Kim/blob/main/README.zh-CN.md)，按快速开始选安装范围，再用一项小任务核对结果。各客户端的支持程度和验证范围，以项目说明为准。

Meta_Kim 项目说明：[English](https://github.com/KimYx0207/Meta_Kim/blob/main/README.md) · [简体中文](https://github.com/KimYx0207/Meta_Kim/blob/main/README.zh-CN.md) · [日本語](https://github.com/KimYx0207/Meta_Kim/blob/main/README.ja-JP.md) · [한국어](https://github.com/KimYx0207/Meta_Kim/blob/main/README.ko-KR.md)。

## 今天先完成哪件事

第一次只选一行。已安装并登录，可以直接进入练习；尚未准备环境，先完成同一行的安装说明。练习时长是阅读与操作的参考，安装、网络和登录耗时另计。

| 你的任务 | 跟着做 | 做完能拿到什么 |
|---|---|---|
| 在终端里修一处代码错误 | [Claude Code 安装](docs/claude-code/01-Claude-Code完整安装指南.md) → [空列表进度练习](docs/claude-code/02-基础使用完整指南.md#先修一个小-bug空任务列表为什么显示-nan) | 复现 `NaN`，修复后通过检查，再独立补一道变式题 |
| 用桌面 App 完成一次小改动 | [Codex App 安装](docs/codex/CX-01-Codex-App安装与认证完整指南.md) → [App 修错练习](docs/codex/CX-02-Codex-App桌面工作流完整指南.md#先用-app-修一个小-bug) | 一份能在 Review 中看懂、能用运行结果检查的改动 |
| 把散乱记录整理成周报 | [WorkBuddy 安装](docs/workbuddy/WB-02-WorkBuddy安装与登录完整指南.md) → [第一份周报](docs/workbuddy/WB-01-WorkBuddy项目介绍完整指南.md#13-把任务交给它) | 保留未完成事项和改期信息的短周报、Word 草稿 |
| 让助手整理今天的待办 | [OpenClaw 安装](docs/openclaw/02-安装部署指南.md) → [待办简报](docs/openclaw/03-快速开始指南.md#先做一份今天的待办简报) | 去重、排除已完成、保留未知时间的行动列表 |

[打开配套练习材料](examples/README.md)：代码、工作记录、7 行订单和三份新旧说明都已备好，使用虚构数据。先照着做一轮，再修改一个条件，看看自己能否判断结果。

四条线保持各自重点：**Claude Code 编程、Codex App 工作流、OpenClaw 助手、WorkBuddy 办公**。CLI / Web / SDK / GitHub Action 在 Codex 系列中作为 App 生态补充。

> 🔗 **GitHub 仓库**：[https://github.com/KimYx0207/AI-Coding-Guide-Zh](https://github.com/KimYx0207/AI-Coding-Guide-Zh)

---

## 📖 项目简介

这是一套**系统化、适合循序学习、也能进入团队落地**的 AI Coding 与 Agent 工作流中文教程，覆盖四类代表性工具：

| | Claude Code | OpenClaw | Codex | WorkBuddy |
|--|-------------|----------|-------|---------|
| **是什么** | Anthropic 官方 AI 编程 CLI 工具 | 开源 AI 私人助手框架 | OpenAI 编程 Agent 平台 | 腾讯 AI 办公助手桌面 App |
| **干什么** | 终端里理解项目、改代码、排查错误 | 整理待办、查询资料，按需接入消息平台和定时任务 | 在 App 中安排任务、审阅改动，配合其他入口协作 | 整理文档和表格，用专家、资料库与连接器处理办公任务 |
| **谁出的** | Anthropic 官方 | Peter Steinberger（原名 Clawdbot，因 Claude 商标被迫改名） | OpenAI 官方（CLI 开源 Apache-2.0） | 腾讯云（与 CodeBuddy 同根生） |
| **教程数** | 13 篇 + 1 速查卡 | 12 篇完整教程 | 14 篇完整教程 | 11 篇完整教程 |

### 👤 作者定位

老金是合伙创业游戏研发公司出身，15 余年一线项目经验：从策划到整体项目负责人，长期处理多部门协同、团队管理、研发里程碑、版本节奏、数据分析和交付风险。

这套教程从项目里常见的小问题开始：进度怎么算、周报该写哪些事实、旧资料还能不能引用。读者先完成一个任务，学会检查和修正结果，再接入自己的工作流与团队规范。

### 🧬 为什么放在一起？

按任务选择工具，学到需要协作时再看其他主线：

1. **编程生产力** — Claude Code 适合深入本地项目、改代码、跑测试、做架构分析
2. **日常自动化** — OpenClaw 适合把 AI 接到消息平台、个人助理和企业流程里
3. **多入口协作** — Codex 适合 App / CLI / Web / Cloud / GitHub 等分层协作
4. **办公出活** — WorkBuddy 适合不写代码的同事，把周报、调研、文档和腾讯生态里的杂活交给 AI
5. **培训与管理** — 用同类任务比较工具选择、权限边界和团队协作方式

### ✨ 核心特色

- **🎓 四线学习路径**：Claude Code 编程线 + OpenClaw 助手线 + Codex Agent 线 + WorkBuddy 办公线，按目标选择
- **🧭 清晰路径**：从安装、第一轮任务到团队规范，按主线逐步推进
- **📚 分层阅读**：新手看路线图，开发者看实操，团队负责人看规范和安全
- **💻 有材料、有结果**：入门任务给出可复制素材、结果对照和常见错误，做完再换条件练一次
- **📊 事实核对**：关键版本号与 App / CLI 行为优先对照 **官方 Release / 文档** 修订；细节仍可能随上游快速变化，请以你本机版本为准
- **🔄 持续更新**：2026-10-03 全量检查了 50 篇教程和速查卡，修正影响安装、配置和跟练的变化；教程参考版本、上游发布记录与本机测试范围分别说明，见[逐章核查清单](docs/2026-10-03-核查清单.md)。

---

## 按高频任务找教程

先找与你手头工作最接近的一行。前四条入门路线已给出完整素材；深入章节会逐步用到你自己的项目或已授权资料。

| 手头的问题 | 从哪里开始 | 重点学会什么 |
|---|---|---|
| 刚接手一个仓库，不知道从哪看 | [Claude Code：只读分析项目](docs/claude-code/02-基础使用完整指南.md#第二步让-claude-先只读分析项目) | 找入口、运行方式和约束，再决定怎么改 |
| 一个 Bug 反复改不对 | [Claude Code 小 Bug](docs/claude-code/02-基础使用完整指南.md#先修一个小-bug空任务列表为什么显示-nan) / [Codex App 小 Bug](docs/codex/CX-02-Codex-App桌面工作流完整指南.md#先用-app-修一个小-bug) | 先复现，限定改动，再用同一检查确认 |
| AI 改了一堆代码，看不懂是否可靠 | [Codex：Review 四层阅读法](docs/codex/CX-10-Codex-Review-GitHub-PR完整指南.md#15-review-的四层阅读法) | 从文件范围、行为变化、检查结果看改动 |
| 周报写得漂亮，却漏了风险 | [WorkBuddy：周报练习](docs/workbuddy/WB-01-WorkBuddy项目介绍完整指南.md#13-把任务交给它) | 区分完成、未完成、改期和待确认 |
| 表格里有重复、空值和退款 | [WorkBuddy：7 行订单练习](docs/workbuddy/WB-03-WorkBuddy专家与专家团完整指南.md#13-第一次实战让数据分析师帮你看表格) | 先定口径，再清洗、汇总和画图 |
| 要把材料整理成 Word 或汇报演示 | [WorkBuddy：专家与专家团](docs/workbuddy/WB-03-WorkBuddy专家与专家团完整指南.md) | 给清受众、素材和结构，检查成稿再继续修改 |
| 新旧资料冲突，答案没有出处 | [WorkBuddy：三份资料问答](docs/workbuddy/WB-06-WorkBuddy知识库完整指南.md#第二步同一个问题查三份资料) | 看生效日期和适用范围，缺信息时保留待确认 |
| 会开完了，还不知道谁该做什么 | [WorkBuddy：提取下一步](docs/workbuddy/WB-06-WorkBuddy知识库完整指南.md#42-工作记录和会议纪要提取可执行的下一步) | 整理行动、负责人、时间和原文依据 |
| 待办重复，做完的还在催 | [OpenClaw：待办简报](docs/openclaw/03-快速开始指南.md#先做一份今天的待办简报) | 去重、筛选、更新状态，不补造时间 |
| 每次都要重新交代偏好 | [OpenClaw：用户画像和偏好记忆](docs/openclaw/07-记忆系统指南.md#用户画像和偏好记忆) | 区分长期偏好与临时任务，核对记忆内容 |
| 文件太多，需要批量整理或写小脚本 | [WorkBuddy：编程任务](docs/workbuddy/WB-09-WorkBuddy-Coding-Mode编程模式完整指南.md) | 先看处理清单，用副本试运行，再处理自己的文件 |
| 同一份检查、简报每天重复做 | [WorkBuddy 定时任务](docs/workbuddy/WB-07-WorkBuddy自动化与计划任务完整指南.md) / [Codex Automations](docs/codex/CX-09-Codex-Automations后台任务完整指南.md) | 先把手动流程跑顺，再设置触发、范围和失败处理 |

团队负责人可从 [Claude Code 企业实战](docs/claude-code/11-企业实战完整指南.md) 和 [Codex 安全与企业基线](docs/codex/CX-13-Codex安全企业完整指南.md) 补协作约定。带课时先选一条入门路线，让学员交出成果并解释一处改动，再安排后续章节。

---

## 📚 教程目录

### 🤖 Part 1：Claude Code — Anthropic 官方编程 CLI

| 序号 | 教程名称 | 学时 | 难度 | 必学度 | 说明 |
|------|---------|------|------|--------|------|
| 01 | [Claude Code完整安装指南](docs/claude-code/01-Claude-Code完整安装指南.md) | 2-3h | ⭐ | ⭐⭐⭐ | 环境搭建、API配置、IDE集成 |
| 02 | [基础使用完整指南](docs/claude-code/02-基础使用完整指南.md) | 4-6h | ⭐ | ⭐⭐⭐ | 从小 Bug 跟练开始，继续学项目规则、使用模式与命令 |
| 03 | [Commands系统完整指南](docs/claude-code/03-Commands系统完整指南.md) | 4-6h | ⭐⭐ | ⭐⭐ | Slash 命令、Skills 工作流与兼容层 |
| 04 | [MCP集成完整指南](docs/claude-code/04-MCP集成完整指南.md) | 4-6h | ⭐⭐ | ⭐⭐⭐ | 10+核心服务器、自定义开发 |
| 05 | [Hooks系统完整指南](docs/claude-code/05-Hooks系统完整指南.md) | 4-6h | ⭐⭐ | ⭐⭐⭐ | 多事件 Hook、4 类处理器、自动化工作流 |
| 06 | [Subagent子代理完整指南](docs/claude-code/06-Subagent子代理完整指南.md) | 1-2h | ⭐⭐ | ⭐⭐ | 官方 Subagents、Agent 委派、Agent Teams（实验性） |
| 07 | [Skills定制完整指南](docs/claude-code/07-Skills定制完整指南.md) | 6-8h | ⭐⭐ | ⭐⭐ | 创建可复用功能包 |
| 08 | [Plugins生态完整指南](docs/claude-code/08-Plugins生态完整指南.md) | 4-6h | ⭐⭐ | ⭐ | `/plugin`、市场、作用域与本地开发 |
| 09 | [Agent-SDK完整指南](docs/claude-code/09-Agent-SDK完整指南.md) | 6-8h | ⭐⭐⭐ | ⭐⭐ | 编程开发AI Agent |
| 10 | [综合实战完整指南](docs/claude-code/10-综合实战完整指南.md) | 2-3h | ⭐⭐⭐ | ⭐⭐ | 团队协作、CI/CD集成 |
| 11 | [企业实战完整指南](docs/claude-code/11-企业实战完整指南.md) | 4-6h | ⭐⭐⭐ | ⭐ | 企业级最佳实践 |
| 12 | [Remote Control完整指南](docs/claude-code/12-Remote-Control完整指南.md) | 1-2h | ⭐⭐ | ⭐⭐ | 跨设备继续本地会话、`/remote-control`、`claude remote-control` |
| 13 | [Channels与计划任务完整指南](docs/claude-code/13-Channels与计划任务完整指南.md) | 2-3h | ⭐⭐⭐ | ⭐ | `--channels`、`/schedule`、`/loop`、`CronCreate` |

**速查**：[Claude Code 快速导航卡](docs/claude-code/快速导航卡.md)

### 🦞 Part 2：OpenClaw — 开源 AI 助手

| 序号 | 教程名称 | 难度 | 说明 |
|------|---------|------|------|
| OC-00 | [阅读指南](docs/openclaw/00-阅读指南.md) | 🟢 | 术语表、文档地图、4条阅读路线 |
| OC-01 | [项目介绍](docs/openclaw/01-OpenClaw项目介绍.md) | 🟢 | OpenClaw 是什么、发展历史、核心架构 |
| OC-02 | [安装部署](docs/openclaw/02-安装部署指南.md) | 🟢 | macOS / Linux / Windows 全平台安装 |
| OC-03 | [快速开始](docs/openclaw/03-快速开始指南.md) | 🟢 | 完成第一份待办简报，再学本地对话与基础检查 |
| OC-04 | [AI 模型配置](docs/openclaw/04-模型配置指南.md) | 🟡 | 接入 OpenAI / Claude / Ollama 等模型 |
| OC-05 | [消息平台接入](docs/openclaw/05-消息平台接入指南.md) | 🟡 | 连接 WhatsApp / Telegram / Discord / 飞书等平台 |
| OC-06 | [技能系统](docs/openclaw/06-技能系统指南.md) | 🟡 | 技能生态与自定义技能开发 |
| OC-07 | [记忆系统](docs/openclaw/07-记忆系统指南.md) | 🟡 | AI 如何记住你的偏好和上下文 |
| OC-08 | [多 Agent 协作](docs/openclaw/08-多Agent协作指南.md) | 🔴 | 一个网关跑多个独立 AI 助手 |
| OC-09 | [Docker 部署](docs/openclaw/09-Docker部署指南.md) | 🔴 | 容器化部署与 VPS 远程访问 |
| OC-10 | [安全配置](docs/openclaw/10-安全配置指南.md) | 🔴 | 安全配置、CVE 防护、权限管理 |
| OC-11 | [常见问题](docs/openclaw/11-常见问题FAQ.md) | 🟢 | 踩坑指南与解决方案 |

### 🤖 Part 3：Codex — OpenAI 编程 Agent 平台

Codex 学习主线：**只有 Codex App 一条主线**。先看 CX-01 安装认证和 CX-02 App 桌面工作流；CX-03 到 CX-10 按功能拆开讲 Commands、项目指令、MCP、Skills、Plugins、Subagents、Automations、Review / GitHub；CX-11 和 CX-12 分别是 Web / Cloud、CLI 辅助；CX-13 安全企业；CX-14 为 Claude Code 对比附录。

| 序号 | 教程名称 | 学时 | 难度 | 说明 |
|------|---------|------|------|------|
| CX-01 | [Codex App 安装与认证](docs/codex/CX-01-Codex-App安装与认证完整指南.md) | 1-2h | ⭐ | Windows Microsoft Store / 防火墙，macOS 官方下载 / Gatekeeper，登录、本地项目和第一个线程 |
| CX-02 | [Codex App 桌面工作流](docs/codex/CX-02-Codex-App桌面工作流完整指南.md) | 3-4h | ⭐⭐⭐ | 先修一处代码并 Review，再深入 Thread、Local、Worktree、Settings |
| CX-03 | [Commands 工作流入口](docs/codex/CX-03-Codex-Commands工作流入口完整指南.md) | 2-3h | ⭐⭐⭐ | App 里的 slash commands、/status、/plan、/review、/mcp，以及 /goal 等长目标入口的确认方法 |
| CX-04 | [项目指令、权限与配置](docs/codex/CX-04-Codex项目指令权限配置完整指南.md) | 2-3h | ⭐⭐⭐ | AGENTS.md、App Settings、权限、沙盒、Rules、Hooks |
| CX-05 | [MCP 外部工具连接](docs/codex/CX-05-Codex-MCP外部工具完整指南.md) | 2-3h | ⭐⭐⭐ | App 中接浏览器、数据库、文档源、内部 API 等外部工具 |
| CX-06 | [Skills 可复用工作流](docs/codex/CX-06-Codex-Skills可复用工作流完整指南.md) | 2-3h | ⭐⭐⭐ | 在 App 中点名、触发、编写和共享 Skills |
| CX-07 | [Plugins / Connectors](docs/codex/CX-07-Codex-Plugins连接器完整指南.md) | 2-3h | ⭐⭐⭐ | App 能力包、GitHub/Gmail/Drive/Slack 等账号连接 |
| CX-08 | [Subagents 多 Agent 协作](docs/codex/CX-08-Codex-Subagents多Agent协作完整指南.md) | 2-3h | ⭐⭐ | App 中的并行分析、分工实现、只读审查与 worktree 配合 |
| CX-09 | [Automations 后台任务](docs/codex/CX-09-Codex-Automations后台任务完整指南.md) | 2-3h | ⭐⭐ | App 里的周期检查、提醒、monitor、Skills + Automation |
| CX-10 | [Review / GitHub / PR](docs/codex/CX-10-Codex-Review-GitHub-PR完整指南.md) | 2-3h | ⭐⭐⭐ | 从 App diff 到 GitHub PR、CI 修复和 Cloud 接力 |
| CX-11 | [Web / Cloud 辅助路径](docs/codex/CX-11-Codex-Web-Cloud辅助指南.md) | 1-2h | ⭐⭐ | 远程仓库、云端 environment、PR 长任务；不是 App 主线 |
| CX-12 | [CLI 辅助指南](docs/codex/CX-12-Codex-CLI辅助完整指南.md) | 1-2h | ⭐⭐ | 终端排查、CI、codex review、MCP/plugin 管理；不是主线 |
| CX-13 | [安全与企业基线](docs/codex/CX-13-Codex安全企业完整指南.md) | 2-3h | ⭐⭐⭐ | 审批、沙盒、Rules、Hooks、MCP/Plugins/Automations 权限 |
| CX-14 | [Codex 与 Claude Code 对比](docs/codex/CX-14-Codex与Claude-Code对比指南.md) | 1-2h | ⭐⭐ | 从 App 主线出发做双工具选择和共存 |

### 🐧 Part 4：WorkBuddy — 腾讯 AI 办公助手

WorkBuddy 主线面向**办公人和国内团队**：会用电脑但不会命令行的人、用企业微信/腾讯文档的团队、想给非技术同事一个 AI 工具的人。跟另外三条开发者主线互补，不冲突。先看 WB-00 阅读指南找到学习路径，再按需学 WB-01~WB-10。

| 序号 | 教程名称 | 学时 | 难度 | 说明 |
|------|---------|------|------|------|
| WB-00 | [阅读指南](docs/workbuddy/WB-00-阅读指南.md) | 5 分钟 | 🟢 | 五大核心概念、文档地图、阅读路线 |
| WB-01 | [项目介绍](docs/workbuddy/WB-01-WorkBuddy项目介绍完整指南.md) | 30-60 分钟 | ⭐ | 用 5 条工作记录完成周报，检查事实，再保存 Word 草稿 |
| WB-02 | [安装与登录](docs/workbuddy/WB-02-WorkBuddy安装与登录完整指南.md) | 20-40 分钟 | ⭐ | Win/Mac 双平台安装、微信扫码、跑通第一个任务 |
| WB-03 | [专家与专家团](docs/workbuddy/WB-03-WorkBuddy专家与专家团完整指南.md) | 1-2h | ⭐⭐ | 7 行订单清洗、专家团与行业 Buddy 跟练 |
| WB-04 | [技能与技能市场](docs/workbuddy/WB-04-WorkBuddy技能与技能市场完整指南.md) | 1-2h | ⭐⭐ | 一键装技能、发邮件查股价读写文件 |
| WB-05 | [连接器与腾讯生态](docs/workbuddy/WB-05-WorkBuddy连接器与腾讯生态完整指南.md) | 1-2h | ⭐⭐ | 接 QQ 邮箱/腾讯文档/腾讯会议/企业微信 |
| WB-06 | [资料库与知识问答](docs/workbuddy/WB-06-WorkBuddy知识库完整指南.md) | 入门 15–20 分钟 | ⭐⭐ | 三份新旧资料练引用、版本判断和纠错，管理与组合用法按需学 |
| WB-07 | [定时任务与远程执行](docs/workbuddy/WB-07-WorkBuddy自动化与计划任务完整指南.md) | 1-2h | ⭐⭐ | 手动跑通后再定时执行，检查在线前提、记录和失败处理 |
| WB-08 | [多端协同](docs/workbuddy/WB-08-WorkBuddy多端协同完整指南.md) | 1h | ⭐⭐ | 桌面与手机任务核对、助理绑定及运行条件 |
| WB-09 | [编程任务与 Worktree](docs/workbuddy/WB-09-WorkBuddy-Coding-Mode编程模式完整指南.md) | 1-2h | ⭐⭐ | 小脚本、执行模式、Worktree 并行修改与本地合并 |
| WB-10 | [企业账号、安全与对比](docs/workbuddy/WB-10-WorkBuddy企业账号安全与对比完整指南.md) | 1-2h | ⭐⭐⭐ | 账号积分、私有云、安全边界、四工具横向对比 |

---

## 📋 环境要求
### Claude Code

- **操作系统**：Windows 10 1809+ / Server 2019+、macOS 13+，Linux 按官方支持的发行版与依赖选择，详见安装指南
- **安装方式**：支持标准安装（`npm install -g @anthropic-ai/claude-code`，需 Node.js 22+）和原生二进制安装；两种方式安装同一原生二进制
- **认证方式**：可用 Claude 订阅登录，也可用 Anthropic Console / 第三方兼容提供商配置
- **IDE**：VS Code、Cursor、Windsurf 或其他支持的编辑器

> ⚠️ **2026年更新**：Claude Code 已提供原生二进制安装，但 **Node.js 22+ 的标准 npm 安装路径仍然受支持**。本仓库安装指南现同时覆盖两条路径，并明确各自适用场景。

### OpenClaw

- **Node.js**：OpenClaw v2026.9.4 推荐 26.x（至少 26.1.0）；兼容 24.x 时至少 24.16.0。25.x 和 26.0.x 不在支持范围内，详见 [安装要求](docs/openclaw/02-安装部署指南.md#2-nodejs-环境安装)
- **AI 模型 API Key**：OpenAI / Anthropic / Google 等（或使用 Ollama 本地模型免 Key）
- **操作系统**：macOS / Linux / Windows（推荐 WSL2）

### Codex

- **Codex App**：App 26.908（2026-09-11）保留为功能快照；安装与安全更新按当前官方入口核对；Codex 已并入 ChatGPT 桌面 App（26.707 起），macOS 从官方入口安装，Windows 以 Microsoft Store / `winget -s msstore` 等官方安装入口为准
- **CLI / Web / Cloud 辅助**：CLI 仅用于终端排查、CI、MCP / plugin 管理等辅助场景；Web / Cloud 用于远程仓库和长任务接力，版本以官方文档和当前账号能力为准
- **认证方式**：ChatGPT 账户登录 或 OpenAI API Key

### WorkBuddy

- **WorkBuddy 桌面 App**：腾讯云出品，账号与积分关系见当前套餐说明；Windows 使用官方支持的 x64 版本，macOS 按官网下载页提供的系统与芯片安装包选择。官方更新日志已列到 5.6.2（2026-09-21），安装从官网首页开始
- **多端**：桌面与手机先核对同一账号和任务，微信/企业微信助理按官方流程绑定；各端可用材料和功能分别检查
- **认证方式**：客户端打开官网登录页，可用微信、手机号、邮箱等方式；企业 SSO 按公司配置及当前页面使用
- **网络**：国内服务器直连，正常办公网络不用代理

---

## 🚀 快速开始

### 取得练习材料

可在 [examples](examples/README.md) 打开并保存单个文件；对应课程也附有完整文本。已经会用 Git 的读者可以克隆仓库：

```bash
git clone https://github.com/KimYx0207/AI-Coding-Guide-Zh.git
cd AI-Coding-Guide-Zh
```

### Claude Code：从一次修错开始

```
Step 1：01 安装指南 → 选择适合本机的安装路径，完成登录
Step 2：02 基础使用 → 用练习材料复现、修复空列表 Bug，重跑测试
Step 3：02 基础使用 → 把真实项目的运行方式和约束写入 CLAUDE.md
接下来：需要外部工具时学 MCP，需要重复动作时学 Hooks / Skills
```

### OpenClaw：从今天的简报开始

```
Step 1：OC-02 安装 → 版本检查、初始化；模型未就绪时对照 OC-04
Step 2：OC-03 快速开始 → 确认模型能回复，再整理示例待办
Step 3：更新一条完成状态 → 对照新的简报，检查是否仍在催已完成事项
接下来：按需求学 OC-07 记忆或 OC-05 消息平台
```

### Codex：在 App 中改一次、看一次

```
Step 1：CX-01 安装与认证 → 装好 App，打开本地练习目录
Step 2：CX-02 小 Bug 练习 → 先复现，再修改，在 Review 中对照
Step 3：自己补 3/8 的检查 → 运行后解释为什么应得到 38
接下来：CX-04 项目指令；需要协作审查时学 CX-10
```

### WorkBuddy：把一周记录整理清楚

```
Step 1：WB-02 安装与登录 → 完成登录，找到任务入口
Step 2：WB-01 周报练习 → 输入 N1–N5，检查未完成和改期，再保存草稿
Step 3：自己改变一条事实 → 让它只修订相关段落，并核对结果
接下来：处理表格去 WB-03，查询资料去 WB-06
```

### 需要系统学习时

下面是分阶段阅读参考，可只选择一条主线。时间取决于已有经验和练习结果，不代表按周读完就能掌握所有功能。

```
Week 1-2：Claude Code 安装 + 基础使用 + MCP
Week 3-4：Claude Code Hooks + Skills + Plugins
Week 5  ：Claude Code 模型配置 + Remote Control + Channels/计划任务
Week 6  ：Claude Code Agent-SDK + 综合实战
Week 7  ：OpenClaw 安装 + 快速开始 + 模型配置
Week 8  ：OpenClaw 消息平台 + 技能系统 + 记忆系统
Week 9  ：OpenClaw 多Agent + Docker部署 + 安全
Week 10 ：Codex App 安装 + App 桌面工作流 + Commands
Week 11 ：项目指令 + MCP + Skills + Plugins / Connectors + Subagents
Week 12 ：Automations + Review / GitHub / PR + Web/Cloud/CLI 辅助 + 安全
Week 13：WorkBuddy 安装 + 项目介绍 + 专家与专家团
Week 14：WorkBuddy 技能 + 连接器 + 知识库 + 自动化 + 多端 + 企业安全
```

---

## 🧰 配套开源项目（老金出品）

Meta_Kim 的介绍与开始入口放在首页前面。学习 Hook 与 Skill 时，还可以按需看 [Kim_Service](https://github.com/KimYx0207/Kim_Service)：各子项目提供自己的 README 或 SKILL.md，选择当前需要的方法，再按说明安装和验证。不要为了跟练一次装完整个合集。

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **教程总数** | 50 篇完整教程（Claude Code 13 / OpenClaw 12 / Codex 14 / WorkBuddy 11）+ 1 速查卡 |
| **内容体量** | 120万+ Markdown 字符（含正文、命令、代码、配置、提示词和 FAQ） |
| **中文核心内容** | 36万+ 中文字 |
| **代码 / 命令 / 配置示例** | 3200+ 个代码块与实操片段（核心示例按当前版本持续校验） |
| **FAQ / 问答条目** | 500+ 个 |
| **覆盖AI模型** | OpenClaw 支持多个主流模型提供商，具体目录以当前安装版本和官方 Models / Onboarding 为准 |
| **覆盖消息平台** | WhatsApp、Telegram、Slack、Discord、Signal、Google Chat、iMessage、Microsoft Teams、Matrix、飞书、LINE、Mattermost、Nextcloud Talk、Nostr、Synology Chat、Twitch、Zalo、WeChat、QQ 等 |
| **参考版本与测试范围** | 各章保留适用版本和功能引入日期；最新发布记录与本机核查范围见下表及[核查清单](docs/2026-10-03-核查清单.md) |

---

## 🔖 版本说明

> **版本校验方法**：本仓库教程中的版本号和 App / CLI 行为，优先对照 **官方 Release / 官方文档** 修订。上游产品迭代很快，部分细节可能在你阅读时已发生变化。
>
> **遇到版本不一致时**：以你本机 App About / Settings、系统应用信息、`claude --version`、CLI `codex --version` 或 `npm list -g` 的输出为准，教程示例按官方最新文档调整。

| 产品 | 教程参考与本次核查范围 | 官方发布记录（2026-10-03 查询） | 官方来源 |
|---|---|---|---|
| Claude Code | 保留 2.1.270 的历史功能说明；按现行文档修正安装、权限、SDK 等。本机 CLI 2.1.236 只读核查 | changelog 最新条目 2.1.288；没有升级本机或执行模型请求 | [Claude Code changelog](https://code.claude.com/docs/en/changelog) |
| OpenClaw | 配置与 Docker 示例按 v2026.9.4 源码复核；本机 2026.7.1-2 只核 help，不验证新版服务行为 | 最新 Release v2026.9.8；不能由版本号推断旧状态可以直接降级 | [GitHub Releases](https://github.com/openclaw/openclaw/releases) |
| ChatGPT / Codex 桌面 App | 26.908 为原功能快照，安装走当前 ChatGPT 桌面入口 | macOS 26.924.20706 修复 9 月 25 日公告的安全问题；安装取官网更新版本 | [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog) |
| Codex CLI | 本机 0.157.1 的 help 与已装入口，以及官方 0.160.0 源码、schema | rust-v0.160.0，10 月 1 日发布；没有升级本机 | [GitHub Release](https://github.com/openai/codex/releases/tag/rust-v0.160.0) |
| WorkBuddy | 现行可访问的官方文档；账号界面与真实授权未实跑 | 更新日志 5.6.2；原价格表保留 9 月 14 日快照，未取得现价正文 | [WorkBuddy 更新日志](https://www.workbuddy.cn/docs/workbuddy/Changelog) |

### 这次具体修了什么

Claude Code 的 npm 安装仍受支持，现行要求是 Node.js 22+；交互、打印模式、工具预批准和实际访问权限也要分清。SDK 示例改成 Python 的真实消息类型，并修正计算器、通知与 Action 示例。

Codex 的桌面安装入口已经迁到 ChatGPT，新 Cloud 环境要先准备、保存并发布；旧 Cloud 的阶段网络与 Secret 规则不能直接搬过来。后台任务结果入口同步为 Scheduled，CLI 参数与权限配置也按实际 help 和源码修正。

OpenClaw 保留明确的参考版本，修正模型、技能、消息平台、路由、记忆和 Docker 备份恢复说明。WorkBuddy 修正登录、菜单、助理及连接器流程，补可对照的练习数据；没有取得依据的固定耗时、费用倍率与权限保证不继续当作产品事实。

旧轮次的详细记录统一放在 [CHANGELOG.md](CHANGELOG.md)。完整范围见[逐章核查清单](docs/2026-10-03-核查清单.md)，其中也列了无需修改的章节与未能核实的内容。安装和界面以当前官方说明与本机版本为准；参考答案表示核对方法，不表示当天在 AI 客户端实跑。

---

## 🔌 第三方模型配置说明

下面三条开发者主线都支持多种模型接入方式，具体配置见各教程：

| 产品 | 支持方式 | 配置入口 |
|------|---------|---------|
| **Claude Code** | Anthropic Console / Claude 订阅 / 第三方兼容提供商（`ANTHROPIC_BASE_URL`） | [01-安装指南：API中转站配置](docs/claude-code/01-Claude-Code完整安装指南.md) |
| **OpenClaw** | 多个主流提供商（OpenAI / Claude / Gemini / Ollama / 本地模型等，实际以当前模型目录为准） | [04-模型配置指南](docs/openclaw/04-模型配置指南.md) |
| **Codex** | ChatGPT 账户登录 / OpenAI API Key | [CX-01 App 安装与认证](docs/codex/CX-01-Codex-App安装与认证完整指南.md) |

> ⚠️ **第三方模型注意事项**：
> - 第三方兼容提供商的 API 行为可能不完全等同于官方（速率限制、模型列表、功能支持可能有差异）
> - 本地模型（Ollama 等）能力取决于模型本身，复杂任务可能不如旗舰模型
> - 各提供商计费方式不同，使用前请确认价格策略

---

## 🎯 适用人群

- ✅ **刚入门的读者**：从未接触过 AI 编程工具，想系统学习
- ✅ **办公人 / 业务用户 / 国内团队**：想用 AI 出周报、调研、PPT，被英文 CLI 劝退过，WorkBuddy 主线为你准备
- ✅ **开发者**：想用 Claude Code 提升编程效率 + 用 OpenClaw 自动化日常工作
- ✅ **团队负责人 / PM**：为团队制定 AI 工具使用规范、评审流程和里程碑验收方式
- ✅ **企业用户**：企业级部署、安全边界、权限管理和最佳实践
- ✅ **高校 / 培训机构**：设计 AI Coding、Agent 工作流和企业实践课程
- ✅ **AI 爱好者**：想搭建自己的 AI 私人助手

---

## 💡 学习建议

### 初学者

**想学编程 AI** → 从 Claude Code Part 1 开始（01 安装 → 02 小 Bug → 项目规则）

**想搭建 AI 助手** → 从 OpenClaw Part 2 开始（OC-01 → OC-02 → OC-03）

**想试 Codex** → 从 Codex Part 3 开始（CX-01 → CX-02 或 CX-03）

**想让 AI 帮忙出办公产物** → 从 WorkBuddy Part 4 开始（WB-00 → WB-02 → WB-01）

**都想学** → 先走 Claude Code CLI 主线，再补 Codex App 桌面工作流，然后学 OpenClaw 助手框架；办公同事另走 WorkBuddy 主线

### 进阶者（有基础）

- Claude Code 重点：04-MCP、05-Hooks、06-Subagent、07-Skills
- OpenClaw 重点：06-技能系统、08-多Agent路由
- Codex 重点：CX-04 项目指令与权限配置、CX-05 MCP、CX-06 Skills、CX-07 Plugins / Connectors

### 高级者（深度定制）

- Claude Code：09-Agent-SDK、10-综合实战
- OpenClaw：08-多Agent、09-Docker部署、10-安全
- Codex：CX-04 项目指令与权限、CX-08 Subagents、CX-09 Automations、CX-10 Review / PR、CX-13 安全企业
- **双工具协作**：Codex + Claude Code 的定位、边界和共存策略详见 CX-14
- 长期 Skill 治理：可参考 [SkillClaw](https://github.com/AMAP-ML/SkillClaw)（skill 演化、去重、合并、共享；论文 [arXiv:2604.08377](https://arxiv.org/abs/2604.08377)）

---

## 📞 联系方式

<div align="center">
  <img src="images/二维码基础款.png" alt="联系方式" width="600"/>
  <p><strong>获取更多 AI 资讯、企业落地和高校培训支持</strong></p>
  <p>
    👤 <strong>作者：老金</strong> | 🔗 <a href="https://github.com/KimYx0207">GitHub</a> | 🌐 <a href="https://aiking.dev/">aiking.dev</a> | 𝕏 <a href="https://x.com/KimYx0207">老金带你玩AI</a> | 📱 微信公众号：<strong>老金带你玩AI</strong>
  </p>
  <p>老金的开源知识库，实时更新群二维码：https://my.feishu.cn/wiki/OhQ8wqntFihcI1kWVDlcNdpznFf</p>
</div>

### ☕ 请我喝杯咖啡

<div align="center">
  <p><strong>如果这个教程对你有帮助，欢迎打赏支持！</strong></p>
  <table align="center">
    <tr>
      <td align="center">
        <img src="images/微信.jpg" alt="微信收款码" width="300"/>
        <br/>
        <strong>微信支付</strong>
      </td>
      <td align="center">
        <img src="images/支付宝.jpg" alt="支付宝收款码" width="300"/>
        <br/>
        <strong>支付宝</strong>
      </td>
    </tr>
  </table>
</div>

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

- 发现错误或过时信息，请提交 Issue
- 有改进建议，欢迎提交 PR
- 想分享使用经验，欢迎在 Discussions 讨论

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。你可以复制、修改、分发和商用，但必须在副本或重要片段中保留版权声明与许可声明。教程作者为老金，原始仓库为 [KimYx0207/AI-Coding-Guide-Zh](https://github.com/KimYx0207/AI-Coding-Guide-Zh)，署名与原始来源见 [NOTICE](NOTICE)。

---

## 🙏 致谢

感谢所有为 Claude Code、OpenClaw、Codex 和 WorkBuddy 生态做出贡献的开发者和社区成员！

---

## 📋 更新说明

完整更新记录统一维护在 [CHANGELOG.md](CHANGELOG.md)。README 保留当前定位、目录、版本基线和阅读入口，避免同一条版本说明在多处漂移。

---

## ⚠️ 免责声明

- 本次核查日期为 2026-10-03，教程参考版本、实际测试与未能核实的范围见[核查清单](docs/2026-10-03-核查清单.md)。WorkBuddy 价格与活动保留注明日期的快照，采购前查看当前订单和官方说明。
- **预发布与 `latest` 以各项目 [Releases](https://github.com/openclaw/openclaw/releases) 与本机版本为准**（持续更新中）
- 部分功能可能随版本更新而变化，请以官方文档为准
- 本教程是学习和实践参考，重要项目请先在测试仓库 / 测试环境验证，再进入生产流程

---

<div align="center">
  <p>⭐ 如果这个教程对你有帮助，欢迎 Star 支持！</p>
  <p>也欢迎把它转给正在学习 AI 编程和 Agent 工作流的朋友。</p>
</div>
