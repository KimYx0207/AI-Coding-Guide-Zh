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
> - **更新日期**：2026年5月30日
> - **信息来源**：OpenAI Codex MCP 官方文档、Codex App Settings、Codex CLI MCP 命令
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)、[CX-04 权限配置](./CX-04-Codex项目指令权限配置完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **理解MCP的本质**：掌握MCP是工具连接层，不是提示词，不是搜索
2. **确认MCP工具可用**：通过`/mcp`和App Settings验证工具是否加载
3. **区分MCP与其他能力**：清楚MCP、Plugins、Connectors、Skills各自的边界
4. **管理MCP权限**：给MCP工具设置最小读写权限，保护生产数据
5. **理解MCP与数据库交互**：默认只读，不给生产写权限
6. **学会用CLI辅助排查**：知道什么时候用CLI管理MCP配置
7. **核对MCP配置**：配置完成后能确认工具可见、权限正确、可审计、可撤销
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
✅ 第9部分：配置核对（3分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握MCP配置和使用

**学习顺序**：从头到尾所有章节

---

## 术语表（小白必读）

MCP 章节最常见的误区是：把 MCP 当成“搜索”“插件”“账号连接”或“万能 API”。先把词拆开：

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| MCP | Model Context Protocol，让模型连接工具和上下文的协议 | 它是工具连接层，不是提示词 |
| MCP server | 暴露一组工具的服务 | 可能是本地命令，也可能是远程 HTTP |
| Tool | server 提供给 Codex 调用的具体动作 | 每个工具都要看读写权限 |
| STDIO server | 通过本地命令启动的 MCP server | 常见于本机工具、文档、浏览器 |
| Streamable HTTP server | 通过 URL 访问的远程 MCP server | 常见于团队服务和云工具 |
| OAuth / Bearer token | 远程 server 的授权方式 | token 不写进仓库 |
| Server instructions | server 初始化时给 Codex 的使用说明 | 适合写跨工具约束和速率限制 |
| Tool approval | MCP 工具调用时的审批行为 | 读写、高风险、外部副作用要区别看 |
| Connector / App | 外部账号连接 | GitHub、Drive、Slack 等账号上下文，不等于 MCP |
| Plugin-provided MCP | 插件打包提供的 MCP server | 安装插件后仍要核对工具和权限 |

一句话：MCP 给 Codex “手”，Connector 给 Codex “账号上下文”，Skill 教 Codex “怎么做”，Plugin 把这些能力打包。

## 0. MCP 的工作机制

我在 MCP 这一讲里坚持要求列来源，是因为老金不希望读者把模型记忆当成官方证据。

一次 MCP 调用可以理解为：

```text
你提出任务
  -> Codex 判断是否需要外部工具
  -> Codex 查看当前可用 MCP server 和工具说明
  -> 如需调用，按工具权限和 approval 设置发起调用
  -> MCP server 执行真实工具逻辑
  -> 结果回到线程，Codex 基于结果继续推理或写代码
```

这个流程里有三个关键点：

1. **工具是否可见**：配置存在不等于 App 当前线程已经能看到。
2. **工具是否合适**：能查数据库不代表应该查生产数据。
3. **结果是否可信**：MCP 返回的是外部工具结果，仍要看来源、时间、权限和副作用。

### 0.1 MCP 适合解决的问题

| 问题 | MCP 是否适合 | 原因 |
|---|---|---|
| 查最新官方文档 | 适合 | 文档 MCP 能提供比模型记忆更新的一手资料 |
| 读取浏览器页面状态 | 适合 | 浏览器 MCP 可以实际打开页面 |
| 查询数据库 schema | 适合，但默认只读 | 能看到真实结构，但数据风险高 |
| 执行公司内部 API | 适合，但要审计 | 需要权限、日志和最小范围 |
| 写一套固定代码审查流程 | 不优先 | 用 Skill 更合适 |
| 定时每天查一次 | MCP 不是调度器 | 用 Automation 调用 MCP / Skill |

### 0.2 MCP 配置不是最终目标

很多教程会把重点放在“怎么 add 一个 server”。但真正的学习目标应该是：你能判断这个 server 从哪里来、能做什么、能读写什么、失败时怎么排查、离职或不用时怎么撤销。

一条成熟 MCP 工作流应该包括：

```text
来源确认
  -> 权限评估
  -> 配置
  -> App 可见性核对
  -> 只读试跑
  -> 写操作边界
  -> 日志和撤销方式
```

## 1. MCP 是什么

MCP 是 Model Context Protocol。它让 Codex 借助标准协议连接外部工具，例如：

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

CLI 配好后回到 App 仍要核对：

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

### 6.1 三类 server 的配置差异

| 类型 | 常见配置 | 风险点 | 新手建议 |
|---|---|---|---|
| STDIO | `command`、`args`、`env`、`cwd` | 本地命令真实运行，依赖本机环境 | 先用只读文档或浏览器工具练 |
| Streamable HTTP | `url`、bearer token、OAuth、headers | 远程服务和 token 管理 | 只连可信服务，token 放环境变量 |
| Plugin-provided | 插件 manifest 提供 server | 插件来源、工具权限、更新变化 | 安装后先看 `/mcp` 和插件详情 |

配置里常见的安全字段包括：

- `enabled`：临时禁用 server，而不是删配置。
- `enabled_tools` / `disabled_tools`：限制工具集合。
- `default_tools_approval_mode`：决定工具默认审批行为。
- 单工具 approval override：高风险工具单独要求审批。
- `startup_timeout_sec` / `tool_timeout_sec`：避免工具卡死太久。

字段会随官方 Config Reference 更新，教程示例只讲用途，不把所有字段写成静态背诵表。

### 6.2 密钥和环境变量怎么放

MCP 配置里最危险的是 token。原则：

| 场景 | 推荐 | 不推荐 |
|---|---|---|
| 本地个人 token | 系统环境变量、密码管理器、Codex 支持的 env 引用 | 写进 `.codex/config.toml` 并提交 |
| 团队共享服务 | 组织 secret 管理、最小 scope、可轮换 | 共享个人账号 token |
| Cloud / remote | environment variables 或官方 secret 入口 | 在 setup 日志里 echo |
| 临时调试 | 临时只读 token，结束后撤销 | 使用生产写 token |

如果配置示例需要提 token，只写变量名，不写真实值：

```toml
[mcp_servers.docs]
url = "https://example.com/mcp"
bearer_token_env_var = "DOCS_MCP_TOKEN"
```

读者看到这段应该知道：真实 token 在环境变量里，不在教程、不在仓库、不在截图里。

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

## 9. 配置核对


一个 MCP 配置写完后，建议按这张表核对：

| 核对项 | 你应该看到 |
|---|---|
| App 可见 | `/mcp` 能看到 server 和工具 |
| 最小权限 | 只给当前任务需要的读写范围 |
| 密钥安全 | token 在环境变量、secret 或系统凭据里，不在仓库 |
| 只读试跑 | 能完成一个只读查询或读取任务 |
| 可审计 | 工具调用结果能回到线程中被 Review |
| 可撤销 | 知道如何禁用 server、撤销 token 或卸载插件 |

### 9.1 MCP 排障流程

| 症状 | 可能原因 | 排查 |
|---|---|---|
| `/mcp` 看不到 server | 配置层未加载、App 未刷新、项目未信任、server disabled | 先看 App Settings，再重启或刷新 App |
| CLI 能看到，App 看不到 | App 和 CLI 当前配置层或会话状态不同 | 回到 App 线程核对，以 App 使用结果为准 |
| server 启动失败 | 命令不存在、依赖未安装、PATH 不一致、timeout 太短 | 在终端单独跑启动命令，检查日志 |
| 工具调用超时 | server 慢、网络慢、工具 timeout 太短 | 缩小任务或调整 timeout |
| OAuth 失败 | 回调 URL / port、账号权限、组织策略问题 | 重新 login，确认 callback 设置 |
| 工具要求过大权限 | server 默认工具太宽 | 用 enabled_tools / disabled_tools 收窄 |
| 结果不可信 | 来源不明、时间过期、权限范围不清 | 要求 Codex 列出来源和查询条件 |

排障时不要第一步就重装。先确认“配置在哪一层、当前线程是否加载、server 是否启动、工具是否可见、调用是否被审批拦住”。

### 9.2 生产数据访问矩阵

| 数据类型 | 建议权限 | 是否允许自动写 | 备注 |
|---|---|---|---|
| 公开文档 | 只读 | 不涉及 | 可作为新手练习 |
| 内部文档 | 只读，限定空间 | 不自动写 | 注意敏感策略 |
| 测试数据库 | 只读起步，写入需测试环境 | 可在明确任务中小范围写 | 禁止导出大量数据 |
| 生产数据库 | 默认不可访问 | 不允许 | 需要单独审批和审计 |
| GitHub issue / PR | 只读起步 | 评论和更新需明确指令 | 不自动合并 |
| 邮箱 / 云盘 | 最小范围只读 | 不自动发送或移动文件 | 隐私风险高 |

MCP 的安全原则不是"绝不用"，而是"先只读、再小范围、可审计、可撤销"。

## 10. 课堂工坊：从只读文档工具到安全排查

### 案例一：用文档 MCP 做只读核对

目标：让 Codex 使用已连接的文档工具核对课程或 README，不修改文件。

1. 在 App Settings 或 `/mcp` 中确认文档类 MCP server 可见。
2. 在项目线程发送：

```text
使用当前可用的文档 MCP，核对 README 里的安装命令是否和官方文档一致。只读，不修改文件。请列出你查询到的来源和 README 中需要关注的行。
```

你应该看到：Codex 明确调用了文档工具，输出来源、差异和建议；Review 面板没有新增 diff。

### 案例二：数据库 MCP 只读查 schema

目标：练习“查数据库”和“改数据库”之间的权限边界。

```text
使用当前数据库 MCP 只读查看用户表相关 schema。只输出字段名、字段含义推测和需要人工确认的点。不要写入数据库，不要导出用户数据。
```

你应该看到：任务只做 schema 或元数据读取；如果工具要求写权限、生产库权限或导出数据，应取消并改成只读连接。

### 案例三：MCP 不可见时的排查顺序

目标：不用猜配置，按 App 到 CLI 的顺序定位问题。

1. 在线程输入 `/mcp`，看 server 是否出现。
2. 如果 App 看不到，再到终端运行：

```bash
codex mcp list
codex mcp --help
```

3. 检查 token 是否只在环境变量或 secret 中，不在仓库文件中。
4. 重启或刷新 App 后，再用只读任务试跑。

你应该看到：CLI 和 App 对同一 server 的可见性差异被说清楚；最终以 App 线程能否调用为准。

## 11. MCP Cookbook：五个真实场景

MCP 的价值不在“连上了”，而在能把外部工具放进可控工作流。下面五个场景可以直接用来训练团队。

### 11.1 官方文档核对

适合：课程、README、SDK 用法、API 参数核对。

```text
使用当前可用的官方文档 MCP，只读核对 docs/install.md 中的安装命令是否仍然准确。
请输出：
1. 你查询的文档来源
2. 教程中可能过期的行
3. 建议修改
不要修改文件。
```

关键点：必须列来源，不允许只说“官方文档显示”。

### 11.2 浏览器本地验证

适合：前端页面、登录流程、响应式布局。

```text
使用当前可用的浏览器 MCP 打开 http://localhost:3000/settings。
只读检查：
1. 页面是否能打开
2. 375px 宽度下按钮文字是否溢出
3. 控制台是否有明显错误
不要修改文件。
```

关键点：先确认本地服务是否已启动；如果要让 Codex 启动服务，要写清命令和停止方式。

### 11.3 数据库 schema 只读核对

适合：确认字段、索引、迁移状态。

```text
使用数据库 MCP 只读查看用户相关 schema。
只输出表名、字段名、索引、需要人工确认的字段含义。
不要读取用户数据行，不要导出数据，不要写入数据库。
```

关键点：schema 和真实用户数据要分开；生产库默认不可写。

### 11.4 PR / issue 上下文读取

适合：结合 GitHub issue、PR 评论、本地 diff 做判断。

```text
使用 GitHub 相关连接器或 MCP，只读读取这个 PR 的描述和 review comments。
结合当前本地 diff，输出哪些评论已处理、哪些未处理。
不要评论 PR，不要 push。
```

关键点：外部评论可能过期，要和当前 diff 对照。

### 11.5 内部 API 诊断

适合：只读健康检查、接口元数据、测试环境状态。

```text
使用内部 API MCP 查询测试环境的 /health 和 /version。
只输出状态码、版本号、时间戳和异常摘要。
不要调用写接口，不要访问生产环境。
```

关键点：内部 API MCP 要有服务端审计日志；不要把它当成万能生产运维入口。

## 12. MCP 设计评审清单

如果你要为团队新增一个 MCP server，先过这张表：

| 问题 | 需要回答 |
|---|---|
| 它解决什么重复问题？ | 不是为了“接一个工具”而接 |
| 有没有现成 Connector / Plugin？ | 有官方路径优先官方路径 |
| 默认读写权限是什么？ | 能只读就先只读 |
| token 怎么存？ | 环境变量、secret、OAuth，不进仓库 |
| 工具命名是否清楚？ | 高风险工具不要起模糊名字 |
| 是否支持 tool allowlist？ | 用 enabled_tools / disabled_tools 收窄 |
| 失败时输出什么？ | 不要只返回 stack trace |
| 日志在哪里？ | 能追踪谁调用了什么 |
| 如何禁用？ | server、token、插件都要能撤 |
| 谁维护？ | 有 owner 和升级路径 |

## 13. 常见错误

| 错误 | 正确做法 |
|---|---|
| 以为 MCP 自动可用 | 用 `/mcp` 或 App 设置确认 |
| 把 MCP 配置写进教程后不验证 | 以当前 CLI / App 输出为准 |
| 给数据库写权限 | 默认只读 |
| 让 Codex “随便查” | 明确目标和范围 |
| 把 API Key 写进 config 示例 | 使用环境变量或 secret |

## 14. 团队 MCP 登记表

团队只要引入 MCP，就应该有一张登记表。它不必复杂，但必须能回答“谁装的、能读什么、怎么关”。

| 字段 | 示例 |
|---|---|
| server 名称 | `context7`、`docs-search`、`github-tools` |
| 来源 | 官方、组织内、第三方 |
| transport | STDIO / HTTP / 插件携带 |
| 数据范围 | 公开文档、指定 repo、测试库 |
| 读写权限 | 只读 / 可评论 / 可写测试环境 |
| token 存放 | 环境变量、组织 secret、无 token |
| owner | 平台组、文档组、某项目维护人 |
| 审计方式 | 线程记录、服务日志、PR 评论 |
| 撤销方式 | disable server、撤销 OAuth、卸载插件 |

这张表能避免“某个 MCP 以前能用，但没人知道它为什么能访问生产系统”的事故。

## 常见问题

### Q1：App 里一定能管理所有 MCP 吗？

不一定。部分配置可能需要 CLI 或 `config.toml`。但 App 仍是使用主线。

### Q2：MCP 工具会不会自动运行？

Codex 会根据任务调用工具，但是否需要审批取决于工具、权限和设置。

### Q3：MCP 和 Web search 一样吗？

不一样。Web search 是搜索网页；MCP 是连接具体工具或服务。

### Q4：MCP 工具返回的内容一定可信吗？

不一定。它只是外部工具返回的结果。你仍要看来源、时间、查询条件、权限范围和是否可能被外部内容误导。

### Q5：MCP 配好了为什么 Codex 还是不用？

可能是任务不需要、工具说明不清、server 不可见、权限需要审批，或 Codex 判断自然语言和本地文件足够。你可以明确要求“使用当前可用的某个 MCP，只读核对来源”。

### Q6：一个 MCP server 工具越多越好吗？

不是。工具越多，选择成本和权限风险越高。团队 server 应该把常用工具命名清楚，把高风险工具单独审批或禁用。

### Q7：MCP 可以替代 Connector 吗？

不一定。Connector 通常负责账号级外部上下文；MCP 负责工具调用。GitHub、Figma、文档系统等场景可能同时存在 Connector、Plugin 和 MCP，先选官方推荐和团队已治理的路径。

---

## 15. MCP 深入：它不是搜索框，而是工具协议

MCP 的全称是 Model Context Protocol。学习时不要把它简化成“给 Codex 上网查资料”。MCP 更像一个标准接口，让 Codex 可以连接外部工具、上下文和服务。

### 15.1 MCP 能给 Codex 什么

| 类型 | 例子 | 价值 |
|------|------|------|
| 文档上下文 | OpenAI Docs、Context7 | 查新文档、减少过期知识 |
| 开发工具 | Playwright、Chrome DevTools | 控制浏览器、检查页面 |
| 设计工具 | Figma | 读取设计上下文 |
| 数据工具 | 数据库 schema、只读查询 | 理解数据结构 |
| 项目工具 | GitHub issue / PR | 读取工程协作上下文 |
| 内部系统 | 私有 API、知识库 | 接入公司上下文 |

### 15.2 MCP 不自动等于可信

MCP 返回的是外部系统给的信息。Codex 仍然要判断：

```text
- 这个 server 是否可信？
- 工具返回的内容是否完整？
- 是否有权限或分页限制？
- 是否可能是过期缓存？
- 是否需要和本地文件交叉核对？
```

课程里要强调：MCP 是“接入能力”，不是“事实保证”。

## 16. MCP Server 类型详解

Codex 支持常见的 STDIO server 和 streamable HTTP server。学习时可以这样理解：

| 类型 | 怎么运行 | 适合场景 |
|------|----------|----------|
| STDIO | 本地命令启动进程 | 本地工具、开发环境、私有脚本 |
| Streamable HTTP | 访问一个 URL | 远程服务、OAuth、云端工具 |

### 16.1 STDIO 示例

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
env_vars = ["LOCAL_TOKEN"]

[mcp_servers.context7.env]
MY_ENV_VAR = "MY_ENV_VALUE"
```

关键字段：

| 字段 | 作用 |
|------|------|
| `command` | 启动 server 的命令 |
| `args` | 传给命令的参数 |
| `env` | 给 server 设置环境变量 |
| `env_vars` | 从 Codex 环境转发变量 |
| `cwd` | 从哪个目录启动 |

### 16.2 Streamable HTTP 示例

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
```

关键字段：

| 字段 | 作用 |
|------|------|
| `url` | MCP server 地址 |
| `bearer_token_env_var` | 从环境变量取 bearer token |
| `http_headers` | 固定请求头 |
| `env_http_headers` | 从环境变量取请求头 |

### 16.3 OAuth 登录

支持 OAuth 的 MCP server 可以通过 CLI 登录：

```bash
codex mcp login server-name
```

如果 OAuth callback 端口或 URL 有企业网络要求，可以在 `config.toml` 配置 callback port 或 callback URL。

## 17. MCP 工具审批：不是所有工具都该自动跑

MCP server 可能暴露很多工具。工具越多，越需要治理。

### 17.1 server 默认审批

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
default_tools_approval_mode = "prompt"
startup_timeout_sec = 20
tool_timeout_sec = 45
enabled = true

[mcp_servers.chrome_devtools.tools.open]
approval_mode = "approve"
```

这个配置表达：

- 只启用 `open` 和 `screenshot`。
- 默认需要 prompt。
- `open` 可以更宽松。
- 超时显式设置，避免 server 卡住任务。

### 17.2 Allowlist 和 denylist

| 字段 | 用法 |
|------|------|
| `enabled_tools` | 只允许列出的工具 |
| `disabled_tools` | 在已启用工具中禁用一部分 |

教学建议：企业或新手优先用 `enabled_tools`。因为“只开需要的”比“先全开再禁几个”更容易解释。

### 17.3 工具风险分级

| 工具类型 | 风险 | 建议 |
|----------|------|------|
| 只读搜索 | 低 | 可以较宽松 |
| 读取私有数据 | 中 | 需要来源说明 |
| 写外部系统 | 高 | 需要人工确认 |
| 执行命令 | 高 | 配合审批和 Rules |
| 访问生产数据 | 很高 | 默认不要给新手练习 |

## 18. MCP 与密钥：环境变量比硬编码安全

MCP 配置经常涉及 token。课程里必须反复强调：不要把 token 写进教程、prompt 或仓库。

### 18.1 错误示例

```toml
[mcp_servers.internal_docs]
url = "https://docs.example.com/mcp"
http_headers = { "Authorization" = "Bearer real-token-here" }
```

### 18.2 更好的写法

```toml
[mcp_servers.internal_docs]
url = "https://docs.example.com/mcp"
bearer_token_env_var = "INTERNAL_DOCS_TOKEN"
```

或者：

```toml
[mcp_servers.internal_docs]
url = "https://docs.example.com/mcp"
env_http_headers = { "Authorization" = "INTERNAL_DOCS_AUTH_HEADER" }
```

### 18.3 密钥排障 prompt

```text
我的 MCP server 需要 token，但我不想把密钥写进配置文件。
请帮我设计环境变量方案。
不要让我把真实 token 粘贴到聊天里。
请说明：
1. config.toml 应该引用哪个环境变量
2. 本机如何设置这个变量
3. 如何验证变量存在但不打印真实值
```

## 19. MCP 与 Plugin 的关系

插件可以 bundle MCP server。这个设计很适合团队分发，但也容易让新人困惑。

### 19.1 普通 MCP 配置

```toml
[mcp_servers.docs]
command = "npx"
args = ["-y", "@example/docs-mcp"]
```

### 19.2 Plugin-provided MCP 配置

```toml
[plugins."sample@test".mcp_servers.sample]
enabled = true
default_tools_approval_mode = "prompt"
enabled_tools = ["read", "search"]

[plugins."sample@test".mcp_servers.sample.tools.search]
approval_mode = "approve"
```

区别是：普通 MCP 的启动命令由用户配置；插件带来的 MCP server 由插件 manifest 管理，用户配置主要控制启用状态和工具策略。

### 19.3 什么时候打包进 Plugin

| 场景 | 做法 |
|------|------|
| 个人临时使用 | 直接配置 MCP |
| 团队共享一套工具和说明 | 打包 Plugin |
| 需要同时带 Skill 和 MCP | 打包 Plugin |
| 需要 marketplace 发现 | 打包 Plugin |

## 20. MCP 课堂案例：文档核对

场景：你要确认课程里的 Codex 命令是否符合官方文档。

```text
请使用可用的官方文档 MCP 或本地官方文档缓存，核对下面这段课程内容。
只做事实核对，不润色。
输出：
1. 正确的说法
2. 可能过期的说法
3. 需要删除或改写的命令
4. 证据来源
```

适合用 MCP 的原因：

- 事实可能随版本变化。
- 官方文档比模型记忆可靠。
- 输出需要证据。

不适合让 MCP 做的事：

```text
- 替你决定课程风格。
- 替你判断商业定位。
- 自动修改所有文档而不 review。
```

## 21. MCP 课堂案例：浏览器验证

场景：本地 web app 改了 UI，需要用浏览器 MCP 或 App in-app browser 验证。

```text
请使用浏览器相关能力打开本地开发服务器。
检查：
1. 页面是否能加载
2. 主要按钮是否可见
3. 控制台是否有明显错误
4. 移动宽度是否有文本重叠

不要提交代码。
如果需要修改，先告诉我问题和涉及文件。
```

注意：浏览器能力和截图不是占位。课程可以讲“如何验证”，但不要在文章里放“此处插入截图”。

## 22. MCP 课堂案例：数据库 schema 只读核对

```text
请使用数据库 MCP 的只读能力查看 schema。
目标：
- 确认 users 表是否有 deleted_at 字段
- 确认 orders 表和 users 表的关联字段
- 不读取真实客户数据
- 不执行写操作

输出只包含 schema 结论和后续代码修改建议。
```

这个案例的重点是最小数据原则：能看 schema 就不看数据，能看测试库就不看生产库。

## 23. MCP 课堂案例：GitHub PR 上下文

```text
请使用 GitHub 相关 MCP 或连接能力读取当前 PR 的评论。
只读操作。
把评论分成：
1. bug
2. 测试
3. 文档
4. 产品问题
5. 可以忽略或需要解释的评论

不要回复评论，不要打 label，不要修改 PR。
```

这个 prompt 可以和 Review 课联动：外部评论来自 GitHub，本地 diff 在 Review 面板里看。

## 24. MCP 课堂案例：内部 API 诊断

```text
请使用内部 API 文档 MCP 查询 `/v1/invoices/{id}` 的错误响应约定。
只读取文档，不调用真实 API。
然后对比当前代码里的错误处理。
输出：
- 文档约定
- 代码当前行为
- 差异
- 建议最小改动
```

这个场景展示 MCP 的强项：把外部规范带进本地代码审查。

## 25. MCP 失败模式大全

| 失败模式 | 表现 | 修复方式 |
|----------|------|----------|
| server 启动失败 | `/mcp` 看不到或报错 | 检查 command、args、cwd |
| token 缺失 | 认证失败 | 用环境变量 |
| 工具太多 | Codex 选错工具 | 用 enabled_tools |
| 工具超时 | 任务卡住 | 调整 timeout 或缩小任务 |
| server 指令太长 | Codex 忽略重点 | MCP server instructions 前 512 字写核心 |
| 返回内容太泛 | prompt 没说明要查什么 | 明确问题和输出 |
| 权限过大 | 读取或写入超范围 | 收窄工具和审批 |
| App / CLI 不一致 | 配置层不同 | 查用户级和项目级 config |

### 25.1 MCP 不被调用时

```text
Codex 没有调用我配置的 MCP。
请先判断：
1. 当前任务是否真的需要 MCP
2. MCP server 是否启用
3. 相关工具是否在 enabled_tools 中
4. prompt 是否明确要求外部上下文
5. 是否有更合适的内置能力
```

### 25.2 MCP 返回不可信时

```text
请把 MCP 返回内容和本地仓库文件交叉核对。
标出：
- MCP 明确给出的事实
- 本地文件支持的事实
- 两者冲突的地方
- 需要人工确认的地方
```

## 26. 综合工坊：接入一个只读文档 MCP

这个工坊适合让学生第一次体验 MCP。目标不是追求复杂配置，而是理解连接、可见、调用、核对四步。

### 26.1 第一步：明确需求

```text
我想让 Codex 在写课程时能查官方开发文档。
请判断是否适合接入文档 MCP。
先解释 MCP 相比普通 Web search 的价值。
不要修改配置。
```

### 26.2 第二步：添加 server

示例：

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

或者直接写 `config.toml`：

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

### 26.3 第三步：查看可见性

在 CLI TUI：

```text
/mcp
```

在 App 中：

```text
请帮我确认当前项目是否能看到文档 MCP。
如果看不到，请按配置层、重启、新线程和项目信任状态排查。
```

### 26.4 第四步：第一次使用

```text
请使用可用文档 MCP 核对 Codex Skills 的目录位置和触发方式。
只做事实核对。
输出：
1. 官方说法
2. 当前课程说法
3. 是否需要修改
```

### 26.5 第五步：复盘

```text
请复盘这次 MCP 使用：
1. MCP 解决了什么问题
2. 哪些信息仍然需要本地文件核对
3. 这个 MCP 是否应该给团队共享
4. 需要哪些权限或工具限制
```

## 27. MCP 设计评审题

给学生一个 server 方案，让他们判断是否能接入：

```md
# Proposed MCP

Name: internal-admin
Transport: HTTP
Tools:
- read_user
- update_user_role
- delete_user
- search_audit_log
Auth: bearer token
Data: production users
```

讨论问题：

```text
1. 哪些工具应该默认禁用？
2. 是否应该允许新手使用？
3. 是否需要测试环境版本？
4. approval mode 应该怎么设？
5. 是否更适合只接 audit log，而不是用户写操作？
```

推荐答案方向：

```text
- `update_user_role` 和 `delete_user` 不适合默认开放。
- 生产用户数据不适合教学。
- 先做只读 audit/search server。
- 写操作需要人工流程和外部系统审计。
```

## 28. MCP 进阶常见问题

### Q1：MCP server 越多越好吗？

不是。server 越多，Codex 可选工具越多，误选和权限风险也越高。优先接入高频、可信、只读或可控的 server。

### Q2：MCP 能替代项目文档吗？

不能。MCP 提供外部上下文，项目自己的命令、目录、规则仍然应该写在 `AGENTS.md` 和仓库文档里。

### Q3：MCP 工具失败是不是任务就失败？

不一定。Codex 可以降级为本地文件、Web search 或让你补充资料。但如果任务依赖该工具的唯一数据源，就需要先修 MCP。

### Q4：HTTP MCP 一定比 STDIO 好吗？

不一定。HTTP 适合远程服务和 OAuth；STDIO 适合本地工具和脚本。选型看数据位置、认证方式和团队维护能力。

### Q5：Plugin 带的 MCP 是否自动可信？

不是。Plugin 可以打包 MCP，但工具权限、认证、数据范围仍然要看。安装来源可信也不等于每个工具都适合自动运行。

## 29. MCP 引入决策会：先问三条问题线

一个 MCP server 值不值得接入，不要只看“能不能跑”。至少要问三条问题线：它能不能帮当前任务，它会打开哪些数据和工具，它是否值得成为团队默认能力。

### 29.1 任务价值

```text
请评估这个 MCP server 对当前开发任务是否有帮助。
只看：
1. 它能提供哪些本地没有的上下文
2. 哪些工具适合启用
3. 哪些工具暂时不需要
```

### 29.2 数据和权限

```text
请从安全角度审查这个 MCP 配置。
重点看数据范围、写工具、token 管理、审批模式和 allowlist。
```

### 29.3 团队采用

```text
请判断这个 MCP 是否应该作为团队默认能力。
给出：
- 推荐使用场景
- 不推荐使用场景
- 需要配套的 Skill 或文档
- 试点方式
```

这三条线可以由一个人先跑，也可以在团队评审里分开讨论。关键是不要只因为“配置成功”就把 server 放进所有项目。

## 30. MCP 作业：写一份 server 引入说明

```md
# MCP Introduction Note

## Server

Name:
Owner:
Transport:

## Why

This server helps Codex...

## Tools

- Allowed:
- Prompt before use:
- Disabled:

## Auth

Environment variables:
OAuth:

## Example Prompt

...

## Risks

...
```

这份作业能训练学生把“我配好了”变成“团队知道怎么用”。

## 31. MCP 长案例：从“能接上”到“能放心用”

很多 MCP 教程停在“配置成功”。真正的课程不能停在那里，因为 MCP 的关键不是接通，而是接通以后 Codex 会用它读什么、写什么、什么时候应该停下来问人。

假设团队想接一个内部文档 MCP，用来回答项目设计问题。坏的引入方式是：

```text
我们有一个 docs MCP，接上以后让 Codex 自己查文档。
```

这句话少了四件事：

```text
1. 查哪些文档。
2. 是只读还是可写。
3. 查到的内容能不能进入代码修改依据。
4. 文档和代码冲突时听谁的。
```

更好的引入说明：

```md
# Internal Docs MCP Adoption Note

## Purpose

Let Codex read internal architecture notes and API docs when answering questions or planning code changes.

## Allowed Use

- Search architecture docs.
- Read API examples.
- Summarize docs into a local implementation plan.
- Cite which document influenced the plan.

## Not Allowed

- Edit internal docs through MCP.
- Treat docs as newer than code without checking repository files.
- Use docs to justify broad refactors without local evidence.

## Conflict Rule

If docs and code disagree, Codex should report the disagreement and ask the user which source is authoritative.
```

第一次试用不要让 Codex 直接改代码。先做只读问答：

```text
请使用可用的内部文档 MCP 回答：

这个项目的 auth redirect 流程设计目标是什么？

要求：
1. 说明你读取了哪些文档。
2. 总结设计目标。
3. 标出仍需要看代码确认的地方。
4. 不要修改文件。
```

第二次试用再让它把文档和代码对齐：

```text
请比较内部文档中对 auth redirect 的描述和当前代码。

输出：
1. 文档和代码一致的地方。
2. 文档提到但代码没体现的地方。
3. 代码存在但文档没提到的地方。
4. 建议先改代码还是先改文档。

不要修改文件。
```

只有当这两轮输出都稳定，才进入写入任务：

```text
根据刚才的文档和代码对比，只更新 README 中 auth redirect 的说明。

边界：
1. 不修改业务代码。
2. 不调用写入型 MCP tool。
3. 文档描述必须和当前代码一致。
4. 如果发现代码行为不确定，先停止并说明。
```

这个案例训练的是 MCP 的真实风险感：工具能读外部系统，不等于外部系统永远正确；工具能写，不等于应该写；工具能给 Codex 更多上下文，不等于可以替代本地证据。

## 32. MCP 失败恢复：不是所有错误都叫“server 坏了”

MCP 出问题时，很多人会直接重装 server。更好的排查顺序是从使用场景开始。

### 32.1 Codex 没有调用 MCP

可能原因：

```text
- prompt 没说清需要外部工具。
- 当前任务用本地文件就能完成。
- tool 没启用或被 allowlist 限制。
- server 已配置但没有在当前项目或当前会话可用。
- Codex 判断调用成本高于收益。
```

排查 prompt：

```text
我希望你使用可用的 MCP 工具读取内部文档。

请先说明：
1. 当前会话中你能看到哪些相关工具。
2. 哪些工具适合这个任务。
3. 如果你不调用 MCP，原因是什么。

不要修改文件。
```

### 32.2 MCP 调用了，但答案不可信

不要立刻否定工具，先要求证据链：

```text
请重新回答刚才的问题。

要求：
1. 列出你使用的 MCP 来源。
2. 每个关键结论对应哪个来源。
3. 标出需要用本地代码确认的结论。
4. 如果来源之间冲突，直接说明冲突。
```

如果回答仍然泛，可以收窄问题：

```text
只查 auth redirect 相关文档。
不要总结整个系统。
只回答 callback URL 在登录前后如何保存。
```

### 32.3 MCP 需要授权或权限失败

这时不要把任务改成更大权限。先判断是否真的需要这个 tool。

```text
请把当前任务拆成两部分：
1. 不需要 MCP 授权也能完成的本地分析。
2. 只有 MCP 授权后才能完成的外部信息读取。

对第二部分，说明读取的必要性和替代方案。
```

如果替代方案足够，就先用本地分析；如果确实需要授权，再让用户知道为什么。

### 32.4 MCP 输出让 Codex 想改外部系统

对课程读者来说，这是一条红线。先把任务降级为只读计划：

```text
不要执行任何外部写入。
请只输出你想调用的 MCP tool、目的、可能影响和替代方案。
等我确认后再继续。
```

这个 prompt 不是为了增加麻烦，而是为了让外部系统写入从“模型顺手做了”变成“人明确决定了”。

## 33. MCP 与 Skills 的组合：把工具使用变成可复用流程

如果一个 MCP 流程只用一次，prompt 就够了。如果它每周都用，应该做成 Skill。

一次性 prompt：

```text
用内部文档 MCP 查 auth redirect 设计，并和当前代码对比。
```

可复用 Skill 的思路：

```text
Skill 名称：docs-code-drift-review
用途：比较内部文档和当前代码是否一致。

流程：
1. 读取用户指定的主题。
2. 使用文档 MCP 查相关资料。
3. 读取仓库中对应文件。
4. 输出一致、不一致、无法判断。
5. 不修改文件，除非用户明确要求下一步。
```

这样设计有三个好处：

```text
- MCP 只是工具，Skill 才是流程。
- 每次不用重新解释输出格式。
- 团队能统一“文档和代码冲突时怎么说”。
```

一个调用示例：

```text
$docs-code-drift-review
主题：auth redirect callback URL
请比较内部文档和当前代码。
输出可行动建议，不要修改文件。
```

如果团队再想分发给别人，就进入 Plugin 章节：把 Skill 和需要的 app/MCP 说明一起打包，而不是让每个人手抄配置。

## 34. MCP 运行记录：工具调用之后要留下什么

MCP 工具调用如果只存在于线程里，团队很难复盘它是否可靠。对于重要任务，可以让 Codex 输出一份轻量运行记录。

```md
# MCP Run Note

## Task

...

## Tools Used

- Server:
- Tool:
- Purpose:

## Data Read

- ...

## Result

- ...

## Local Evidence Checked

- Files:
- Tests:

## Conflicts

- Docs vs code:
- Tool result vs local result:

## Next

- ...
```

调用 prompt：

```text
请在完成 MCP 查询后输出一份 MCP Run Note。

要求：
1. 说明调用了哪个 server / tool。
2. 说明读取了什么类型的数据。
3. 说明哪些结论已经用本地代码确认。
4. 标出不能确认或冲突的地方。
5. 不要包含敏感原文。
```

这个记录在三种情况下特别有用：

```text
- 外部文档影响了代码修改。
- MCP 查询结果和本地代码不一致。
- 团队要决定是否把这个 MCP 加入默认工具集。
```

示例：

```md
# MCP Run Note

## Task

Compare auth redirect docs with current code.

## Tools Used

- Server: internal-docs
- Tool: search/read docs
- Purpose: find redirect design notes

## Data Read

- Architecture note for auth redirect
- API example for callback URL

## Result

Docs say callback URL should be preserved through login.

## Local Evidence Checked

- `src/auth/redirect.ts`
- `tests/auth-redirect.test.ts`

## Conflicts

Current test covers default redirect only, not callback URL.

## Next

Add regression test before changing implementation.
```

MCP Run Note 能避免一个常见问题：过了两周以后，没人记得当时 Codex 为什么相信某份外部资料。课程里训练这个记录，会让外部工具使用变得可追踪。

## 35. MCP 课堂练习：把写入工具改成只读试点

给学生一个高风险描述：

```text
我们想接一个 issue tracker MCP，让 Codex 自动更新 issue 状态。
```

要求先改成只读试点：

```md
# Issue Tracker MCP Read-only Trial

## Goal

Let Codex read issue status and summarize work items.

## Allowed

- Search issues.
- Read issue comments.
- Summarize blockers.
- Suggest local next actions.

## Not Allowed

- Update issue status.
- Assign users.
- Add labels.
- Post comments.
- Create or close issues.

## Trial Prompt

Use the issue tracker MCP to read open issues related to auth redirect.
Summarize blockers and link them to local files.
Do not write to the issue tracker.
```

再让学生写升级条件：

```text
只有当只读试点连续两周输出可靠，
并且团队明确 owner、授权范围、撤销路径后，
才讨论是否开放写入 tool。
```

这个练习能把“我们想自动化外部系统”改成“先验证读取是否真的有价值”。很多团队的 MCP 风险，就是跳过了这一步。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解MCP是工具连接层，不是提示词也不是搜索
- [ ] 知道用`/mcp`或App Settings确认工具是否可用
- [ ] MCP工具只给了当前任务需要的最小权限
- [ ] 密钥/token存放在环境变量或系统凭据中，不在仓库里
- [ ] 完成过一个只读MCP查询任务
- [ ] 工具调用结果能在线程中被Review
- [ ] 知道如何禁用server、撤销token或卸载插件

**全部勾选后即掌握 Codex MCP。**

---

## 附录

### A. MCP相关命令速查

| 命令 | 用途 |
|------|------|
| `/mcp` | 查看当前MCP server和工具 |
| `codex mcp list` | CLI中列出MCP工具 |
| `codex mcp --help` | CLI中查看MCP帮助 |

### B. MCP配置核对

| 核对项 | 你应该看到 |
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
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-06 Skills：在 App 中调用和编写可复用工作流](./CX-06-Codex-Skills可复用工作流完整指南.md)。
