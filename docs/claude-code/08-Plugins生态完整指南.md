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
> - **更新日期**：2026年9月14日
> - **适用版本**：Claude Code v2.1.270（验证于 2026-09-14；旧差量和 v2.1.90+ 插件市场 env 说明保留为历史基线）

---

## 📚 本课学习目标

我看插件生态时最关心三件事：来源、权限、可撤销；这比插件名字听起来多厉害更重要。

完成本课学习后，你将能够：

1. **理解Plugin生态**：掌握Plugin与Commands/Skills/MCP的区别
2. **安装和使用Plugin**：掌握当前 `/plugin` + market 的主路径，以及本地目录开发模式
3. **浏览Marketplace**：在官方市场发现和安装 Plugin
4. **创建自定义Plugin**：从零开发一个完整的Plugin包
5. **发布Plugin**：将Plugin分享到GitHub和社区
6. **排查Plugin问题**：解决大多数常见故障

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
| **Marketplace** | Marketplace | 列出插件与下载来源的目录，可通过 `/plugin` 或 `claude plugin marketplace` 注册和管理；网页是浏览入口之一 |
| **.claude-plugin/plugin.json** | - | Plugin的元数据清单文件，位于 `.claude-plugin/` 子目录中 |
| **--plugin-dir** | - | Claude Code 启动参数，主要用于本地开发 / 调试加载指定目录 |
| **Skill** | Skill | Plugin中的核心能力模块（SKILL.md定义） |
| **Hook** | Hook | Plugin中的自动化触发器（如代码提交前检查） |

---

## 第1章：Plugins生态概览


> **2026-09-14 插件更新（v2.1.270 基线）**：v2.1.224 起支持通过 HTTPS zip 安装 archive 插件，并可选 SHA-256 固定校验；v2.1.232 起市场支持 GitLab 仓库，`/plugin install plugin@marketplace` 会先刷新市场。v2.1.233 起，`claude plugin validate` 还能检查 `.claude/skills` 目录。v2.1.269 新增 `claude plugin eval`，用于运行插件评测集并生成 JSON 和 HTML 报告；它会运行评测，先用 `claude plugin eval --help` 确认参数与所需环境，再按评测集说明执行。来源：[官方 changelog](https://code.claude.com/docs/en/changelog)。

> **v2.1.139→v2.1.158 插件更新**：插件依赖会被强制检查；Marketplace / Browse / Details 会展示 commands、agents、skills、hooks、MCP/LSP servers、更新时间和 projected context cost；插件启用、禁用、安装、HTTPS clone 以及 root-level `SKILL.md` 暴露都有修复。v2.1.153 起 `github` / `git` marketplace source 可用 `skipLfs` 跳过 Git LFS 下载；无 GitHub SSH key 的环境可用 `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` 优先 HTTPS clone。v2.1.154 起插件可在 `plugin.json` 或 marketplace entry 声明 `defaultEnabled: false`，由用户通过 `/plugin` 或 `claude plugin enable` 显式开启；Discover tab 也会根据当前目录给出 “suggested for this directory” 推荐。v2.1.157 起 `.claude/skills` 目录里的插件会自动加载，无需 marketplace；`claude plugin init <name>` 可直接脚手架新插件，`/plugin` 参数也会补全子命令、已安装插件和已知 marketplace 插件。企业环境还要看 `pluginSuggestionMarketplaces` allowlist，避免把未经允许的组织市场推荐给用户。教程中遇到插件清单差异时，以 `/plugin` 当前界面为准。

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
APP更新          | 市场插件用 /plugin 更新；开发目录才用 git pull
```

**核心价值**：

1. **可复用性**：一次开发，多个项目使用
2. **易分享性**：通过GitHub一键克隆
3. **模块化**：每个Plugin专注一个领域
4. **社区驱动**：社区持续贡献优质Plugin

### 插件的新扩展方式：Mods

v2.1.287（2026-10-01）新增 Claude Mods：插件可以用 mods 注册事件处理、界面面板、命令和工具调用规则。它适合需要更深行为或界面扩展的插件，普通 Markdown Skill 仍按原方式使用。先看[官方 Mods 概览](https://code.claude.com/docs/en/plugins/mods/overview)，核对客户端版本、运行环境和组织策略；本课的 Hello World 不依赖 Mods。

此外，v2.1.275 起，claude.ai 账号启用的 skills 和 plugins 可以同步到已登录的终端。需要关闭对应同步时，使用 `syncClaudeAiSkills: false` 或 `syncClaudeAiPlugins: false`。遇到“本地没有装却出现了资源”，先检查账号同步和 `/plugin`，再排查项目目录。

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

### 1.3 Plugins 生态现状（2026年9月）

**官方数据**：

- **当前版本**：Claude Code v2.1.270（2026年9月14日验证）
- **官方市场**：✅ 已上线，可通过 `/plugin` 和网页入口协同使用
- **社区Plugin**：持续增长中

**主流Plugin来源**：

1. **Anthropic官方Marketplace**：
   - URL：`https://code.claude.com/plugins`
   - 特点：审核严格，质量保证，网页浏览

2. **Jeremy Longshore社区合集**：
   - URL：`https://github.com/jeremylongshore/claude-code-plugins-plus`
   - 特点：社区维护的插件合集；安装前按具体插件检查清单、资源目录和依赖，不能保证整个合集都通过当前官方校验

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

这一段按三步走：先把插件目录放进本地项目，再用 `--plugin-dir` 指给 Claude Code，最后在会话里确认资源是否出现。

**步骤1：准备一个真正的插件目录**

先完成第4.2节的 `hello-world-plugin`，或者克隆你已检查过的单个插件仓库。若下载的是插件合集，应按其目录说明找到具体插件；合集仓库根目录不一定就是一个可加载的插件。

**步骤2：加载该插件目录**

```bash
claude --plugin-dir /path/to/hello-world-plugin
```

插件资源位于标准目录时，manifest 可以省略；需要元数据、自定义路径或配置选项时，再使用 `.claude-plugin/plugin.json`。

**步骤3：在会话里确认入口**

```text
/hello-world-plugin:hello
```

**加载多个插件目录**：

```bash
claude --plugin-dir ./plugin-a --plugin-dir ./plugin-b
```

### 2.3 卸载Plugin

通过市场安装的插件，在 `/plugin` 中卸载，或用 `claude plugin uninstall <name>@<marketplace> --scope <scope>`，作用域与安装时一致。通过 `--plugin-dir` 加载的开发目录，下一次启动不再传该目录即可；不用先删除开发文件。想回收空间时，确认具体目录和文件都不再需要后再自行清理。

---

## 第3章：使用Marketplace深度指南


### 3.1 浏览Marketplace

Marketplace 是插件目录，Claude Code 通过已注册的目录发现插件。你可以在交互界面的 `/plugin` 中浏览，也可以用 `claude plugin marketplace` 在终端管理；网页浏览是补充入口。

**访问方式**：

打开浏览器访问 `https://code.claude.com/plugins`

**Marketplace功能**：

| 功能 | 说明 |
|------|------|
| **分类浏览** | 按用途分类：文档处理、代码质量、项目管理等 |
| **搜索** | 按关键词搜索Plugin |
| **详情页** | 查看当前条目的说明、来源、组件及安装信息；展示内容以页面为准 |
| **安装指引** | 按条目所属市场安装，通常为 `/plugin install <name>@<marketplace>`；克隆仓库只用于需要自己加载的开发目录 |

### 3.2 安装Plugin的方式

**方式1：通过已注册市场安装（日常主路径）**

在会话里先用 `/plugin` 浏览，然后执行 `/plugin install <name>@<marketplace>`。如果是开发中的插件或尚未加入市场的单独仓库，再按下面的本地加载方式操作。

**本地开发：克隆单个插件仓库**

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

通过 marketplace 安装的插件，用 `/plugin` 或 CLI 管理，并注意安装作用域；不要直接修改其缓存目录。先在终端执行 `claude plugin list` 查看，再按需用 `claude plugin update <name>@<marketplace>` 或 `claude plugin uninstall <name>@<marketplace>` 操作。

下面的文件 / git 操作只适用于你自己克隆并通过 `--plugin-dir` 加载的开发目录：

```bash
# 查看已安装的Plugins
ls .claude/plugins/

# 更新Plugin（git pull最新版本）
git -C .claude/plugins/my-plugin pull

# 切换Plugin版本
git -C .claude/plugins/my-plugin checkout v1.2.0
# 仅当仓库确实存在该 tag；有本地修改时先妥善保存

# 查看Plugin信息
cat .claude/plugins/my-plugin/.claude-plugin/plugin.json
```

### 3.4 Plugin配置

v2.1.285 起，终端可以用 `claude plugin configure <name>@<marketplace>` 查看插件提供的选项及缺失值；先用 `claude plugin list` 取得完整 ID，configure 不接受单独的插件名。交互会话也可以在 `/plugin` 的插件详情中配置。只有插件声明了相应选项才会出现，具体取值以它的说明为准。不要直接编辑市场安装的插件缓存；自动化输入方式先查 `claude plugin configure --help`。

部分Plugin支持自定义配置。查看Plugin的 `.claude-plugin/plugin.json`：

```bash
# 查看Plugin元数据
cat .claude/plugins/my-plugin/.claude-plugin/plugin.json
```

对于你自己维护并用 `--plugin-dir` 加载的开发目录，配置文件按其 README 创建。市场安装的插件按 `/plugin` 或 `claude plugin configure` 提供的选项配置；如果 README 要求外部配置文件，使用它指定的位置，不要把设置写到安装缓存中。

---

## 第4章：创建自定义Plugin

### 4.1 Plugin结构规范

**最小Plugin结构**：

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # 可选但推荐：Plugin元数据清单
├── .mcp.json            # 可选：MCP配置
├── README.md            # 推荐：使用文档
├── skills/              # 可选：Agent Skills
│   └── my-skill/
│       └── SKILL.md
├── commands/            # 可选：Slash Commands
│   └── my-command.md
├── agents/              # 可选：Agent定义
│   └── my-agent.md
└── hooks/               # 可选：Hook配置与脚本
    ├── hooks.json       # 注册事件与处理器；仅放脚本不会自动执行
    └── pre-commit.py    # 由hooks.json里的command处理器调用
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
claude --plugin-dir /path/to/hello-world-plugin
\`\`\`

## Usage

In Claude Code interactive mode:
\`\`\`
You: /hello-world-plugin:hello
\`\`\`

## Features

- A friendly greeting
- A question about how Claude can help
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
Use the code-review-plugin:code-reviewer skill for analysis.
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
✅ 使用 manifest 时包含必填 name，并按需填写 version、description、author；标准目录插件可以省略 manifest
✅ 运行 claude plugin validate <插件目录>，检查错误与警告
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
# 1. 确认指定的是实际插件根目录
ls /path/to/your/plugin

# 2. 校验资源、manifest和自定义路径；标准目录插件可省略manifest
claude plugin validate /path/to/your/plugin

# 3. 使用debug模式启动
claude --plugin-dir /path/to/your/plugin --debug
```

### 6.2 命令不显示

**可能原因**：

| 原因 | 解决方案 |
|------|----------|
| commands目录路径错误 | 确认在Plugin根目录下有 `commands/` 目录 |
| 命令文件不是.md格式 | 命令文件必须是 `.md` 后缀 |
| manifest 格式错误或自定义路径错误 | 运行 `claude plugin validate <path>`；标准目录插件可不带 manifest |
| 文件权限问题 | 确认文件可读：`chmod 644 commands/*.md` |

### 6.3 Skills不生效

**排查**：

```bash
# 确认SKILL.md存在且格式正确
cat /path/to/plugin/skills/my-skill/SKILL.md

# 确认frontmatter格式
# frontmatter 用 --- 包围；name 和 description 是推荐字段
# name 缺省时使用目录名，description 缺省时回退到正文首段
```

### 6.4 多Plugin冲突

如果多个Plugin定义了同名命令：

```bash
# 不同插件的 skills / commands 通常用各自的插件命名空间区分
claude --plugin-dir ./plugin-a --plugin-dir ./plugin-b
# 分别用 /plugin-a:review、/plugin-b:review 调用，别靠加载顺序解决撞名
# 若两个插件用了相同 manifest name，先改成不同名字并检查 /plugin 的 Errors
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

Skill 和 command 会影响 Claude 的指令与工具选择；插件还可能包含 hooks、MCP 服务器或可执行文件，这些代码会以你的用户权限运行。Claude 的工具权限和 OS sandbox 是不同层面的控制，不能保证整个插件都被沙箱隔离。安装前检查来源和实际执行内容，再按需要配置权限、沙箱与组织策略。

### Q4：如何更新Plugin？

市场安装的插件，优先用 `/plugin` 的更新入口，或在终端运行：

```bash
claude plugin update my-plugin@my-marketplace
```

自行克隆并用 `--plugin-dir` 加载的开发目录才用 `git pull`。更新后检查当前会话是否需要 `/reload-plugins` 或重启。

### Q5：如何卸载Plugin？

市场安装的插件，用 `/plugin` 的卸载入口，或在终端运行：

```bash
claude plugin uninstall my-plugin@my-marketplace
```

如果你用了 project / local 作用域，先用 `claude plugin uninstall --help` 确认 `--scope`，避免只卸掉用户级副本。通过 `--plugin-dir` 临时加载的插件，下一次启动不再传这个目录即可；确认不需要开发文件后再自行删除。

### Q6：可以同时加载多少个Plugin？

当前文档没有给出统一的插件数量上限，也没有“最多5个”的通用建议。开销取决于各插件的常驻指令、工具、Hook 和服务；用 `claude plugin details <name>@<marketplace>` 看组件和预估上下文成本，再禁用本次任务不需要的插件。

### Q7：Plugin开发需要懂编程吗？

不一定。最简单的Plugin只需要写Markdown文件（Commands和Skills都是Markdown）。只有需要Hooks（自动化脚本）时才需要编程能力。

### Q8：Plugin可以离线使用吗？

已经下载的插件文件通常可以从本地加载，但 Claude Code 调用模型仍需要网络；插件里的远程 MCP、安装依赖和更新也可能联网。只能说本地资源加载与是否联网调用服务是两回事，不能把插件加载成功当成整套工作流可离线运行。

### Q9：如何让Plugin在所有项目中生效？

市场插件在 user 作用域安装即可对所有项目生效：

```bash
claude plugin install my-plugin@my-marketplace --scope user
```

先注册对应市场，并替换为实际条目。`--plugin-dir /path/to/my-plugin` 适用于开发目录的单次加载；不要为了全局生效把 `claude` 命令本身替换为带固定路径的别名。

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
| **停止加载开发目录** | 下一次启动不传该目录的 `--plugin-dir` 参数 |
| **查看Plugin信息** | `cat .claude/plugins/<name>/.claude-plugin/plugin.json` |
| **开发时重载** | 会话中 `/reload-plugins`；按当前提示处理，必要时重启 |
| **调试Plugin** | `claude --plugin-dir <path> --debug` |

### Plugin目录结构速查

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # 可选但推荐：元数据清单
├── .mcp.json            # 可选：MCP配置
├── README.md            # 推荐：文档
├── commands/*.md        # 可选：Slash命令
├── skills/*/SKILL.md    # 可选：Agent能力
├── agents/*.md          # 可选：Agent定义
└── hooks/
    ├── hooks.json      # 可选：Hook事件配置
    └── *.py            # 可选：由配置调用的脚本
```

> 💡 **命名空间**：Plugin中的Skills会自动添加命名空间前缀，格式为 `/plugin-name:skill-name`，避免与其他Plugin冲突。

---

> **最后更新**：2026年9月14日 | **适用版本**：Claude Code v2.1.270
