# CX-09 Automations 完整指南：App 里的后台任务、提醒和周期检查


本篇是 App 主线中的 Automations 后台任务篇。

主要来源：OpenAI Codex App Automations、App Features、Skills、Rules、CLI / GitHub Action 官方文档。

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
> - **信息来源**：OpenAI Codex App Automations、App Features、Skills、Rules、CLI / GitHub Action 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **理解Automations的本质**：掌握它是后台/周期执行重复任务的能力，不是一次性工具
2. **创建规范的Automation**：写清频率、目录、目标、权限、输出、停止条件
3. **区分三类自动化任务**：摘要（只读）、检查（只读或最小写入）、修复（必须Review）
4. **组合Skill和Automation**：Automation管"什么时候运行"，Skill管"怎么做"
5. **理解与Command/Skill的区别**：Command手动触发、Skill复用流程、Automation按计划执行
6. **掌握安全基线**：学习阶段只读优先，不自动提交、不自动推送、不自动删除
7. **验收Automation效果**：时间、范围、输出、失败处理、副作用、暂停入口六维检查
8. **区分App/CI/SDK场景**：知道什么时候用App Automation、什么时候用GitHub Action或SDK

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想快速创建一个每日检查任务

**只看这些章节**：

```
✅ 第1-2部分：Automations是什么 + 创建方式（5分钟）
✅ 第3部分：三类常见任务（3分钟）
✅ 第10部分：设计模板（7分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握Automations和安全基线

**学习顺序**：从头到尾所有章节

---

## 1. Automations 是什么

Automations 是让 Codex 在后台或按计划执行重复任务的能力。

适合：

- 每天检查测试是否失败。
- 每周总结依赖更新。
- 定期检查文档和代码是否漂移。
- 监控 PR、部署或 issue 状态。
- 生成团队例行摘要。

不适合：

- 一次性问题。
- 目标不清楚的大改。
- 需要人工决策的高风险写操作。

## 2. App 中的创建方式

<p align="center"><img src="../../images/official/codex-create-automation.webp" alt="Codex App 创建 Automation 表单" width="720"/></p>

App 主线里可以直接自然语言创建：

```text
每天早上 9 点检查这个项目的测试是否失败。如果失败，只汇总失败测试和可能原因，不要修改文件。
```

好的 Automation 需要说明：

- 运行频率。
- 工作目录。
- 任务目标。
- 是否允许写文件。
- 输出去哪里。
- 什么情况下停止或升级给人。

创建后不要立刻信任它。先检查：

1. App 是否显示 automation 名称和状态。
2. 运行时间是否符合你的时区。
3. 工作目录是否是目标项目。
4. 是否只读或写入范围受限。
5. 输出会回到当前线程、通知、PR 评论还是其他地方。
6. 有没有暂停、删除或修改入口。

## 3. Automations 的三类常见任务

| 类型 | 示例 | 权限建议 |
|---|---|---|
| 摘要 | 每周总结 open issues | 只读 |
| 检查 | 每天运行测试或 lint | 只读或最小写入 |
| 修复 | 自动修小问题并提交 PR | 必须明确范围和 Review |

学习阶段优先只读。

## 4. Cron、Heartbeat 和 Thread Follow-up 怎么理解

App 里的自动化可以理解成三类使用体验：

| 类型 | 适合 | 注意 |
|---|---|---|
| 定时 / 周期任务 | 每天、每周、每小时检查 | 写清时区、目录、输出 |
| 当前线程稍后继续 | 30 分钟后提醒、稍后复查 | 适合短期 follow-up |
| 监控任务 | 盯 PR、部署、issue 状态 | 要写清停止条件 |

不要手写复杂调度语法给普通读者。App 用户优先用自然语言创建，再在 App 里 Review 生成的计划。

## 5. 与 Skills 组合

Automation 管“什么时候运行”，Skill 管“怎么做”。

例子：

```text
每周一上午运行 $dependency-review，总结 package.json 的依赖风险。不要自动升级依赖。
```

好处：

- Automation 保持短。
- Skill 里沉淀详细流程。
- 团队可以复用同一个 Skill。

## 6. 与 Commands 的区别

| 能力 | 触发方式 | 适合 |
|---|---|---|
| Command | 当前会话手动输入 | 立即执行 |
| Skill | 用户点名或自然语言触发 | 可复用流程 |
| Automation | 时间或后台事件触发 | 重复任务 |

不要用 Automation 做本来一次就能完成的事。

## 7. 安全基线

| 任务 | 建议 |
|---|---|
| 文档漂移检查 | 只读，输出报告 |
| 测试守护 | 先只读，失败后提醒 |
| PR 修复 | 用 worktree 或分支，必须 Review |
| 依赖升级 | 不自动合并 |
| 外部服务通知 | 限定目标 channel / repo |

所有自动化都要避免：

- 读取 `.env*`。
- 自动推送主分支。
- 自动删除文件。
- 自动扩大外部服务权限。

## 8. 运行后验收

第一次运行后必须检查：

| 验收项 | 通过标准 |
|---|---|
| 时间 | 按预期时间触发，不跨错时区 |
| 范围 | 只读/只写指定目录 |
| 输出 | 摘要足够人判断下一步 |
| 失败处理 | 失败时汇报原因，不无限重试 |
| 副作用 | 没有自动提交、推送、发错消息 |
| 暂停入口 | 能在 App 中暂停或删除 |

## 9. 与 GitHub Action / CI 的区别

| 类型 | 运行位置 | 适合 |
|---|---|---|
| App Automation | Codex App / 用户环境 | 个人和团队例行检查 |
| GitHub Action | CI runner | PR、push、仓库自动化 |
| CLI `codex exec` | 终端或脚本 | 无头一次性任务 |
| SDK | 自研系统 | 内部平台和复杂队列 |

不要把 App Automation 当成 webhook server。接飞书、钉钉、企业微信或内部系统时，通常应由外部系统触发 CI / SDK / Cloud，而不是让桌面 App 暴露公网。

## 10. 设计模板

### 8.1 只读摘要任务

```text
每周五 17:00 总结本仓库本周 open PR 的状态，列出阻塞原因和需要人工决策的项。只读，不评论 PR。
```

### 8.2 测试守护任务

```text
每天 9:00 在当前项目运行 npm test。如果失败，汇总失败测试名、错误摘要和相关文件。不要修改文件。
```

### 8.3 文档漂移任务

```text
每周一检查 README、AGENTS.md 和 docs/ 是否与 package.json 的脚本一致。只输出 drift report，不修改文件。
```

### 8.4 小范围自动修复任务

```text
每周三检查 docs 中失效的内部相对链接。只允许修改 docs/ 下的 markdown 链接，改完展示 diff，不自动提交。
```

## 常见问题

### Q1：电脑关机时 App Automations 还会运行吗？

取决于当前 App 和环境能力。需要可靠持续运行时，优先考虑云端 runner、GitHub Action 或 Codex Cloud。

### Q2：Automation 能自动修 bug 吗？

能，但不建议一开始就自动修。先做只读报告，再逐步放开小范围写入。

### Q3：可以用配置文件批量管理 Automations 吗？

以当前 App 支持能力为准。教程不要臆造不存在的 `.codex/automations.toml` 主路径。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解Automation是后台/周期执行，不是一次性工具
- [ ] 能写清频率、目录、目标、权限、输出、停止条件
- [ ] 学习阶段优先只读任务（摘要、检查）
- [ ] 知道如何组合Skill和Automation
- [ ] 第一次运行后做了六维验收（时间/范围/输出/失败/副作用/暂停）
- [ ] 不让Automation自动提交、推送、删除或扩大权限

**如果以上全部勾选，恭喜你掌握Codex Automations！**

---

## 附录

### A. 自动化能力对比

| 能力 | 触发方式 | 适合 |
|------|---------|------|
| Command | 手动输入 | 立即执行 |
| Skill | 用户点名 | 可复用流程 |
| Automation | 时间/后台事件 | 重复任务 |

### B. 推荐学习资源

- **Codex Automations 官方文档**：https://developers.openai.com/codex/automations
- **本系列上一篇**：[CX-08 Subagents](./CX-08-Codex-Subagents多Agent协作完整指南.md)
- **本系列下一篇**：[CX-10 Review / GitHub / PR](./CX-10-Codex-Review-GitHub-PR完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-10 Review / GitHub / PR 工作流](./CX-10-Codex-Review-GitHub-PR完整指南.md)。
