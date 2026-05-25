# Claude Code Plugins生态完整指南：从安装到自定义开发

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：4-6小时
> - **难度等级**：⭐⭐ 入门级
> - **更新日期**：2026年4月
> - **适用版本**：Claude Code v2.1.150（验证于 2026-05-25；v2.1.90+ 插件市场 env 见文内 release 摘录）

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/claude-code-agent-view-dark.png" alt="Claude Code 官方 Agent View 深色界面：Needs input、Working、Completed 分组" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-agent-view.png" alt="Claude Code 官方 Agent View：多后台会话状态" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-product-ui.jpg" alt="Claude Code 官方 CLI 任务界面：任务执行、文件变更与终端状态" width="720"/></p>

完成本课学习后，你将能够：

1. **理解Plugin生态**：掌握Plugin与Commands/Skills/MCP的区别
2. **安装和使用Plugin**：掌握当前 `/plugin` + market 的主路径，以及本地目录开发模式
3. **浏览Marketplace**：在官方市场发现和安装 Plugin
4. **创建自定义Plugin**：从零开发一个完整的Plugin包
5. **发布Plugin**：将Plugin分享到GitHub和社区
6. **排查Plugin问题**：独立解决90%的常见故障

---

## 🗺️ 学习路径导航（先看这里！）

### 路径A：快速上手（⏱️ 30分钟）

**适合人群**：急着用Plugin，想快速体验

**只看这些章节**：

```
✅ 术语表（3分钟）
✅ 第1章：Plugins概览（10分钟）
✅ 第2章：5分钟快速开始（15分钟）
```

### 路径B：Plugin开发者（⏱️ 3小时）

**适合人群**：想创建自己的Plugin

**学习顺序**：

```
✅ 第1-2章：概念+快速上手（30分钟）
✅ 第3章：Marketplace深度指南（30分钟）
✅ 第4章：创建自定义Plugin（90分钟）
✅ 第5章：发布与分享（30分钟）
```

### 路径C：问题排查（⏱️ 5分钟）

**适合人群**：Plugin出问题了

**直接跳到**：

```
🔧 第6章：故障排查指南
🔧 第7章：FAQ
```

---

## 术语表（小白必读）

| 术语 | 英文 | 解释 |
|------|------|------|
| **Plugin** | Plugin | Claude Code 的扩展包，可封装 agents、skills、hooks、MCP、LSP、bin、settings 等资源 |
| **Marketplace** | Marketplace | Plugin商店，浏览和发现Plugin的网页平台 |
| **.claude-plugin/plugin.json** | - | Plugin的元数据清单文件，位于 `.claude-plugin/` 子目录中 |
| **--plugin-dir** | - | Claude Code 启动参数，主要用于本地开发 / 调试加载指定目录 |
| **Skill** | Skill | Plugin中的核心能力模块（SKILL.md定义） |
| **Hook** | Hook | Plugin中的自动化触发器（如代码提交前检查） |

---

## 第1章：Plugins生态概览

> **v2.1.143→v2.1.150 插件更新**：插件依赖会被强制检查；Marketplace / Browse / Details 会展示 commands、agents、skills、hooks、MCP/LSP servers、更新时间和 projected context cost；插件启用、禁用、安装、HTTPS clone 以及 root-level `SKILL.md` 暴露都有修复。教程中遇到插件清单差异时，以 `/plugin` 当前界面为准。

### 1.1 什么是Claude Code Plugin？

**定义**：

Plugin是Claude Code的扩展包，可以添加新的命令、专业能力和自动化流程，且可以跨项目和团队共享。

**类比理解**：

```
手机              |  Claude Code
------------------|------------------
操作系统(iOS/Android) | Claude Code核心
App Store        | Plugin Marketplace（网页）
安装的APP        | 已安装的Plugins
APP更新          | Plugin手动更新（git pull）
```

**核心价值**：

1. **可复用性**：一次开发，多个项目使用
2. **易分享性**：通过GitHub一键克隆
3. **模块化**：每个Plugin专注一个领域
4. **社区驱动**：社区持续贡献优质Plugin

### 1.2 Plugins vs Commands/Skills/MCP

| 维度 | Commands | Skills | MCP | **Plugins** |
|------|----------|--------|-----|-------------|
| **定义** | Markdown提示词 | 专业Agent能力 | 外部服务集成 | **打包的扩展** |
| **位置** | `.claude/commands/`（兼容层） | `.claude/skills/` | `.mcp.json` | **本地目录 + market 安装** |
| **可分享性** | ❌ 手动复制 | ❌ 手动复制 | ⚠️ 需配置 | **✅ 市场安装 / CLI / 本地开发目录** |
| **包含内容** | 单个提示词 | 多个文件+配置 | 服务器配置 | **manifest + agents/skills/hooks/MCP/LSP/bin/settings** |
| **加载方式** | 自动（在项目目录中） | 自动（在项目目录中） | 自动（配置后） | **`/plugin` 为主，`--plugin-dir` 为本地开发补充** |

**关键区别**：Plugin是一个"超集"概念：

```
Plugin = manifest + runtime resources + optional markets/scope + 文档
```

### 1.3 Plugins生态现状（2026年4月）

**官方数据**：

- **当前版本**：Claude Code v2.1.150（2026年5月验证）
- **官方市场**：✅ 已上线，可通过 `/plugin` 和网页入口协同使用
- **社区Plugin**：持续增长中

**主流Plugin来源**：

1. **Anthropic官方Marketplace**：
   - URL：`https://code.claude.com/plugins`
   - 特点：审核严格，质量保证，网页浏览

2. **Jeremy Longshore社区合集**：
   - URL：`https://github.com/jeremylongshore/claude-code-plugins-plus`
   - 特点：100%符合Anthropic Skills Schema

3. **GitHub搜索**：
   - 搜索关键词：`claude-code-plugin`
   - 特点：最丰富的来源，质量参差不齐

> ⚠️ **重要说明**：Claude Code 现在既有交互里的 `/plugin`，也有 CLI 子命令 `claude plugin`（别名 `claude plugins`）。对普通用户来说，`/plugin` 依旧是最顺手的入口；`claude plugin` 更适合脚本化和精确控制作用域。

---

## 第2章：5分钟快速开始

### 2.1 安装你的第一个Plugin

**目标**：先用官方主路径装一个 Plugin，再了解本地开发模式

**前置条件检查**：

```bash
# 确认Claude Code已安装
claude --version
# 预期输出：2.1.92 (Claude Code)

# 确认在项目目录中
cd /path/to/your/project
```

**步骤1：在 Claude Code 里打开插件入口**

```text
/plugin
```

在这里你可以浏览市场、查看已安装插件、执行安装和管理操作。

**步骤2：按市场路径安装**

```text
/plugin install <plugin-name-or-market-entry>
```

> 💡 **实际名称** 取决于当前 market 提供的条目。最稳妥的做法是先 `/plugin` 浏览，再从列表里安装。

**步骤3：确认插件已生效**

安装后，检查对应的命令、skill 或行为是否已经出现在会话里。

---

### 2.2 本地开发模式：使用 `--plugin-dir`

如果你在本地开发一个还没发布到市场的 Plugin，才需要手动目录加载。

```bash
# 创建plugins目录（如果不存在）
mkdir -p .claude/plugins

# 克隆一个Plugin（以社区Plugin为例）
git clone https://github.com/jeremylongshore/claude-code-plugins-plus .claude/plugins/plugins-plus
```

**步骤1：克隆Plugin到本地**

```bash
# 创建plugins目录（如果不存在）
mkdir -p .claude/plugins

# 克隆一个Plugin（以社区Plugin为例）
git clone https://github.com/jeremylongshore/claude-code-plugins-plus .claude/plugins/plugins-plus
```

**步骤2：使用 `--plugin-dir` 加载Plugin**

```bash
# 启动Claude Code时指定Plugin目录
claude --plugin-dir .claude/plugins/plugins-plus
```

Claude Code 会自动扫描该目录下的 `.claude-plugin/plugin.json`，加载其中定义的 manifest、skills、hooks、agents 等资源。

> 💡 **开发小技巧**：开发本地 Plugin 时，优先把 `--plugin-dir` 当成调试入口，而不是最终分发方式。

**步骤3：验证Plugin已加载**

在Claude Code交互模式中：

```bash
You: /help

# 如果Plugin包含自定义命令，你会在命令列表中看到它们
# 如果Plugin包含Skills，Claude会自动获得对应能力
```

**步骤4：多个Plugin目录**

```bash
# 可以同时加载多个Plugin目录
claude --plugin-dir ./plugin-a --plugin-dir ./plugin-b
```

### 2.3 卸载Plugin

如果你是通过市场安装，优先在 `/plugin` 里卸载；如果你是本地目录加载，删除目录即可：

```bash
# 删除Plugin目录
rm -rf .claude/plugins/plugins-plus

# 下次启动不带 --plugin-dir 参数即可
```

---

## 第3章：使用Marketplace深度指南

### 3.1 浏览Marketplace

> ⚠️ **注意**：Marketplace 是**网页平台**，不是CLI命令。

**访问方式**：

打开浏览器访问 `https://code.claude.com/plugins`

**Marketplace功能**：

| 功能 | 说明 |
|------|------|
| **分类浏览** | 按用途分类：文档处理、代码质量、项目管理等 |
| **搜索** | 按关键词搜索Plugin |
| **详情页** | 查看 Plugin 说明、安装量、评分、仓库链接 |
| **安装指引** | 每个Plugin页面提供安装命令（git clone） |

### 3.2 安装Plugin的方式

**方式1：从GitHub克隆（最常用）**

```bash
# 在Marketplace找到Plugin后，复制其GitHub地址
git clone https://github.com/author/my-plugin .claude/plugins/my-plugin

# 启动时加载
claude --plugin-dir .claude/plugins/my-plugin
```

**方式2：指定本地路径（开发调试用）**

```bash
# 直接指向本地开发中的Plugin
claude --plugin-dir /path/to/my-local-plugin
```

**方式3：指定当前目录（Plugin项目本身）**

```bash
# 在Plugin项目根目录中
claude --plugin-dir .
```

### 3.3 管理已安装Plugins

由于Plugin就是本地目录，管理操作都是标准文件/git操作：

```bash
# 查看已安装的Plugins
ls .claude/plugins/

# 更新Plugin（git pull最新版本）
cd .claude/plugins/my-plugin && git pull

# 切换Plugin版本
cd .claude/plugins/my-plugin && git checkout v1.2.0

# 查看Plugin信息
cat .claude/plugins/my-plugin/.claude-plugin/plugin.json
```

### 3.4 Plugin配置

部分Plugin支持自定义配置。查看Plugin的 `.claude-plugin/plugin.json`：

```bash
# 查看Plugin元数据
cat .claude/plugins/my-plugin/.claude-plugin/plugin.json
```

配置方式取决于Plugin的实现——通常在Plugin目录下创建配置文件。具体请参考每个Plugin的README。

---

## 第4章：创建自定义Plugin

### 4.1 Plugin结构规范

**最小Plugin结构**：

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # 必需：Plugin元数据清单
├── .mcp.json            # 可选：MCP配置
├── README.md            # 推荐：使用文档
├── skills/              # 可选：Agent Skills
│   └── my-skill/
│       └── SKILL.md
├── commands/            # 可选：Slash Commands
│   └── my-command.md
├── agents/              # 可选：Agent定义
│   └── my-agent.md
└── hooks/               # 可选：Hooks
    └── pre-commit.py
```

**.claude-plugin/plugin.json 规范**：

```json
{
  "name": "my-awesome-plugin",
  "description": "A plugin that does awesome things",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

> 💡 **注意**：`plugin.json` 必须放在 `.claude-plugin/` 子目录中，不是 Plugin 根目录。`name`、`description`、`version` 是最常见核心字段，`author` 是可选项，且官方示例中通常写成对象。

### 4.2 创建第一个Plugin：Hello World

**步骤1：创建Plugin目录**

```bash
mkdir -p hello-world-plugin/.claude-plugin
mkdir -p hello-world-plugin/skills/hello
cd hello-world-plugin
```

**步骤2：创建 .claude-plugin/plugin.json**

```json
{
  "name": "hello-world-plugin",
  "description": "A simple hello world plugin for learning",
  "version": "1.0.0",
  "author": {
    "name": "Claude Student"
  }
}
```

**步骤3：创建第一个 Skill**

创建 `skills/hello/SKILL.md`：

```markdown
---
description: Greet the user with a friendly message
disable-model-invocation: true
---

Greet the user warmly and ask how you can help them today.
```

**步骤4：创建 README.md**

```markdown
# Hello World Plugin

A simple plugin that adds a namespaced skill to Claude Code.

## Installation

\`\`\`bash
claude --plugin-dir ./hello-world-plugin
\`\`\`

## Usage

In Claude Code interactive mode:
\`\`\`
You: /hello-world-plugin:hello
\`\`\`

## Features

- Creative greetings
- Current date display
- Random programming jokes
```

**步骤5：测试 Plugin**

```bash
# 在项目目录中启动Claude Code，加载Plugin
claude --plugin-dir /path/to/hello-world-plugin

# 在交互模式中使用
You: /hello-world-plugin:hello
```

> 💡 **为什么这里用了 namespaced 命令？** 官方当前规范里，plugin 内的 skill 会自动加上 `plugin-name:` 前缀，例如 `/hello-world-plugin:hello`。这样做是为了避免多个 plugin 之间撞名。

### 4.3 进阶Plugin：带Skills的Plugin

**目标**：创建一个包含Skill的Plugin，让Claude具备代码审查能力

**目录结构**：

```
code-review-plugin/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   └── review.md
└── skills/
    └── code-reviewer/
        └── SKILL.md
```

**skills/code-reviewer/SKILL.md**：

```markdown
---
name: code-reviewer
description: Expert code review skill
---

You are an expert code reviewer. When reviewing code:

1. Check for security vulnerabilities (SQL injection, XSS, etc.)
2. Identify performance bottlenecks
3. Suggest improvements for readability
4. Verify error handling completeness
5. Check naming conventions consistency

Output format:
- 🔴 CRITICAL: Must fix before merge
- 🟡 WARNING: Should fix
- 🟢 INFO: Nice to have
```

**commands/review.md**：

```markdown
Review the current git diff and provide a detailed code review.
Use the code-reviewer skill for analysis.
Focus on security, performance, and maintainability.
```

**测试**：

```bash
claude --plugin-dir ./code-review-plugin

You: /code-review-plugin:review
# Claude会在 plugin 命名空间下调用 review 入口，并结合 code-reviewer skill 分析你的代码变更
```

### 4.4 Plugin最佳实践

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个Plugin专注一个领域（代码审查、文档生成等） |
| **清晰文档** | README必须包含安装步骤、使用示例、配置说明 |
| **版本管理** | 使用语义化版本号（SemVer），打git tag |
| **最小依赖** | 尽量减少外部依赖，保持Plugin轻量 |
| **安全第一** | 不在Plugin中硬编码密钥，使用环境变量 |

---

## 第5章：发布与分享Plugin

### 5.1 发布前检查清单

```
✅ .claude-plugin/plugin.json 字段完整（至少有 name / version / description；author 推荐但可选）
✅ README.md 包含安装和使用说明
✅ 所有命令和Skills已测试通过
✅ 无硬编码密钥或敏感信息
✅ .gitignore 排除了不必要的文件
✅ LICENSE 文件存在
```

### 5.2 发布到GitHub

```bash
# 初始化git仓库
cd my-plugin
git init
git add -A
git commit -m "feat: initial release v1.0.0"

# 创建GitHub仓库并推送
gh repo create my-plugin --public --source=. --push

# 打版本标签
git tag v1.0.0
git push --tags
```

**推荐的GitHub仓库设置**：

- 添加 Topics：`claude-code-plugin`、`claude-code`、`ai-plugin`
- 写清楚 Description
- 添加 `claude-code-plugin` topic 方便社区搜索发现

### 5.3 分享到社区

1. **提交到 claude-code-plugins-plus**：
   - Fork `jeremylongshore/claude-code-plugins-plus`
   - 添加你的Plugin信息
   - 提交PR

2. **在GitHub Discussions分享**：
   - 到 `anthropics/claude-code` 的 Discussions 板块分享

3. **提交到官方Marketplace**：
   - 访问 `code.claude.com/plugins` 查看提交指南
   - 需要通过官方审核

---

## 第6章：故障排查指南

### 6.1 Plugin加载失败

**症状**：`--plugin-dir` 指定后，Plugin的命令/Skills没有生效

**排查步骤**：

```bash
# 1. 确认路径正确
ls /path/to/your/plugin/.claude-plugin/plugin.json

# 2. 验证plugin.json格式
cat /path/to/your/plugin/.claude-plugin/plugin.json | python3 -m json.tool

# 3. 使用debug模式启动
claude --plugin-dir /path/to/your/plugin --debug
```

### 6.2 命令不显示

**可能原因**：

| 原因 | 解决方案 |
|------|----------|
| commands目录路径错误 | 确认在Plugin根目录下有 `commands/` 目录 |
| 命令文件不是.md格式 | 命令文件必须是 `.md` 后缀 |
| .claude-plugin/plugin.json 缺失 | 确认Plugin根目录下有 `.claude-plugin/plugin.json` |
| 文件权限问题 | 确认文件可读：`chmod 644 commands/*.md` |

### 6.3 Skills不生效

**排查**：

```bash
# 确认SKILL.md存在且格式正确
cat /path/to/plugin/skills/my-skill/SKILL.md

# 确认frontmatter格式
# 必须以 --- 开头和结尾，包含name和description
```

### 6.4 多Plugin冲突

如果多个Plugin定义了同名命令：

```bash
# 后加载的Plugin会覆盖先加载的
# 调整 --plugin-dir 的顺序来控制优先级
claude --plugin-dir ./plugin-low-priority --plugin-dir ./plugin-high-priority
```

---

## 第7章：FAQ（常见问题）

### Q1：Plugin和Skill有什么区别？

**Skill** 是单个能力定义（一个SKILL.md文件），**Plugin** 是一个完整的扩展包，可以包含多个Skills + Commands + Hooks + MCP配置。Plugin是Skill的超集。

### Q2：有没有 `claude plugins install` 命令？

Claude Code 现在同时提供两类入口：
1. 交互模式里的 `/plugin`
2. CLI 里的 `claude plugin`（别名 `claude plugins`）

日常使用更推荐 `/plugin`，本地开发和自动化更常用 `claude plugin ...` 或 `--plugin-dir`。

### Q3：Plugin会访问我的代码吗？

Plugin中的Skills和Commands在Claude Code的沙箱中运行，遵循与内置工具相同的权限模型。Plugin不能绕过权限系统。

### Q4：如何更新Plugin？

```bash
cd .claude/plugins/my-plugin
git pull origin main
```

下次启动Claude Code时会自动加载最新版本。

### Q5：如何卸载Plugin？

```bash
# 删除Plugin目录
rm -rf .claude/plugins/my-plugin

# 启动时不再指定该 --plugin-dir 即可
```

### Q6：可以同时加载多少个Plugin？

没有硬性限制，但每个Plugin都会增加上下文占用。建议同时加载不超过5个Plugin，按需加载。

### Q7：Plugin开发需要懂编程吗？

不一定。最简单的Plugin只需要写Markdown文件（Commands和Skills都是Markdown）。只有需要Hooks（自动化脚本）时才需要编程能力。

### Q8：Plugin可以离线使用吗？

可以。Plugin是本地文件，加载后不需要网络。但如果Plugin包含MCP配置连接外部服务，那部分功能需要网络。

### Q9：如何让Plugin在所有项目中生效？

```bash
# 方法1：每次启动时指定
claude --plugin-dir ~/.claude/global-plugins/my-plugin

# 方法2：设置shell别名
alias claude='claude --plugin-dir ~/.claude/global-plugins/my-plugin'
```

### Q10：Plugin报错如何获取帮助？

1. 查看Plugin的GitHub Issues
2. 使用 `claude --debug` 查看详细日志
3. 检查Plugin的README中的Troubleshooting部分

---

## 🔗 相关链接

| 资源 | 链接 | 说明 |
|------|------|------|
| **上一节** | [07-Skills定制完整指南](./07-Skills定制完整指南.md) | 创建可复用功能包 |
| **下一节** | [09-Agent-SDK完整指南](./09-Agent-SDK完整指南.md) | 编程开发AI Agent |

---

## 📋 附录：速查表

### Plugin操作速查

| 操作 | 命令 |
|------|------|
| **安装Plugin** | `/plugin install <name>` |
| **浏览市场** | 交互里输入 `/plugin`，或浏览器访问 `code.claude.com/plugins` |
| **本地开发加载** | `claude --plugin-dir .claude/plugins/<name>` |
| **本地加载多个** | `claude --plugin-dir ./a --plugin-dir ./b` |
| **更新本地克隆** | `cd .claude/plugins/<name> && git pull` |
| **卸载本地Plugin** | `rm -rf .claude/plugins/<name>` |
| **查看Plugin信息** | `cat .claude/plugins/<name>/.claude-plugin/plugin.json` |
| **开发时重载** | 修改后重新启动会话，或重新以 `--plugin-dir` 进入调试 |
| **调试Plugin** | `claude --plugin-dir <path> --debug` |

### Plugin目录结构速查

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # 必需：元数据清单
├── .mcp.json            # 可选：MCP配置
├── README.md            # 推荐：文档
├── commands/*.md        # 可选：Slash命令
├── skills/*/SKILL.md    # 可选：Agent能力
├── agents/*.md          # 可选：Agent定义
└── hooks/*.py           # 可选：自动化脚本
```

> 💡 **命名空间**：Plugin中的Skills会自动添加命名空间前缀，格式为 `/plugin-name:skill-name`，避免与其他Plugin冲突。

---

> **最后更新**：2026年5月25日 | **适用版本**：Claude Code v2.1.150
