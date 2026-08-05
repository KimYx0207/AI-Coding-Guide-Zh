# CX-01 Codex App 安装与认证完整指南：Windows / macOS 从下载到第一个线程

本篇只解决一件事：把 **Codex App** 正确装好、登上号、打开本地项目，并跑通第一个安全任务。

官方来源：OpenAI Codex App 文档、Codex changelog、[Codex App Windows](https://developers.openai.com/codex/app/windows)、[Codex Quickstart](https://developers.openai.com/codex/quickstart)、Codex CLI 文档。本篇按 2026-06-18 可查官方文档、Codex App 26.609 与 Codex CLI 0.141.0 修订；CLI 只用于辅助安装、自动化和排查，入口、包名和版本会变化，以官方页面和当前 App 为准。

---

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时
> - **难度等级**：⭐ 零基础入门
> - **更新日期**：2026年5月31日
> - **信息来源**：[Codex App Windows](https://developers.openai.com/codex/app/windows) | [Codex Quickstart](https://developers.openai.com/codex/quickstart) | Codex changelog | Codex CLI 文档（辅助）
> - **前置要求**：无（本系列第一篇）

---

## 📚 本课学习目标

完成本课学习后，你将能够：

1. **理解Codex App的定位**：掌握Codex App与CLI的本质区别，知道App是主线、CLI是辅助
2. **准备系统环境**：确认Windows/macOS系统要求和必备开发工具（Git、Node.js等）
3. **完成Codex App安装**：掌握Microsoft Store（Windows）和官方下载（macOS）两条安装路径
4. **处理首次启动问题**：独立解决防火墙弹窗、Gatekeeper拦截、PowerShell执行策略等常见问题
5. **完成账号登录**：正确使用ChatGPT/OpenAI账号登录Codex App
6. **创建第一个线程**：在App中添加本地项目并创建Local thread
7. **跑通只读和可写任务**：完成第一个只读分析任务和第一个安全可写任务，确认Review面板可用
8. **了解CLI的辅助角色**：知道CLI不是主线，但可用于排查配置和CI场景

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：这是一篇长教程，不用全看！根据你的目标选择路径。

### 路径A：快速上手（⏱️ 30分钟）

**适合人群**：急着装好Codex App，想快速跑起来

**只看这些章节**（其他跳过）：

```
✅ 第0部分：安装目标说清（3分钟）
✅ 第1部分：系统要求（5分钟）
✅ 第2-3部分：安装 + 首次启动（15分钟）
✅ 第9-10部分：第一个只读/可写任务（7分钟）
```

**30分钟后你能达到**：Codex App装好、登上网、跑通第一个只读任务

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想深入理解每个安装细节，掌握所有平台的安装方法

**学习顺序**：从头到尾所有章节

**建议分段学习**：
- 第1阶段（1小时）：第0-3部分（目标+系统要求+安装+首次启动）
- 第2阶段（1小时）：第4-8部分（防火墙+agent+开发工具+PowerShell+macOS）
- 第3阶段（30分钟）：第9-13部分（项目+可写任务+CLI+检查清单+FAQ）

---

### 路径C：问题排查（⏱️ 10分钟）

**适合人群**：安装过程遇到问题，需要快速解决

**直接跳到这些章节**：

```
🔧 第4部分：Windows防火墙弹窗
🔧 第7部分：PowerShell执行策略
🔧 第8.5部分：macOS常见问题
🔧 第13部分：常见问题FAQ
```

---

## 术语表（小白必读）

安装篇不只是“下载软件”。你要先知道自己正在安装哪一层能力。

| 术语 | 一句话解释 | 安装时要注意 |
|---|---|---|
| Codex App | 桌面应用，是本系列主线 | Windows / macOS 按官方入口安装 |
| Local thread | 在本机项目上开的任务线 | 需要本地目录权限和 Git |
| Agent | Codex 执行读文件、写文件、跑命令的执行单元 | 受 sandbox 和 approval 约束 |
| Sandbox | 限制 agent 能访问什么的安全边界 | 不建议默认 full access |
| Review pane | 安装后验证改动可见性的关键面板 | Git 仓库里才最有价值 |
| CLI | 终端辅助工具 | 不是安装课主线，排查和 CI 时再学 |
| WSL2 | Windows 上的 Linux 子系统 | Linux 工具链项目可用，新手不优先 |
| Gatekeeper | macOS 的应用安全校验 | 只信任官方安装包 |
| Windows Firewall | Windows 网络访问提示 | 一般只放行专用网络 |

## 安装课的心智模型

你不是在安装一个"聊天软件"，而是在本机建立一条开发执行链路：

```text
App 能打开
  -> 账号能登录
  -> 本地项目能添加
  -> Git 状态能识别
  -> Agent 能只读分析
  -> Agent 能小范围写文件
  -> Review 能看到 diff
```

前面任何一环没通，后面的高级功能都会变得不稳定。例如 Git 没装，Review 体验会缺关键证据；项目目录权限没给，Codex 读不到文件；一开始就开管理员或 full access，短期省事，长期风险很大。

### 新手安装顺序

1. **先装 App**：Windows 走 Microsoft Store，macOS 走官方入口。
2. **再装 Git**：没有 Git，Review 和 PR 工作流都会受影响。
3. **按项目装工具链**：Node、Python、.NET、Xcode 不是所有人都要全装。
4. **先只读测试**：让 Codex 总结项目，不修改文件。
5. **再小范围写入**：只改 README 一个错别字，确认 Review 面板。
6. **最后再考虑 CLI**：CLI 用于排查、CI、远程和自动化，不抢 App 主线。

### 安装失败的判断路径

| 症状 | 先看哪里 | 常见原因 |
|---|---|---|
| App 装不上 | 官方来源、系统版本、企业策略 | Store / MDM 限制 |
| App 打不开 | 系统安全提示、安装包来源 | Gatekeeper、下载损坏 |
| 登不上账号 | 网络、账号权限、组织策略 | 账号不匹配或网络限制 |
| 打不开项目 | 目录权限、路径、Git 仓库 | macOS 权限或 Windows 路径 |
| Git 不可用 | `git --version`、Command Line Tools | Git 未装或 PATH 未刷新 |
| 命令不可用 | 项目工具链、PATH、终端设置 | Node / Python / Xcode 未装 |
| Review 没 diff | 项目不是 Git 仓库或没改动 | 先 `git status` |

## 0. Critical：先把安装目标说清楚

老金我把 Codex 第一课放在 App 安装和认证，是因为这条主线先解决“能不能安全打开本地项目”。

本系列不是从 CLI 开始，而是从 App 开始。你安装成功的标准不是"终端里有 codex 命令"，而是：

1. 桌面 Codex App 能打开。
2. 能登录 ChatGPT / OpenAI 账号。
3. 能添加本地项目。
4. 能创建一个线程。
5. 能让 Codex 只读分析项目。
6. 能看到 Review / diff / Settings 等 App 能力。

CLI、Web / Cloud、SDK 都是后续辅助。

## 1. 系统要求和推荐准备

### 1.1 Windows

官方 Windows 页说明：Codex App for Windows 通过 **Microsoft Store** 下载，支持 Windows 原生 sandbox 和 PowerShell，也可以配置到 WSL2。

建议准备：

| 项目 | 建议 |
|---|---|
| Windows 版本 | Windows 11 是推荐基线；近期且 fully updated 的 Windows 10 属于 best effort，实操上至少需要 Windows 10 1809+ 的现代终端能力 |
| 安装来源 | Microsoft Store，或 `winget install Codex -s msstore` |
| 终端 | PowerShell 默认可用；也可在 App 设置里选 Command Prompt、Git Bash、WSL |
| 项目位置 | 新手优先放在 Windows 文件系统，例如 `C:\Users\<你>\Projects\repo` |
| Git | 必装，Review 面板和 diff 依赖 Git |
| Node / Python | 按项目需要安装 |
| 防火墙 | 首次启动或本地 agent 通信时可能弹出 Windows 防火墙提示，见第 4 节 |

### 1.2 macOS

macOS 用户同样是一等主线，不是补充路径。安装后也要跑通登录、本地项目、只读线程和 Review。

建议准备：

| 项目 | 建议 |
|---|---|
| macOS 版本 | 使用仍受 Apple 支持的 macOS 版本 |
| 芯片 | Apple Silicon / Intel 都先以官方下载页提供的包为准 |
| 安装来源 | 官方 Codex App 页面，不要从第三方网盘下载 |
| 终端 | 系统 Terminal / zsh 默认可用；项目也可能用 iTerm2、Homebrew 工具链 |
| 项目位置 | 新手优先放在用户目录，例如 `~/Projects/repo` |
| Git | 必装，Review 面板和 diff 依赖 Git |
| Node / Python / Xcode | 按项目需要安装 |
| 系统权限 | 首次打开项目、访问目录、运行终端或控制本机应用时，按最小权限授权 |

### 1.3 Linux

如果当前官方 App 没覆盖你的 Linux 桌面环境，Linux 用户先用 CLI / Web / Cloud。不要把 Windows / macOS App 步骤硬套到 Linux。

## 2. Windows 安装：Microsoft Store 是主路径


### 2.1 图形界面安装

1. 打开官方 Codex App 页面：[https://developers.openai.com/codex/app/windows](https://developers.openai.com/codex/app/windows)
2. 点击页面里的 **Codex app for Windows / Microsoft Store** 链接。
3. 在 Microsoft Store 中点击获取 / 安装。
4. 安装完成后，从开始菜单搜索 `Codex` 并打开。

注意：

- 当前 Windows 官方主路径就是 Microsoft Store。
- 不要从不明网盘、第三方安装包或“解包版”安装。
- 企业电脑如果禁用了 Microsoft Store，需要让管理员通过企业管理工具分发，或使用第 2.2 节的 `winget` 路径。

### 2.2 命令行安装

如果你不想打开 Store 界面，或者企业环境允许 `winget`：

```powershell
winget install Codex -s msstore
```

这仍然是从 Microsoft Store 源安装，不是独立安装包。

### 2.3 更新 Codex App

官方 Windows 页给出的更新方式是：

1. 打开 Microsoft Store。
2. 进入 Downloads / 下载。
3. 点击 Check for updates / 获取更新。
4. 等 Store 安装最新版本。

如果 App 提示版本过旧，也先去 Microsoft Store 更新。

## 3. Windows 首次启动

### 3.1 打开 App

从开始菜单启动：

```text
开始菜单 → 搜索 Codex → 打开
```

如果需要管理员权限运行某些命令，官方 Windows 页说明可以从开始菜单右键 Codex，选择 **Run as administrator**。新手不建议默认管理员运行，只有任务确实需要时再用。

### 3.2 登录

App 打开后按界面提示登录。通常优先使用 ChatGPT / OpenAI 账号。

如果你做 CI、SDK 或服务端自动化，才考虑 API Key。不要把 API Key 写入教程、截图、`AGENTS.md` 或仓库配置。

### 3.3 第一次看到权限提示

首次使用时，Codex 可能要求访问本地项目、运行命令或使用终端。你要区分：

- 选择项目目录：正常。
- 运行只读命令：通常低风险。
- 写文件、安装依赖、删除文件、联网：需要看清楚再同意。

## 4. Windows 防火墙弹窗怎么处理

这个点安装篇必须写清楚。

在 Windows 上，Codex App、集成终端、本地 agent、浏览器/本地服务协作时，系统可能弹出 **Windows Defender Firewall** 提示，询问是否允许 Codex 或相关进程通信。

建议：

| 选项 | 建议 |
|---|---|
| Private networks / 专用网络 | 个人电脑、本地开发网络下通常允许 |
| Public networks / 公用网络 | 一般不要勾选，除非你明确知道需要 |
| 企业电脑 | 按公司安全策略处理，必要时找管理员放行 |

为什么会弹：

- App 或 agent 可能需要和本地进程通信。
- 本地开发服务器、浏览器预览、MCP server、App server 类能力可能使用 localhost 端口。
- Windows 防火墙会把这类监听或连接行为拦出来让你确认。

怎么判断是否正常：

- 弹窗来源应是 Codex、OpenAI、终端、Node/Python/项目本地服务等你当前正在启动的程序。
- 如果你只是打开 Codex App 并添加本地项目，允许专用网络通常能避免本地连接失败。
- 如果弹窗来源可疑，不要允许，先取消并检查进程。

如果不小心点了取消：

1. 打开 Windows 安全中心。
2. 进入防火墙和网络保护。
3. 找到“允许应用通过防火墙”。
4. 找到 Codex 或相关本地服务。
5. 只勾选专用网络。

官方 Windows 文档没有把防火墙弹窗列成安装前提；这是 Windows 本地 agent / 本地服务常见实操问题，所以本教程把它作为首次启动排障项。

## 5. Windows 原生 agent、PowerShell 和 WSL2


官方 Windows 页说明：

- 默认是 Windows 原生 agent。
- Windows 原生 agent 在 PowerShell 中运行命令。
- App 支持 Windows sandbox。
- 也可以配置让 agent 在 WSL2 中运行。

新手建议：

| 项目位置 | 推荐 |
|---|---|
| 普通 Windows 项目 | 使用 Windows 原生 agent + PowerShell |
| 项目在 WSL 文件系统 | 可以通过 `\\wsl$\` 添加，但新手不优先 |
| 长期 Linux 工具链项目 | 考虑切到 WSL2 agent，并重启 App |

官方建议如果继续使用 Windows 原生 agent，项目优先放在 Windows 文件系统；如果要给 WSL 访问，可从 WSL 里通过 `/mnt/c/...` 访问。

## 6. Windows 必备开发工具

官方 Windows 页列了几类常用工具：Git、Node.js、Python、.NET SDK、GitHub CLI。不是每个项目都全需要，但 Git 强烈建议安装。

常用安装命令：

```powershell
winget install --id Git.Git
winget install --id OpenJS.NodeJS.LTS
winget install --id Python.Python.3.14
winget install --id GitHub.cli
```

如果做 .NET / Windows 原生应用：

```powershell
winget install --id Microsoft.DotNet.SDK.10
```

安装后重新打开 Codex App，让新 PATH 生效。

## 7. PowerShell 执行策略问题

Windows 新机器可能遇到：

```text
npm.ps1 cannot be loaded because running scripts is disabled on this system.
```

这是 PowerShell execution policy 问题，不是 Codex 特有问题。

常见修复：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

改执行策略前要理解影响；企业电脑按管理员策略处理。

## 8. macOS 安装：官方入口、系统权限和开发工具链

> **2026-06-09 安装口径**：Codex App 主线按官方 App 入口、Microsoft Store / macOS 下载页与 App 内更新为准。CLI 安装只作为自动化、CI 和排查补充；官方 changelog 已确认 `install.sh` / `install.ps1` 支持 `CODEX_NON_INTERACTIVE=1` 非交互安装。App 登录适合桌面工作流，API key / CLI 路径适合自动化、CI 和排查。

### 8.1 从哪里下载

macOS 用户从官方 Codex App 页面进入下载：

1. 打开官方 Codex App 页面：[https://developers.openai.com/codex/app/](https://developers.openai.com/codex/app/)
2. 选择 macOS 下载入口。
3. 按页面提示下载适合当前 Mac 的安装包。
4. 打开安装包，把 Codex App 安装到 Applications / 应用程序。
5. 从 Launchpad 或 Applications 打开 Codex。

注意：

- 如果页面区分 Apple Silicon 和 Intel，按你的芯片选择；不确定时看“关于本机”。
- 不要从第三方网盘、论坛附件或别人转发的安装包安装。
- 如果公司 Mac 有 MDM / 安全软件限制，按公司软件分发流程安装。

### 8.2 第一次打开和 Gatekeeper

macOS 可能出现 Gatekeeper 或系统安全提示。处理原则：

| 提示 | 建议 |
|---|---|
| “无法打开，因为无法验证开发者” | 先确认来源是官方页面；再到系统设置的隐私与安全里按提示允许 |
| 请求访问项目目录 | 只授权当前项目或你明确需要的目录 |
| 请求访问桌面、文稿、下载 | 不要全给；项目在哪里就给哪里 |
| 请求控制其他应用 | 只有任务确实需要本机自动化或浏览器验证时再授权 |

如果 App 打不开，不要立刻改系统全局安全设置。先确认安装包来源、重新下载、检查系统设置中的拦截提示。

### 8.3 macOS 登录与首次线程

安装后检查：

1. App 能打开。
2. 能登录账号。
3. 能选择本地项目目录。
4. 能创建线程。
5. 能看到 Review / Settings。

登录建议和 Windows 一样：普通 App 使用优先走 ChatGPT / OpenAI 账号；API Key 只用于 CLI、CI、SDK 或服务端自动化，不写进仓库。

### 8.4 macOS 必备开发工具

macOS 项目常见准备：

```bash
git --version
xcode-select --install
```

如果项目使用 Homebrew：

```bash
brew --version
```

Node / Python 按项目选择，不要所有教程都强制安装：

```bash
node --version
python3 --version
```

常见判断：

| 项目类型 | 建议工具 |
|---|---|
| Web / Node 项目 | Node.js、包管理器、Git |
| Python 项目 | Python 3、虚拟环境工具、Git |
| iOS / macOS 原生项目 | Xcode、Command Line Tools、Git |
| 需要本地浏览器验证 | Chrome / Safari，以及项目要求的浏览器工具 |

### 8.5 macOS 常见问题

| 问题 | 处理 |
|---|---|
| App 看不到项目文件 | 检查目录权限，重新选择项目目录 |
| Git 状态不可用 | 安装 Command Line Tools，确认项目是 Git 仓库 |
| `xcrun` / `git` 不可用 | 运行 `xcode-select --install` |
| Node 命令不可用 | 安装 Node，并重新打开 App 让 PATH 生效 |
| 权限给多了 | 到系统设置的隐私与安全里撤销不必要权限 |

## 9. 第一次打开项目

推荐用一个普通 Git 仓库测试，不要一上来打开生产仓库。

步骤：

1. 打开 Codex App。
2. 添加本地项目目录。
3. 确认 App 能识别 Git 状态。
4. 创建 Local thread。
5. 先发只读任务：

```text
阅读这个项目，告诉我它的技术栈、启动命令、测试命令，以及你建议写进 AGENTS.md 的内容。不要修改文件。
```

如果它开始尝试改文件，停下并重新强调只读。

## 10. 第一个安全可写任务


确认只读正常后，做一个低风险改动：

```text
修正文档中的一个错别字。改完后展示 diff，不要自动提交。
```

你要确认：

- Review 面板能看到 diff。
- 改动只在预期文件里。
- Codex 没有自动提交。
- 你知道怎么撤销或继续修改。

## 11. CLI 只作为辅助安装

App 用户不需要先学 CLI。但建议装 CLI 用于排查：

```bash
codex --help
codex app
codex review
codex exec "summarize this repo"
```

CLI 安装和深入使用放到 CX-12。安装篇只要求你知道它不是主线。

## 12. 安装后检查清单

| 检查项 | 你应该看到 |
|---|---|
| App 安装 | Windows 从 Microsoft Store / `winget -s msstore` 安装，macOS 从官方 App 入口安装 |
| 登录 | App 显示已登录账号 |
| 防火墙 | Windows 弹窗已按专用网络最小放行处理 |
| macOS 权限 | 只授权必要项目目录和必要系统能力 |
| Git | App 能看到项目 Git 状态 |
| 项目 | 能添加本地仓库 |
| 线程 | 能创建 Local thread |
| 只读 | 能总结项目，不改文件 |
| 可写 | 小改动能在 Review 中看到 diff |
| 安全 | 没有默认开 full access |

## 13. 课堂工坊：从安装到第一个线程

这一节建议你拿一台日常开发机器跟练，不要用生产仓库做第一次实验。

### 案例一：Windows 从 Store 到 Local thread

目标：确认 Windows 上的 App、登录、Git、Review 都能跑通。

1. 用 Microsoft Store 安装 Codex，或在 PowerShell 里运行：

```powershell
winget install Codex -s msstore
```

2. 启动 Codex，登录 ChatGPT / OpenAI 账号。
3. 如果弹出 Windows 防火墙提示，只在你信任的专用网络里放行。
4. 打开一个测试 Git 仓库，创建 Local thread。
5. 发送只读提示：

```text
阅读这个项目，只输出技术栈、启动命令、测试命令和主要目录。不要修改文件，不要安装依赖。
```

你应该看到：Codex 能读项目并说明命令来源；Review 面板没有新增 diff。

### 案例二：macOS 从官方包到第一个安全改动

目标：确认 macOS 权限、Git 和 Review 可用。

1. 从官方 Codex App 页面下载安装包。
2. 如果 Gatekeeper 拦截，先确认安装包来源，再到系统设置的隐私与安全里按提示允许。
3. 只授权当前项目目录，不要一次性授权桌面、文稿、下载等所有位置。
4. 打开测试仓库，发送一个小范围写入任务：

```text
修正 README.md 里一处明显错别字。只改 README.md，改完展示 diff 摘要，不要提交。
```

你应该看到：Review 面板只出现 README.md；Codex 没有运行提交、推送或安装依赖。

### 案例三：CLI 只做排查，不抢 App 主线

目标：知道 CLI 能帮你定位问题，但不把它当安装课主角。

```bash
codex --help
codex review
codex exec "Read this repo and report the test command. Do not modify files."
```

如果 `codex` 不存在，不影响 App 主线学习；先确认 App 能登录、能打开项目、能创建线程。CLI 安装和 CI 用法放到 CX-12。

## 14. 常见问题

### Q1：Windows 一定要 Microsoft Store 吗？

当前官方 Windows 页写的是从 Microsoft Store 下载；命令行路径也是 `winget install Codex -s msstore`。如果公司禁用 Store，让管理员通过企业管理工具分发。

### Q2：启动时防火墙必须允许吗？

如果你要使用本地项目、agent、本地服务或 localhost 相关能力，通常需要允许专用网络。不要随便允许公用网络。官方没有把它写成安装硬条件，但实操中遇到弹窗要处理。

### Q3：PowerShell 和 WSL2 选哪个？

新手用默认 Windows 原生 agent + PowerShell。项目强依赖 Linux 工具链时再切 WSL2。

### Q4：为什么 App 里 Git 功能不可用？

通常是没有安装 Git，或项目不在 Git 仓库里。先安装 Git 并重新打开 App。

### Q5：能不能默认管理员运行？

不建议。只有明确需要管理员权限的任务才右键 Run as administrator。

### Q6：macOS 和 Windows 哪个是主线？

都是主线。Windows 要写清 Microsoft Store、PowerShell、防火墙；macOS 要写清官方下载、Gatekeeper、目录权限、Command Line Tools。CLI / Web / Cloud 才是辅助线。

---

## 15. 安装排障总表：按症状定位，不要乱重装

安装课最怕学生遇到问题后反复卸载重装。Codex App 的安装问题通常不是"软件坏了"，而是系统、账号、Git、终端、权限或项目目录其中一环没对齐。排障时先定位症状，再选择动作。

| 症状 | 常见原因 | 第一反应 |
|------|----------|----------|
| App 装不上 | Store、系统版本、企业策略限制 | 先确认安装来源和系统更新 |
| App 能打开但登录失败 | 浏览器登录态、网络、账号权限 | 先换浏览器登录或重新授权 |
| 项目加不进去 | 目录权限、路径过深、云盘同步冲突 | 先换一个简单本地 Git 仓库 |
| Review 面板不可用 | 没有 Git 或不是 Git 仓库 | 安装 Git，确认 `git status` |
| 终端命令跑不动 | PowerShell policy、Node/Python 缺失 | 先在集成终端跑版本命令 |
| Windows 防火墙弹窗 | 本地服务或开发服务器通信 | 只放行可信网络 |
| WSL 项目状态异常 | Windows 原生 agent 和 WSL 文件系统混用 | 优先把项目放 Windows 本机盘 |
| macOS 打不开 | Gatekeeper 或下载来源 | 从官方入口下载并按系统提示授权 |

### 15.1 Windows 安装失败排障

先做只读检查：

```powershell
winget --version
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsHardwareAbstractionLayer
where.exe git
where.exe node
where.exe python
```

如果 `winget` 不可用，不要急着换第三方下载站。先从 Microsoft Store 图形界面安装。企业电脑如果禁用了 Store，需要找 IT 确认 Microsoft Store app distribution 或企业管理工具是否允许安装 Codex。

### 15.2 Windows 路径排障

路径问题经常伪装成 Codex 问题。课堂里建议准备一个干净测试仓库：

```powershell
mkdir C:\code\codex-smoke
cd C:\code\codex-smoke
git init
"# Codex Smoke" | Out-File README.md -Encoding utf8
git add README.md
git commit -m "init smoke project"
```

如果这个简单仓库能在 App 里正常打开，说明 Codex App 基本可用，问题大概率在原项目的路径、权限、Git 状态或工具链上。

### 15.3 PowerShell policy 排障

如果遇到第 7 节提过的 `npm.ps1 cannot be loaded...`，不要把它理解成 Codex App 安装失败。它是 PowerShell execution policy 问题，课堂处理顺序是：

```powershell
Get-ExecutionPolicy -List
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

不要为了省事把所有东西都切到管理员权限。管理员权限会扩大 Codex 能影响的系统范围。只有明确需要系统级安装或权限变更时，才临时用管理员启动。

### 15.4 macOS Gatekeeper 排障

macOS 新手遇到“无法打开”时，先确认来源：

```bash
uname -a
xcode-select -p
git --version
```

如果 Command Line Tools 缺失：

```bash
xcode-select --install
```

如果是系统权限提示，不要一次性授予全盘访问。先让 Codex 访问你的项目目录、终端需要的工具和必要开发目录。需要更多权限时，再根据任务逐项开放。

## 16. 账号、认证和组织权限

安装完成不等于可以完成所有任务。Codex 还要受账号、订阅、组织、连接器和项目权限影响。

### 16.1 登录失败的三层判断

| 层级 | 问题 | 处理方式 |
|------|------|----------|
| 浏览器层 | 默认浏览器登录态混乱 | 退出重登，换浏览器完成授权 |
| 账号层 | 登录了错误账号 | 确认 ChatGPT / OpenAI 账号 |
| 组织层 | 企业策略限制功能 | 查看 workspace 管理策略或问管理员 |

### 16.2 不要把 API Key 当 App 登录方案

App 学习主线是使用 Codex App 登录与桌面工作流。API Key 更常见于 CLI 自动化、CI 或 `codex exec` 场景。新手不要一遇到 App 登录问题就把密钥贴进聊天框或配置文件。

错误做法：

```text
这是我的 API key：sk-...
帮我配置一下 Codex。
```

正确做法：

```text
我在 Codex App 登录时遇到认证问题。
请先帮我区分是浏览器登录态、账号选择、网络访问还是企业策略问题。
不要让我粘贴任何密钥。
```

## 17. 第一个项目应该怎么选

学习 Codex App 时，第一项目不要选最大、最乱、最重要的生产仓库。应该选一个低风险但真实的 Git 项目。

### 17.1 好的第一项目

| 项目特征 | 为什么适合 |
|----------|------------|
| 是 Git 仓库 | Review 面板可用 |
| 有 README | Codex 能快速理解项目 |
| 有简单测试命令 | 能练验证闭环 |
| 文件数量适中 | 不会一开始就迷路 |
| 没有敏感密钥 | 降低误读风险 |

### 17.2 不适合第一项目

| 项目 | 原因 |
|------|------|
| 公司核心生产仓库 | 心理压力大，权限复杂 |
| 没有 Git 的文件夹 | Review 体验不完整 |
| 桌面同步盘里的半成品 | 容易遇到文件锁和同步冲突 |
| 巨型 monorepo | 新手难判断上下文边界 |
| 带真实客户数据的目录 | 不适合练习 |

### 17.3 第一项目 prompt

```text
这是我第一次用 Codex App 打开这个项目。
请先只读分析，不要修改文件。
请告诉我：
1. 这个项目的主要语言和框架
2. 常见开发命令可能在哪里
3. 哪些文件适合作为入门阅读
4. 如果我要做一个安全小改动，应该从哪里开始
```

这个 prompt 的重点是建立安全感。第一次不要直接让 Codex 改代码。

## 18. 安装后的第一周训练计划

Claude Code 的厚课程强在“学完能做事”。Codex App 安装课也要给学习者一周路径。

### 第 1 天：只读认识项目

```text
请只读分析当前项目。
不要修改文件，不要运行写入命令。
输出：
- 项目结构
- 开发命令候选
- 测试命令候选
- 我应该先读的 5 个文件
```

学习目标：知道 Codex 能读项目，但不会默认改。

### 第 2 天：让 Codex 解释终端输出

```text
我会在集成终端运行项目测试。
请读取终端输出，帮我解释失败原因。
不要修改文件。
```

学习目标：理解 App 的集成终端和线程协作。

### 第 3 天：做一个文档小改

```text
请修改 README 中的安装说明，使它和 package.json 里的脚本一致。
只改 README。
完成后告诉我 Review 面板里应该看哪几行。
```

学习目标：看到第一个小 diff。

### 第 4 天：用 Review 面板留言

```text
请根据我在 Review 面板里的 inline comments 修改刚才的 README 改动。
保持范围不变。
```

学习目标：体验 line-specific feedback。

### 第 5 天：写第一份 `AGENTS.md`

```text
请根据这个项目生成一份最小 `AGENTS.md` 草稿。
先给我内容预览，不要直接写入。
内容包括：
- 项目简介
- 常用命令
- 修改边界
- 安全注意事项
```

学习目标：从 App 使用进入项目指令。

### 第 6 天：开一个 worktree 线程

```text
请帮我判断这个任务是否适合开 worktree：
我想尝试重写 README 的快速开始部分，但不想影响当前工作区。
先解释选择理由，不要直接改文件。
```

学习目标：理解 local 和 worktree 的差异。

### 第 7 天：复盘安装和工作流

```text
请根据这一周的使用，帮我复盘：
1. Codex App 已经能稳定完成哪些任务
2. 哪些问题来自项目配置
3. 哪些问题来自系统工具链
4. 下一周我应该学习 Commands、MCP、Skills 还是 Review
```

学习目标：从安装成功走向稳定使用。

## 19. 企业安装：让 IT、工程和安全说同一种语言

企业里安装 Codex App 不是个人下载这么简单。课程应该让不同角色都知道自己负责哪一段。

### 19.1 IT 负责人关心什么

```text
- Windows 是否通过 Microsoft Store 或企业分发安装。
- macOS 是否通过官方来源安装。
- 是否需要代理、证书或网络策略。
- 是否需要统一安装 Git、Node.js、Python、GitHub CLI。
- 是否有软件更新策略。
```

### 19.2 工程负责人关心什么

```text
- 项目是否都有 Git。
- README 和 AGENTS.md 是否能让 Codex 找到命令。
- 测试命令是否能在本机跑通。
- 是否需要 monorepo 局部说明。
- 是否建议默认使用 worktree。
```

### 19.3 安全负责人关心什么

```text
- 默认权限是否足够窄。
- 是否禁止把密钥粘贴进线程。
- 是否需要 Rules、Hooks 或受管配置。
- 插件、MCP、Automation 是否有登记流程。
- full access 是否只在受控场景使用。
```

### 19.4 新人安装交接卡

```md
# Codex App Onboarding Card

## Installed

- Codex App
- Git
- Node.js or project runtime
- Python if project needs it
- GitHub CLI if PR context is needed

## First Project

- Open a small Git repository first.
- Run a read-only project summary.
- Do one README-only change.
- Inspect the diff in Review.

## Safety

- Do not paste secrets.
- Do not start with full access.
- Do not use production data as practice material.
```

## 20. 安装课里的常见心理误区

安装不是纯技术问题。新手卡住时，常见心理误区也会影响学习。

| 误区 | 真实情况 | 建议 |
|------|----------|------|
| 装不上就是我不适合 | 通常是系统或权限问题 | 按症状排障 |
| App 打开就应该能做所有事 | 还受 Git、工具链、账号影响 | 分层检查 |
| 权限越大越省事 | 权限越大风险越高 | 默认窄权限 |
| 第一次就要改大项目 | 大项目会放大不确定性 | 先用练习仓库 |
| CLI 更专业，所以先学 CLI | App 是本课程主线 | CLI 放到辅助课 |

这部分看似“不技术”，但能显著降低新手放弃率。

## 21. 大型综合工坊：从一台新电脑到可交付的 Codex 工作台

这个工坊适合直播课最后 40 分钟，也适合企业新人入职当天完成。目标不是"把软件装上"，而是让学习者完成一条真实工作流：安装、登录、打开项目、只读分析、小改动、Review、复盘。

### 21.1 工坊准备

讲师提前准备：

```text
- 一个公开或低风险 Git 仓库。
- README 中有一处可以安全更新的说明。
- package.json 或 pyproject.toml 中有可读命令。
- 不包含真实密钥。
- 能在 Windows 和 macOS 上打开。
```

学习者准备：

```text
- Codex App。
- Git。
- 项目所需基础 runtime。
- 一个能登录 Codex 的账号。
- 20 分钟不被打断的时间。
```

### 21.2 第一步：确认系统工具链

Windows：

```powershell
git --version
node --version
python --version
gh --version
```

macOS：

```bash
git --version
node --version
python3 --version
gh --version
```

不要求每个项目都需要所有工具。这个步骤的目的，是让学习者知道“Codex 能力”和“本机工具链”不是同一件事。

### 21.3 第二步：打开项目并只读分析

Prompt：

```text
这是我第一次在 Codex App 中打开这个项目。
请只读分析，不要修改文件，不要运行会写入的命令。
请输出：
1. 项目用途
2. 主要目录
3. 常用命令候选
4. 我应该先读的文件
5. 这个项目里最适合新手练习的小改动
```

讲师讲解点：

```text
- 让 Codex 先读项目，比直接改更稳。
- “常用命令候选”不是最终事实，后面要用文件和终端确认。
- 小改动应该能在 Review 面板里清楚看到。
```

### 21.4 第三步：确认命令而不是盲跑

Prompt：

```text
请根据项目文件推断最可能的测试、lint 和启动命令。
先不要运行。
把每条命令旁边标出你从哪个文件看到的依据。
```

然后学习者手动在终端跑一条安全命令：

```bash
git status
```

再问：

```text
请解释当前终端里的 Git 状态。
如果工作区不干净，请告诉我哪些改动可能已经存在，不要修改文件。
```

这一步训练学习者把 Codex 回答和真实终端状态连起来。

### 21.5 第四步：做一个 README 小改

Prompt：

```text
请只修改 README 中的快速开始部分。
目标：让安装命令和 package.json 中的脚本一致。
边界：
- 不改代码
- 不改 lockfile
- 不改项目配置
- 不新增图片提示

完成后告诉我：
- 改了哪几处
- 为什么改
- Review 面板里应该重点看哪里
```

这个任务的好处是低风险，但包含完整的写入和 Review 流程。

### 21.6 第五步：Review 面板反馈

学习者在 Review 面板看 diff 后，用线程继续：

```text
请根据当前 Review diff 反向解释你的改动。
如果有任何改动超出了 README 快速开始范围，请指出。
不要继续修改。
```

如果需要修：

```text
请只修正 README 中我刚才指出的问题。
不要扩大范围。
```

### 21.7 第六步：写复盘卡

Prompt：

```text
请帮我生成本次 Codex App 入门复盘：
1. 我完成了哪些步骤
2. 哪些问题来自系统安装
3. 哪些问题来自项目配置
4. 哪些能力下一课要继续学
5. 本项目是否需要 AGENTS.md
```

这张复盘卡可以放进团队 onboarding 文档。

## 22. 安装课讲师手册：课堂节奏怎么排

### 22.1 90 分钟直播课结构

| 时间 | 内容 |
|------|------|
| 0-10 分钟 | 讲清 Codex App 主线和 CLI 辅助线 |
| 10-25 分钟 | Windows / macOS 安装差异 |
| 25-40 分钟 | 登录、项目打开、Git 工具链 |
| 40-55 分钟 | 第一次只读分析 |
| 55-70 分钟 | 第一个 README 小改 |
| 70-82 分钟 | Review 面板和终端复盘 |
| 82-90 分钟 | 常见问题和下一课 |

### 22.2 讲师不要跳过的解释

```text
- App 安装成功不等于项目工具链可用。
- 登录成功不等于外部 GitHub PR context 可用。
- Git 可用是 Review 面板体验的关键。
- Windows 原生、PowerShell、WSL 是三个不同层面。
- 不要让学生第一天使用高权限练习。
```

### 22.3 课堂提问设计

```text
问题 1：为什么第一次任务要只读？
问题 2：Review 面板依赖什么？
问题 3：PowerShell policy 报错时为什么不建议直接管理员运行？
问题 4：App 和 CLI 哪个是本课程主线？
问题 5：什么项目适合作为第一个练习项目？
```

这些问题会让学习者建立判断力，而不是只记步骤。

## 23. 安装课排障脚本库

### 23.1 Windows 基础诊断

```powershell
Write-Host "Windows"
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion

Write-Host "Git"
where.exe git
git --version

Write-Host "Node"
where.exe node
node --version

Write-Host "Python"
where.exe python
python --version

Write-Host "GitHub CLI"
where.exe gh
gh --version
```

### 23.2 macOS 基础诊断

```bash
echo "macOS"
sw_vers

echo "Git"
which git
git --version

echo "Xcode Command Line Tools"
xcode-select -p

echo "Node"
which node
node --version

echo "Python"
which python3
python3 --version
```

### 23.3 项目 Git 诊断

```bash
git rev-parse --show-toplevel
git status --short
git branch --show-current
git log --oneline -5
```

### 23.4 诊断输出分析 prompt

```text
下面是我的安装和项目诊断输出。
请帮我判断：
1. Codex App 本身是否可能安装正常
2. 项目 Review 面板是否具备条件
3. 哪个开发工具缺失会影响当前项目
4. 下一步最小修复动作是什么
不要建议我粘贴密钥或使用不可信下载源。
```

## 24. 安装课进阶常见问题

### Q1：为什么我能聊天，但 Codex 不能运行项目命令？

聊天能力来自 Codex；项目命令依赖本机工具链。比如 Node 项目需要 Node.js 和包管理器，Python 项目需要 Python 和依赖环境。先让 Codex 只读分析项目，再根据项目文件确认命令。

### Q2：为什么 Review 面板说项目不是 Git 仓库？

Review 面板基于 Git diff。你打开的目录如果不是 Git 仓库，或者打开了仓库外层/内层错误目录，Review 就无法按预期工作。用 `git rev-parse --show-toplevel` 确认项目根目录。

### Q3：Windows 上我应该把项目放在 `C:\code` 还是 `\\wsl$`？

如果你使用 Windows 原生 agent，优先把项目放在 Windows 本机盘，例如 `C:\code`。如果你的项目主要在 WSL 里开发，再考虑 WSL agent 和 WSL 文件系统。不要在不理解差异时混用。

### Q4：安装 GitHub CLI 是不是必需？

不是所有 Codex App 任务都需要 GitHub CLI。它主要帮助 GitHub PR context、评论和 GitHub 工作流。只做本地文档修改时，Git 本身更重要。

### Q5：为什么我不建议把生产仓库当练习项目？

新手阶段的目标是建立操作感。生产仓库往往有复杂权限、真实数据、敏感文件和发布风险。先用低风险仓库练会 App、Review、权限，再进入重要仓库。

### Q6：为什么课程强调“不要第一天高权限”？

因为学习阶段最常见的错误不是 Codex 不够努力，而是任务边界不清。高权限会让边界错误的后果变大。先用窄权限学会描述任务和检查 diff，后面再按需要扩大。

## 25. 安装可用状态：别只看 App 能不能打开

安装完成后，先用三种真实场景判断它是否进入可用状态。

### 25.1 个人练习可用

你能登录 App，打开一个低风险 Git 项目，创建 Local thread，让 Codex 做只读项目分析，再完成一个 README 小改，并在 Review 面板里看到 diff。到这里就可以进入下一课，不需要第一天就接 MCP、Plugin、Cloud 或 Automation。

### 25.2 团队试点可用

团队里至少有两个人能用同一套路径完成同一个练习：打开同一个项目，发送同一条只读 prompt，做同一个文档小改，看到相近的 Review diff。如果两个人表现差异很大，先查安装来源、项目路径、Git、终端和权限配置，不要急着上高级功能。

```text
请帮我们比较两台电脑上的 Codex App 试点结果。
关注：
1. 安装来源是否一致
2. 项目路径是否一致
3. Git 和终端工具链是否一致
4. App 权限和 sandbox 是否一致
5. 为什么同一条 prompt 得到不同执行结果
```

### 25.3 企业环境可用

企业环境里，除了个人可用，还要确认分发、更新、代理、证书、账号 workspace、默认权限和敏感数据边界。这里可以由 IT、安全、平台工程一起确认，但课程正文不需要把它写成固定角色表；关键是让学习者知道安装问题可能来自组织策略，而不是自己操作失败。

```text
请根据企业电脑的 Codex 安装现象，帮我区分：
- 软件分发限制
- 网络或代理限制
- 账号 workspace 限制
- 项目目录权限
- Git 或开发工具链缺失
```

## 26. 安装问题案例库：课堂现场怎么处理

### 案例一：App 能打开，但 Review 面板不可用

排查顺序：

```text
1. 当前目录是不是 Git 仓库。
2. Git 是否安装。
3. App 打开的是否是仓库根目录。
4. 工作区是否在云盘或受限目录。
5. 是否需要重新打开项目。
```

Prompt：

```text
请帮我只读排查 Codex App Review 面板不可用。
我会提供 `git status`、`git rev-parse --show-toplevel` 和项目路径。
不要修改文件。
```

### 案例二：Windows 中 npm 无法运行

排查顺序：

```text
1. `node --version`
2. `npm --version`
3. `Get-ExecutionPolicy -List`
4. 是否在 PowerShell、CMD、Git Bash 或 WSL 中运行
```

Prompt：

```text
我的 Windows 集成终端里 npm 命令失败。
请先根据终端输出判断是 Node 缺失、PATH 问题、PowerShell policy，还是项目依赖问题。
不要建议我直接切到管理员权限，除非确实需要。
```

### 案例三：macOS 打开项目后 Codex 不能写文件

排查顺序：

```text
1. 项目目录权限。
2. App 是否有必要的系统授权。
3. 项目是否在只读位置。
4. sandbox 是否是 read-only。
5. 任务 prompt 是否明确允许写入。
```

Prompt：

```text
Codex App 能读项目但不能写文件。
请帮我区分是 macOS 权限、Codex sandbox、项目目录权限还是任务边界问题。
先给排查步骤，不要直接修改配置。
```

### 案例四：登录了但看不到团队功能

排查顺序：

```text
1. 是否登录了正确账号。
2. 是否在正确 workspace。
3. 企业策略是否限制功能。
4. 是否需要重新授权 GitHub 或其它连接器。
5. App 是否需要更新。
```

Prompt：

```text
我已经登录 Codex App，但看不到预期的团队功能。
请帮我按账号、workspace、企业策略、连接器授权、App 版本五层排查。
不要让我粘贴任何 token。
```

## 27. 第一课作业：把安装经验变成团队文档

完成安装后，学习者应该产出一段可复用说明：

```md
# My Codex Setup Notes

## Machine

- OS:
- Shell:
- Project location:

## Installed Tools

- Git:
- Node:
- Python:
- GitHub CLI:

## First Project

- Project path:
- Git status:
- First read-only prompt:
- First safe edit:

## Issues Found

- ...

## Team Notes

- What should a new teammate do differently?
```

这份文档不需要华丽，它的价值是把个人踩坑变成团队资产。

## 28. 团队安装现场：20 个人一起装时怎么不乱

个人安装只要自己能跑就行。团队安装课的难点是：每个人的系统、账号、项目路径、shell、Git 状态都可能不同。如果没有节奏，课堂会变成一堆零散报错。

建议把现场分成四个检查点。

### 28.1 检查点一：账号和 workspace

先确认每个人登录的是正确账号，而不是先排查代码。

```text
请确认：
1. 你使用的是团队允许的 ChatGPT / OpenAI 账号。
2. App 里看到的是正确 workspace。
3. 如果团队使用 GitHub 或其他连接器，授权账号也一致。
4. 不要在聊天里粘贴 token、cookie 或个人密钥。
```

现场 prompt：

```text
我正在参加团队 Codex 安装课。
我已经登录 App，但不确定 workspace 是否正确。
请帮我列出不涉及 token 的自查步骤。
不要要求我粘贴任何凭据。
```

### 28.2 检查点二：项目路径和 Git 状态

很多安装问题其实是打开了错误项目。

```text
请确认：
1. 项目在团队推荐目录下。
2. 当前目录是 Git 仓库。
3. 没有未保存的重要本地改动。
4. 默认分支和练习分支区分清楚。
```

第一条只读 prompt：

```text
请只读检查当前项目。
输出：
1. 项目类型。
2. 主要语言和包管理器。
3. 可能的测试命令。
4. Git 状态是否适合做练习。

不要修改文件。
```

如果有人打开了生产仓库，不要让他继续练习写入任务。改用只读：

```text
这个仓库可能是生产项目。
本节课只做只读探索。
请不要修改文件，只总结项目结构和安全注意事项。
```

### 28.3 检查点三：第一条可写任务必须足够小

团队安装课第一条写入任务不要选真实 bug。选低风险文件，比如练习 README。

```text
请在 README 末尾添加一行本地安装练习记录。

要求：
1. 只修改 README。
2. 不改 package.json、源码或配置。
3. 修改后说明 diff。
4. 等我在 Review 面板确认。
```

如果有人失败，先让他贴错误摘要，不要贴密钥或全量日志：

```text
请根据这个错误摘要帮我判断是路径、权限、Git 状态还是 App 配置问题。
只给下一步排查，不要让我粘贴敏感信息。
```

### 28.4 检查点四：安装完成不等于可以自由写

最后要让每个人完成一份 setup note：

```md
# Team Codex Setup Result

## Account

- Workspace confirmed:
- GitHub connector needed:

## Project

- Path:
- Git branch:
- First read-only prompt:
- First safe edit:

## Local Notes

- Shell:
- Package manager:
- Any setup issue:

## Next Practice

- Review panel:
- AGENTS.md:
- PR workflow:
```

这份 note 比“我装好了”有用，因为它能让下一个同事少走一次弯路。

## 29. 安装课故障分流：别让所有人等一个问题

团队课堂里最怕一个人的环境问题拖住所有人。可以把故障分成三类。

```text
A 类：能继续上课
- App 已登录。
- 能打开项目。
- 只读 prompt 可用。
- 可写任务暂时失败。

B 类：需要旁路协助
- 登录或 workspace 有问题。
- GitHub 授权不对。
- 项目路径或权限不清楚。

C 类：先退出写入练习
- 生产仓库风险。
- 本机有敏感配置不清楚。
- 无法确认账号或组织权限。
```

对 A 类，不要卡住：

```text
你先继续只读练习和 Review 观察。
可写任务留到课后处理。
```

对 B 类，单独排查：

```text
请用账号、workspace、项目路径、Git 状态四项描述问题。
不要贴 token 或 cookie。
```

对 C 类，直接降级：

```text
本节课只做只读观察，不做写入。
先确认安全边界，再进入下一课。
```

这套分流能让课堂继续推进，也保护了那些环境暂时不适合写入的人。安装课的目标不是所有人同一分钟完成同一个动作，而是每个人离开时知道自己的环境处在哪个状态。

## 📝 总结与检查清单

完成本课后，请确认以下所有项：

**安装与登录：**

- [ ] Codex App 已安装（Windows从Microsoft Store / macOS从官方入口）
- [ ] 成功登录 ChatGPT / OpenAI 账号
- [ ] Windows防火墙已按最小放行处理（仅专用网络）
- [ ] macOS权限只授权了必要目录

**开发环境：**

- [ ] Git 已安装且App可见项目状态
- [ ] 必要的开发工具已安装（Node.js / Python等，按项目需要）
- [ ] PowerShell执行策略已正确设置（Windows）

**项目与任务：**

- [ ] 能添加本地Git仓库到App
- [ ] 能创建Local thread
- [ ] 完成第一个只读分析任务（Codex总结项目，未修改文件）
- [ ] 完成第一个安全可写任务（小改动在Review中看到diff）
- [ ] 没有默认开启 full access

**全部勾选后即完成 Codex App 安装。**

---

## 附录

### A. 安装路径速查

| 平台 | 安装方式 | 命令 |
|------|---------|------|
| Windows | Microsoft Store | `winget install Codex -s msstore` |
| macOS | 官方下载 | https://developers.openai.com/codex/app/ |
| Linux | CLI / Web / Cloud | App暂无Linux桌面版 |

### B. 常用CLI辅助命令

```bash
codex --help           # 查看CLI帮助
codex app              # 从终端打开或配合App
codex review           # 审查当前改动
codex exec "任务描述"   # 无头执行一次任务
```

### C. 推荐学习资源

- **Codex App 官方文档**：https://developers.openai.com/codex
- **Codex App Windows**：https://developers.openai.com/codex/app/windows
- **Codex Quickstart**：https://developers.openai.com/codex/quickstart
- **本系列下一篇**：[CX-02 Codex App 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)

---

**课程制作**：老金
**最后更新**：2026年6月18日
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---

## 下一步

下一篇：[CX-02 Codex App 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)。
