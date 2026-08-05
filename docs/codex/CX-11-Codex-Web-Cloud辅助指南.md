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
> - **更新日期**：2026年5月30日
> - **信息来源**：OpenAI Codex Web/Cloud、GitHub integration、Environments、Secrets 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)、[CX-10 Review/PR](./CX-10-Codex-Review-GitHub-PR完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **理解Cloud的定位**：掌握Cloud是远程执行路径，不是"更强的本地App"
2. **判断何时用Cloud**：远程仓库任务、长任务、PR修复、不依赖本机文件的改动
3. **理解Environment**：知道如何定义云端任务的仓库、依赖、setup script、secrets
4. **编写安全的setup script**：短而稳定、不写交互式命令、不输出密钥
5. **掌握App到Cloud的接力流程**：本地确认范围→创建issue/PR→Cloud接手→回到App Review
6. **管理Cloud安全**：最小权限secrets、不打印到日志、不把生产写权限给调试任务
7. **核对Cloud结果**：回到App看diff、本地跑验证、检查范围外改动
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

## 术语表（小白必读）

Cloud 这一章最重要的不是"云端更强"，而是知道它和本机 App 的边界完全不同。

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| Codex Web / Cloud | 远程执行 Codex 任务的环境 | 不是本机 App 的复制品 |
| Cloud environment | 远程任务的仓库、依赖、脚本、变量、网络配置 | 环境可复现比模型能力更重要 |
| Setup script | agent 开始前安装依赖和准备环境的脚本 | 默认可联网，不要输出 secrets |
| Agent phase | Codex 真正执行任务的阶段 | 默认不联网，除非显式开启 |
| Environment variables | setup 和 agent 阶段都可用的变量 | 不适合存高度敏感值 |
| Secrets | setup 阶段可用、agent 前移除的敏感值 | 适合拉私有依赖，不适合 agent 阶段长期使用 |
| Internet access | agent 阶段是否允许联网 | 默认关闭，开启要限制域名和方法 |
| GitHub handoff | 从本地 App 交给远程仓库任务 | 本地未推送文件 Cloud 看不到 |
| 回流 | Cloud 完成后回到 App / PR Review | 不能跳过本地 diff 和验证 |

一句话：App 适合本机控制，Cloud 适合远程仓库执行；两者之间必须靠 Git、PR、任务交接包和 Review 衔接。

## 0. Cloud 的执行模型

我把 Web 和 Cloud 放成辅助篇，是因为老金这套 Codex 课的主舞台仍然是 App，本地证据要先站稳。

一次 Cloud 任务通常经历：

```text
选择仓库和分支
  -> 创建或复用 Cloud environment
  -> 运行 setup script 安装依赖
  -> 移除 setup-only secrets
  -> 进入 agent phase 执行任务
  -> 产出分支、PR、评论或报告
  -> 回到 App / GitHub Review
```

这条链路解释了几个常见现象：

- Cloud 不知道你本机未保存、未提交、未推送的文件。
- setup script 能安装依赖，但 `export FOO=bar` 不等于 agent 阶段一定持久可用。
- agent 阶段默认不联网，所以“查最新接口”需要显式开启网络或改成本地/文档证据。
- secrets 适合 setup 阶段，不应该指望 agent 阶段一直能读到。
- Cloud 完成不等于可以合并，最终仍要 Review。

### 0.1 什么时候 Cloud 是优势

| 情况 | Cloud 优势 |
|---|---|
| PR 评论反复修 | 远程分支和 GitHub 上下文更直接 |
| 长时间测试 / 构建 | 不占用本机 |
| 从手机或另一台电脑派任务 | 不依赖当前本地会话 |
| 团队统一环境 | 比每个人本机更可复现 |
| 并行跑多个远程任务 | 可以减少本机工作区冲突 |

### 0.2 什么时候 Cloud 会变弱

| 情况 | 原因 |
|---|---|
| 依赖本机数据库 | Cloud 环境拿不到你的本地服务 |
| 依赖桌面 GUI | Cloud 不等于你的桌面 |
| 需要未推送文件 | Cloud 只看远程仓库和配置 |
| 需要生产 secret 在 agent 阶段持续可用 | secrets 默认只在 setup 阶段 |
| 需要人工频繁判断 UI | 本机 App 更适合 |

## 1. Web / Cloud 是什么

Codex Web / Cloud 是远程执行路径。它通常围绕已连接的 GitHub 仓库、PR 和云端环境工作。

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

Cloud 任务启动后通常会创建容器、检出所选仓库分支、运行 setup script，再进入 agent 执行阶段。setup script 默认可以联网安装依赖；agent 阶段默认不联网，除非你在 environment 中显式开启并限制访问范围。

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

### 4.1 App 转 Cloud 前的最小交接包

不要只写“帮我继续修”。给 Cloud 的任务要包含：

```text
仓库/分支：owner/repo 的 feature/login-mobile 分支。
目标：修复登录页移动端按钮溢出。
范围：只改 src/pages/login.tsx、src/styles/login.css 和相关测试。
环境：使用 pnpm install --frozen-lockfile；验证 pnpm test -- login 和 pnpm lint。
限制：不要改认证逻辑，不要新增依赖，不要接触 secrets。
交付：打开 PR 或更新现有 PR，PR 描述包含 Summary / Verification / Risk。
```

这份交接包能减少 Cloud 因上下文不足而扩大改动。

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
- 不依赖 `export FOO=bar` 在 agent 阶段继续生效；需要持久环境变量时放到 environment 设置或写入合适的 shell 启动配置。

### 5.1 好的 setup script 长什么样

好的 setup script 像 CI 的准备步骤，短、稳定、可重复：

```bash
corepack enable
pnpm install --frozen-lockfile
pnpm build
```

不好的 setup script：

```bash
npm install
echo $PRIVATE_TOKEN
read -p "continue?"
open http://localhost:3000
```

问题分别是：依赖不可复现、泄露 secret、交互式阻塞、依赖本机 GUI。

### 5.2 setup 失败怎么排查

| 症状 | 可能原因 | 修正 |
|---|---|---|
| 依赖安装失败 | lockfile 不一致、私有 registry token 缺失 | 修 lockfile 或把 token 放 secret |
| 构建命令不存在 | Cloud 没读到正确包管理器或目录 | 在交接包写清工作目录 |
| setup 卡住 | 有交互式命令 | 改成非交互命令 |
| agent 阶段找不到变量 | 变量只在 setup shell 中 export | 放到 environment variables |
| secret 出现在日志 | 脚本 echo 或工具打印 | 立即轮换 secret，删日志可见引用 |

## 6. Internet Access 与 Secrets

Cloud 任务可能需要联网或 secret。规则：

- 默认最小权限。
- 只给任务需要的 secret。
- 不把 secret 打印到日志。
- 不把生产写权限给调试任务。
- 定期轮换密钥。

要分清两类值：

| 类型 | 作用时间 | 适合 |
|---|---|---|
| Environment variables | setup script 和 agent 阶段都可用 | 普通环境开关、非敏感配置 |
| Secrets | 只在 setup script 阶段解密可用，agent 阶段前移除 | 安装私有依赖、拉取私有资源 |

如果 agent 阶段需要访问外部网络，要在 environment 中开启 agent internet access，并尽量只允许必要域名和 HTTP 方法。

### 6.1 网络访问决策表

| 任务 | agent 阶段是否需要联网 | 建议 |
|---|---|---|
| 修本仓库代码并跑测试 | 通常不需要 | 保持默认关闭 |
| 安装依赖 | setup 阶段需要 | 放到 setup script |
| 查官方文档 | 可能需要 | 优先使用已配置文档源，或限制域名 |
| 调第三方 API 验证 | 高风险 | 使用测试环境，只允许必要域名 |
| 访问生产服务 | 默认不建议 | 需要单独审批、审计和最小权限 |

### 6.2 Secrets 生命周期

不要把 secret 当成“云端环境里的永久变量”。更稳的理解是：

```text
Secrets
  -> setup 阶段用于安装私有依赖或拉取私有资源
  -> agent 阶段前移除

Environment variables
  -> setup 和 agent 阶段都可用
  -> 适合非敏感配置或经过风险评估的运行参数
```

如果你发现一个任务必须在 agent 阶段持续使用敏感生产凭据，先停下来重新设计。很多时候应该改成只读报告、测试环境 token、外部 CI、或人工批准的短期动作。

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

## 8. Cloud 回到 App 怎么核对


Cloud 完成后，回到 App 做：

1. 拉取远端分支或打开对应 PR。
2. 在 App Review 里看 diff。
3. 本地运行关键验证命令。
4. 检查 Cloud 是否改了范围外文件。
5. 检查 PR 描述和测试记录。
6. 决定是否继续让 App 修，还是回 Cloud 处理远程 CI。

不要因为 Cloud 任务“通过”就跳过本地 Review。

### 8.1 Cloud 回流的四个常见风险

| 风险 | 检查方式 |
|---|---|
| 云端环境和本机不同 | 本地重新跑关键命令 |
| Cloud 改了范围外文件 | App Review 查看文件列表 |
| PR 描述过度乐观 | 对照 diff 和测试日志重写 Verification |
| Secrets / 网络权限过宽 | 检查 environment 和 GitHub connector 权限 |

Cloud 适合长任务，但最终合并仍然要回到 Review、测试和人工判断。

### 8.2 Cloud 结果的反向检查提示

Cloud 完成后，在 App 或 PR 里让 Codex 做一次反向解释：

```text
基于当前 Cloud 分支 diff，逐文件解释：
1. 为什么这个文件必须改
2. 对应任务交接包里的哪一条
3. 运行了哪些验证
4. 哪些风险还没有覆盖
不要继续修改文件。
```

如果解释不清，说明 Cloud 可能扩大了范围，或者 PR 描述写得过度乐观。

### 8.3 Cloud 与 App 的交接清单

| 阶段 | 谁负责 | 要交付什么 |
|---|---|---|
| App 本地发现 | 人 + App | 问题、复现、范围 |
| Cloud 接手前 | 人 | 仓库、分支、任务包、验证命令 |
| Cloud 执行 | Cloud | 分支、PR、日志、验证记录 |
| App 回流 | 人 + App | diff Review、本地验证、风险判断 |
| 合并前 | 人 / 团队 | CI、PR review、最终说明 |

Cloud 是执行者，不是最终审批者。

## 9. 课堂工坊：App 到 Cloud 再回 App

### 案例一：把本地发现的问题交给 Cloud 修

目标：学习 Cloud 接力包怎么写，避免“继续修一下”这种空任务。

```text
仓库/分支：owner/repo 的 feature/login-mobile 分支。
目标：修复登录页移动端按钮溢出。
范围：只改 src/pages/login.tsx、src/styles/login.css 和相关测试。
环境：使用 pnpm install --frozen-lockfile；验证 pnpm test -- login 和 pnpm lint。
限制：不要改认证逻辑，不要新增依赖，不要接触 secrets。
交付：更新现有 PR 或打开新 PR，PR 描述包含 Summary / Verification / Risk。
```

你应该看到：Cloud 任务围绕远程仓库和分支执行；它不会看到你未同步到 GitHub 的本机私有文件。

### 案例二：配置 setup script 和网络边界

目标：让 Cloud 能安装依赖，但不让 agent 阶段随意联网。

```bash
pnpm install --frozen-lockfile
pnpm build
```

在 environment 中确认：setup script 可以联网安装依赖；agent internet access 默认关闭。若必须联网查包或远程 API，只允许必要域名，并优先限制为 `GET` / `HEAD` / `OPTIONS`。

### 案例三：Cloud 结果回到 App 做最后检查

目标：把 Cloud 产物拉回本地，用 App Review 收口。

1. 在本地拉取 Cloud 更新的分支或打开 PR 分支。
2. 用 App Review 看文件列表和 diff。
3. 本地运行关键验证命令。
4. 对照 Cloud 的 PR 描述，修正 Verification 和 Risk。
5. 决定继续让 App 修，还是把远程 CI 问题交回 Cloud。

你应该看到：Cloud 的“完成”只是执行结束；合并前仍由本地 Review、测试和人工判断收口。

## 10. Web / Cloud 与 Automations

| 需求 | 优先 |
|---|---|
| 本地项目周期检查 | App Automation |
| 远程仓库长任务 | Cloud |
| PR / CI 触发 | GitHub / CI / Cloud |
| 内部系统调度 | SDK / 外部队列 |

不要用桌面 App 伪装 webhook server。

## 11. Cloud Runbook：从 issue 到合并

### 11.1 Issue 进入 Cloud 前

```text
Issue：
目标：
影响范围：
不改范围：
分支：
验证命令：
是否需要网络：
是否需要 secret：
交付方式：
```

如果这些信息写不出来，说明任务还不适合交给 Cloud。

### 11.2 Cloud 执行中

关注：

- setup script 是否成功。
- agent 阶段是否需要联网。
- 是否出现范围外文件。
- 是否打印了敏感信息。
- 是否卡在环境问题而不是代码问题。

不要一看到失败就放大权限。先判断是依赖、脚本、路径、网络还是任务本身不清楚。

### 11.3 Cloud 完成后

```text
回到 App：
1. 拉取 Cloud 分支
2. 看 Review 文件列表
3. 看单文件 diff
4. 本地运行关键验证
5. 对照 PR 描述
6. 修正 Verification / Risk
7. 决定继续 App 修、Cloud 修，还是人工处理
```

### 11.4 Cloud 复盘

| 问题 | 看什么 |
|---|---|
| Cloud 是否比本地更合适？ | 是否依赖远程仓库和长任务 |
| environment 是否可复现？ | setup 是否稳定 |
| 权限是否过宽？ | secret 和 network |
| PR 是否可 Review？ | diff 大小、描述、验证 |
| 下次能否模板化？ | 交接包是否可复用 |

## 常见问题

### Q1：Cloud 能访问互联网吗？

setup script 默认可以联网安装依赖；agent 阶段默认不联网。需要 agent 联网时，在 environment 中显式开启并审查风险。

### Q2：Cloud 能用我的本机文件吗？

不能默认假设。Cloud 主要使用远程仓库和配置的环境。

### Q3：Cloud 任务完成后还要本地 Review 吗？

要。最终合并前仍要看 diff、测试和 PR。

### Q4：Cloud 能看到我本机未提交的改动吗？

不能默认看到。除非你通过支持的本地到 Cloud delegation 明确带上工作状态，否则 Cloud 主要基于远程仓库和 environment。稳妥做法是把必要改动推到分支或写进 issue / PR。

### Q5：setup script 里 export 的变量为什么 agent 阶段没了？

因为 setup script 的 shell 状态不等于 agent 阶段持久环境。需要持续可用的普通变量放到 environment variables；敏感值按 secrets 生命周期设计。

### Q6：Cloud 适合跑 UI 截图验证吗？

如果任务需要本机浏览器、桌面状态或人工视觉判断，优先留在 App。本地页面、真实桌面应用和私有服务通常不是 Cloud 的优势。

### Q7：Cloud PR 通过测试就能合并吗？

不能只看“通过”。仍要看范围、diff、PR 描述、风险、CI 日志和 reviewer 反馈。Cloud 通过只是证据之一。

---

## 12. 深入理解：Cloud 是远端执行环境，不是“更强的本地 App”

Cloud 的优势不是神秘的"云上更聪明"，而是它能在一个可配置的容器环境里跑任务、安装依赖、修改代码、展示 diff，并把结果带回你的工作流。它和 App 的关系应该是接力，而不是替代。

| 维度 | App 本地 | Cloud |
|------|----------|-------|
| 项目状态 | 看得到本机工作区和未提交改动 | 通常从仓库分支或 commit checkout |
| 环境 | 你的电脑、终端、权限、工具链 | 容器环境和 setup script |
| 适合任务 | 交互式修改、Review、本地 UI 检查 | 可复现任务、CI 修复、远端分支工作 |
| 网络 | 受本地设置和权限影响 | setup 阶段有网络，agent 阶段默认无网络 |
| 密钥 | 本机账号和配置 | secrets 只在 setup 阶段可用 |
| 回流 | 直接看 Review 面板 | 需要打开 diff、PR 或 apply 回本地 |

课程里要强调：Cloud 不是把本地上下文“原样搬到云端”。你要给它可复现的分支、环境和任务说明。

## 13. Cloud 任务的五阶段执行模型

官方 Cloud environments 文档给出的执行顺序可以转成课堂图：

```text
选择仓库、分支或 commit
  ↓
创建容器并 checkout 代码
  ↓
运行 setup script
  ↓
应用网络设置
  ↓
agent 循环执行任务、编辑、检查
  ↓
展示最终回答和 diff
  ↓
人决定 PR、回流或继续追问
```

### 13.1 每个阶段人的责任

| 阶段 | 人要准备什么 |
|------|--------------|
| checkout | 明确分支、commit、任务入口 |
| setup | 安装依赖、工具、系统包 |
| network | 决定 agent 阶段是否需要联网 |
| agent | 给清楚任务和边界 |
| diff | 人工 review 结果 |
| handoff | 决定开 PR、继续修、回本地 |

Cloud 的关键不是"扔一个任务过去"，而是让远端环境能复现项目。

## 14. Setup Script：Cloud 成败的第一道门

Setup script 是 Cloud 课最需要讲透的部分。它决定了 Codex 能不能安装依赖、运行测试、使用项目工具。

### 14.1 好的 setup script

```bash
set -euo pipefail

corepack enable

if [ -f pnpm-lock.yaml ]; then
  pnpm install --frozen-lockfile
elif [ -f package-lock.json ]; then
  npm ci
fi

if [ -f pyproject.toml ]; then
  poetry install --with test
fi

echo "Setup complete"
```

这段脚本体现几个原则：

- 失败要尽早暴露。
- 根据 lockfile 判断包管理器。
- 不把 secret 打印到日志。
- 不把临时 `export` 当成 agent 阶段变量。

### 14.2 setup 与 agent 阶段的变量差异

官方文档强调：环境变量在 setup 和 agent 阶段都可用；secrets 只在 setup 阶段可用；setup script 里的 `export` 不会自动进入 agent 阶段。

| 类型 | setup 阶段 | agent 阶段 | 用法 |
|------|------------|------------|------|
| Environment variable | 可用 | 可用 | 普通配置、非敏感开关 |
| Secret | 可用 | 不可用 | 安装私有依赖、一次性认证 |
| `export` in setup | 当前 shell 可用 | 不持久 | 不要依赖它传给 agent |

### 14.3 错误示例

```bash
export API_BASE_URL=https://staging.example.com
npm ci
npm test
```

如果 agent 阶段还需要 `API_BASE_URL`，这段写法不可靠。应该在 Cloud environment 的环境变量里配置。

### 14.4 setup 排障 prompt

```text
我的 Codex Cloud setup script 失败了。
请先不要修改业务代码。
请根据 setup 日志判断：
1. 是依赖安装失败、系统工具缺失、网络问题还是脚本语法问题
2. 哪条命令最先失败
3. 是否有 secret 或环境变量缺失的迹象
4. 最小 setup script 修复建议是什么
```

## 15. Internet Access：不要把网络当默认能力

Cloud setup 阶段可以访问互联网安装依赖。Agent 阶段默认没有互联网，除非你配置 limited 或 unrestricted。这个边界很重要，因为它会影响测试、文档查询和外部 API 调用。

### 15.1 网络决策表

| 任务 | agent 阶段需要联网吗 | 说明 |
|------|----------------------|------|
| 修本地单元测试 | 通常不需要 | 依赖应在 setup 安装 |
| 查官方最新文档 | 可能需要 | 也可以在本地先给资料 |
| 调外部 staging API | 可能需要 | 要考虑凭据和数据 |
| 运行纯 lint | 不需要 | 不该依赖网络 |
| 安装依赖 | setup 阶段处理 | 不要放到 agent 任务里 |

### 15.2 无网络 agent prompt

```text
这个 Cloud 任务的 agent 阶段没有互联网。
请只使用仓库内文件、setup 后已有依赖和任务描述中的上下文。
如果你需要外部资料，请说明缺少什么，不要猜最新 API 行为。
```

### 15.3 有限网络 agent prompt

```text
这个 Cloud 任务允许有限网络访问。
只能访问官方文档和项目允许的服务。
不要把 secrets 打印到日志。
如果外部请求失败，请降级为基于仓库代码的分析。
```

## 16. App 到 Cloud 的交接包

从 App 把任务交给 Cloud 时，最常见的问题是上下文断裂。解决办法是写交接包。

### 16.1 交接包模板

```md
# Cloud Handoff

## Goal

Fix the failing checkout retry test on this branch.

## Branch / Commit

Use branch: fix/checkout-retry

## Known Failure

`pnpm test tests/checkout-retry.spec.ts` fails with timeout after retry state change.

## Relevant Files

- src/checkout/retry.ts
- tests/checkout-retry.spec.ts
- docs/checkout.md

## Constraints

- Keep public API unchanged.
- Do not refactor unrelated checkout code.
- Do not update lockfiles.

## Suggested Verification

- Run the targeted checkout test.
- Run the package lint command if dependencies are installed.
```

### 16.2 交接 prompt

```text
请把当前本地发现的问题整理成 Codex Cloud 交接包。
不要修改文件。
交接包要包括：
- 目标
- 分支或 commit
- 已知失败
- 相关文件
- 不能做的事
- 建议运行的命令
```

这一步适合在 App 本地完成，然后再把整理好的任务交给 Cloud。

## 17. Cloud 回到 App：不要只看最终回答

Cloud 完成后会展示回答和 diff。你要把它带回 App 或 PR 流程里看。

### 17.1 回流检查顺序

```text
1. 读 Cloud 的最终回答。
2. 看 changed files。
3. 看 diff 是否只覆盖任务范围。
4. 看 Cloud 是否运行了命令。
5. 如果开了 PR，在 App 里看 PR context。
6. 如果 apply 到本地，用 Review 面板看 uncommitted changes。
```

### 17.2 Cloud 结果复盘 prompt

```text
请复盘这个 Cloud task 的结果。
先不要继续修改。
回答：
1. 它改了哪些文件
2. 它声称解决了什么问题
3. 它运行了哪些命令
4. 哪些风险仍需本地 App Review
5. 我是否应该开 PR、继续追问，还是回本地处理
```

### 17.3 Cloud diff 回本地后的 App prompt

```text
我已经把 Cloud 任务的改动带回本地。
请在 App Review 视角帮我检查：
1. diff 是否和 Cloud 任务目标一致
2. 是否有本地未提交改动混入
3. 是否需要补充本地验证
4. PR 描述应该提到哪些风险
```

## 18. Cloud 与 GitHub PR：把远端任务变成可 review 结果

Cloud 很适合把一个明确 issue 或 PR 评论变成一个可审查的分支。关键是任务要小。

### 18.1 适合 Cloud 的 PR 任务

| 任务 | 适合原因 |
|------|----------|
| 修一个可复现 CI 失败 | 远端环境接近 CI |
| 更新依赖后修测试 | setup 可固定依赖 |
| 补文档或类型错误 | diff 容易 review |
| 处理明确 PR 评论 | 范围可控 |

### 18.2 不适合 Cloud 的 PR 任务

| 任务 | 原因 |
|------|------|
| 需要本机登录态 UI | Cloud 无法复现你的浏览器账号 |
| 需要访问本地未提交草稿 | Cloud checkout 看不到 |
| 产品方向未定 | 远端会猜 |
| 大范围重构 | diff 太大，review 成本高 |

### 18.3 Cloud PR prompt

```text
Fix the failing CI test described below.

Scope:
- Make the smallest code change that addresses the failure.
- Do not refactor unrelated modules.
- Do not update dependencies.

Failure:
- Test file: tests/payment/retry.spec.ts
- Error: retry state never returns to idle after provider timeout.

Expected:
- Add or update one regression test if needed.
- Run the targeted test.
- Summarize changed files and remaining risks.
```

这类 prompt 把 Cloud 的强项发挥出来：可复现、范围清楚、结果可 review。

## 19. Cloud 环境维护：缓存、维护脚本和版本固定

Cloud container 会缓存一段时间，以加速后续任务。缓存是好事，但也会带来“为什么这次和上次不一样”的疑问。

### 19.1 什么时候重置缓存

| 情况 | 动作 |
|------|------|
| setup script 改了 | 缓存会失效或需要刷新 |
| 环境变量或 secrets 改了 | 重新跑环境 |
| 依赖 lockfile 大改 | 可能要 reset cache |
| 维护脚本失效 | 修 maintenance script |
| 任务表现和本地差异很大 | 对比环境版本 |

### 19.2 版本固定思路

```text
Node: 根据项目 .nvmrc 或 package engines 固定
Python: 根据 pyproject 或 runtime.txt 固定
Package manager: 根据 lockfile 固定
System tools: 在 setup script 明确安装
```

### 19.3 维护脚本适用场景

```bash
set -euo pipefail

if [ -f pnpm-lock.yaml ]; then
  pnpm install --frozen-lockfile
fi

if [ -f pyproject.toml ]; then
  poetry install --with test
fi
```

维护脚本适合缓存恢复时同步依赖，不适合做一次性 secret 输出或复杂业务初始化。

## 20. Cloud 安全边界：secrets、日志和外部服务

Cloud 的安全重点是：不要把凭据暴露给 agent 阶段，不要把 secret 打到日志里，不要让任务访问不该访问的外部系统。

### 20.1 Secret 使用原则

```text
用 secret 安装私有依赖。
不要在 agent prompt 里粘贴 secret。
不要在 setup script 里 echo secret。
不要让测试把 secret 打到失败日志。
agent 阶段如果需要长期配置，用 environment variable，而不是 setup export。
```

### 20.2 外部 API 测试

```text
如果 Cloud 任务需要调用 staging API：
1. 使用专门的测试账号和测试数据。
2. 限制网络范围。
3. 在 prompt 里说明哪些请求可以发。
4. 失败时返回诊断，不要重试到制造噪音。
```

### 20.3 安全复盘 prompt

```text
请从安全角度复盘这个 Cloud task。
检查：
1. 是否可能把 secret 打进日志
2. 是否在 agent 阶段依赖了不该有的 secret
3. 是否访问了任务之外的网络资源
4. 是否修改了超出目标的文件
5. 是否需要在 PR 里说明环境限制
```

## 21. Cloud 常见失败模式

| 失败模式 | 表现 | 修复方式 |
|----------|------|----------|
| setup 装不动依赖 | 第一步就失败 | 固定包管理器和版本 |
| agent 需要联网 | 查文档或 API 失败 | 开有限网络或本地提供资料 |
| secret 阶段误解 | agent 阶段找不到 secret | 改成环境变量或调整任务 |
| 本地草稿没带上 | Cloud 改的是旧代码 | 先提交、推分支或写清 commit |
| diff 太大 | Review 成本高 | 缩小任务 |
| Cloud 结果和本地不一致 | 版本或环境差异 | 比对 setup、lockfile、工具版本 |
| PR 评论没读到 | GitHub 访问或分支上下文不足 | 回到 App 接 PR context |

### 21.1 失败后不要立刻重跑

先问：

```text
请根据这次 Cloud 失败输出，判断重跑是否有意义。
如果失败是配置问题，请给 setup 或环境修复建议。
如果失败是任务描述问题，请给更窄的 prompt。
如果失败是缺少权限，请说明需要哪类权限。
```

## 22. App、Cloud、Automation 的组合路线

一个完整团队常见路线：

```text
App:
  发现问题、复现问题、写交接包

Cloud:
  在远端分支上做可复现修复

Review:
  看 diff、处理 PR 评论

Automation:
  后续周期检查同类问题是否复发
```

示例：

```text
1. App 中发现 checkout 测试 flaky。
2. App 整理 Cloud handoff。
3. Cloud 修复并开 PR。
4. App Review 面板检查 PR diff。
5. Automation 每天检查相关测试是否再次失败。
```

这比“所有事情都在 Cloud 做”更稳，因为每个界面做自己擅长的事。

## 23. 综合工坊：把一个 CI 失败交给 Cloud

这个工坊展示 Cloud 的强项：明确、可复现、远端环境适合执行的任务。

### 23.1 任务背景

CI 在 `tests/payment/retry.spec.ts` 失败。本地你已经知道大概失败信息，但不想在本机长时间跑完整环境。

### 23.2 App 中先整理 handoff

```text
请把当前 CI 失败整理成 Codex Cloud handoff。
不要修改文件。
包括：
- 目标
- 分支或 commit
- 失败测试
- 相关文件
- 不允许做的事
- 建议验证命令
```

### 23.3 Cloud task prompt

```text
Fix the CI failure in `tests/payment/retry.spec.ts`.

Scope:
- Make the smallest change needed to fix the failing retry behavior.
- Do not refactor unrelated payment code.
- Do not update dependencies or lockfiles.

Known failure:
- Retry state does not return to idle after provider timeout.

Expected:
- Add or update one regression test if needed.
- Run the targeted test.
- Summarize changed files, commands run, and remaining risks.
```

### 23.4 Cloud 完成后回 App

```text
我已经拿到 Cloud task 的 diff。
请从 App Review 视角检查：
1. 是否只解决 CI 失败
2. 是否有无关重构
3. 是否需要本地补充验证
4. PR 描述应该怎样写
```

## 24. 综合工坊：Cloud 环境 setup 从失败到稳定

### 24.1 失败 setup

```bash
npm install
npm test
export API_BASE_URL=https://staging.example.com
```

问题：

```text
- `npm install` 可能不尊重 lockfile。
- 全量 test 放 setup 阶段会拖慢每次任务。
- `export` 不会让 agent 阶段持久获得变量。
```

### 24.2 改进 setup

```bash
set -euo pipefail

if [ -f package-lock.json ]; then
  npm ci
elif [ -f pnpm-lock.yaml ]; then
  corepack enable
  pnpm install --frozen-lockfile
fi

echo "Dependencies installed"
```

环境变量放 Cloud environment settings，不写在 setup 临时 export 里。

### 24.3 setup review prompt

```text
请审查这个 Codex Cloud setup script。
重点看：
1. 是否尊重 lockfile
2. 是否把测试放错阶段
3. 是否错误依赖 export
4. 是否可能打印 secret
5. 是否能更快、更稳定
```

## 25. Cloud 设计题

### 25.1 题目 A

```text
让 Cloud 修复我本机浏览器登录后的 UI bug。
```

判断：不适合，Cloud 不具备你的本机浏览器登录态。更适合 App、本地 in-app browser 或手动复现后交接。

### 25.2 题目 B

```text
让 Cloud 修复一个 CI 中可复现的单元测试失败。
```

判断：适合。失败明确、环境可复现、结果可 review。

### 25.3 题目 C

```text
让 Cloud 自动重构整个支付系统。
```

判断：不适合。范围太大，风险高，review 成本不可控。应拆小任务。

## 26. Cloud 进阶常见问题

### Q1：Cloud 能看到我本机未提交改动吗？

通常不能。Cloud 从仓库分支或 commit checkout。未提交本地草稿需要先提交、推分支、生成 patch，或在 handoff 里描述清楚。

### Q2：setup script 里跑测试好不好？

通常不建议把主要验证放 setup。setup 负责安装依赖和准备环境；agent 阶段再按任务运行目标测试。

### Q3：Cloud 通过测试后能直接合并吗？

不建议。Cloud 通过测试只是证据之一。仍然要看 diff、PR、业务风险和本地/CI 结果。

### Q4：Cloud 适合处理文档任务吗？

适合明确的文档更新，特别是仓库内文档和代码一致性。不适合需要大量本机资料或未同步资料的任务。

### Q5：Cloud 和 Automation 有什么区别？

Cloud 是远端执行环境，适合一次任务或远端分支工作。Automation 是按时间运行的后台任务，可以本地或 worktree 执行。

## 27. Cloud 交接案例：远端执行不能变成远端失控

Cloud 适合把明确、可复现、能在仓库里完成的任务交给远端环境。它不适合承接一句“帮我修一下”的模糊愿望。好的 Cloud handoff 要让远端 agent 知道边界，也要让本地用户知道回来以后怎么检查 diff。

一个完整交接可以分成四段。

第一段，交代本地发现：

```text
我在本地分支 `fix/auth-redirect` 上看到 `auth redirect` 测试失败。
失败命令：
`npm test -- auth-redirect`

已知现象：
- 登录后没有回到原目标页面。
- 失败集中在 redirect 参数保留逻辑。
```

第二段，限制远端任务：

```text
请在 Cloud 环境中只处理这个测试失败。

允许：
- 读取相关 auth 路由、redirect helper、测试文件。
- 修改最小必要代码和对应测试。
- 运行相关测试。

不要：
- 重构整个 auth 模块。
- 修改登录 UI 文案。
- 新增外部依赖。
- 处理无关失败。
```

第三段，让远端返回可审查证据：

```text
完成后请返回：
1. 改动摘要。
2. 修改文件列表。
3. 失败原因判断。
4. 运行过的命令和结果。
5. 没有覆盖的风险。
```

第四段，本地回收：

```text
请只读审查 Cloud 返回的 diff。

重点判断：
1. 是否只解决 auth redirect 测试。
2. 是否引入新依赖或扩大范围。
3. 验证命令是否足够。
4. 哪些行为需要我本地再跑一遍。
```

Cloud 环境本身也要有人维护：setup script、runtime 版本、环境变量、secrets 和 cache 策略都属于环境稳定性的一部分。安全检查不需要每次都重走一遍大会，但只要任务涉及 secrets、外部 API、联网下载或无人值守写入，就应该把边界写进 handoff，而不是事后靠 Review 猜。

## 28. Cloud 作业：写一个 handoff，再挑错

### 28.1 初稿

```md
Fix the tests.
```

要求学生指出缺少：

```text
- 哪个测试。
- 哪个分支。
- 已知失败。
- 相关文件。
- 禁止事项。
- 验证命令。
```

### 28.2 合格版

```md
Fix the failing auth redirect test on branch `fix/auth-redirect`.

Known failure:
- `pnpm test tests/auth/redirect.spec.ts`
- Expected fallback redirect, got blank path.

Scope:
- Keep public route names unchanged.
- Do not update dependencies.
- Do not refactor unrelated auth helpers.

Verification:
- Run the targeted test.
- Summarize changed files and remaining risk.
```

## 29. Cloud 失败二次交接：远端没修好时怎么继续

Cloud 任务失败并不等于浪费。失败结果里通常有三类有用信息：环境是否搭起来了、测试是否能跑、失败是否比原来更窄。不要直接重新发一句“再试试”，要把第二次 handoff 写得更具体。

第一次失败摘要可能是：

```text
Cloud run failed.
Could not install dependencies.
pnpm not found.
No tests were run.
```

这不是代码问题，而是环境问题。第二次不要继续要求“fix test”，先修 setup：

```text
The previous Cloud task failed before running tests because `pnpm` was not available.

Please focus only on environment setup diagnosis.

Return:
1. What setup command is missing.
2. Whether package manager is declared in the repo.
3. Suggested setup script change.
4. Do not modify application code.
```

如果第一次失败是测试仍然失败：

```text
Cloud ran the targeted test but it still failed.
Failure narrowed to:
- expected redirect path: /dashboard
- actual redirect path: /
Changed files:
- src/auth/redirect.ts
- tests/auth-redirect.test.ts
```

第二次 handoff 就应该围绕剩余失败：

```text
Continue from the previous Cloud result.

The environment works and the targeted test runs.
Focus only on the remaining redirect path mismatch:
- expected /dashboard
- actual /

Do not change setup script.
Do not refactor auth module.
Inspect only redirect helper and test expectation first.
If you need another file, explain why.
```

如果 Cloud 修改太大：

```text
Previous Cloud result changed too many unrelated files.

Please do not continue implementation.
Instead, produce a rollback plan:
1. Which files are directly related to auth redirect.
2. Which files are unrelated.
3. Which changes should be discarded or split out.
4. What local Review steps I should take.
```

Cloud 的二次交接能力很重要，因为远端任务天然缺少本地人的即时纠偏。每次失败都要变成更窄的下一次任务，而不是更急的同一句话。

## 30. Cloud 环境演进：setup script 不要写成魔法咒语

Setup script 是 Cloud 任务能不能开始的基础。很多团队一开始会把它写成一堆命令，能跑就不管。课程里要教读者把 setup script 当成团队资产维护。

坏版本：

```bash
npm install
npm test
```

问题：

```text
- 不知道项目实际包管理器。
- setup 阶段不应该默认跑完整测试。
- 失败时很难知道卡在哪一步。
- 依赖版本和缓存策略不清楚。
```

更稳的思路：

```bash
corepack enable
pnpm install --frozen-lockfile
```

如果项目需要生成客户端或准备测试依赖，分段写：

```bash
corepack enable
pnpm install --frozen-lockfile
pnpm run generate
```

然后在 handoff 里说明真正要跑的测试：

```text
After setup, run:
pnpm test tests/auth/redirect.spec.ts
```

不要把所有验证都塞进 setup script。setup 的任务是让环境可用，agent 阶段的任务才是根据目标运行相关命令。

Cloud 环境维护 note：

```md
# Cloud Environment Note

## Runtime

Node:
Package manager:

## Setup Script

Commands:

## Environment Variables

Used during setup:
Not available during agent phase:

## Common Failures

- package manager missing
- lockfile mismatch
- generated files missing
- test browser dependency missing

## Last Updated

...
```

这份 note 的价值是让 Cloud 失败不再靠记忆排查。新同事看到环境失败，可以先看这份说明，而不是直接怀疑 Codex 不会修。

## 31. Cloud 与本地 Review 的闭环：远端完成不等于本地结束

Cloud 完成后，本地至少做三件事。

第一，检查范围：

```text
请只读审查 Cloud 返回的 changed files。
判断：
1. 哪些文件和目标直接相关。
2. 哪些文件可能是顺手改动。
3. 是否新增依赖或改配置。
4. 是否需要拆 PR。
```

第二，检查证据：

```text
请阅读 Cloud 返回的命令记录。
判断：
1. 是否运行了目标测试。
2. 是否只运行了 setup 而没有验证行为。
3. 是否有失败命令被忽略。
4. 我本地应该补跑什么。
```

第三，检查叙事：

```text
请基于 Cloud diff 起草 PR 描述。

要求：
1. Summary 只写真实改动。
2. Verification 只写 Cloud 或本地实际运行过的命令。
3. Risk 说明需要本地人工确认的路径。
4. 不要写“all tests passed”，除非有证据。
```

Cloud 的价值是并行和远端执行，不是绕过 Review。把 Cloud 结果带回 App，本地人仍然要做最后的范围判断、证据判断和合并判断。

## 32. Cloud 拆任务案例：不要把一个月的技术债扔给远端

Cloud 适合明确任务，不适合承接“整理整个项目技术债”。如果任务太大，先拆成多次远端任务，每次都有清楚输入和输出。

坏 handoff：

```text
Please clean up the whole auth module and fix tests.
```

问题：

```text
- 范围过大。
- 不知道哪些测试失败。
- 容易重构。
- 很难 Review。
- 成功或失败都不好判断下一步。
```

拆成三次 Cloud：

```text
Cloud Task 1：只读诊断
- 找 auth 模块当前失败测试和高风险区域。
- 不修改文件。
- 输出建议拆分。

Cloud Task 2：最小修复
- 只修 auth redirect regression。
- 只改 helper 和测试。
- 返回 diff 和命令。

Cloud Task 3：文档同步
- 根据已合并行为更新 auth docs。
- 不改业务代码。
```

Task 1 prompt：

```text
Analyze the auth module without modifying files.

Return:
1. Failing or fragile tests.
2. Areas with highest regression risk.
3. A recommended first small fix.
4. Files that should not be touched in the first fix.
```

Task 2 prompt：

```text
Fix only the auth redirect regression identified in the previous analysis.

Scope:
- redirect helper
- matching regression test

Do not:
- refactor auth module
- update dependencies
- change UI copy

Return changed files, commands run, and remaining risk.
```

Task 3 prompt：

```text
Update auth documentation to match the merged redirect behavior.

Scope:
- docs/auth.md
- README auth section if present

Do not:
- change source code
- invent behavior not visible in code or tests
```

这种拆法让 Cloud 结果更容易回收。远端任务越小，本地 Review 越快；远端任务越大，本地人越难判断它到底做对了什么。

## 33. Cloud 成本和注意力：不是所有并行都值得

Cloud 可以并行，但并行不是免费的。成本不只来自机器和运行时间，也来自你之后要 Review 多个 diff。

适合并行：

```text
- 三个独立文档更新。
- 多个只读调查。
- 不同平台的失败复现。
- 两个互不重叠的小 bug。
```

不适合并行：

```text
- 同一个核心模块的多个实现方案同时写。
- 多个任务都可能改同一组测试。
- 你没有时间 Review 多个结果。
- 每个任务都需要不断人工选择方向。
```

并行前 prompt：

```text
请判断这个任务是否适合拆成多个 Cloud task。

输出：
1. 可以并行的子任务。
2. 不能并行的原因。
3. 每个子任务的文件范围。
4. 回收顺序。
5. 最先应该跑的只读任务。
```

如果 Codex 建议 5 个并行任务，继续收窄：

```text
请把并行任务限制到最多 2 个。
优先选择文件范围不重叠、Review 成本最低的任务。
```

Cloud 并行的成熟使用方式，不是"开更多任务"，而是“让远端做互不干扰的事，让本地人能轻松回收结果”。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 理解Cloud是远程执行路径，不是本地App的替代品
- [ ] 知道什么任务适合Cloud（远程仓库、长任务、PR修复）
- [ ] 知道什么任务不适合Cloud（本机私有文件、GUI任务）
- [ ] 了解Environment、setup script、secrets的基本概念
- [ ] Cloud完成后会回到App做本地Review
- [ ] 不因为Cloud"通过"就跳过本地Review

**全部勾选后即掌握 Codex Web/Cloud 辅助。**

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
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-12 CLI 辅助指南](./CX-12-Codex-CLI辅助完整指南.md)。
