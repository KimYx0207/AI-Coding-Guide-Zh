# CX-01 Codex App 安装与认证完整指南：Windows / macOS 从下载到第一个线程


本篇只解决一件事：把 **Codex App** 正确装好、登上号、打开本地项目，并跑通第一个安全任务。

官方来源：OpenAI Codex App 文档、Codex changelog、[Codex App Windows](https://developers.openai.com/codex/app/windows)、[Codex Quickstart](https://developers.openai.com/codex/quickstart)、Codex CLI 文档。本篇按 2026-05-25 可查官方文档与 Codex App changelog 26.519 修订；入口、包名和版本会变化，以官方页面和当前 App 为准。

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
> - **更新日期**：2026年5月
> - **信息来源**：[Codex App Windows](https://developers.openai.com/codex/app/windows) | [Codex Quickstart](https://developers.openai.com/codex/quickstart) | Codex CLI 文档
> - **前置要求**：无（本系列第一篇）

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/codex-integrated-terminal.webp" alt="Codex App 官方集成终端界面" width="720"/></p>

<p align="center"><img src="../../images/official/codex-app-review-pane.webp" alt="Codex App 官方 Review 面板与 diff 实操界面" width="720"/></p>

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

## 0. Critical：先把安装目标说清楚

本系列不是从 CLI 开始，而是从 App 开始。你安装成功的标准不是“终端里有 `codex` 命令”，而是：

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
| Windows 版本 | 使用仍受支持的 Windows 10 / Windows 11 |
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

<p align="center"><img src="../../images/official/codex-windows-sandbox-setup.webp" alt="Codex App Windows sandbox 设置提示" width="720"/></p>

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

> **2026-05-25 安装口径**：Codex App 以官方 App 入口和 App 内更新为准；CLI v0.133.0 的安装路径包括官方 install script、Windows PowerShell install script、npm、Homebrew 和 GitHub Release 二进制包。App 登录适合桌面工作流；API key / CLI 路径适合自动化、CI 和排查。

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

| 检查项 | 通过标准 |
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

## 13. 常见问题

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

**如果以上全部勾选，恭喜你完成Codex App安装！**

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
**最后更新**：2026年5月
**许可**：本课程采用CC BY-NC-SA 4.0许可

---

## 下一步

下一篇：[CX-02 Codex App 桌面工作流](./CX-02-Codex-App桌面工作流完整指南.md)。
