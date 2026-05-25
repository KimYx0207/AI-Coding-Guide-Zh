# CX-08 Subagents 完整指南：App 中的多 Agent 协作


主要来源：OpenAI Codex Subagents、App Features、CLI Slash Commands 官方文档。

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
> - **更新日期**：2026年5月
> - **信息来源**：OpenAI Codex Subagents、App Features、CLI Slash Commands 官方文档
> - **前置要求**：已完成CX-01至CX-07，熟悉App基本操作

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-in-app-browser.webp" alt="Codex App 官方内置浏览器与页面反馈界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **判断何时需要Subagents**：任务可拆成独立子任务、多文件互不重叠时才用
2. **设计安全的分工方案**：写清总目标、子任务边界、文件所有权、是否允许写
3. **掌握文件所有权规则**：并行写代码时明确每个Agent负责的文件范围
4. **组合Worktree和Subagents**：用Worktree隔离工作区 + Subagents分工并行
5. **正确合并Subagents输出**：看证据、看冲突、看所有权、主线程整合
6. **避免常见失败模式**：多个agent改同一文件、主线程不知道进展、子任务太大
7. **理解Subagents与Skills的配合**：Subagent执行角色，Skill提供工作流方法
8. **建立Review纪律**：并行改动合并前统一Review，不直接相信总结

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想快速知道什么时候该用Subagents

**只看这些章节**：

```
✅ 第1部分：Subagents解决什么问题（3分钟）
✅ 第2部分：App中什么时候用（5分钟）
✅ 第4部分：推荐分工模板（7分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握多Agent协作

**学习顺序**：从头到尾所有章节

---

## 1. Subagents 解决什么问题

Subagents 适合把一个任务拆成多个相对独立的子任务：

- 并行读不同模块。
- 一个实现、一个审查。
- 一个查官方文档、一个查代码。
- 前端、后端、测试分开推进。

它不是扩大单个上下文窗口，也不是让任务自动变聪明。它的价值是并行和分工。

## 2. App 中什么时候用

适合用：

```text
这个重构涉及前端、API 和测试。请先制定分工计划，再并行处理互不重叠的部分。
```

不适合用：

```text
修一个拼写错误。
```

判断标准：

| 条件 | 是否适合 |
|---|---|
| 任务可拆成独立子任务 | 适合 |
| 多个文件/模块互不重叠 | 适合 |
| 需要独立审查 | 适合 |
| 下一步必须等一个结果 | 先主线程做 |
| 单文件小改 | 不适合 |

## 3. App 中启动前要写清的内容

让 App 调 subagents 前，提示词至少要包含：

| 内容 | 示例 |
|---|---|
| 总目标 | “把认证模块迁移到新 SDK” |
| 子任务边界 | “前端只读 `src/pages/login.tsx`，后端只读 `src/api/auth/*`” |
| 文件所有权 | “Agent A 只改 docs，Agent B 只改 tests” |
| 是否允许写 | “先只读分析，不改文件” |
| 汇总方式 | “每个 agent 输出结论、证据、风险和建议动作” |
| 停止条件 | “遇到权限/测试/依赖问题先汇报，不自行扩大范围” |

不写这些，subagent 很容易变成多个不受控的普通对话。

## 4. 推荐分工模板

```text
先给出 subagent 分工计划，不要立刻改文件。

目标：重构认证模块。
范围：src/auth、tests/auth。
约束：不要改数据库迁移，不要引入新依赖。
分工：
- Agent A：阅读现有 auth 代码，列出风险。
- Agent B：核对官方 SDK 文档。
- Agent C：审查测试覆盖缺口。
汇总后再决定是否执行。
```

## 5. 文件所有权

并行写代码时必须明确文件所有权：

| Agent | 负责范围 |
|---|---|
| Frontend agent | `src/pages/login.tsx`、`src/components/auth/*` |
| Backend agent | `src/api/auth/*` |
| Test agent | `tests/auth/*` |
| Review agent | 只读 diff，不改文件 |

没有文件边界的并行开发很容易互相覆盖。

## 6. Subagents 与 worktree

| 能力 | 作用 |
|---|---|
| Subagent | 分工和并行思考 / 执行 |
| Worktree | 隔离 Git 工作区 |
| Review | 合并前看 diff |

大任务建议组合：

```text
Worktree thread + Subagents + Review
```

这样既能分工，又能降低污染主工作区的风险。

## 7. Subagents 与 Skills

Subagent 可以执行一个明确角色，Skill 提供工作流方法。

例子：

```text
让一个只读 subagent 使用 $tutorial-verifier skill 核对这篇教程的官方来源。
```

注意：不要假设所有 subagent 都自动拥有所有工具或插件。以当前 App 暴露能力为准。

## 8. Review 与合并规则

Subagents 返回后，主线程不要直接相信总结。按这个顺序合并：

1. 看每个 subagent 的输出是否有证据。
2. 看是否有互相冲突的结论。
3. 看文件所有权是否被遵守。
4. 由主线程整合方案。
5. 执行或合并后用 App Review 看 diff。
6. 运行验证命令。

如果两个 agent 给出相反建议，不要让其中一个继续硬改；先让主线程整理冲突点，再决定下一步。

## 9. 常见失败模式

| 失败模式 | 原因 | 修正 |
|---|---|---|
| 多个 agent 改同一文件 | 所有权不清 | 明确文件范围 |
| 主线程不知道进展 | 没有汇总点 | 要求阶段性汇报 |
| 子任务太大 | 拆分不够 | 缩小到模块级 |
| agent 自己发散 | 缺少目标和验收 | 写清停止条件 |
| 没有 Review | 并行改动难合并 | 合并前统一 review |

## 常见问题

### Q1：Subagents 会自动更正确吗？

不会。它们只是并行执行单元。正确性来自清晰分工、约束和 Review。

### Q2：什么时候不用 Subagents？

单文件小改、一步任务、目标不清楚的任务，都不应该先拉 subagents。

### Q3：Subagents 能和 Automation 一起用吗？

可以，但自动化任务更要限制权限和范围。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 知道什么时候该用Subagents（可拆分、多文件、独立子任务）
- [ ] 知道什么时候不该用（单文件小改、一步任务）
- [ ] 能写出包含总目标、边界、文件所有权、停止条件的分工提示词
- [ ] 理解Worktree + Subagents + Review的组合模式
- [ ] 知道合并前必须看证据、看冲突、看所有权
- [ ] 不为了让任务"看起来高级"而滥用Subagents

**如果以上全部勾选，恭喜你掌握Codex Subagents！**

---

## 附录

### A. Subagents使用判断

| 条件 | 适合？ |
|------|--------|
| 任务可拆成独立子任务 | ✅ |
| 多个文件/模块互不重叠 | ✅ |
| 需要独立审查 | ✅ |
| 下一步必须等一个结果 | ❌ 先主线程 |
| 单文件小改 | ❌ |

### B. 分工提示词模板

```text
先给出 subagent 分工计划，不要立刻改文件。
目标：[总目标]
范围：[目录/文件]
约束：[不能做的事]
分工：
- Agent A：[任务A]
- Agent B：[任务B]
汇总后再决定是否执行。
```

### C. 推荐学习资源

- **Codex Subagents 官方文档**：https://developers.openai.com/codex/subagents
- **本系列上一篇**：[CX-07 Plugins 连接器](./CX-07-Codex-Plugins连接器完整指南.md)
- **本系列下一篇**：[CX-09 Automations 后台任务](./CX-09-Codex-Automations后台任务完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-09 Automations：App 里的后台任务和周期检查](./CX-09-Codex-Automations后台任务完整指南.md)。
