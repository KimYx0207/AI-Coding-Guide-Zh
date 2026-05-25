# CX-07 Plugins / Connectors 完整指南：App 能力扩展与账号连接


主要来源：OpenAI Codex App Features、Plugins、Apps / Connectors、MCP、Skills 官方文档。

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
> - **信息来源**：OpenAI Codex App Features、Plugins、Apps/Connectors、MCP、Skills 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-in-app-browser.webp" alt="Codex App 官方内置浏览器与页面反馈界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **区分四个核心概念**：清楚Connector、Plugin、Skill、MCP各自是什么、不是什么
2. **理解连接器工作流**：掌握安装→授权→引用→执行→验收的完整流程
3. **安装前安全检查**：知道看来源、能力、权限、数据范围、撤销方式
4. **掌握GitHub连接器**：完成GitHub连接器的最小可用流程（只读→只读总结→控制写权限）
5. **理解Plugin的能力包结构**：知道Plugin可以包含Skills、MCP、Connectors和配置
6. **遵循最小权限原则**：只给必要权限、不再使用及时禁用
7. **验收连接器和插件**：App可见、权限清楚、只读试跑、写操作可控、可撤销
8. **避免常见连接错误**：不混淆概念、不忽略MCP、不给过大权限

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想快速连接GitHub到Codex App

**只看这些章节**：

```
✅ 第1部分：先分清四个概念（3分钟）
✅ 第2部分：App中的连接器工作流（5分钟）
✅ 第6部分：GitHub连接器的最小可用流程（7分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握所有连接器和插件用法

**学习顺序**：从头到尾所有章节

---

## 1. 先分清四个概念

| 概念 | 本质 | 例子 | App 用户怎么理解 |
|---|---|---|---|
| Connector / App | 外部账号连接 | GitHub、Gmail、Drive、Slack | 把外部上下文带进 App |
| Plugin | 能力包 | 一组 skills、MCP、apps、配置 | 安装后扩展 App 能力 |
| Skill | 可复用工作流 | 代码审查 SOP | 教 Codex 怎么做 |
| MCP | 工具协议 | 浏览器、数据库、文档源 | 给 Codex 一双外部工具手 |

不要把它们混成一个词。插件可以包含 Skills、MCP、Apps，但不等于其中任何一个。

## 2. App 中的连接器工作流

典型流程：

1. 打开 App 的 Plugins / Connectors / Apps 入口。
2. 选择要连接的服务。
3. 完成账号授权。
4. 回到线程，用 `@`、mention、按钮或自然语言引用外部上下文。
5. 让 Codex 基于这些上下文执行任务。

示例：

```text
读取这个 GitHub issue 和当前仓库代码，判断问题是否已经被修复。只读，不修改文件。
```

## 3. 安装或连接前的检查

在 App 里点安装或授权前，先看清楚：

| 检查项 | 要确认什么 |
|---|---|
| 来源 | 是官方插件、组织内插件，还是第三方插件 |
| 能力 | 带 Skills、MCP、Connectors、配置还是组合包 |
| 权限 | 只读、评论、写文件、创建 PR、发消息分别需要什么权限 |
| 数据范围 | 能访问哪些仓库、文档、邮箱、群聊或日历 |
| 撤销方式 | 在 App、服务后台或组织管理端哪里撤销 |

安装和授权是两件事。插件装上后，不代表它已经可以访问你的 GitHub、Drive、Slack 或邮箱。

## 4. 常见连接场景

| 场景 | 连接器价值 | 风险点 |
|---|---|---|
| GitHub | 读取 issue、PR、仓库上下文 | 写权限、PR 评论权限 |
| Google Drive / Docs | 读取团队文档 | 文档访问范围 |
| Gmail / Outlook | 引用邮件上下文 | 隐私和敏感信息 |
| Slack / Teams | 查讨论和决策 | 群聊范围和成员隐私 |
| Calendar | 查日程和会议背景 | 个人隐私 |

连接器不是“装了就能看所有内容”。具体可见范围取决于账号授权、组织策略和连接器权限。

## 5. Plugin 在 App 中怎么用

插件常见用途：

- 带来一组 Skills。
- 带来 MCP server。
- 带来外部 App / Connector。
- 提供项目模板或规则。
- 提供特定平台的部署、监控、开发流程。

安装后要检查：

- 插件说明。
- 它带了哪些 Skills。
- 它是否要求外部账号授权。
- 它是否带 MCP server。
- 它是否会运行本地命令。
- 它是否有禁用或卸载入口。

## 6. GitHub 连接器的最小可用流程

GitHub 是最常见的 App 连接场景。建议按这个顺序验证：

1. 在 App 的 Connectors / Apps / Plugins 入口找到 GitHub。
2. 完成账号授权。
3. 确认授权范围：只读仓库、issue、PR，还是包含写权限。
4. 回到项目线程，引用一个 issue 或 PR。
5. 先让 Codex 只读总结上下文。
6. 再决定是否允许评论、创建分支、提交或更新 PR。

示例：

```text
读取这个 PR 的描述、评论和当前本地 diff，判断是否还有未处理 review 意见。只读，不评论、不修改文件。
```

## 7. 最小权限原则

插件和连接器都要按最小权限使用：

| 动作 | 建议 |
|---|---|
| 第一次安装 | 只给必要权限 |
| 只读任务 | 不给写权限 |
| 需要发消息 / 改 PR | 明确说明目标和范围 |
| 团队插件 | 先在测试项目验证 |
| 不再使用 | 及时禁用或卸载 |

不要让 Codex “随便查一下所有邮件 / 所有文档 / 所有群聊”。

## 8. CLI 作为辅助

App 是主线。CLI 只在这些情况使用：

```bash
codex plugin --help
codex plugin list
codex plugin marketplace --help
```

适合：

- 排查插件是否安装。
- 自动化团队安装流程。
- 查看低层配置。

不适合：

- 作为普通用户的第一入口。
- 替代 App 内授权和权限确认。

## 9. Plugin、MCP、Skill 的组合例子

一个 GitHub 工作流插件可能包含：

```text
Plugin
  Apps / Connector: GitHub
  Skills: issue-triage, pr-review
  MCP: GitHub tool server
  Config: allowed repository patterns
```

App 用户关心的是“我能完成什么工作流”，而不是先背内部结构。

## 10. 验收清单

连接器或插件启用后，检查：

| 验收项 | 通过标准 |
|---|---|
| App 可见 | 线程里能看到对应 App / Plugin / Skill / Tool |
| 权限清楚 | 知道它能读什么、写什么 |
| 只读试跑 | 能基于外部上下文做只读摘要 |
| 写操作可控 | 评论、提交、发消息前需要明确指令或审批 |
| 可撤销 | 知道在哪里断开连接或卸载 |

## 11. 常见错误

| 错误 | 正确做法 |
|---|---|
| 以为安装插件自动授权 | 安装和授权分开看 |
| 把 Figma / GitHub 等统称为 Skill | 它们可能是 App、MCP、Plugin 或 Skill |
| 忽略插件带来的 MCP | 安装后检查工具列表 |
| 给插件过大权限 | 最小权限授权 |
| 不知道怎么撤销 | 学会禁用、卸载、撤销授权 |

## 常见问题

### Q1：插件和连接器哪个优先？

如果只是连接一个外部服务，优先看 Connector / App。若需要一整套工作流、工具和技能，再看 Plugin。

### Q2：插件会不会自动访问我的数据？

不应这样理解。访问外部数据通常还需要授权，具体范围取决于连接器和组织设置。

### Q3：Plugin 能带 Skill 吗？

可以。插件是能力包，Skill 是其中一种能力。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 能区分Connector、Plugin、Skill、MCP四个概念
- [ ] 安装前检查了来源、能力、权限、数据范围、撤销方式
- [ ] 完成过GitHub连接器的只读试跑
- [ ] 遵循最小权限原则（只给必要权限）
- [ ] 知道如何在App中禁用/卸载连接器或插件
- [ ] 理解Plugin可以包含Skills、MCP、Connectors

**如果以上全部勾选，恭喜你掌握Codex连接器与插件！**

---

## 附录

### A. 概念速查

| 概念 | 本质 | 例子 |
|------|------|------|
| Connector / App | 外部账号连接 | GitHub、Gmail、Drive、Slack |
| Plugin | 能力包 | 包含Skills、MCP、Apps、配置 |
| Skill | 可复用工作流 | 代码审查SOP |
| MCP | 工具协议 | 浏览器、数据库、文档源 |

### B. 安装前检查清单

| 检查项 | 要确认什么 |
|--------|-----------|
| 来源 | 官方/组织内/第三方？ |
| 能力 | 带Skills/MCP/Connectors？ |
| 权限 | 只读/写文件/发消息？ |
| 数据范围 | 能访问哪些数据？ |
| 撤销方式 | 在哪里断开/卸载？ |

### C. 推荐学习资源

- **Codex Plugins 官方文档**：https://developers.openai.com/codex/plugins
- **本系列上一篇**：[CX-06 Skills](./CX-06-Codex-Skills可复用工作流完整指南.md)
- **本系列下一篇**：[CX-08 Subagents 多Agent协作](./CX-08-Codex-Subagents多Agent协作完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-08 Subagents：App 中的多 Agent 协作](./CX-08-Codex-Subagents多Agent协作完整指南.md)。
