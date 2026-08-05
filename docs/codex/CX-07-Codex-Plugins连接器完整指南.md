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
> - **更新日期**：2026年5月30日
> - **信息来源**：OpenAI Codex App Features、Plugins、Apps/Connectors、MCP、Skills 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **区分四个核心概念**：清楚Connector、Plugin、Skill、MCP各自是什么、不是什么
2. **理解连接器工作流**：掌握安装→授权→引用→执行→核对的完整流程
3. **安装前安全检查**：知道看来源、能力、权限、数据范围、撤销方式
4. **掌握GitHub连接器**：完成GitHub连接器的最小可用流程（只读→只读总结→控制写权限）
5. **理解Plugin的能力包结构**：知道Plugin可以包含Skills、MCP、Connectors和配置
6. **遵循最小权限原则**：只给必要权限、不再使用及时禁用
7. **核对连接器和插件**：App可见、权限清楚、只读试跑、写操作可控、可撤销
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

## 术语表（小白必读）

插件和连接器最容易被混成一个词。先把它们拆开：

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| Connector / App | 外部账号连接 | 重点看授权范围 |
| Plugin | 可安装的能力包 | 可能包含 Skills、MCP、Apps、配置 |
| Marketplace | 插件来源目录 | 来源可信比数量重要 |
| Skill | 插件可能携带的工作流 | 看触发和输出 |
| MCP server | 插件可能携带的工具服务 | 看工具权限和审批 |
| Consent dialog | 授权前的确认界面 | 认真读 scope |
| Scope | 外部服务授权范围 | 只给必要权限 |
| Revocation | 撤销授权或卸载 | 使用前就要知道怎么关 |

## 0. 安装、授权、调用是三件事

老金在插件这篇里会反复提醒授权范围，因为连接器一旦接上账号，教学就必须讲清楚撤销和审计。

很多安全事故来自一个误解：以为“安装插件 = 可以访问所有数据”。更准确的流程是：

```text
安装 Plugin
  -> 查看它带来的 Skills / MCP / Apps / 配置
  -> 对外部服务单独授权
  -> 在线程中引用或调用
  -> 工具或外部动作按权限和审批执行
  -> 不用时撤销授权或卸载
```

### 0.1 连接器决策树

| 你要做什么 | 优先选择 | 原因 |
|---|---|---|
| 读取 GitHub PR / issue 上下文 | GitHub Connector / App | 账号上下文最直接 |
| 使用浏览器、数据库、文档工具 | MCP | 工具协议更合适 |
| 复用团队固定流程 | Skill | 不需要外部授权 |
| 一次安装一整套工作流 | Plugin | 能打包 Skills、MCP、Apps |
| 定时读外部状态 | Automation + Connector / Skill | Connector 不负责调度 |

### 0.2 插件安全阅读法

安装前读四层：

1. **来源**：官方、组织内、第三方、还是本地 marketplace。
2. **能力**：带 Skills、MCP、Apps、hooks、配置中的哪些。
3. **权限**：只读、评论、写入、发消息、创建 PR 是否分开。
4. **撤销**：App 里卸载、服务后台 revoke、组织后台禁用在哪里。

安装后第一件事不是让它写，而是做一个只读试跑。

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
codex
# 在交互界面输入 /plugins

codex plugin marketplace list
codex plugin marketplace add owner/repo
codex plugin marketplace upgrade
codex plugin marketplace remove marketplace-name
```

适合：

- 在 CLI 交互界面浏览插件目录。
- 管理 marketplace 来源。
- 排查插件来自哪个 marketplace。

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

## 10. 启用后核对


连接器或插件启用后，检查：

| 核对项 | 你应该看到 |
|---|---|
| App 可见 | 线程里能看到对应 App / Plugin / Skill / Tool |
| 权限清楚 | 知道它能读什么、写什么 |
| 只读试跑 | 能基于外部上下文做只读摘要 |
| 写操作可控 | 评论、提交、发消息前需要明确指令或审批 |
| 可撤销 | 知道在哪里断开连接或卸载 |

### 10.1 常见故障排查

| 症状 | 可能原因 | 排查 |
|---|---|---|
| 插件安装了但没有能力 | 插件只带 metadata 或未启用相关能力 | 看插件详情页 |
| Connector 授权后仍读不到内容 | scope 不够、组织策略限制、目标资源不可访问 | 重新检查授权范围和组织设置 |
| Skill 没出现 | 插件带的 Skill 未启用或名称不对 | 打开 Skills / 插件详情 |
| MCP 工具不可见 | 插件 MCP 需要额外配置或启动失败 | 看 `/mcp` 和插件说明 |
| 外部写操作没执行 | 权限不足或需要审批 | 看 consent、approval 和线程提示 |
| 不知道怎么关闭 | 安装和授权位置不同 | 同时检查 App 插件页和外部服务授权页 |

### 10.2 团队插件登记表

| 字段 | 示例 |
|---|---|
| 插件名称 | GitHub workflow pack |
| 来源 | OpenAI curated / 组织 marketplace / 第三方 |
| 能力 | Skills、GitHub Connector、MCP |
| 授权范围 | 指定 repo 只读，PR 评论需审批 |
| Owner | 平台组 |
| 试跑任务 | 只读总结一个 issue |
| 撤销方式 | App 卸载 + GitHub OAuth revoke |

团队不要靠“谁电脑上装了什么”来管理插件。插件一旦参与开发流程，就应该像依赖一样有来源、owner 和撤销路径。

## 11. 课堂工坊：GitHub、插件和 Skill 组合

### 案例一：GitHub 连接器只读读 PR

目标：确认连接器能提供 PR 上下文，但不会自动评论或改代码。

1. 在 App 的 Plugins / Connectors / Apps 入口连接 GitHub。
2. 授权时优先选择当前练习仓库需要的最小范围。
3. 回到项目线程，引用一个 issue 或 PR，发送：

```text
读取这个 PR 的标题、描述、评论和当前本地 diff。只读总结：还有哪些 review 意见没处理。不要评论 PR，不要修改文件。
```

你应该看到：Codex 能总结 PR 上下文和本地 diff 的关系；没有 GitHub 评论、提交或文件改动。

### 案例二：安装插件前做权限阅读

目标：练习安装前先读能力和权限，不盲点 Add。

1. 打开 App 的 Plugins。
2. 选择一个你有权限使用的插件，先读详情页。
3. 记录它是否包含 Skills、Apps、MCP servers 或本地命令。
4. 只在确认来源和撤销方式后安装。
5. 开新线程发送：

```text
说明当前已安装的这个插件能提供哪些工作流，以及第一次使用时应该先做哪个只读试跑。不要调用外部写操作。
```

你应该看到：Codex 先解释能力和边界，而不是直接触发外部服务动作。

### 案例三：Plugin + MCP + Skill 的一条工作流

目标：理解插件是能力包，不是单个按钮。

```text
使用已安装的 GitHub 相关插件或连接器，结合当前项目规则，帮我做一次 issue triage。只读读取 issue 和本地代码，输出：问题是否可复现、可能涉及文件、建议下一步。不要创建分支，不要评论 issue。
```

你应该看到：Codex 会把外部 issue、项目文件和工作流方法组合起来；如果插件还需要登录或 MCP server 未配置，它会提示缺少哪一层能力。

## 12. 插件治理 Runbook

插件一旦进入团队工作流，就不再只是个人偏好。它可能带来外部账号、MCP server、Skills、配置和本地命令。下面是一套轻量治理流程。

### 12.1 引入前评审

| 问题 | 要看什么 |
|---|---|
| 来源是否可信 | 官方、组织内、第三方、GitHub repo、维护活跃度 |
| 能力是否必要 | 是否已有 App / Connector / MCP / Skill 能解决 |
| 权限是否合理 | 是否要求过大的账号 scope |
| 是否有本地执行 | 是否带 hooks、scripts、MCP stdio 命令 |
| 是否能禁用 | App、CLI、外部服务是否都有撤销路径 |
| 是否有替代方案 | 不安装插件能不能用现有能力完成 |

评审不是为了拖慢使用，而是避免“装了才发现它能读太多东西”。

### 12.2 试点流程

1. 选择一个非生产项目。
2. 安装插件但不立刻授权外部账号。
3. 阅读插件详情，列出它带来的 Skills、MCP、Apps 或配置。
4. 如需授权，只给试点 repo / 测试空间。
5. 做一个只读任务。
6. 记录输出是否可靠、权限提示是否清楚、撤销是否方便。
7. 试点稳定后再推广到团队。

### 12.3 插件升级前

插件升级可能改变能力和权限。升级前看：

- 是否新增 MCP server。
- 是否新增外部账号连接。
- 是否改变 Skill 行为。
- 是否新增 hooks 或本地命令。
- 是否改变默认权限或 approval 行为。
- 是否影响 Windows / macOS 路径。

升级后做一次只读试跑，不要直接让升级后的插件执行写操作。

### 12.4 插件下线

下线不是点“卸载”就结束：

```text
App 中禁用或卸载插件
  -> 外部服务后台撤销 OAuth / app grant
  -> 删除或禁用相关 MCP 配置
  -> 检查 Automations 是否还引用它
  -> 检查 Skills 是否还依赖它
  -> 更新团队登记表
```

如果插件曾经能评论 PR、发消息或访问文档，外部授权撤销尤其重要。

## 13. 常见错误

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

### Q4：插件能带 Hooks 或 MCP 吗？

可以带生命周期配置或 MCP server，但启用后仍要经过信任、权限和工具可见性核对。不要因为它来自插件就跳过审查。

### Q5：连接器读取的外部内容会不会影响 Codex 判断？

会。外部 issue、邮件、文档都可能包含过期信息或误导性内容。让 Codex 引用来源、区分事实和推测，不要直接把外部内容当命令执行。

### Q6：团队应该允许每个人随便装插件吗？

不建议。个人实验可以宽一些，团队仓库和企业环境应有 marketplace、白名单、owner 和撤销流程。

---

## 14. 深入理解：Plugin 不是"装更多按钮"，而是交付一组可复用能力

很多人学 Plugin 的第一反应是：我是不是要像装浏览器扩展一样，把能装的都装上？这会把 Codex 用歪。Plugin 的真正价值不是"多一个入口"，而是把一个团队已经认可的工作方式打包成可安装、可分享、可关闭、可治理的能力包。

在 Codex 里，一个 Plugin 可能带来三类能力：

| 能力 | 解决什么问题 | 学习时怎么理解 |
|------|--------------|----------------|
| Skill | 让 Codex 按固定流程做一类任务 | 相当于“带说明书的工作方法” |
| App integration | 连接 GitHub、Slack、Google Drive 等外部系统 | 相当于“账号和数据通道” |
| MCP server | 给 Codex 新工具或新上下文 | 相当于“工具箱和接口层” |

所以 Plugin 的学习顺序应该是：

1. 先判断任务是否真的需要外部能力。
2. 再判断外部能力是账号连接、工具调用，还是流程复用。
3. 最后才决定安装、共享、禁用或移除。

### 14.1 插件安装后的四层变化

安装 Plugin 后，变化不一定立刻出现在聊天输入框里。你要从四层看：

| 层级 | 你会看到什么 | 常见误解 |
|------|--------------|----------|
| 目录层 | App 的 Plugins 页面出现已安装条目 | 以为出现条目就等于外部账号已连接 |
| 能力层 | `@` mention 或 bundled skills 可被调用 | 以为所有能力都会自动触发 |
| 授权层 | 外部 App 可能要求登录或授权 | 以为安装插件就授权了所有数据 |
| 执行层 | Codex 根据 prompt、权限和审批调用工具 | 以为插件能绕过审批或沙盒 |

一个成熟团队会把这四层分开沟通。新人只要记住一句话：**安装是让能力可见，授权是让数据可用，调用是让任务发生，审批是最后的安全门。**

### 14.2 App 插件目录里的三类来源

Codex App 的插件目录会把插件按来源分组。对课程学习来说，你可以这样判断：

| 来源 | 适合谁 | 处理方式 |
|------|--------|----------|
| Curated by OpenAI | 个人学习、通用场景 | 先看说明和权限，再安装 |
| Shared with you | 团队共享工作流 | 问清团队推荐使用场景 |
| Created by you | 自己开发或本地打包 | 先在小项目里试用 |

课堂练习不要一上来就安装很多外部账号插件。先用一个低风险的插件理解“浏览、安装、授权、调用、关闭”的生命周期，再逐步接入 GitHub、Slack、Drive 这类真实数据源。

## 15. Plugin 生命周期：从发现到下线

下面是一条完整的插件生命周期。你可以把它当成团队内部培训的主流程。

```text
发现需求
  ↓
判断是否需要 Plugin
  ↓
阅读插件说明、权限、来源
  ↓
小范围安装
  ↓
第一次显式调用
  ↓
观察输出和工具调用
  ↓
沉淀团队使用模板
  ↓
定期复盘是否保留
  ↓
禁用、升级或移除
```

### 15.1 发现需求：先写任务，不先找插件

错误说法：

```text
帮我看看有什么好用的插件。
```

这种问法会把注意力引到“有什么新玩具”。更好的说法是：

```text
我每周要整理 GitHub PR 评论、Slack 讨论和项目 README 的差异。
请判断这个任务是否适合用 Codex Plugin、MCP、Skill 或普通 App 线程完成。
先解释选择理由，再给我最小可行流程。
```

这个 prompt 会让 Codex 先理解业务流程，而不是马上推荐安装。

### 15.2 小范围安装：先挑一个低风险任务

插件第一次进入团队时，建议选只读任务。比如 GitHub 场景：

```text
请使用 GitHub 相关连接能力读取当前 PR 的标题、描述和评论。
只做摘要，不修改分支，不发表评论，不创建 issue。
输出：
1. PR 当前讨论焦点
2. 仍未解决的问题
3. 需要我人工决定的事项
```

这类任务的好处是：它验证了连接、权限和上下文读取，却没有直接写外部系统。

### 15.3 第一次显式调用：用 `@` 降低歧义

安装多个插件后，Codex 可能有多种路径能完成任务。为了教学和排障，第一次使用时建议显式点名：

```text
@github 请读取当前仓库的 PR 上下文。
只总结评论，不改文件，不调用写操作。
如果你无法访问 PR，请告诉我缺少哪一步配置。
```

显式调用不是永远需要。它的价值在于让新人看清：到底是哪个插件参与了这次任务。

### 15.4 观察输出：看“用了什么”，不只看“答得像不像”

插件任务结束后，不要只读最后摘要。你还要追问：

```text
请复盘刚才这次插件任务：
1. 你使用了哪些插件或工具能力？
2. 哪些信息来自外部系统？
3. 哪些结论是你根据上下文推断的？
4. 有没有权限、网络、认证或数据范围限制？
```

这一步能训练团队把“AI 说了什么”和“AI 凭什么说”分开。

## 16. 本地与团队插件市场：从个人工具到组织能力

Codex 支持通过 marketplace 管理可发现插件。课程里要把它理解成“团队的能力目录”，而不是公共应用商店的简单复制。

### 16.1 什么时候需要本地 marketplace

下面这些情况适合维护一个 repo 级或个人级 marketplace：

| 场景 | 为什么不用单个本地插件就完事 |
|------|------------------------------|
| 团队有多个可复用插件 | 需要统一入口和命名 |
| 插件要跟项目一起交付 | 需要让新人打开项目就知道有哪些能力 |
| 插件需要版本控制 | 需要 Git 历史记录和 review |
| 插件要分组 | 需要按产品、工程、数据、安全分类 |
| 插件要逐步推广 | 需要先让少数人安装，再共享给团队 |

### 16.2 CLI 管理 marketplace 的正确命令

Marketplace 是 CLI 辅助路径，不是 App 用户的主学习入口。你需要记住的命令是这一组：

```bash
codex plugin marketplace add owner/repo
codex plugin marketplace add owner/repo --ref main
codex plugin marketplace add https://github.com/example/plugins.git --sparse .agents/plugins
codex plugin marketplace add ./local-marketplace-root
codex plugin marketplace list
codex plugin marketplace upgrade
codex plugin marketplace upgrade marketplace-name
codex plugin marketplace remove marketplace-name
```

注意这里管理的是 marketplace，不是用一个普通 `plugin list` 命令列出所有插件。App 用户日常仍然从 App 的 Plugins 页面和 CLI TUI 的 `/plugins` 浏览。

### 16.3 Repo 级 marketplace 的课堂示例

假设团队把插件放在仓库的 `plugins/` 目录，并用 `.agents/plugins/marketplace.json` 暴露：

```json
{
  "name": "team-codex-plugins",
  "plugins": [
    {
      "name": "pr-review-pack",
      "source": {
        "source": "local",
        "path": "./plugins/pr-review-pack"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Engineering"
    },
    {
      "name": "docs-drift-pack",
      "source": {
        "source": "local",
        "path": "./plugins/docs-drift-pack"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_USE"
      },
      "category": "Documentation"
    }
  ]
}
```

这段示例要表达三个重点：

- `source.path` 是相对 marketplace root 的路径。
- `policy.authentication` 表达的是安装或使用时的认证时机。
- `category` 是为了让人更容易浏览，而不是安全边界。

### 16.4 插件目录与实际文件的关系

很多团队会卡在路径理解上。你可以用这张图讲清楚：

```text
repo-root/
  .agents/
    plugins/
      marketplace.json
  plugins/
    pr-review-pack/
      .codex-plugin/
        plugin.json
      skills/
        pr-review/
          SKILL.md
    docs-drift-pack/
      .codex-plugin/
        plugin.json
      skills/
        docs-drift/
          SKILL.md
```

Marketplace 负责“让 Codex 找到插件”。Plugin manifest 负责“告诉 Codex 插件里有什么”。Skill 负责“告诉 Codex 具体怎么做事”。

## 17. 从 Skill 升级为 Plugin：一个完整案例

假设你已经有一个 `pr-review` skill，用来审查 PR 的风险。什么时候应该升级成 Plugin？

| 信号 | 含义 |
|------|------|
| 多个仓库都要用 | 复制 skill 文件开始变得难维护 |
| 需要 GitHub 连接 | 不再只是提示词流程 |
| 需要附带 MCP | 需要把工具配置一起分发 |
| 需要图标、名称、默认 prompt | 面向团队用户，需要更好的界面表达 |
| 需要 workspace sharing | 想让指定成员安装，而不是让每个人手动复制 |

### 17.1 最小插件 manifest

```json
{
  "name": "pr-review-pack",
  "version": "1.0.0",
  "description": "Reusable PR review workflow for Codex.",
  "skills": "./skills/"
}
```

这里的 `name` 要稳定。改名会影响人对插件的识别，也会让团队文档和使用模板失效。

### 17.2 插件内的 Skill

```md
---
name: pr-review
description: Review a pull request for correctness, security risk, missing tests, and maintainability. Use when the user asks for PR or diff review.
---

Review the pull request like an owner.

Workflow:
1. Read the diff and nearby code before giving findings.
2. Prioritize behavior regressions, security issues, and missing test coverage.
3. Cite file paths and line references when available.
4. Separate confirmed issues from questions.
5. Keep the final response concise and actionable.
```

这个 Skill 的核心不是"让 Codex 更像审查员"，而是把团队认可的 review 顺序写下来。

### 17.3 插件使用 prompt

```text
@pr-review-pack 请审查当前分支相对 main 的改动。
重点看：
1. 真实 bug
2. 安全风险
3. 缺失测试
4. 破坏现有行为的可能性

不要重写代码。先给 findings，再给我建议下一步。
```

这比“帮我 review 一下”更适合教学，因为它告诉学习者：Plugin 提供能力，任务边界仍然由人定义。

## 18. Plugin、MCP、Skill、Automation 的组合设计

Plugin 经常不是单独使用，而是和其它 Codex 模块组成完整工作流。

### 18.1 PR 巡检组合

```text
Plugin: GitHub 连接能力
Skill: PR review 工作流
Automation: 每天上午检查未处理评论
Review pane: 查看本地 diff
Human: 决定是否提交和推送
```

可用 prompt：

```text
$pr-review
请读取当前 PR 的评论和本地 diff。
输出：
1. 评论按主题分组
2. 哪些评论已经在本地改动中处理
3. 哪些评论仍需人工判断
4. 建议下一次最小修改范围

不要提交，不要推送，不要回复 GitHub 评论。
```

### 18.2 文档漂移组合

```text
Plugin: Google Drive 或内部文档连接
MCP: 官方 API 文档查询
Skill: docs-drift 工作流
Automation: 每周一生成漂移报告
```

可用 prompt：

```text
$docs-drift
请比较项目 README、docs/ 目录和外部设计说明中的关键事实。
只列出不一致点、可能过期的段落和建议更新位置。
不要直接改文档，先给我报告。
```

### 18.3 安全 triage 组合

```text
Plugin: Codex Security 或团队安全插件
Rules: 限制危险命令
Skill: security-triage
Review pane: 人工看 diff
```

可用 prompt：

```text
$security-triage
请检查当前改动是否引入敏感信息泄露、认证绕过、危险依赖或日志暴露。
只基于当前仓库和允许读取的上下文。
把结果分成：需要立刻处理、建议跟进、无法判断。
```

## 19. 插件治理：从个人试用走到团队共享

一门课程如果只教“怎么装”，就会把团队带进风险里。插件治理不是官僚流程，而是让插件从个人尝鲜变成稳定能力。

可以把插件采用拆成三步。

第一步，证明它确实缩短了一个流程，而不是只是看起来新鲜。

```md
# Plugin Adoption Note

Plugin: pr-review-pack
Owner: Engineering Productivity
Primary workflow: PR comment triage and local diff review
First users: frontend team
Expected use: before PR update and after reviewer comments arrive
Human decision points: commit, push, external comment replies
```

这份记录回答的不是"插件好不好"，而是“它服务哪个具体工作流”。如果说不清工作流，先不要推广。

第二步，把工程边界写清楚。

```md
# Engineering Use Notes

Allowed:
- Read PR context
- Summarize comments
- Suggest local fix plan
- Run project tests when user approves

Needs human action:
- Stage files
- Commit
- Push
- Reply to external reviewers

Not for:
- Broad refactors
- Secret handling
- Unreviewed production changes
```

第三步，检查能力面是否扩大。插件可能带来 MCP、外部账号、本地命令和 workspace sharing。采用前至少问清楚：

```text
1. 它会读取哪些系统？
2. 它会不会写文件或写外部系统？
3. 数据会经过哪个 app、connector 或 MCP server？
4. 失败时会留下什么状态？
5. 项目或 workspace 能不能禁用它？
```

禁用示例：

```toml
[plugins."gmail@openai-curated"]
enabled = false
```

这不是"永远不让用"，而是在某些项目、账号或阶段暂时收窄能力面。团队真正需要的是一条可逆路径：先个人试用，再小团队试点，最后共享给 workspace；一旦发现权限、输出质量或责任边界不合适，可以退回上一层。

## 20. 插件排障：按生命周期定位问题

插件出问题时，不要只说“插件坏了”。按生命周期查：

| 症状 | 优先检查 | 解释 |
|------|----------|------|
| 插件目录看不到 | marketplace 是否添加、App 是否重启 | Codex 可能还没发现来源 |
| 插件能看到但不能安装 | 权限、workspace sharing、网络 | 目录可见不等于可安装 |
| 安装后 `@` 找不到 | 新线程、插件是否启用 | 旧线程可能没有刷新能力 |
| 调用后无法读外部数据 | 外部 App 是否登录 | 插件安装不等于账号授权 |
| MCP 工具不可用 | bundled MCP 是否还需配置 | 插件可带 MCP，但认证仍可能独立 |
| 输出很泛 | prompt 没说明来源和范围 | Codex 不知道该用哪个插件 |
| 团队成员表现不一致 | marketplace、版本、账号权限不同 | 先对齐安装来源和权限 |

### 20.1 插件不可见的排查 prompt

```text
我安装或配置了一个 Codex Plugin，但在当前线程里看不到。
请按顺序帮我排查：
1. 插件来源是否应该出现在 App Plugins 页面或 CLI `/plugins`
2. marketplace 路径或配置是否可能没被发现
3. 是否需要重启 Codex 或新建线程
4. 是否是 workspace sharing 或账号权限问题
5. 下一步我应该查看哪个文件或界面
```

### 20.2 插件能用但结果不对的排查 prompt

```text
刚才的插件任务结果不符合预期。
请不要继续调用外部写操作。
先复盘：
1. 你是否真的调用了目标插件
2. 你读取了哪些外部上下文
3. 哪些结论缺少证据
4. prompt 中哪些边界不清楚
5. 下一轮我应该怎样改写任务
```

### 20.3 插件升级后的排查 prompt

```text
插件升级后，同样的任务输出变了。
请帮助我比较：
1. 插件版本或 marketplace 来源是否变化
2. bundled skills 的说明是否变化
3. MCP 或外部 app 权限是否变化
4. 旧 prompt 是否依赖了未说明的默认行为
5. 是否需要把团队使用模板更新
```

## 21. 插件课程里的 12 个训练题

这些训练题不需要真实外部系统也能练，适合作为直播课或自学作业。

1. 给一个真实重复任务，判断它适合普通 prompt、Skill、MCP、Plugin 还是 Automation。
2. 读一个插件说明，列出它可能带来的 Skill、App、MCP 三类能力。
3. 写一个只读 GitHub PR 摘要 prompt。
4. 写一个“插件结果复盘” prompt，让 Codex 解释它用了什么上下文。
5. 设计一个团队插件登记表。
6. 设计一个插件下线流程。
7. 把一个 Skill 升级成 Plugin，并说明升级理由。
8. 给插件 marketplace 写一个 repo 级目录结构。
9. 解释为什么安装插件不等于授权外部账号。
10. 解释为什么插件不能绕过审批和沙盒。
11. 设计一个插件升级前的沟通模板。
12. 写一段新人入职说明，告诉他什么时候该用 `@` 显式调用插件。

## 22. 综合工坊：把课程审查 Skill 打包成 Plugin

这个工坊让学习者理解 Plugin 不是抽象概念，而是把可复用能力交付给团队。

### 22.1 目标

把 `zh-course-review` Skill 打包成一个本地 Plugin，并通过 repo marketplace 暴露给团队。

### 22.2 目录结构

```text
repo-root/
  .agents/
    plugins/
      marketplace.json
  plugins/
    course-authoring-pack/
      .codex-plugin/
        plugin.json
      skills/
        zh-course-review/
          SKILL.md
```

### 22.3 Plugin manifest

```json
{
  "name": "course-authoring-pack",
  "version": "1.0.0",
  "description": "Reusable Codex workflows for Chinese technical course authoring.",
  "skills": "./skills/"
}
```

### 22.4 Marketplace

```json
{
  "name": "course-team",
  "plugins": [
    {
      "name": "course-authoring-pack",
      "source": {
        "source": "local",
        "path": "./plugins/course-authoring-pack"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Documentation"
    }
  ]
}
```

### 22.5 安装和使用

```text
1. 重启 Codex。
2. 打开 App Plugins 页面或 CLI `/plugins`。
3. 找到 course-team marketplace。
4. 安装 course-authoring-pack。
5. 新开线程显式调用 bundled skill。
```

使用：

```text
@course-authoring-pack
请审查 docs/codex/CX-06-Codex-Skills可复用工作流完整指南.md。
只做课程质量和事实边界审查，不修改文件。
```

## 23. Plugin 设计练习：判断是否应该打包

### 23.1 候选能力 A

```text
每天提醒我喝水。
```

判断：不适合 Plugin。更像个人提醒或普通 automation。

### 23.2 候选能力 B

```text
团队每周都要检查 PR 评论、生成风险摘要、附带 GitHub 连接能力和 PR review skill。
```

判断：适合 Plugin。因为它包含可复用 Skill、外部 app 能力和团队分发需求。

### 23.3 候选能力 C

```text
一次性修复 checkout bug。
```

判断：不适合 Plugin。放 prompt 或普通线程。

### 23.4 候选能力 D

```text
公司内部设计规范审查，需要读取 Figma、团队设计术语表和 UI review workflow。
```

判断：可能适合 Plugin。可以 bundle Skill、references 和 Figma 相关能力，但要先评估权限和数据范围。

## 24. Plugin 进阶常见问题

### Q1：安装 Plugin 后为什么旧线程没变化？

旧线程可能没有刷新能力列表。安装、启用或禁用插件后，建议新开线程或重启 Codex。

### Q2：Plugin 可以只包含 Skill 吗？

可以。最小 Plugin 可以只打包一个或多个 Skills。它的价值是分发和安装，而不是一定要连接外部 app。

### Q3：Plugin 和 marketplace 是什么关系？

Plugin 是能力包。Marketplace 是让 Codex 发现和安装这些能力包的目录。

### Q4：团队共享 Plugin 是否等于公开发布？

不是。workspace sharing 可以只在工作区或组织边界内共享，不等于公开发布到公共目录。

### Q5：Plugin 卸载后外部 App 会自动断开吗？

不一定。卸载插件会移除 Codex 中的插件 bundle，但外部 app 连接可能需要在 ChatGPT 或对应服务里单独管理。

### Q6：Plugin 能不能替代 MCP？

不能简单替代。Plugin 可以打包 MCP，也可以只打包 Skill 或 App integration。MCP 是工具协议，Plugin 是分发单位。

## 25. Plugin 安装决策：个人试用、团队试点、组织共享

Plugin 的采用可以分三档，不必每次都拉一堆人开会。

### 25.1 个人试用

只读、低风险、不接真实客户数据、不共享给团队。目标是判断它是否真的解决一个重复流程。

```text
请帮我为这个插件设计一次个人试用任务。
要求：
1. 只读
2. 不写外部系统
3. 不涉及真实客户数据
4. 结束后能判断是否值得团队试点
```

### 25.2 团队试点

当插件开始影响多人工作流时，要写使用模板、owner、推荐场景和下线方式。团队试点看的是流程价值，不是插件本身多新。

### 25.3 组织共享

当插件涉及 workspace sharing、外部账号、bundled MCP 或受管配置时，才进入组织级治理。这个阶段要明确 marketplace 来源、数据边界、禁用路径和升级责任。

## 26. Plugin 作业：设计团队插件目录

```md
# Team Plugin Catalog

## Engineering

- PR Review Pack
- CI Triage Pack

## Documentation

- Docs Drift Pack
- Course Authoring Pack

## Product

- Release Notes Pack
- Spec Review Pack

## Security

- Security Triage Pack
```

要求学生为每个插件写：

```text
- 使用场景
- bundled skills
- 是否需要 external app
- 是否有 MCP
- 默认是否只读
- owner
```

## 27. Plugin 长案例：把一个 PR Review Skill 变成团队插件

Skill 解决“流程可复用”，Plugin 解决“能力可安装、可分发、可治理”。如果团队只有一个仓库，Skill 放在仓库里就够了；如果多个团队都要用同一套 PR review、CI triage、docs drift 流程，就适合进入 Plugin。

假设已经有一个 Skill：

```text
pr-risk-review
用途：审查 PR diff 的行为风险、安全风险、测试缺口和 scope creep。
```

个人阶段可以这样用：

```text
$pr-risk-review
请审查当前 diff，重点看认证、权限和测试覆盖。
```

团队阶段要问的问题变了：

```text
1. 谁维护这个 Skill？
2. 哪些项目默认启用？
3. 是否需要 GitHub connector 或 MCP？
4. 输出是否适合进入 PR 描述？
5. 如何禁用或回滚？
```

一个插件采用说明可以这样写：

```md
# PR Review Pack

## Purpose

Provide reusable PR review workflows for local diff review, PR comment triage, and pre-merge risk checks.

## Bundled Skills

- pr-risk-review
- pr-comment-triage
- pr-description-writer

## Optional Integrations

- GitHub connector for PR context.
- Read-only docs MCP for architecture references.

## Default Behavior

- Read-only review by default.
- No staging, commit, push, or external replies.
- Human decides all Git and GitHub actions.

## Owner

Engineering Productivity
```

试点时不要一上来全 workspace 推广。先选一个团队和一种 PR 类型：

```text
试点范围：
- frontend team
- 只用于 UI bugfix PR
- 只读 review
- 两周后复盘输出质量和噪音
```

试点 prompt：

```text
使用 PR Review Pack 帮我审查当前 UI bugfix PR。

重点：
1. 用户可见行为是否清楚。
2. 是否有无关样式重构。
3. 测试或手测路径是否缺失。
4. PR 描述是否能让 reviewer 快速判断。

不要修改文件。
```

如果试点发现输出太长，不要马上撤掉插件。先改 Skill 或使用模板：

```text
请把 PR Review Pack 的输出压缩成：
1. Blocking
2. Should fix before merge
3. Follow-up

每类最多 3 条。
```

只有当试点证明它能缩短真实流程，再考虑组织共享。Plugin 的目标不是"把能力装满"，而是让团队少手抄、少走偏、少在权限上猜。

## 28. Plugin 下线和回滚：会安装，也要会撤掉

插件治理里最容易被忽略的是下线。一个插件只要能读取外部系统、调用 MCP 或影响多人流程，就必须知道如何停用。

常见下线原因：

```text
- 输出质量下降，误导用户。
- 依赖的外部系统权限变化。
- bundled Skill 过期。
- 插件扩大了不该有的数据访问范围。
- 新版本和团队配置冲突。
```

下线不是删除一切。先判断影响范围：

```text
请帮我写一份 Plugin rollback note。

插件：
PR Review Pack

问题：
新版输出包含大量无关 style comment。

需要回答：
1. 哪些团队正在使用。
2. 是否要禁用整个插件，还是只禁用某个 Skill。
3. 回滚后用户该用哪个替代流程。
4. 需要通知谁。
5. 什么时候重新评估。
```

一个团队通知模板：

```md
# PR Review Pack Temporary Rollback

What changed:
- We are temporarily disabling the latest PR Review Pack update.

Why:
- The new review workflow produces too many non-blocking style comments.

What to use instead:
- Continue using the previous local PR review prompt.
- For high-risk PRs, use manual Review pane checks.

What not to do:
- Do not install unreviewed plugin copies from personal sources.

Next:
- Engineering Productivity will revise the bundled skill and run a small trial again.
```

课程里讲下线很重要，因为它会改变读者对插件的心理模型：插件不是装上就永远存在的"功能"，而是一组可维护、可暂停、可替换的工作流资产。

## 29. Plugin 与 MCP 的组合风险：不要把工具链打包成黑箱

Plugin 可以把 Skills、MCP、Connectors 组合起来，这很强，也容易变成黑箱。团队使用者如果只知道“装这个插件就行”，但不知道它背后会读什么系统，风险就会被包装起来。

引入组合型插件时，至少写清三层：

```text
Skill 层：
- 它会触发什么工作流？
- 输出是什么？
- 是否会修改文件？

MCP 层：
- 它会读取哪些外部系统？
- 哪些 tool 默认启用？
- 是否存在写入 tool？

Connector 层：
- 是否需要 GitHub、Slack、Gmail 或浏览器权限？
- 数据会进入哪个上下文？
- 用户如何撤销授权？
```

一个组合型插件说明：

```md
# Release Notes Pack

## Skills

- release-note-draft
- changelog-risk-review

## MCP / External Reads

- Read-only issue tracker search.
- Read-only GitHub PR metadata.

## Writes

- No external writes.
- Local markdown edits only after user confirms.

## Human Decisions

- Publishing release notes.
- Replying to external comments.
- Tagging releases.
```

如果插件说明不能把这三层讲清楚，就不要先推广。读者要学会一种朴素判断：能力越像“一键完成”，越要拆开看它背后读了什么、写了什么、谁负责。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 能区分Connector、Plugin、Skill、MCP四个概念
- [ ] 安装前检查了来源、能力、权限、数据范围、撤销方式
- [ ] 完成过GitHub连接器的只读试跑
- [ ] 遵循最小权限原则（只给必要权限）
- [ ] 知道如何在App中禁用/卸载连接器或插件
- [ ] 理解Plugin可以包含Skills、MCP、Connectors

**全部勾选后即掌握 Codex 连接器与插件。**

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
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-08 Subagents：App 中的多 Agent 协作](./CX-08-Codex-Subagents多Agent协作完整指南.md)。
