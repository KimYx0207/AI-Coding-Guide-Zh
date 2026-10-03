# Hooks系统完整指南：自动化工作流的终极武器

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：4-6小时
> - **难度等级**：⭐⭐ 入门级（有Claude Code基础即可）
> - **更新日期**：2026年10月3日
> - **适用版本**：既有说明保留 v2.1.270 历史基线；新增 Mods 区别与治理适用于 v2.1.287+，参考官方说明核对于 2026-10-03。
> - **前置要求**：已完成Claude Code安装和基础使用

---

## 本课学习目标

我写 Hooks 这类内容时不会只给脚本，重点是让团队知道什么时候该拦、什么时候不该拦。

> **2026-06-18 操作口径**：v2.1.178 起权限规则支持 `Tool(param:value)` 形式，例如只允许特定模型的 `Agent(model:opus)`；v2.1.176 修复了 Hook `if` 条件的路径匹配。团队课程里讲 Hook 时，要把“匹配范围”和“参数级权限”分开演示，避免只用一个大而全的 allow/deny 例子。

> **2026-09-14 当前基线（v2.1.270）**：v2.1.251 新增 `PreModelSwitch`（切换前允许、拒绝或请求确认）和 `PostModelSwitch`（切换后补充上下文）。两个事件不能互换：后者不负责撤销已经完成的切换。`SessionStart` 的 resume hook 还可取得会话陈旧度和预估重新缓存成本。`PermissionRequest` 在 `--print` 模式下不触发的问题已在 v2.1.268 修复；阻断型 `Stop` 导致下一轮丢失推理、部分模型错过缓存的问题已在 v2.1.259 修复。v2.1.268 还修复了 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 对未单独配置 `timeout` 的 SessionEnd hook 不生效的问题。来源：[官方 Hooks 文档](https://code.claude.com/docs/en/hooks)与[changelog](https://code.claude.com/docs/en/changelog)。

完成本课学习后，你将能够：

1. **理解Hooks的核心价值**：掌握Hooks与传统提示词的本质区别
2. **配置第一个Hook**：5分钟内完成最简单的Hook配置并看到效果
3. **按事件族理解Hooks**：理解工具、会话、任务、失败、文件系统、压缩和 Elicitation 等事件面
4. **实现自动化工作流**：Git提交检查、代码格式化、文件保护等实战场景
5. **排查Hook故障**：解决大多数常见配置和执行问题
6. **安全使用Hooks**：理解安全风险并正确配置权限

---

## 学习路径导航（先看这里！）

> **根据你的情况选择学习路径**：这是一篇3000+行的长教程，不用全看！根据你的目标选择路径。

### 路径A：快速上手（30分钟）

**适合人群**：急着体验Hooks，想快速配一个看效果

**只看这些章节**（其他跳过）：

```
✅ 术语表（5分钟） - 快速了解Hook核心概念
✅ 第一部分1.1-1.2：Hooks简介（5分钟） - 理解Hook是什么
✅ 第二部分：5分钟快速开始（15分钟） - 配置第一个Hook
✅ 第三部分3.1：PreToolUse基础（5分钟） - 最常用的Hook类型
```

**30分钟后你能达到**：成功配置第一个Hook，Claude Code能自动执行你的脚本

---

### 路径B：完整学习（4-6小时）

**适合人群**：想深入理解Hooks，掌握常用事件和高级用法

**学习顺序**：从头到尾所有章节

**建议分段学习**：
- 第1天（2小时）：第1-3部分（理解+常用事件）
- 第2天（2小时）：第4-5部分（实战场景+故障排查）
- 第3天（1小时）：第6-7部分（FAQ+附录）

---

### 路径C：问题排查（10分钟）

**适合人群**：Hook配置出问题，需要快速解决

**直接跳到这些章节**：

```
🔧 第五部分：故障排查 - 按错误类型查找解决方案
🔧 第六部分：FAQ - 20个常见问题解答
```

**使用方法**：
1. 按 `Ctrl + F` 搜索你的错误信息关键词
2. 找到对应的Q&A
3. 按步骤解决

---

### 路径D：专项学习（30-60分钟/主题）

**适合人群**：已经会配置Hook，想学习特定功能

| 想学什么 | 看哪几节 | 预计时间 |
|----------|---------|---------|
| **Git自动化** | 第四部分4.1节 | 45分钟 |
| **代码格式化** | 第三部分3.2节的自动代码格式化示例 | 30分钟 |
| **文件保护** | 第三部分3.1节 | 20分钟 |
| **提示词优化** | 第三部分3.3节 | 30分钟 |
| **安全最佳实践** | 第一部分1.4节 + 第五部分 | 40分钟 |

---

## 术语表（小白必读）

在开始之前，先了解这些关键术语。**用生活类比帮助理解**：

| 术语 | 英文全称 | 通俗解释 | 生活类比 |
|------|----------|----------|----------|
| **Hook** | - | 在特定事件发生时自动执行的脚本 | 汽车传感器（检测到碰撞自动弹安全气囊） |
| **PreToolUse** | Pre Tool Use | 工具调用**前**触发的Hook | 机场安检门（登机前检查） |
| **PostToolUse** | Post Tool Use | 工具调用**后**触发的Hook | 快递签收后的自动通知 |
| **UserPromptSubmit** | User Prompt Submit | 用户输入提交时触发的Hook | 邮件发送前的拼写检查 |
| **Notification** | - | 通知事件触发的Hook | 手机APP推送通知 |
| **SessionStart** | Session Start | 会话开始时触发的Hook | 开机自动启动程序 |
| **SessionEnd** | Session End | 会话结束时触发的Hook | 关机前自动保存 |
| **Stop** | - | AI停止响应时触发的Hook | 紧急刹车后的状态保存 |
| **WorktreeCreate** 🆕 | Worktree Create | 工作树**创建**时触发的Hook | 新开一个平行工作台时的初始化 |
| **WorktreeRemove** 🆕 | Worktree Remove | 工作树**删除**时触发的Hook | 关闭平行工作台时的清理 |
| **Matcher** | - | 匹配规则，决定Hook对哪些工具生效 | 筛选器（只检查特定行李） |
| **Decision** | - | PreToolUse Hook的返回决策 | 安检结果（放行/拦截/询问） |
| **stdin** | Standard Input | 标准输入，Hook接收数据的方式 | 传送带送入检查口 |
| **stdout** | Standard Output | 标准输出，Hook返回结果的方式 | 检查结果显示屏 |
| **stderr** | Standard Error | 标准错误输出；退出0时只进debug日志，其他退出码按事件显示或反馈 | 排障日志或阻断理由 |
| **timeout** | - | 超时时间；到期后的流程按事件和处理器决定 | 限时检查 |
| **JSON** | JavaScript Object Notation | 一种通用的数据格式，用花括号`{}`组织数据，settings.json配置文件就是JSON格式 | 标准化的表格模板 |
| **`~`（波浪号）** | Home Directory | 用户的"家目录"，macOS是`/Users/用户名`，Linux是`/home/用户名`，Windows对应`C:\Users\用户名` | 你电脑上"我的文档"的上级目录 |

---

## 第一部分：Hooks简介（5分钟理解）


### 先分清两种 Hooks

这篇的主要练习是 **settings hooks**：你在设置文件里登记事件，让 Claude Code 运行脚本、发 HTTP 请求，或调用相应处理器。v2.1.287 新增的 **Mods 函数 hooks** 则在 Claude Code 进程内运行 JavaScript/TypeScript，使用自己的事件名和 API，还能修改界面。两者都叫 hook，但配置方式不同，不是往现有 `settings.json` 填一个 `type: function`。

你只想自动格式化或记录一次工具操作，可以继续用本篇脚本；想增加界面计数或由代码直接处理自定义命令，再做[08 的 Mods 练习](08-Plugins生态完整指南.md#45-做一个-mods让工具调用次数显示出来)。Mods 不会让现有 settings hooks 退役，权限和组织控制也需要分别检查。依据：[官方比较说明](https://code.claude.com/docs/en/plugins/mods/overview#compare-mods-settings-hooks-skills-and-mcp-servers)。

### 1.1 Hooks是什么

> **一句话理解**：Hooks是Claude Code的"自动化传感器"，在特定事件发生时自动执行你的脚本，实现可靠的自动化。

#### 为什么需要Hooks？

**没有Hooks之前（靠AI"记住"）**：

```
问题：AI有时会"忘记"你的要求

你：每次写代码后帮我运行格式化
Claude：好的！（这次记住了）

...10分钟后...

Claude：代码写好了！
你：等等，你忘了格式化！
Claude：抱歉，我忘了...
```

**配置了 Hooks 之后（匹配事件自动触发）**：

```
解决方案：不依赖AI记忆，配置Hook后自动执行

配置PostToolUse Hook → 监听Write工具 → 自动运行格式化脚本

Claude：代码写好了！
[Hook自动触发：运行 prettier --write xxx.js]
结果：事件匹配后运行格式化脚本；是否成功要检查工具依赖、退出结果和文件内容
```

> **生活类比**：
> - **没有Hooks**：靠人记住每次开车前检查轮胎（经常忘）
> - **有Hooks后**：汽车传感器自动检测胎压，异常自动报警（更可靠）

#### Hooks的核心价值

| 对比维度 | 提示词方式 | Hooks方式 |
|----------|-----------|-----------|
| **可靠性** | 依赖AI是否执行要求 | 匹配事件后自动调用处理器；仍需处理失败和超时 |
| **一致性** | 每次可能不同 | 每次完全相同 |
| **自动化** | 需要AI主动执行 | 事件触发自动执行 |
| **团队协作** | 每人都要提醒AI | 配置一次，全员生效 |
| **适用场景** | 灵活建议 | 强制规则 |

### 1.2 Hooks能做什么（6个实际案例）

**案例1：文件保护（PreToolUse）**
```
场景：禁止Claude修改production目录下的文件

Hook触发：Claude尝试Write(file_path="production/config.js")
Hook检查：路径包含"production/"
Hook决策：deny（拒绝）
结果：Claude收到错误提示，文件未被修改
```

**案例2：代码格式化（PostToolUse）**
```
场景：每次保存代码后自动格式化

Hook触发：Claude成功执行Write(file_path="src/app.js")
Hook执行：运行 prettier --write src/app.js
结果：代码自动格式化，无需手动操作
```

**案例3：提示词优化（UserPromptSubmit）**
```
场景：自动在写作任务后追加写作规范

用户输入："帮我写一篇关于AI的文章"
Hook检测：输入含任一写作关键词（如“写”“文章”）
Hook追加："\n\n## 写作规范\n1. 风格：接地气\n2. 字数：1500字"
Claude收到：原始输入 + 写作规范
```

**案例4：Git提交检查（PreToolUse + Bash）**
```
场景：提交前自动检查代码质量

Hook触发：Claude执行Bash(command="git commit -m xxx")
Hook执行：运行lint检查、测试、敏感信息扫描
Hook决策：全部通过 → allow；有问题 → deny
结果：这个 Bash 命令在检查失败时被拦截；其他提交渠道需另外配置检查
```

**案例5：会话初始化（SessionStart）**
```
场景：启动Claude Code时自动加载项目配置

Hook触发：Claude Code启动
Hook执行：检查Python依赖是否安装
结果：缺少依赖时自动提示安装命令
```

**案例6：桌面通知（Notification）**
```
场景：Claude需要用户确认时发送桌面通知

Hook触发：Claude发送通知请求用户确认
Hook执行：调用系统通知API
结果：用户收到桌面弹窗，不会错过重要确认
```

### 1.3 Hooks执行流程

**完整生命周期图**：

```
用户输入
    ↓
[UserPromptSubmit Hook] ← 可以补充上下文或阻止提交
    ↓
Claude处理提示词
    ↓
决定调用工具（如Write）
    ↓
[PreToolUse Hook] ← 可以允许/拒绝/询问
    ↓
执行工具（如Write）
    ↓
[PostToolUse Hook] ← 可以执行后处理
    ↓
返回结果给用户
```

**当前常见 Hook 事件族与触发时机（概念快照，不等于完整清单）**：

| Hook类型 | 触发时机 | 典型用途 | 可否阻止后续操作 |
|----------|----------|----------|-----------------|
| **UserPromptSubmit** | 用户输入提交后 | 提示词优化、敏感词过滤 | ✅ 是 |
| **PreToolUse** | 工具调用前 | 权限校验、参数验证 | ✅ 是 |
| **PostToolUse / PostToolUseFailure** | 工具调用成功后 / 失败后 | 格式修复、自动测试、失败告警 | ❌ 否 |
| **Notification** | 通知发送时 | 日志记录、桌面通知 | ❌ 否 |
| **SessionStart** | 会话开始时 | 环境初始化 | ❌ 否 |
| **SessionEnd** | 会话结束时 | 清理临时文件 | ❌ 否 |
| **Stop** | Claude 准备结束响应时 | 完成条件校验 | ✅ 可要求继续 |
| **StopFailure** | API 错误导致回合停止时 | 错误告警、记录失败 | ❌ 无决策控制 |
| **TaskCreated / TaskCompleted** | 任务创建 / 标记完成时 | 创建校验、完成条件校验 | ✅ 可回滚创建 / 阻止标记完成 |
| **PermissionDenied** | 权限被拒绝时 | 审计、自动补救提示 | ❌ 否 |
| **PreCompact** | 上下文即将压缩时 | 保存关键上下文、压缩前校验 | ✅ 可阻止压缩 |
| **PostCompact** | 上下文压缩完成后 | 记录压缩摘要 | ❌ 不撤销压缩 |
| **CwdChanged / FileChanged** | 工作目录切换 / 文件变化时 | 同步环境、触发检查 | ❌ 否 |
| **Elicitation** | MCP 请求额外交互输入时 | 接受、拒绝或取消请求 | ✅ 可拒绝请求 |
| **ElicitationResult** | 用户响应交互输入后、返回 MCP 前 | 验证或修改响应 | ✅ 可拒绝响应 |

> 💡 **记忆方式**：先记三大高频入口 `UserPromptSubmit`、`PreToolUse`、`PostToolUse`，再按“失败 / 任务 / 文件 / 压缩 / 交互”五个补充事件族扩展。

### 1.4 安全警告（重要！）

> ⚠️ **严重警告**：Hooks可以执行**任意Shell命令**，这意味着配置不当可能导致：
> - 文件被删除或修改
> - 敏感信息泄露
> - 系统被恶意脚本攻击

**安全最佳实践**：

| 风险 | 防护措施 |
|------|---------|
| **恶意脚本** | 只运行你信任的脚本，不要从不明来源复制配置 |
| **权限过大** | 脚本只请求必要的权限，避免使用sudo |
| **敏感信息** | 不要在脚本中硬编码密码/Token |
| **无限循环** | 设置合理的timeout，避免脚本卡死 |
| **团队配置** | 代码审查.claude/settings.json变更 |

**配置检查清单**：

```
□ 脚本来源可信吗？（自己写的/官方示例/信任的开源）
□ 脚本权限最小化了吗？（不需要sudo就不用）
□ 敏感信息用环境变量了吗？（不硬编码）
□ 设置了合理的timeout吗？（防止卡死）
□ 团队成员都知道这个Hook吗？（透明度）
```

---

> **v2.1.139→v2.1.158 关键更新**：Hook exec form 支持 `args: string[]`，避免路径占位符被 shell quoting 破坏；`PostToolUse` 支持 `continueOnBlock`；Hook JSON 输出新增 `terminalSequence`；`Stop` / `SubagentStop` 输入可包含 `background_tasks` 与 `session_crons`。v2.1.152 又补充了 `SessionStart.reloadSkills`、`hookSpecificOutput.sessionTitle` 和 `MessageDisplay` hook，适合在会话启动时安装/刷新 Skills、设置标题，或在展示阶段隐藏/转换助手消息文本。

## 第二部分：5分钟快速开始（立即见效）


> **本节目的**：用最快速度配置第一个Hook，让你立即看到效果！
>
> ⏱️ **预计时间**：5-10分钟

### 2.1 配置第一个Hook（最简单版本）

**为什么选这个示例？**

- ✅ 最简单，只需要3个文件
- ✅ 效果直观，立即看到输出
- ✅ 只用 Python 标准库；先安装 Python 3，并确认终端中的 `python --version` 可用。若本机只有 `python3`，后续配置和测试统一改用 `python3`

#### 步骤1：创建Hook脚本目录

**这一步要做什么**：在项目根目录创建 `.claude/hooks/` 目录

**Windows系统（PowerShell）：**
```powershell
# 进入你的项目目录
cd C:\你的项目路径

# 创建hooks目录
New-Item -ItemType Directory -Path ".claude\hooks" -Force
```

**macOS/Linux系统：**
```bash
# 进入你的项目目录
cd ~/你的项目路径

# 创建hooks目录
mkdir -p .claude/hooks
```

**验证是否成功：**
```bash
# 检查目录是否存在
ls .claude/hooks
# 应该显示空目录（暂时没有文件）
```

#### 步骤2：创建最简单的Hook脚本

**这一步要做什么**：创建一个Python脚本，在每次Write工具执行后打印提示

**创建文件 `.claude/hooks/post-write-hello.py`**：

> 💡 **你有两种选择**：
>
> **选择A：在Claude Code对话框里说人话（推荐新手）**
>
> ```
> 帮我创建.claude/hooks/post-write-hello.py文件，内容是一个PostToolUse Hook脚本，在Write工具执行后打印提示信息
> ```
>
> （换行用 `Shift + Enter`，最后按 `Enter` 发送）
>
> Claude Code会自动帮你创建正确格式的文件！
>
> **选择B：在终端里用命令行（熟悉命令行的用户）**
> 见下方PowerShell/Bash代码

**Windows（PowerShell）：**
```powershell
@'
#!/usr/bin/env python3
"""
最简单的PostToolUse Hook示例
每次Write工具执行后记录日志
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# 从stdin读取工具执行信息
try:
    input_data = json.loads(sys.stdin.read())
except:
    sys.exit(0)

# 获取工具名称和文件路径
tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', '')

# 只处理Write工具
if tool_name == 'Write':
    # PostToolUse Hook执行后处理任务
    # 本示例只写日志，不打印成功消息
    # PostToolUse 可通过 JSON 的 systemMessage 显示消息，
    # 或用 additionalContext 给 Claude 补充上下文
    log_file = Path.home() / '.claude' / 'hooks' / 'post-write.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] ✅ 文件已保存: {file_path}\n")

sys.exit(0)
'@ | Out-File -FilePath ".claude\hooks\post-write-hello.py" -Encoding utf8
```

**macOS/Linux：**
```bash
cat > .claude/hooks/post-write-hello.py << 'EOF'
# 粘贴上方 Windows 示例中 @' 和 '@ 之间的完整 Python 脚本
EOF

# 本例由 Python 解释器读取脚本，不要求 chmod +x
# 只有直接执行脚本路径时，才需要执行权限和有效的 shebang
```

这两个平台使用的是同一份 Python 脚本，差别只在写入文件的命令；本例由 Python 解释器读取脚本，不要求执行位。不要维护两份略有差异的 Hook 代码，否则排查时很容易把平台问题误判成脚本问题。

**验证脚本创建成功：**
```bash
# 查看文件内容
cat .claude/hooks/post-write-hello.py
# 应该显示你刚才写入的Python代码
```

#### 步骤3：配置settings.json

**这一步要做什么**：告诉Claude Code在PostToolUse时运行你的脚本

**创建或编辑 `.claude/settings.json`**：

下面是一份新建文件示例。如果文件已存在，把对应事件合并进现有 `hooks`，保留 permissions、env 等其他设置；不要直接覆盖整个文件。后续所有配置示例也按这个合并方式使用。

> 💡 **你有两种选择**：
>
> **选择A：在Claude Code对话框里说人话（推荐新手）**
>
> ```
> 帮我创建.claude/settings.json配置文件，配置PostToolUse Hook监听Write工具并运行post-write-hello.py脚本
> ```
>
> （换行用 `Shift + Enter`，最后按 `Enter` 发送）
>
> Claude Code会自动帮你创建正确格式的配置文件！
>
> **选择B：在终端里用命令行（熟悉命令行的用户）**
> 见下方PowerShell/Bash代码

**Windows（PowerShell）：**
```powershell
@'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-write-hello.py"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
'@ | Out-File -FilePath ".claude\settings.json" -Encoding utf8
```

**macOS/Linux：**
```bash
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-write-hello.py"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
EOF
```

> 💡 **配置说明**：
> - `"PostToolUse"`：Hook类型，工具执行后触发
> - `"matcher": "Write"`：只匹配Write工具
> - `"command"`：要执行的脚本命令
> - `"timeout": 10`：超时10秒

#### 步骤4：启动Claude Code并测试

**这一步要做什么**：重启Claude Code，让它读取新配置

```bash
# 在项目目录启动Claude Code
claude
```

**测试命令**：

```
你：帮我创建一个test.txt文件，内容是"Hello Hooks!"
```

**预期结果**：

Claude 用 Write 创建文件后，这份脚本会把带时间戳的文件路径追加到 `~/.claude/hooks/post-write.log`，不会打印“Hook触发成功”。

```bash
cat ~/.claude/hooks/post-write.log
# 找到本次运行新增的一行：带当前时间戳和 test.txt 的实际路径
```

PowerShell 可用 `Get-Content "$HOME/.claude/hooks/post-write.log"`。确认本次新增记录才是这个示例的验证依据，不要求界面出现固定成功文案。

### 2.2 验证Hook工作正常

**完整验证清单**：

- [ ] `.claude/hooks/` 目录存在
- [ ] `.claude/hooks/post-write-hello.py` 文件存在且内容正确
- [ ] `.claude/settings.json` 文件存在且JSON格式正确
- [ ] 已安装 Python 3，配置使用本机可用的解释器命令
- [ ] Claude Code启动时没有报错
- [ ] 让 Claude 用 Write 创建文件后，日志出现本次新增记录

**如果日志没有新增记录**：

1. **检查JSON格式**：
```bash
# 验证JSON格式是否正确
python -c "import json; json.load(open('.claude/settings.json'))"
# 如果没报错说明格式正确
```

2. **检查Python是否可用**：
```bash
python --version
# 应该显示Python 3.x
```

3. **手动测试脚本**：
```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.txt"}}' | python .claude/hooks/post-write-hello.py
# 不会打印消息；测试后查看 ~/.claude/hooks/post-write.log 是否新增 test.txt 记录
```

### 2.3 恭喜完成第一个Hook！

**你刚才完成了什么？**

1. ✅ 创建了Hook脚本目录
2. ✅ 编写了第一个Hook脚本
3. ✅ 配置了settings.json
4. ✅ 验证了Hook正常工作

**接下来可以**：

- 继续学习各类 Hook 事件（第三部分）
- 学习实战应用场景（第四部分）
- 遇到问题查看故障排查（第五部分）

---

## 第三部分：常用 Hook 事件详解


> **本节目的**：掌握常用 Hook 事件的用法与控制边界
>
> ⏱️ **预计时间**：1.5-2小时

### 3.1 PreToolUse（工具调用前）

> **一句话理解**：PreToolUse就像"安检门"，在工具执行前检查是否允许通过。

#### 触发时机

在Claude准备调用工具（如Write、Edit、Bash）时，**但尚未执行**。

#### 输入参数（通过stdin的JSON）

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "C:/project/src/app.js",
    "content": "console.log('Hello World');"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `tool_name` | string | 工具名称（Write, Edit, Bash, Read等） |
| `tool_input` | object | 工具的输入参数 |

#### 决策输出（通过stdout的JSON）

PreToolUse Hook可以返回**决策指令**控制工具是否执行。

> **新旧API并存**：v2.1.49+ 推荐使用新版 `hookSpecificOutput.permissionDecision` 字段，旧版 `decision` 字段仍然支持但已废弃。

**新版API（推荐）** — 通过 `hookSpecificOutput.permissionDecision` 字段：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "禁止修改production目录下的文件"
  }
}
```

`hookEventName` 必填，拒绝原因写在同级的 `permissionDecisionReason`，不要写成顶层 `message`。

**旧版API（已废弃但仍支持）** — 通过 `decision` 字段：

```json
{
  "decision": "block",
  "reason": "禁止修改production目录下的文件"
}
```

**新版决策值**（`hookSpecificOutput.permissionDecision`）：

| 决策值 | 说明 | 工具是否执行 |
|------------|------|-------------|
| `"allow"` | 允许匹配调用跳过常规权限询问；仍受系统保护例外约束 | 通常执行，例外需确认 |
| `"deny"` | 拒绝执行，原因会反馈给Claude | ❌ 否 |
| `"ask"` | 暂停，询问用户决定 | 🤔 等待用户决定 |
| 无输出 | 不做决策，交给正常权限流程 | 按权限设置决定 |

`allow` 的边界要和实际操作一起看。v2.1.287 起，整工具 `Bash` allow 或 Hook 的允许决策，不会直接放行向 Claude 或宿主凭据存储等系统保护文件的 shell 写入，这类调用仍会要求人工确认。通过仓库已提交的符号链接写到敏感文件或工作树外时，也会说明最终写入位置并等你决定。看到提示时先核对目的与实际目标，不能把“Hook 返回 allow”当成所有写入都已获准。依据见[官方 2.1.287 权限变化](https://github.com/anthropics/claude-code/releases/tag/v2.1.287)。

**旧版决策值**（`decision`，已废弃）：

| 旧版值 | 等同于新版 | 说明 |
|--------|-----------|------|
| `"approve"` | `"allow"` | 允许执行 |
| `"block"` | `"deny"` | 拒绝执行 |

> **PostToolUse 和 UserPromptSubmit 的决策值**：两者都可返回 `"block"`，但含义不同。UserPromptSubmit 可以阻止提示词提交；PostToolUse 发生在工具执行之后，只能把阻断反馈交给 Claude，不能撤销已经发生的工具操作。无输出表示这个 Hook 没有追加决策。

#### 完整示例1：文件保护Hook

**场景**：演示拦截 Write / Edit 输入路径中含 `production/`、`prod/` 或 `.env` 的调用。下面按字符串匹配，不解析符号链接和 `..`，也不覆盖 Bash、MCP 等其他写入渠道；它不能作为整个目录的安全隔离。严格保护需结合工具权限和操作系统访问控制。

**脚本 `.claude/hooks/pre-protect-production.py`**：

```python
#!/usr/bin/env python3
"""
PreToolUse Hook - 保护production目录
禁止Write/Edit工具修改production目录下的文件
"""
import sys
import json

# 读取stdin的JSON输入
try:
    input_data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', '')

# 只检查Write和Edit工具
if tool_name not in ['Write', 'Edit']:
    sys.exit(0)

# 规范化路径（处理Windows和Unix路径）
file_path_normalized = file_path.replace('\\', '/')

# 检查是否是保护目录
protected_dirs = ['production/', 'prod/', '.env']
for protected in protected_dirs:
    if protected in file_path_normalized:
        # 拒绝执行
        decision = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"❌ 禁止修改受保护的路径！\n路径: {file_path}\n原因: 包含受保护目录 '{protected}'\n\n请先切换到dev环境或手动操作。"
            }
        }
        print(json.dumps(decision, ensure_ascii=False))
        sys.exit(0)

# 不做决策，交给正常权限流程
sys.exit(0)
```

**配置 `.claude/settings.json`**：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-protect-production.py"],
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**运行效果**：

当Claude尝试修改`production/config.json`时：

```
Claude：我来修改production/config.json...

❌ 禁止修改受保护的路径！
路径: C:/project/production/config.json
原因: 包含受保护目录 'production/'

请先切换到dev环境或手动操作。
```

#### 完整示例2：危险命令拦截Hook

**场景**：用正则识别一些明显危险的 Bash 文本（如 `rm -rf /`）。它不能完整解析 shell；改变参数顺序、引号或调用别的程序都可能绕过。下面用于理解 PreToolUse 决策，不代替工具权限、沙箱或系统访问控制。

**脚本 `.claude/hooks/pre-block-dangerous-cmd.py`**：

```python
#!/usr/bin/env python3
"""
PreToolUse Hook - 拦截危险命令
阻止执行可能造成破坏的Shell命令
"""
import sys
import json
import re

# 危险命令模式
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',           # rm -rf /
    r'rm\s+-rf\s+~',           # rm -rf ~
    r'rm\s+-rf\s+\*',          # rm -rf *
    r'rm\s+-rf\s+\.\.',        # rm -rf ..
    r':\(\)\s*{\s*:\|:&\s*};:',  # Fork炸弹
    r'mkfs\.',                  # 格式化磁盘
    r'dd\s+if=.+of=/dev/',     # 覆盖磁盘
    r'>\s*/dev/sda',           # 覆盖磁盘
    r'chmod\s+-R\s+777\s+/',   # 危险权限
]

# 读取输入
try:
    input_data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})
command = tool_input.get('command', '')

# 只检查Bash工具
if tool_name != 'Bash':
    sys.exit(0)

# 检查危险模式
for pattern in DANGEROUS_PATTERNS:
    if re.search(pattern, command, re.IGNORECASE):
        decision = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"🚨 危险命令已拦截！\n\n命令: {command}\n\n匹配的危险模式: {pattern}\n\n如果确实需要执行，请在终端手动运行。"
            }
        }
        print(json.dumps(decision, ensure_ascii=False))
        sys.exit(0)

sys.exit(0)
```

**配置**：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-block-dangerous-cmd.py"],
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### 3.2 PostToolUse（工具调用后）

> **一句话理解**：PostToolUse就像"快递签收通知"，在工具成功执行后自动触发后续操作。

#### 触发时机

在工具**成功执行后**立即触发，可以处理工具的输出结果。

#### 输入参数（通过stdin的JSON）

下面省略会话等公共字段，只展示工具相关部分。`tool_input` 和 `tool_response` 的具体结构随工具变化，不能把 Write 的返回字段当成所有工具的通用字段：

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "C:\\project\\src\\app.js",
    "content": "console.log('Hello');"
  },
  "tool_response": {
    "filePath": "C:\\project\\src\\app.js",
    "type": "create"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `tool_name` | string | 工具名称 |
| `tool_input` | object | 工具的输入参数 |
| `tool_response` | 依工具而定 | 工具的返回结果；字段名不是 `tool_output` |

#### 输出格式

PostToolUse 已在工具执行之后，可以做格式化、备份、测试等后处理，也可以返回 JSON：

- `systemMessage`：向用户显示消息
- `hookSpecificOutput.additionalContext`：向 Claude 补充上下文
- `hookSpecificOutput.updatedToolOutput`：替换随后发给 Claude 的工具结果；内置工具必须保持原结果的结构，不能随意改成纯文本
- 顶层 `decision: "block"` 配合 `reason`：把反馈交给 Claude，不能撤销已经完成的操作

退出 `0` 时的 stderr 只进入 debug 日志，不会直接打印在对话里；退出 `2` 可把 stderr 反馈给 Claude，但工具已执行。下面的格式化示例只做后处理并写 debug 日志。

#### 完整示例1：自动代码格式化

**场景**：在Write工具保存.js/.ts文件后，自动运行Prettier格式化

**脚本 `.claude/hooks/post-auto-format.py`**：

```python
#!/usr/bin/env python3
"""
PostToolUse Hook - 自动代码格式化
保存代码文件后自动运行对应的格式化工具
"""
import sys
import json
import subprocess
from pathlib import Path

# 格式化工具配置
# 本示例在 macOS / Linux / WSL 中运行，并先安装项目需要的格式化工具。
# 文件路径作为独立参数传递，不插入 shell 命令。
FORMATTERS = {
    '.js': ['npx', 'prettier', '--write', '--'],
    '.ts': ['npx', 'prettier', '--write', '--'],
    '.jsx': ['npx', 'prettier', '--write', '--'],
    '.tsx': ['npx', 'prettier', '--write', '--'],
    '.json': ['npx', 'prettier', '--write', '--'],
    '.css': ['npx', 'prettier', '--write', '--'],
    '.py': ['black', '--'],
    '.go': ['gofmt', '-w'],
}

# 排除的目录
EXCLUDED_DIRS = {'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build', '.git'}

def should_format(file_path: str) -> bool:
    """检查是否应该格式化该文件"""
    path = Path(file_path)

    # 检查是否在排除目录中
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return False

    # 检查文件扩展名
    return path.suffix in FORMATTERS

def run_formatter(file_path: str) -> str:
    """运行格式化工具"""
    path = Path(file_path)
    suffix = path.suffix

    if suffix not in FORMATTERS:
        return None

    cmd = [*FORMATTERS[suffix], str(path.resolve())]

    try:
        result = subprocess.run(
            cmd,
            shell=False,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return f"✅ 格式化成功"
        else:
            return f"⚠️ 格式化失败: {result.stderr[:100]}"
    except subprocess.TimeoutExpired:
        return "⚠️ 格式化超时"
    except FileNotFoundError:
        return "⚠️ 格式化工具未安装"
    except Exception as e:
        return f"⚠️ 格式化错误: {str(e)}"

def main():
    # 读取输入
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # 只处理Write工具
    if tool_name != 'Write':
        return

    # 检查是否需要格式化
    if not file_path or not should_format(file_path):
        return

    # 运行格式化
    result = run_formatter(file_path)
    if result:
        print(f"\n[AutoFormat] {Path(file_path).name}: {result}", file=sys.stderr)

if __name__ == '__main__':
    main()
```

**配置**：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-auto-format.py"],
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**验证效果**：Write 完成后检查文件是否按对应格式化工具改变。脚本把 `[AutoFormat]` 结果写到 stderr；退出 `0` 时在 debug 日志中查看，不要求对话界面显示这行。需要用户可见结果时，另用 `systemMessage` 返回消息。

#### 完整示例2：自动备份Hook

**场景**：在Edit工具修改重要文件后，自动创建备份

**脚本 `.claude/hooks/post-auto-backup.py`**：

```python
#!/usr/bin/env python3
"""
PostToolUse Hook - 自动备份
编辑重要文件后自动创建.bak备份
"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# 需要备份的目录
BACKUP_DIRS = ['config', 'src', 'docs', '.claude']

def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # 只处理Edit工具
    if tool_name != 'Edit':
        return

    # 检查是否在需要备份的目录中
    should_backup = any(dir_name in file_path for dir_name in BACKUP_DIRS)

    if should_backup and Path(file_path).exists():
        # 创建备份
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{file_path}.{timestamp}.bak"

        try:
            shutil.copy2(file_path, backup_path)
            print(f"[Backup] ✅ 已创建备份: {Path(backup_path).name}", file=sys.stderr)
        except Exception as e:
            print(f"[Backup] ⚠️ 备份失败: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
```

### 3.3 UserPromptSubmit（用户提示词提交）

> **一句话理解**：UserPromptSubmit就像"邮件发送前的自动补充"，可以在用户输入发送给Claude之前自动增强或过滤。

#### 触发时机

在用户提交提示词后，**Claude处理之前**。

#### 输入参数（通过stdin的JSON）

> ⚠️ **重要**：UserPromptSubmit的输入是**JSON格式**，不是纯文本！

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../session.jsonl",
  "cwd": "/your/project/path",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "请帮我写一篇关于AI的文章"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `session_id` | string | 当前会话ID |
| `prompt` | string | 用户输入的原始提示词 |
| `cwd` | string | Claude Code的工作目录 |
| `permission_mode` | string | 权限模式（default/plan/bypassPermissions等） |
| `hook_event_name` | string | 事件类型标识 |

#### 输出格式

退出 `0` 时，纯文本 stdout 会作为额外上下文交给 Claude；若输出 JSON，则只按支持的字段处理。它不会改写用户原始提示词，也不等于向用户显示一条消息。

**方式1：直接输出文本**（会作为额外上下文添加）
```
## 写作要求
- 字数：1500字
- 风格：老金式接地气风格
- 包含实战案例
```

**方式2：输出JSON格式**（更多控制）
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "写作时请包含具体案例，并核对事实来源。"
  }
}
```

#### 完整示例：写作规范自动追加

**场景**：检测到写作任务时，自动追加写作规范

**脚本 `.claude/hooks/user-prompt-enhance.py`**：

```python
#!/usr/bin/env python3
"""
UserPromptSubmit Hook - 提示词自动增强
检测到特定任务时自动追加相关规范

【重要】：输入是JSON格式，必须先解析！
"""
import sys
import json

# 从stdin读取JSON输入
try:
    input_data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    # JSON解析失败，直接退出
    sys.exit(0)

# 获取用户输入的提示词
user_input = input_data.get('prompt', '').strip()

# 如果没有prompt字段，直接退出
if not user_input:
    sys.exit(0)

# 过滤简单回复（不需要增强）
simple_responses = ['好的', '是的', '继续', 'ok', 'yes', 'no', '确认', '取消']
if user_input.lower() in simple_responses or len(user_input) < 5:
    # 不需要增强，不输出任何内容
    sys.exit(0)

# 过滤斜杠命令
if user_input.startswith('/'):
    sys.exit(0)

# 检查是否是写作任务
writing_keywords = ['写', '文章', '生成', '创作', 'write', 'article', '内容']
is_writing_task = any(kw in user_input.lower() for kw in writing_keywords)

if is_writing_task:
    # 输出额外上下文（会添加到AI上下文中）
    enhancement = """
---
## 写作规范提醒（Hook自动注入）
1. **风格**：接地气、说人话，避免AI腔
2. **结构**：开头金句 -> 核心要点 -> 实战案例 -> 总结升华
3. **字数**：1500-2000字
4. **检查**：完成后按上述规范逐项检查；如有项目自定义检查命令，先确认它存在再调用
---"""
    print(enhancement)
    print(f"[Hook] 已为写作任务注入规范", file=sys.stderr)

sys.exit(0)
```

> 💡 **注意**：
> - 输入是JSON，必须用`json.loads()`解析
> - 用户原始输入在`prompt`字段中
> - 本例用纯文本 stdout 添加上下文；也可改用 `hookSpecificOutput.additionalContext` 的 JSON 格式
> - 本例退出 `0`，stderr 进入 debug 日志，不直接显示在对话中

**配置**：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/user-prompt-enhance.py"],
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**运行效果**：

用户输入：
```
帮我写一篇关于Claude Code的介绍文章
```

Claude实际收到：
```
帮我写一篇关于Claude Code的介绍文章

---
## 写作规范提醒（自动追加）
1. **风格**：接地气、说人话，避免AI腔
2. **结构**：开头金句 -> 核心要点 -> 实战案例 -> 总结升华
3. **字数**：1500-2000字
4. **检查**：完成后按上述规范逐项检查；如有项目自定义检查命令，先确认它存在再调用
---
```

### 3.4 Notification（通知）

> **一句话理解**：Notification Hook就像"消息推送处理器"，在Claude发送通知时触发。

#### 触发时机

常见类型包括权限等待、输入空闲、认证完成、MCP 表单 / URL 请求、后台代理状态和额度恢复。权限等待等通知有空闲计时条件；如果要在权限请求出现时立即处理，使用 `PermissionRequest`。通知类型与具体触发条件见[官方 Notification 参考](https://code.claude.com/docs/en/hooks#notification)。

#### 输入参数（通过stdin的JSON）

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../session.jsonl",
  "cwd": "/your/project/path",
  "hook_event_name": "Notification",
  "message": "Claude is waiting for your input",
  "title": "Input needed",
  "notification_type": "idle_prompt"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `session_id` | string | 当前会话ID |
| `transcript_path` | string | 会话记录文件路径 |
| `cwd` | string | 工作目录 |
| `hook_event_name` | string | 事件类型标识（固定为"Notification"） |
| `message` | string | 通知正文 |
| `title` | string | 可选通知标题；缺省时由转发脚本给默认值 |
| `notification_type` | string | 通知类型，也是 Notification matcher 匹配的值 |

> **字段说明**：Notification 输入有 `message` 和 `notification_type`，还可以包含 `title`。转发时保留已有标题；没有标题时再使用默认值。Notification Hook 用于通知等副作用，不能靠它修改或阻断原通知。

#### 完整示例：桌面通知Hook

**场景**：将Claude的通知转发到系统桌面通知

**脚本 `.claude/hooks/notification-desktop.py`**：

```python
#!/usr/bin/env python3
"""
Notification Hook - 桌面通知
将Claude的通知转发到系统桌面通知
"""
import sys
import json
import subprocess
import platform

def send_notification(title: str, message: str):
    """把通知作为数据传入，避免拼进 AppleScript 或 PowerShell 代码。"""
    system = platform.system()
    try:
        if system == 'Darwin':
            script = 'on run argv\ndisplay notification (item 2 of argv) with title (item 1 of argv)\nend run'
            subprocess.run(['osascript', '-e', script, title, message], check=True)
        elif system == 'Linux':
            subprocess.run(['notify-send', title, message], check=True)
        elif system == 'Windows':
            # 需先安装 BurntToast；JSON 使用 base64 传入，通知正文不参与脚本解析。
            import base64
            payload = base64.b64encode(
                json.dumps({'title': title, 'message': message}, ensure_ascii=False).encode('utf-8')
            ).decode('ascii')
            script = (
                "$ErrorActionPreference = 'Stop'; "
                "$data = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('"
                + payload + "')) | ConvertFrom-Json; "
                "Import-Module BurntToast -ErrorAction Stop; "
                "New-BurntToastNotification -Text $data.title, $data.message"
            )
            subprocess.run(['powershell', '-NoProfile', '-Command', script], check=True)
    except Exception as e:
        print(f'通知发送失败: {e}', file=sys.stderr)

def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    # Notification 输入包含 message、可选 title 和 notification_type
    message = input_data.get('message', '')
    session_id = input_data.get('session_id', '')

    if not message:
        return

    # 保留事件标题；缺失或为空时使用默认值。
    title = input_data.get("title") or "Claude Code"

    # 发送桌面通知
    send_notification(title, message)
    print(f"[Notification] 已发送桌面通知: {message[:50]}...", file=sys.stderr)

if __name__ == '__main__':
    main()
```

### 3.5 SessionStart（会话开始）

> **一句话理解**：SessionStart就像"开机自启动程序"，在Claude Code启动时自动执行初始化任务。

#### 触发时机

新建会话、恢复会话、`/clear`、压缩后及 fork 新会话时触发，输入 `source` 分别说明来源；需要只在新建时执行，可以设 `matcher: "startup"`。

#### 用途

- 初始化环境
- 检查依赖
- 加载配置

#### 完整示例：环境检查Hook

**脚本 `.claude/hooks/session-start-check.py`**：

```python
#!/usr/bin/env python3
"""
SessionStart Hook - 环境检查
启动时检查必需的工具和依赖是否已安装
"""
import sys
import shutil

# 检查必需的工具
required_tools = {
    'node': 'Node.js（从 Node.js 官方安装说明安装）',
    'python': 'Python 3.x',
    'git': 'Git版本控制',
}

# 可选但推荐的工具
optional_tools = {
    'prettier': 'Prettier代码格式化 (npm install -g prettier)',
    'black': 'Black Python格式化 (pip install black)',
}

missing_required = []
missing_optional = []

# 检查必需工具
for tool, desc in required_tools.items():
    if not shutil.which(tool):
        missing_required.append(f"  X {tool}: {desc}")

# 检查可选工具
for tool, desc in optional_tools.items():
    if not shutil.which(tool):
        missing_optional.append(f"  ! {tool}: {desc}")

# 输出检查结果
if missing_required or missing_optional:
    print("\n" + "="*50, file=sys.stderr)
    print("环境检查结果", file=sys.stderr)
    print("="*50, file=sys.stderr)

    if missing_required:
        print("\nX 缺少必需工具（请安装）：", file=sys.stderr)
        for item in missing_required:
            print(item, file=sys.stderr)

    if missing_optional:
        print("\n! 缺少可选工具（建议安装）：", file=sys.stderr)
        for item in missing_optional:
            print(item, file=sys.stderr)

    print("\n" + "="*50 + "\n", file=sys.stderr)
else:
    print("V 环境检查通过，所有工具已就绪", file=sys.stderr)

# 向用户显示汇总；上面的详细 stderr 留在 debug 日志中
import json
summary = "环境检查通过" if not missing_required else "缺少必需工具：" + "; ".join(missing_required)
if missing_optional:
    summary += "；可选工具：" + "; ".join(missing_optional)
print(json.dumps({"systemMessage": summary}, ensure_ascii=False))
sys.exit(0)
```

**配置**：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start-check.py"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### 3.6 SessionEnd 和 Stop

#### SessionEnd（会话结束）

**触发时机**：Claude Code正常退出时

**用途**：
- 清理临时文件
- 保存会话状态
- 备份日志

**示例脚本 `.claude/hooks/session-end-cleanup.sh`**：

```bash
#!/bin/bash
# SessionEnd Hook - 清理临时文件

temp_dir="$HOME/.claude/temp"
if [ -d "$temp_dir" ]; then
    rm -rf "$temp_dir"/*
    echo "V 临时文件已清理" >&2
fi

exit 0
```

#### Stop（AI停止响应）

**触发时机**：当Claude Code代理完成响应时

**输入参数（通过stdin的JSON）**：

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../session.jsonl",
  "cwd": "/your/project/path",
  "hook_event_name": "Stop"
}
```

> ⚠️ **注意**：上面只是省略事件字段的最小输入示意。Stop 还包含 `stop_hook_active`、`last_assistant_message` 及任务、定时任务状态；`reason` 是要求继续时的输出反馈字段，不是这个输入里的停止原因。返回 `decision: "block"` 时先检查 `stop_hook_active`，避免反复要求继续。

**用途**：
- 保存当前状态
- 记录会话信息
- 可以通过输出`{"continue": false}`强制停止

**示例脚本 `.claude/hooks/stop-save-state.py`**：

```python
#!/usr/bin/env python3
"""
Stop Hook - 保存状态
AI停止时保存当前会话状态
"""
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    input_data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    input_data = {}

# 获取标准字段（注意：没有reason字段）
session_id = input_data.get('session_id', 'unknown')
cwd = input_data.get('cwd', str(Path.cwd()))

# 保存状态
state_dir = Path.home() / '.claude' / 'state'
state_dir.mkdir(parents=True, exist_ok=True)
state_file = state_dir / 'last-session-state.json'

state = {
    "stopped_at": datetime.now().isoformat(),
    "session_id": session_id,
    "project_dir": cwd
}

with open(state_file, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"V 会话状态已保存到: {state_file}", file=sys.stderr)
sys.exit(0)
```

---

### 3.7 WorktreeCreate 和 WorktreeRemove（工作树管理）🆕

> **v2.1.49+ 新增**：这两个Hook类型配合 Claude Code 内置的 Git Worktree 功能使用，用于 Git Worktree（工作树）的生命周期管理。

#### 什么是 Git Worktree？

> 💡 **生活类比**：Git Worktree 就像在同一个项目里开了多个"平行工作台"。你可以在工作台A修bug，同时在工作台B开发新功能，互不干扰。Claude Code 使用 Worktree 来实现并行任务隔离。

#### WorktreeCreate（工作树创建时触发）

**触发时机**：通过 `claude --worktree`、配置了 `isolation: "worktree"` 的子代理或需要隔离的后台会话创建工作副本时。

配置这个 Hook 后，Claude Code 会把默认的 Git 创建过程交给它。Hook 必须实际创建工作目录并返回路径；仅写一条“已创建”的日志会使创建失败。适合自定义 Git 流程，或接入 SVN、Perforce、Mercurial 等版本控制系统。

**输入数据**（通过 stdin 接收 JSON）：

```json
{
  "session_id": "example-session",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

`name` 是用户指定或自动生成的工作树短名称。此时目录还没有由默认流程创建，输入里没有供你直接使用的 `worktree_path` 或 `branch`。

**完整示例：由 Hook 创建 Git 工作树**

适用于已有提交的 Git 仓库，需要 Git 和 Python 3。把下面代码保存为项目中的 `.claude/hooks/create-worktree.py`。示例只接受字母或数字开头的短名称，创建 `hook-worktree/<name>` 新分支；目录或分支已存在时直接报错，不覆盖既有成果。

```python
import json
import re
import subprocess
import sys
from pathlib import Path

request = json.load(sys.stdin)
name = request["name"]
if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
    raise ValueError("worktree name must be a simple slug")

root = Path(subprocess.run(
    ["git", "-C", request["cwd"], "rev-parse", "--show-toplevel"],
    check=True, capture_output=True, text=True,
).stdout.strip()).resolve()
base = root / ".claude" / "worktrees"
for parent in (root / ".claude", base):
    if parent.is_symlink():
        raise ValueError("worktree parent must not be a symlink")
base.mkdir(parents=True, exist_ok=True)
target = base / name
if target.exists() or target.is_symlink():
    raise FileExistsError(target)

branch = "hook-worktree/" + name
subprocess.run(
    ["git", "check-ref-format", "--branch", branch],
    check=True, stdout=sys.stderr,
)
subprocess.run(
    ["git", "-C", str(root), "worktree", "add", "-b", branch, str(target), "HEAD"],
    check=True, stdout=sys.stderr,
)
print(str(target.resolve()))
```

将下列事件合并到现有 `.claude/settings.json` 的 `hooks` 中。这里使用 exec form，脚本路径作为独立参数，能处理项目路径中的空格；若本机 Python 命令叫 `python3`，相应修改 `command`。

```json
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/create-worktree.py"],
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**输出契约**：command Hook 把创建目录的路径放在 stdout 最后一条非空行，其他日志写 stderr。非零退出、没有返回路径，或返回的目录无法进入，都会使创建失败。优先返回规范化的绝对路径；不要含 `.`、`..`，也不要经过仓库内部的符号链接。HTTP Hook 则通过 `hookSpecificOutput.worktreePath` 返回路径，并设置 `hookEventName: "WorktreeCreate"`。

自定义创建接管了整个默认流程，`.worktreeinclude` 不会自动处理；需要复制哪些本地配置或执行哪些初始化步骤，要由创建脚本明确实现。这里只演示创建工作树，没有安装依赖或复制本地配置。

#### WorktreeRemove（工作树删除时触发）

**触发时机**：工作树即将被移除时，例如退出工作树会话并选择删除，或隔离子代理结束。输入使用 `worktree_path`，这与创建事件的 `name` 不同：

```json
{
  "session_id": "example-session",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/path/to/project/.claude/worktrees/feature-auth"
}
```

Git 工作树由 Claude Code 使用 `git worktree remove` 清理。下面是可选的调试 Hook，只把收到的删除路径写到 stderr，不承担删除动作：

```json
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import json, sys; data = json.load(sys.stdin); print('WorktreeRemove requested: ' + data['worktree_path'], file=sys.stderr)"
            ],
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

如果用 WorktreeCreate 创建了非 Git 工作副本，还必须自己实现配套的清理逻辑：从 stdin 读取 `worktree_path`，先核对规范化路径和允许清理的根目录，再清理该工作副本；只记录日志不会完成清理。没有配套清理 Hook 时，目录会留在磁盘上。

**失败契约**：WorktreeRemove 非零退出且目标目录仍存在时，移除失败；后台会话删除也会保留对应会话。它的 JSON 决策字段会被忽略，不能靠 `continue: false` 代替退出码；已被脚本删除的内容也不会因此恢复。完整规则见 [官方 WorktreeCreate](https://code.claude.com/docs/en/hooks#worktreecreate) 与 [WorktreeRemove](https://code.claude.com/docs/en/hooks#worktreeremove)。

#### 与 `--worktree` 启动参数的关系

> 🔥 **重要**：2026年2月（v2.1.49），Claude Code 正式内置了 Git Worktree 支持，这是一个**核心功能级别**的更新，不仅仅是 Hook。

**`--worktree`（`-w`）启动参数**：

```bash
# 在独立工作树中启动 Claude Code
claude --worktree
# 或简写
claude -w
```

**工作原理**：

```
你的项目仓库（主工作目录）
├── .git/                    # 共享的 Git 历史
├── .claude/worktrees/       # 工作树存放目录（加到 .gitignore）
│   ├── worktree-abc123/     # Agent A 的独立工作目录
│   └── worktree-def456/     # Agent B 的独立工作目录
├── src/                     # 主工作目录的文件
└── ...
```

**使用场景**：

| 场景 | 说明 |
|------|------|
| 并行开发 | 终端1: `claude -w` 开发新功能 / 终端2: `claude -w` 修复 bug |
| 代码审查 | 主工作目录继续开发,工作树中运行审查 Agent |
| 实验性修改 | 在工作树中试验方案,不影响主目录 |

**配置步骤**：

```bash
# 1. 将工作树目录加到 .gitignore
echo ".claude/worktrees/" >> .gitignore

# 2. 启动第一个 Agent（在工作树中）
claude -w

# 3. 打开另一个终端，启动第二个 Agent（在另一个工作树中）
claude -w
```

**Hook 的角色**：
- **Git 用户**：直接使用 `claude -w` 即可；只有需要接管默认创建流程时才配置 WorktreeCreate。配置后要负责实际创建，不能只添加安装依赖或日志命令。
- **非 Git 用户**（SVN/Perforce/Mercurial）：通过 WorktreeCreate/WorktreeRemove Hook 自定义工作树的创建和清理逻辑，替代默认的 Git 行为

---

### 3.8 SubagentStart 和 SubagentStop（子代理生命周期）🆕

> **v2.1.49+ 新增**：这两个Hook类型用于监控和管理子代理（Subagent/Agent）的生命周期。

#### SubagentStart（子代理启动时触发）

**触发时机**：Claude Code 启动子代理（通过 Agent 工具；旧资料可能写作 Task）时自动触发

**典型用途**：
- 记录子代理启动日志
- 初始化子代理专属的环境配置
- 监控并发子代理数量

**配置示例**：

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"子代理已启动: $(date)\" >> ~/.claude/subagent.log",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

#### SubagentStop（子代理停止时触发）

**触发时机**：子代理准备结束响应时触发。可以返回 `decision: "block"` 和 `reason` 要求它继续处理未完成事项；不要把它当成所有强制终止都会经过的清理保证。

**典型用途**：
- 收集子代理执行结果
- 清理子代理使用的临时资源
- 记录子代理执行耗时

---

### 3.9 PermissionRequest（权限请求）🆕

> **v2.1.49+ 新增**：在权限请求时触发，可用于实现自动审批策略。

**触发时机**：Claude Code 请求执行需要用户授权的操作时

**典型用途**：
- 根据规则自动批准/拒绝权限请求
- 记录权限请求审计日志
- 实现基于项目的权限策略

**配置示例**：

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "timeout": 5,
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/permission-policy.py"
            ]
          }
        ]
      }
    ]
  }
}
```

这里的 `permission-policy.py` 是扩展入口，需先创建脚本并实现具体策略：从 stdin 读取权限请求，在退出 `0` 时通过 `hookSpecificOutput` 返回 `hookEventName: "PermissionRequest"` 和 `decision.behavior`（`allow` / `deny`）。不要把一个尚不存在的脚本路径当成完整的自动审批方案；精确结构见 [官方 PermissionRequest 参考](https://code.claude.com/docs/en/hooks#permissionrequest)。

---

### 3.10 PreCompact（上下文压缩前）🆕

> **v2.1.49+ 新增**：在 Claude Code 执行上下文压缩（Compact）前触发。

**触发时机**：当对话上下文即将被压缩时；matcher 可用 `manual` 或 `auto`。

**典型用途**：
- 在压缩前保存关键上下文信息
- 记录压缩事件日志
- 在必要校验未完成时阻止压缩

**控制方式**：退出码 `2`，或退出 `0` 并返回 `{"decision":"block"}`，都能阻止压缩。手动 `/compact` 的 stderr 会显示给用户。阻止提前触发的自动压缩时，会话继续保持未压缩状态；如果压缩是为恢复 API 已返回的上下文超限错误而触发，阻止它会让原错误继续暴露、本次请求失败。`continue` 和 `systemMessage` 在这个事件中会被忽略。

---

### 3.11 ConfigChange（配置变更）🆕

> **v2.1.49+ 新增**：在 Claude Code 配置发生变更时触发。

**触发时机**：会话中的设置文件、部分受管策略文件或 Skill 文件变化时，输入中的 `source` 标明来源，`file_path` 可能提供具体路径。

**典型用途**：
- 配置变更审计和日志记录
- 校验新的项目或用户设置
- 阻止不符合策略的新设置应用到当前会话

**控制方式**：退出码 `2` 或 `{"decision":"block"}` 可阻止当前会话应用新配置，不会回滚磁盘上已经写入的文件。`policy_settings` 是例外：本机受管设置文件变化会触发审计，但阻断结果被忽略；服务端受管设置下发或刷新不触发此事件。

---

### 3.12 TeammateIdle（队友空闲）🆕

> **v2.1.49+ 新增**：在多代理协作场景中，队友即将进入空闲状态时触发。

**触发时机**：队友完成当前回合、准备空闲时；不支持 matcher。

**典型用途**：
- 检查交付文件或验证结果是否齐全
- 发送状态通知
- 把未完成事项反馈给队友继续处理

**控制方式**：退出码 `2` 会把 stderr 反馈给队友，让它继续工作而非进入空闲。另一种控制是返回 `{"continue":false,"stopReason":"..."}`，这会停止该队友；两者作用相反，不能混用。

---

### 3.13 新增Hook事件类型 🆕

> **v2.1+ 新增**：以下Hook类型进一步扩展了Claude Code的事件覆盖范围，让你能捕捉到更多关键时刻。
>
> 🎯 **生活类比**：如果之前的Hook是"门窗报警器"，这些新Hook就是"烟雾报警器、水浸传感器、燃气检测器"——覆盖了之前监控不到的异常场景。

#### StopFailure（API异常停止时触发）

**触发时机**：当API错误（429限流、401认证失败、500服务器错误等）导致会话异常停止时触发

> **与 Stop 的区别**：`Stop` 在 Claude 准备结束响应时触发，可要求继续；`StopFailure` 在 API 错误导致回合结束时替代 Stop。用户退出会话属于 SessionEnd，不能与 Stop 混为一谈。

**典型用途**：
- 发送告警通知（Slack/邮件/钉钉）
- 记录错误日志用于后续分析
- 记录恢复线索，供后续重试或降级时使用

**配置示例**：

```json
{
  "hooks": {
    "StopFailure": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "timeout": 10,
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/alert-on-failure.py"
            ]
          }
        ]
      }
    ]
  }
}
```

> **输入与控制**：`error` 是错误类型（如 `rate_limit`），具体说明在可选的 `error_details` 中，`last_assistant_message` 此时可能是展示给用户的 API 错误文本。除 `terminalSequence` 外，输出和退出码均不参与决策，不能靠返回 block 或 continue 重启失败的回合。示例中的 `alert-on-failure.py` 需要你先实现；可只记录错误类型和必要的排障信息。

---

#### PostCompact（上下文压缩后触发）

**触发时机**：执行 `/compact` 命令或上下文自动压缩完成后触发

> 🎯 **生活类比**：就像搬家后清点物品——压缩完成后，你想知道"丢掉了多少东西、还剩多少空间"。

**典型用途**：
- 记录 `trigger`（manual / auto）和 `compact_summary`
- 按压缩摘要更新外部记录
- 记录压缩完成的时间；前后 token 数需另外采集，事件不直接提供这两个计数

**配置示例**：

```json
{
  "hooks": {
    "PostCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date)] 上下文已压缩\" >> ~/.claude/compact.log",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

> ⚠️ **注意**：PostCompact 是**不可阻止**的Hook，压缩已经完成，你只能执行后续操作。与 `PreCompact`（压缩前）配合使用效果更佳。

---

#### InstructionsLoaded（指令文件加载时触发）

**触发时机**：CLAUDE.md 等指令文件加载到上下文时触发

> 🎯 **生活类比**：就像新员工入职时检查培训手册是否齐全——确保AI读到了正确且完整的指令。

**典型用途**：
- 验证指令文件的完整性和正确性
- 记录哪些指令文件被加载（便于调试）
- 触发项目特定的初始化操作

**配置示例**：

```json
{
  "hooks": {
    "InstructionsLoaded": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "timeout": 5,
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/verify-instructions.py"
            ]
          }
        ]
      }
    ]
  }
}
```

> **输入与控制**：每次事件提供一个已加载文件的 `file_path`，以及 `memory_type`、`load_reason` 等字段，不是路径列表。它会随启动加载和后续惰性加载多次触发，异步运行且不能阻止或修改指令加载。示例中的 `verify-instructions.py` 是需要自行实现的审计脚本，不能靠它返回 deny 来阻止文件生效。

---

#### Elicitation 和 ElicitationResult（MCP交互输入）🆕

> **v2.1+ 新增**：这两个Hook配合MCP Elicitation功能使用，让你能监控和管理MCP服务器与用户之间的交互输入。
>
> 🎯 **生活类比**：`Elicitation` 就像客服系统弹出问卷调查——MCP服务器需要向用户询问信息；`ElicitationResult` 就像用户填完问卷提交——你可以记录和验证填写的内容。

**Elicitation — MCP请求输入时触发**

**触发时机**：MCP服务器通过Elicitation API向用户发起交互输入请求时

**典型用途**：
- 记录MCP交互请求日志
- 自动填充常用值（如默认配置）

**ElicitationResult — 用户完成输入后触发**

**触发时机**：用户响应 MCP 交互请求后、结果返回 MCP server 之前；Hook 可以检查、改写或拒绝这份响应。

**典型用途**：
- 验证用户输入数据的合法性
- 记录交互结果用于审计
- 触发后续自动化流程

**配置示例**：

```json
{
  "hooks": {
    "Elicitation": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"MCP请求输入: $(date)\" >> ~/.claude/elicitation.log",
            "timeout": 5
          }
        ]
      }
    ],
    "ElicitationResult": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "timeout": 5,
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/validate-elicitation.py"
            ]
          }
        ]
      }
    ]
  }
}
```

`Elicitation` 的退出码 `2` 拒绝输入请求；`ElicitationResult` 的退出码 `2` 拒绝响应，把 action 改为 `decline`。这两个事件的 stderr 不会显示给用户或 Claude。需要明确返回结果时，使用 `hookSpecificOutput`，填写对应的 `hookEventName` 和 `action`（`accept` / `decline` / `cancel`），`content` 只在接受时承载表单数据。

上例中的 `validate-elicitation.py` 需要自行实现：读取 stdin 的 `mcp_server_name`、`action` 和可选的 `content`，再按上述契约返回。配置示例本身不包含校验策略。其他字段见 [官方 Elicitation 参考](https://code.claude.com/docs/en/hooks#elicitation)。

---

### 3.14 HTTP Hooks（远程Webhook集成）🆕

> **v2.1+ 新增**：除了传统的Shell命令Hook，现在可以直接将Hook事件POST到远程URL，无需编写本地脚本。
>
> 🎯 **生活类比**：之前的Hook像是"自家装的门铃"——得自己接线、自己写响铃逻辑；HTTP Hook像是"接入物业监控中心"——事件发生时自动通知远程服务，你只管接收处理。

**配置格式**：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "https://your-webhook.example.com/hook",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**工作原理**：
- 当Hook事件触发时，Claude Code 自动向配置的URL发送 **POST** 请求
- 请求体为JSON格式，自动包含该Hook的标准输入数据（与Shell Hook的stdin内容相同）
- 支持设置超时时间，防止远程服务无响应时阻塞工作流

**Shell Hook vs HTTP Hook 对比**：

| 特性 | Shell Hook | HTTP Hook 🆕 |
|------|-----------|-------------|
| 执行方式 | 运行本地脚本/命令 | POST JSON到远程URL |
| 需要本地脚本 | ✅ 是 | ❌ 否 |
| 跨平台一致性 | ❌ 需处理OS差异 | ✅ 任何平台行为一致 |
| 适合场景 | 本地文件操作、代码检查 | 远程通知、日志收集、CI/CD |
| 网络依赖 | ❌ 无 | ✅ 需要网络连接 |
| 配置复杂度 | 中（需写脚本） | 低（只需URL） |

**适用场景**：
- **Slack/Discord通知**：代码提交、构建完成时自动发送消息
- **CI/CD触发**：Hook事件触发远程构建管道
- **日志收集服务**：将所有Hook事件发送到Datadog/ELK等平台
- **团队协作**：多人开发时自动同步状态到共享服务

> ⚠️ **安全提示**：HTTP Hook会将Hook数据发送到外部服务，确保目标URL可信且使用HTTPS。避免在Hook数据中包含敏感信息（API密钥、密码等）。

---

### 3.15 直接调用 MCP 工具的 Hook

当前 Hook 有五种处理器：`command`、`http`、`mcp_tool`、`prompt`、`agent`。`mcp_tool` 从 v2.1.118 起可用，可以让事件直接调用已配置 MCP 服务器上的工具；它与让 Claude 自行选择调用工具不同。

下面是配置示意：先配置名为 `my_server`、确实提供 `security_scan` 的服务器，并在 `/mcp` 中确认连接与认证。将事件合并进现有设置；示例没有提供扫描服务器，不能只粘贴 JSON 就完成扫描。

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "mcp_tool",
        "server": "my_server",
        "tool": "security_scan",
        "input": {"file_path": "${tool_input.file_path}"},
        "timeout": 30
      }]
    }]
  }
}
```

`server` 和 `tool` 必填，`input` 是工具参数，字符串里的 `${路径}` 从事件 JSON 取值。插件附带的服务器要写作用域名称，例如 `plugin:my-plugin:db`。工具的文本结果按 command Hook 的 stdout 规则解析；`isError: true` 只产生非阻断错误，不能当作可靠的拒绝开关。

在 `PreToolUse`、`Stop` 这类能影响流程的事件上，连接中的服务器会在 MCP 连接超时和 Hook 自身超时范围内被等待；通知等观察事件不等待。Hook 不会替你开启 OAuth 登录。启动时的 `SessionStart`（包括 resume / continue）和所有 `Setup` 发生在 MCP 客户端可用之前，会跳过 `mcp_tool`；会话内 `/clear` 或压缩后的 `SessionStart` 才能调用它。启动必须执行的工作使用 command Hook。完整契约见[官方 MCP tool Hook 参考](https://code.claude.com/docs/en/hooks#mcp-tool-hook-fields)。

---

## 第四部分：实战应用场景

> **本节目的**：学习真实项目中的Hook应用
>
> ⏱️ **预计时间**：1-1.5小时

### 4.1 Git自动化工作流

#### 场景1：提交前自动检查

**需求**：在`git commit`前自动运行代码检查，包括：
- 代码风格检查（lint）
- 敏感信息检查（API Key等）
- 分支保护（禁止直接提交main）

**完整脚本 `.claude/hooks/git-pre-commit-checker.py`**：

下面的 Python 脚本按 macOS / Linux / WSL 环境讲解，并先安装所需的 ruff、eslint。它只匹配 Bash 输入里字面包含 `git commit` 的命令；`git -C ... commit`、`git -c ... commit` 或其他工具执行提交都可能绕过它。因此它是事件检查示例，不能当完整提交策略。需要统一执行的规则，应结合真正的 Git hook、CI 和受保护分支；也要检查对应工具和配置是否可被绕过。

```python
#!/usr/bin/env python3
"""
Git提交前检查系统
在执行git commit前自动运行多项检查
"""
import sys
import json
import subprocess
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
CONFIG = {
    'protected_branches': ['main', 'master', 'production'],
    'secret_patterns': [
        r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]{20,}',
        r'(?i)(secret|password|passwd|pwd)\s*[=:]\s*["\']?[\w-]{8,}',
        r'(?i)(access[_-]?token|auth[_-]?token)\s*[=:]\s*["\']?[\w-]{20,}',
        r'sk-[a-zA-Z0-9]{20,}',  # OpenAI API Key
        r'ghp_[a-zA-Z0-9]{36,}',  # GitHub Token
    ],
}

def run_command(cmd, timeout=60):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'Command timed out'
    except Exception as e:
        return -1, '', str(e)

def check_branch():
    """检查分支规则"""
    code, stdout, _ = run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    if code != 0:
        return False, "无法获取当前分支，检查未完成"

    branch = stdout.strip()
    if branch in CONFIG['protected_branches']:
        return False, f"X 禁止直接提交到受保护分支: {branch}\n请使用Pull Request"

    return True, f"当前分支: {branch}"

def check_secrets():
    """检查敏感信息"""
    code, stdout, _ = run_command(['git', 'diff', '--cached'])
    if code != 0:
        return False, "无法获取diff，检查未完成"

    findings = []
    for pattern in CONFIG['secret_patterns']:
        if re.search(pattern, stdout):
            findings.append(f"发现可疑模式: {pattern[:40]}...")

    if findings:
        return False, "X 发现可能的敏感信息:\n" + '\n'.join(findings)
    return True, "敏感信息检查通过"

def check_lint():
    """代码风格检查"""
    code, stdout, _ = run_command(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z'])
    if code != 0:
        return False, "无法获取变更文件列表，检查未完成"

    files = [f for f in stdout.split('\0') if f]
    py_files = [f for f in files if f.endswith('.py')]
    js_files = [f for f in files if f.endswith(('.js', '.ts', '.jsx', '.tsx'))]

    errors = []

    # Python文件检查
    if py_files:
        code, stdout, stderr = run_command(['ruff', 'check', '--', *py_files])
        if code != 0:
            errors.append(f"Python代码问题:\n{stdout or stderr}")

    # JavaScript/TypeScript文件检查
    if js_files:
        code, stdout, stderr = run_command(['npx', 'eslint', '--quiet', '--', *js_files])
        if code != 0:
            errors.append(f"JS/TS代码问题:\n{stdout or stderr}")

    if errors:
        return False, '\n'.join(errors)
    return True, "代码风格检查通过"

def main():
    # 读取输入
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get('tool_name', '')
    command = input_data.get('tool_input', {}).get('command', '')

    # 只处理git commit命令
    if tool_name != 'Bash' or 'git commit' not in command:
        return

    # 运行检查
    checks = [
        ('分支检查', check_branch),
        ('敏感信息', check_secrets),
        ('代码风格', check_lint),
    ]

    results = []
    all_passed = True

    # 并行执行检查
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_check = {executor.submit(check[1]): check[0] for check in checks}
        for future in as_completed(future_to_check):
            check_name = future_to_check[future]
            try:
                passed, message = future.result()
                results.append((check_name, passed, message))
                if not passed:
                    all_passed = False
            except Exception as e:
                results.append((check_name, False, f"检查异常: {str(e)}"))
                all_passed = False

    # 输出报告
    print("\n" + "="*60, file=sys.stderr)
    print("Git提交前检查报告", file=sys.stderr)
    print("="*60, file=sys.stderr)

    for name, passed, message in results:
        status = "V PASS" if passed else "X FAIL"
        print(f"\n{status} {name}", file=sys.stderr)
        print(f"   {message}", file=sys.stderr)

    print("\n" + "="*60, file=sys.stderr)

    # 输出决策
    if not all_passed:
        decision = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": "检查未通过，请确认是否继续提交。"
            }
        }
        print(json.dumps(decision, ensure_ascii=False))
    else:
        print("所有检查通过，允许提交", file=sys.stderr)

if __name__ == '__main__':
    main()
```

**配置**：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/git-pre-commit-checker.py"],
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### 4.2 代码质量保障

#### 场景：Markdown文章质量检查

**需求**：保存Markdown文章后自动检查：
- 字数统计
- 标题检查
- 段落数量

**脚本 `.claude/hooks/post-article-quality.py`**：

```python
#!/usr/bin/env python3
"""
PostToolUse Hook - 文章质量检查
保存Markdown文件后自动进行质量检查
"""
import sys
import json
from pathlib import Path

def check_article_quality(file_path):
    """检查文章质量"""
    try:
        content = Path(file_path).read_text(encoding='utf-8')
    except Exception as e:
        return f"无法读取文件: {e}"

    # 统计指标
    char_count = len(content)
    word_count = len(content.split())
    has_title = content.strip().startswith('# ')
    paragraphs = [p for p in content.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs)

    # 生成报告
    report = []
    report.append("\n" + "="*50)
    report.append("文章质量检查报告")
    report.append("="*50)
    report.append(f"\n字符数: {char_count} {'V' if char_count > 500 else '! 偏短'}")
    report.append(f"词数: {word_count}")
    report.append(f"标题: {'V 有' if has_title else 'X 缺少一级标题'}")
    report.append(f"段落数: {paragraph_count} {'V' if paragraph_count > 3 else '! 偏少'}")

    # 建议
    suggestions = []
    if char_count < 500:
        suggestions.append("- 建议增加内容，至少500字")
    if not has_title:
        suggestions.append("- 建议添加一级标题（# 标题）")
    if paragraph_count < 3:
        suggestions.append("- 建议增加段落，改善可读性")

    if suggestions:
        report.append("\n改进建议:")
        report.extend(suggestions)
    else:
        report.append("\nV 文章质量良好！")

    report.append("="*50 + "\n")

    return '\n'.join(report)

def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # 只处理Write工具和.md文件
    if tool_name != 'Write' or not file_path.endswith('.md'):
        return

    # 检查质量
    report = check_article_quality(file_path)
    print(report, file=sys.stderr)

if __name__ == '__main__':
    main()
```

### 4.3 完整配置示例

**综合配置 `.claude/settings.json`**：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/user-prompt-enhance.py"],
            "timeout": 5
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-protect-production.py"],
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-block-dangerous-cmd.py"],
            "timeout": 5
          },
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/git-pre-commit-checker.py"],
            "timeout": 120
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-auto-format.py"],
            "timeout": 30
          },
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-article-quality.py"],
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-auto-backup.py"],
            "timeout": 10
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start-check.py"],
            "timeout": 10
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/notification-desktop.py"],
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

---

## 第五部分：故障排查

> **本节目的**：快速解决Hook配置和执行问题
>
> ⏱️ **预计时间**：按需查阅

### 5.1 Hook不执行

**症状**：配置了Hook但完全没有触发

**排查步骤**：

1. **检查配置文件路径**
```bash
# 确认settings.json在正确位置
ls -la .claude/settings.json
# 应该存在且有内容
```

2. **检查JSON格式**
```bash
# 验证JSON格式
python -c "import json; json.load(open('.claude/settings.json'))"
# 没有报错说明格式正确
```

3. **检查Matcher是否匹配**
```text
错误的字段片段："matcher": "write"  （工具名应使用大写 W）
正确的字段片段："matcher": "Write"
```

4. **检查脚本路径**
```bash
# 确认脚本存在
ls -la .claude/hooks/your-hook.py

# macOS/Linux检查执行权限
chmod +x .claude/hooks/your-hook.py
```

5. **重启Claude Code**
```bash
# 退出当前会话
exit

# 重新启动
claude
```

### 5.2 Hook执行报错

**症状**：Hook触发了但报错退出

**排查步骤**：

1. **手动测试脚本**
```bash
# 模拟输入测试
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.txt"}}' | python .claude/hooks/your-hook.py

# 查看输出和错误
```

2. **检查Python版本**
```bash
python --version
# 应该是Python 3.x
```

3. **检查依赖是否安装**
```bash
# 如果脚本import了第三方库
pip install 缺少的库
```

4. **查看stderr输出**
```python
# 在脚本中添加调试输出
import sys
print("DEBUG: 脚本开始执行", file=sys.stderr)
print(f"DEBUG: 收到输入: {input_data}", file=sys.stderr)
```

### 5.3 Hook超时

**症状**：Hook执行时间过长被强制终止

**解决方案**：

1. **增加timeout配置**

下面是内层 `hooks` 数组中的一个 handler，`timeout` 的单位为秒。先提供实际脚本，再合并到对应事件：

```json
{
  "type": "command",
  "command": "python",
  "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/slow-hook.py"],
  "timeout": 120
}
```

2. **优化脚本性能**
```python
# 避免不必要的文件扫描
# 使用增量检查而不是全量检查
# 并行执行多个检查任务
```

3. **异步处理**
```python
# 对于不需要阻塞的任务，可以后台执行
import subprocess
subprocess.Popen(['python', 'background-task.py'],
                 stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL)
```

### 5.4 Windows特有问题

**问题1：中文乱码**

**症状**：Hook输出中文显示为乱码

**解决方案**：
```python
# 在脚本开头设置编码
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

**问题2：路径分隔符**

**症状**：Windows路径包含反斜杠导致问题

**解决方案**：
```python
# 统一处理路径
file_path = file_path.replace('\\', '/')
```

**问题3：Batch脚本编码**

**症状**：.bat文件中文乱码

**解决方案**：
```batch
@echo off
chcp 65001 >nul
REM 脚本内容...
```

### 5.5 调试技巧

**技巧1：日志文件**
```python
# 写入调试日志
from pathlib import Path
from datetime import datetime

log_file = Path.home() / '.claude' / 'hooks-debug.log'
log_file.parent.mkdir(parents=True, exist_ok=True)

with open(log_file, 'a', encoding='utf-8') as f:
    f.write(f"[{datetime.now()}] {message}\n")
```

**技巧2：条件调试**
```python
import os

# 通过环境变量控制调试模式
DEBUG = os.getenv('CLAUDE_HOOK_DEBUG', '').lower() == 'true'

if DEBUG:
    print(f"DEBUG: {data}", file=sys.stderr)
```

**技巧3：逐步排除法**

先只保留一个 Hook 测试：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Hook triggered!' >&2"
          }
        ]
      }
    ]
  }
}
```

---

## 第六部分：FAQ（20个常见问题）

### 基础问题

**Q1: Hook和CLAUDE.md有什么区别？**

| 对比 | Hook | CLAUDE.md |
|------|------|-----------|
| **执行方式** | 自动执行Shell命令 | Claude解读后决定是否遵循 |
| **可靠性** | 匹配事件自动调用；依赖配置、程序和运行结果 | 依赖Claude是否遵循 |
| **用途** | 强制规则、自动化 | 提供上下文、建议 |

**Q2: Hook可以用什么语言写？**

任何可执行程序都可以：
- Python（推荐，跨平台）
- Bash/Shell（macOS/Linux）
- Batch（Windows）
- Node.js
- Go、Rust等（需要编译）

**Q3: Hook的timeout默认是多少？**

当前默认值按处理器和事件区分：command / http / mcp_tool 通常为600秒，prompt为30秒，agent为60秒；前三类在 UserPromptSubmit、PreModelSwitch、PostModelSwitch 上默认30秒，在 MessageDisplay 上默认10秒。SessionEnd 另有默认1.5秒总预算，显式较长 timeout 可提高预算，但上限60秒。`timeout` 单位是秒，生产检查应按任务明确设置，而不是依赖一个统一默认值。

**Q4: 一个事件可以配置多个Hook吗？**

可以。匹配到同一事件的多个 Hook 会并行运行，不保证数组顺序。如果后一步必须读取前一步的结果，把这些步骤放在同一个脚本里串行执行。下面两个 Hook 应当互不依赖。示例是 `hooks.PostToolUse` 数组中的一个匹配组，需放入现有配置的对应位置：

```json
{
  "matcher": "Write",
  "hooks": [
    {"type": "command", "command": "python hook1.py"},
    {"type": "command", "command": "python hook2.py"}
  ]
}
```

**Q5: PreToolUse的decision有哪些值？**

PreToolUse 有新旧两套API（新旧并存）：

**新版（推荐）** — 通过 `hookSpecificOutput.permissionDecision` 字段：

| 值 | 效果 |
|---|------|
| `"allow"` | 跳过常规权限询问；系统保护例外仍需人工确认 |
| `"deny"` | 拒绝执行，原因会反馈给Claude |
| `"ask"` | 暂停，询问用户决定 |
| 无输出 | 不做决策，按该事件的正常流程继续 |

**旧版（已废弃但仍支持）**：通过 `decision` 字段返回，映射关系见前文“旧版决策值”表。这里不重复展开，实际新脚本优先使用 `hookSpecificOutput.permissionDecision`。

PostToolUse 的 `"block"` 是执行后的反馈，不能撤销工具操作；UserPromptSubmit 的 `"block"` 可阻止提示词提交。无输出表示没有追加决策。

### 配置问题

**Q6: settings.json应该放在哪里？**

项目根目录的 `.claude/settings.json`

**Q7: Matcher支持正则表达式吗？**

支持！例如：
- `"Write"` - 精确匹配
- `"Write|Edit"` - 匹配Write或Edit
- `".*"` - 匹配所有工具（慎用）

**Q8: 如何让Hook只对特定目录的文件生效？**

在脚本中检查文件路径：

```python
if '/articles/' not in file_path:
    sys.exit(0)  # 不在目标目录，跳过
```

**Q9: 环境变量怎么传递给Hook脚本？**

Claude Code自动传递的环境变量：
- `CLAUDE_PROJECT_DIR` - 项目根目录的绝对路径（Claude Code启动目录）

> ⚠️ **注意**：`session_id`不是环境变量，而是通过stdin的JSON输入传递！

使用方法：
```python
import os
import json
import sys

# 从环境变量获取项目目录
project_dir = os.getenv('CLAUDE_PROJECT_DIR', os.getcwd())

# 从stdin的JSON获取session_id（不是环境变量！）
input_data = json.loads(sys.stdin.read())
session_id = input_data.get('session_id', '')
```

**Q10: 如何临时禁用Hook？**

临时关闭可在设置中写 `"disableAllHooks": true`。只想关闭本次会话时，从终端启动：

```bash
claude --settings '{"disableAllHooks": true}'
```

它不能从用户或项目层关闭组织受管 Hook。若只删除某个 Hook，编辑其对应条目即可；不要重命名整个 settings.json，那会连 permissions、env 等其他配置一起停用。

### 脚本问题

**Q11: 如何读取Hook的输入？**

```python
import sys
import json

# stdin读取JSON
input_data = json.loads(sys.stdin.read())
tool_name = input_data.get('tool_name')
```

**Q12: 如何在Hook中向用户输出信息？**

不同事件的输出机制不同。向用户显示消息，通常返回 `systemMessage`；向 Claude 添加上下文，使用该事件支持的 `additionalContext`。两者不要混淆。

```python
import json
print(json.dumps({"systemMessage": "格式化检查完成"}, ensure_ascii=False))
```

PostToolUse 可显示消息、追加上下文或替换工具输出，但不能撤销工具操作。UserPromptSubmit 的纯文本 stdout 或 `hookSpecificOutput.additionalContext` 是给 Claude 的上下文。PreToolUse 的拒绝理由写 `hookSpecificOutput.permissionDecisionReason`。

退出 `0` 时的 stderr 只进入 debug 日志；退出 `2` 或其他非零码的显示、阻断效果要按事件判断。Notification、MessageDisplay 等事件会忽略 `systemMessage`，不要对所有事件套同一返回格式。完整规则见[官方输入输出参考](https://code.claude.com/docs/en/hooks#hook-input-and-output)。

**Q13: 如何返回决策（PreToolUse）？**

使用stdout输出JSON：
```python
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "原因"
    }
}))
```

> 退出码 0 且无输出表示这个 Hook 没有决策，工具调用会走正常权限流程；沉默不等于批准。

**Q14: 脚本报错会影响Claude Code吗？**

需要按事件和返回内容判断。普通脚本错误且没有合法决策时，多数事件报告非阻断错误并继续；PreToolUse 退出 `2` 会阻止工具，合法 JSON 决策也可能拒绝操作。WorktreeCreate 的任意非零退出都会使创建失败，WorktreeRemove 非零且目录仍在会使移除失败。不要把“程序异常”与“策略正常拒绝”混在一起，也不要默认所有失败都会放行。

**Q15: 如何处理Windows/macOS/Linux兼容性？**

```python
import platform
system = platform.system()

if system == 'Windows':
    pass  # 在此放 Windows 特定代码
elif system == 'Darwin':  # macOS
    pass  # 在此放 macOS 特定代码
else:  # Linux
    pass  # 在此放 Linux 特定代码
```

### 高级问题

**Q16: Hook可以修改Claude的输出吗？**

可以改变特定层面的输出：MessageDisplay 的 `hookSpecificOutput.displayContent` 可以替换屏幕显示文本，但不改变会话记录或发给 Claude 的内容；PostToolUse 的 `updatedToolOutput` 可替换随后发给 Claude 的工具结果。UserPromptSubmit 添加上下文，不改写原始用户输入。先区分显示文本、工具结果和实际文件，再选择事件。

**Q17: 多个Hook的执行顺序是什么？**

同一事件匹配到的多个 Hook 会并行运行，不保证配置文件或数组中的顺序。有前后依赖的步骤应放进同一个脚本，由脚本串行执行；Q4 的两个独立 Hook 不能依赖彼此先完成。

**Q18: Hook可以调用Claude API吗？**

可以，但要注意：
- 会消耗额外Token
- 可能导致无限循环
- 建议设置调用限制

**Q19: 如何在团队中共享Hook配置？**

将 `.claude/` 目录加入Git版本控制：
```bash
git add .claude/settings.json
git add .claude/hooks/
git commit -m "Add Claude Code hooks"
```

**Q20: Hook有性能影响吗？**

有一定影响：
- 只有配置的事件和 matcher / if 条件匹配时才运行对应 Hook
- 复杂脚本会增加延迟
- 建议优化脚本性能，设置合理timeout

---

## 附录A：配置速查表

### 本课常用 Hook 类型速查

| Hook类型 | 触发时机 | 输入格式 | 输出格式 | 可阻止 | 重要 |
|----------|----------|----------|----------|--------|:----:|
| UserPromptSubmit | 用户输入后 | JSON | 文本（注入上下文） | V |  |
| PreToolUse | 工具调用前 | JSON | JSON决策 | V | ⭐ |
| PostToolUse | 工具调用成功后 | JSON | JSON 反馈或上下文 | 不撤销已执行操作 | ⭐ |
| Notification | 通知发送时 | JSON | 无 | X |  |
| SessionStart | 会话开始或恢复 | JSON | 文本或 JSON 上下文 | X |  |
| SessionEnd | 会话结束 | JSON | 清理与日志 | X |  |
| Stop | Claude 准备结束响应 | JSON | block + reason | V：可要求继续 |  |
| SubagentStart 🆕 | 子代理启动 | JSON | 无 | X |  |
| SubagentStop | 子代理准备结束 | JSON | block + reason | V：可要求继续 |  |
| PermissionRequest 🆕 | 权限请求 | JSON | JSON决策 | V |  |
| PreCompact 🆕 | 上下文压缩前 | JSON | 退出码 2 或 decision: block | V：可阻止压缩 |  |
| ConfigChange 🆕 | 新配置应用前 | JSON | 退出码 2 或 decision: block | V：policy_settings 除外 |  |
| TeammateIdle 🆕 | 队友即将空闲 | JSON | 退出码 2 + stderr 反馈 | V：让队友继续工作 |  |
| WorktreeCreate | 接管工作树创建 | JSON（含 name） | 创建目录路径 | V：失败或无路径则创建失败 |  |
| WorktreeRemove | 工作树即将移除 | JSON（含 worktree_path） | 退出码；JSON 决策忽略 | V：非零且目录仍存在则失败 |  |
| StopFailure 🆕 | API异常停止 | JSON | 无 | X |  |
| PostCompact 🆕 | 上下文压缩后 | JSON | 无 | X |  |
| InstructionsLoaded 🆕 | 指令文件加载 | JSON | 无 | X |  |
| Elicitation 🆕 | MCP 请求输入 | JSON | action / content，或退出码 2 | V：可拒绝请求 |  |
| ElicitationResult 🆕 | 输入返回 MCP 前 | JSON | action / content，或退出码 2 | V：可拒绝响应 |  |
| PreModelSwitch | 用户或客户端请求切换模型前 | JSON | JSON 决策 | V |  |
| PostModelSwitch | 模型切换后 | JSON | 文本或 JSON 上下文 | 不撤销切换 |  |

此表只列本课常用事件。其他事件及精确输入、输出字段请查[官方事件参考](https://code.claude.com/docs/en/hooks#hook-events)。

### 常用工具名速查

| 工具名 | 功能 | 常用Hook | 重要 |
|--------|------|---------|:----:|
| Write | 写入文件 | PostToolUse格式化 | ⭐ |
| Edit | 编辑文件 | PostToolUse备份 |  |
| Read | 读取文件 | PreToolUse权限控制 |  |
| Bash | 执行命令 | PreToolUse危险命令拦截 | ⭐ |
| Glob | 文件搜索 | - |  |
| Grep | 内容搜索 | - |  |
| WebSearch | 网络搜索 | - |  |

### Decision值速查

**PreToolUse 新版API**（`hookSpecificOutput.permissionDecision`，推荐）：

| 值 | 含义 | 工具执行 | 重要 |
|----|------|---------|:----:|
| `"allow"` | 跳过常规权限询问；系统保护例外仍需确认 | 通常执行 | ⭐ |
| `"deny"` | 拒绝，原因反馈给Claude | X | ⭐ |
| `"ask"` | 暂停，询问用户 | ? |  |
| 无输出 | 不做决策，交给正常权限流程 | 按权限设置决定 |  |

**PreToolUse 旧版 API**：`decision` 字段仍可兼容旧脚本，映射关系沿用前文“旧版决策值”表；新脚本优先写新版字段。

**PostToolUse / UserPromptSubmit**：

| 值 | 含义 |
|----|------|
| `"block"` | UserPromptSubmit 阻止提交；PostToolUse 提供执行后反馈，不撤销工具操作 |
| 无输出 | 不做决策，按该事件的正常流程继续 |

---

## 附录B：完整脚本模板

### Python脚本模板

```python
#!/usr/bin/env python3
"""
Hook名称 - 功能描述
"""
import sys
import json

def main():
    # 读取输入
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    # 你的逻辑
    # ...

    # 本例退出0时，stderr只进入debug日志
    print("信息", file=sys.stderr)

    # PreToolUse 如需拒绝，使用合法的事件专用字段：
    # print(json.dumps({"hookSpecificOutput": {
    #     "hookEventName": "PreToolUse", "permissionDecision": "deny",
    #     "permissionDecisionReason": "拒绝原因"
    # }}))

if __name__ == '__main__':
    main()
```

### Bash脚本模板

```bash
#!/bin/bash
# Hook名称 - 功能描述

# 读取stdin
input_json=$(cat)

# 使用Python解析JSON
tool_name=$(echo "$input_json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))")

# 你的逻辑
# ...

# 输出日志
echo "信息" >&2

exit 0
```

---

## 附录C：参考资源

### 官方文档

- [Claude Code Hooks官方文档](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Claude Code官方指南](https://docs.anthropic.com/en/docs/claude-code)

### 社区资源

- [ClaudeLog Hooks教程](https://claudelog.com/mechanics/hooks/)
- [GitButler Agent 集成](https://docs.gitbutler.com/ai-agents/getting-started)：按当前官方支持配置 Agent 集成，旧 Hooks 专页已移除。
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)

### 相关课程

- 第3部分：Commands系统 - Slash命令开发
- 第4部分：MCP集成 - 外部工具连接
- 第6部分：Skills定制 - 技能包开发

---

## 学习总结

通过本课学习，你已经掌握：

1. **Hooks核心概念**：理解Hook是什么、为什么需要、能做什么
2. **常用事件族**：工具调用、会话、子代理、权限、压缩、配置、工作树和 MCP 交互等事件的适用场景与控制方式
3. **配置方法**：settings.json配置格式、Matcher语法、timeout设置
4. **实战场景**：Git自动化、代码格式化、文件保护、质量检查
5. **故障排查**：常见问题诊断和解决方法
6. **安全意识**：Hook安全风险和最佳实践

**下一步建议**：

1. 从第二部分的简单示例开始实践
2. 根据你的项目需求，选择合适的Hook类型
3. 参考第四部分的实战案例，逐步构建自己的自动化工作流
4. 遇到问题查阅第五部分和第六部分

**记住**：Hooks是自动化的终极武器，合理使用可以让你的开发效率翻倍！
