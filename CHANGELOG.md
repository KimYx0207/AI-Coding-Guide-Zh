# 更新日志（Changelog）

本项目所有重要变更均记录在此文件中。

---

## [v2.1.136] - 2026-05-25

### 修改

- 全库版本基线同步至 Claude Code v2.1.150、OpenClaw 稳定版 v2026.5.22、Codex CLI v0.133.0 / Codex App 26.519
- README 与三条教程线补充官方图片资源，并在正文关键章节插入场景图，不再只在文档顶部展示图片
- Claude Code 教程补充 v2.1.134→v2.1.150 差量：
  - 新增 Agent View（`claude agents`）、`/goal` 长目标、`/scroll-speed`、`/resume` 后台会话、`claude agents --json`、后台会话固定、后台子代理完成耗时、转录视图快捷导航等工作流内容
  - 同步 `/simplify` 改名为 `/code-review`，并补充 effort 参数、PR inline comment、旧清理行为移除等说明
  - 同步 `/usage` 分类用量、`/diff` 键盘滚动、GFM task list 渲染、`/plugin` 组件清单 / token cost / 最近更新时间 / LSP server 展示等 CLI 体验变化
  - 补充 Hooks、MCP、Plugins、企业治理和权限相关变化：`terminalSequence`、hook `args` exec form、`continueOnBlock`、`CLAUDE_PROJECT_DIR`、`allowAllClaudeAiMcps`、`settings.autoMode.hard_deny`、`ANTHROPIC_WORKSPACE_ID`、`forceLoginOrgUUID` / `forceLoginMethod` enforcement 等
  - 修订 Windows / PowerShell / worktree / sandbox / auto-updater 相关注意事项，包括 PowerShell 权限绕过修复、worktree 写入白名单收窄、PowerShell prefix allow 规则、Windows Terminal 显示和 paste 问题、`pwsh` 安装路径兼容等
- OpenClaw 教程补充 v2026.4.24→稳定版 v2026.5.22 差量：
  - 同步 Node.js 24 推荐、Node.js 22.19+ 兼容、Pi 0.75.1、Codex harness `@openai/codex` 0.132.0、macOS Peekaboo Bridge 3.2.1 等运行基线
  - 同步 Gateway / 性能 / 启动路径变化：通道目录和插件元数据缓存、startup-idle plugin lazy-load、ACPX runtime 延迟加载、Gateway ready 信号优化、restart trace 诊断等
  - 补充消息平台与语音能力：Discord voice 跟随用户进入语音频道、bounded profile context、会议记录插件、Telegram wildcard topic defaults、Slack / Telegram ack reactions、Feishu dynamic agents 等
  - 补充技能、插件、浏览器、媒体和模型变化：`openclaw skills install/update --global`、Policy plugin、Upstash Box、media provider credential 说明、Gemini CLI / Antigravity media guidance、xAI device-code OAuth、OpenRouter provider routing 等
  - 修订安全与配置口径：旧 `cat SKILL.md && printf ...` allowlist 兼容路径移除、SecretRef 和 plaintext secret 警告、trusted-proxy scope、Gateway BYOH IPv4 binding、agent subagent bootstrap 默认只带 `AGENTS.md` / `TOOLS.md` 等
- Codex 教程补充 CLI v0.129.0→v0.133.0 / Codex App 26.519 差量：
  - 同步 v0.131.0 的 TUI session controls、`@` mentions 统一搜索、marketplace / plugin 分享流程、remote-control daemon、Python SDK `openai-codex` / `openai_codex`、`codex doctor`、Windows sandbox 加固等
  - 同步 v0.132.0 的 Python SDK 认证、text-only turn API、`codex exec resume --output-schema`、remote executor 标准认证、图片 fidelity 保留、goal continuation 限制、session picker 和 remote websocket 修复等
  - 同步 v0.133.0 的 Goals 默认启用、dedicated storage、`codex remote-control` 前台化、permission profiles 列表 API / 继承 / managed `requirements.toml` / runtime refresh / Windows sandbox 集成、插件发现输出和 extension lifecycle events
  - 更新 `/plan`、`/goal`、CLI 安装、App server / API 文档、安全企业章节和 AGENTS 指令加载可靠性说明；明确 0.134.0-alpha.3 为预发布，不作为教程稳定基线

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

- OpenClaw 全套文档重写 — 技术错误修复 + 小白友好化改造
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

- **双顶流合璧 — Claude Code x OpenClaw 中文教程** 发布
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
