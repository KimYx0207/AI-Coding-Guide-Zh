# CX-10 Review / GitHub / PR 工作流：从 App 改动到可合并结果

本篇聚焦 App 主线里的 Review、GitHub 和 PR。

主要来源：OpenAI Codex App Review、GitHub integration、Codex Cloud / Web、CLI review 官方文档。

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
> - **信息来源**：OpenAI Codex App Review、GitHub integration、Codex Cloud/Web、CLI review 官方文档
> - **前置要求**：已完成 [CX-01 安装](./CX-01-Codex-App安装与认证完整指南.md)、[CX-02 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)、[CX-07 Plugins](./CX-07-Codex-Plugins连接器完整指南.md)

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **掌握Review工作流**：从Codex改代码到Review面板看diff到最终确认的完整流程
2. **读懂App Review面板**：逐项检查文件列表、单文件diff、命令记录、行内评论
3. **使用`/review`命令**：用带重点描述的`/review`发现特定类型问题
4. **管理GitHub Connector**：授权正确的仓库范围，控制读写权限
5. **完成App到GitHub PR的全流程**：Review → 运行测试 → stage → commit → push → create PR
6. **写好PR描述**：包含Summary、Verification、Risk三部分
7. **判断Cloud与App分工**：知道什么时候交给Cloud处理PR，什么时候留在App
8. **避免Review常见风险**：不让Codex顺手重构、不跳过测试、不改主分支

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：不用全看！

### 路径A：快速上手（⏱️ 15分钟）

**适合人群**：想让Codex改代码并提交PR

**只看这些章节**：

```
✅ 第1-2部分：Review主关口 + 完整改动流程（5分钟）
✅ 第6部分：从App到GitHub PR（5分钟）
✅ 第7部分：PR前核对清单（5分钟）
```

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想系统掌握Review和PR工作流

**学习顺序**：从头到尾所有章节

---

## 术语表（小白必读）

Review 篇的核心是：Codex 改完不等于你可以合并。你要能读懂 Git 状态、diff 和验证证据。

| 术语 | 一句话解释 | 新手注意 |
|---|---|---|
| Diff | 当前文件相对 Git 的变化 | Review 面板显示的是 Git 状态 |
| Uncommitted changes | 还没提交的工作区改动 | 可能包含你自己改的，不全是 Codex 改的 |
| Last turn changes | 最近一轮 assistant 造成的变化 | 适合定位刚才那次改动 |
| Branch changes | 当前分支相对 base 的差异 | 适合 PR 前整体检查 |
| Staged | 已准备提交的改动 | 不代表已提交 |
| Unstaged | 还没加入提交区的改动 | 常见于继续修改中 |
| Inline comment | Review 面板里对具体行的反馈 | 比泛泛说“这里不对”更准 |
| PR context | GitHub PR 描述、评论、changed files | 需要 GitHub 访问和 `gh auth login` |
| Verification | 真实运行过或明确未运行的检查 | 不要编造“已测试” |

## 0. Review 的底层逻辑

老金我把 Review 单独成课，是因为能看懂 diff、评论和 PR 状态，才算真正掌握 Codex App 工作流。

App Review 面板不是"Codex 的成果展示页"，而是 Git diff 工作台：

```text
工作区产生改动
  -> Review 面板读取 Git 状态
  -> 你检查文件、hunk、行和 staged 状态
  -> 用 inline comment 或提示让 Codex 定点修
  -> 你决定 stage、revert、commit、push
```

这解释了两个常见现象：

- Review 里可能出现你自己改的文件，因为它看的是 Git 状态。
- Codex 说“我改了 A”，Review 里却有 B，也许 B 是之前未提交改动，不一定是这轮新改。

### 0.1 Review 的三种视角

| 视角 | 适合什么时候 | 要看什么 |
|---|---|---|
| Uncommitted changes | 本地还没提交前 | 当前工作区所有改动 |
| Last turn changes | 刚让 Codex 修完一轮 | 这一轮是否引入新问题 |
| All branch changes | PR 或分支合并前 | 当前分支整体是否合理 |

不要只用一个视角。小修看 last turn，大合并看 branch，提交前看 staged / unstaged。

## 1. App Review 是合并前的主关口

Codex 写完代码后，不要只看它的总结。你应该进入 Review：

1. 看改了哪些文件。
2. 看每个文件 diff。
3. 确认是否超出任务范围。
4. 确认测试是否运行。
5. 必要时行内评论让 Codex 修。
6. 人工决定是否 stage / commit / push。

## 2. 一个完整 App 改动流程


```text
目标：修复登录页移动端按钮换行问题。
范围：只改 src/pages/login.tsx 和 src/styles/login.css。
验证：运行 npm test -- login 和 npm run lint。
交付：展示 diff 摘要，不要自动提交。
```

完成后检查：

| 检查 | 标准 |
|---|---|
| 范围 | 只改目标文件 |
| 行为 | 修复目标问题，没有顺手重构 |
| 测试 | 运行了相关测试 |
| 样式 | 和现有代码风格一致 |
| 风险 | 没有引入密钥、网络、权限变化 |

## 3. App Review 面板里具体看什么

Review 不是只看“Codex 说完成了”。逐项看：

| 区域 | 要看什么 |
|---|---|
| 文件列表 | 是否出现范围外文件、生成物、锁文件、配置文件 |
| 单文件 diff | 是否有无关重构、删除、格式化噪音 |
| 命令记录 / 线程输出 | 是否真的运行过验证命令，失败是否解释清楚 |
| 行内评论 | 能否针对具体行要求 Codex 修复 |
| Stage / Commit | 是否由你确认提交范围和 message |
| Push / PR | 是否推到正确分支和远端 |

如果 Review 中发现问题，优先用行内评论或明确提示让 Codex 修，不要重新开一个含糊的大任务。

### 3.1 Review 的严重程度分级

| 级别 | 例子 | 处理 |
|---|---|---|
| P0 必修 | 泄露 secret、删库脚本、绕过权限、改错业务逻辑 | 立即停止，人工处理 |
| P1 必修 | 测试失败、范围外核心文件、破坏兼容性 | 让 Codex 定点修复后重新 Review |
| P2 建议修 | 命名不清、重复逻辑、缺少边界测试 | 看时间和风险决定是否修 |
| P3 可后续 | 文案、格式、非阻塞优化 | 记录到后续任务 |

不要把所有 review comment 都当成同一优先级。Codex 很容易为了修小建议扩大 diff，真正要拦的是 P0/P1。

## 4. `/review` 的用法

在 App 或 CLI 中，`/review` 可以审查当前改动：

```text
/review
```

更好的写法：

```text
/review 重点检查移动端布局、CSS specificity、是否影响桌面端，以及测试缺口。
```

`/review` 适合发现问题，但最终是否接受仍要看 Review 面板和测试结果。

## 5. GitHub Connector 的角色

GitHub Connector / integration 适合：

- 读取 issue。
- 读取 PR 上下文。
- 查 CI 状态。
- 评论或更新 PR（取决于权限）。
- 从 App / Cloud 之间接力任务。

授权前要确认：

- 访问哪些仓库。
- 是否有写权限。
- 是否能评论 PR。
- 是否能创建分支或提交。

如果要在 App 里看到 PR 上下文，通常还需要：当前项目在 PR 分支上、GitHub 访问已配置、机器上安装 GitHub CLI，并用 `gh auth login` 完成认证。否则 PR 详情、评论或 changed files 可能不会完整显示在侧边栏或 Review 面板里。

## 6. 从 App 到 GitHub PR


典型流程：

```text
App thread
  -> Codex 修改本地文件
  -> Review 面板检查
  -> 运行测试
  -> git status / diff
  -> stage
  -> commit
  -> push branch
  -> create PR
```

提交信息建议让 Codex 先草拟，但由你确认：

```text
根据当前 diff 写一个简短 commit message。不要执行 git commit。
```

### 6.1 提交前让 Codex 做“反向解释”

在真正提交前，让 Codex 解释 diff 而不是继续写：

```text
请基于当前 diff 反向解释：每个文件为什么必须改、对应哪个需求、验证证据是什么、还有什么没覆盖。不要修改文件。
```

如果它解释不清某个文件为什么改，通常说明这个文件要么是范围外改动，要么需要你重新审。

## 7. PR 前核对清单


创建 PR 前确认：

| 项 | 你应该看到 |
|---|---|
| 分支 | 不是直接在 `main` 上提交 |
| Diff | 没有范围外改动 |
| 测试 | 至少运行相关测试或说明不能运行原因 |
| 描述 | Summary / Verification / Risk 写清楚 |
| Secret | 没有 `.env`、token、账号信息 |
| 连接器权限 | GitHub 写权限只用于目标 repo / PR |

### 7.1 PR 描述不是营销文案

好的 PR 描述只写证据支持的内容：

| 部分 | 应该写 | 不该写 |
|---|---|---|
| Summary | 具体改了什么 | “全面优化系统” |
| Verification | 真实运行的命令和结果 | 没跑却写 passed |
| Risk | 影响范围和未覆盖点 | “无风险”这种空话 |
| Rollback | 必要时怎么撤 | 复杂改动不写回滚 |

一个诚实的 Verification 比漂亮的总结更重要。

### 7.2 Review 排障表

| 症状 | 可能原因 | 处理 |
|---|---|---|
| Review 面板不可用 | 项目不是 Git 仓库 | 先初始化或打开 Git 项目 |
| 文件重复出现在 staged / unstaged | Git 同一文件有两种状态 | 分别检查 staged 和 unstaged diff |
| PR 评论不显示 | 不在 PR 分支、GitHub 未授权、`gh` 未登录 | 切分支并 `gh auth login` |
| Codex 修错评论 | 提示太泛，没引用具体 comment | 引用评论内容和文件行 |
| Verification 写得过度 | Codex 把推测当事实 | 只保留真实命令和明确未运行项 |
| 改动范围太大 | 任务范围没写清或 Codex 顺手重构 | 要求解释每个文件为什么必须改 |

## 8. 课堂工坊：从一个小 bug 到 PR

### 案例一：本地小修，先 Review 再提交

目标：练习 App 本地主线，不让 Codex 自动提交。

```text
目标：修复登录页移动端按钮换行问题。
范围：只改 src/pages/login.tsx 和 src/styles/login.css。
验证：运行 npm test -- login 和 npm run lint。
交付：展示 diff 摘要、命令结果和剩余风险。不要 git commit，不要 push。
```

你应该看到：Review 面板只显示目标文件；线程或终端记录里能看到验证命令结果；提交信息只由 Codex 草拟，不自动执行。

### 案例二：处理 PR 评论

目标：用 GitHub 上下文修特定 review comment。

1. 切到 PR 分支。
2. 确认 `gh auth login` 已完成。
3. 打开 App Review，查看 PR 评论和当前 diff。
4. 发送：

```text
只处理 PR 中关于登录页按钮溢出的那条 review comment。请先引用评论内容，再说明要改哪些文件。改完运行相关测试，不要处理其他评论。
```

你应该看到：Codex 只处理指定评论；如果 PR 上下文不可见，它应提示缺少 GitHub / gh / 分支条件，而不是编造评论。

### 案例三：写 PR 描述但不发布

目标：把 diff 变成可审的 PR 说明。

```text
根据当前 diff 草拟 PR 描述，包含 Summary、Verification、Risk。不要创建 PR，不要 push。
```

你应该看到：PR 描述里的 Verification 只写真实运行过或明确未运行的命令；Risk 不夸大“完全无风险”。

## 9. 什么时候用 Cloud / Web 处理 PR

适合 Cloud / Web：

- 远程仓库任务，不需要本机环境。
- 长时间跑的修复。
- PR 评论和 CI 反复修。
- 你不想占用本机 App 线程。

不适合：

- 依赖本机私有服务。
- 需要本地 GUI / 本机文件。
- 需要你频繁交互判断的小任务。

## 10. CLI review 是辅助

CLI 可以在 CI 或终端中做补充：

```bash
codex review
codex review --help
```

适合：

- CI 中自动审查 PR。
- 终端里快速检查当前 diff。
- 和 App Review 结果交叉验证。

不要用 CLI review 取代 App Review 面板。

## 11. PR 描述模板

```markdown
## Summary
- 修复登录页移动端按钮换行
- 限制按钮最小宽度，避免文本溢出

## Verification
- npm test -- login
- npm run lint

## Risk
- 仅影响登录页样式
- 已检查桌面断点
```

## 12. 常见风险

| 风险 | 防法 |
|---|---|
| Codex 顺手重构 | 任务里写清范围 |
| 未运行测试 | 明确验证命令 |
| 改了主分支 | 使用 worktree / feature branch |
| PR 太大 | 拆任务 |
| CI 失败自动乱修 | 限定失败项和文件范围 |

## 13. Review 复盘模板

每周从团队 PR 里抽 2-3 个 Codex 参与的改动做复盘，会比单纯要求“大家注意”更有效。

### 13.1 单个 PR 复盘

```markdown
## Task
- 原始任务是什么？
- 范围是否写清？

## Diff
- 改了哪些文件？
- 是否有范围外改动？

## Verification
- 运行了哪些命令？
- 哪些应该运行但没运行？

## Review Findings
- Codex review 发现了什么？
- 人工 review 发现了什么？
- 哪些问题本可以通过 AGENTS.md / Skill / Rules 提前避免？

## Follow-up
- 更新任务模板
- 更新 AGENTS.md
- 增加测试
- 增加 Rule / Skill / Automation
```

### 13.2 Review 常见改进动作

| 复盘发现 | 改进 |
|---|---|
| Codex 总是改范围外文件 | 更新任务模板，强制写范围和排除项 |
| 经常漏测试 | 在 `AGENTS.md` 和 review Skill 里写测试要求 |
| PR 描述夸大验证 | 固定 PR 模板，Verification 只写真实命令 |
| 外部 PR 评论处理不准 | 要求引用具体评论内容 |
| 安全问题反复出现 | 增加 Rules、Hook 或 security-triage Skill |

Review 的目标不是抓错，而是让下一次任务更好写、更好查、更好合并。

## 常见问题

### Q1：Codex 可以自动提交吗？

技术上可以，但学习阶段不建议。先让它展示 diff 和 commit message，再由你确认。

### Q2：App Review 和 GitHub PR Review 哪个重要？

都重要。App Review 是本地合并前检查；GitHub PR Review 是团队协作关口。

### Q3：Cloud 修 PR 后怎么回到 App？

看当前 App / Cloud 的 handoff 能力和 Git 分支状态。可靠做法是拉取远端分支，在 App 中继续 Review。

### Q4：Review 面板里出现的都是 Codex 刚改的吗？

不是。Review 反映 Git 仓库状态，可能包含你自己之前的未提交改动。需要区分 last turn、uncommitted 和 branch changes。

### Q5：Inline comment 比普通提示好在哪里？

它绑定到具体 diff 行，Codex 更容易知道你要修哪里。普通提示适合整体策略，行内评论适合定点修改。

### Q6：PR 评论能不能全交给 Codex 自动修？

不建议无边界自动修。先选择具体评论，限定文件范围和验证命令，再让 Codex 处理。多个评论最好分批修。

### Q7：什么时候应该 revert 而不是继续让 Codex 修？

当改动方向错、范围扩大、触碰敏感文件或解释不清时，revert 比继续补丁更稳。

---

## 14. 深入理解：Review 面板显示的是 Git 状态，不只是 Codex 的手

很多新人打开 Review 面板后会有一个误会：这里显示的都是 Codex 刚才改的。官方文档说得很清楚，Review 面板反映的是 Git 仓库状态。也就是说，它可能同时包含：

- Codex 改的文件。
- 你自己在编辑器里改的文件。
- 其它工具生成的文件。
- 之前未提交但还留在工作区的改动。

这就是为什么 Review 课不能只教“点开看 diff”。你要先教学习者区分 diff 的来源。

### 14.1 Review 前先问三句话

```text
1. 这个仓库现在干净吗？
2. 当前面板显示的是 uncommitted changes、all branch changes 还是 last turn changes？
3. 这些改动里哪些是我本来就有的，哪些是 Codex 新增的？
```

如果这三句话没问清楚，后面很容易把旧改动误判成 Codex 的问题，或者把用户自己的草稿误 revert。

### 14.2 三种 diff 范围

| 范围 | 适合什么时候看 | 风险 |
|------|----------------|------|
| Uncommitted changes | 本地提交前检查 | 混入手写改动 |
| All branch changes | PR 前看整个分支 | 范围大，容易失焦 |
| Last turn changes | 看 Codex 最近一轮 | 可能忽略之前遗留状态 |

课程里建议这样讲：**先用 Last turn 看 Codex 刚做什么，再用 Uncommitted 看本地整体状态，最后用 All branch changes 看 PR 级别影响。**

## 15. Review 的四层阅读法

Review 不只是找 bug。一个成熟 review 要从四层读 diff。

| 层级 | 看什么 | 常见问题 |
|------|--------|----------|
| 意图层 | 这次改动要解决什么 | diff 和任务目标不一致 |
| 行为层 | 用户可见行为是否改变 | 漏掉边界条件 |
| 结构层 | 代码组织是否变复杂 | 为小问题引入大重构 |
| 证据层 | 测试、命令、日志是否支持 | 只改代码不验证 |

### 15.1 意图层 prompt

```text
请根据当前 diff 反向解释这次改动的意图。
不要评价好坏，先回答：
1. 这次改动试图解决什么问题？
2. 哪些文件承担了主要行为变化？
3. 有没有文件看起来偏离任务目标？
```

### 15.2 行为层 prompt

```text
请从用户行为角度审查当前 diff。
重点看：
- 输入为空时发生什么
- 权限不足时发生什么
- 网络或外部服务失败时发生什么
- 旧数据或旧配置是否仍可处理
```

### 15.3 结构层 prompt

```text
请审查当前 diff 是否引入不必要复杂度。
如果有问题，请指出：
1. 哪个抽象还太早
2. 哪个函数承担了太多职责
3. 哪个改动可以缩小范围
4. 哪些重命名或搬迁不值得
```

### 15.4 证据层 prompt

```text
请检查当前 diff 的验证证据。
回答：
1. 哪些测试或命令已经支持这个改动？
2. 哪些高风险路径还没有证据？
3. 如果只补一个测试，应该补哪里？
4. 如果现在不能跑测试，应该在 PR 里怎样说明？
```

## 16. Inline comments：把反馈贴到具体行上

Inline comment 的价值是“定位”。相比一句“这里不太对”，贴在具体 diff 行上的评论能让 Codex 更容易理解你想改哪里。

### 16.1 好评论和差评论

| 差评论 | 好评论 |
|--------|--------|
| 这里优化一下 | 这里把空数组当成成功态了，请区分空结果和请求失败 |
| 逻辑不对 | 这个分支没有处理 token 过期，请沿用上面 `refreshSession` 的错误路径 |
| 改好看点 | 这个错误文案会换行挤压按钮，请缩短到一行或改成 tooltip |
| 加测试 | 请补一个 regression test 覆盖 `status === 401` 的分支 |

### 16.2 评论后还要发线程消息

只贴 inline comment 不够。你还要在主线程里告诉 Codex 怎么处理这些评论：

```text
请处理我刚才在 Review 面板里留下的 inline comments。
保持改动范围最小。
不要重构没有被评论到的代码。
处理后告诉我每条评论对应改了哪里。
```

这样 Codex 才能把评论当成一组明确任务，而不是把它们当成散落的备注。

## 17. Stage、Unstage、Revert：用 Git 动作塑造 diff

Review 面板里的 Git 动作不是装饰。它让你在提交前选择保留哪些改动。

### 17.1 Stage 的含义

Stage 是“我准备把这部分放进下一次提交”。它不等于已经提交，也不等于代码一定正确。

适合：

- 接受某个文件的改动。
- 接受某个 hunk。
- 把一个大 diff 拆成多个提交。

### 17.2 Unstage 的含义

Unstage 是“暂时不把这部分放进下一次提交”。文件内容还在，只是从暂存区拿出来。

适合：

- 提交前发现范围太大。
- 想先提交核心逻辑，再提交文档。
- 想重新组织 commit。

### 17.3 Revert 的含义

Revert 是“丢弃这部分未提交改动”。这个动作要谨慎，因为它会让本地文件回到 Git 记录里的状态。

适合：

- Codex 改错了一个文件。
- 自动生成物不该提交。
- 某个 hunk 明显偏离任务。

不适合：

- 你不确定这是不是自己手写的内容。
- 你还没看清 diff 来源。
- 你只是想暂时不提交，这时用 unstage。

### 17.4 拆提交 prompt

```text
请帮我把当前 diff 拆成建议的提交组。
不要执行 git commit。
只按逻辑分组说明：
1. 每组包含哪些文件
2. 每组建议的 commit message
3. 哪些文件还不适合提交
```

这个 prompt 特别适合 App Review 面板配合使用。

## 18. GitHub PR 上下文：App 不是凭空知道 PR

App 要显示 PR context，需要当前项目在 PR 分支上，并且有 GitHub 访问能力。通常还要安装 GitHub CLI 并通过 `gh auth login` 登录。

### 18.1 PR 上下文准备

```bash
git status
git branch --show-current
gh auth status
gh pr status
```

如果 `gh` 不可用，App 可能看不到 PR 评论、上下文或 changed files。这不是 Review 面板坏了，而是 GitHub 上下文没接上。

### 18.2 PR 评论处理 prompt

```text
请读取当前 PR 的评论和本地 diff。
先把评论分成：
1. 已经通过本地改动解决
2. 可以直接修复
3. 需要我确认产品或兼容性
4. 不建议处理并说明原因

不要发表评论，不要推送。
```

### 18.3 PR 回合制修复

```text
请只处理评论组 2 中的第一个问题。
保持改动最小。
完成后告诉我：
- 改了哪些文件
- 对应哪条 PR 评论
- 我应该在 Review 面板里看哪几处 diff
- 还剩哪些评论没处理
```

回合制的好处是降低 diff 失控概率。不要一次让 Codex 处理几十条评论，除非评论都很小且同类。

## 19. `/review` 与人工 Review 的分工

`/review` 是让 Codex 以 review 姿态看 diff，但它不能替代人。课程里要讲清楚它的强项和盲区。

| 事项 | `/review` 擅长 | 人更擅长 |
|------|----------------|----------|
| 代码层 bug | 是 | 也要看关键路径 |
| 安全敏感点 | 可以帮忙找 | 要结合业务威胁模型 |
| 测试缺口 | 是 | 判断测试投入优先级 |
| 产品取舍 | 不稳定 | 人来决定 |
| 发布节奏 | 不稳定 | 人来决定 |
| 团队规范 | 取决于 `AGENTS.md` | 人维护规则 |

### 19.1 定向 `/review`

```text
/review
重点看：
1. 是否有真实行为回归
2. 是否漏了错误状态
3. 是否有安全或权限问题
4. 是否缺少最小测试

不要评论纯风格问题，除非它会影响维护。
```

### 19.2 Review 后修复

```text
请只处理 `/review` 结果里的 high 和 medium 问题。
low 问题先列出，不要改。
每处理一个问题，说明对应的 diff 文件。
```

这能避免 Codex 被低优先级建议带偏。

## 20. PR 描述：不是讲故事，是交代风险

PR 描述要让 reviewer 快速知道三件事：为什么改、改了什么、怎么检查。

### 20.1 小修 PR 模板

```md
## Summary

- Fix checkout error handling when payment provider returns an empty response.
- Keep the existing retry behavior unchanged.

## Verification

- Ran targeted checkout tests.
- Manually checked the error message path in local dev.

## Risk

- Low. The change is limited to the error branch.
- Main success path is unchanged.
```

### 20.2 中等改动 PR 模板

```md
## Summary

- Split account settings validation into a shared helper.
- Update web and admin entry points to use the same validation result.
- Add regression coverage for expired sessions.

## User Impact

- Users now see the same error message across web and admin flows.

## Verification

- Ran account settings unit tests.
- Ran lint for the affected package.

## Review Notes

- The helper is intentionally narrow.
- No database schema changes.
```

### 20.3 不确定风险说明

```md
## Risk

- Medium. This touches login fallback behavior.
- I could verify the normal login path locally.
- I could not verify legacy SSO clients because I do not have a test account.
- Please pay special attention to `src/auth/ssoFallback.ts`.
```

诚实的风险说明比“全部正常”更有价值。

## 21. Review 排障：为什么 App 里看不到该看的东西

| 症状 | 可能原因 | 下一步 |
|------|----------|--------|
| Review 面板不可用 | 项目不是 Git 仓库 | 初始化或打开 Git 项目 |
| 看不到 PR 评论 | `gh` 未安装或未登录 | `gh auth login` |
| diff 里有奇怪旧改动 | 工作区本来不干净 | 先看 `git status` |
| Staged/Unstaged 像重复文件 | Git 暂存区状态不同 | 分别查看两边 |
| Codex 没处理 inline comment | 评论后没发线程消息 | 发明确 follow-up |
| Revert 后内容没了 | revert 丢弃了本地改动 | 以后先确认来源 |
| `/review` 太泛 | 没给 review 重点 | 用定向 prompt |

### 21.1 排查 prompt

```text
我在 Codex App Review 面板里看到的 diff 和预期不一致。
请先不要修改文件。
帮我判断：
1. 当前 diff 范围可能是什么
2. 哪些改动可能不是你刚才做的
3. 我应该先看 git status 还是切换 review scope
4. 哪些文件不应该直接 revert
```

## 22. 课堂综合案例：从 PR 评论到本地修复

完整流程：

```text
1. 打开 PR 分支。
2. 确认 `gh auth status` 正常。
3. 在 App 里查看 PR context。
4. 让 Codex 分类评论。
5. 选择一组评论进行小范围修复。
6. 用 Review 面板看 last turn changes。
7. 用 Uncommitted changes 看本地总状态。
8. Stage 想保留的 hunk。
9. 写 PR 描述。
10. 人工决定 commit 和 push。
```

对应 prompt：

```text
请帮我处理当前 PR 的评论，但一次只处理一类问题。

第一步：
- 读取 PR 评论和本地 diff。
- 把评论分类。
- 不改文件。

第二步：
- 等我选择一类评论后，再做最小修复。

第三步：
- 修复后告诉我 Review 面板应该看哪些文件。
- 不要 commit，不要 push，不要回复评论。
```

这个案例的重点是让学习者理解：Codex 可以推进 PR 回合，但合并权仍然在人手里。

## 23. 综合工坊：从 `/review` findings 到最小修复

### 23.1 第一步：运行定向 review

```text
/review
请审查当前 diff。
只看：
1. 真实行为回归
2. 安全或权限风险
3. 缺失测试
4. 超出任务范围的改动

不要评论纯格式。
```

### 23.2 第二步：分级

```text
请把 review findings 分成：
- 现在必须修
- 可以稍后修
- 需要我判断
- 不建议处理

不要修改文件。
```

### 23.3 第三步：只修一个

```text
请只处理“现在必须修”里的第一项。
保持改动最小。
如果需要改超过 2 个文件，先说明原因。
```

### 23.4 第四步：复查

```text
请复查刚才的修复是否只解决了目标 finding。
输出：
- finding
- 修改文件
- 为什么是最小修复
- 是否需要补测试
```

这个工坊的关键是把 review findings 当成队列，而不是一次全吞。

## 24. 综合工坊：PR 评论三回合

### 24.1 第 1 回合：分类评论

```text
请读取当前 PR 评论和本地 diff。
先不要改文件。
把评论分成：
1. 明确 bug
2. 测试缺口
3. 文档问题
4. 产品或兼容性问题
5. 可以解释但不一定要改的问题
```

### 24.2 第 2 回合：处理明确 bug

```text
请只处理分类 1 中最小的一条明确 bug。
不要处理其它评论。
完成后说明对应哪条评论和哪些文件。
```

### 24.3 第 3 回合：准备回复草稿

```text
请为已处理的 PR 评论草拟回复。
不要发布。
每条回复包括：
- 我改了什么
- 如何验证
- 如果没有完全处理，说明原因
```

示例：

```md
Handled this in `src/auth/redirect.ts` by preserving the existing fallback path when the session is expired. Added a regression test in `tests/auth.spec.ts`.
```

## 25. Review 设计题

### 25.1 题目 A

```text
请 review 一下，顺便把问题都修了。
```

判断：不够好。review 和修复混在一起，容易扩大范围。

改写：

```text
/review
请先只审查，不修改文件。
输出 findings 后等我选择要修哪一项。
```

### 25.2 题目 B

```text
请把当前 diff 拆成两个 commit。
```

更稳写法：

```text
请先建议如何拆成两个 commit。
列出每组文件和 commit message。
不要执行 git commit。
```

### 25.3 题目 C

```text
请 revert 所有不必要改动。
```

风险：可能丢掉用户手写内容。

改写：

```text
请先列出哪些改动可能不属于本任务。
不要 revert。
等我确认每个文件后再处理。
```

## 26. Review 进阶常见问题

### Q1：Review 面板能证明测试通过吗？

不能。Review 面板显示 diff 和 Git 状态。测试证据来自终端、线程、CI 或你运行的命令。

### Q2：Inline comments 能不能替代 prompt？

不能。Inline comments 定位具体行，线程 prompt 说明整体意图。两者配合最好。

### Q3：Stage 后是不是 Codex 就会提交？

不是。Stage 只是暂存。提交和推送仍然需要你决定或明确要求。

### Q4：为什么 staged 和 unstaged 里同一个文件出现两次？

这是 Git 正常行为。一个文件可能部分内容已暂存，部分内容仍未暂存。

### Q5：什么时候应该新开 PR，而不是继续修当前 PR？

如果发现问题已经超出当前 PR 目标，比如需要重构、改 API、改数据模型，通常应该拆新 PR 或先讨论。

## 27. Review 案例：同一个 diff 要被看三遍

一个 PR 能不能合，不只取决于“代码有没有报错”。真正的 Review 至少要经过三层阅读：作者自查、审查者查风险、合并前判断范围。Codex 的价值在于把这些阅读动作显性化，而不是替人按下合并按钮。

作者自查时，可以这样让 Codex 先把 diff 讲明白：

```text
请基于当前 diff 做作者自查。

输出：
1. 本次改动原目标是什么。
2. 每个文件为什么被修改。
3. 是否存在看起来无关的改动。
4. 我应该在 PR 描述里主动说明的风险。
5. 还缺哪些验证命令。
```

这一轮的重点是“我能不能解释自己改了什么”。如果 Codex 解释不清某个文件，通常说明这个文件要么不该在 PR 里，要么需要补充上下文。

审查者阅读时，prompt 要更尖锐：

```text
请只读审查当前 diff。

重点找：
1. 行为回归。
2. 测试没有覆盖的关键路径。
3. 错误处理、权限、兼容性或数据迁移风险。
4. PR 描述没有交代清楚的地方。

不要给泛泛建议。每个发现都要绑定文件或 diff 证据。
```

合并前再看一次范围：

```text
请判断这个 PR 是否应该拆分。

输出：
1. 核心行为改动。
2. 测试和文档改动。
3. 可能应该拆出去的顺手改动。
4. 如果不拆，合并风险是什么。
5. 如果拆，推荐拆分顺序。
```

这个三遍阅读法适合课程练习，因为读者会马上发现：Review 不是一个按钮，而是一组不同问题。作者问“我改清楚了吗”，审查者问“哪里会出事”，合并前问“这个 PR 是否太大”。同一个 diff 被这三种问题照过，质量会明显不同。

## 28. Review 作业：把一个大 diff 拆小

```text
请根据当前 diff 设计拆分方案。
输出：
1. 核心行为改动
2. 测试改动
3. 文档改动
4. 不该在本 PR 出现的改动
5. 推荐提交顺序

不要执行 git 操作。
```

要求学生说明：哪些改动可以一起提交，哪些应该拆出去。

## 29. 长案例：PR 评论回来以后，Codex 应该怎么帮你收口

很多人第一次把 Codex 接进 PR 流程时，会把 reviewer 的评论直接整段贴给 Codex，然后说“全部修掉”。这类 prompt 看起来省事，实际很容易把 PR 越修越大。更好的做法是把评论先变成任务清单，再让 Codex 只处理其中一条。

假设 reviewer 留了三类评论：

```text
1. auth redirect 测试失败，登录后没有回到原页面。
2. 这里的变量名太含糊，看不出是不是 callback URL。
3. 这个 PR 顺手改了 toast 样式，和认证逻辑无关。
```

第一轮不要修，先让 Codex 分类：

```text
请根据 reviewer 评论和当前 diff 做只读分类。

输出：
1. 必须在本 PR 修的阻塞问题。
2. 可以在本 PR 顺手修的小问题。
3. 应该拆出当前 PR 的无关改动。
4. 每条评论对应哪些文件或测试。

不要修改文件。
```

理想输出应该把第 1 条归为阻塞问题，第 2 条归为小问题，第 3 条归为拆分问题。接下来只处理阻塞问题：

```text
只处理 auth redirect 测试失败。

边界：
1. 只改 redirect 相关逻辑和对应测试。
2. 不改 toast 样式。
3. 如果变量名小改有助于解释 redirect，可以一起改，但要说明原因。
4. 修改后运行最相关的测试。
5. 输出改动文件和剩余风险。
```

修完以后，不要急着提交。让 Codex 站在 reviewer 的位置读一次：

```text
请只读审查刚才的改动。

重点看：
1. reviewer 的第 1 条评论是否被解决。
2. 是否意外处理了第 3 条 toast 样式。
3. 测试是否覆盖“登录前访问受保护页面，登录后回到原页面”。
4. 还有哪些地方需要人工打开页面确认。
```

最后更新 PR 描述。不要写“fix comments”这种看不出行为的摘要。

```md
## Summary

- Preserve redirect target during auth login flow.
- Add regression coverage for protected-page redirect after login.
- Leave unrelated toast styling change out of this fix.

## Verification

- Ran auth redirect test.
- Reviewed diff to confirm only auth redirect files changed.

## Review Notes

- Addressed reviewer comment about failed redirect behavior.
- Did not handle toast styling in this PR because it is unrelated.

## Risk

- Manual browser check is still useful for the full login flow.
```

这个案例的关键不是 prompt 多漂亮，而是顺序对：先分类，再窄修，再复核，再说明。Codex 在这里像一个能读 diff 的协作者，但 PR 的边界仍然由人来守。

## 30. Review 错误恢复：当 Codex 把 PR 修大了怎么办

如果 Codex 已经把一个小 PR 修成了大 diff，第一反应不要继续问“能不能优化一下”。先把现场固定住。

```text
请只读分析当前 diff。

我怀疑这个 PR 已经超出原目标。
请输出：
1. 和原目标直接相关的改动。
2. 可能是顺手改的改动。
3. 需要拆出去的改动。
4. 哪些文件应该保留，哪些文件应该人工回退或另开任务。

不要执行 git 操作。
```

如果输出里出现“顺手重构”“格式化大量文件”“改了公共组件但 PR 目标不是公共组件”，就先停止写代码。接着让 Codex 帮你设计恢复路线：

```text
请给出恢复路线，不要执行。

目标：
1. 保留 auth redirect 的最小修复。
2. 把 toast 样式和公共组件重构拆出去。
3. 说明应该如何用 Review 面板逐文件检查。
4. 给出 PR 描述该怎么解释这次收窄。
```

App Review 面板在这里比单纯命令行更有优势：你可以逐个文件看 diff，选择哪些文件应该保留，哪些不该进入本次 PR。Codex 可以解释和建议，但 stage、revert、commit 这类 Git 动作要由你明确决定。

一个收窄后的 PR 说明可以这样写：

```md
## Summary

- Narrow this PR back to the auth redirect regression.
- Remove unrelated styling and shared component refactor from this change.

## Why

The first pass included unrelated cleanup. This update keeps the PR reviewable and leaves broader UI cleanup for a separate task.

## Verification

- Rechecked diff file by file in Review.
- Ran the auth redirect test again after narrowing.
```

这段写法有两个好处：它没有掩盖“之前修大了”，也没有把 reviewer 拉进一堆无关讨论。PR 越小，Codex 越容易帮你看清楚；PR 越大，Codex 越容易给出漂亮但泛化的建议。

## 31. Review prompt 片段库：按真实场景提问

Review prompt 不要只写“帮我看看”。下面这些片段可以按场景复制。

改动很小，但你怕漏测试：

```text
请只读审查当前 diff。
重点找：有没有应该补测试但没有补的路径。
不要评论命名、格式或风格，除非它会影响行为理解。
```

PR 很大，你要先拆：

```text
请把当前 diff 按 PR 拆分。
输出每个建议 PR 的目标、文件范围、依赖顺序和不应该混在一起的原因。
不要修改文件。
```

 reviewer 评论很多，你要排序：

```text
请把这些 PR 评论按处理顺序排序。
分类为：阻塞合并、需要澄清、可以顺手修、应该拆出本 PR。
每条评论都说明对应文件和建议下一步。
```

你准备回应 reviewer：

```text
请帮我起草 PR 回复。
要求：
1. 逐条回应 reviewer 关心的问题。
2. 说明已经改了什么。
3. 说明哪些没有改以及原因。
4. 不要承诺没有跑过的测试。
```

你要从本地 diff 写 PR 描述：

```text
请基于当前 diff 写 PR 描述。
包含 Summary、User Impact、Verification、Risk。
Verification 只能写已经在终端或线程里出现过的命令，不要编造。
```

你担心安全或权限风险：

```text
请只读审查当前 diff 的安全风险。
重点看认证、授权、敏感日志、外部请求、配置默认值和错误处理。
每个发现都绑定具体文件或 diff 位置。
```

好的 Review prompt 会主动收窄问题。你问得越像真实 reviewer，Codex 的输出越像可处理反馈；你问得越泛，输出越容易像一篇代码改进散文。

## 32. Review 会议案例：把争论变成可处理 diff

团队 Review 里常见一种低效争论：有人说“这个 PR 看起来不太稳”，有人说“我觉得还好”。这种争论如果没有文件证据，很难收口。Codex 可以把讨论变成结构化 diff 问题。

会议前先让 Codex 做只读准备：

```text
请为当前 PR 准备 Review 会议材料。

输出：
1. 这个 PR 的主目标。
2. 改动文件按功能分组。
3. 最需要会议讨论的 3 个风险。
4. 不需要会议讨论、可以异步处理的问题。
5. 需要作者现场确认的问题。

不要修改文件。
```

会议中如果出现争论，不要让 Codex 直接裁判。让它整理双方观点：

```text
请把这段 Review 讨论整理成可处理问题。

讨论摘要：
- A 担心 auth redirect 会影响 SSO。
- B 认为本 PR 只改普通登录，不涉及 SSO。
- QA 想知道是否需要手测移动端。

输出：
1. 哪些是事实问题，需要看代码或测试。
2. 哪些是范围问题，需要决定是否进本 PR。
3. 哪些是验证问题，需要补测或手测。
4. 下一步最小行动。
```

整理后，通常会得到三类任务：

```text
事实问题：
- SSO 是否复用同一个 redirect helper。

范围问题：
- 本 PR 是否承诺覆盖 SSO。

验证问题：
- 移动端登录后 redirect 是否需要手测。
```

接着让 Codex 只查事实问题：

```text
请只读检查 SSO 是否复用当前修改的 redirect helper。
只回答文件证据和调用链。
不要提出修复方案。
```

最后把会议结果写回 PR：

```md
## Review Follow-up

- Confirmed SSO does / does not reuse the modified redirect helper.
- This PR covers normal login redirect only.
- Mobile redirect path still needs manual check before merge.
- SSO-specific behavior will be handled separately if needed.
```

这类用法能让 Codex 从“帮我争赢 Review”变成“帮团队把争论落到文件、范围和验证”。这才是 Review 工作流真正的效率提升。

## 33. Review 质量练习：让学生改写坏反馈

坏反馈：

```text
这个代码不太好，建议优化。
```

要求改成可处理反馈：

```text
当前 `redirect.ts` 在 callback URL 缺失时直接回到 `/`。
如果用户从受保护页面进入登录页，登录后可能丢失原目标。
建议补一个测试：访问 `/settings` -> 登录 -> 回到 `/settings`。
```

坏反馈：

```text
这里有安全问题。
```

改成：

```text
当前改动把 redirect target 从 query string 直接传入 navigation。
请确认是否限制为站内路径，避免开放跳转。
需要检查文件：`src/auth/redirect.ts`。
```

坏反馈：

```text
测试不够。
```

改成：

```text
测试只覆盖默认 redirect，没有覆盖带 callback URL 的路径。
建议新增一条 regression test，证明登录后保留原目标页面。
```

给 Codex 的练习 prompt：

```text
请把下面 5 条模糊 Review 反馈改写成可处理反馈。

要求：
1. 每条包含具体行为。
2. 尽量绑定文件或测试。
3. 说明为什么重要。
4. 不写人格化评价。
5. 不要求作者做大范围重构。
```

这个练习能让读者理解：Review 的质量不只取决于谁发现问题，也取决于问题是否能被作者准确处理。Codex 很适合训练这件事，因为它可以反复把模糊语言改成可执行反馈。

## 34. Review 收口案例：把 findings 变成修复队列

`/review` 或人工 Review 之后，最容易出问题的地方是 findings 太多。作者一着急，就会说“都修了吧”。结果是小 PR 被修成大 PR。更稳的做法是把 findings 变成修复队列。

示例 findings：

```text
1. callback URL 没有测试。
2. redirect helper 没有限制站外 URL。
3. README 里的登录流程图过期。
4. toast 样式被顺手改了。
5. 变量名 `next` 不清楚。
```

第一步，分类：

```text
请把这些 Review findings 转成修复队列。

分类：
1. 本 PR 必须修。
2. 本 PR 可以小改。
3. 应该拆到后续 PR。
4. 只需要文档或说明。
5. 需要先问 reviewer。

每条都说明原因。
不要修改文件。
```

可能输出：

```text
本 PR 必须修：
- callback URL 测试。
- 站外 URL 限制。

本 PR 可以小改：
- 变量名 `next`。

后续 PR：
- README 流程图。
- toast 样式。
```

第二步，只修第一组：

```text
只处理“本 PR 必须修”的两条：
1. callback URL 测试。
2. 站外 URL 限制。

不要处理 README、toast 样式或其他重命名。
如果发现必须改其他文件，先暂停说明。
```

第三步，修完后再复核队列：

```text
请检查当前 diff 是否只处理了修复队列中的“本 PR 必须修”。
输出：
1. 已解决 findings。
2. 未解决但可接受后续处理的 findings。
3. 意外进入当前 diff 的改动。
4. PR 描述中应该如何说明。
```

最后 PR 回复：

```md
Addressed:
- Added callback URL regression coverage.
- Guarded redirect target against external URL usage.

Left for follow-up:
- README flow diagram update.
- Toast style cleanup.

Not changed:
- Broader auth refactor.
```

这个收口案例会让读者明白：Review findings 不是待办清单的同义词。它们需要排序、拆分和解释。Codex 可以帮你整理队列，但不能替你决定一个 PR 应该承担多少范围。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

- [ ] 能在Review面板中逐项检查文件列表、diff、命令记录
- [ ] 知道用带重点描述的`/review`发现特定问题
- [ ] 不跳过Review直接合并
- [ ] 完成过App到GitHub PR的完整流程
- [ ] PR描述包含Summary、Verification、Risk
- [ ] 不在main分支上直接提交
- [ ] 知道什么时候用Cloud处理PR，什么时候留在App

**全部勾选后即掌握 Codex Review 与 PR 工作流。**

---

## 附录

### A. PR描述模板

```markdown
## Summary
- [改动概述]

## Verification
- [验证命令]

## Risk
- [风险评估]
```

### B. Review面板检查清单

| 区域 | 要看什么 |
|------|---------|
| 文件列表 | 是否有范围外文件 |
| 单文件diff | 是否有无关改动 |
| 命令记录 | 是否真的运行了验证命令 |
| 行内评论 | 能否针对性修复 |
| Stage/Commit | 是否由你确认 |

### C. 推荐学习资源

- **Codex App Review 官方文档**：https://developers.openai.com/codex/app/review
- **本系列上一篇**：[CX-09 Automations](./CX-09-Codex-Automations后台任务完整指南.md)
- **本系列下一篇**：[CX-11 Web / Cloud 辅助](./CX-11-Codex-Web-Cloud辅助指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-11 Web / Cloud：App 的云端辅助路径](./CX-11-Codex-Web-Cloud辅助指南.md)。
