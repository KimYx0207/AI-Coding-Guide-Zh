# CX-04 项目指令、配置、权限与沙盒：让 App 知道怎么安全工作


本篇是 App 主线中的项目指令、权限与安全配置篇。

主要来源：OpenAI Codex Config、Rules、Hooks、Settings、CLI 官方文档。

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
> - **信息来源**：OpenAI Codex Config、Rules、Hooks、Settings、CLI 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md) 和 [CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-in-app-browser.webp" alt="Codex App 官方内置浏览器与页面反馈界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **编写AGENTS.md**：用项目级指令文件告诉Codex项目规则、命令、风格和禁止事项
2. **掌握多层指令结构**：理解根目录和子目录AGENTS.md的层级关系
3. **理解App权限入口**：通过Settings、审批提示、`/`命令列表管理权限
4. **区分沙盒模式**：清楚read-only、workspace-write、danger-full-access各自的含义
5. **了解config.toml的作用**：知道什么时候需要它，什么时候App Settings就够了
6. **理解Rules和Hooks**：区分命令策略（Rules）和事件脚本（Hooks），知道各自适合什么
7. **建立项目安全基线**：为个人和团队项目配置最小权限基线
8. **验收配置改动**：每次改完配置后能正确验证是否生效

---

## 先做一个15分钟实操：写出第一份 `AGENTS.md`

这一章会讲权限、沙盒、Rules 和 Hooks，但 App 用户最先应该做的是 `AGENTS.md`。它决定 Codex 打开项目后先理解哪些规则。

### 第一步：让 Codex 只读分析项目

在 Codex App 当前项目线程里输入：

```text
Read this project. Report:
1. what this project does
2. the install command
3. the test command
4. the main source and docs directories
5. files or directories that should not be changed casually

Do not modify files.
```

这一步只收集项目事实，不让 Codex 写文件。

### 第二步：创建最小可用的 `AGENTS.md`

在项目根目录创建 `AGENTS.md`：

```markdown
# AGENTS.md

这份文件约束 Codex 在本项目里的工作方式，用来减少常见的 AI 编程失误。你可以在此基础上继续补充项目专属规则。

参考来源：https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md

取舍说明：这些规则更偏向谨慎和可验证，而不是最快完成。遇到很小的简单任务时，可以按实际情况简化流程。

## 项目背景

开始修改前，先阅读 README、配置文件和目录结构，确认项目目标、技术栈和关键目录；不要凭经验猜。

## 常用命令

只使用本项目已经声明的命令。优先从 README、`package.json` scripts、Makefile、`pyproject.toml`、`Cargo.toml`、CI 配置中确认。

不要把示例命令写成项目事实；没有确认过的命令不要写进本文件，也不要留下占位文本。

## 1. 写代码前先想清楚

不要假装已经理解，也不要把不确定性藏起来。该说清楚的地方先说清楚。

开始实现前：

- 明确写出你的假设；不确定就问。
- 如果需求存在多种理解，把几种理解列出来，不要悄悄选一个。
- 如果有更简单的做法，要主动说明。
- 该反对时要反对；发现需求不清楚，就停下来指出哪里不清楚。

## 2. 简单优先

只写解决当前问题所需的最少代码，不做猜测式扩展。

- 不添加用户没有要求的功能。
- 不为只用一次的代码设计抽象层。
- 不加入没有被要求的灵活性、配置项或扩展点。
- 不为不可能出现的场景堆错误处理。
- 如果 200 行能改成 50 行，就回头简化。

自检问题：资深工程师看到这段实现，会不会觉得过度设计？如果会，就删减。

## 3. 外科手术式修改

只碰必须修改的地方。只清理自己造成的问题。

编辑已有代码时：

- 不顺手“优化”旁边的代码、注释或格式。
- 不重构没有坏的部分。
- 匹配项目现有风格，即使你个人会用另一种写法。
- 发现无关的废代码可以提一句，不要直接删除。

如果你的改动制造了无用内容：

- 删除由本次改动造成的无用 import、变量、函数。
- 不删除本来就存在的死代码，除非任务明确要求。

检查标准：每一行改动都应该能追溯到用户这次请求。

## 4. 目标驱动执行

把任务转成可验证的目标，然后循环到验证完成。

示例：

- “加校验” -> “先写非法输入测试，再让测试通过”
- “修 bug” -> “先写复现 bug 的测试，再修到测试通过”
- “重构 X” -> “重构前后都确认测试通过”

多步骤任务先写简短计划：

```text
1. [步骤] -> 验证：[检查方式]
2. [步骤] -> 验证：[检查方式]
3. [步骤] -> 验证：[检查方式]
```

清晰的成功标准能让你独立推进；含糊的标准，比如“让它能用”，会导致反复追问。

## 安全边界

- 不读取、打印或提交 `.env*`、密钥、Token、证书等敏感信息。
- 不编辑生成文件、构建产物、锁文件，除非任务明确要求。
- 涉及依赖、权限、脚本、部署配置的变化，先说明理由再改。

## 验证要求

- 改源码后运行相关测试、lint 或 build。
- 如果验证命令不存在、失败或耗时过长，要写清楚原因和已做的替代检查。
- 最终回复说明改了哪些文件、验证了什么、还剩什么风险。

## 这些规则生效时应该看到

- diff 里无关改动更少。
- 因为过度复杂而返工的次数更少。
- 澄清问题发生在动手前，而不是出错之后。
- 每次修改都有明确验证方式。
```

创建正式 `AGENTS.md` 前，先让 Codex 根据第一步的分析输出完整版本。命令必须来自项目文件或你亲自确认；没有确认的命令整行删除，不要留空、不要写占位。

### 第三步：验证 Codex 是否读到了规则

开启一个新线程，输入：

```text
Summarize the project rules from AGENTS.md.
Then tell me how you would verify a source-code change in this project.
Do not modify files.
```

如果 Codex 能复述项目规则、测试命令和禁止事项，说明 `AGENTS.md` 已经成为项目上下文的一部分。

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想让Codex知道项目规则

**只看这些章节**：

```
✅ 先做一个15分钟实操：写出第一份 AGENTS.md
✅ 第1部分：App用户先写AGENTS.md（5分钟）
✅ 第4部分：App中的权限入口（5分钟）
✅ 第5部分：沙盒模式（5分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握权限和安全配置

**学习顺序**：从头到尾所有章节

---

### 路径C：企业配置（⏱️ 20分钟）

**适合人群**：需要给团队设统一安全边界

**直接跳到**：

```
🔧 第6-7部分：config.toml + Rules
🔧 第10部分：App项目基线
```

---

## 1. App 用户先写 `AGENTS.md`

`AGENTS.md` 是项目级指令文件。App 打开项目后，会把它作为重要上下文。

它应该回答：

- 项目是什么。
- 技术栈是什么。
- 常用命令是什么。
- 代码风格是什么。
- 修改后如何验证。
- 哪些文件或动作禁止。

推荐模板：

```markdown
# Project Instructions

## Overview
这是一个 Next.js 应用，主代码在 `src/`，测试在 `tests/`。

## Commands
- 安装依赖：`npm install`
- 开发服务：`npm run dev`
- 类型检查：`npm run typecheck`
- 单元测试：`npm test`
- 格式检查：`npm run lint`

## Code Style
- 使用 TypeScript strict mode。
- 不新增 `any`。
- 复用现有组件和工具函数。

## Testing
- 修改业务逻辑时补充或更新测试。
- 提交前至少运行相关测试。

## Safety
- 不读取或修改 `.env*`。
- 不提交真实密钥。
- 不直接改数据库迁移，除非任务明确要求。
```

## 2. `AGENTS.md` 不该写什么

不要写：

- API Key、token、cookie。
- 只针对本次任务的临时要求。
- 个人机器路径。
- 不稳定的模型名称或价格。
- “写高质量代码”这种无法验证的口号。

临时要求写在 App 当前线程里；长期规则才写进 `AGENTS.md`。

## 3. 多层 `AGENTS.md`

Monorepo 可以在根目录和子目录放不同的 `AGENTS.md`：

```text
repo/
  AGENTS.md
  apps/web/AGENTS.md
  packages/api/AGENTS.md
```

理解方式：

- 根目录写全局规则。
- 子目录写局部规则。
- 越靠近当前文件的指令越能补充具体上下文。
- 不要依赖“同名标题自动覆盖”这种想象，写规则时要尽量避免冲突。

## 4. App 中的权限入口

App 用户优先通过这几处理解权限：

- App Settings。
- 当前线程的审批提示。
- 当前 App 的 `/` 命令列表中显示的权限入口。
- Review 面板中的 diff。

常见策略：

| 场景 | 建议 |
|---|---|
| 陌生项目 | 保守审批，先只读 |
| 日常小改 | 允许常见读写和安全命令 |
| 大规模重构 | 使用 worktree，严格 review |
| CI / 自动化 | 外部沙箱 + 最小权限 |
| 涉及密钥 / 生产数据 | 默认拒绝，人工确认 |

## 5. 沙盒模式怎么理解

Codex 的沙盒是为了限制命令和文件访问范围。CLI 中常见模式包括：

| 模式 | 含义 |
|---|---|
| `read-only` | 只读，适合审计和探索 |
| `workspace-write` | 可写工作区，适合日常开发 |
| `danger-full-access` | 无沙盒限制，只能在外部可信沙箱中使用 |

App 用户不需要一开始背 CLI 参数，但要理解：权限越大，越需要 Review、Git 和备份。

## 6. `config.toml` 是什么

`config.toml` 是 Codex 的配置文件。它适合团队或高级用户管理：

- 默认 profile。
- 审批和沙盒默认值。
- MCP server。
- feature flags。
- 终端和环境策略。

App 主线中，普通读者不需要先手写它。推荐顺序：

1. 先在 App Settings 里完成模型、权限、终端、插件和 MCP 的基础设置。
2. 团队需要统一策略时，再查官方 Config Reference。
3. 只复制官方当前支持的字段。
4. 改完后重启或刷新 App，再用 `/status`、Settings、MCP 列表等入口验收。

如果教程需要展示配置，优先展示“要查官方 schema”而不是写死字段：

```toml
# 只作为结构提示，实际字段以官方 Config Reference 和当前 App 为准。
# 不要把模型名、实验开关或公司密钥硬写进教程示例。
```

注意：字段会随版本变化，写教程时应链接官方 Config Reference，不要复制过时字段，也不要发明 `features.goals` 这类未核实字段。

## 7. Rules：比 prompt 更硬的命令边界

Rules 用来限制或允许命令执行。适合团队把危险命令拦住：

```toml
[[rules]]
match = "rm -rf *"
action = "deny"
message = "禁止危险递归删除；需要清理时先列出目标路径并人工确认。"
```

Rules 适合：

- 禁止危险命令。
- 要求高风险命令人工审批。
- 给团队设置统一安全边界。

Rules 不适合：

- 写代码风格。
- 写长工作流。
- 替代测试。

## 8. Hooks：事件脚本

Hooks 是事件触发脚本，适合做：

- 命令执行前检查。
- 工具执行后记录日志。
- 自动格式化。
- 外部审计。

App 用户应先理解它的风险：

- Hook 会运行真实脚本。
- Hook 可能读取敏感上下文。
- Hook 写错会阻塞工作流。

学习阶段不要急着写 Hook。先用 `AGENTS.md`、Settings、Rules。

## 9. 改完配置后怎么验收

每次改 `AGENTS.md`、Settings、Rules、Hooks 或 `config.toml` 后，都按这张表验收：

| 改动 | App 中怎么验收 |
|---|---|
| `AGENTS.md` | 新线程里让 Codex 总结项目规则，看是否读到正确内容 |
| 权限 / 沙盒 | `/status` 或 Settings 显示符合预期 |
| MCP 配置 | `/mcp` 能看到 server 和工具 |
| Rules | 试一个应被拦截的无害模拟命令，确认提示正确 |
| Hooks | 在测试仓库里触发一次，看日志和副作用 |

配置没验收就等于没配置。

## 10. App 项目基线

个人项目的最小基线：

```text
AGENTS.md
  写清项目命令、测试、禁止事项

App Settings
  使用默认或保守审批

Review
  每次改动都看 diff

Git
  小步提交，不混 unrelated changes
```

团队项目再增加：

```text
.codex/config.toml
.rules
.codex/hooks/
CI 中的 codex review 或测试任务
```

## 常见问题

### Q1：可以在 `AGENTS.md` 里指定模型吗？

不建议。模型选择属于运行配置，不是项目事实。

### Q2：Rules 和 Hooks 有什么区别？

Rules 更像命令策略；Hooks 是事件脚本。能用 Rules 解决的，不要先写 Hook。

### Q3：App 用户必须学 `config.toml` 吗？

不必须。单人使用先掌握 App Settings 和 `AGENTS.md`。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 已为当前项目编写AGENTS.md（项目说明、命令、风格、禁止事项）
- [ ] 知道App Settings和`/permissions`是权限管理的主入口
- [ ] 理解read-only、workspace-write、danger-full-access三种沙盒模式
- [ ] 知道config.toml适合团队统一配置，新手先不需要
- [ ] 能区分Rules（命令策略）和Hooks（事件脚本）
- [ ] 每次改完配置都做过验收

**如果以上全部勾选，恭喜你掌握Codex权限与配置！**

---

## 附录

### A. 配置层级速查

| 配置项 | 适合谁 | 入口 |
|--------|--------|------|
| `AGENTS.md` | 所有用户 | 项目根目录/子目录 |
| App Settings | 所有用户 | App界面 |
| `/permissions` | 所有用户 | App命令 |
| `config.toml` | 团队/高级 | `.codex/config.toml` |
| Rules | 团队 | `.codex/config.toml` |
| Hooks | 高级/企业 | `.codex/hooks/` |

### B. AGENTS.md最小模板

```markdown
# AGENTS.md

这份文件约束 Codex 在本项目里的工作方式。

参考来源：https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md

## 项目背景

开始修改前，先阅读 README、配置文件和目录结构，确认项目目标、技术栈和关键目录；不要凭经验猜。

## 常用命令

只写本项目已经确认过的真实命令。不要保留示例命令或占位文本。

## 1. 写代码前先想清楚

- 先确认需求、影响范围和验证方式。
- 信息不足时先问，不根据经验猜项目规则。
- 有多种方案时，先说明权衡，再选择适合当前任务的方案。

## 2. 简单优先

- 只实现当前任务需要的内容。
- 不主动新增框架、依赖、配置项或抽象层。
- 能用小改动解决，就不用大改动。

## 3. 外科手术式修改

- 保持改动集中，不顺手重构无关代码。
- 优先使用项目已有写法。
- 不统一格式化无关文件。
- 发现无关问题可以说明，不直接处理。

## 4. 目标驱动执行

- 复杂任务先拆成可检查的小步骤。
- 每一步都写清楚验证方式。
- 计划不成立时先说明原因，再调整。

## 安全边界

- 不读取 `.env*`。
- 不提交密钥、Token、证书。
- 不编辑生成文件，除非任务明确要求。

## 验证要求

- 改源码后运行相关测试；无法运行时说明原因。
- 最终回复说明改了什么、验证了什么、还剩什么风险。

## 这些规则生效时应该看到

- diff 能清楚对应本次需求。
- 无关改动少。
- 结果有测试或检查步骤支撑。
```

### C. 推荐学习资源

- **Codex Config 官方文档**：https://developers.openai.com/codex/config
- **本系列上一篇**：[CX-03 Commands](./CX-03-Codex-Commands工作流入口完整指南.md)
- **本系列下一篇**：[CX-05 MCP 外部工具](./CX-05-Codex-MCP外部工具完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-05 MCP：在 App 中连接外部工具](./CX-05-Codex-MCP外部工具完整指南.md)。
