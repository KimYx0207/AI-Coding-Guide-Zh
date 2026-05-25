# CX-11 Codex Web / Cloud 辅助指南：什么时候离开 App


本篇是 App 主线的云端辅助篇。

主要来源：OpenAI Codex Web / Cloud、GitHub integration、Environments、Internet Access、Secrets 官方文档。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：1-2小时
> - **难度等级**：⭐⭐ 入门级
> - **更新日期**：2026年5月
> - **信息来源**：OpenAI Codex Web/Cloud、GitHub integration、Environments、Secrets 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)、[CX-10 Review/PR](./CX-10-Codex-Review-GitHub-PR完整指南.md)

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-in-app-browser.webp" alt="Codex App 官方内置浏览器与页面反馈界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

完成本课学习后，你将能够：

1. **理解Cloud的定位**：掌握Cloud是远程执行路径，不是"更强的本地App"
2. **判断何时用Cloud**：远程仓库任务、长任务、PR修复、不依赖本机文件的改动
3. **理解Environment**：知道如何定义云端任务的仓库、依赖、setup script、secrets
4. **编写安全的setup script**：短而稳定、不写交互式命令、不输出密钥
5. **掌握App到Cloud的接力流程**：本地确认范围→创建issue/PR→Cloud接手→回到App Review
6. **管理Cloud安全**：最小权限secrets、不打印到日志、不把生产写权限给调试任务
7. **验收Cloud结果**：回到App看diff、本地跑验证、检查范围外改动
8. **区分App/Cloud/Automation场景**：知道各自适合什么类型的任务

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 10分钟）

**适合人群**：想知道什么时候该把任务交给Cloud

**只看这些章节**：

```
✅ 第1-2部分：Web/Cloud是什么 + 什么时候用（5分钟）
✅ 第7部分：App到Cloud的接力（5分钟）
```

---

### 路径B：完整学习（⏱️ 1-2小时）

**适合人群**：想系统掌握Cloud配置和使用

**学习顺序**：从头到尾所有章节

---

## 1. Web / Cloud 是什么

Codex Web / Cloud 是远程执行路径。它通常围绕远程仓库、PR 和云端环境工作。

与 App 的区别：

| 维度 | App | Web / Cloud |
|---|---|---|
| 执行位置 | 本机 / 本地项目 | 云端环境 |
| 主要对象 | 本地线程、worktree、Review | 远程仓库、任务、PR |
| 环境依赖 | 本机工具和文件 | Cloud environment |
| 适合 | 本地开发、桌面多线程 | 长任务、远程 PR、云端 CI 风格任务 |

## 2. 什么时候用 Cloud

适合：

- 远程仓库上直接修 issue。
- PR 评论修复。
- CI 失败后云端排查。
- 长时间后台任务。
- 不依赖本机私有文件的改动。

不适合：

- 需要本机数据库或本地 GUI。
- 需要访问未同步的本机文件。
- 需要你频繁看 UI 的任务。
- 密钥和生产数据边界不清的任务。

## 3. Environment 是什么

Cloud environment 定义云端任务怎么跑：

- 选择仓库。
- 安装依赖。
- 设置 setup script。
- 配置 secrets。
- 控制网络访问。
- 设定运行验证方式。

好的 environment 应该能让 Codex 在云端稳定复现项目。

## 4. 创建 Cloud 任务前先准备什么

从 App 接力到 Cloud 前，先准备：

| 项 | 要写清 |
|---|---|
| 仓库 | Cloud 要操作哪个 GitHub repo / branch |
| 任务范围 | 改哪些目录，不改哪些目录 |
| 依赖安装 | 用 `npm ci`、`pnpm install --frozen-lockfile` 还是其他命令 |
| 验证命令 | build、test、lint 具体怎么跑 |
| Secrets | 需要哪些，是否只读，是否会进日志 |
| 网络 | 是否需要 Internet access |
| 回流方式 | 生成 PR、推分支，还是只输出报告 |

Cloud 不是“更强的本地 App”。它缺少你的本机文件、GUI 状态和本地服务，必须靠远程仓库和 environment 复现。

## 5. Setup Script

Setup script 用来准备云端环境，例如：

```bash
npm ci
npm run build
```

原则：

- 短而稳定。
- 不写交互式命令。
- 不输出密钥。
- 失败时错误清晰。
- 与项目 README / AGENTS.md 保持一致。

## 6. Internet Access 与 Secrets

Cloud 任务可能需要联网或 secret。规则：

- 默认最小权限。
- 只给任务需要的 secret。
- 不把 secret 打印到日志。
- 不把生产写权限给调试任务。
- 定期轮换密钥。

## 7. App 到 Cloud 的接力

常见流程：

```text
App 中发现问题
  -> 本地确认范围
  -> 创建 GitHub issue / PR
  -> Cloud 接手长时间修复或 CI 修复
  -> 回到 App 拉取分支
  -> App Review 最终检查
```

Cloud 是辅助执行，不是绕过 Review。

## 8. Cloud 回到 App 怎么验收

Cloud 完成后，回到 App 做：

1. 拉取远端分支或打开对应 PR。
2. 在 App Review 里看 diff。
3. 本地运行关键验证命令。
4. 检查 Cloud 是否改了范围外文件。
5. 检查 PR 描述和测试记录。
6. 决定是否继续让 App 修，还是回 Cloud 处理远程 CI。

不要因为 Cloud 任务“通过”就跳过本地 Review。

## 9. Web / Cloud 与 Automations

| 需求 | 优先 |
|---|---|
| 本地项目周期检查 | App Automation |
| 远程仓库长任务 | Cloud |
| PR / CI 触发 | GitHub / CI / Cloud |
| 内部系统调度 | SDK / 外部队列 |

不要用桌面 App 伪装 webhook server。

## 常见问题

### Q1：Cloud 能访问互联网吗？

取决于当前 environment 和官方能力。需要联网时显式配置并审查风险。

### Q2：Cloud 能用我的本机文件吗？

不能默认假设。Cloud 主要使用远程仓库和配置的环境。

### Q3：Cloud 任务完成后还要本地 Review 吗？

要。最终合并前仍要看 diff、测试和 PR。

---

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解Cloud是远程执行路径，不是本地App的替代品
- [ ] 知道什么任务适合Cloud（远程仓库、长任务、PR修复）
- [ ] 知道什么任务不适合Cloud（本机私有文件、GUI任务）
- [ ] 了解Environment、setup script、secrets的基本概念
- [ ] Cloud完成后会回到App做本地Review
- [ ] 不因为Cloud"通过"就跳过本地Review

**如果以上全部勾选，恭喜你掌握Codex Web/Cloud辅助！**

---

## 附录

### A. App vs Cloud 对比

| 维度 | App | Web / Cloud |
|------|-----|-------------|
| 执行位置 | 本机 | 云端环境 |
| 主要对象 | 本地线程、worktree | 远程仓库、PR |
| 适合 | 本地开发、桌面多线程 | 长任务、远程PR |

### B. 推荐学习资源

- **Codex Cloud 官方文档**：https://developers.openai.com/codex/cloud
- **本系列上一篇**：[CX-10 Review / GitHub / PR](./CX-10-Codex-Review-GitHub-PR完整指南.md)
- **本系列下一篇**：[CX-12 CLI 辅助](./CX-12-Codex-CLI辅助完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-12 CLI 辅助指南](./CX-12-Codex-CLI辅助完整指南.md)。
