# CX-06 Skills 完整指南：在 App 中调用和编写可复用工作流

主要来源：OpenAI Codex Skills 官方文档、Codex App Features、Plugins 文档。

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
> - **信息来源**：OpenAI Codex Skills 官方文档、Codex App Features、Plugins 文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)、[CX-03 Commands](./CX-03-Codex-Commands工作流入口完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **理解Skill的本质**：掌握Skill是可复用工作流，不是快捷命令
2. **判断什么时候升级成Skill**：一个流程重复三次以上、团队多人需要时就该沉淀
3. **编写规范的Skill**：写出目标明确、触发清晰、步骤可执行、输出稳定的SKILL.md
4. **管理Skill资源**：合理组织references/和scripts/，不藏危险脚本
5. **区分Skills与其他能力**：清楚Command、Skill、Automation、MCP、Plugin各自的分工
6. **团队共享Skill**：通过项目级`.agents/skills/`或 Plugin 打包分发
7. **自查Skill质量**：从触发、输出、权限、平台、资源、维护六个角度核对
8. **避免Skill反模式**：不写不可验证的口号、不写密钥、不伪装工具API

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想快速写一个团队复用的Skill

**只看这些章节**：

```
✅ 第1部分：Skill是什么（2分钟）
✅ 第3部分：Skill的文件结构（5分钟）
✅ 第4部分：好Skill的标准（3分钟）
✅ 第5部分：什么时候从prompt升级成Skill（5分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握Skill开发、共享和治理

**学习顺序**：从头到尾所有章节

---

## 术语表（小白必读）

Skill 的学习重点不是"会创建一个文件夹"，而是知道什么时候该把一次提示沉淀成可复用能力。

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| Skill | 可复用的任务说明、资源和可选脚本 | 本质是工作流，不是普通快捷键 |
| `SKILL.md` | Skill 的入口说明文件 | 必须写清触发条件、流程和输出 |
| Frontmatter | `SKILL.md` 顶部的 name / description 等元数据 | description 决定隐式触发质量 |
| Progressive disclosure | Codex 先看到 Skill 摘要，需要时再读全文 | Skill 列表太大时描述可能被缩短 |
| Explicit invocation | 用户点名 `$skill-name` | 最稳定，适合教学和团队流程 |
| Implicit invocation | Codex 根据 description 判断要不要用 | 依赖描述是否准确 |
| `references/` | Skill 附带的参考资料 | 放大段规范，不要塞满入口文件 |
| `scripts/` | Skill 附带的可选脚本 | 有真实副作用，要写清权限 |
| `agents/openai.yaml` | App UI metadata 和策略配置 | 可设置展示、依赖、隐式调用策略 |
| Plugin | Skill 的分发包装方式之一 | 想分享给更多人时再打包 |

一句话：Skill 把“每次都要重复说的话”变成“稳定、可触发、可维护的流程”。

## 0. Skill 的工作机制

老金我把 Skills 当作可复用判断，不是简单 prompt 收藏；能复用的必须包含步骤、边界和验收方式。

Codex 使用 Skill 的过程大致是：

```text
启动时扫描可用 Skills
  -> 把 name / description / path 放进初始上下文
  -> 用户点名或任务匹配 description
  -> Codex 读取对应 SKILL.md
  -> 必要时再读取 references、调用 scripts 或工具
  -> 按 Skill 约定输出结果
```

这就是为什么 Skill 的 `description` 很重要。它不是介绍文案，而是触发路由。写得太泛，Codex 可能乱用；写得太窄，真正需要时触发不了。

### 0.1 一个流程什么时候值得做成 Skill

| 信号 | 说明 | 是否适合 Skill |
|---|---|---|
| 同一提示复制三次以上 | 说明流程稳定重复 | 适合 |
| 多人需要同一做法 | 需要团队一致性 | 适合 |
| 输出格式总要固定 | 方便 Review、PR、报告 | 适合 |
| 需要附带规范或模板 | references 能降低入口长度 | 适合 |
| 只做一次的临时任务 | 没有复用价值 | 不适合 |
| 需要实时调外部 API | 工具连接更重要 | 先看 MCP / Connector |
| 需要每天运行 | 调度更重要 | Automation 调用 Skill |

### 0.2 Skill 设计的三个边界

1. **触发边界**：什么时候应该用，什么时候不该用。
2. **执行边界**：能读什么、能写什么、是否能跑脚本。
3. **输出边界**：最后交付什么格式，先报告问题还是先总结。

很多 Skill 不好用，是因为只写了“你是一个专家”，却没写边界。好的 Skill 应该让 Codex 知道“在什么场景下，按什么步骤，产出什么结果，哪些事不要做”。

## 1. Skill 是什么

Skill 是一组可复用指令、资源和可选脚本。它不是单纯"快捷命令"，而是一套工作流。

适合：

- 代码审查流程。
- 文档核对流程。
- 发布检查。
- 写作规范。
- 团队固定 SOP。

不适合：

- 只执行一次的临时任务。
- 需要实时外部 API 的工具连接。
- 需要定时运行的周期任务。

## 2. App 中怎么调用 Skill


常见方式：

```text
$code-review 审查当前 diff，重点看安全、测试和边界情况。
```

或自然语言触发：

```text
按我们的代码审查 Skill 检查这次改动。
```

App 也可能通过插件提供 Skills。可用 Skills 取决于当前 App、插件、项目和用户目录。

调用前先确认三件事：

1. 当前 App 是否能看到这个 Skill。
2. 这个 Skill 是用户级、项目级，还是插件带来的。
3. 它会不会读取额外资源、运行脚本或调用工具。

如果点名 `$skill-name` 没有触发，先检查名称、路径、插件是否安装，以及 App 当前会话是否已加载。

## 3. Skill 的文件结构


最小结构：

```text
.agents/skills/code-review/
  SKILL.md
```

放在哪里要分清：

| 位置 | 适合 |
|---|---|
| 项目级 `.agents/skills/` | 当前仓库专用 SOP |
| 用户级 skills 目录 | 个人跨项目复用 |
| 插件内 Skill | 团队或市场分发的能力包 |

项目级 Skill 更适合教程，因为读者打开仓库就能看到规则；用户级 Skill 适合个人工作流，不应该写进团队仓库。

示例：

```markdown
---
name: code-review
description: Review code changes for bugs, regressions, security risks, and missing tests.
---

# Code Review

## Workflow
1. Inspect the current diff.
2. Identify behavior changes.
3. Look for bugs, security risks, and missing tests.
4. Report findings first, ordered by severity.

## Output
- Findings with file and line references.
- Open questions.
- Test gaps.

## Rules
- Do not rewrite code unless explicitly asked.
- Do not praise changes before listing findings.
```

## 4. 好 Skill 的标准


| 标准 | 说明 |
|---|---|
| 目标明确 | 一句话说清它解决什么问题 |
| 触发清晰 | 用户点名或描述能稳定触发 |
| 步骤可执行 | 不写空泛原则 |
| 输出稳定 | 有明确交付格式 |
| 资源最小 | 只带必要参考文件和脚本 |
| 安全边界明确 | 写清哪些动作不能做 |

### 4.1 `description` 怎么写

description 是 Skill 的触发说明。推荐格式：

```text
Use when [任务场景]. Do [核心动作]. Do not use when [边界].
```

例子：

```yaml
description: Use when reviewing code changes for correctness, regressions, security risks, and missing tests. Report findings first. Do not use for general code generation.
```

不要写：

```yaml
description: Helps write high quality code.
```

因为它既不说明触发场景，也不说明边界。

### 4.2 `SKILL.md` 推荐结构

```markdown
---
name: code-review
description: Use when reviewing changed code for bugs, regressions, security risks, and missing tests. Report findings first.
---

# Code Review

## When To Use
- Current diff or PR needs review.
- User asks for review, audit, or risk check.

## Do Not Use
- User asks to implement a feature from scratch.
- There is no code diff or target file.

## Workflow
1. Inspect the diff.
2. Identify behavior changes.
3. Check correctness, security, tests, and scope.
4. Report findings first, ordered by severity.

## Output
- Findings with file / line references.
- Open questions.
- Verification gaps.
```

这个结构比“角色定义 + 你很专业”更可执行。

## 5. 什么时候从 prompt 升级成 Skill

满足任一条件就考虑 Skill：

- 同一流程重复使用三次以上。
- 团队多人需要统一做法。
- 流程包含多个检查步骤。
- 需要附带模板、脚本或参考文档。
- 希望被 Automation 调用。

临时任务不要急着写 Skill。

## 6. Skills、Commands、Automations 的分工

| 需求 | 首选 |
|---|---|
| 当前线程快速动作 | Command |
| 固定 SOP / 复用流程 | Skill |
| 定时或后台重复执行 | Automation |
| 外部工具连接 | MCP / Connector |
| 打包分发一组能力 | Plugin |

例子：

- `/review` 是 Command。
- `$code-review` 是 Skill。
- “每天早上 review 未合并 PR”是 Automation + Skill。

## 7. 带资源的 Skill

复杂 Skill 可以带资源：

```text
my-skill/
  SKILL.md
  references/
    checklist.md
    style-guide.md
  scripts/
    validate.js
```

原则：

- 大段参考资料放 `references/`。
- 重复性强、容易写错的逻辑放 `scripts/`。
- `SKILL.md` 只写入口、流程、路由规则和必要摘要。

带脚本的 Skill 要额外写清：

- 脚本需要什么运行时。
- 是否会写文件。
- 是否会联网。
- 失败时输出什么。
- 是否能在 Windows / macOS 都跑。

不要把一段危险脚本藏在 Skill 里让 App 自动执行。

### 7.1 Progressive disclosure 怎么影响文件组织

Codex 初始只看 Skill 的摘要，不会一开始把所有参考资料都塞进上下文。你应该这样组织：

| 内容 | 放哪里 | 原因 |
|---|---|---|
| 触发场景、流程、输出 | `SKILL.md` | Codex 必须先看到 |
| 长规范、示例、术语表 | `references/` | 需要时再读，省上下文 |
| 可重复机械检查 | `scripts/` | 比模型手写更稳定 |
| 图片、图标、UI metadata | `assets/`、`agents/openai.yaml` | App 展示和依赖说明 |

不要把 20 页规范全部复制到 `SKILL.md`。入口文件越长，越难维护，Codex 也更难快速抓住触发和流程。

### 7.2 带脚本 Skill 的安全写法

带脚本时必须写清：

```markdown
## Scripts

- `scripts/check-links.js`
  - Purpose: check internal markdown links.
  - Reads: docs/**/*.md
  - Writes: nothing by default.
  - Network: no.
  - Runtime: Node.js 20+.
  - Failure: print broken links and exit non-zero.
```

如果脚本会写文件、联网、调用外部服务，必须在 Skill 里明确说明，并让当前权限和审批策略接住它。

## 8. 团队共享

团队共享方式：

| 方式 | 适合 |
|---|---|
| 项目级 `.agents/skills/` | 当前仓库专用 |
| 用户级 skills 目录 | 个人跨项目复用 |
| Plugin | 打包给团队或市场分发 |

团队 Skill 要避免写个人路径、个人 token、个人偏好。

共享前自查：

| 项 | 标准 |
|---|---|
| 触发 | 点名和自然语言都能稳定触发 |
| 输出 | 结果格式稳定，方便 Review |
| 权限 | 不默认要求危险权限 |
| 平台 | Windows / macOS 路径写法不冲突 |
| 资源 | references 和 scripts 都能按相对路径找到 |
| 维护 | 有 owner，知道谁负责更新 |

## 9. Skill 与插件

Plugin 可以携带 Skills，但 Skill 不等于 Plugin。

| 能力 | 关系 |
|---|---|
| Skill | 一个可复用工作流 |
| Plugin | 一个能力包，可以包含多个 Skills、MCP、Apps、配置 |

当你只需要一个团队审查流程，用 Skill。需要打包 GitHub 连接器、MCP、多个 Skills、配置时，才考虑 Plugin。

## 10. 常见反模式

| 反模式 | 问题 |
|---|---|
| “做高质量代码” | 不可验证 |
| 在 Skill 里写密钥 | 安全风险 |
| 把工具 API 伪装成 Skill | 应该用 MCP |
| 把长期周期任务写成 Skill | 应该用 Automation 调用 Skill |
| 一个 Skill 解决所有事 | 边界过大，难维护 |

## 10.1 Skill 排障表

| 症状 | 可能原因 | 处理 |
|---|---|---|
| 点名 `$skill` 没触发 | 名称写错、Skill 未加载、路径不在扫描范围 | 查 App Skills 列表或重启 Codex |
| 自然语言没触发 | description 太泛或太隐晦 | 重写 description，加入触发词 |
| 触发了错误 Skill | 多个 Skill 名称 / 描述重叠 | 缩小描述，明确 Do Not Use |
| Skill 输出不稳定 | 没写输出格式 | 在 `Output` 中固定结构 |
| Skill 读错资料 | references 路径不清 | 在流程里说明何时读取哪个文件 |
| 脚本运行失败 | runtime、路径、权限或平台问题 | 写清运行时，测试 Windows / macOS |
| 团队成员看不到 | Skill 放在个人目录 | 放项目 `.agents/skills/` 或打包 Plugin |

### 10.2 Skill 版本和维护

团队 Skill 一旦多人使用，就要有维护纪律：

| 项 | 建议 |
|---|---|
| Owner | 每个 Skill 有负责人 |
| Changelog | 大改触发条件或输出格式时记录 |
| 测试提示 | 保留 3-5 条典型触发 prompt |
| 回滚 | 出问题能回到旧版 |
| 安全审查 | 带脚本或工具依赖的 Skill 要 Review |

Skill 是团队知识资产，不是一次性 prompt 草稿。

## 11. 课堂工坊：把重复提示沉淀成 Skill

### 案例一：从一段 prompt 升级为 `SKILL.md`

目标：把“每次都要说的代码审查要求”变成项目级 Skill。

1. 创建目录：

```text
.agents/skills/code-review/
  SKILL.md
```

2. 写入最小 Skill：

```markdown
---
name: code-review
description: Review changed code for correctness, security, and missing tests.
---

# Code Review

## Workflow
1. Read the current diff.
2. Check correctness, security, test coverage, and scope creep.
3. Report findings first, ordered by severity.
4. Do not modify files unless the user asks for fixes.

## Output
- Findings
- Open questions
- Verification notes
```

3. 在 App 新线程中触发：

```text
使用 $code-review 审查当前 diff。只报告问题，不修改文件。
```

你应该看到：输出按 findings 优先，而不是泛泛总结；没有新增 diff。

### 案例二：给 Skill 加 references

目标：让 Skill 引用团队固定规范，而不是把所有内容塞进入口文件。

```text
.agents/skills/release-check/
  SKILL.md
  references/
    release-policy.md
```

在 `SKILL.md` 里写清什么时候读取 `references/release-policy.md`。你应该看到：Codex 只在发布检查任务中加载这份参考，不会把 release 规则误用于普通修 bug。

### 案例三：Plugin 中的 Skill 和项目 Skill 怎么选

目标：理解分发边界。

| 场景 | 放哪里 |
|---|---|
| 当前仓库专用 SOP | `.agents/skills/` |
| 个人跨项目习惯 | 用户级 skills 目录 |
| 团队要安装、启用、卸载的一组能力 | Plugin |

练习提示：

```text
这个流程只服务当前仓库。请帮我判断它应该做成项目级 Skill、用户级 Skill，还是 Plugin，并说明理由。不要创建文件。
```

你应该看到：Codex 根据复用范围、权限和分发方式做判断，而不是默认都做成插件。

## 12. Skill Cookbook：四类高价值 Skill

### 12.1 Code Review Skill

适合每个工程团队的第一个 Skill。

```markdown
---
name: code-review
description: Use when reviewing code changes for correctness, regressions, security risks, missing tests, and scope creep. Report findings first. Do not use for implementation.
---

# Code Review

## Workflow
1. Inspect the current diff or PR diff.
2. Identify behavior changes.
3. Check correctness, security, performance, tests, and scope.
4. Report findings first, ordered by severity.

## Output
- Findings with file and line references
- Open questions
- Verification gaps
- Suggested next action

## Rules
- Do not modify files unless explicitly asked.
- Do not praise before findings.
- Do not invent test results.
```

### 12.2 Release Readiness Skill

适合发布前检查。

```markdown
---
name: release-readiness
description: Use before a release to check changelog, tests, docs, migration notes, and rollback risk. Do not deploy.
---

# Release Readiness

## Workflow
1. Read release notes or changelog.
2. Check changed files and migration notes.
3. Verify relevant test / build commands.
4. Identify missing docs, rollback gaps, and risky dependencies.

## Output
- Ready / Not ready
- Blocking issues
- Non-blocking follow-ups
- Verification evidence
- Rollback notes
```

### 12.3 Docs Drift Skill

适合课程、README、开发文档维护。

```markdown
---
name: docs-drift-check
description: Use when checking whether docs match current repository commands, config, and source behavior. Report drift with evidence. Do not rewrite docs unless asked.
---

# Docs Drift Check

## Workflow
1. Read target docs.
2. Read source-of-truth files such as package.json, AGENTS.md, config, scripts, or official docs.
3. Compare claims with evidence.
4. Report drift and suggested edits.

## Output
- Document location
- Claim
- Source of truth
- Drift type
- Suggested correction
```

### 12.4 Security Triage Skill

适合把“安全检查”变成稳定流程。

```markdown
---
name: security-triage
description: Use when triaging a suspected security issue in code, config, MCP, plugins, automations, or cloud setup. Report impact and containment steps first.
---

# Security Triage

## Workflow
1. Identify asset, entry point, and affected scope.
2. Check whether secrets, production data, permissions, or external services are involved.
3. Separate confirmed facts from assumptions.
4. Recommend containment, verification, and follow-up.

## Output
- Severity
- Affected files / systems
- Evidence
- Immediate containment
- Follow-up fixes
```

### 12.5 Skill 评审问题

每个 Skill 合并前问：

| 问题 | 为什么 |
|---|---|
| description 是否能准确触发？ | 决定是否会误用 |
| Do Not Use 是否写清？ | 防止泛化 |
| 输出格式是否稳定？ | 方便 Review 和自动化 |
| 是否需要 references？ | 避免入口文件过长 |
| 是否需要 scripts？ | 有脚本就有安全和平台问题 |
| 是否适合项目级而非用户级？ | 团队复用要放仓库 |
| 是否能被 Automation 调用？ | 需要耐久 prompt |

## 常见问题

### Q1：Skills 是 slash commands 吗？

不完全是。Skill 可以被点名触发，也可能显示成命令入口，但本质是可复用工作流。

### Q2：Codex App 会自动加载所有 Skills 吗？

取决于当前会话、项目、用户目录和插件。以 App 当前可见列表为准。

### Q3：Skill 能运行脚本吗？

可以引用脚本资源，但是否执行取决于权限和当前环境。脚本要最小权限、可审计。

### Q4：为什么我的 Skill 没有被自动使用？

最常见原因是 description 不够清楚。先用 `$skill-name` 显式触发验证流程，再优化 description 做隐式触发。

### Q5：项目级 Skill 和用户级 Skill 冲突怎么办？

不要依赖自动合并。两者可能同时出现。团队流程优先放项目级，个人习惯放用户级，名称尽量避免重复。

### Q6：Skill 要不要写很多人设包装？

不需要。语气设定可以帮助表达，但真正决定质量的是触发边界、流程、输入、输出、禁止事项和验证方式。

### Q7：什么时候把 Skill 打包成 Plugin？

当它要跨项目、跨团队分发，或者需要和 MCP、Connector、配置、UI metadata 一起安装时，再打包成 Plugin。单仓库 SOP 放 `.agents/skills/` 就够。

---

## 13. Skill 设计的核心：让流程可重复，而不是让 prompt 更长

Skill 的价值不是把一大段 prompt 换个地方存起来。它的价值是把一个高频、可复用、边界清楚的工作流变成 Codex 能稳定发现和执行的能力。

### 13.1 好 Skill 的四个特征

| 特征 | 说明 |
|------|------|
| 触发清楚 | description 里写明什么时候用 |
| 边界清楚 | 也写明什么时候不用 |
| 输入输出清楚 | Codex 知道读什么、交付什么 |
| 内容分层 | 常用指令在 `SKILL.md`，长资料放 references |

### 13.2 Skill 不该承载什么

```text
- 一次性任务。
- 当前项目的临时 bug。
- 模糊人设包装。
- 需要每天变化的命令。
- 真实密钥或私有账号信息。
```

一次性任务放 prompt。项目事实放 `AGENTS.md`。可复用流程才放 Skill。

## 14. `description` 写作课

Codex 初始只看到 skill 的 name、description 和路径。description 写不好，Skill 就很难被自动选中。

### 14.1 差 description

```yaml
description: A powerful helper for many tasks.
```

问题：没有触发词，没有边界，没有具体任务。

### 14.2 好 description

```yaml
description: Review Markdown course chapters for factual consistency, broken commands, missing learner steps, and Chinese readability. Use when editing docs or course material; do not use for source code review.
```

好在哪里：

- 有对象：Markdown course chapters。
- 有动作：review factual consistency、commands、steps、readability。
- 有触发场景：editing docs or course material。
- 有边界：do not use for source code review。

### 14.3 description 模板

```text
<Verb> <target artifact> for <specific outcome>. Use when <trigger>. Do not use when <non-goal>.
```

示例：

```yaml
description: Prepare release notes from Git commits and PR summaries. Use when the user asks for changelog or release communication; do not use for code implementation.
```

## 15. Skill 文件结构深入

推荐结构：

```text
.agents/skills/
  docs-drift/
    SKILL.md
    references/
      docs-style.md
      product-terms.md
    scripts/
      link_check.js
    assets/
      icon.png
    agents/
      openai.yaml
```

### 15.1 `SKILL.md`

放高频、短、必须读的流程：

```md
---
name: docs-drift
description: Check documentation against code, config, and recent changes. Use for docs drift review; do not use for general copywriting.
---

Workflow:
1. Identify the document scope.
2. Read nearby source files and config.
3. Compare commands, paths, feature names, and behavior claims.
4. Return confirmed drift, likely drift, and questions.
```

### 15.2 `references/`

放长资料、规范、术语表：

```md
# Product Terms

Use "workspace" for the user's active project boundary.
Use "thread" for a Codex conversation.
Avoid calling plugins "extensions" in course material.
```

Codex 只有在需要时才读取 reference，避免一开始挤占上下文。

### 15.3 `scripts/`

放确定性辅助脚本：

```js
// scripts/check-links.js
// Check local Markdown links and print broken targets.
```

脚本适合做确定性检查，不适合把复杂判断都塞进去。复杂判断仍然交给 Codex 按 Skill workflow 做。

### 15.4 `assets/`

放图标、示例文件、模板资源。课程里不需要空白素材提示，但可以把真实可复用资源放进 assets。

### 15.5 `agents/openai.yaml`

放 App UI metadata、默认 prompt、依赖提示或 invocation policy：

```yaml
interface:
  display_name: "Docs Drift"
  short_description: "Check docs against code and config"
  brand_color: "#3B82F6"
  default_prompt: "Check this document for drift against the project."

policy:
  allow_implicit_invocation: false
```

如果 `allow_implicit_invocation` 设为 `false`，Codex 不会因为普通 prompt 自动触发，但显式 `$docs-drift` 仍然可以用。

## 16. Progressive Disclosure：为什么 Skill 不应该一股脑塞资料

Codex 会先看到技能列表，再按需要读取完整 `SKILL.md`。技能列表会受上下文预算限制，description 可能被截短。课程里要让学生理解三个后果：

```text
1. description 的前半句最重要。
2. 不要把所有资料写进 description。
3. 长资料放 references，需要时再读。
```

### 16.1 技能很多时的命名策略

| 差命名 | 好命名 |
|--------|--------|
| helper | docs-drift |
| review | pr-security-review |
| writer | zh-course-editor |
| tool | release-notes |

名字要让人和 Codex 都能猜到用途。

### 16.2 大团队技能过多怎么办

```text
- 每个 Skill 只做一件事。
- 禁用不常用或不相关 Skill。
- 把同类 Skill 打包进 Plugin。
- 用清晰 description 避免互相抢触发。
- 对高风险 Skill 关闭 implicit invocation。
```

## 17. Skill 与 `AGENTS.md` 的边界

| 内容 | 放哪里 |
|------|--------|
| 项目测试命令 | `AGENTS.md` |
| 项目目录结构 | `AGENTS.md` |
| 可复用审查流程 | Skill |
| 可复用写作流程 | Skill |
| 项目安全边界 | `AGENTS.md` + Rules |
| 长期团队工作法 | Skill 或 Plugin |

### 17.1 组合示例

`AGENTS.md`：

```md
## Commands

- Test docs links: `pnpm docs:links`
- Lint Markdown: `pnpm docs:lint`
```

Skill：

```md
---
name: docs-drift
description: Check docs against project source and config.
---

Workflow:
1. Read the target doc.
2. Use AGENTS.md commands when verification is needed.
3. Compare claims against source and config.
4. Return drift findings and suggested edits.
```

`AGENTS.md` 告诉 Codex 项目怎么跑，Skill 告诉 Codex 这类任务怎么做。

## 18. Skill 与 Commands、Automations、Plugins 的组合

### 18.1 Command + Skill

```text
/plan
我准备使用 $docs-drift 检查 docs/codex。
请先规划要读哪些文件和如何分批执行。
不要修改文件。
```

### 18.2 Automation + Skill

```text
$docs-drift
每周一检查 docs/ 是否和代码、配置、README 不一致。
默认只读。
有发现时进入 Triage，没有发现时归档。
```

### 18.3 Plugin + Skill

当 Skill 要分发给团队或附带 App/MCP 能力时，打包为 Plugin。

```json
{
  "name": "course-authoring-pack",
  "version": "1.0.0",
  "description": "Course authoring workflows for Codex.",
  "skills": "./skills/"
}
```

## 19. Skill 案例：课程章节审查

```md
---
name: course-chapter-review
description: Review Chinese course chapters for learner flow, factual accuracy, command correctness, missing examples, and natural tone. Use for Markdown course material; do not use for code review.
---

Workflow:
1. Identify the target learner and chapter goal.
2. Read the chapter headings before editing.
3. Check whether examples match the feature being taught.
4. Flag commands or feature claims that need source verification.
5. Improve learner flow before polishing language.
6. Do not add screenshot placeholders.

Output:
- Key issues
- Suggested edits
- Questions that need source verification
```

使用 prompt：

```text
$course-chapter-review
请审查 docs/codex/CX-05-Codex-MCP外部工具完整指南.md。
重点看新手是否能按章节一步步学会 MCP。
不要直接改文件，先给问题列表。
```

## 20. Skill 案例：PR 风险审查

```md
---
name: pr-risk-review
description: Review a pull request or Git diff for behavior regression, security risk, missing tests, and review readiness. Use when the user asks for PR or diff review.
---

Workflow:
1. Read the diff and nearby files.
2. Identify user-visible behavior changes.
3. Prioritize correctness, security, and test gaps.
4. Avoid style-only findings unless they affect maintainability.
5. Return findings first, then questions.
```

使用 prompt：

```text
$pr-risk-review
请审查当前分支相对 main 的 diff。
不要修改文件。
只输出真实风险和需要我判断的问题。
```

## 21. Skill 案例：发布说明生成

```md
---
name: release-notes
description: Draft release notes from commits, PR summaries, and product impact notes. Use for changelog and release communication; do not use for implementation.
---

Workflow:
1. Gather commits or PR summaries.
2. Group changes by user impact.
3. Separate features, fixes, docs, and internal changes.
4. Avoid exaggeration.
5. Call out migration or risk notes when present.
```

使用 prompt：

```text
$release-notes
请根据最近 10 个 commit 生成中文发布说明。
不要编造用户影响。
如果 commit 信息不足，请列出需要补充的问题。
```

## 22. Skill 调试：为什么它没有触发

| 症状 | 可能原因 | 处理 |
|------|----------|------|
| `$skill` 找不到 | 路径不在 `.agents/skills` 或未刷新 | 检查路径、新线程或重启 |
| 自动不触发 | description 不清楚 | 改 description 前半句 |
| 触发错 skill | 多个 description 重叠 | 收窄触发词 |
| Skill 太啰嗦 | `SKILL.md` 塞太多资料 | 拆 references |
| 输出不稳定 | workflow 没有步骤和输出 | 加输入、步骤、输出 |
| 高风险 skill 自动触发 | implicit 太宽 | 关闭 implicit 或改 description |

### 22.1 调试 prompt

```text
我的 Skill 没有按预期触发。
请帮我检查：
1. name 和 description 是否清楚
2. 这个任务是否应该显式用 `$skill`
3. 是否有其它 Skill 抢触发
4. `SKILL.md` 是否缺少输入、步骤或输出
5. 是否应该把长资料移到 references
```

## 23. Skill 维护：像维护小产品一样维护

Skill 用久了会过期。维护时看：

```text
- 触发是否准确。
- 输出是否稳定。
- 里面的命令是否还存在。
- references 是否过期。
- scripts 是否还能跑。
- 是否应该升级成 Plugin。
```

### 23.1 Skill 变更记录模板

```md
# Skill Change Note

Skill: docs-drift

## Why

The previous workflow missed package script drift.

## Changed

- Added package metadata check.
- Added output section for uncertain claims.

## How to try

Use `$docs-drift` on README and package.json.
```

## 24. 团队 Skill 库设计

一套团队 Skill 库不要追求多，而要覆盖高频流程。

| 类别 | Skill |
|------|-------|
| Review | `pr-risk-review` |
| Docs | `docs-drift`、`course-chapter-review` |
| Release | `release-notes` |
| Security | `security-triage` |
| Support | `incident-summary` |
| Product | `spec-review` |

### 24.1 新 Skill 引入流程

```text
1. 先用普通 prompt 跑 3 次。
2. 确认流程稳定。
3. 写 `SKILL.md`。
4. 用显式 `$skill` 测试。
5. 再考虑 implicit invocation。
6. 多人使用后再打包 Plugin。
```

这条路线能防止团队把一堆一次性 prompt 都塞进 Skills。

## 25. 综合工坊：把一个重复 prompt 变成 Skill

这个工坊适合 Skills 课的核心练习。

### 25.1 原始 prompt

```text
请审查这篇中文课程文档。
看看有没有事实错误、命令过期、步骤跳跃、术语不一致、表达太像 AI 的地方。
先给问题，再给修改建议。
```

这个 prompt 已经有重复使用价值，但还不够结构化。

### 25.2 提炼触发条件

```text
Use when:
- 审查中文课程文档
- 检查教程章节
- 对比命令和事实

Do not use when:
- 审查源代码
- 写营销文案
- 生成图片或视频
```

### 25.3 创建 Skill

```md
---
name: zh-course-review
description: Review Chinese technical course chapters for factual accuracy, command correctness, learner flow, terminology consistency, and natural tone. Use for Markdown course material; do not use for source code review.
---

Workflow:
1. Read the chapter title, learning goals, and heading structure.
2. Identify the target learner.
3. Check commands, paths, and feature claims against available sources.
4. Look for missing hands-on steps.
5. Separate factual issues from writing improvements.
6. Keep edits course-facing and learner-facing.

Output:
- Key issues
- Suggested structure improvements
- Fact checks needed
- Rewrite suggestions
```

### 25.4 显式调用测试

```text
$zh-course-review
请审查 docs/codex/CX-03-Codex-Commands工作流入口完整指南.md。
不要修改文件，先给审查结果。
```

### 25.5 根据结果迭代

如果输出太泛，改 Skill：

```md
When reviewing command examples:
- Flag commands that may not exist in Codex.
- Prefer current official command names.
- Distinguish App commands, CLI commands, Skills, Plugins, and MCP.
```

Skill 不是一次写完，而是根据真实使用慢慢变准。

## 26. Skill 测试题：让学生判断放哪里

把下面内容分类到 prompt、`AGENTS.md`、Skill、Plugin 或 Automation。

| 内容 | 应该放哪里 |
|------|------------|
| “只改 README” | prompt |
| “本项目用 pnpm test” | `AGENTS.md` |
| “审查中文课程章节的固定流程” | Skill |
| “每周一检查 docs 漂移” | Automation + Skill |
| “把 docs skill 和 GitHub app 一起分发给团队” | Plugin |
| “不要读 `.env` 文件” | `AGENTS.md` + permissions |
| “今天修 checkout bug” | prompt |
| “PR 风险审查流程” | Skill |

### 26.1 讨论题

```text
为什么“今天修 checkout bug”不应该做成 Skill？
为什么“PR 风险审查流程”适合做成 Skill？
为什么每周检查 docs 不是单独 Skill，而是 Automation + Skill？
```

## 27. Skill 进阶常见问题

### Q1：Skill 越长越好吗？

不是。常用流程要短，长资料放 references。Skill 太长会让 Codex 每次加载都消耗大量上下文。

### Q2：Skill 可以包含代码吗？

可以包含脚本，但脚本适合确定性检查。不要把需要判断的复杂推理全塞进脚本。

### Q3：Skill 和 prompt 模板有什么区别？

Prompt 模板是一次性或手动复用。Skill 能被 Codex 发现、显式调用，并和 references、scripts、assets、UI metadata 组成完整能力包。

### Q4：为什么我显式 `$skill` 后结果仍然不好？

可能是 Skill workflow 本身不清楚、输入不够、项目资料缺失，或任务不适合这个 Skill。显式调用只能保证使用，不保证设计正确。

### Q5：什么时候把 Skill 打包进 Plugin？

当它要跨团队分发，或需要附带 App integration、MCP server、图标、marketplace metadata、workspace sharing 时。

## 28. Skill 生命周期：从草稿到团队资产

一个 Skill 不是写完 `SKILL.md` 就结束。它通常会经历四个阶段。

### 28.1 Prompt 阶段

先用普通 prompt 跑几次，确认这件事真的高频、可复用、边界清楚。如果 prompt 每次都要大改，先不要做成 Skill。

### 28.2 Skill 草稿阶段

写清 `description`、workflow 和输出格式。这个阶段优先显式 `$skill` 调用，不急着依赖自动触发。

### 28.3 使用反馈阶段

观察它是否误触发、输出是否太泛、是否缺少 references、是否需要脚本辅助。根据真实任务修，不要凭想象堆说明。

### 28.4 团队资产阶段

当多人复用后，再考虑 owner、版本说明、Plugin 打包和定期复查。

```md
# Skill Owner Note

Skill:
Owner:
Primary users:
Trigger:
Non-goals:
Known failure modes:
Last reviewed:
```

## 29. Skill 作业：写三个不同粒度的 Skill

### 作业 A：太宽的 Skill

```yaml
name: helper
description: Help with all project tasks.
```

要求：指出为什么不合格。

### 作业 B：合格的 Skill

```yaml
name: pr-risk-review
description: Review Git diffs for correctness, security risk, missing tests, and scope creep. Use when preparing a PR; do not use for implementation.
```

要求：补 workflow 和 output。

### 作业 C：高风险 Skill

```yaml
name: prod-db-fixer
description: Fix production database issues automatically.
```

要求：说明为什么不应作为普通 Skill，应该转成只读诊断流程或外部 incident runbook。

## 30. Skill 长案例：从一句重复 prompt 到团队可复用资产

假设你每次写 PR 前都会让 Codex 做同一件事：

```text
帮我看一下这个 PR 有没有风险。
```

第一次这么问没问题。第三次还这么问，就说明它应该变成 Skill 了。把 prompt 升级成 Skill 的关键不是换一个文件名，而是把隐含要求写成可执行流程。

坏版本：

```yaml
name: pr-helper
description: Help with PRs.
```

坏在哪里：

```text
- 触发太宽，什么 PR 任务都可能误用。
- 没说只读还是可写。
- 没说输出格式。
- 没说风险优先级。
- 没说不应该做什么。
```

改成可用版本：

```yaml
name: pr-risk-review
description: Review Git diffs for correctness, security risk, missing tests, and scope creep. Use before opening or updating a PR. This skill is read-only and should not implement fixes.
```

`SKILL.md` 的 workflow 可以这样写：

```md
# PR Risk Review

## When To Use

Use when the user is preparing a PR, updating a PR after comments, or deciding whether a diff is safe to submit.

## Workflow

1. Read the user's stated PR goal.
2. Inspect the current diff or provided files.
3. Classify findings by severity.
4. Check for scope creep and missing tests.
5. Return actionable findings with file evidence.

## Do Not

- Modify files.
- Stage, commit, push, or reply to external reviewers.
- Invent test results.
- Comment on style unless it affects behavior or reviewability.

## Output

Return:
- Summary
- Findings
- Missing verification
- Scope concerns
- Suggested next prompt
```

调用时就不需要每次重讲规则：

```text
$pr-risk-review
请审查当前 diff，重点看 auth redirect、测试覆盖和是否有无关改动。
```

这类 Skill 的价值在于稳定。它不替你做判断，但它让团队每次看 PR 风险时问同一组问题。

## 31. Skill 反例修正：不是所有重复内容都适合做 Skill

### 31.1 一次性任务不要做 Skill

坏例子：

```yaml
name: fix-today-checkout-bug
description: Fix today's checkout bug in branch kim/test.
```

问题：

```text
- 带有今天、具体分支、具体事故。
- 过期很快。
- 没有复用价值。
```

改法：保持为普通 prompt。

```text
请修复当前分支的 checkout bug。
范围：只改 checkout flow 和相关测试。
修完后运行 checkout 相关测试。
```

### 31.2 太抽象的经验不要做 Skill

坏例子：

```yaml
name: think-better
description: Think deeply before doing any task.
```

问题：

```text
- 无法判断何时触发。
- 没有明确输入输出。
- 会和所有任务抢上下文。
```

改法：把具体项目习惯写进 `AGENTS.md`，或者把某个特定流程做成 Skill。

### 31.3 高风险动作不要做成自动执行 Skill

坏例子：

```yaml
name: prod-hotfix
description: Fix production incidents automatically.
```

改法：把它降级成只读诊断 Skill。

```yaml
name: incident-readonly-triage
description: Summarize incident context, logs, likely code areas, and safe next questions. Use during incident analysis. Do not execute production actions.
```

对应 workflow：

```text
1. 总结现象。
2. 读取允许的日志或本地材料。
3. 标出可能影响范围。
4. 给出下一步人工决策。
5. 明确不执行回滚、发布、封禁或生产写入。
```

Skill 不是“让 Codex 更大胆”的工具。好的 Skill 让 Codex 更稳定、更可解释、更容易被团队复用。

## 32. Skill 版本演进：每次修改都要知道为什么

Skill 一旦被多人使用，就不能像个人 prompt 那样随手改。每次改动至少回答三件事：

```text
1. 这次改动解决什么重复问题？
2. 会影响哪些使用场景？
3. 如果效果变差，怎么退回？
```

一个轻量 changelog：

```md
# Skill Changelog

## 2026-06-09

Changed:
- Added "scope concerns" to PR risk output.
- Clarified that the skill is read-only.

Why:
- Reviewers kept missing unrelated cleanup in large PRs.

Watch:
- If output becomes too long, split findings into blocking and follow-up.
```

当 Skill 输出变差时，不要只改 description。先收集失败样例：

```text
请分析这个 Skill 的三次失败输出。

目标：
1. 找出是触发条件不清楚、workflow 不清楚，还是用户输入不够。
2. 建议修改 SKILL.md 的哪一段。
3. 不要重写整个 Skill。
```

团队维护 Skill 时，可以设一个 owner note：

```md
# Skill Owner Note

Skill: pr-risk-review
Owner: Engineering Productivity
Primary users: feature teams before PR update
Trigger: preparing or updating a PR
Non-goals: implementation, commit, external replies
Known failure modes: too many style comments, missing security angle
Last reviewed: 2026-06-09
```

这让 Skill 从“某个人写的好 prompt”变成“团队知道谁维护、为什么存在、坏了怎么修”的资产。

## 33. Skill 触发调试：为什么 Codex 没有使用你的 Skill

Skill 写好了但 Codex 没用，常见原因不是"Skill 坏了"，而是触发描述、任务输入或安装位置不清楚。

先检查 description：

```yaml
name: docs-helper
description: Help with docs.
```

这个 description 太宽。Codex 很难判断它什么时候比普通 prompt 更合适。

改成：

```yaml
name: docs-drift-review
description: Compare documentation against repository code and scripts. Use when checking whether README, docs, or examples are outdated. This skill is read-only unless the user asks for a specific documentation edit.
```

再检查用户 prompt：

```text
帮我看看文档。
```

这也太宽。改成：

```text
$docs-drift-review
请检查 README 的安装命令是否和 package scripts 一致。
只读输出问题，不要修改文件。
```

如果仍然没有触发，排查：

```text
1. Skill 是否在 `.agents/skills` 或用户/插件可发现位置。
2. `SKILL.md` frontmatter 的 name 是否清楚。
3. description 是否描述了触发场景，而不是性格。
4. 是否有多个同名 Skill 让选择变混乱。
5. App 是否需要 reload skills。
```

调试 prompt：

```text
我希望你使用 `$docs-drift-review`。
请先说明你是否能看到这个 Skill。
如果能看到，请按它的 workflow 执行。
如果不能看到，请告诉我可能的安装或发现问题。
不要改文件。
```

Skill 触发调试教给读者一个重要观念：Skill 的发现依赖清晰描述和正确位置。写一个很长的人设，不如写一句准确的“何时使用”。

## 34. Skill 输出调试：结果太散怎么办

Skill 被触发了，但输出每次都不一样，也需要调试。通常是 output contract 不够具体。

坏输出要求：

```md
## Output

Give useful suggestions.
```

改成：

```md
## Output

Return exactly these sections:

1. Summary
2. Blocking Issues
3. Follow-up Suggestions
4. Files Referenced
5. Suggested Next Prompt

Rules:
- Each Blocking Issue must include a file path or evidence.
- Do not include more than 5 Follow-up Suggestions.
- If no issue is found, say "No obvious drift found" and stop.
```

调试 prompt：

```text
请分析这个 Skill 的输出为什么太散。

重点看：
1. output section 是否清楚。
2. 是否限制数量。
3. 是否要求证据。
4. 是否定义没有发现时怎么回答。
5. 是否把实现和审查混在一起。
```

一个好 Skill 不只是让 Codex “知道做什么”，还要让 Codex “每次用相似格式交付”。这就是团队复用的核心。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解Skill是可复用工作流，不是快捷命令
- [ ] 知道什么时候该把prompt升级成Skill（重复3次+、团队统一）
- [ ] 能写出规范的SKILL.md（目标明确、步骤可执行、输出稳定）
- [ ] 理解Skill与Command、Automation、MCP、Plugin的分工
- [ ] 知道项目级、用户级、插件级Skill的放置位置
- [ ] 共享前做过触发、输出、权限、平台、资源、维护六维自查

**全部勾选后即掌握 Codex Skills。**

---

## 附录

### A. 能力分工速查

| 需求 | 首选 |
|------|------|
| 当前线程快速动作 | Command |
| 固定SOP/复用流程 | Skill |
| 定时或后台重复执行 | Automation |
| 外部工具连接 | MCP / Connector |
| 打包分发一组能力 | Plugin |

### B. Skill文件结构

```text
.agents/skills/my-skill/
  SKILL.md          # 入口、流程、规则
  references/       # 参考文档
  scripts/          # 可选脚本
```

### C. 推荐学习资源

- **Codex Skills 官方文档**：https://developers.openai.com/codex/skills
- **本系列上一篇**：[CX-05 MCP 外部工具](./CX-05-Codex-MCP外部工具完整指南.md)
- **本系列下一篇**：[CX-07 Plugins 连接器](./CX-07-Codex-Plugins连接器完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-07 Plugins / Connectors：App 能力扩展与账号连接](./CX-07-Codex-Plugins连接器完整指南.md)。
