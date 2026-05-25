# CX-12 Codex CLI 辅助指南：App 用户什么时候需要终端

<p align="center"><img src="../../images/official/openai-codex-cli-splash.png" alt="OpenAI Codex 官方图" width="720"/></p>


主要来源：OpenAI Codex CLI、CLI Slash Commands、Config、MCP、Review 官方文档。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时
> - **难度等级**：⭐⭐ 入门级
> - **更新日期**：2026年5月
> - **信息来源**：OpenAI Codex CLI、CLI Slash Commands、Config、MCP、Review 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **理解CLI的定位**：CLI是App的辅助工具，不是普通用户的第一入口
2. **掌握CLI常用命令**：`codex --help`、`codex exec`、`codex review`、`codex mcp list`
3. **理解审批与沙盒参数**：`--ask-for-approval`和`--sandbox`的组合使用
4. **使用`codex exec`无头执行**：在CI和脚本中运行一次性只读任务
5. **使用`codex review`终端审查**：快速检查当前diff，与App Review交叉验证
6. **掌握CLI slash commands**：`/status`、`/permissions`、`/plan`、`/compact`等常用命令
7. **用CLI管理MCP和Plugins**：排查工具配置、统一团队安装
8. **理解CI安全原则**：最小权限、外部沙箱、不输出密钥、明确范围、人工合并

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 10分钟）

**适合人群**：想知道CLI能干什么

**只看这些章节**：

```
✅ 第1-2部分：CLI定位 + 常用命令（5分钟）
✅ 第4部分：codex exec（5分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：需要用CLI做CI或排查

**学习顺序**：从头到尾所有章节

---

## 1. CLI 的定位

> **v0.133.0 CLI 基线**：`codex remote-control` 前台化并报告 readiness；goals 默认启用；permission profiles 增加 list API、继承、managed `requirements.toml` 与 Windows sandbox 强化；plugin discovery 更容易检查；extension lifecycle 可观察 subagent start/stop、tool execution、turn metadata 和 async approval / turn processing。安装方式以官方 CLI 文档为准，不再只写 npm。

CLI 是 App 的辅助工具，适合：

- 排查配置。
- 管理 MCP。
- 在 CI 中无头执行。
- 终端中快速 review。
- 用脚本批处理。
- Linux 或远程服务器环境。

不适合：

- 作为普通 App 用户的第一入口。
- 替代 App Review 面板。
- 让新手先背所有参数。

## 2. 常用命令

```bash
codex --help
codex
codex app
codex exec "summarize this repo"
codex review
codex mcp list
codex plugin --help
codex features
```

App 用户学习 CLI 的顺序：

1. 先会用 `codex --help` 看本机支持项。
2. 再会用 `codex app` 从终端打开或配合 App。
3. 需要无头任务时再学 `codex exec`。
4. 需要审查时再学 `codex review`。
5. 需要排查外部工具时再学 `codex mcp` 和 plugin 命令。

不要先背参数表。CLI 版本变化快，本机 `--help` 比教程里的静态列表可靠。

## 3. 审批与沙盒

CLI 常见参数：

```bash
codex --ask-for-approval on-request --sandbox workspace-write
codex --ask-for-approval never --sandbox read-only
```

危险模式只用于外部已经隔离的一次性环境：

```bash
codex --dangerously-bypass-approvals-and-sandbox
```

不要把危险模式写成团队默认推荐。

如果你不知道该选什么，App 用户默认做法是：

| 场景 | 建议 |
|---|---|
| 只读分析 | read-only / 需要审批 |
| 小范围改 docs | workspace-write / 明确目录 |
| 跑测试 | 允许普通命令，危险命令仍审批 |
| CI runner | 只给 PR diff 或目标目录 |
| 一次性隔离环境 | 才考虑无审批无沙盒 |

## 4. `codex exec`

无头执行一次任务：

```bash
codex exec "read the repo and summarize test commands"
```

适合：

- CI。
- 脚本化只读分析。
- 生成报告。

不适合：

- 需要频繁交互的大改。

一个更清楚的无头任务示例：

```bash
codex exec "Read package.json and AGENTS.md. Report the install, test, lint, and build commands. Do not modify files."
```

## 5. `codex review`

终端审查当前改动：

```bash
codex review
```

适合：

- CI PR 审查。
- 本地提交前快速检查。
- 与 App Review 交叉验证。

## 6. CLI slash commands

终端交互模式中可以输入 `/help` 查看当前 slash commands。不要把命令表写死；以当前 CLI 为准。

App 用户重点掌握：

- `/status`
- `/permissions`
- `/plan`
- `/goal`
- `/review`
- `/mcp`
- `/plugins`
- `/compact`
- `/resume`

如果这些命令没有出现在你本机 `/help`，以本机输出为准，不要按教程硬敲。

## 7. CLI 管理 MCP / Plugins

当 App 中看不到工具或需要团队统一配置时：

```bash
codex mcp --help
codex plugin --help
```

CLI 是管理和排查路径，不是普通用户调用外部工具的唯一方式。

CLI 改完 MCP 或插件后，仍要回 App 验收：

1. App 里能否看到工具或插件。
2. 线程中能否调用。
3. 权限提示是否符合预期。
4. 是否能撤销或禁用。

## 8. CI 安全原则

| 原则 | 说明 |
|---|---|
| 最小权限 | CI token 只给需要的仓库权限 |
| 外部沙箱 | 无沙盒模式只在 runner 自身可信时使用 |
| 不输出密钥 | 日志中不得打印 secret |
| 明确范围 | 只审查 PR diff 或指定路径 |
| 人工合并 | 自动评论可以，自动合并要慎重 |

## 常见问题

### Q1：App 用户不装 CLI 可以吗？

可以，但排查和 CI 会不方便。建议安装，但不先学。

### Q2：CLI 和 App 的配置完全共享吗？

不要做绝对假设。看当前版本和官方文档。能通过 App 设置解决的，优先用 App。

### Q3：CLI 能替代 Automations 吗？

不能完全替代。CLI 适合脚本和 CI；App Automations 是 App 内的后台/周期任务体验。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解CLI是App的辅助，不是主线
- [ ] 掌握`codex exec`无头执行和`codex review`终端审查
- [ ] 知道审批和沙盒参数的组合使用
- [ ] 不把CLI教程写成Codex主线
- [ ] CI中遵循最小权限、不输出密钥、人工合并原则

**如果以上全部勾选，恭喜你掌握Codex CLI辅助！**

---

## 附录

### A. CLI命令速查

| 命令 | 用途 |
|------|------|
| `codex --help` | 查看帮助 |
| `codex` | 交互模式 |
| `codex app` | 打开或配合App |
| `codex exec "任务"` | 无头执行 |
| `codex review` | 审查当前改动 |
| `codex mcp list` | 列出MCP工具 |
| `codex plugin --help` | 插件管理帮助 |

### B. 推荐学习资源

- **Codex CLI 官方文档**：https://developers.openai.com/codex/cli
- **本系列上一篇**：[CX-11 Web / Cloud 辅助](./CX-11-Codex-Web-Cloud辅助指南.md)
- **本系列下一篇**：[CX-13 安全与企业](./CX-13-Codex安全企业完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-13 安全与企业基线](./CX-13-Codex安全企业完整指南.md)。
