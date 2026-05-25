# CX-02 Codex App 桌面工作流完整指南：把 App 当主控台


定位说明：本篇是整个 Codex 系列的主轴。后续 Commands、MCP、Skills、Plugins、Automations、Review、Cloud 都围绕这里展开。

主要来源：OpenAI Codex App Features、App Commands、Settings、Review、Automations、MCP、Skills、Plugins、CLI Slash Commands 官方文档。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：3-4小时
> - **难度等级**：⭐ 零基础入门
> - **更新日期**：2026年5月
> - **信息来源**：OpenAI Codex App Features、Settings、Review、Automations、MCP、Skills、Plugins 官方文档
> - **前置要求**：已完成 [CX-01 Codex App 安装与认证](./CX-01-Codex-App安装与认证完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-in-app-browser.webp" alt="Codex App 官方内置浏览器与页面反馈界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

完成本课学习后，你将能够：

1. **理解App的核心模型**：掌握Thread、Worktree、Review、Terminal、Settings等核心概念
2. **区分三种工作方式**：清楚Local thread、Worktree thread、Cloud handoff各自的适用场景
3. **写好任务描述**：用目标-范围-约束-验证-交付五要素模板描述任务
4. **掌握Review工作流**：在App中查看diff、审批命令、合并改动
5. **理解Settings配置**：知道模型、审批、沙盒、插件、MCP在App中的配置入口
6. **建立App全局视角**：知道Commands、MCP、Skills、Plugins、Automations在App中各自的位置和关系
7. **避免常见翻车场景**：不盲目给写权限、不跳过Review、不用Cloud替代本地App
8. **跑通完整的App改动流程**：从任务描述到diff检查到合并提交的全流程

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：这是一篇长教程，不用全看！

### 路径A：快速上手（⏱️ 20分钟）

**适合人群**：装好了App，想快速知道怎么用

**只看这些章节**（其他跳过）：

```
✅ 第1部分：App的核心模型（5分钟）
✅ 第2部分：三种工作方式（5分钟）
✅ 第3部分：任务描述模板（5分钟）
✅ 第6部分：Review工作流（5分钟）
```

**20分钟后你能达到**：能用App描述任务、看懂diff、做基本操作

---

### 路径B：完整学习（⏱️ 3-4小时）

**适合人群**：想系统掌握Codex App的全部工作流

**学习顺序**：从头到尾所有章节

---

### 路径C：问题排查（⏱️ 5分钟）

**适合人群**：使用App时遇到问题

**直接跳到**：

```
🔧 第10部分：常见错误
🔧 第11部分：常见问题FAQ
```

---

## 1. App 的核心模型

Codex App 可以理解为一个桌面开发主控台。它把这些能力放到同一个工作流里：

| 能力 | App 中的意义 |
|---|---|
| Thread | 一条任务线。每个线程都有上下文、历史和状态 |
| Local workspace | 直接围绕当前本地目录工作 |
| Worktree | 给任务创建隔离分支/目录，降低互相覆盖风险 |
| Review | 查看 diff、文件变更、行内反馈、stage / unstage |
| Terminal | 让 Codex 在受控环境中运行命令 |
| Settings | 模型、审批、沙盒、插件、MCP、外观、Git 等配置 |
| Automations | 周期性或后台检查任务 |
| Plugins / Connectors | 连接 GitHub、Gmail、Drive、Slack 等外部上下文 |

本系列后续功能都要回到这个模型里解释。

## 2. 三种工作方式

### 2.1 Local thread

适合小任务和只读任务：

```text
阅读这个项目并总结启动命令、测试命令、主要目录。不要修改文件。
```

优点：快，直接使用当前工作区。

风险：如果让 Codex 写文件，改动会进入当前工作区。学习阶段要盯住 Review 面板。

### 2.2 Worktree thread

适合功能开发、重构、风险较高的改动：

```text
在新的 worktree 里实现登录页移动端布局修复。改完运行相关测试，最后给我 diff 摘要。
```

优点：隔离改动，多个任务可以并行。

注意：worktree 仍然是真实 Git 工作区。合并前要 Review。

### 2.3 Cloud / Web handoff

适合云端仓库任务、长时间后台任务和 PR 工作流。App 是本地主控台，Cloud 是远程执行环境。不要把 Cloud 当成本地 App 的替代品。

## 3. App 任务描述模板

好任务要包含五件事：

```text
目标：修复用户资料页加载失败。
范围：只改 src/pages/profile.tsx 和 src/api/user.ts。
约束：不要改数据库 schema，不要引入新依赖。
验证：运行 npm test -- profile。
交付：展示 diff 摘要和测试结果，不要自动提交。
```

不要只写：

```text
帮我修一下。
```

因为 Codex 不知道范围、验证方式和停止条件。

## 4. App Review 工作流

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App Review 面板与 diff 实操界面" width="720"/></p>

每次 Codex 修改文件后，你都应该看 Review：

1. 看文件列表：确认只改了目标范围。
2. 看 diff：确认行为变化合理。
3. 看测试输出：确认验证真的跑过。
4. 行内指出问题：让 Codex 继续修。
5. 需要提交时再 stage / commit。

典型提示：

```text
Review 这次 diff。重点检查是否改了范围外文件、是否缺测试、是否引入兼容性风险。
```

## 5. App 中的 Commands

Commands 是 App 里最快的工作流入口。你可以在输入框里输入 `/` 查看当前可用命令。

常见类型：

| 类型 | 例子 | 用途 |
|---|---|---|
| 会话 | `/new`、`/resume`、`/compact` | 管理线程和上下文 |
| 状态 | `/status` | 查看模型、工作区、审批、上下文状态 |
| 工作流 | `/plan`、`/review` | 计划、审查 |
| 工具 | `/mcp`、Apps / Plugins 入口 | 外部能力入口 |
| 反馈 | `/feedback` | 向产品反馈问题 |

不同版本、实验开关和插件会改变命令列表。App 用户先输入 `/` 看当前列表；`/goal`、`/loop` 等长目标/循环入口如果当前 App 显示，再按 CX-03 的实验能力写法使用。完整讲解见 CX-03。

## 6. App 中的项目指令

`AGENTS.md` 是 Codex 理解项目规则的核心文件。它应该写：

- 项目是什么。
- 常用命令是什么。
- 代码风格和测试要求。
- 哪些文件不要动。
- 修改后如何验证。

不要把临时任务、密钥、个人路径写进去。详见 CX-04。

## 7. App 中的 MCP

MCP 是外部工具协议。App 通过 MCP 使用浏览器、数据库、文档源、内部系统等工具。

App 用户应该先理解：

- MCP 不是 prompt。
- MCP server 可能带权限和数据风险。
- 连接后要在 App 或 `/mcp` 中确认工具是否可用。
- CLI 管理 MCP 只是辅助，不是主线。

详见 CX-05。

## 8. App 中的 Skills

Skills 是可复用工作流。适合把“每次都要重复说的步骤”沉淀下来。

例如：

- 代码审查流程。
- 发布前检查。
- 文档核对流程。
- 特定团队的写作规范。

App 中可以通过自然语言或 `$skill-name` 点名触发。详见 CX-06。

## 9. App 中的 Plugins / Connectors

Plugins 是能力包，可能包含 Skills、MCP、Apps、配置等。Connectors 是连接外部服务的入口，例如 GitHub、Google Drive、Slack、Gmail 等。

App 用户要记住：

- 安装插件不等于自动授权所有外部数据。
- 连接器需要单独登录和授权。
- 外部服务权限要按最小范围配置。

详见 CX-07。

## 10. App 中的 Subagents

Subagents 适合并行分析、分工改代码、独立审查。不要滥用。

适合：

- 一个 agent 查 API 文档，一个 agent 看代码实现。
- 一个 agent 改前端，一个 agent 改测试。
- 一个 agent 做实现，一个 agent 做 review。

不适合：

- 单个错别字。
- 线性的一步任务。
- 你还没定义清楚范围的大任务。

详见 CX-08。

## 11. App 中的 Automations

Automations 用来让 Codex 周期性或后台执行任务：

- 每天检查测试是否失败。
- 每周总结依赖更新。
- 定期检查文档是否和代码漂移。
- 监控某个 PR 或部署状态。

创建自动化前要明确：

- 运行频率。
- 工作目录。
- 是否允许写文件。
- 找到问题后通知还是自动修。

详见 CX-09。

## 12. App 与 GitHub / PR

App 的 Git 工作流通常是：

1. Codex 修改本地文件。
2. 你在 Review 面板检查。
3. 运行测试。
4. stage / commit。
5. 推送分支。
6. 创建 PR。
7. 必要时交给 Cloud / Web 继续处理。

GitHub / PR 详见 CX-10。

## 13. App 用户什么时候看 CLI / Web

| 你要做什么 | 看哪里 |
|---|---|
| 只用桌面 App 开发 | CX-01 到 CX-10 |
| 排查 slash / MCP / config | CX-12 CLI |
| CI 或无头任务 | CX-12 CLI |
| 云端仓库任务 / 长跑 PR | CX-11 Web / Cloud |
| 内部平台接 Codex | SDK / App Server 官方文档 |

## 常见问题

### Q1：App 是不是只能聊天？

不是。App 是本地开发主控台，核心是线程、文件改动、Review、终端、插件、自动化。

### Q2：所有功能都要学吗？

不需要。先掌握 Thread、Review、Commands、AGENTS.md，再按需要学 MCP、Skills、Plugins、Automations。

### Q3：App 中看到的命令和 CLI 一样吗？

不一定。以当前 App 的 `/help`、命令补全和官方文档为准。CLI 能帮助核对，但不是 App 的替代品。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解Local thread、Worktree thread、Cloud handoff三种工作方式的区别
- [ ] 能用五要素模板（目标-范围-约束-验证-交付）描述任务
- [ ] 知道如何在App中查看diff和审批命令
- [ ] 理解Settings中模型、审批、沙盒等配置入口
- [ ] 知道Commands、MCP、Skills、Plugins、Automations在App中的位置
- [ ] 不跳过Review直接合并
- [ ] 陌生项目先用只读模式

**如果以上全部勾选，恭喜你掌握Codex App核心工作流！**

---

## 附录

### A. App核心概念速查

| 概念 | 一句话解释 |
|------|-----------|
| Thread | 一条任务线，包含上下文、历史和状态 |
| Local thread | 直接在当前工作区执行的任务线 |
| Worktree thread | 在隔离Git分支/目录中执行的任务线 |
| Cloud handoff | 将任务交给云端执行的接力模式 |
| Review面板 | 查看diff、文件变更、行内反馈的关口 |
| Settings | 模型、审批、沙盒、插件、MCP等配置入口 |

### B. 任务描述模板

```text
目标：[你要达到什么效果]
范围：[只改哪些文件/目录]
约束：[不能做什么]
验证：[怎么确认改对了]
交付：[期望的输出形式]
```

### C. 推荐学习资源

- **Codex App 官方文档**：https://developers.openai.com/codex
- **本系列上一篇**：[CX-01 Codex App 安装与认证](./CX-01-Codex-App安装与认证完整指南.md)
- **本系列下一篇**：[CX-03 Commands 工作流入口](./CX-03-Codex-Commands工作流入口完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-03 Commands：App 里的 slash commands 与工作流入口](./CX-03-Codex-Commands工作流入口完整指南.md)。
