# 更新日志（Changelog）

本项目所有重要变更均记录在此文件中。

---

## [Unreleased] - 2026-08-06

### 修复

- 修复上一次"AI 腔清洗"过度编辑造成的 172 处病句：清洗把"X 不是 Y，而是 Z"句式中的"不是 Y"机械删除，留下缺谓语残句。本轮逐处精准补回对比连词，分布在 docs/claude-code/（7 篇 12 处）、docs/codex/（14 篇 113 处）、docs/openclaw/（10 篇 47 处）。不改动其他字，不恢复作者人设词，经 rg 反向扫描 + 抽样人审复核零残留。

### 修改

- 课程稳定基线刷新到 Claude Code v2.1.222（从 v2.1.181）、Codex App 26.727 + CLI 0.146.1（从 26.609 + 0.141.0）、OpenClaw v2026.7.1-2（从 v2026.6.8，预发布线推进到 v2026.7.2-beta.7）。README 徽章、版本表、差异速览、免责声明同步更新。
- Claude Code 课程按 v2.1.222 补关键变化：Sonnet 5 成默认（1M 上下文）、Opus 5 成默认、"Default" 权限模式改名 "Manual"（v2.1.200）、ultraplan 移除（v2.1.222）、subagent 默认后台 + 嵌套深度 3、新 `/doctor` / `/commit-push-pr` / `/fork` / `/code-review` 命令、性能 79× transcript 缩小 / 7× 工具回合提速（v2.1.208）、Remote Control 不再允许仓库级开启、新 hooks（DirectoryAdded / EndConversation / Notification）、OTel `OTEL_LOG_USER_PROMPTS=1` 行为变化。
- Codex 课程按 App 26.727 + CLI 0.146.1 补关键变化：Codex 并入 ChatGPT 桌面 App（26.707）、GPT-5.6 Sol/Terra/Luna 全系（272K 上下文）、PR Chat、多仓库 diff 审查、本地项目多文件夹、Activity view、Chrome 扩展、多 Agent V2 稳定、`/import` 从 Claude Code + Cursor 迁移、远程插件默认开、MCP 交互式认证默认、新 `writes` 审批模式、Agent Plugins manifest + 新市场（Amazon Bedrock + Claude Code）、系统代理 PAC/WPAD、企业 in-app 更新管控。
- OpenClaw 课程按 v2026.7.1-2 补关键变化：State safety & recovery（quarantine store、SQLite 崩溃可恢复快照、schema 升级拒丢数据）、durable channel delivery（Telegram/Slack 跨崩溃保消息）、session rewind and branching、interactive MCP Apps、structured agent questions、meeting plugins（Teams/Zoom）、Wear OS companion；修复 Memory Core 启动冲突 fatal restart loop、Codex progress replies 中途停。

---

## [v4.4] - 2026-06-18

### 修改

- 本轮把课程稳定基线更新到 Claude Code v2.1.181、OpenClaw v2026.6.8、Codex App 26.609 与 Codex CLI 0.141.0，并在 README 统一维护版本表和差异速览，避免每章重复堆同一批 release notes。
- Claude Code 课程补充 v2.1.169 -> v2.1.181 关键变化：`/config key=value`、`Tool(param:value)` 权限语法、嵌套 `.claude/skills` / agents / workflows 就近优先、subagent 多层委派、`enforceAvailableModels`、Remote Control presence file、Bun 1.4 与云盘写入修复。
- Codex 课程继续保持 App-first：按 App 26.609 补充 Developer mode / CDP 浏览器调试、composer `/init`、Migrate to Codex、Windows Computer Use per-app controls、Automations 审批模式继承，并把 CLI 0.139 -> 0.141 的 `/usage`、`/import`、`/delete`、远程执行与 PostToolUse blocking 收进 CX-12。
- OpenClaw 课程按 v2026.6.8 更新安装升级、模型/provider、搜索 opt-in、ClawHub pinned commit / policy checks、消息平台富文本、fail-closed 权限边界、SecretRef、agent run recovery、`/usage` 和 FAQ 排障口径。
- 内容组织原则：README 放总览，CHANGELOG 放完整变更，产品章节只放“会改变实操判断”的短更新卡；不复制整段发布记录到多个章节。

---

## [v4.3] - 2026-06-10

### 修改

- 完成一次面向读者的课程复核，继续以 Claude Code CLI、Codex App、OpenClaw 助手框架三条主线组织内容。
- OpenClaw 文档统一收敛模型、上下文窗口、价格和隐私表述：不再把具体模型名、固定窗口、固定价格或“全部本地”等说法写成默认结论，改为引导读者按当前模型目录、onboarding、provider 输出和部署方式确认。
- Codex 课程保持 App-first：项目指令、权限、Rules、Hooks、Review、Subagents、Automations 和 CLI 辅助章节按 App 工作流重新区分职责，减少与 Claude Code CLI 课程的语义重复。
- Claude Code 课程保持 CLI 主线，同时修正本地执行、模型上下文、企业受控 provider 和安全边界的表达。
- 清理多处重复命令块、示例配置和旧版说明，把完整命令留在主章节，辅助章节改为指向主章节，减少阅读负担。
- README 的公开表达改为更稳的课程说明：保留作者定位、学习路线和版本基线，弱化夸张营销词，让读者更容易判断自己该从哪里开始。
- 更新许可和来源说明，保留 MIT 协议下的版权、署名和原始仓库提示，方便引用、转载和二次分发时正确保留来源。

---

## [v4.2] - 2026-05-31

### 修改

- 全库稳定基线同步至 Claude Code v2.1.158、OpenClaw 稳定版 v2026.5.27、Codex App 26.527（Windows 包 26.527.3686.0）；OpenClaw v2026.5.28 beta / v2026.5.29-alpha.1 与 Codex CLI v0.136.0-alpha.1 仍按预发布处理，不作为教程默认基线
- README 重写项目定位、适用人群、学习路线和统计口径，统一表达为 39 篇完整教程 + 1 张速查卡、80 万+ Markdown 内容量、1500+ 实操示例和 250+ 问答条目；Codex 徽章、版本表和免责声明统一改为 App 主线
- Codex App 主线强化：CX-02 扩展为 App 桌面工作流主轴，补充 App 主控台认知、三条安全线、Local / Worktree / Cloud 选择表、任务模板、Review 逐项检查法、从零到 PR 实战和课程交叉验证口径
- Codex 专题继续补强：CX-03 增加 App 命令工作流配方与 `/review` 维度表；CX-09 增加 Automation 合格输出和失败收敛策略；CX-10 增加 Review 严重程度分级和提交前反向解释；CX-11 增加 App -> Cloud 交接包和 Cloud 回流风险表；CX-12 补充 CLI v0.134.0 -> v0.135.0 差量
- Codex 官方链接修正：将失效的 `/codex/review`、`/codex/automations`、`/codex/config` 口径改为当前可访问的 `/codex/app/review`、`/codex/app/automations`、`/codex/app/settings`、`/codex/cli/reference`
- Claude Code 教程补充 v2.1.134 -> v2.1.158 差量，覆盖 Opus 4.8、`/effort xhigh`、`/goal`、`/workflows`、Agent View、后台 shell 会话、`/reload-skills`、`disallowed-tools`、`MessageDisplay` hook、插件 marketplace、MCP 审批、auto mode、遥测和企业治理等内容
- OpenClaw 教程补充 v2026.4.24 -> v2026.5.27 差量，覆盖 Node.js 24 / 22.19+ 基线、Gateway ready 性能、Transcript 核心化、Control UI Activity、Talk / Discord voice、Meeting Notes、消息平台 durable delivery、模型目录、媒体处理、Docker runtime workspace templates 和安全边界
- 固化后续更新规则：版本迭代必须同时检查正文教程差量、README 版本表、文档头尾更新时间、官方链接和可复制命令，避免只改徽章或统计口径

---

## [v2.1.135] - 2026-05-10

### 修改

- 集中更新说明：README 和各教程不再维护独立更新日志、差量更新或版本基线块，统一以 `CHANGELOG.md` 作为唯一更新记录
- 清理 Claude Code、Codex、OpenClaw 教程中分散的版本更新附录、页脚版本历史和文首版本提示，减少多处说明漂移
- README 的更新日志区块改为“更新说明”入口，只保留当前项目介绍、目录和使用入口
- 合并 README 原有历史更新摘要：v4.1 全库审计与 v2.1.93→v2.1.133 内容增强、v4.0 Codex 系列新增、v3.x OpenClaw / Claude Code 同步修订、v2.0 Claude Code 2.1.52 适配、v1.0 初始发布记录

### 从 README 合并的历史摘要

- v4.1（2026-05-08）：完成全库审计与内容增强，修正 Codex 系列结构、Claude Code 权限配置路径、README 版本说明和第三方模型配置入口，并补充 Claude Code v2.1.93→v2.1.133 的 Monitor、Session Recap、Skills、Plugins、Hooks、MCP、Subagent、SDK、企业实战等变更
- v4.0（2026-05-07）：项目升级为 Claude Code、OpenClaw、Codex 三教程结构，新增 `docs/codex/` 系列，覆盖 Codex App 安装认证、桌面工作流、Commands、项目配置、MCP、Skills、Plugins、Subagents、Automations、Review / GitHub / PR、Web / Cloud / CLI 辅助、安全企业和 Claude Code 对比
- v3.3（2026-04-05）：OpenClaw README 徽章与统计表改为稳定版 v2026.3.28 口径，说明预发布与稳定版并存，并统一目录、贡献路线和版本基线表述
- v3.2（2026-04-05）：同步 Claude Code 安装、基础使用、MCP、Commands、Hooks、Subagents、Plugins、企业实战等章节，新增 Remote Control 与 Channels / 计划任务教程，修正 Hooks、Subagents、Plugins 和 OpenClaw 安装、模型、技能、FAQ 等章节口径
- v3.0（2026-02-25）：项目从 Claude Code 单教程扩展为 Claude Code 与 OpenClaw 双教程，新增 OpenClaw 阅读指南和 11 篇教程，重组 `docs/claude-code/` 与 `docs/openclaw/` 目录，并补充 Claude Code 权限、MCP、Agent SDK 等内容
- v2.0（2026-02-25）：适配 Claude Code 2.1.52，更新教程版本号、README 徽章、Hooks 工作树管理、`--worktree`、`/fast`、API 中转站配置，并修复旧版本标记和快速导航描述
- v1.0（2026-02-11）：发布 10 篇 Claude Code 初始教程，包含约 104,000 字内容、70+ 代码示例和 120 个 FAQ

---

## [v2.1.134] - 2026-05-10

### 修改

- Claude Code 02 基础使用：新增 `CLAUDE.md` 实操入口，并将模板调整为可验证、少改动、简单优先的项目协作规则
- Claude Code 03 Commands：将内置命令速查调整为练习后的参考内容，降低“命令解读表”阅读压力
- Codex CX-04：新增 `AGENTS.md` 实操入口，并补充参考来源与项目级协作规则模板
- OpenClaw 03 快速开始：强化“先跑通第一个对话”的实操目标，并将 Control UI 介绍后置
- OpenClaw 06 技能系统：新增低风险技能练习，帮助读者先看到技能对助手行为的影响
- 将多篇教程前置的差量更新 / 版本基线说明移动到文末附录，避免打断正文学习路径

---

## [v2.1.133] - 2026-05-08

### 变更

- **仓库更名为 `AI-Coding-Guide-Zh`**（原 `Claude-Code-x-OpenClaw-Guide-Zh`），更简洁、更包容
- 更新 README.md 所有仓库链接和徽章引用

### 新增

- **全库教程版本升级至 Claude Code v2.1.133**（从 v2.1.92/v2.1.119）
- **11 篇教程新增 v2.1.93→v2.1.133 功能内容**，覆盖以下重要变更：
  - effort 五级推理控制（新增 `xhigh`/`max`，Opus 4.7 推荐默认 `xhigh`）
  - MCP `alwaysLoad` 跳过 ToolSearch 懒加载
  - Hooks 接收 `effort.level` + `$CLAUDE_EFFORT` 环境变量
  - `PostToolUse` 可通过 `hookSpecificOutput.updatedToolOutput` 替换所有工具输出
  - `worktree.baseRef` 控制 worktree 分叉来源（`fresh`/`head`）
  - Monitor 后台监控工具
  - Session Recap（终端失焦后自动回顾）
  - 自定义主题（Plugin 声明 color palette）
  - `skillOverrides` 设置控制 Skill 可见性
  - `/skills` 搜索过滤、`/proactive` 命令（`/loop` 别名）
  - `parentSettingsBehavior` 企业托管设置合并策略
  - `claude project purge` 清理项目状态
  - `CLAUDE_CODE_SESSION_ID` / `CLAUDE_CODE_FORK_SUBAGENT` 环境变量
  - `--channels` 支持 Console auth 登录
  - Native binaries（CLI 迁移到原生二进制文件）
  - Opus 4.7 成为 Max/Team Premium 默认模型
- **新增 Codex 教程目录** `docs/codex/`，含 CX-11 对比指南

### 修改

- 01-安装指南：effort 说明更新为五级，模型名更新为 Opus 4.7
- 02-基础使用：新增 Monitor/Session Recap/自定义主题/Native binaries 章节
- 03-Commands：新增 v2.1.93→v2.1.133 命令增强，effort 五级对比
- 04-MCP：新增 `alwaysLoad` 配置说明，更新变更摘录至 v2.1.133
- 05-Hooks：更新变更摘录至 v2.1.133，修正 PostToolUse 输出机制说明
- 06-Subagent：新增 `worktree.baseRef`、`CLAUDE_CODE_FORK_SUBAGENT` 说明
- 07-Skills：新增 `skillOverrides` 和 `/skills` 搜索过滤
- 08-Plugins：新增自定义主题、`plugin prune`、`--plugin-url`、`.zip` 支持
- 09-SDK：新增 `CLAUDE_CODE_SESSION_ID`、`localSettings`、`mcp_authenticate`
- 11-企业实战：新增 `parentSettingsBehavior`、`claude project purge`、Bedrock service tier
- 12-Remote-Control：扩展 v2.1.121+ 和 v2.1.133 增强条目
- 13-Channels：更新 `--channels` 支持 Console auth
- README：版本徽章、功能描述、版本追踪表同步更新

---

## [v2.1.119] - 2026-04-26

### 新增

- **全库教程版本升级至 Claude Code v2.1.119 + OpenClaw v2026.4.24**
- 版本号、徽章、README 同步更新

---

## [v2.1.92] - 2026-04-29

### 修复

- 补齐 12/13 教程课程信息头（GitHub / 公众号 / X / 博客）
- 同步 Claude Code command 和 agent 文档
- 移除误提交的计划文件（findings.md、progress.md）

---

## [v2.1.78] - 2026-04-07

### 新增

- **新增 12-Remote Control 完整指南**
- **新增 13-Channels 与计划任务完整指南**
- 01-安装指南新增第 8.5 部分：模型配置完整章节（+379 行）
- 删除独立的 12-Claude-Code 模型配置完整指南.md（内容合并到安装指南）
- 同步更新快速导航卡：14 个教程 → 13 个，序号重排
- 对齐 Remote/Channels 教程序号与文件名（12/13）并修正全库链接

### 修复

- 教程版本对齐与口径修正
- 在输出格式代码块前添加空行，改进文档渲染

### 修改

- 更新配置文档：`allowedTools` 改为 `allow`

---

## [v2.1.69] - 2026-03-18

### 新增

- 补充 Claude Code v2.1.69→v2.1.78 新功能到全部教程
- 更新 README 和快速导航卡，同步 v2.1.78 新功能

---

## OpenClaw 重写 - 2026-02-26

### 新增

- OpenClaw 全套文档重写：修正技术口径，补足入门路径和排障说明
- 新增 06-Subagent 子代理教程 + 全站模型名更新

### 修复

- 全量审核修复 OpenClaw 教程 01-11 全部虚构配置
- 修正 OpenClaw 教程 10 处配置错误（验证 GitHub 源码）
- 修复 6 篇 OpenClaw 教程 28 处虚构配置 + GitHub 仓库名修正
- 安装指南新增 NPM 备选方案 + Windows PATH 详细排查
- 修正安装指南 Windows 路径 + Hooks 输出机制纠错

---

## 项目初始化 - 2026-02-25

### 新增

- **Claude Code x OpenClaw 中文教程** 发布，项目从单一工具教程扩展为双工具学习路径
- 初始化 Claude Code 中文教程项目
- 新增 Git Worktree 内置并行任务隔离功能文档
- 全面迭代教程适配 Claude Code v2.1.45
- 清除全部待办项 — Task/Subagent、权限系统、新 MCP 服务

### 修复

- 重写 07-Plugins 教程 — 清除 60+ 处虚假 CLI 命令
- 全面体检修复 — 7 个 CRITICAL + 5 个 WARNING
- 二次验证修复 5 篇文档 16 处确认错误
- 修复 03-Commands 指南嵌套代码块渲染问题
- 移除 02-基础使用指南中 `#` 前缀的错误描述

---

> 格式参考：基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)
