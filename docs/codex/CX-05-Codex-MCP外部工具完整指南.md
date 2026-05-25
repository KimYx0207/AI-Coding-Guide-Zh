# CX-05 MCP 完整指南：在 App 中连接外部工具


本篇只讲 MCP 外部工具连接。Subagents 已单独拆到 CX-08。

主要来源：OpenAI Codex MCP 官方文档、Codex App Settings、Codex CLI MCP 命令。

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
> - **信息来源**：OpenAI Codex MCP 官方文档、Codex App Settings、Codex CLI MCP 命令
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)、[CX-04 权限配置](./CX-04-Codex项目指令权限配置完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-in-app-browser.webp" alt="Codex App 官方内置浏览器与页面反馈界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **理解MCP的本质**：掌握MCP是工具连接层，不是提示词，不是搜索
2. **确认MCP工具可用**：通过`/mcp`和App Settings验证工具是否加载
3. **区分MCP与其他能力**：清楚MCP、Plugins、Connectors、Skills各自的边界
4. **管理MCP权限**：给MCP工具设置最小读写权限，保护生产数据
5. **理解MCP与数据库交互**：默认只读，不给生产写权限
6. **学会用CLI辅助排查**：知道什么时候用CLI管理MCP配置
7. **验收MCP配置**：配置完成后能确认工具可见、权限正确、可审计、可撤销
8. **避免MCP常见错误**：不假设自动可用、不写API Key进配置

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 10分钟）

**适合人群**：想快速确认MCP能不能用

**只看这些章节**：

```
✅ 第1部分：MCP是什么（2分钟）
✅ 第2部分：App中的MCP工作流（5分钟）
✅ 第9部分：验收清单（3分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握MCP配置和使用

**学习顺序**：从头到尾所有章节

---

## 1. MCP 是什么

MCP 是 Model Context Protocol。它让 Codex 通过标准协议连接外部工具，例如：

- 浏览器自动化。
- 数据库查询。
- 内部 API。
- 文档系统。
- 设计工具。
- GitHub / issue / PR 工具。

一句话：MCP 不是提示词，而是工具连接层。

## 2. App 中的 MCP 工作流

App 主线应该这样学：

1. 在 App Settings 或集成入口启用 / 配置 MCP。
2. 回到线程。
3. 用 `/mcp` 查看当前可见工具。
4. 用自然语言要求 Codex 使用工具。
5. 观察工具调用和权限提示。
6. Review 结果。

示例：

```text
使用当前可用的文档 MCP，核对 README 里的安装步骤是否和官方文档一致。只读，不修改文件。
```

## 3. 从 0 配一个 MCP 前先确认什么

不要一上来复制一段 MCP 配置。先确认四件事：

| 问题 | 为什么重要 |
|---|---|
| 这个工具是本地命令还是远程服务？ | 决定是 stdio、HTTP 还是插件/连接器提供 |
| 需要什么账号或 token？ | 决定密钥放哪里，不能写进仓库 |
| 它默认能读写什么？ | 决定是否只读、是否需要审批 |
| App 里是否已经有连接器或插件？ | 有现成入口时不要重复手写 MCP |

App 里已经能通过 Connector / Plugin 完成的事情，优先用 App 入口。MCP 更适合“需要把一个具体工具暴露给 Codex 调用”的场景。

## 4. App 用户常见场景

| 场景 | MCP 怎么帮忙 | 注意事项 |
|---|---|---|
| 查官方文档 | 连接文档搜索工具 | 优先一手来源 |
| 查数据库 | 只读查询 schema / 样例数据 | 不要给生产写权限 |
| 浏览器验证 | 打开本地页面，点按钮，截图 | 需要明确目标 URL |
| 设计稿核对 | 读取 Figma 等设计上下文 | 注意账号授权 |
| 内部 API | 调用公司内部服务 | 最小权限和审计 |

## 5. CLI 管理 MCP 是辅助路径

当 App 里看不到 MCP，或团队要统一配置时，才用 CLI：

```bash
codex mcp --help
codex mcp list
codex mcp add <name> -- <command>
```

也可以在 `config.toml` 中写 MCP server。具体字段以官方 Config Reference 为准。

CLI 配好后回到 App 仍要验收：

1. 重启或刷新 Codex App。
2. 打开项目线程。
3. 输入 `/mcp`。
4. 确认 server 名称、工具列表、连接状态。
5. 用一个只读任务试跑。

不要把“CLI 显示配置存在”当成“App 已经能用”。最终以 App 线程里能看到并成功调用为准。

## 6. MCP Server 类型

常见类型：

| 类型 | 说明 |
|---|---|
| stdio | 本地命令启动，适合本机工具 |
| HTTP / SSE | 远程服务，适合团队或云服务 |
| 插件携带 | Plugin 安装后提供 MCP server |

App 用户重点不是背协议，而是知道工具从哪里来、权限是什么、结果能否验证。

## 7. MCP、Plugins、Connectors、Skills 的区别

| 能力 | 本质 | 例子 |
|---|---|---|
| MCP | 工具协议 | 浏览器、数据库、文档搜索 |
| Plugin | 能力包 | 打包 skills、MCP、apps、配置 |
| Connector / App | 外部账号连接 | GitHub、Gmail、Drive、Slack |
| Skill | 可复用工作流 | 审查 SOP、发布检查 |

不要把 MCP 当万能插件系统。如果只是写固定流程，用 Skill；如果要连接外部工具，用 MCP 或 Connector。

## 8. 安全边界

配置 MCP 前先问：

- 它能读什么数据？
- 它能写什么数据？
- 它是否会联网？
- 它是否需要账号授权？
- 它是否会把数据发给第三方？
- 它能不能在只读模式下完成任务？

生产数据库、客户数据、内部文档、邮箱、云盘都要按最小权限配置。

## 9. 验收清单

一个 MCP 配置写完后，必须过这张表：

| 验收项 | 通过标准 |
|---|---|
| App 可见 | `/mcp` 能看到 server 和工具 |
| 最小权限 | 只给当前任务需要的读写范围 |
| 密钥安全 | token 在环境变量、secret 或系统凭据里，不在仓库 |
| 只读试跑 | 能完成一个只读查询或读取任务 |
| 可审计 | 工具调用结果能回到线程中被 Review |
| 可撤销 | 知道如何禁用 server、撤销 token 或卸载插件 |

## 10. 常见错误

| 错误 | 正确做法 |
|---|---|
| 以为 MCP 自动可用 | 用 `/mcp` 或 App 设置确认 |
| 把 MCP 配置写进教程后不验证 | 以当前 CLI / App 输出为准 |
| 给数据库写权限 | 默认只读 |
| 让 Codex “随便查” | 明确目标和范围 |
| 把 API Key 写进 config 示例 | 使用环境变量或 secret |

## 常见问题

### Q1：App 里一定能管理所有 MCP 吗？

不一定。部分配置可能需要 CLI 或 `config.toml`。但 App 仍是使用主线。

### Q2：MCP 工具会不会自动运行？

Codex 会根据任务调用工具，但是否需要审批取决于工具、权限和设置。

### Q3：MCP 和 Web search 一样吗？

不一样。Web search 是搜索网页；MCP 是连接具体工具或服务。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解MCP是工具连接层，不是提示词也不是搜索
- [ ] 知道用`/mcp`或App Settings确认工具是否可用
- [ ] MCP工具只给了当前任务需要的最小权限
- [ ] 密钥/token存放在环境变量或系统凭据中，不在仓库里
- [ ] 完成过一个只读MCP查询任务
- [ ] 工具调用结果能在线程中被Review
- [ ] 知道如何禁用server、撤销token或卸载插件

**如果以上全部勾选，恭喜你掌握Codex MCP！**

---

## 附录

### A. MCP相关命令速查

| 命令 | 用途 |
|------|------|
| `/mcp` | 查看当前MCP server和工具 |
| `codex mcp list` | CLI中列出MCP工具 |
| `codex mcp --help` | CLI中查看MCP帮助 |

### B. MCP验收清单

| 验收项 | 通过标准 |
|--------|---------|
| App可见 | `/mcp`能看到server和工具 |
| 最小权限 | 只给当前任务需要的读写范围 |
| 密钥安全 | token在环境变量/secret中 |
| 只读试跑 | 能完成一个只读查询任务 |
| 可审计 | 工具调用结果回到线程 |
| 可撤销 | 知道如何禁用/卸载 |

### C. 推荐学习资源

- **Codex MCP 官方文档**：https://developers.openai.com/codex/mcp
- **本系列上一篇**：[CX-04 权限配置](./CX-04-Codex项目指令权限配置完整指南.md)
- **本系列下一篇**：[CX-06 Skills 可复用工作流](./CX-06-Codex-Skills可复用工作流完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-06 Skills：在 App 中调用和编写可复用工作流](./CX-06-Codex-Skills可复用工作流完整指南.md)。
