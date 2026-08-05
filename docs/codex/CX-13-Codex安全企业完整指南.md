# CX-13 安全与企业指南：围绕 App 建立权限、审计和合规边界

本篇是 App 主线的安全与企业篇。

主要来源：OpenAI Codex Settings、Config、Rules、Hooks、MCP、Plugins、Automations 官方文档。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时
> - **难度等级**：⭐⭐⭐ 进阶级
> - **更新日期**：2026年6月18日
> - **信息来源**：OpenAI Codex Settings、Config、Rules、Hooks、MCP、Plugins、Automations 官方文档
> - **前置要求**：已完成CX-01至CX-12，熟悉App所有基本功能

---

## 📚 本课学习目标

完成本课学习后，你将能够：

> **2026-06-18 安全口径**：App 26.609 增加 Windows Computer Use per-app controls，Automations 会遵循选定 approval mode；CLI 0.141 强化 PostToolUse blocking、加密凭证、Windows sandbox 和远程执行边界。企业落地时要把 App 权限、CLI profile、Hook 信任、Automation 审批和区域性 Memories / Chronicle 策略分开登记。

1. **理解安全模型总览**：掌握六类风险（敏感文件、危险命令、大量改文件、外部数据、工具调用、后台任务）及各自的控制手段
2. **设置审批与沙盒基线**：为不同场景（只读、日常、陌生仓库、CI、生产）配置合理的审批和沙盒策略
3. **编写有效的Rules**：用Rules拦住危险命令，不把代码风格和测试写在Rules里
4. **评估Hooks风险**：理解Hook会运行真实代码，企业环境必须做代码审查
5. **管理MCP安全**：检查只读、生产访问、联网、审计日志、授权范围
6. **安全使用Plugins和Connectors**：安装和授权分开看，定期审查权限范围
7. **建立企业安全基线**：编写插件/连接器/MCP/Automation的登记表，明确谁能改配置
8. **处理Windows团队特殊注意点**：统一安装路径、防火墙策略、终端配置、执行策略

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：个人开发者（⏱️ 20分钟）

**适合人群**：个人使用Codex，想建立基本安全习惯

**只看这些章节**：

```
✅ 第1-2部分：安全模型 + 审批与沙盒（10分钟）
✅ 第9部分：敏感文件规则（5分钟）
✅ 常见问题FAQ（5分钟）
```

---

### 路径B：企业安全（⏱️ 2-3小时）

**适合人群**：需要给团队设统一安全边界

**学习顺序**：从头到尾所有章节，重点第8部分企业基线

---

## 术语表（进阶必读）

企业安全篇的重点不是"把权限关到最死"，而是把风险分类、控制手段、责任人和审计证据串起来。

| 术语 | 一句话解释 | 在 Codex 里对应什么 |
|---|---|---|
| Least privilege | 最小权限 | sandbox、approval、Connector scope、MCP 工具限制 |
| Defense in depth | 多层防护 | `AGENTS.md` + Settings + Rules + Hooks + Review + CI |
| Blast radius | 误操作影响范围 | workspace、worktree、repo、组织账号、生产系统 |
| Human-in-the-loop | 人在关键点确认 | 审批、Review、PR 合并、生产访问 |
| Audit trail | 可追踪记录 | 线程、终端输出、PR、CI、Hook 日志、MCP 服务日志 |
| Managed requirements | 管理员强制要求 | 组织级 sandbox / approval / hooks / rules / MCP 限制 |
| Trust boundary | 信任边界 | 本机、Cloud、Connector、MCP、插件、外部服务 |
| Incident response | 事故响应 | secret 泄露、误推送、生产写入后的处理流程 |
| Data classification | 数据分级 | 公开、内部、敏感、生产、客户数据 |

一句话：安全不是单个开关，而是一套“分类、限制、记录、复核、响应”的流程。

## 0. Codex 安全架构总览

老金在安全企业篇里把最小权限放前面，因为团队要的是可持续协作，不是一次性跑通。

Codex 安全可以按六条链路看：

```text
输入层：用户提示、AGENTS.md、Skills、插件说明
  -> 上下文层：本地文件、Git diff、PR、外部连接器、MCP
  -> 决策层：模型推理、计划、工具选择
  -> 执行层：文件写入、命令、MCP 工具、外部服务动作
  -> 审查层：Review 面板、PR、CI、人工审批
  -> 治理层：Rules、Hooks、managed requirements、日志和登记表
```

任何一层都可能出问题：

- 输入层可能把 secret 贴进提示。
- 上下文层可能读到不该读的文件。
- 决策层可能误判任务范围。
- 执行层可能跑危险命令。
- 审查层可能被跳过。
- 治理层可能没人维护。

所以企业不能只说“大家小心用”。要把不同风险放到不同控制点上。

### 0.1 威胁模型：Codex 最常见的 8 类风险

| 风险 | 例子 | 控制点 |
|---|---|---|
| 敏感信息泄露 | `.env`、token、客户数据被读出或写入日志 | `AGENTS.md`、sandbox、Rules、Hook 扫描 |
| 危险命令执行 | 递归删除、生产部署、直接推 main | approval、Rules、profiles |
| 范围外改动 | 小 bug 变成大重构 | 任务范围、worktree、Review |
| 外部账号越权 | Connector 读到过多仓库或文档 | OAuth scope、组织策略、登记表 |
| MCP 写生产 | 数据库或内部 API 被写入 | MCP 只读、enabled_tools、审批、审计 |
| 后台任务失控 | Automation 自动提交、无限评论 | 只读起步、停止条件、Triage |
| Cloud 环境误配 | secret 打到日志、agent 阶段联网过宽 | environment、secrets 生命周期、网络 allowlist |
| Hook / Plugin 供应链 | 未审查脚本或插件运行代码 | 来源审查、trust review、managed policy |

### 0.2 风险分级

| 级别 | 判断 | 处理 |
|---|---|---|
| 低 | 只读公开文档、改非关键文档 | 普通 Review |
| 中 | 改业务代码、跑测试、读内部文档 | workspace-write + Review + 测试 |
| 高 | 改权限、依赖、部署、数据库、外部服务 | 计划、审批、worktree、PR review |
| 极高 | 生产写入、secret、组织级配置、自动合并 | 专门审批、审计、最小临时权限、事故预案 |

学习阶段可以简单：低中风险用 App 主线，高风险先停下来做计划，极高风险默认不让 Codex 自动做。

## 1. 安全模型总览

Codex App 安全不是"完全不让它做事"，而是让每类动作有边界：

| 风险 | 控制手段 |
|---|---|
| 读敏感文件 | AGENTS.md、权限、沙盒、Rules |
| 运行危险命令 | 审批、Rules、Hooks |
| 大量改文件 | Worktree、Review、Git |
| 外部数据访问 | Connectors 最小授权 |
| 工具调用风险 | MCP 权限和审计 |
| 后台任务失控 | Automation 只读优先 |

## 2. 审批与沙盒


> **v0.133.0→v0.141.0 权限与审计更新**：permission profiles 已支持列表、继承、managed `requirements.toml`、运行时刷新、named profiles 和更强的 Windows sandbox 集成；后续版本又补强了 cloud-managed config、remote-control grants、personal access token v2、plugin JSON 输出、配置错误展示、`/app` 交接到 Desktop、加密凭证、PostToolUse blocking、远程执行权限路径保留和 Windows sandbox 修复。企业文档里不要只写单一 approval mode，要把 profile、requirements、项目规则、`--profile` 迁移、插件结构化输出和 `codex doctor` 诊断证据一起看。

推荐基线：

| 场景 | 审批 | 沙盒 |
|---|---|---|
| 只读审计 | 不允许写入 | read-only |
| 日常开发 | 危险命令审批 | workspace-write |
| 陌生仓库 | 保守审批 | read-only 起步 |
| CI | 外部隔离 + 最小权限 | 看 runner 环境 |
| 生产数据 | 默认拒绝 | 明确人工授权 |

App 落地时按这个顺序做：

1. App Settings 里使用保守审批。
2. 陌生项目先只读分析。
3. 写入前看文件范围。
4. 写完用 App Review 看 diff。
5. 大任务用分支或 worktree。
6. 自动化、插件、MCP 先只读试跑。

## 3. Rules

Rules 适合硬性限制命令。官方 Rules 通常写在 `rules/*.rules` 文件中，用 `prefix_rule()` 描述命令前缀和决策：

沿用第 3 节的 `rm -rf` rule 示例，不需要重新写一份。练习重点是验证它是否真的生效：让 Codex 解释规则、模拟一个安全命令和一个会被拦截的命令，并确认它不会直接执行危险操作。

上线前用 `codex execpolicy check` 检查规则是否按预期命中。

团队应该用 Rules 拦住：

- 递归删除。
- 生产数据库写操作。
- 直接推送 main。
- 输出 secret 的命令。
- 未经确认的部署命令。

## 4. Hooks

Hooks 是事件脚本。配置入口通常是 `.codex/hooks.json` 或 `.codex/config.toml` 中的 `[hooks]`；脚本文件可以放在 `.codex/hooks/`，但目录本身不是配置入口。Hooks 适合：

- 审计日志。
- 命令前检查。
- 文件写入后自动格式化。
- 提交前策略检查。

风险：

- Hook 本身会运行代码。
- Hook 可以泄露上下文。
- Hook 写错会阻塞开发。

企业环境要对 Hook 做代码审查。

## 5. MCP 安全

MCP 工具可能访问外部系统。检查清单：

- 是否只读？
- 是否访问生产？
- 是否会联网？
- 是否有审计日志？
- 是否需要用户级授权？
- 是否能限定路径 / 数据库 / 表 / 仓库？

默认不要给生产写权限。

## 6. Plugins / Connectors 安全

安装和授权分开看：

| 步骤 | 要问的问题 |
|---|---|
| 安装 Plugin | 它带了什么能力？ |
| 启用 Connector | 它能访问哪些账号数据？ |
| 授权 scope | 是否过大？ |
| 使用外部上下文 | 是否包含敏感信息？ |
| 卸载 | 是否撤销外部授权？ |

## 7. Automations 安全

Automation 默认建议只读：

```text
每天检查测试失败并汇总，不要修改文件。
```

允许写入时必须限制：

- 目录范围。
- 文件类型。
- 分支或 worktree。
- 是否提交。
- 是否通知人工。

## 8. 企业基线


建议最小基线：

```text
AGENTS.md
.codex/config.toml
.codex/rules/default.rules
必要的 hooks
插件和 MCP 白名单
连接器授权说明
自动化任务登记表
```

登记表至少包含：

| 类别 | 必填 |
|---|---|
| Plugin / Connector | 名称、来源、授权 scope、owner、撤销方式 |
| MCP | server 名、访问数据、读写权限、token 存放方式 |
| Automation | 运行频率、目录、权限、输出位置、停止条件 |
| Rules / Hooks | 规则目的、触发条件、维护人、回滚方式 |
| 高风险命令 | 是否允许、谁审批、日志位置 |

团队要明确：

- 谁能改配置。
- 谁能安装插件。
- 哪些 MCP 允许用。
- 哪些目录禁止写。
- 自动化任务谁负责。

### 8.0 企业落地路线图

不要一上来追求“全自动 AI 开发平台”。更稳的路线是四阶段：

| 阶段 | 目标 | 典型动作 |
|---|---|---|
| 第 1 阶段：个人安全习惯 | 不泄露、不乱改、不跳过 Review | `AGENTS.md`、只读起步、Review 面板 |
| 第 2 阶段：团队统一基线 | 同一仓库同一套规则 | 根 `AGENTS.md`、Rules、插件/MCP 登记表 |
| 第 3 阶段：企业治理 | 权限、网络、Hook、MCP 有组织策略 | managed requirements、profiles、白名单 |
| 第 4 阶段：自动化扩展 | 后台任务和 Cloud 可审计可回滚 | Automations、Cloud env、CI、事故演练 |

每一阶段都要先跑通“只读 -> 小范围写入 -> Review -> 回滚”闭环，再进入下一阶段。

### 8.1 v0.133.0 permission profile 落地清单


`v0.133.0` 以后，企业治理应把 permission profiles 当成可审计配置，而不是只靠口头约定：

| 自查项 | 建议做法 |
|---|---|
| profile 列表 | 明确只读、日常开发、CI、应急四类 profile |
| profile 继承 | 共享默认限制，只在子 profile 放必要例外 |
| managed `requirements.toml` | 写清最低工具权限、网络边界、禁止目录和 Windows sandbox 要求 |
| plugin / MCP JSON | 插件、MCP、marketplace 和 CI 报告尽量保留结构化输出 |
| token 与 remote-control | PAT v2、remote-control grants、App handoff 都要有授权来源和撤销路径 |
| runtime refresh | 改 profile 后验证旧线程和新线程的实际生效差异 |
| Windows sandbox | Windows 团队建议单独验证防火墙、PowerShell、工作区写入范围 |

最小治理流程：

1. 安全负责人定义 profiles。
2. 项目维护者在 `AGENTS.md` 写清项目边界。
3. 开发者在 App Settings 中选择团队允许的 profile。
4. 每次大改前记录当前线程状态、权限配置和 Review 证据；App 内入口以当前界面和 `/` 列表为准。
5. PR Review 时确认没有临时切到危险模式。

## 9. 敏感文件

在 `AGENTS.md` 中写：

```markdown
## Safety
- 不读取或修改 `.env*`。
- 不输出 token、cookie、API key。
- 不访问生产数据库，除非任务明确要求且用户确认。
- 不直接推送 main。
```

不要只依赖 `.gitignore`。模型仍可能读到工作区里的文件，关键规则要写清楚。

## 10. Windows 团队额外注意

如果团队主要使用 Windows：

| 项 | 建议 |
|---|---|
| 安装 | 统一说明 Microsoft Store / `winget -s msstore` |
| 防火墙 | 首次启动只允许专用网络，企业策略由管理员配置 |
| 终端 | 说明默认 PowerShell，WSL2 项目要单独配置 |
| 路径 | 教程示例避免只写 macOS/Linux 路径 |
| 执行策略 | PowerShell 脚本运行策略由团队统一约定 |

安全教程不能只按 macOS/Linux 习惯写，否则 Windows 用户会卡在安装、权限和本地通信上。

## 10.1 安全事故处理流程

如果 Codex 相关流程出现安全问题，不要只删聊天记录。按类型处理：

| 事故 | 立即动作 | 后续动作 |
|---|---|---|
| secret 出现在提示、日志或 diff | 立即撤销 / 轮换 secret | 查来源，补 `.gitignore`、AGENTS、Hook 扫描 |
| 误改大量文件 | 停止任务，保存 diff 证据 | 用 Git / Review 撤回，拆小任务重做 |
| 误推远端分支 | 通知团队，锁定 PR 或回滚 commit | 复盘权限和自动 push 规则 |
| MCP 访问了不该访问的数据 | 禁用 server / token | 查服务日志，缩小 scope |
| Automation 反复产生错误副作用 | 暂停 automation | 改 prompt、权限、worktree 和停止条件 |
| Hook 阻塞全员 | 临时禁用或回滚 Hook 配置 | 在测试仓库验证后再恢复 |

### 10.2 企业审计包应该包含什么

一次高风险 Codex 改动，建议保留这些证据：

```text
任务提示
当前权限 / sandbox / profile
涉及文件列表
命令输出或测试日志
Review / PR 评论
MCP / Connector / Cloud 环境说明
最终 diff 和 commit
人工审批记录
```

这些证据不是为了形式主义，而是为了事故后能回答：谁让它做的、它看到了什么、它执行了什么、谁批准了、怎么回滚。

## 11. 课堂工坊：把安全基线落到一个团队仓库

### 案例一：给新仓库建立只读起步规则

目标：让陌生项目先被理解，再允许写入。

1. 在 `AGENTS.md` 写清项目背景、常用命令、禁止读取的文件和验证要求。
2. 在 App Settings 中选择保守审批和只读起步。
3. 新线程发送：

```text
阅读这个项目，只输出技术栈、启动命令、测试命令、敏感文件风险和建议的安全边界。不要修改文件，不要读取 .env*。
```

你应该看到：Codex 能总结项目边界；没有 diff；没有输出任何 token、cookie 或私有账号信息。

### 案例二：用 Rules 拦危险命令

目标：把“不要递归删除”变成可执行的命令策略。

```python
# ~/.codex/rules/default.rules 或受信任项目里的 .codex/rules/default.rules
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "禁止递归删除。需要清理时先列出目标路径并人工确认。",
    match = [
        "rm -rf build",
        "rm -rf ./dist",
    ],
)
```

用规则检查命令确认匹配：

```bash
codex execpolicy check --pretty --rules ~/.codex/rules/default.rules -- rm -rf build
```

你应该看到：规则命中并返回 forbidden。Windows 团队可用同样思路限制 PowerShell 危险命令，具体命令前缀按团队实际脚本写。

### 案例三：插件、MCP、Automation 登记表

目标：让外部能力可追踪、可撤销。

| 类型 | 示例记录 |
|---|---|
| Plugin / Connector | GitHub；来源；repo 范围；owner；撤销入口 |
| MCP | docs-search；只读；token 在环境变量；owner |
| Automation | 每日测试检查；9:00；只读；输出到 Triage；owner |
| Rules / Hooks | 禁止递归删除；维护人；回滚方式 |

你应该看到：每个外部能力都有 owner、权限范围和撤销方式；没有“谁装的、能读什么、怎么关掉”说不清的条目。

## 12. 企业治理包模板

企业落地 Codex，不需要一开始写很厚的制度，但要有一组最小治理文件。

### 12.1 推荐目录

```text
ai-governance/
  codex-usage-policy.md
  codex-permission-profiles.md
  codex-mcp-registry.md
  codex-plugin-registry.md
  codex-automation-registry.md
  codex-incident-response.md
  codex-review-guidance.md
```

这些文件可以放在内部知识库，也可以放在团队配置仓库。关键是它们要被维护，而不是写完没人看。

### 12.2 `codex-usage-policy.md`

```markdown
# Codex Usage Policy

## Allowed By Default
- Read repository source code in approved workspaces.
- Modify files inside assigned task scope.
- Run project test, lint, and build commands.
- Use approved read-only MCP servers.

## Requires Explicit Human Approval
- Push, merge, release, deploy.
- Modify dependencies, lockfiles, database migrations.
- Use external service write actions.
- Run networked commands outside allowlisted domains.

## Not Allowed
- Read or print secrets.
- Access production customer data.
- Auto-merge PRs.
- Store credentials in AGENTS.md, Skill, MCP config, or prompts.
```

### 12.3 `codex-permission-profiles.md`

| Profile | 用途 | Sandbox | Approval | 备注 |
|---|---|---|---|---|
| read-only | 审计、学习、陌生仓库 | read-only | on-request | 默认入口 |
| daily-dev | 日常小改 | workspace-write | on-request | 允许测试和小范围写入 |
| review-only | PR 审查 | read-only | on-request | 不写文件 |
| automation-readonly | 后台摘要 | read-only | never 或组织允许项 | 不产生 diff |
| emergency | 事故处理 | 受控临时配置 | 手动审批 | 有时间限制和审计 |

profile 名称要让普通开发者看得懂，不要叫 `profile-1`、`dev2` 这种无法判断风险的名字。

### 12.4 `codex-mcp-registry.md`

| Server | 来源 | 数据范围 | 权限 | Token | Owner | 审计 | 撤销 |
|---|---|---|---|---|---|---|---|
| docs-search | 官方 / 内部 | 公开和内部文档 | 只读 | env var | Docs team | 线程 + server log | disable server |
| github-tools | 组织 | 指定 repo | 只读 + PR 评论需审批 | OAuth | Platform | GitHub audit | revoke app |
| db-schema | 内部 | 测试库 schema | 只读 | secret | Data team | DB audit | rotate token |

登记表要把“生产写权限”作为例外，而不是默认。

### 12.5 `codex-automation-registry.md`

| Automation | 类型 | 频率 | 项目 | 权限 | 输出 | Owner | 停止条件 |
|---|---|---|---|---|---|---|---|
| daily-test-report | standalone | 工作日 9:00 | web | read-only | Triage | QA | 连续 5 天无问题可降频 |
| docs-drift | standalone | 每周一 | docs | read-only | Triage | Docs | release 后重评 |
| pr-followup | thread | 30 分钟 | PR 线程 | read-only | thread | Reviewer | CI 通过或连续 6 次无变化 |

### 12.6 事故演练

每季度至少演练一次：

1. 假设 secret 出现在 Codex 线程或 PR diff。
2. 找到泄露位置和传播范围。
3. 轮换 secret。
4. 更新 `AGENTS.md`、Rules 或 Hook。
5. 记录复盘：为什么发生、以后怎么发现更早。

安全体系如果没有演练，真正出事时大家会只会删消息、改历史，而忘了轮换和审计。

## 常见问题

### Q1：可以彻底跳过审批和沙盒吗？

只在外部已经隔离的一次性环境中考虑。日常 App 使用不建议。

### Q2：企业应该先管什么？

先管插件、连接器、MCP、自动化和危险命令。它们的外部影响最大。

### Q3：安全规则放 AGENTS.md 还是 Rules？

项目事实和说明放 AGENTS.md；硬性命令策略放 Rules；事件脚本放 Hooks。

### Q4：企业能不能直接开放 full access 提高效率？

不建议作为默认。full access 只适合外部已经隔离、可回滚、任务范围明确的一次性环境。日常开发更适合 workspace-write、on-request、Rules 和 Review。

### Q5：MCP 和 Connector 谁风险更大？

看具体权限。Connector 可能带账号级数据范围，MCP 可能带工具级读写能力。两者都要登记来源、scope、owner、撤销方式和审计日志。

### Q6：Hooks 是不是企业安全必需？

不是第一步。先有 `AGENTS.md`、Settings、Rules、Review 和 CI，再用 Hooks 做审计、命令检查或自动校验。Hook 自身也是代码，也要审查。

### Q7：怎么判断一个自动化任务能不能允许写文件？

看四点：是否只改低风险目录、是否有 worktree 隔离、是否有停止条件、是否有人 Review。四点缺一，先只读报告。

### Q8：Cloud 比本地更安全吗？

不是绝对。Cloud 有隔离和可复现优势，但也有 environment、secret、网络和远程仓库权限风险。安全来自正确配置和 Review，不来自“云端”这个词本身。

---

## 13. 企业威胁模型：先看风险入口，再谈效率

Codex 的安全不是单点功能，而是一组入口的组合：本地文件、命令、MCP、Plugins、Automations、Cloud、GitHub、Review、Subagents。企业课要先让管理者看到风险来自哪里。

| 风险入口 | 典型风险 | 主要控制手段 |
|----------|----------|--------------|
| 本地文件 | 误读或误改敏感文件 | sandbox、permissions、AGENTS.md |
| Shell 命令 | 删除、发布、外部写入 | approvals、Rules、Hooks |
| MCP | 外部数据和工具扩大能力面 | allowlist、tool approval |
| Plugins | 外部账号和 bundled tools | 插件治理、禁用、共享策略 |
| Automations | 后台无人值守执行 | read-only、worktree、Triage |
| Cloud | secrets、网络、远端环境差异 | setup 边界、环境变量、Review |
| GitHub/PR | 评论、推送、合并风险 | gh auth、Review、人工合并 |
| Subagents | 并行扩大执行面 | 文件所有权、权限继承 |

### 13.1 企业安全的第一原则

```text
默认让 Codex 在最小边界内工作。
需要扩大能力时，要能说明：
1. 扩大了什么能力
2. 为什么需要
3. 如何回滚
4. 人在哪里审查结果
```

## 14. 数据分类：不是所有仓库都能用同一套权限

企业里最常见的错误是“一套配置打天下”。更好的做法是先按数据和业务风险分层。

| 项目类型 | 默认策略 |
|----------|----------|
| 开源课程、公开文档 | workspace write，可接只读文档 MCP |
| 内部普通业务仓库 | workspace write + Rules |
| 涉及客户数据 | read-only 起步，禁止生产数据 |
| 支付、认证、权限模块 | 定向任务 + Review + 高审批 |
| 基础设施脚本 | 严格 Rules，限制外部写操作 |
| 生产配置仓库 | 默认只读，人工变更流程 |

### 14.1 敏感数据提示写进 `AGENTS.md`

```md
## Sensitive Data

- Do not read or modify `.env*` files.
- Do not use production customer data for tests.
- Do not call production APIs from local tasks.
- Ask before changing authentication, billing, or permission logic.
```

### 14.2 用 permissions 拦敏感文件

```toml
[permissions.project-edit]
extends = ":workspace"

[permissions.project-edit.filesystem.":workspace_roots"]
"**/.env" = "deny"
"**/.env.*" = "deny"
"secrets/**" = "deny"
"src/generated/**" = "read"
```

## 15. 审批策略：人不需要批准一切，但要批准关键动作

审批不是为了拖慢工作，而是为了把风险动作变成人的判断。

### 15.1 应该默认允许的动作

```text
- 读取项目文件。
- 运行只读 Git 命令。
- 搜索代码。
- 运行快速本地测试。
- 修改明确范围内的普通代码或文档。
```

### 15.2 应该 prompt 的动作

```text
- 安装依赖。
- 修改锁文件。
- 运行迁移。
- 修改权限、认证、支付相关代码。
- 调用外部写操作。
- 访问项目外目录。
```

### 15.3 应该拒绝或禁止的动作

```text
- 未确认的 force push。
- 未确认的 publish。
- 删除项目外目录。
- 打印或提交 secrets。
- 后台自动化直接操作生产系统。
```

### 15.4 Rules 示例：发布和推送

```python
def prefix_rule(argv):
    if len(argv) >= 2 and argv[0] == "npm" and argv[1] == "publish":
        return "prompt"
    if len(argv) >= 2 and argv[0] == "git" and argv[1] == "push":
        return "prompt"
    if len(argv) >= 3 and argv[0] == "git" and argv[1] == "push" and "--force" in argv:
        return "deny"
    return None
```

## 16. MCP 企业治理

MCP 是企业引入 Codex 后最需要治理的能力之一，因为它把 Codex 连接到外部工具和数据。

### 16.1 MCP 登记表

```md
# MCP Registry

## Server

Name:
Owner:
Transport: STDIO / Streamable HTTP
Data accessed:
Tools exposed:
Write tools:
Authentication:
Default approval mode:
Allowed projects:
Review cadence:
```

### 16.2 MCP allowlist 思路

企业可以通过受管配置限制哪些 MCP server 可启用。课程里不用让新人写完整企业配置，但要理解原则：

```text
- server 名称和身份都要匹配。
- stdio 看 command。
- HTTP 看 url。
- 空 allowlist 可以表示不允许任何 MCP。
```

### 16.3 MCP 安全 prompt

```text
请从企业安全角度评估这个 MCP server 是否适合接入 Codex。
关注：
1. 它读取什么数据
2. 它是否有写工具
3. 它需要什么认证
4. 哪些工具应该 disabled
5. 默认 approval mode 应该是什么
```

## 17. Plugin 企业治理

Plugin 可能带 Skill、App integration、MCP server 和 lifecycle config。它不是普通素材包。

### 17.1 Plugin 登记表

```md
# Plugin Registry

Plugin:
Marketplace:
Owner:
Purpose:
Bundled skills:
Bundled apps:
Bundled MCP servers:
External services:
Authentication timing:
Allowed teams:
Disable path:
Upgrade owner:
```

### 17.2 Workspace sharing 策略

```text
- 个人测试插件先不分享。
- 团队试点插件只分享给试点组。
- 涉及外部账号的插件需要说明数据范围。
- 安全敏感插件由指定 owner 维护。
- 不再使用的插件要 disable 或 uninstall。
```

### 17.3 禁用示例

```toml
[plugins."gmail@openai-curated"]
enabled = false
```

## 18. Automation 企业治理

Automations 是无人值守执行，所以企业里要更保守。

### 18.1 自动化分级

| 级别 | 行为 | 管理方式 |
|------|------|----------|
| A | 只读摘要 | 允许个人创建 |
| B | 只读 + 外部插件 | 需要登记数据来源 |
| C | worktree 中写文件 | 需要 Review |
| D | 外部系统写操作 | 默认不开放 |
| E | 生产系统操作 | 不适合作为普通 Codex automation |

### 18.2 Automation 登记表

```md
# Automation Registry

Name:
Owner:
Schedule:
Projects:
Run mode: local / worktree
Permissions:
Plugins / MCP:
Writes files:
External writes:
Triage owner:
Stop condition:
```

### 18.3 自动化默认 prompt

```text
这是企业环境中的后台自动化。
默认只读。
如果发现需要写文件，请生成建议，不要直接修改。
如果需要外部写操作，请请求人工处理。
没有发现时归档，避免制造噪音。
```

## 19. Cloud 企业治理

Cloud 的治理重点是环境、secrets、网络和 PR 回流。

### 19.1 Cloud 环境记录

```md
# Codex Cloud Environment

Environment:
Owner:
Repos:
Setup script:
Maintenance script:
Environment variables:
Secrets used in setup:
Agent internet access:
Cache policy:
Allowed task types:
Review path:
```

### 19.2 Secret 边界

```text
- Secrets 只在 setup 阶段可用。
- Agent 阶段需要的普通配置用 environment variables。
- 不在 setup 日志打印 secret。
- 不把 secret 放进 prompt。
- 私有依赖安装后，不让 agent 继续持有安装密钥。
```

### 19.3 Cloud PR 策略

```text
- Cloud 可以生成 diff 或 PR。
- 合并前必须经过 Review。
- Cloud 通过测试不等于业务风险为零。
- 本地无法复现的环境差异要写进 PR。
```

## 20. Subagents 企业治理

Subagents 会增加并行度，也会增加协调成本。

### 20.1 默认规则

```text
- 只有明确要求并行时才使用。
- 读多写少优先。
- 写入前必须有文件所有权。
- reviewer agent 默认只读。
- 不鼓励递归委派。
```

### 20.2 企业 subagent prompt

```text
Use subagents only for read-only review.
Spawn one agent for security, one for tests, and one for maintainability.
Do not edit files.
Wait for all agents and merge findings in the main thread.
```

### 20.3 写入型并行的限制

```text
如果要并行写入：
- 每个 agent 必须有 disjoint file ownership。
- 主线程必须合并结果。
- 不允许 worker 自己提交或推送。
- 完成后用 Review 面板检查所有 diff。
```

## 21. 审计包：出了问题能回看

企业落地 Codex 时，审计包不是为了形式，而是为了能回答“发生了什么”。

### 21.1 单次任务审计

```md
# Codex Task Audit

Thread:
Project:
User:
Goal:
Files changed:
Commands run:
MCP / Plugins used:
Approvals granted:
Review result:
Final human action:
```

### 21.2 月度治理复盘

```md
# Monthly Codex Governance Review

## Usage

- Active projects
- Common task types
- Automations running
- MCP servers enabled
- Plugins installed

## Risks

- Repeated approval escalations
- Failed automations
- Over-broad permissions
- Unused plugins or MCP servers

## Changes

- Config updates
- New rules
- Retired automations
- Training topics for next month
```

## 22. 事故响应：不要让 Codex 继续扩大现场

如果怀疑 Codex 造成了错误修改、密钥暴露或外部系统误操作，先停止扩大。

### 22.1 第一反应

```text
1. 停止当前线程继续执行。
2. 不要让 Codex 自动修复事故。
3. 保存 thread、terminal、diff、PR、automation run。
4. 确认是否有 secrets 暴露。
5. 如果涉及外部系统，查看外部审计日志。
```

### 22.2 事故分析 prompt

```text
请帮助我做只读事故复盘。
不要修改文件，不要运行外部写操作。
基于当前 diff、终端输出和线程内容，整理：
1. 发生了什么
2. 哪些文件或系统受影响
3. 哪些动作需要人工立即处理
4. 后续如何调整 AGENTS.md、Rules、MCP、Plugin 或 Automation
```

## 23. 企业推广路线：不要第一天全员全功能

### 第 1 阶段：个人试点

```text
- 只用 App。
- 只读分析和文档小改。
- 不接外部生产系统。
- 收集 prompt 和 Review 经验。
```

### 第 2 阶段：团队仓库

```text
- 写根目录 AGENTS.md。
- 建 Rules 拦高风险命令。
- 接只读 MCP。
- 训练 Review 面板。
```

### 第 3 阶段：外部能力

```text
- 引入 GitHub、文档、浏览器能力。
- 插件登记。
- 自动化只读试点。
- Cloud 用于明确 CI 修复。
```

### 第 4 阶段：治理固化

```text
- 受管配置。
- MCP allowlist。
- Plugin 共享策略。
- Automation 分级。
- 月度审计和培训。
```

## 24. 企业分层训练路径

| 学习对象 | 第一课 | 第二课 | 第三课 |
|------|--------|--------|--------|
| 工程师 | App + Review | AGENTS.md + Rules | MCP + Skills |
| Tech Lead | 任务拆分 | Subagents | PR/Cloud |
| 安全 | Permissions | MCP/Plugin governance | Incident response |
| IT | 安装部署 | 认证和更新 | 受管配置 |
| 产品 | App 任务描述 | diff 用户影响 | Automation 摘要 |
| 文档 | Skills | docs drift | Review |

这能让企业培训不是"一场大课讲所有功能"，而是按实际工作内容分批吸收。

## 25. 综合工坊：给一个 20 人团队制定 Codex 使用基线

### 25.1 背景

团队有 20 人，包含前端、后端、QA、产品和安全。准备在两个业务仓库试点 Codex App。

### 25.2 第一步：分层目标

```text
第 1 周：只读分析、README 小改、Review 面板训练。
第 2 周：AGENTS.md、Rules、PR review prompt。
第 3 周：只读 MCP、Skills。
第 4 周：Automation 和 Cloud 小范围试点。
```

### 25.3 第二步：默认权限

```text
- 默认 workspace。
- 敏感文件 deny。
- full access 不作为默认教学配置。
- 自动化默认只读或 worktree。
- 外部写操作需要人决定。
```

### 25.4 第三步：共享模板

```md
# Team Codex Baseline

## Required

- Root AGENTS.md
- Project command list
- Sensitive file notes
- PR review prompt
- Automation owner if any

## Recommended

- docs-drift Skill
- read-only docs MCP
- GitHub CLI login for PR context
```

### 25.5 第四步：试点评审会

```text
每周 30 分钟：
- 哪些任务节省时间
- 哪些 prompt 容易跑偏
- 哪些权限请求过多
- 哪些 MCP/Plugin 需要登记
- 哪些自动化该停
```

## 26. 企业安全演练题

### 26.1 演练 A：Codex 误改 `.env.example`

问题：

```text
它不是真实 secret，但可能误导部署。
```

处理：

```text
1. Review diff。
2. 判断是否应保留。
3. 在 AGENTS.md 写环境文件规则。
4. permissions 中 deny `.env*` 或收窄。
```

### 26.2 演练 B：Automation 每天制造低价值提醒

处理：

```text
1. 降频或停用。
2. 改 prompt：无发现自动归档。
3. 增加 Triage owner。
4. 一周后复查。
```

### 26.3 演练 C：MCP 暴露了写生产数据工具

处理：

```text
1. 立即 disabled 写工具。
2. 调整 enabled_tools allowlist。
3. 重新登记 MCP。
4. 新建测试环境 server。
5. 通知使用者不要在生产数据上练习。
```

## 27. 企业进阶常见问题

### Q1：企业能不能禁止所有 MCP？

可以，但不一定最佳。更实际的是 allowlist：允许可信、必要、只读或受控的 MCP，禁用未知和高风险工具。

### Q2：安全团队是不是应该审批所有 Codex 任务？

不现实。安全团队应该定义边界、模板和高风险审批点。普通低风险任务由工程流程和 Review 承接。

### Q3：Codex 是否适合处理生产事故？

可以辅助只读复盘、日志总结、修复建议。但生产操作、回滚、封禁、发布仍应走既有 incident 流程。

### Q4：企业培训最容易失败在哪里？

一开始就讲太多高级功能，而没有让每个人完成 App、Review、AGENTS.md 的基本闭环。

## 28. 企业责任链：别让“大家都知道”变成没人负责

企业落地 Codex 最怕一种含糊状态：工程同学以为平台会管，平台以为安全会批，安全以为业务自己知道风险。最后出了问题，大家都能解释为什么自己没有错，但没人能说清楚流程应该怎么走。

把责任链写进课程，比单纯讲“要治理”更有用。下面是一套可以直接改成内部政策的写法。

```text
`AGENTS.md`
- 由项目技术负责人维护。
- 工程负责人确认它符合团队开发流程。
- 安全团队只参与敏感目录、权限边界和高风险命令部分。
- 全体开发者需要知道它是项目内 Codex 的默认工作说明。

Rules
- 由平台或工程效能团队维护。
- 安全团队确认高风险命令限制。
- 项目团队反馈误拦截和漏拦截。
- 规则变更要能追踪原因。

MCP allowlist
- 由平台团队维护清单。
- 数据 owner 判断哪些系统可以读、哪些绝不能写。
- 安全团队确认授权范围和审计方式。
- 开发者只使用已登记的 server 和 tool。

Plugin sharing
- 插件 owner 说明插件解决什么流程、需要哪些权限。
- workspace admin 控制共享范围。
- 安全团队只在插件读取外部系统、扩大权限或处理敏感数据时介入。
- 使用者要知道插件可以禁用、移除和替换。

Automation
- 创建者负责 prompt、频率和输出质量。
- 团队负责人判断结果是否进入真实工作流。
- 涉及外部系统、写文件或无人值守执行时再拉安全检查。
- 团队成员需要知道输出在哪里、谁处理、何时停用。

Cloud environment
- 平台团队维护 setup script、runtime、cache 和环境变量。
- 工程负责人判断哪些任务适合远端执行。
- 安全团队确认 secrets、联网和外部 API 边界。
- 本地用户负责回收 diff 和最终 Review。

Incident response
- 事故负责人统一调度。
- 业务 owner 决定影响和优先级。
- 安全和工程提供只读分析、修复建议和复盘材料。
- 回滚、封禁、发布、生产操作仍走既有 incident 流程。
```

这段责任链的价值不是增加流程，而是避免“没人拥有风险”。真正有效的企业课程应该让每个人知道：我在什么情况下可以自己做，什么情况下要找谁，什么动作永远不能交给 unattended agent。

## 29. 企业作业：写一份 Codex 使用政策

```md
# Codex Usage Policy

## Allowed by Default

- Read project files.
- Run documented test commands.
- Edit files in scoped tasks.
- Use approved read-only MCP servers.

## Requires Human Decision

- Git push.
- Publishing packages.
- Database migrations.
- External system writes.
- Expanding sandbox permissions.

## Not Allowed

- Pasting secrets into prompts.
- Using production customer data for practice.
- Running unregistered high-risk MCP tools.
- Letting unattended automations modify production systems.
```

要求学生根据自己团队补充具体例子。

## 30. 企业安全演练：Codex 读到了不该读的文件怎么办

安全课程不能只讲“不要粘贴密钥”。更真实的演练是：Codex 在一个任务里读到了不该进入上下文的文件，团队如何停止、判断、修复流程。

场景：

```text
开发者让 Codex 排查登录失败。
Codex 在探索时读取了包含测试 token 的本地配置文件。
文件没有提交到 Git，但内容出现在了线程摘要里。
```

第一步，停止继续扩散：

```text
请停止当前任务。
不要继续读取文件，不要总结敏感内容。
只回答：
1. 哪个文件可能包含敏感信息。
2. 这个文件是否需要从后续上下文中避免引用。
3. 我应该联系谁处理。
```

第二步，人来判断敏感级别：

```text
判断问题：
- 这是生产 secret、测试 token，还是无效样例？
- 是否已经进入远端服务、PR、日志或公开仓库？
- token 是否需要轮换？
- 现有 deny 规则为什么没挡住？
```

第三步，修流程，不是只怪人：

```md
# Sensitive File Follow-up

## What happened

Codex read a local config file while investigating auth failure.

## Immediate action

- Stop the thread.
- Rotate affected token if needed.
- Remove sensitive content from any draft docs or PR text.

## Process fix

- Add sensitive file pattern to project instructions.
- Add deny rule or permission boundary where supported.
- Update onboarding docs to explain where local secrets live.

## Future prompt pattern

When investigating auth, first list candidate files.
Do not read `.env`, local credential files, or token dumps.
```

这个演练要让团队知道：事故响应不是“以后小心点”。真正有用的是把敏感文件模式、权限边界、默认 prompt 和培训材料都修掉。

## 31. 企业例外流程：什么时候可以临时放宽权限

企业治理不能只有禁止。现实中会有例外：某个迁移任务需要写多个目录，某个 Cloud setup 需要联网安装依赖，某个 MCP 需要读取内部系统。关键是例外要有边界和结束时间。

一个例外申请模板：

```md
# Codex Permission Exception

## Task

What needs to be done:

## Why default permissions are not enough

...

## Temporary access requested

- Files/directories:
- Commands:
- Network or external systems:
- Duration:

## Not allowed even during exception

- ...

## Review after task

- Diff review owner:
- Commands to run:
- How to return to default:
```

例外 prompt：

```text
这个任务需要临时扩大文件写入范围。

请先只读检查：
1. 为什么默认范围不够。
2. 最小需要扩大到哪些目录。
3. 哪些目录仍然禁止。
4. 任务完成后如何回到默认权限。

不要开始修改。
```

例外结束后要收回：

```text
请生成本次权限例外复盘。

输出：
1. 实际使用了哪些额外权限。
2. 有没有访问未预期文件。
3. 哪些改动需要人工 Review。
4. 是否应把例外变成正式流程，还是保持一次性。
```

治理的目标不是让所有人每次都等审批，而是把“临时放宽”从模糊口头决定变成可回看的任务边界。

## 32. 企业推广失败案例：第一天全员全功能为什么会翻车

很多企业推广 Codex 的失败，不是因为工具不好，而是第一天就把所有功能同时打开：

```text
- App 本地写代码。
- MCP 接内部系统。
- Plugins 接外部应用。
- Automations 后台运行。
- Cloud 远端执行。
- Subagents 并行任务。
```

学习者还没建立 Review 和权限意识，就已经面对一整套能力面。更稳的推进方式是按风险递增。

第一周：

```text
- App 本地只读分析。
- 小范围 README 或测试修改。
- Review 面板训练。
- 不接外部系统。
```

第二周：

```text
- 写项目 `AGENTS.md`。
- 引入保守权限 profile。
- 练习 `/plan` 和 `/review`。
- PR 描述和风险说明。
```

第三周：

```text
- 只读 MCP 试点。
- 一个团队 Skill。
- 一个插件个人试用。
- 明确禁用和撤销路径。
```

第四周：

```text
- 只读 Automation。
- Cloud 处理明确 CI 失败。
- 企业责任链和例外流程。
```

推广 prompt：

```text
请为我们团队设计 4 周 Codex 试点计划。

团队背景：
- 12 名工程师。
- 两个 Node 项目。
- 已有 GitHub PR 流程。
- 还没有统一 AI 使用规范。

要求：
1. 第 1 周只做低风险本地任务。
2. 第 2 周加入 AGENTS.md 和 Review。
3. 第 3 周试点只读 MCP 和 Skill。
4. 第 4 周再评估 Automation 和 Cloud。
5. 每周都要有可以停止或回退的条件。
```

这类推广计划比“功能培训大课”有效得多。企业落地不是让每个人立刻掌握所有功能，而是让团队在每个阶段都有清楚边界。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解六类风险及各自的控制手段
- [ ] App使用保守审批基线
- [ ] 陌生项目先只读分析
- [ ] 知道Rules适合硬性命令限制，不适合写代码风格
- [ ] 理解Hook的风险（运行真实代码、可泄露上下文）
- [ ] MCP默认不给生产写权限
- [ ] 插件安装和授权分开看
- [ ] 团队有插件/连接器/MCP/Automation登记表

**全部勾选后即掌握 Codex 安全与企业基线。**

---

## 附录

### A. 安全检查速查

| 风险 | 控制手段 |
|------|---------|
| 读敏感文件 | AGENTS.md、权限、沙盒 |
| 运行危险命令 | 审批、Rules、Hooks |
| 大量改文件 | Worktree、Review、Git |
| 外部数据访问 | Connectors最小授权 |
| 工具调用风险 | MCP权限和审计 |
| 后台任务失控 | Automation只读优先 |

### B. 企业最小基线

```text
AGENTS.md                    # 项目规则
.codex/config.toml           # 团队配置
.codex/rules/default.rules   # 命令策略
插件/MCP/自动化登记表         # 资产管理
```

### C. 推荐学习资源

- **Codex Security 官方文档**：https://developers.openai.com/codex/security
- **本系列上一篇**：[CX-12 CLI 辅助](./CX-12-Codex-CLI辅助完整指南.md)
- **本系列下一篇**：[CX-14 Codex vs Claude Code](./CX-14-Codex与Claude-Code对比指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-14 Codex 与 Claude Code 对比](./CX-14-Codex与Claude-Code对比指南.md)。
