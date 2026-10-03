# Claude Code & OpenClaw & Codex & WorkBuddy 中文教程

<div align="center">

<p>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/KimYx0207/AI-Coding-Guide-Zh?style=flat-square&amp;logo=github&amp;label=Stars"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh/forks"><img alt="Forks" src="https://img.shields.io/github/forks/KimYx0207/AI-Coding-Guide-Zh?style=flat-square&amp;logo=github&amp;label=Forks"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/KimYx0207/AI-Coding-Guide-Zh?style=flat-square&amp;label=License"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="Tutorial Version" src="https://img.shields.io/badge/教程版本-v5.2-blueviolet.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="Claude Code" src="https://img.shields.io/badge/Claude_Code-2.1.270-green.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="OpenClaw" src="https://img.shields.io/badge/OpenClaw-v2026.9.4-blue.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="Codex App" src="https://img.shields.io/badge/Codex_App-26.908-orange.svg"></a>
  <a href="https://github.com/KimYx0207/AI-Coding-Guide-Zh"><img alt="WorkBuddy" src="https://img.shields.io/badge/WorkBuddy-5.5.6-purple.svg"></a>
</p>

**AI Coding / Agent 工作流中文实战教程**

</div>

> **先做出一个能检查的成果，再把方法用到自己的工作里。**
>
> 老金基于游戏研发、项目管理和数据分析经验，把四款工具放进日常任务里讲：修代码、写周报、处理表格、查资料、整理待办。每条入门路线都有材料和结果对照，做完再按需要深入。

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
- **🔄 持续更新**：教程基线为 Claude Code v2.1.270 / OpenClaw v2026.9.4 / Codex App 26.908 / WorkBuddy 5.5.6；Codex CLI 辅助基线为 0.154.0（核查日：2026-09-14，使用时对照官方 changelog 和本机版本）。

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
| WB-08 | [多端协同](docs/workbuddy/WB-08-WorkBuddy多端协同完整指南.md) | 1h | ⭐⭐ | 桌面/微信/小程序/企业微信无缝接力 |
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

- **Codex App**：当前主线按 App 26.908（2026-09-11 官方 changelog）复核；Codex 已并入 ChatGPT 桌面 App（26.707 起），macOS 从官方入口安装，Windows 以 Microsoft Store / `winget -s msstore` 等官方安装入口为准
- **CLI / Web / Cloud 辅助**：CLI 仅用于终端排查、CI、MCP / plugin 管理等辅助场景；Web / Cloud 用于远程仓库和长任务接力，版本以官方文档和当前账号能力为准
- **认证方式**：ChatGPT 账户登录 或 OpenAI API Key

### WorkBuddy

- **WorkBuddy 桌面 App**：腾讯云出品，与 CodeBuddy 同账号同团队、积分共享；Windows 10/11、macOS（Apple Silicon / Intel）都支持。当前客户端 5.5.6（2026-09-10），从官网首页下最新版即可——官方文档里的「历史版本下载」页只归档到 v5.1.2，别拿它当下载口
- **多端**：桌面 App + 微信公众号/小程序 + 企业微信，同一微信账号打通
- **认证方式**：微信扫码（推荐）、QQ 扫码、手机号验证码、腾讯云账号密码
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

教程里讲到的 Hook、Skill、多 Agent 编排和结果验证，下面两个仓库给出了能直接装进 Claude Code / Codex 环境的实现。学到对应章节时顺手装上，比只看文字快。

| 项目 | 解决什么问题 | 什么时候装 | 许可 |
|------|-------------|-----------|------|
| [**Meta_Kim**](https://github.com/KimYx0207/Meta_Kim)<br>[简体中文说明](https://github.com/KimYx0207/Meta_Kim/blob/main/README.zh-CN.md) | 给 Claude Code / Codex / OpenClaw / Cursor 加一层治理执行：先把模糊需求整理成目标和验收标准，再路由到合适的 agent、skill 和工具，安全的活并行拆开，做完先 Review 再核验证据，可复用的经验经审批写回。自带本地 Live 看板，一张执行图看清每次运行的分工、阻塞项、产出和验证证据；没跑的检查会明确标成未验证，不会当成通过 | 学完 Claude Code 05 Hooks、06 Subagent，或 Codex CX-08 Subagents 之后，想把「多 Agent + 验证」真正用进项目 | Apache-2.0 |
| [**Kim_Service**](https://github.com/KimYx0207/Kim_Service) | 老金自制维护的 Hook 与 Agent Skill 合集（除 Find Skill 是在开源项目基础上改造，其余均为原创），按需单独装：HookPrompt（把随口说的需求整理成可验收的提示词）、Agent Teams Playbook（多 Agent 并行编排）、Memory 3-Layer（三层记忆）、GoalPro（Goal / Loop Prompt）、Kim Decision（把模糊问题收敛成有证据的决策）、Meta Skill Creator（做 Skill 的 Skill）、Semgrep Skill（代码安全扫描）、Find Skill（找并装 Skill）、Xiaohongshu Skill | 学 Claude Code 05 Hooks、07 Skills，或 Codex CX-06 Skills 时，想拿现成的用，或者照源码学怎么写 | MIT（各子项目许可独立生效） |

Meta_Kim 一条命令装好：

```bash
npx --yes github:KimYx0207/Meta_Kim meta-kim
```

装完在 Claude Code 或 Codex 里照常提需求即可，不用背命令；第一次治理运行会自动拉起本地 Live 看板，手动打开用 `meta-kim live`。Kim_Service 里每个 Hook / Skill 都带自己的 README 或 SKILL.md，进对应目录按说明装到项目或个人环境。两个仓库都在持续更新（核查日 2026-09-13：Meta_Kim v3.1.2，Kim_Service V1.1），版本以各自的 Releases 为准。

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
| **Claude Code版本** | 教程基线 v2.1.270，与 npm `latest` 一致；`stable` 仍为 2.1.236，两者是不同发布通道（核查日：2026-09-14；来源 npm registry 与 [GitHub Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.270)） |
| **OpenClaw版本** | 教程基线 v2026.9.4，与上游 npm `latest` 一致（`extended-stable` 2026.6.35；核查日：2026-09-13） |
| **Codex版本** | 教程基线 Codex App 26.908（2026-09-11 官方 changelog）+ Codex CLI 0.154.0（与上游 npm `latest` 一致；核查日：2026-09-13）；App 版本以本机"关于"页和官方 changelog 为准 |
| **WorkBuddy版本** | 教程基线客户端 5.5.6（2026-09-10，官方更新日志）；与 CodeBuddy 同账号同团队，积分共享 |

---

## 🔖 版本说明

> **版本校验方法**：本仓库教程中的版本号和 App / CLI 行为，优先对照 **官方 Release / 官方文档** 修订。上游产品迭代很快，部分细节可能在你阅读时已发生变化。
>
> **遇到版本不一致时**：以你本机 App About / Settings、系统应用信息、`claude --version`、CLI `codex --version` 或 `npm list -g` 的输出为准，教程示例按官方最新文档调整。

| 产品 | 教程基线版本 | 上游当前版本（核查日 2026-09-14） | 官方来源 |
|------|-------------|------------------|---------|
| Claude Code | v2.1.270 | npm `latest` 2.1.270 / `stable` 2.1.236 | [Claude Code changelog](https://code.claude.com/docs/en/changelog) / [GitHub Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.270) |
| OpenClaw | v2026.9.4 | npm `latest` 2026.9.4 / `extended-stable` 2026.6.35 | [GitHub Releases](https://github.com/openclaw/openclaw/releases) |
| Codex App | 26.908 | 26.908（2026-09-11 官方 changelog） | [Codex changelog](https://developers.openai.com/codex/changelog) |
| Codex CLI | 0.154.0 | npm `latest` 0.154.0 | [Codex changelog](https://developers.openai.com/codex/changelog) / [GitHub Releases](https://github.com/openai/codex/releases) |
| WorkBuddy | 客户端 5.5.6 | 5.5.6（2026-09-10 官方更新日志） | [WorkBuddy 更新日志](https://www.workbuddy.cn/docs/workbuddy/Changelog) / App 内"关于"页 |

> **教程基线与上游当前版本的关系**：本轮在 2026-09-13 至 2026-09-14 对照官方记录修订四条产品线，并把 Claude Code 补到 v2.1.270。这里是核查时的快照，不代表实时版本。使用前先看本机 `claude --version` / `codex --version` / `openclaw --version`；WorkBuddy 看侧栏版本号或 App「关于」页，再按官方 changelog 对照差异。

### 本轮版本差异速览（2026-09-14 复核）

这一轮把四条线都从旧基线拉到了上游当前版本。下表第二列是上游改了什么，第三列是教程里已经落到哪些章节。

| 产品 | 从旧基线到当前基线 | 教程章节的跟进状态 |
|------|------------------|--------------|
| Claude Code v2.1.222 → v2.1.270 | 模型切换 hooks、`/diff` 全屏侧栏、`/skill-doctor`、`/output-style`、`/advisor` 文本形式、`/effort` 选择器的会话级 `s`；`keybindingFlavor` 不再生效，默认词编辑改为 Bash 风格；补回中间版本的默认模型变量、fork 行为、受限模式与插件入口；v2.1.270 修复只读 Git 命令误请求权限 | 14 个文件的基线统一到 v2.1.270；修正 Hooks 决策与配置、MCP 新旧协议协商、成本上限、云供应商 `/loop` 行为，并补齐插件诊断与评测入口 |
| ~~Claude Code v2.1.181 → v2.1.222（上一轮）~~ | **Sonnet 5 成默认**（v2.1.197，1M 上下文）、**Opus 5 成默认**（v2.1.219）、"Default" 权限模式改名 **"Manual"**（v2.1.200）、**ultraplan 移除**（v2.1.222）、subagent 默认后台 + 嵌套深度 3、新 `/doctor` / `/commit-push-pr` / `/fork` / `/code-review`、性能 79× transcript 缩小 / 7× 工具回合提速（v2.1.208）、Remote Control 不再允许仓库级开启、新 hooks（DirectoryAdded / EndConversation / Notification）、OTel `OTEL_LOG_USER_PROMPTS=1` 现也记录响应文本 | 已跟进到 v2.1.222：02 基础使用（权限模式重命名）、03 Commands（新命令 + ultraplan 移除）、12 Remote Control（仓库级禁用）；06 Subagents 跟进到 v2.1.219（后台默认 + 嵌套 3）。**仍停留在 v2.1.181**：01 安装、04 MCP、05 Hooks、07 Skills、08 Plugins、09 Agent SDK、10 综合实战、11 企业实战、快速导航卡 |
| OpenClaw v2026.7.1-2 → v2026.9.4 | 新安装流程、模型与个人技能库、统一 Plugins 工作区、公开只读分享与只读配置；升级回滚受数据库结构、旧包兼容性及配置检查约束。Docker 镜像固定标签不带 `v`，备份需读取实际卷名 | 12 篇的基线与关键变化已更新；02 / 09 / 10 / 11 补充备份、受控降级、Docker 卷名和空卷恢复说明 |
| ~~OpenClaw v2026.6.8 → v2026.7.1-2（上一轮）~~ | **新模型与提供商**（Claude Sonnet 5 / Mythos 5、Featherless、ClawRouter；GPT-5.6 成为新装默认）、**Control UI 与原生 macOS 聊天重做**（会话优先、可搜索侧栏、reasoning 滑杆）、**对话式 onboarding**（Crestodian 真跑 agent loop）、**移动端离线与语音**（iOS/Android 预渲染缓存、Apple Watch 完整语音、iOS 朗读回复）、会话分组与自动标题、Telegram 与 Codex 连续性（私聊 `/login`、`/steer` 与 `/tell`）、**启动与升级恢复**（容器迁移先于 readiness、可恢复的旧 state 不再阻塞启动、反复非正常启动后进入 control-plane-safe 模式）；v2026.7.1-1 修复 Memory Core 启动冲突导致的 fatal restart loop、Codex progress replies 中途停、WSL state permissions；v2026.7.1-2 修复 npm 插件更新的 singleton-array metadata | 已跟进到 v2026.7.1-2：07 记忆系统。**仍停留在 v2026.6.8 及更早**：02 安装部署、03 快速开始、05 消息平台、06 技能系统、08 多 Agent、09 Docker、10 安全、11 FAQ |
| Codex App 26.727 → 26.908 | **Pets 悬浮控件**（快速对话，`@` 带上下文、`$` 选 skill）、Windows 同时按下两个 Alt 键截 Appshot、Sources 面板直接打开文件、Codex Micro 插入文本、宠物恢复默认尺寸与听写遵循主语言、浏览器标签稳定性 | 已跟进：CX-01 安装认证、CX-02 桌面工作流补了 26.908 基线段；CX-03 / CX-14 已于 2026-09-14 对照当前官方文档复核：补齐命令分组、Goal 控制、正式导入流程，以及桌面审查 / worktree / 云端边界 |
| ~~Codex App 26.609 → 26.727（上一轮）~~ | **Codex 并入 ChatGPT 桌面 App**（26.707，可设为默认视图）、**PR Chat**（在 ChatGPT 桌面内审 PR）、**多仓库 diff 审查**（26.727）、本地项目多文件夹（26.715）、Activity view（26.727）、Chrome 扩展（提及打开标签页 / 高亮文本）、Markdown 行内编辑、内置浏览器更智能 | 已跟进到 26.727：CX-01 安装认证。**仍停留在 26.609**：CX-02 桌面工作流、CX-03 Commands、CX-04 项目指令、CX-13 安全企业、CX-14 对比。CX-10 Review/PR 与 CX-11 Web/Cloud 未标注 App 版本 |
| Codex CLI 0.146.1 → 0.154.0 | 已核实 0.147.0–0.152.1 正式版本；补任务导出与接续、异步及 MCP Hooks、Interrupt、MCP 启动等待与单工具输出预算；`update_plan` 默认关闭与 `/plan` 模式分开说明。保留 `codex mcp-server` 移除、Guardian 与实验性 worktree 的升级提示 | CX-04 / 05 / 07 / 08 / 12 已补中间版本，纠正插件 `add` 子命令、连接应用账号的审批隔离和子代理工作区边界；CX-13 保留旧 MCP server 脚本迁移提醒 |
| ~~Codex CLI 0.141.0 → 0.146.1（上一轮）~~ | **GPT-5.6 Sol/Terra/Luna 全系**（272K 上下文）、**多 Agent V2 稳定**（可配置 subagent 模型/推理等级/并发）、`/import` 扩展到 **Claude Code + Cursor**、`/new` + `/clear` 命名/置顶线程、线程分叉、**远程插件默认开**（npm marketplace）、**MCP 交互式认证默认**（非实验）、新 `writes` 审批模式、Agent Plugins manifest + workspace 发布、新市场 Amazon Bedrock + Claude Code、系统代理 PAC/WPAD、企业 in-app 更新管控 | 已跟进到 0.146.1：CX-01。CX-08 Subagents 跟进到 0.145.0（多 Agent V2）。**仍停留在 0.141.0**：CX-04 项目指令、CX-12 CLI 辅助、CX-13 安全企业。CX-05 MCP、CX-06 Skills、CX-07 Plugins 未标注 CLI 版本 |
| WorkBuddy 2026.08 → 客户端 5.5.6 | 「自动化」更名「定时任务」、「订阅和用量」入口、四档个人价格、资料库引用、行业 Buddy、Worktree、Office 预览上限与锁屏三档 | WB-00～WB-10 保留主体更新；WB-03 补行业 Buddy 跟练，WB-09 补 Agent / Plan / 仅问答与完整 Worktree 练习；WB-07 定时巡检、WB-08 锁屏前提、WB-10 价格资格与活动窗口的修订继续保留 |

> 表里带删除线的行是上一轮（v5.0，2026-08-06）的历史记录，其中「仍停留在」描述当时的状态。当前跟进范围看本轮对应行；各章带日期的历史说明保留用于版本比较。
>
> 本轮既更新版本说明，也修订会影响实操的命令、Hook JSON、MCP 协议流程、Docker 备份与恢复、定时任务和价格条件。章节中原有的功能引入版本保留，不把所有历史版本号替换成新基线。

> ⚠️ **版本号会随上游更新而失效**。教程中标注的版本号是编写/验证时的快照，不代表实时最新。遇到界面、命令或参数不一致时，优先查 App 更新日志、官方文档和 CLI 帮助（`--help`）。

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

- 本轮（核查日：2026-09-14）四条线的教程基线：Claude Code **v2.1.270**；OpenClaw **v2026.9.4**；Codex **App 26.908 / CLI 0.154.0**，CLI 仍为辅助路径；WorkBuddy **5.5.6**。价格和活动条件按 WorkBuddy 国内官方定价页核对，使用或采购前仍需对照本机与官网显示。
- **预发布与 `latest` 以各项目 [Releases](https://github.com/openclaw/openclaw/releases) 与本机版本为准**（持续更新中）
- 部分功能可能随版本更新而变化，请以官方文档为准
- 本教程是学习和实践参考，重要项目请先在测试仓库 / 测试环境验证，再进入生产流程

---

<div align="center">
  <p>⭐ 如果这个教程对你有帮助，欢迎 Star 支持！</p>
  <p>也欢迎把它转给正在学习 AI 编程和 Agent 工作流的朋友。</p>
</div>
