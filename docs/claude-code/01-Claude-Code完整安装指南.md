# Claude Code 完整安装指南：从零开始到成功运行

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：2-3小时（原生安装更简单！）
> - **难度等级**：⭐ 零基础入门
> - **更新日期**：2026年9月14日
> - **适用版本**：Claude Code v2.1.270（验证于 2026-09-14；旧差量保留为历史基线）
> - **重要更新**：当前同时支持原生安装与标准 npm 安装；原生更省心，npm 路径仍然受支持且需要 Node.js 22+

---

## 📚 本课学习目标

我把安装部分写得很细，是因为很多人输在账号、终端和路径这些第一步；后续更新会继续放在 GitHub：https://github.com/KimYx0207。

完成本课学习后，你将能够：

1. **理解Claude Code的核心价值**：掌握Claude Code与传统AI编程工具的本质区别
2. **了解两条安装路径**：知道什么时候优先用原生安装，什么时候仍然可以走 npm 标准安装
3. **选择认证方式**：根据已有订阅、Console 或组织提供的服务完成登录；只有使用 API Key 时才配置密钥
4. **完成Claude Code安装**：掌握原生安装与 npm 标准安装两条主路径
5. **集成到主流IDE**：VS Code、Cursor、JetBrains等编辑器配置
6. **验证环境可用性**：通过Hello World测试确认所有组件正常工作
7. **掌握故障排查技能**：解决大多数常见安装问题
8. **了解从npm迁移**：如果你之前用npm安装过，如何迁移到原生版本

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：这是一篇3000+行的长教程，不用全看！根据你的目标选择路径。

### 路径A：快速上手（⏱️ 30分钟）

**适合人群**：急着体验Claude Code，想快速跑起来

**只看这些章节**（其他跳过）：

```
✅ 术语表（3分钟） - 快速了解关键概念
✅ 第4部分：选择账号和认证方式（10分钟）
✅ 第5部分：选择一条安装路径（5分钟）
✅ 第6部分：首次启动与验证（12分钟）
```

**完成这条路径后**：你应能启动 Claude Code，并检查 Hello World 示例的文件和运行结果。这里的时间只是学习安排，登录、下载和排障可能需要更久。

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想深入理解每个细节，掌握所有功能

**学习顺序**：从头到尾所有章节

**建议分段学习**：
- 第1阶段（约1小时）：第1–5部分，了解工具、检查系统、选择账号和安装方式
- 第2阶段（约1小时）：第6–7部分，验证启动并按需配置 IDE
- 第3阶段（约30分钟）：第8–9部分，查故障排查和 FAQ；模型配置可在安装成功后按需阅读

---

### 路径C：问题排查（⏱️ 10分钟）

**适合人群**：安装过程遇到问题，需要快速解决

**直接跳到这些章节**：

```
🔧 第7部分：故障排查 - 按错误类型查找解决方案
🔧 第8部分：FAQ - 学员最常问的问题
🔧 附录：从npm迁移 - 如果你之前用npm装过
```

**使用方法**：
1. 按 `Ctrl + F` 搜索你的错误信息关键词
2. 找到对应的Q&A
3. 按步骤解决

---

### 路径D：专项学习（⏱️ 30-60分钟/主题）

**适合人群**：已经装好Claude Code，想学习某个特定功能

| 想学什么 | 看哪几节 | 预计时间 |
|----------|---------|---------|
| **IDE集成** | 第6部分 | 30分钟 |
| **权限配置** | 第6.5节（危险参数）+ 第7.3节 | 20分钟 |
| **从npm迁移** | 附录：迁移指南 | 15分钟 |

---

## 术语表（小白必读）

> ⚠️ **2026年重要更新**：Claude Code 现在提供原生安装，但 **npm 标准安装仍受支持**。Node.js 和 npm 不再是唯一入口，但也没有“彻底消失”。

在开始之前，先了解这些关键术语：

| 术语                    | 英文全称                          | 通俗解释                                                           |
| ----------------------- | --------------------------------- | ------------------------------------------------------------------ |
| **CLI**           | Command Line Interface            | 命令行界面，就是那个黑色/白色的文字输入窗口，通过打字来操作电脑    |
| **原生安装器** ⭐   | Native Installer                  | Claude Code官方提供的独立安装程序，不需要其他依赖                   |
| **Node.js** | - | JavaScript 运行环境；如果你走 `npm install -g @anthropic-ai/claude-code` 这条标准安装路径，仍需要 22+ |
| **npm** | Node Package Manager | Node.js 的包管理器；Claude Code 的标准安装路径之一仍然会用到它 |
| **LTS**           | Long Term Support                 | 长期支持版本，稳定、bug少、官方持续维护，适合正式使用              |
| **API**           | Application Programming Interface | 应用程序接口，软件之间"对话"的方式                                 |
| **API Key**       | -                                 | API密钥，类似"通行证"，证明你有权使用某个服务                      |
| **Token**         | -                                 | 计费单位，AI处理文字的最小单元，约等于0.75个英文单词或1-2个汉字    |
| **环境变量**      | Environment Variable              | 操作系统级别的配置项，程序可以读取但不会写在代码里                 |
| **PATH**          | -                                 | 系统环境变量之一，告诉电脑去哪里找可执行程序                       |
| **终端/Terminal** | -                                 | 运行命令行的程序窗口                                               |
| **全局安装**      | Global Install                    | 安装后在电脑任何位置都能使用的安装方式                             |

---

## 第一部分：Claude Code 简介

### 1.1 什么是 Claude Code


Claude Code 是 Anthropic 公司开发的**命令行 AI 编程助手**。本课程主讲 CLI：从终端启动、读项目、改文件、跑命令、做 Review 和自动化。它现在也有 IDE、Desktop、Web 等入口，但这些在本系列里只作为 CLI 工作流的延伸，不反客为主。

**核心特征：**

- **本地执行架构**：文件读写和命令执行发生在你的电脑或企业受控环境里；任务上下文会按登录方式和模型提供商策略发送给 AI 服务
- **全能AI助手**：基于Claude模型，理解复杂技术需求
- **工具整合能力**：可调用文件操作、终端命令、Web搜索等工具
- **对话式开发**：用自然语言描述需求，AI帮你生成和修改代码

**简单理解：**

把 Claude Code 想象成一个在终端里工作的高级程序员。你用中文或英文告诉它需求，它能帮你写代码、改 bug、搜资料、运行测试。**本课程抓住的最大特点是 CLI**：它可以在当前项目目录里读写文件、运行系统命令，并把这些动作纳入脚本化和自动化流程。

### 1.2 核心优势：为什么值得学习

#### 优势1：隐私与安全

很多在线 AI 工具要求你先把代码粘贴到网页里。Claude Code 的不同点不是"永远不把任何内容发给模型"，而是**文件访问、命令执行和权限确认发生在你的本地项目工作流里**。你仍然要根据登录方式、模型提供商、企业策略和项目敏感度控制哪些上下文可以进入模型。

- ✅ 文件改动发生在本地工作区，读写范围受当前目录、权限模式和配置约束
- ✅ 可接企业托管配置、私有网络、Bedrock / Vertex / 第三方兼容提供商等受控路径
- ✅ 敏感项目要配合 allow/deny、MCP 白名单、日志边界、密钥管理和人工 Review，不能只靠一句“本地优先”

#### 优势2：真正的编程助手

**实际案例：**

```
你：帮我把项目中所有console.log改成更规范的日志系统

Claude Code：
1. [扫描] 找到37个console.log调用
2. [询问] 是否使用Winston日志库？
3. [执行] 安装依赖、创建配置、批量替换代码
4. [验证] 运行测试确认改动正确
```

#### 优势3：多语言多框架支持

不限于特定技术栈：

- **前端**：React、Vue、Next.js
- **后端**：Node.js、Python、Go
- **移动端**：React Native、Flutter
- **基础设施**：Docker、Kubernetes配置

### 1.3 与主流工具对比

**CLI工具 vs IDE集成工具对比：**

| 对比项               | Claude Code（CLI）  | Cursor（IDE集成） |
| -------------------- | ------------------- | ----------------- |
| **运行方式**   | 命令行独立运行      | VS Code编辑器内置 |
| **文件操作**   | ✅ 直接读写         | ✅ 直接读写       |
| **项目理解**   | ✅ 全项目上下文     | ✅ 全项目上下文   |
| **脚本自动化** | ✅ 完美支持         | ⚠️ 有限         |
| **CI/CD集成**  | ✅ 原生支持         | ❌ 困难           |
| **远程服务器** | ✅ 完美支持         | ❌ 需要图形界面   |
| **隐私性**     | ✅ 本地优先         | ⚠️ 云端处理     |
| **学习曲线**   | 中等（需要CLI基础） | 低（图形界面）    |

**推荐使用场景：**

**选Claude Code（CLI）适合：**

- ✅ 重构遗留项目、批量代码处理
- ✅ CI/CD自动化、脚本集成
- ✅ 远程服务器开发、无图形界面环境
- ✅ 企业级开发（私有部署、安全要求高）
- ✅ 高级开发者（熟悉命令行、需要自动化）

**选Cursor（IDE集成）适合：**

- ✅ 日常开发、快速原型
- ✅ 学习新框架、初学者友好
- ✅ 需要图形界面和可视化
- ✅ 实时代码补全和建议

### 1.4 适合谁学习

**强烈推荐：**

1. **有1年+编程经验的开发者**：能充分利用AI加速工作流
2. **技术Leader/架构师**：需要快速审查和重构代码
3. **独立开发者**：一个人维护多个项目，需要AI协作
4. **开源贡献者**：快速理解陌生代码库

**需要慎重考虑：**

1. **编程零基础**：建议先学基础语法和终端操作（建议学习时长：3-6个月）
2. **只用图形界面**：可以选择 IDE 扩展或 Desktop；本章的终端路径需要先熟悉基本命令行操作
3. **网络受限**：先确认所选服务支持你的所在地区，以及当前网络能访问对应登录和模型端点；组织网络按管理员提供的代理配置处理

---

## 课前准备检查清单

> ⚠️ **2026年重大更新**：原生安装路径确实**不需要 Node.js**，但 npm 标准安装仍然存在，所以本章会同时教你两条路径。

在开始安装前,请确认以下内容已完成:

| 检查项                      | 状态            | 如果未完成                   |
| --------------------------- | --------------- | ---------------------------- |
| **操作系统兼容** | [ ] 确认 | macOS 13+；Windows 10 1809+ / Server 2019+；Linux 发行版见第二部分 |
| **账号或服务可用** | [ ] 已确认 | 订阅、Console 或组织提供的云服务，见第四部分；API Key 仅适用于相应路径 |
| **终端可用** | [ ] 能打开 | macOS 用终端，Windows 用 PowerShell 或 CMD |
| **网络连接** | [ ] 可访问所选服务 | 核对服务地区、登录端点和模型端点；代理使用实际提供的地址 |

**如果所有项都已完成,让我们开始吧!**

> 💡 **提示**：选择原生安装时无需为 Claude Code 单独安装 Node.js；选择 npm 时仍需 Node.js 22+。运行项目所需的 Python、Git 等工具要按项目要求另行准备，Alpine 还需安装官方列出的系统依赖。

---

## 第二部分：系统要求快速检查

> 💡 **本节目的**：快速确认你的电脑能不能运行Claude Code，3分钟搞定！

### 2.1 快速检查清单（核心3项）

在开始安装前，确认以下3项**核心要求**：

| 检查项 | 最低要求 | 如何检查 | 不符合怎么办 |
|--------|---------|---------|-------------|
| **操作系统** | macOS 13.0+；Windows 10 1809+ / Server 2019+；Ubuntu 20.04+、Debian 10+、Alpine 3.19+ | 查看系统版本 | 按官方支持范围升级系统或换环境 |
| **内存** | 4GB RAM | 右键"此电脑"→属性 | 不足4GB无法运行 |
| **网络** | 能访问外网 | 打开 google.com 试试 | 国内用户需要配置代理（见附录B） |

**快速验证命令：**

**所有平台通用：**
```bash
# 检查 API 的 HTTPS 连接；PowerShell 中请用 curl.exe
curl -I https://api.anthropic.com
# 收到 HTTP 响应可确认已连到服务；不代表认证已通过
# 超时或 TLS 错误时，检查代理、证书和防火墙；ping 失败不能证明 HTTPS 不通
```

**如果3项全部✅ → 恭喜，你的电脑满足要求，继续往下！**

**如果有❌ → 跳到附录A查看详细要求和解决方案。**

---

### 2.2 详细要求说明（可选阅读）

> ⚠️ **小白注意**：这部分是详细技术说明，如果上面快速检查都通过了，可以跳过直接看第三部分！

**操作系统详细兼容性：**

| 操作系统 | 最低版本 | 推荐版本 | 说明 |
|---------|---------|---------|------|
| Windows | Windows 10 1809+ / Server 2019+ | Windows 11 | x64 或 ARM64；原生 Windows 不支持 OS sandbox |
| macOS | 13.0+ | 当前受支持版本 | Intel / Apple Silicon 均支持 |
| Linux | Ubuntu 20.04+、Debian 10+、Alpine 3.19+ | 当前受支持版本 | 同时核对发行版及依赖，不能只看内核版本 |

**硬件推荐（非强制）：**
- **CPU**：双核+（i3或同等性能即可）
- **内存**：8GB更佳（4GB也能用，大项目会慢点）
- **存储**：SSD更快（机械硬盘也行）

> 💡 **建议**：别被这些要求吓到！只要你电脑能正常开发写代码，就肯定能跑Claude Code。这些是"推荐配置"不是"必需配置"。
>
> **详细性能对比和配置建议** → 见附录A

---

## 第三部分：原生安装说明（⭐ 重要更新）

> 💡 **安装路径**：原生安装是官方推荐方式，不需要 Node.js；npm 标准安装仍受支持，需要 Node.js 22+。下面按你的平台选择一条路径。
>
> ⏱️ **预计时间**：安装本身可能只需几分钟，实际下载、登录与排障时间另计。

### 3.1 为什么切换到原生安装？

**背景说明：**

本次按 2026-10-03 的官方安装文档核对：

- 仍然保留 **标准安装**：`npm install -g @anthropic-ai/claude-code`
- 推荐 **原生二进制安装**；npm 也安装同一原生二进制
- 安装后建议运行 `claude doctor` 检查当前安装类型

因此，这里更准确的理解不是"npm 被删除了"，而是：

> Claude Code 从“只有 npm 一条路”，变成了“原生安装 + npm 标准安装并存”。

**原生安装 vs npm安装对比：**

| 对比项         | 原生安装 ⭐ | npm标准安装 |
| -------------- | ----------- | ----------------- |
| 需要Node.js    | ❌ 不需要    | ✅ 需要 22+      |
| 安装准备       | 直接下载二进制 | 先有 Node.js 22+，再由 npm 下载二进制 |
| 自动更新       | 默认开启，可配置 | 默认开启；全局目录不可写时需处理权限 |
| PATH配置       | 按安装器提示核对用户目录 | 核对 npm 全局 bin 目录 |
| 跨平台支持     | 按官方支持的系统和架构选择 | 使用同一原生二进制，亦需符合平台要求 |
| 安装管理       | 原生安装器管理 | npm 管理，需允许 optional dependencies |

**简单理解：**

现在更像是：

- **原生安装**：买成品，拿来即用
- **npm 安装**：由 npm 下载同一原生二进制，安装时需要 Node.js 22+ 和 optional dependencies

### 3.2 原生安装的工作原理

**它是什么？**

原生安装器是一个独立的可执行程序，由Anthropic官方编译和签名。它包含：

- ✅ Claude Code核心程序
- ✅ 所有必需的依赖库
- ✅ 自动更新机制
- ✅ 安全签名验证

**安装到哪？**

| 操作系统   | 安装位置                          |
| ---------- | --------------------------------- |
| Windows    | `C:\Users\你的用户名\.local\bin\` |
| macOS/Linux | `~/.local/bin/claude`             |

### 3.3 自动更新机制

**原生安装器的一大优势：自动更新！**

- ✅ 后台自动检查更新（无需手动操作）
- ✅ 更新在后台下载并安装，下次启动时使用新版本
- ✅ 可配置更新策略（见高级配置）

**如何禁用自动更新？（可选）**

```bash
# 如果你想手动控制更新，可以设置环境变量
export DISABLE_AUTOUPDATER=1
```

> 💡 **建议**：保留自动更新通常更省心。更新跟随所选的 `latest` 或 `stable` 通道；`stable` 通常稍晚，不能把自动更新理解为始终运行最新发布版本。

### 3.4 如果你之前用npm安装过？

**官方提供了迁移命令。**

如果你之前通过 `npm install -g @anthropic-ai/claude-code` 安装过，运行：

```bash
claude install
```

这会下载并安装原生版本。安装程序与原有配置分开管理；迁移前仍建议备份自己的规则和设置。完成后运行 `claude doctor` 检查实际启动路径，确认新副本可用后，再按附录卸载不再需要的 npm 副本。

**详细迁移步骤** → 见附录：从npm迁移指南

---

## 第四部分：Anthropic 账号准备

先确认你准备用哪种账号，再安装和登录；API Key 是其中一种认证凭据。

- **已有 Pro、Max、Team 或 Enterprise**：安装后用 claude.ai 账号在浏览器中登录。团队用户先确认管理员已邀请你并给了相应席位。
- **使用 Claude Console**：按 API 用量结算。当前客户端也支持 Console 浏览器登录而不创建 API Key；组织策略可能改变可选路径。
- **组织使用 Bedrock、Google Cloud Agent Platform、Foundry 或 Claude apps gateway**：先拿到管理员提供的接入说明，再按对应官方部署文档配置。

### 4.1 准备可用账号

订阅入口见 [Claude 价格页](https://claude.com/pricing)，Console 入口见 [Claude Console](https://platform.claude.com/)。已有账号无需为了跟练再注册。创建账号前先核对[官方支持的国家和地区](https://www.anthropic.com/supported-countries)，注册方式、验证要求和组织资格以实际页面为准。

本教程没有验证中国大陆手机号注册成功率，也不能承诺固定赠送额度。验证码或地区资格有问题时，请查官方支持说明或联系支持，不要依据旧教程猜测可用号码或登录按钮。

下一节只供选择 API Key 路径的读者使用；订阅和 Console 浏览器登录用户可以直接进入第五部分。

### 4.2 API Key 获取步骤

**什么是API Key？**

API Key 是一串认证凭据，用来证明调用者身份并把请求计入所属组织。API 费用按实际模型和用量计算，不是只按请求次数结算。

**格式示例：**

```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**获取步骤：**

1. 打开 [Console 的 API Keys 页面](https://platform.claude.com/settings/keys)，确认当前组织和工作区。
2. 按实际页面创建 Key。组织角色可能限制你能创建的密钥；不要为了跟练默认扩大权限。
3. 把凭据存入自己的密码管理器或组织认可的凭据存储。不要把它保存成项目文件，也不要认为 Documents 中的明文文本自动安全。
4. 配置到本机后，用下面的命令检查客户端当前使用哪种认证：

   ```bash
   claude auth status --text
   ```

这条命令显示认证状态，不发起模型生成请求，也不证明余额和模型资格都已可用。等首次实际任务成功后，再核对客户端结果与 Console 用量。不要为了验证安装先执行一条可能计费的 `/v1/messages` 请求，也不要把密钥打印到终端或贴到排障截图里。

### 4.3 环境变量配置

**什么是环境变量？**

环境变量是操作系统级别的配置，让程序可以读取敏感信息（如API Key），而不需要写在代码里。

**好处：**

- ✅ 减少把密钥直接写入源码的需要，但环境变量仍可能被进程、日志或 shell 历史泄露
- ✅ 不同电脑可以使用不同凭据
- ✅ Claude Code 支持 `ANTHROPIC_API_KEY`；其他工具要按自己的文档配置

#### Windows配置方法

**推荐方法：PowerShell 7（最佳选择）**

```powershell
# 永久添加用户环境变量（PowerShell 7）
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-api03-你的key', 'User')

# 关闭并重新打开 PowerShell 后，检查是否已配置；不要显示密钥值
[bool]$env:ANTHROPIC_API_KEY
```

**临时配置（仅当前终端有效）：**

```powershell
# PowerShell（包括PowerShell 5和7）
$env:ANTHROPIC_API_KEY="sk-ant-api03-你的key"

# CMD（不推荐，功能有限）
set ANTHROPIC_API_KEY=sk-ant-api03-你的key
```

**永久配置方法2：通过图形界面**

1. 右键"此电脑" → 属性
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"用户变量"区域点击"新建"
5. 变量名：`ANTHROPIC_API_KEY`
6. 变量值：`sk-ant-api03-你的完整key`
7. 点击"确定"保存
8. **重启所有终端窗口**

> **提示**：图形界面方法适合不熟悉命令行的用户，但PowerShell 7方法更快捷。

#### macOS/Linux配置方法

```bash
# 确定使用的Shell
echo $SHELL

# 如果是bash,编辑~/.bashrc
# 如果是zsh(macOS默认),编辑~/.zshrc

# 添加以下行（替换为真实Key）
export ANTHROPIC_API_KEY="sk-ant-api03-你的key"

# 保存后重新加载
source ~/.zshrc  # 或 source ~/.bashrc

# 只检查是否设置，不打印密钥
if [ -n "$ANTHROPIC_API_KEY" ]; then echo "API Key 已配置"; else echo "API Key 未配置"; fi
```

**使用nano编辑器示例：**

```bash
# 打开配置文件
nano ~/.zshrc

# 添加Key配置
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"

# 保存：Ctrl+O → 回车 → Ctrl+X退出
```

#### 安全注意事项

**✅ 正确做法：**

- 只在本地配置环境变量
- 不要提交 `.env` 文件到Git
- 定期轮换API Key

**❌ 错误做法：**

- 把Key直接写在代码里：`const key = "sk-ant-..."`
- 在GitHub Issues/论坛公开Key
- 与他人共享Key

**泄露后的处理：**

1. 立即到Console删除泄露的Key
2. 创建新Key
3. 更新环境变量
4. 检查API使用记录是否异常

### 4.3.1 API中转站配置（可选）

> 💡 **自定义端点是什么？** 组织网关或第三方服务可能给你一个不同的 API 地址。它与 Anthropic 官方订阅、Console 或官方支持的云平台接入不是同一件事。

这里不评价第三方服务的价格、稳定性、支付方式或赠送额度。接入前先确认它是否兼容 Claude Code 所需的 Anthropic 协议、实际认证变量和模型名称，以及谁能看到请求内容；不能仅凭“可以连接”认定所有功能都受支持。

**配置方法：**

中转站会提供一个自定义的 API 地址（Base URL），你需要同时配置 `ANTHROPIC_API_KEY` 和 `ANTHROPIC_BASE_URL` 两个环境变量。

**Windows（PowerShell）：**

```powershell
# 设置中转站API Key（中转站提供的Key）
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', '你的中转站Key', 'User')

# 设置中转站API地址
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL', 'https://网关提供的实际基础地址', 'User')

# 重启终端后验证
$env:ANTHROPIC_BASE_URL
```

**macOS/Linux：**

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export ANTHROPIC_API_KEY="你的中转站Key"
export ANTHROPIC_BASE_URL="https://网关提供的实际基础地址"

# 根据你使用的 shell 重新加载对应文件
source ~/.zshrc  # Bash 用户改为 source ~/.bashrc
```

**验证中转站是否生效：**

```bash
# 启动Claude Code后，观察是否能正常连接
claude

# 连接成功后，用 /status 核对认证和模型，再检查实际任务结果
# 报错时按服务提供方的文档核对 Base URL、认证方式和协议；不要随意补 /v1
```

> 自定义端点会改变请求接收方。仅把允许交给该服务的材料放入任务；如果要恢复官方接入，还要核对并移除不再需要的 Base URL 与第三方认证配置。

### 4.4 计费与订阅

**Claude Code需要付费吗？**

费用取决于你选择的接入方式：

1. **Claude 订阅**：Pro、Max、Team、Enterprise 通过相应计划使用 Claude Code，仍有用量和席位条件；需要额外用量的功能可能另收 usage credits。
2. **Console 或云提供商**：按对应模型、输入输出、缓存等实际用量计费，组织可以设置支出限制。

公开 GitHub 仓库不等于 Claude Code 本体采用开源许可。其[官方许可](https://github.com/anthropics/claude-code/blob/main/LICENSE.md)说明使用受 Anthropic 的服务条款约束；本课程的 MIT 许可也不适用于 Claude Code 产品。

**Token 是什么？**

Token 是模型处理文本的单位。分词结果随语言、文本和模型变化，不能用固定的“1–2 个汉字”或“1000 tokens = 750 字”精确推算账单。API 计费还要区分输入、输出和缓存。

具体计划见 [Claude 价格页](https://claude.com/pricing)，API 价格见 [官方 API 价格文档](https://platform.claude.com/docs/en/about-claude/pricing)。使用中运行 `/usage` 查看当前客户端提供的用量信息，实际支出再到所用服务的账单页面核对。

---

## 第五部分：Claude Code 原生安装（⭐ 核心重点）

> 💡 **本部分目标**：一行命令完成安装，5分钟搞定！
> ⏱️ **预计时间**：3-5分钟

### 5.1 安装方式概览

**下面列出常见安装方式**，选择其中一条即可：

| 安装方式 | 适用平台 | 要检查什么 |
|----------|----------|------------|
| **脚本安装** | macOS / Linux / WSL | 使用对应 shell；Alpine 先准备系统依赖 |
| **PowerShell** | 原生 Windows | 用户目录安装，不必默认管理员 |
| **Homebrew cask** | macOS / Linux，按当前 cask 支持列表确认 | 由 Homebrew 管理，按 cask 通道升级 |
| **WinGet** | 支持 WinGet 的 Windows | 包管理器升级方式与原生自动更新不同 |
| **npm** | 支持的平台 | Node.js 22+，不要禁用 optional dependencies |

Linux 还可使用官方 apt / dnf / apk 软件源；需要这条路径时参照[官方安装说明](https://code.claude.com/docs/en/setup#install-with-linux-package-managers)。

> 💡 **推荐**：
> - **Windows用户**：用PowerShell（最简单）
> - **Mac用户**：用脚本安装或Homebrew（都很快）
> - **Linux用户**：用脚本安装
> - **原生安装失败？**：可以试试官方支持的 npm 方式（见方式4），先准备 Node.js 22+ 并确认 optional dependencies 没有被禁用

---

### 5.2 方式1：脚本安装（推荐 - 跨平台）

#### macOS / Linux / WSL 安装

**打开终端，复制粘贴以下命令：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**一行命令解释：**

| 部分                      | 作用                                   |
| ------------------------- | -------------------------------------- |
| `curl -fsSL`             | 下载安装脚本（-f遇到 HTTP 错误时返回失败，-s静默，-S显示错误，-L跟随重定向） |
| `https://claude.ai/install.sh` | Anthropic官方安装脚本地址              |
| `| bash`                 | 把下载的内容直接传给bash执行           |

**安装过程：**

```
[终端显示]
Downloading Claude Code...
Installing to /home/你的用户名/.local/bin/claude
✓ Installation complete!
✓ Added to PATH

Run 'claude --version' to verify.
```

**验证安装：**

```bash
claude --version
# 输出当前安装版本；安装类型和启动路径用 claude doctor 核对
```

#### Windows PowerShell 安装

**步骤1：打开PowerShell**

- 按 `Win` 键
- 输入 `PowerShell`
- 按 `Enter` 打开普通 PowerShell 窗口；原生安装不需要管理员权限

**步骤2：执行安装命令**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**命令解释：**

| 部分                        | 作用                           |
| --------------------------- | ------------------------------ |
| `irm`                       | `Invoke-RestMethod` 的别名，下载内容 |
| `https://claude.ai/install.ps1` | Windows安装脚本地址           |
| `| iex`                     | `| Invoke-Expression`，执行下载的脚本 |

**安装过程：**

```
[PowerShell显示]
Downloading Claude Code...
Installing to C:\Users\你的用户名\.local\bin\
✓ Installation complete!

Run 'claude --version' to verify.
```

> ⚠️ **重要提醒**：PowerShell 脚本安装完成后，**不会自动配置 PATH 环境变量**！你需要手动配置 PATH 才能在终端中直接使用 `claude` 命令。请继续阅读下方的 **PATH 环境变量配置** 章节。

---

### 5.3 方式2：Homebrew安装（macOS/Linux）

如果你是Mac用户且已经安装了Homebrew，这是最简单的方式：

```bash
brew install --cask claude-code
```

**优势：**
- ✅ Homebrew自动管理依赖
- ✅ 方便更新：`brew upgrade claude-code`
- ✅ 方便卸载：`brew uninstall claude-code`

**注意：** Homebrew安装**不会自动更新**，需要手动运行更新命令。

---

### 5.4 方式3：WinGet安装（Windows）

Windows 10/11用户可以使用WinGet包管理器：

```powershell
winget install Anthropic.ClaudeCode
```

**优势：**
- ✅ Windows原生包管理器
- ✅ 系统级安装
- ✅ 方便更新：`winget upgrade Anthropic.ClaudeCode`

---

### 5.5 方式4：NPM安装（标准兼容路径）

> ⚠️ **重要说明**：当前官方仍支持 npm 安装，它下载的也是原生二进制。npm 安装需要 Node.js 22+，并允许安装 optional dependencies；装好后的 `claude` 不依赖 Node.js 运行。新手优先走原生安装，也可以按自己的环境选择 Homebrew、WinGet 或 npm。

**前提条件**：需要先安装 [Node.js](https://nodejs.org/) 22 或更高版本。

```bash
# 检查 Node.js 版本（需要 22+）
node --version

# 通过 NPM 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code
```

**各平台安装细节：**

**Windows（CMD 或 PowerShell）：**

```powershell
# 直接全局安装
npm install -g @anthropic-ai/claude-code

# 验证
claude --version
# 这里只核对版本号；安装类型用 claude doctor 查看
```

**macOS/Linux：**

```bash
# 全局安装（不要用 sudo！）
npm install -g @anthropic-ai/claude-code

# 如果提示权限错误，修复 npm 全局目录权限
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# 然后重新安装
npm install -g @anthropic-ai/claude-code
```

**NPM 安装 vs 原生安装的区别：**

| 对比项 | 原生安装 ⭐ | NPM 安装 ⚠️ |
|--------|------------|-------------|
| 需要 Node.js | ❌ 不需要 | ✅ 需要 22+ |
| 自动更新 | 默认开启，可配置 | 默认开启；手动升级用 `npm install -g @anthropic-ai/claude-code@latest` |
| 安装大小 | ~80MB | ~80MB + Node.js |
| 官方支持 | ✅ 当前更推荐 | ✅ 仍受支持 |
| 适合场景 | 所有用户 | 原生安装失败时的备选 |

> 💡 **建议**：如果你是全新环境，优先试原生安装；如果你本来就有稳定的 Node 22+ 环境，或者原生安装在你机器上受阻，npm 仍然是完全合理的选择。装好之后也可以随时通过 `claude install` 迁移到原生版本。

---

### 5.6 配置 PATH 环境变量（Windows 必读）

> 💡 **为什么需要配置 PATH？** Claude Code 通过 PowerShell 脚本安装后，可执行文件位于 `C:\Users\你的用户名\.local\bin\`，但该目录可能不在系统的 PATH 环境变量中。不配置 PATH，终端就找不到 `claude` 命令，会报 `'claude' 不是内部或外部命令` 的错误。

#### 方法1：PowerShell 命令配置（推荐）

```powershell
# 将 Claude Code 安装目录添加到用户 PATH 环境变量
[System.Environment]::SetEnvironmentVariable(
    'Path',
    [System.Environment]::GetEnvironmentVariable('Path', 'User') + ';' + "$env:USERPROFILE\.local\bin",
    'User'
)
```

> ⚠️ 配置完成后，**必须重启 PowerShell / CMD 窗口**才能生效！

**验证 PATH 是否配置成功：**

```powershell
# 重启终端后执行
claude --version
# 能显示当前版本号，说明此终端能找到 claude；安装类型用 claude doctor 核对
```

#### 方法2：通过系统设置（图形界面）

1. 按下 `Win + R` 打开"运行"对话框
2. 输入 `sysdm.cpl`，按回车，打开"系统属性"
3. 点击 **"高级"** 选项卡
4. 点击底部的 **"环境变量"** 按钮
5. 在 **"用户变量"** 区域找到 `Path`，双击编辑
6. 点击 **"新建"**，添加：`%USERPROFILE%\.local\bin`
7. 点击 **"确定"** 保存所有对话框
8. **重启所有终端窗口**

#### macOS / Linux 用户

脚本安装通常会自动将 `~/.local/bin` 添加到 PATH。如果安装后 `claude` 命令不可用，手动添加：

```bash
# 添加到 shell 配置文件（zsh 用户）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# bash 用户
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### 5.7 验证安装成功

**无论用哪种方式，安装完成后验证：**

```bash
# 检查版本
claude --version
# 输出当前安装版本；安装类型和启动路径用 claude doctor 核对

# 检查帮助
claude --help
# 应该显示完整帮助信息

# 检查安装位置
where.exe claude  # Windows PowerShell / CMD
which claude     # macOS/Linux
```

**成功的标志：**
- ✅ 显示当前安装版本，`claude doctor` 能确认安装类型和启动路径
- ✅ 命令可以直接运行（不提示找不到命令）
- ✅ `--help` 能显示帮助信息

---

### 5.8 安装失败排查

#### 问题1：检查 PATH 环境变量配置是否正确

```
claude: command not found
# 或 Windows 上的：
'claude' 不是内部或外部命令
```

**原因**：PATH 环境变量未包含 Claude Code 安装目录

**排查步骤：**

```powershell
# 第一步：确认 claude 可执行文件存在
# Windows:
Test-Path "$env:USERPROFILE\.local\bin\claude.exe"
# 如果返回 True，说明安装成功，只是 PATH 没配

# macOS/Linux:
ls ~/.local/bin/claude
```

```powershell
# 第二步：检查 PATH 是否包含安装目录
# Windows:
$env:Path -split ';' | Select-String '.local'
# 如果没有输出，说明 PATH 未配置

# macOS/Linux:
echo $PATH | tr ':' '\n' | grep '.local'
```

**解决方案：** 按照上方 **5.6 配置 PATH 环境变量** 章节进行配置，然后**重启终端窗口**。

#### 问题2：权限被拒绝

```bash
Error: EACCES: permission denied
```

**解决方案：**

```bash
# macOS/Linux: 不需要sudo了！原生安装会安装到用户目录
# 如果还是提示权限，检查目录所有权
ls -la ~/.local/bin

# Windows 原生用户目录安装也通常不需要管理员；先检查实际路径、文件占用和组织策略
```

#### 问题3：网络连接失败

```
Error: Failed to download
```

**解决方案：**

```bash
# 配置代理（如果使用代理）
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890

# 然后重新运行安装命令
curl -fsSL https://claude.ai/install.sh | bash
```

#### 问题4：Windows SmartScreen拦截

```
Windows已保护你的电脑
```

**解决方案：**

先核对文件是否来自官方安装入口，并按[官方签名说明](https://code.claude.com/docs/en/setup#platform-code-signatures)验证发布者和完整性。来源或签名异常时不要继续运行；公司设备按管理员流程处理。不能仅凭出现 SmartScreen 就断定是新签名误报并点击“仍要运行”。

---

### 5.9 卸载 Claude Code

先用 `claude doctor` 确认安装方式，按对应路径卸载。以下两个代码块只用于原生安装：

**macOS/Linux：**

```bash
# 移除原生启动器和版本文件
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell：**

```powershell
Remove-Item -LiteralPath "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -LiteralPath "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

这些步骤保留用户设置和会话。只有明确要清除数据时，先备份自己的规则和记录，再按[官方清理配置说明](https://code.claude.com/docs/en/setup#remove-configuration-files)处理 `~/.claude/` 和 `~/.claude.json`。不要从 Path 中直接删除整个 `.local/bin`，因为其他程序也可能使用这个目录。

**Homebrew卸载：**

```bash
brew uninstall --cask claude-code
```

**WinGet卸载：**

```powershell
winget uninstall Anthropic.ClaudeCode
```

---

## 第六部分：首次启动与验证

### 6.1 启动 Claude Code：交互会话与打印模式

**方式1：标准交互模式（最常用）**

```bash
# 在任意目录启动
claude

# 启动流程：
# 1. 检测当前目录
# 2. 加载CLAUDE.md（如果存在）
# 3. 进入交互式对话界面
```

**方式2：带初始问题的交互会话**

```bash
# 启动交互会话，并把这句话作为第一条消息
claude "你的问题或指令"

# 示例：
claude "What is 2 + 2?"
claude "List files in current directory"
claude "Explain this code: app.js"
```

**方式3：打印模式（脚本友好）**

```bash
# 只输出AI响应,不显示格式
claude -p "你的问题"

# 示例：
claude -p "hello" > output.txt
echo "分析这段代码" | claude -p
```

### 6.2 首次启动的初始化流程

当你第一次运行 `claude` 时，会经历一个交互式配置向导。

**配置步骤1：选择主题**

按照终端中实际列出的主题选择，使用箭头键和 Enter 确认。菜单会随版本变化，不必寻找本教程旧示意中的 `System` 选项；进入会话后还能用 `/theme` 调整。

**配置步骤2：安全须知确认**

阅读当前客户端显示的使用和安全提示，确认你理解工具可以读取文件、修改文件并运行命令。不要把目录信任提示理解为系统隔离；下面的权限说明才是检查操作边界的入口。

**重要理解 - Claude Code的权限模型：**

1. **先看当前权限模式**：工具调用按模式、已有规则和组织策略处理，不一定每次修改都再问你。v2.1.283 起，交互终端和 VS Code 在满足可用条件时默认使用 auto；显式设置和部分环境会改变起始模式，详见[官方起始模式说明](https://code.claude.com/docs/en/permission-modes#which-mode-a-session-starts-in)。
2. **目录不是隔离边界**：在项目目录启动不代表只能访问这里；额外目录、工具、MCP、hooks 与权限规则都要结合检查。
3. **沙箱另行配置**：OS sandbox 主要约束 shell 的文件与网络访问，需要按平台启用；原生 Windows 不支持，不能假定安装后自动获得隔离。
4. **用结果核对操作**：查看会话中的工具调用和实际文件改动；需要组织审计时另行配置日志，不能把会话记录当完整的安全审计系统。

**配置步骤3：目录信任确认**

客户端请求信任目录时，先检查显示的实际路径和仓库来源，再按界面中的选项决定是否继续。本教程不要求你信任上级目录；具体选项以当前客户端为准。

**不要信任以下目录：**

- ✗ 下载目录（可能有恶意代码）
- ✗ 临时目录（不需要持久访问）
- ✗ 系统目录（危险！）
- ✗ 不明来源的代码目录

**配置步骤4：认证方式选择**

按照第四部分选好的账号登录。订阅和 Team / Enterprise 用户通常走 claude.ai 浏览器登录；Console 用户可以选择当前支持的浏览器登录路径或 API Key；组织云平台用户按对应接入说明配置。

若已设置 `ANTHROPIC_API_KEY`，客户端可能先要求确认使用该凭据，而不打开订阅登录流程。登录完成后，在 shell 运行 `claude auth status --text`，在会话中用 `/status` 核对实际认证。环境变量、浏览器登录和密钥存储各有用途，不能用星级断言一种总是最安全。

**第三方平台与 AWS Bedrock（v2.1.92，摘自官方 release）**：[v2.1.92](https://github.com/anthropics/claude-code/releases/tag/v2.1.92) 写明，在登录界面选择 **「3rd-party platform」** 时，可使用 **interactive Bedrock setup wizard**，引导完成 *AWS authentication, region configuration, credential verification, and model pinning*。菜单文案与步骤顺序以你安装的 CLI 版本为准；与仅使用 API Key / `modelOverrides` 走 Bedrock 的路径是否等价，请按官方文档区分场景。

**配置步骤5：完成初始化**

完成后，确认可以输入任务，并用 `/status` 查看实际工作目录、模型与认证。界面版本号和默认模型随安装渠道、账号和组织设置变化，不必和旧示意中的 v2.1.92 / Sonnet 4 相同。

### 6.3 配置文件结构

常用配置位置如下。先分清项目指令、设置文件和客户端状态，再决定改哪一份：

```text
~/.claude/settings.json             用户设置
~/.claude.json                      客户端状态与部分全局配置
项目目录/CLAUDE.md                  项目指令
项目目录/.claude/settings.json      项目共享设置
项目目录/.claude/settings.local.json 个人项目设置
项目目录/.claude/agents/            子代理定义
项目目录/.claude/skills/            Skills
项目目录/.claude/commands/          legacy commands
项目目录/.mcp.json                  项目 MCP 配置
```

组织还可以提供 managed settings；部分配置有专属作用域。认证凭据的存储方式随平台和认证路径变化，不要照着旧 `auth-token.json` 文件名手工创建或编辑。详见[官方设置文件与优先级](https://code.claude.com/docs/en/settings)。

---

## 第6.5部分：Claude Code启动方式详解

> 💡 **本节重点**：掌握2种启动Claude Code的方式，理解权限参数的作用

### 6.5.1 启动方式概览

Claude Code有**2种启动方式**：

| 启动方式               | 适用场景            | 优点                 | 缺点         |
| ---------------------- | ------------------- | -------------------- | ------------ |
| **终端命令启动** | 独立使用Claude Code | 快速、灵活、支持参数 | 需要记命令   |
| **IDE扩展启动**  | 在编辑器内使用      | 可视化、方便         | 需要安装扩展 |

> 💡 **推荐**：初学者先学终端启动，掌握后再用IDE扩展（更灵活）

---

### 6.5.2 方式一：终端命令启动（基础必学）

**这是什么？**
在命令行（终端）里输入 `claude` 命令，直接启动Claude Code的对话界面。

**为什么要学这个？**

- ✅ 最基础的启动方式，适用所有场景
- ✅ 可以添加参数控制行为
- ✅ 支持脚本自动化

#### 基础启动命令

**最简单的启动方式：**

```bash
# 在任意目录下运行
claude
```

**运行后会看到：**

```
╭─────────────────────────────────────────────────────────╮
│                                                         │
│  Welcome to Claude Code v2.1                           │
│                                                         │
│  • Type /help to see available commands                │
│  • Use /exit to quit                                    │
╰─────────────────────────────────────────────────────────╯

Claude Code v2.1.92
Working directory: /你的当前目录

You: █
```

看到这个界面 → ✅ 启动成功！

#### 带参数的启动命令

**常用启动参数：**

| 参数                                      | 作用                   | 什么时候用           |
| ----------------------------------------- | ---------------------- | -------------------- |
| `claude` | 默认启动；权限按当前模式与规则处理 | 日常使用 |
| `claude --dangerously-skip-permissions` | 跳过大多数权限确认 | 仅限已做好隔离的受控环境 |
| `claude -p "你的问题"`                  | 直接提问模式           | 快速查询，不需要对话 |
| `claude -p "任务" --output-format json` | 打印模式，输出 JSON | 脚本读取结构化结果 |

#### --dangerously-skip-permissions 详解（重要！）

**这是什么？**
这个参数会让Claude Code跳过权限询问，直接执行所有操作（读文件、写文件、运行命令）。Anthropic官方称之为**"Safe YOLO mode"**（You Only Live Once模式）。

**为什么叫"dangerously"（危险）？**

因为Claude Code是AI助手，它可能会：
- 修改你的代码文件
- 删除文件
- 运行系统命令
- 安装/卸载软件包

如果跳过权限询问，AI做错了你可能来不及阻止！

**理解风险：**

这个参数等同于进入 `bypassPermissions`，会跳过权限流程中的大多数检查，但不是所有来源信任与配置规则都消失。它也不会建立 OS sandbox。文件、shell 和外部工具都可能造成实际改动，使用前应按[官方权限模式说明](https://code.claude.com/docs/en/permission-modes)检查边界。

不加参数时也不一定每次操作都问你：当前交互会话可能从 auto 开始，已有 allow 规则也可能免确认。需要手动检查时，用 `claude --permission-mode default` 从 Manual 开始，再看每次提示。

**什么时候考虑使用？**

只在你已经建立隔离边界、能接受工作区被改动的受控环境里考虑使用。官方建议使用隔离容器或虚拟机，并限制它能接触的文件和网络。模型调用本身仍需要连接所选服务；“隔离网络”指限制其他网络访问，不是让 Claude 离线推理。

`permissions.allow` 只指定哪些调用可以免审批，不会把其余工具从会话中移除，也不能恢复 bypass 模式跳过的确认。日常开发优先保留正常权限流程；文件分析可以使用下面的受限打印模式。Git 能帮助恢复已跟踪的改动，但不能保护未提交内容、密钥或外部服务。

**使用示例：**

```bash
# 文件分析：v2.1.248+ 的受限模式移除命令执行等工具
# 它仍不是操作系统级隔离，具体限制见 CLI 参考
claude --restricted -p "分析这个项目的依赖关系"

# 若希望跟练时手动查看权限提示，从 Manual 开始
claude --permission-mode default
```

> 是否考虑 bypass，取决于文件与网络隔离、可恢复的数据和明确的任务范围，不取决于已经学了几周，也不取决于仓库属于个人还是公司。初次练习保留正常权限流程，查看实际工具调用和 diff；需要自动化时再为具体工具配置有限的允许规则。

#### 启动验证清单

启动成功后，确认以下内容：

```
□ 看到Claude Code的欢迎界面
□ 显示正确的工作目录路径
□ 显示版本号（v2.1+）
□ 能看到 "You: █" 光标闪烁
□ 输入 /help 能看到帮助信息
```

全部打勾 → 🎉 启动成功！

---

### 6.5.3 方式二：IDE扩展启动（进阶）

**这是什么？**
在VS Code或Cursor编辑器内安装扩展/插件，通过点击按钮或快捷键启动Claude Code，不用手敲命令。

**为什么要用这个方式？**

- ✅ 可视化界面，更直观
- ✅ 和编辑器深度集成
- ✅ 不用切换窗口

**适用工具：**

- VS Code（需要安装Claude Code扩展）
- Cursor（可安装官方扩展，也可在集成终端或 Tasks 中运行 CLI）

#### VS Code扩展安装（官方扩展已发布）

> 官方提供 VS Code 扩展，也支持 Cursor 等兼容编辑器；安装和登录条件见[官方 IDE 指南](https://code.claude.com/docs/en/vs-code)。

**扩展信息：**
- **名称**：Claude Code for VS Code
- **发布者**：Anthropic
- **要求**：VS Code 1.98.0+
- **市场地址**：https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code

**安装步骤：**

1. **打开扩展市场**
   - 按 `Ctrl/Cmd + Shift + X`

2. **搜索并安装**
   - 搜索：`Claude Code`
   - 找到Anthropic官方扩展
   - 点击"Install"

3. **验证安装**
   - 左侧活动栏出现 **⚡火花图标**
   - 点击图标打开Claude Code面板

**扩展功能（vs 终端CLI）：**
- ✅ 侧边栏专用面板（代码和对话分离）
- ✅ 实时内联差异显示（修改高亮）
- ✅ Checkpoint自动保存（按Esc两次回滚）
- ✅ @提及文件/函数（智能引用）

**参考文档**：https://code.claude.com/docs/en/vs-code

#### Cursor 集成方式

1. 在 Cursor 的扩展面板搜索 **Claude Code**，或使用[官方页面的 Install for Cursor 入口](https://code.claude.com/docs/en/vs-code#install-the-extension)。
2. 安装后打开 Claude Code 面板，按实际页面完成登录；没出现时重启编辑器或执行 `Developer: Reload Window`。
3. 确认面板可接受任务。扩展带有供聊天面板使用的 CLI 副本；如果还要在集成终端运行 `claude`，需完成本章独立 CLI 安装。

编辑器无法安装扩展时，可以在集成终端运行 CLI，或按第7.1节建立 Tasks。Tasks 是调用终端命令的快捷入口，不包含扩展的全部界面能力，也没有证据保证它更稳定。

---

### 6.5.4 启动方式选择建议

| 你的情况       | 推荐方式         | 原因           |
| -------------- | ---------------- | -------------- |
| 刚开始学习     | 终端命令启动     | 理解基础，灵活 |
| 熟悉后日常使用 | 终端 + IDE快捷键 | 效率最高       |
| 只想快速体验   | 终端命令启动     | 最简单         |
| 需要自动化     | 终端 + 参数      | 支持脚本       |

**老金的建议：**
先用终端命令启动，等你熟悉了Claude Code的行为，再配置IDE快捷键。这样基础扎实，以后遇到问题好排查！

---

### 6.6 Hello World 快速验证

> 💡 **重要**：启动成功后，立即做这个快速验证，确保Claude Code能正常工作！这样后面配置IDE时心里有底。

#### 6.6.1 基础功能测试（5分钟）

**下面用4项检查确认基本启动和问答：** 问答会发起模型请求，可能消耗订阅额度或 API 用量；不要求回复逐字等于示意。

```bash
# 测试1：版本检查
claude --version
# 输出当前安装版本；安装类型和启动路径用 claude doctor 核对

# 测试2：简单问答
claude -p "What is 2 + 2?"
# 预期输出：4

# 测试3：中文支持
claude -p "你好,请用一句话介绍你自己"
# 预期输出：中文回复（确认中文正常）

# 测试4：帮助命令
claude --help
# 预期输出：显示所有可用命令
```

**如果以上4项全部成功 → ✅ Claude Code工作正常，继续往下！**

**如果有失败 → ⚠️ 跳到第8部分故障排查**

---

#### 6.6.2 Hello World 项目实战（15分钟）

**这是什么？**
创建一个完整的小项目，测试Claude Code的文件操作、代码生成、测试生成等核心功能。

**为什么要做？**
快速测试能发现大多数配置问题，避免后续出错。

**操作步骤：**

先确认已经有 Python：macOS/Linux 通常用 `python3 --version`，Windows 可用 `python --version` 或 `py --version`。这些运行时不随原生 Claude Code 一起安装；未准备好时，可以先检查文件，运行结果留到环境就绪后验证。这个练习不需要 Git，已有 Git 的读者可以自行建仓库观察 diff。

1. 用编辑器创建空目录 `claude-hello-world`，在该目录打开终端。
2. 运行 `claude`，在交互会话中输入：

   ```text
   在当前练习目录创建一个 Python Hello World 项目：
   hello.py 打印 Hello, Claude Code!，README.md 说明运行命令，
   .gitignore 写入 Python 常见忽略项。只修改这个目录，不新增依赖。
   完成后告诉我实际创建了哪些文件；没有运行 Python 就明确说明。
   ```

3. 按当前权限提示处理，并在编辑器中核对 `hello.py`、`README.md` 和 `.gitignore` 的实际内容。不要仅凭回复里列了文件就认为已经创建。
4. 返回 shell，在这个目录运行 `python3 hello.py`（macOS/Linux）或已确认可用的 `python hello.py` / `py hello.py`（Windows）。预期输出为 `Hello, Claude Code!`；没出现时按实际报错排查。

**预期项目结构：**
```
claude-hello-world/
├── .git/
├── .gitignore
├── hello.py
└── README.md
```

**验证成功标志：**
- ✅ 文件自动创建成功
- ✅ Python程序能正常运行
- ✅ Claude理解你的中文指令

---

#### 6.6.3 完整验证清单

启动和验证都成功后，最后确认：

| 验证项 | 命令 | 预期结果 | 状态 |
|--------|------|----------|------|
| 版本信息 | `claude --version` | 显示当前安装版本 | [ ] |
| 帮助文档 | `claude --help` | 显示命令列表 | [ ] |
| 认证方式 | `claude auth status --text` | 符合你选择的账号或提供商 | [ ] |
| 网络连通 | 对所用服务做 HTTPS 检查 | 能收到 HTTP 响应；不代表已获模型权限 | [ ] |
| 文件操作 | 在编辑器中核对 Hello World 文件 | 内容符合练习任务 | [ ] |
| 代码执行 | 使用上一步确认可用的 Python 命令 | 正常输出；没有 Python 时先补环境 | [ ] |

**全部打勾 → Claude Code 安装和配置成功。**

**现在你可以：**
- ✅ 继续学习第7部分（IDE集成配置）
- ✅ 跳过第7部分，直接开始用Claude Code写项目
- ✅ 查看第9部分FAQ了解更多技巧

---

## 第七部分：IDE 集成配置

> ⚠️ **重要提示**：这部分是**可选的高级配置**！
>
> **前置条件**：第6部分的Hello World验证必须成功，否则别急着配置IDE！
>
> **适合人群**：
> - ✅ 已经成功启动Claude Code并完成Hello World测试
> - ✅ 想在VS Code/Cursor里更方便地使用Claude Code
> - ✅ 愿意花30分钟配置快捷键和任务
>
> **如果你只想用终端命令**：可以跳过这部分，直接用 `claude` 命令就够了！

### 7.1 VS Code 完整集成方案


> 💡 **这一节讲什么**：配置VS Code/Cursor编辑器，让它能完美运行Claude Code命令。配置后你就能在编辑器里一键调用AI助手了。

#### 步骤1：VS Code基础配置

首先确保VS Code已安装最新版本：

```bash
# 检查VS Code版本
code --version

# 如果未安装，访问：https://code.visualstudio.com/
```

> 💡 **Cursor 用户**：下面的终端和 Tasks 配置可作为参考；编辑器版本、扩展和快捷键可能不同，合并时保留已有设置并逐项验证。

#### 步骤2：配置集成终端

**这是什么？**
"集成终端"就是编辑器下方那个黑框框（或白框框），用来运行命令的地方。配置它就是告诉编辑器："用哪个翻译器来执行我的命令"。

**什么时候需要配置？**
先打开编辑器自带终端，运行 `claude --version`。能用就不必重写终端配置；需要更换 shell 或调整显示时，再按下面的设置添加相应项目。

**操作方法：**
打开设置（`Ctrl/Cmd + ,`），从命令面板打开 **Preferences: Open User Settings (JSON)**，把需要的字段合并到现有对象中。下面指定 `pwsh.exe` 的部分要求先安装 PowerShell 7；只有系统自带 PowerShell 5.1 时，保留已可用的终端配置，不要照抄这个 profile。

```json
{
  // ==========================================
  // 终端配置（告诉编辑器用哪个"翻译器"）
  // ==========================================

  // Windows用户 → 用PowerShell（Windows推荐的命令行工具）
  "terminal.integrated.defaultProfile.windows": "PowerShell",

  // Mac用户 → 用zsh（Mac 2019年后的默认Shell，比bash更现代）
  "terminal.integrated.defaultProfile.osx": "zsh",

  // Linux用户 → 用bash（Linux通用Shell）
  "terminal.integrated.defaultProfile.linux": "bash",

  // ==========================================
  // PowerShell 7配置（Windows推荐）
  // ==========================================
  // 指定用PowerShell 7而不是老版PowerShell 5.1
  // PowerShell 7功能更强大，跨平台，推荐使用
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell",
      "path": "pwsh.exe"  // pwsh.exe = PowerShell 7
    }
  },

  // ==========================================
  // 终端外观配置（让终端更好看）
  // ==========================================
  "terminal.integrated.fontFamily": "Menlo, Monaco, 'Courier New', monospace",
  "terminal.integrated.fontSize": 13,  // 13号字体，比默认稍大，更舒适

  // ==========================================
  // Claude Code专用配置
  // ==========================================
  // 让CLAUDE.md文件有Markdown语法高亮
  "files.associations": {
    "CLAUDE.md": "markdown"
  },

  // ==========================================
  // 自动保存（强烈推荐！）
  // ==========================================
  "files.autoSave": "afterDelay",  // 编辑后自动保存，不怕忘记保存丢失改动
  "files.autoSaveDelay": 1000      // 延迟1秒（1000毫秒）保存
}
```

> 💡 **配置说明（小白版）**：
>
> | 配置项                     | 人话翻译            | 为啥要配               |
> | -------------------------- | ------------------- | ---------------------- |
> | `defaultProfile.windows` | Windows用PowerShell | 确保命令能正常运行     |
> | `defaultProfile.osx`     | Mac用zsh            | Mac最新系统的默认Shell |
> | `defaultProfile.linux`   | Linux用bash         | Linux通用Shell         |
> | `profiles.windows`       | 用PowerShell 7      | 比老版更强大           |
> | `fontSize: 13`           | 终端字体13号        | 比默认大一点，看着舒服 |
> | `CLAUDE.md`              | 识别Claude配置文件  | 有语法高亮，好编辑     |
> | `autoSave`               | 自动保存            | 不怕忘记保存丢失改动   |
>
> **生活类比**：把电脑想象成一家国际餐厅
>
> - **中文服务员** = zsh（Mac专用）
> - **英文服务员** = PowerShell（Windows专用）
> - **通用服务员** = bash（大家都能用）
>
> 这个配置就是在告诉餐厅："我需要中文服务员/英文服务员来服务"。

**验证配置是否生效：**

1. 按 ``Ctrl + ` ``（Esc键下面那个键）打开终端
2. 运行验证命令：

**Windows用户：**

```powershell
# 查看PowerShell版本
$PSVersionTable.PSVersion
# 预期输出：显示版本号，比如 7.4.0
```

**Mac/Linux用户：**

```bash
# 查看当前Shell类型
echo $SHELL
# 预期输出Mac：/bin/zsh
# 预期输出Linux：/bin/bash
```

如果显示正确 → ✅ 配置成功！

#### 步骤3：创建VS Code任务（可选但推荐）

**这是什么？**
"任务（Task）"就是把常用命令做成一键按钮。比如"启动Claude Code"、"审查当前文件"这些操作，不用每次手敲命令，点一下就能执行。

**为什么要创建？**
类比：不用任务 = 每次都要手动打开微信；用任务 = 桌面有微信图标，一键打开。

**操作方法：**
在项目根目录创建 `.vscode/tasks.json`：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Claude Code: 启动交互模式",
      "type": "shell",
      "command": "claude",
      "problemMatcher": [],
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": true,
        "panel": "dedicated",
        "clear": true
      }
    },
    {
      "label": "Claude Code: 审查当前文件",
      "type": "shell",
      "command": "claude \"Review ${relativeFile} and suggest improvements\"",
      "problemMatcher": []
    },
    {
      "label": "Claude Code: 解释当前文件",
      "type": "shell",
      "command": "claude \"Explain what ${relativeFile} does\"",
      "problemMatcher": []
    },
    {
      "label": "Claude Code: 生成测试",
      "type": "shell",
      "command": "claude \"Generate unit tests for ${relativeFile}\"",
      "problemMatcher": []
    }
  ]
}
```

**使用任务：**

**方法1：命令面板（推荐）**

1. 按 `Ctrl/Cmd + Shift + P`（打开命令面板）
2. 输入：`Tasks: Run Task`
3. 选择你要运行的任务，比如"Claude Code: 启动交互模式"

**方法2：菜单操作**
点击菜单 `Terminal → Run Task...`

> 💡 **任务说明**：
>
> | 任务名称     | 作用                 | 使用场景         |
> | ------------ | -------------------- | ---------------- |
> | 启动交互模式 | 一键启动Claude Code  | 开始编程前       |
> | 审查当前文件 | 让Claude检查代码质量 | 写完代码想优化时 |
> | 解释当前文件 | 让Claude解释代码逻辑 | 看不懂别人代码时 |
> | 生成测试     | 自动生成单元测试     | 需要写测试时     |

#### 步骤4：配置快捷键（可选）

**这是什么？**
给刚才创建的"任务"绑定键盘快捷键，比如按 `Ctrl+Shift+C` 就能启动Claude Code，连菜单都不用点。

**为什么要配置？**
更快！按一个键盘快捷键 vs 打开菜单找任务，哪个快？当然是快捷键！

**操作方法：**
从命令面板打开 **Preferences: Open Keyboard Shortcuts (JSON)**，把下面的绑定加入用户 `keybindings.json`。它不放在项目 `.vscode/keybindings.json` 中；已有绑定要合并，并先检查快捷键冲突。

```json
[
  {
    "key": "ctrl+shift+c",  // 快捷键：Ctrl+Shift+C
    "command": "workbench.action.tasks.runTask",
    "args": "Claude Code: 启动交互模式"  // 执行哪个任务
  },
  {
    "key": "ctrl+shift+r",  // 快捷键：Ctrl+Shift+R
    "command": "workbench.action.tasks.runTask",
    "args": "Claude Code: 审查当前文件"
  },
  {
    "key": "ctrl+shift+e",  // 快捷键：Ctrl+Shift+E
    "command": "workbench.action.tasks.runTask",
    "args": "Claude Code: 解释当前文件"
  }
]
```

> 💡 **快捷键说明**：
>
> | 快捷键           | 执行任务        | 记忆方法    |
> | ---------------- | --------------- | ----------- |
> | `Ctrl+Shift+C` | 启动Claude Code | C = Claude  |
> | `Ctrl+Shift+R` | 审查当前文件    | R = Review  |
> | `Ctrl+Shift+E` | 解释当前文件    | E = Explain |
>
> ⚠️ **Mac用户**：把 `ctrl` 改成 `cmd` 即可

### 7.2 Cursor 编辑器集成

**Cursor是什么？**
Cursor是基于VS Code魔改的AI编辑器，自带AI助手。和Claude Code配合使用，效果更好！

**Cursor独特优势：**

- ✓ 内置AI对话面板（不用切换工具）
- ✓ AI代码补全（边写边提示）
- ✓ 与Claude Code互补而非冲突（两个AI工具不打架）

> 💡 **复用配置时**：Cursor 支持常见的 VS Code 终端和 Tasks 设置，但具体扩展、设置入口和快捷键仍要在当前编辑器中验证。先确认 `claude --version` 能在集成终端运行，再按需加 Tasks。

Cursor界面和VS Code略有不同，打开设置JSON文件的方法如下：

#### 方法 A：用命令面板打开（最推荐）

**步骤：**

1. 在 Cursor 按 `Ctrl + Shift + P`（打开命令面板）
2. 输入：`open user settings`（不区分大小写）
3. 选择：**Preferences: Open User Settings (JSON)** 或中文：**首选项: 打开用户设置(JSON)**
4. 自动打开 `settings.json` 文件

**打开快捷键配置同理：**

- 输入：`open keyboard shortcuts`
- 选择：**Preferences: Open Keyboard Shortcuts (JSON)** 或中文：**首选项: 打开键盘快捷方式(JSON)**

---

#### 方法 B：直接打开文件路径（万能方法）

如果方法A找不到菜单（Cursor版本不同可能有差异），用这个方法**通常有效**：

**步骤：**

1. 在 Cursor 按 `Ctrl + P`（快速打开文件）
2. 粘贴下面对应你系统的路径，按回车：

**Windows系统：**

```
C:\Users\你的用户名\AppData\Roaming\Cursor\User\settings.json
```

**Mac系统：**

```
~/Library/Application Support/Cursor/User/settings.json
```

> ⚠️ **注意**：把"你的用户名"改成你电脑的实际用户名！比如你的用户名是 `admin`，路径就是 `C:\Users\admin\AppData\...`

---

同一项目中的 `.vscode/tasks.json` 可以继续作为任务配置，不要为了 Cursor 把整个 `.vscode` 复制或改名成 `.cursor`。用户设置和快捷键属于各编辑器自己的配置；在 Cursor 中分别打开对应 JSON 文件，合并实际需要的字段。

**推荐工作流：**

| 场景         | 使用工具     | 原因             |
| ------------ | ------------ | ---------------- |
| 快速代码补全 | Cursor内置AI | 快速，无需切换   |
| 复杂逻辑重构 | Claude Code  | 更强推理能力     |
| 代码审查     | Claude Code  | 更全面上下文理解 |
| 生成测试     | Claude Code  | 更完整测试覆盖   |

### 7.3 JetBrains IDEs 集成

适用于WebStorm、PyCharm、IntelliJ IDEA等。

#### 步骤1：配置External Tools

1. 打开设置：

   - Windows/Linux: `File → Settings → Tools → External Tools`
   - macOS: `Preferences → Tools → External Tools`
2. 点击 `+` 添加新工具：

**Tool 1：Claude Code交互模式**

| 字段              | 值                   |
| ----------------- | -------------------- |
| Name              | Claude Code          |
| Program           | claude               |
| Arguments         | （留空）             |
| Working directory | `$ProjectFileDir$` |

**Tool 2：审查当前文件**

| 字段              | 值                                               |
| ----------------- | ------------------------------------------------ |
| Name              | Claude: Review File                              |
| Program           | claude                                           |
| Arguments         | `"Review $FilePath$ and suggest improvements"` |
| Working directory | `$ProjectFileDir$`                             |

#### 步骤2：配置快捷键

1. `Settings → Keymap`
2. 搜索 `External Tools`
3. 右键 → `Add Keyboard Shortcut`
4. 设置快捷键（如 `Ctrl+Shift+C`）

---

## 第八部分：故障排查

### 8.1 平台特定问题

#### Windows平台

**问题1：PowerShell 执行策略限制 npm 启动脚本**

如果错误提到 `npm.ps1` 或 `claude.ps1`，PowerShell 的执行策略可能在阻止 npm 创建的脚本启动器。原生 `claude.exe` 与 `irm ... | iex` 安装方式不受这个脚本文件策略影响，不要把该报错归因于原生二进制。

先用 `npm.cmd` / `claude.cmd` 验证对应 npm 启动器，或选择原生安装。如果确实需要改变自己的脚本策略，并且组织允许，可以按[官方排障说明](https://code.claude.com/docs/en/troubleshoot-install#running-scripts-is-disabled-on-this-system)设置 `RemoteSigned -Scope CurrentUser`；这个用户级设置通常不需要管理员权限。

**问题2：安全软件阻止或隔离文件**

先查看安全软件的检测记录、文件路径和来源，不要直接判定为误报。确认安装来自官方入口，并按[官方签名与完整性说明](https://code.claude.com/docs/en/setup#binary-integrity-and-code-signing)核对；公司电脑交给管理员处理。不要为了完成安装把整个 `.local/bin` 加入排除列表或关闭实时保护。

**问题3：命令找不到**

```bash
# 症状
'claude' 不是内部或外部命令
# 或
claude: The term 'claude' is not recognized as a name of a cmdlet
```

**原因**：原生安装目录未添加到PATH

**解决方案（手动添加 PATH 环境变量）：**

Claude Code 原生安装后，可执行文件通常位于以下路径：
- **原生安装**：`C:\Users\<你的用户名>\.local\bin\`
- **NPM 安装**：`C:\Users\<你的用户名>\AppData\Roaming\npm\`

**方法1：通过系统设置（图形界面，推荐新手用）**

1. 按下 `Win + R` 打开"运行"对话框
2. 输入 `sysdm.cpl`，按回车，打开"系统属性"
3. 点击 **"高级"** 选项卡
4. 点击底部的 **"环境变量"** 按钮
5. 在 **"用户变量"** 区域（上半部分），找到名为 `Path` 的变量，双击它
6. 在弹出的"编辑环境变量"窗口中，点击 **"新建"**
7. 输入 Claude Code 的安装路径：
   - 原生安装填：`%USERPROFILE%\.local\bin`
   - NPM 安装填：`%APPDATA%\npm\`
8. 点击 **"确定"** 保存所有对话框
9. **关闭并重新打开所有终端窗口**（重要！已打开的终端不会自动刷新 PATH）

**方法2：通过 PowerShell 命令**

```powershell
# 查看当前用户 PATH
[System.Environment]::GetEnvironmentVariable('Path', 'User')

# 添加 Claude Code 到 PATH（原生安装路径）
$currentPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$newPath = "$currentPath;$env:USERPROFILE\.local\bin"
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')

# 如果是 NPM 安装，改用这个路径
# $newPath = "$currentPath;$env:APPDATA\npm"

# 重启 PowerShell 后验证
claude --version
```

**方法3：快捷方式（Win+R）**

```
Win+R → 输入 sysdm.cpl → 回车 → 高级 → 环境变量 → 用户变量的 Path → 编辑 → 新建 → 粘贴路径 → 确定
```

> ⚠️ **注意**：修改 PATH 后，必须**重新打开终端**才能生效！已经打开的 PowerShell/CMD 窗口用的还是旧的 PATH，必须关掉重开。

#### macOS平台

**问题1：命令找不到但已安装**

```bash
# 症状
claude: command not found

# 原因可能是安装目录未在当前终端 PATH 中；以安装器提示和实际路径为准

# 解决方案：检查原生安装位置
ls ~/.local/bin/claude
# 或
ls /usr/local/bin/claude

# 如果文件存在，添加到PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**问题2：macOS Gatekeeper阻止**

先核对下载来源、实际发布文件及其代码签名。Claude Code 的 macOS 官方二进制有签名和公证说明，见[官方平台签名文档](https://code.claude.com/docs/en/setup#platform-code-signatures)。文件来源不明或签名异常时不要通过移除隔离属性继续运行；组织设备按管理员要求排查。

---

### 8.2 原生安装常见问题

**问题1：安装脚本下载失败**

```bash
# 症状
curl: (7) Failed to connect to claude.ai port 443
```

**原因**：网络无法访问claude.ai

**解决方案：**

```bash
# 方案1：配置代理
export https_proxy=http://127.0.0.1:7890
curl -fsSL https://claude.ai/install.sh | bash

# 方案2：使用包管理器（Homebrew/WinGet）
brew install --cask claude-code
# 或
winget install Anthropic.ClaudeCode

# 方案3：按官方排障页面选其他 CLI 安装方法
# https://code.claude.com/docs/en/troubleshoot-install
# claude.ai/download 是图形应用入口，不要把 Desktop 安装包当 CLI 安装包
```

**问题2：安装版本不是最新**

```bash
claude --version
# 显示版本较旧
```

**解决方案：**

```bash
# 原生安装支持自动更新，运行：
claude update

# 或重新运行安装脚本
curl -fsSL https://claude.ai/install.sh | bash
```

**问题3：检测到旧的npm安装**

```bash
claude doctor
# 查看安装类型与启动路径，确认是否仍从 npm 全局目录启动
```

**解决方案：**

```bash
# 运行迁移命令
claude install

# 安装后用 claude doctor 检查实际启动路径
# 如果还存在旧的 npm 安装，确认新版本可用后再按附录卸载旧副本
```

### 8.3 网络连接问题

**问题：访问所用服务超时**

先确定当前认证和端点。`ping` 用的是 ICMP，超时不能证明 HTTPS API 不可用；对 Anthropic API 可以在 shell 做下面的只读检查：

```bash
curl -I https://api.anthropic.com
```

Windows PowerShell 可用 `curl.exe -I https://api.anthropic.com`。收到 HTTP 错误码也说明服务器有响应，但不证明你有模型资格或认证成功。订阅登录和其他提供商还需检查各自端点，参照[官方网络配置](https://code.claude.com/docs/en/network-config)。

组织要求代理时，使用管理员提供的实际 HTTP/HTTPS 代理地址，再启动新会话；`127.0.0.1:7890` 只是示例，只有本机确有代理监听才可使用。不要仅因一次超时就改系统 DNS、绕过服务地区条件或改用未经确认的中转服务。

**问题2：SSL证书错误**

**症状：**

```bash
claude
# Error: unable to verify the first certificate
```

**解决方案：**

```powershell
# Windows：通过Windows Update更新根证书
Start-Process ms-settings:windowsupdate

# macOS：系统自动维护，确保系统保持最新
# 系统设置 → 通用 → 软件更新

# Linux：更新CA证书
sudo apt update && sudo apt upgrade ca-certificates
# 或
sudo yum update ca-certificates
```

**问题3：API连接超时**

**症状：**

```bash
claude
# Error: Connection timeout after 30000ms
```

**解决方案：**

```bash
# 1. 先确认是网络还是服务端问题
curl -I https://api.anthropic.com

# 2. 如果 curl 也超时，按上面「无法访问 api.anthropic.com」的代理配置步骤重试

# 3. 如果 curl 正常但 claude 仍超时，检查是否有残留的代理环境变量
env | grep -i proxy

# 4. 企业网络下确认公司防火墙放通了 api.anthropic.com 的 443 端口
```

### 8.4 API Key 配置问题

这一节只排查选择了 API Key 的路径。订阅或 Console 浏览器登录用户先运行 `claude auth status --text`，不要因环境变量为空就创建或更换 API Key。

**问题：环境变量未生效**

只检查是否设置，不回显凭据。在 Bash / Zsh 中运行：

```bash
if [ -n "$ANTHROPIC_API_KEY" ]; then echo "API Key 已配置"; else echo "API Key 未配置"; fi
```

Windows PowerShell 中运行：

```powershell
[bool]$env:ANTHROPIC_API_KEY
```

若当前进程没有值，回到第4.3节检查你实际使用的 shell 配置。修改用户级永久变量后重新打开终端；已有 Claude Code 进程不会自动读取 shell 后续变更。

**问题：Key无效或过期**

```json
{
  "error": {
    "type": "authentication_error",
    "message": "invalid x-api-key"
  }
}
```

**解决方法：**

1. 登录 console.anthropic.com
2. Settings → API Keys
3. 检查Key是否被删除或禁用
4. 如果无效，创建新Key
5. 更新环境变量

**问题3：Key格式错误**

**症状**：Key看起来不完整或有空格

**检查方法：**

确认复制时没有前后空格、换行或缺字，并核对凭据来自你实际使用的服务。不要用固定 `api03` 前缀或“约95字符”判断所有 Key；第三方凭据格式也可能不同。只检查存在性和复制完整性，不打印完整值。仍报认证错误时，到相应提供方检查凭据状态或按官方登录排障处理。

### 8.5 终端相关问题

**问题：中文乱码（Windows）**

```bash
# 临时切换到UTF-8
chcp 65001

# 永久设置
reg add HKCU\Console /v CodePage /t REG_DWORD /d 65001 /f
```

**PowerShell中文显示：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**问题3：复制粘贴不工作**

不同终端的复制粘贴快捷键不同：

**Windows Terminal：**

- 右键选中文本自动复制
- `Ctrl+Shift+C` 复制
- `Ctrl+Shift+V` 粘贴

**Windows CMD：**

- 右键 → 标记 → 选中文本 → 回车复制
- 右键粘贴

**macOS Terminal：**

- `Cmd+C` 复制
- `Cmd+V` 粘贴

**Linux终端：**

- `Ctrl+Shift+C` 复制
- `Ctrl+Shift+V` 粘贴
- 或鼠标中键粘贴（选中即复制）

**问题4：命令历史记录丢失**

**症状**：重启终端后之前输入的命令无法通过上下箭头找回

**PowerShell 7配置：**

```powershell
# PowerShell 7默认已配置历史记录
# 查看历史记录位置
$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\

# 增强历史记录功能（编辑PowerShell配置文件）
notepad $PROFILE

# 添加以下内容：
Set-PSReadLineOption -HistorySearchCursorMovesToEnd
Set-PSReadLineOption -MaximumHistoryCount 10000
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
```

**Bash/Zsh配置（macOS/Linux）：**

```bash
# 确认历史记录文件
echo $HISTFILE
# 应该是~/.bash_history或~/.zsh_history

# 如果为空，添加到配置
# Zsh用户（编辑~/.zshrc）：
echo 'export HISTFILE=~/.zsh_history' >> ~/.zshrc
echo 'export HISTSIZE=10000' >> ~/.zshrc
echo 'export SAVEHIST=10000' >> ~/.zshrc
source ~/.zshrc

# Bash用户（编辑~/.bashrc）：
echo 'export HISTFILE=~/.bash_history' >> ~/.bashrc
echo 'export HISTSIZE=10000' >> ~/.bashrc
echo 'export HISTFILESIZE=20000' >> ~/.bashrc
source ~/.bashrc
```

**验证历史记录：**

```powershell
# PowerShell 7
Get-History

# Bash/Zsh
history | tail -20
```

---

## 第九部分：学员常见问题FAQ


> 💡 **本节收录**：直播课程中学员最常问的20个问题，帮你避开90%的坑！

### 9.1 安装与配置类

#### Q1：运行 `code --version` 报错说找不到命令？

**A1：先分清命令属于哪个程序，再检查它是否在 PATH 中。**

- `code --version` 检查 VS Code；`cursor --version` 检查 Cursor；`claude --version` 检查 Claude Code。
- 命令不由你当前打开哪个编辑器决定。在 Cursor 终端里也可能运行 `code`，前提是 VS Code 的 CLI 已安装并加入 PATH。
- 要打开 IDE 配置而相应命令不可用时，可先用编辑器菜单或命令面板；安装 Claude Code 本身不要求 `code` 可用。

#### Q2：找不到settings.json文件在哪儿？

**A2：不同编辑器位置不同！**

**Cursor位置：**

- Windows: `C:\Users\你的用户名\AppData\Roaming\Cursor\User\settings.json`
- Mac: `~/Library/Application Support/Cursor/User/settings.json`

**VS Code位置：**

- Windows: `C:\Users\你的用户名\AppData\Roaming\Code\User\settings.json`
- Mac: `~/Library/Application Support/Code/User/settings.json`

**快速打开方法：**

1. 按 `Ctrl/Cmd + Shift + P`
2. 输入：`open user settings json`
3. 选择：`Preferences: Open User Settings (JSON)`

#### Q3：配置后还是报错，怎么办？

**A3：按照这个检查清单逐项排查：**

```
□ settings.json文件保存了吗？（看文件名有没有*号）
□ JSON格式正确吗？（大括号、逗号、引号都对吗）
□ 重启了终端吗？（配置需要重启终端才生效）
□ 重启了编辑器吗？（有时需要完全重启）
```

**还是不行？** 把错误信息截图，群里问老金！

#### Q4：zsh、PowerShell、bash 有什么区别？我该用哪个？

**A4：它们都是Shell（命令行翻译器），选对应你系统的就行！**

| 操作系统          | 推荐Shell  | 为什么             |
| ----------------- | ---------- | ------------------ |
| **Windows** | PowerShell | 系统自带，功能强大 |
| **Mac**     | zsh        | 2019年后的系统默认 |
| **Linux**   | bash       | 通用标准           |

先用编辑器当前能打开的 shell；要更换时，确认目标 shell 已安装。第7.1节中的 PowerShell 7 profile 依赖 `pwsh.exe`，不能替系统自动安装它。

#### Q5：怎么知道我现在用的是哪个Shell？

**A5：根据当前终端检查。**

- Windows PowerShell：运行 `$PSVersionTable.PSVersion`，查看实际 PowerShell 版本。
- Bash / Zsh：`echo "$SHELL"` 通常显示账号的默认登录 shell；如果你临时切换过 shell，再用 `ps -p $$ -o comm=` 检查当前进程。

PowerShell 中的 `$SHELL` 通常没有对应值，不能期待它返回 `powershell`。

---

### 9.2 启动与使用类

#### Q6：怎么启动Claude Code？

**A6：有2种方式，推荐第1种！**

**方式1：终端命令启动（推荐）**

```bash
# 进入项目目录
cd /你的项目路径

# 启动Claude Code
claude
```

**方式2：IDE快捷键启动**

- 配置tasks.json（见第7.1节）
- 按 `Ctrl/Cmd + Shift + P` → 选 `Tasks: Run Task` → 选 `Claude Code: 启动交互模式`

#### Q7：启动后看到什么才算成功？

**A7：看到这个界面就成功了：**

```
╭─────────────────────────────────────────╮
│  Welcome to Claude Code v2.1           │
│  • Type /help to see available commands │
╰─────────────────────────────────────────╯

You: █
```

关键要素：

- ✅ 显示欢迎信息
- ✅ 显示版本号（v2.1+）
- ✅ 显示工作目录
- ✅ 有输入光标 `█`

#### Q8：`--dangerously-skip-permissions` 是什么？我该用吗？

**A8：这个参数跳过权限询问，新手别用！**

先看会话底部的权限模式。当前交互会话可能默认使用 auto，已有允许规则也会影响是否询问；不加参数不等于每次都要确认。

需要手动查看权限提示时，从 `claude --permission-mode default` 的 Manual 开始。减少常规询问时，检查 auto、acceptEdits 或有限的 allow 规则。只有明确建立文件和网络隔离的受控环境才考虑 bypass；“学了两周”和“个人小项目”都不能替代隔离。详细说明见第6.5.2节。

#### Q9：启动Claude Code后怎么退出？

**A9：两种方法：**

**方法1：命令退出**

```bash
/exit
```

**方法2：快捷键退出**

- 按 `Ctrl + C` 两次
- 或 `Ctrl + D`

#### Q10：能同时打开多个Claude Code吗？

**A10：可以！每个终端窗口都能启动一个Claude Code实例。**

**使用场景：**

- 窗口1：处理前端代码
- 窗口2：处理后端代码
- 窗口3：运行测试

---

### 9.3 配置文件类

#### Q11：tasks.json文件放在哪里？

**A11：放在项目根目录的 `.vscode` 文件夹里！**

**完整路径示例：**

```
你的项目/
├── .vscode/
│   └── tasks.json  ← 放这里
├── src/
└── package.json
```

**创建步骤：**

1. 在项目根目录创建 `.vscode` 文件夹（如果没有）
2. 在 `.vscode` 里创建 `tasks.json` 文件
3. 复制第7.1节的配置粘贴进去
4. 保存

#### Q12：配置后快捷键不生效？

**A12：检查这些：**

```
□ keybindings.json保存了吗？
□ 快捷键有冲突吗？（换个组合试试）
□ 重启编辑器了吗？
```

**查看快捷键冲突：**

1. 按 `Ctrl/Cmd + K, Ctrl/Cmd + S`（打开快捷键设置）
2. 搜索你配置的快捷键
3. 看是否有其他命令占用

#### Q13：粘贴配置后报JSON错误？

**A13：大多数情况是格式问题！**

**常见错误：**

| 错误                  | 原因          | 解决                         |
| --------------------- | ------------- | ---------------------------- |
| `Unexpected token`  | 多了/少了逗号 | 最后一项配置不要逗号         |
| `Invalid character` | 中文引号      | 把 `""` 改成 `""`        |
| `Unexpected end`    | 大括号不匹配  | 数数 `{` 和 `}` 是否相等 |

**快速检查：**

- 用在线工具检查JSON格式：https://jsonlint.com/
- 复制你的配置粘贴进去，它会告诉你哪里错了

---

### 9.4 权限与安全类

#### Q14：Claude Code会偷偷上传我的代码吗？

**A14：Claude Code 会把完成任务所需的上下文发给模型服务，包括它读取的相关文件、对话和工具结果；这不一定仅限你逐个点名的文件。**

**工作原理：**

1. 你问问题 → Claude Code读取相关文件
2. 把任务所需的上下文发给当前配置的模型提供商处理
3. 收到AI回复后显示给你

**隐私保护：**

- 先确认当前服务提供方和数据使用政策，再决定哪些内容可以交给模型。
- 用权限规则限制文件工具，并为 shell、MCP 等其他访问路径单独设置边界。
- 项目规则和忽略文件有不同用途，不能把它们当成数据隔离保证。

#### Q15：我不想让Claude Code访问某些文件，怎么办？

**A15：在 `.claude/settings.json` 中配置权限拒绝规则，并核对其他工具的访问能力。**

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./**/*.key)",
      "Read(./secrets/**)",
      "Read(./config/production.json)"
    ]
  }
}
```

`.gitignore` 控制 Git 跟踪和部分搜索行为，不是保密边界；官方没有把 `.claudeignore` 定义为统一的文件访问控制入口。`Read` 拒绝规则限制相应文件工具，仍须审查 shell、MCP、hooks 等其他读取路径。需要严格隔离时，把敏感文件留在执行环境之外或结合 OS sandbox。

---

### 9.5 网络与性能类

#### Q16：Claude Code响应很慢，怎么优化？

**A16：检查网络和上下文大小！**

先看 `/context`，确认是不是上下文过大，再核对当前模型、服务状态和网络。到无关的新任务可以用 `/clear`，同一任务需要保留重点时用 `/compact`。

网络检查使用实际服务的 HTTPS 端点，不能用 `ping` 延迟阈值保证模型响应速度。减少无关材料时明确任务范围，并把生成目录加入合适的搜索忽略配置；官方没有把 `.claudeignore` 定义为统一的文件访问或上下文控制入口。代理只在你的网络实际需要时配置。

#### Q17：国内网络访问Anthropic API很慢？

**A17：配置代理！**

**临时代理（当前终端生效）：**

```bash
# macOS/Linux
export HTTPS_PROXY=http://127.0.0.1:7890

# Windows PowerShell
$env:HTTPS_PROXY="http://127.0.0.1:7890"
```

**永久代理（推荐）：**
在 `~/.zshrc` 或 `~/.bashrc` 添加：

```bash
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
```

---

### 9.6 错误信息类

#### Q18：启动时报错 `claude: command not found`？

**A18：Claude Code没安装或PATH未配置！**

**解决步骤：**

1. 检查是否安装：

   ```bash
   claude --version
   ```

2. 如果提示命令找不到：

   **macOS/Linux:**

   ```bash
   # 检查安装位置
   ls ~/.local/bin/claude

   # 如果存在，添加到PATH
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

   **Windows:**

   ```powershell
   # 检查安装位置
   Test-Path "$env:USERPROFILE\.local\bin\claude.exe"

   # 如果返回 True，手动添加到 PATH
   # 系统设置 → 环境变量 → 用户变量的 Path → 添加：
   # %USERPROFILE%\.local\bin
   ```

3. 如果确实没安装：

   **macOS/Linux:**

   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

   **Windows:**

   ```powershell
   irm https://claude.ai/install.ps1 | iex
   ```

#### Q19：启动时报错 `API key not found`？

**A19：先看实际认证，不要仅凭旧报错文字断定缺环境变量。**

```bash
claude auth status --text
```

订阅或 Console 浏览器登录不必设置 `ANTHROPIC_API_KEY`。选择 API Key 路径却未配置时，回到第四部分处理；已经设置却报错时，检查凭据状态、当前提供商和残留配置。不要把完整密钥输出到终端。

#### Q20：我之前用npm安装过Claude Code，怎么办？

**A20：官方提供了迁移命令！**

```bash
# 一键迁移到原生版本
claude install
```

`claude install` 安装原生副本。随后运行下面的只读检查，确认实际启动路径和新版本；旧 npm 副本是否还在，要以诊断结果为准，不能保证自动卸载。

**验证迁移成功：**

```bash
claude --version
claude doctor
# 核对版本、安装类型与实际启动路径
```

**确认原生副本已经可用后，需要时再卸载旧 npm 副本：**

```bash
npm uninstall -g @anthropic-ai/claude-code
```

#### Q21：原生安装和npm安装有什么区别？

**A21：简单来说，原生安装更省心；npm 安装仍然是官方支持的标准路径。**

| 对比项         | 原生安装 ⭐ | npm标准安装 |
| -------------- | ----------- | ----------------- |
| 需要Node.js    | ❌ 不需要    | ✅ 需要 22+      |
| 安装时间       | ⏱️ 3-5分钟  | ⏱️ 30-40分钟    |
| 自动更新       | 默认开启，可配置 | 默认开启；全局目录不可写时需处理权限 |
| PATH配置       | 按安装器提示核对用户目录 | 核对 npm 全局 bin 目录 |
| 安装管理       | 原生安装器管理 | npm 管理，需允许 optional dependencies |

#### Q22：原生安装可以离线使用吗？

**A22：常规 Anthropic 或云提供商接入需要联网。**

原生安装省去 Node.js 依赖，不会把 Claude 模型安装到本机。安装包下载、登录、模型请求与更新都有各自网络需求。Ollama 提供[单独的 Claude Code 集成](https://docs.ollama.com/integrations/claude-code)；只有已下载的本地模型、相应硬件和不依赖外网的工具链都就绪时，才可以讨论离线运行，不能把云模型或整个 Claude Code 功能都算作离线可用。

#### Q23：原生安装会占用多少空间？

**A23：按实际安装目录和保留版本检查。**

原生启动器位于 `~/.local/bin`，版本文件位于 `~/.local/share/claude`；用户设置和会话还会占用 `~/.claude`。具体大小随平台、版本和记录变化，不能保证固定100–200MB或比npm节省50%。

#### Q24：我电脑上已经有Node.js了，还需要卸载吗？

**A24：不需要！可以共存。**

- ✅ Node.js可以继续用于其他项目
- ✅ Claude Code原生安装不影响Node.js
- ✅ 如果你不用Node.js做开发，可以考虑卸载节省空间

#### Q25：原生安装会自动更新吗？可以关闭吗？

**A25：默认自动更新，可以关闭。**

**查看更新状态：**

```bash
claude doctor
# 查看 Auto-updates 与最近更新诊断；--version 只显示当前版本
```

**禁用自动更新：**

```bash
# macOS/Linux
export DISABLE_AUTOUPDATER=1

# Windows PowerShell
$env:DISABLE_AUTOUPDATER="1"
```

**手动更新：**

```bash
claude update
# 原生安装手动更新；包管理器安装按对应管理器升级
```

#### Q26：公司电脑安装需要管理员权限吗？

**A26：原生用户目录安装通常不需要管理员权限，Windows 也一样。**

Windows 原生安装写入自己的用户目录，不必以管理员身份运行 PowerShell。Homebrew、WinGet、Linux 包管理器、WSL 启用或组织策略可能有各自的权限要求；遇到权限错误时先确定安装路径和错误来源，不要一律提权。公司设备按管理员的部署要求操作。

#### Q27：安装脚本安全吗？会不会有病毒？

**A27：从官方入口取得脚本，并核对实际发布文件。**

下载脚本可读不等于产品采用开源许可，也不能保证所有平台的脚本和二进制都以同一种方式签名。官方分别说明 macOS / Windows 代码签名以及 Linux 的 manifest 完整性验证；按[官方验证步骤](https://code.claude.com/docs/en/setup#binary-integrity-and-code-signing)检查你的安装方式。

**如果你担心，可以先查看脚本：**

```bash
# 只下载不执行
curl -fsSL https://claude.ai/install.sh
# 阅读后觉得安全再执行
curl -fsSL https://claude.ai/install.sh | bash
```

#### Q28：我的问题不在这里，怎么办？

**A28：这样做：**

1. 运行 `claude --help` 和 `claude doctor` 查看帮助与只读诊断。
2. 需要日志时，用 `claude --debug-file <实际日志路径>` 明确日志位置，再查看错误；不要假定所有版本都写入 `~/.claude/logs/`。
3. 访问[官方排障文档](https://code.claude.com/docs/en/troubleshooting)。
4. 在[官方 GitHub Issues](https://github.com/anthropics/claude-code/issues)搜索类似问题。
5. ✅ 把错误信息截图，在学习群里问老金！

**提问时请提供：**

- 操作系统和版本
- Claude Code版本（`claude --version`）
- 完整错误信息（截图或复制文字）
- 你做了什么操作

---

## 第8.5部分：模型配置（安装后的进阶配置）

> 💡 **本节重点**：装好 Claude Code 后，最重要的进阶配置之一就是选择合适的模型。这一节把模型配置讲透，让你从"会用"升级到"用对"。
>
> ⏱️ **预计时间**：30分钟
>
> **前置条件**：Claude Code 安装成功（完成第五部分）

### 8.5.0 先说结论

Claude Code 现在的模型配置，不只是"选 Sonnet 还是 Opus"。

它已经变成一整套策略层：

- **会话级选择**：`/model`、`--model`
- **默认策略**：`settings.json` 里的 `model`
- **能力限制**：`availableModels`
- **别名映射**：`ANTHROPIC_DEFAULT_*_MODEL`
- **第三方部署重写**：`modelOverrides`
- **推理强度控制**：`/effort`、`effortLevel`
- **长上下文控制**：`sonnet[1m]`、`opus[1m]`

如果你只记一句话：

> `model` 决定"默认选谁"，`availableModels` 决定"能不能选"，`opusplan` 决定"规划和执行是否分模型"。

---

### 8.5.1 当前可用的模型别名

官方文档当前明确给出的别名如下：

| 别名 | 含义 | 适合场景 |
|------|------|----------|
| `default` | 回到系统默认模型，不是具体模型名 | 不想手动管版本时 |
| `best` | 当前最强可用模型，现阶段等价于 `opus` | 直接追求最强效果 |
| `sonnet` | 最新 Sonnet，用于日常编码 | 默认主力 |
| `opus` | 最新 Opus，用于复杂推理 | 架构、疑难问题 |
| `haiku` | 更快更轻量 | 简单任务、快速处理 |
| `sonnet[1m]` | Sonnet + 1M 上下文 | 大项目、长会话 |
| `opus[1m]` | Opus + 1M 上下文 | 超长上下文 + 深度推理 |
| `opusplan` | 规划时用 Opus，执行时切回 Sonnet | 复杂任务又要控成本 |

#### `opusplan` 是什么

这是当前最值得单独掌握的别名之一。

它的行为是：

- **进入 plan mode 时**：用 `opus`
- **进入执行阶段时**：自动切到 `sonnet`

也就是说，它不是单纯"更贵的模型"，而是一种**规划强、执行稳、成本更合理**的混合策略。

适合：

- 复杂重构
- 架构设计
- 需要先规划再执行的任务
- 团队里想把 Opus 用在刀刃上

---

### 8.5.2 模型配置优先级

当前官方口径的优先级，从高到低是：

1. **会话中即时切换**：`/model <alias|name>`
2. **启动参数**：`claude --model <alias|name>`
3. **环境变量**：`ANTHROPIC_MODEL=<alias|name>`
4. **设置文件**：`settings.json` 中的 `model`
5. **新会话的默认值**：`ANTHROPIC_DEFAULT_MODEL=<alias|name>`（v2.1.236+）

> **默认模型补充（核查日：2026-09-14）**：`ANTHROPIC_DEFAULT_MODEL` 用于指定新会话的起始模型；交互式 `/model` 保存的选择仍可覆盖它，并在重启后保留。它与优先级更高的 `ANTHROPIC_MODEL` 不同。组织托管策略还可能限制可选模型，详见[官方模型配置](https://code.claude.com/docs/en/model-config#set-a-default-model-for-new-sessions)。

#### 常见用法

```bash
# 启动时直接用 Opus
claude --model opus

# 会话里切回 Sonnet
/model sonnet
```

```json
{
  "model": "opusplan"
}
```

---

### 8.5.3 effort：思考深度

`/effort` 控制的是**推理强度**，不是换模型。

可用值（v2.1.105-113 起新增 `xhigh`）：

- `low`
- `medium`
- `high`
- **`xhigh`**（推荐 Opus 4.8 默认）
- `max`
- `auto`

| 级别 | 含义 | 适合场景 |
|------|------|----------|
| `low` | 更快、更省 | 简单问答、格式转换 |
| `medium` | 平衡 | 日常编码 |
| `high` | 更深推理 | 复杂调试、架构分析 |
| **`xhigh`** | **深度推理（推荐 Opus 4.8 默认）** | **深度重构、关键决策** |
| `max` | 最深推理 | 极复杂问题，成本最高 |
| `auto` | 回到模型默认 | 不想手动管时 |

**官方建议**：

- **Opus 4.8 用户推荐默认 `xhigh`**
- 先在当前模型上查看支持等级；例如官方 effort 支持列表没有列 Haiku，不能假定它也接受 low / medium
- `max` 只在确实需要时开
- 如果只是偶发一次深推理，不一定非要改全局设置，可以在 prompt 中写 `ultrathink`

**配置方式**：

- `/effort low|medium|high|xhigh|max|auto`
- `/effort` 不带参数弹出交互式滑块
- `/model` 面板里调节
- `claude --effort xhigh`
- `CLAUDE_CODE_EFFORT_LEVEL=xhigh`
- `settings.json` 中的 `effortLevel`
- skill / subagent frontmatter 里的 `effort`

---

### 8.5.4 1M 上下文怎么用

现在 `Opus 4.8` 和 `Sonnet 5` 都支持 1M 上下文，但是否可见、是否默认可用，取决于计划和部署方式。

#### 最简单的用法

```bash
/model opus[1m]
/model sonnet[1m]
```

或者：

```bash
/model claude-opus-4-8[1m]
```

#### 什么情况下该开 1M

适合：

- monorepo
- 很长的多轮会话
- 一次性理解大型代码库
- 需要大规模跨文件关联分析

不适合：

- 小项目
- 只改 1-2 个文件
- 你更在乎速度和成本

#### 关闭 1M

如果团队不希望出现 1M 选项，可以设置：

```bash
CLAUDE_CODE_DISABLE_1M_CONTEXT=1
```

---

### 8.5.5 团队治理：`availableModels`、默认模型、别名映射

#### `availableModels`

如果你是团队管理员，想限制“用户能选什么”，可以在组织托管设置中配置 `availableModels`。下面是字段示例；普通用户或项目文件里的列表不能当作不可绕过的组织约束。

```json
{
  "availableModels": ["sonnet", "haiku"]
}
```

它的作用是：

- 限制 `/model`
- 限制 `--model`
- 限制 `ANTHROPIC_MODEL`
- 限制 Config 工具中的模型切换

#### 注意：`model` 不是强制锁定

`model` 只是**会话启动时默认选哪个**，并不代表用户不能换。

如果你要真正治理模型体验，通常要组合这三类配置：

- `model`
- `availableModels`
- `ANTHROPIC_DEFAULT_SONNET_MODEL / OPUS / HAIKU`

---

### 8.5.6 第三方部署与 `modelOverrides`

如果你跑的是：

- Bedrock
- Vertex AI
- Foundry

就不要只写别名，还要考虑**模型版本绑定**。

#### 为什么需要 `modelOverrides`

因为第三方平台上，Claude Code 看到的是 Anthropic 的模型 ID，但真正发给平台的，可能要换成：

- ARN
- deployment name
- provider-specific model ID

#### 典型配置

```json
{
  "modelOverrides": {
    "claude-opus-4-8": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-sonnet-5": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

用在：

- 企业按版本精确路由
- 不同区域 / 不同成本中心分流
- 防止别名自动飘到新版本

---

### 8.5.7 自定义模型入口

如果你有内部网关或特殊部署，可用：

- `ANTHROPIC_CUSTOM_MODEL_OPTION`
- `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME`
- `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION`

这样可以在 `/model` 里额外加一个选项，而不是替换原有别名。

适合：

- 自研 LLM gateway
- A/B 测试特殊路由
- 内部灰度模型

---

### 8.5.8 推荐配置场景

#### 个人开发者

```json
{
  "model": "sonnet",
  "effortLevel": "medium"
}
```

建议：

- 日常用 `sonnet`
- 架构问题临时切 `opus` 或 `opusplan`
- 遇到超大仓库时再用 `[1m]`

#### 高强度架构 / 重构

```json
{
  "model": "opusplan",
  "effortLevel": "medium"
}
```

建议：

- 默认用 `opusplan`
- 真正卡住时再把 effort 提到 `high`

#### 团队成本控制

```json
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

建议：

- 限掉随手切 `opus`
- 只给必要团队开更强模型

---

### 8.5.9 常见误区

| 误区 | 真相 |
|------|------|
| `model` 就是强制锁模型 | 不是。它只是初始值。 |
| `opusplan` = 永远更贵 | 不完全对。它是"规划用 Opus，执行回 Sonnet"，很多复杂任务反而更划算。 |
| 1M 一定更好 | 不一定。上下文更大不等于响应更快，也不等于更省钱。 |
| effort 越高越好 | 也不对。高 effort 在简单任务上很容易"过度思考"。 |

---

### 8.5.10 实用速查

```bash
# 当前会话直接切模型
/model opus

# 开 1M 上下文
/model sonnet[1m]

# 切高 effort
/effort high

# 启动就用 opusplan
claude --model opusplan
```

---

### 8.5.11 下一步建议

- 想把模型配置纳入团队治理和企业实战：继续看 [企业实战完整指南](./11-企业实战完整指南.md)
- 想跨设备继续本地会话：继续看 [Remote Control完整指南](./12-Remote-Control完整指南.md)
- 想理解 Channels 与计划任务：继续看 [Channels与计划任务完整指南](./13-Channels与计划任务完整指南.md)

---

## 总结与检查清单

### 完成本课后，请确认以下所有项：

**系统要求：**

- [ ] 操作系统和硬件满足第二部分的要求
- [ ] 终端可用（PowerShell / CMD / Terminal / Bash）
- [ ] 磁盘有足够空间，具体占用按实际安装检查

**账号准备：**

- [ ] 已确认所选订阅、Console 或组织服务允许使用 Claude Code
- [ ] `claude auth status --text` 的认证方式符合预期
- [ ] 只有使用 API Key 时才配置并妥善保管凭据

**系统配置：**

- [ ] 终端能正确显示中文
- [ ] 所选服务的登录与模型端点可访问；组织要求代理时已使用实际配置

**Claude Code安装：**

- [ ] Claude Code原生安装成功
- [ ] `claude --version` 显示当前安装版本
- [ ] `claude --help` 显示帮助信息

**功能验证：**

- [ ] 通过基础测试套件
- [ ] 完成Hello World项目
- [ ] IDE集成配置完成（可选）

**全部勾选后即完成准备工作。**

> ⚠️ **2026年更新说明**：本课程现已更新为“原生安装 + npm 标准安装并存”的口径。如果你是从旧版教程过来的，请优先参考本章新的安装路径说明，不要再默认把 npm 视为唯一入口，也不要误以为 Node.js 已被完全移除。

---

## 附录

### A. 常用命令速查

```bash
# Claude Code版本和帮助
claude --version           # 查看当前安装版本
claude --help              # 查看帮助
claude doctor              # 系统诊断

# Claude Code操作
claude                     # 进入交互模式
claude "你的问题"          # 带初始问题进入交互会话
claude -p "问题"           # 打印模式（脚本友好）

# 更新原生安装；包管理器安装用对应管理器升级
claude update

# 查看认证状态，不打印密钥
claude auth status --text

# HTTPS 检查（Windows PowerShell 用 curl.exe）
curl -I https://api.anthropic.com
# 收到HTTP响应不等于认证或模型调用成功

# 配置管理
claude                    # 启动交互会话
# 进入后输入 /config 打开设置；项目配置放在 .claude/settings.json
```

### B. 从npm迁移到原生安装

**如果你之前通过npm安装过Claude Code，请按以下步骤迁移：**

**步骤1：检查当前安装方式**

```bash
claude doctor
# 核对安装类型和启动路径；npm 安装仍受支持，迁移是可选的
```

**步骤2：运行迁移命令**

```bash
claude install
```

**步骤3：验证迁移成功**

```bash
claude --version
claude doctor
# 核对版本、安装类型与实际启动路径
```

**步骤4：卸载npm版本（可选）**

```bash
npm uninstall -g @anthropic-ai/claude-code
```

迁移通常沿用已有用户设置，但先备份自己的规则和记录，并在新副本中核对实际加载结果；常用位置包括 `~/.claude/` 和 `~/.claude.json`。

**特殊场景：使用 nvm / asdf 的用户**

先完成原生安装和验证，再用 `nvm ls` 查看实际已安装的 Node 版本。逐个切换到确实留有旧 Claude Code npm 包的版本，按需卸载该包；不要照抄 `nvm use 20` / `22` 当成自己的版本列表。卸载旧包后再运行 `claude doctor` 核对路径。

如果使用 asdf，按 asdf 的命令重新生成相应 shims，不要直接删除一个猜测的 shim 文件。否则在删掉最后一个 npm 启动器后再执行 `claude install`，可能已经找不到该命令。

### C. 推荐学习资源

**Claude Code官方文档：**

- 英文：https://code.claude.com/docs/en/
- 中文：https://code.claude.com/docs/zh-CN/

**Anthropic API文档：**

- https://docs.anthropic.com/

**终端使用教程：**

- Windows Terminal：https://learn.microsoft.com/zh-cn/windows/terminal/
- macOS终端：https://support.apple.com/zh-cn/guide/terminal/

**社区支持：**

- Claude Discord：https://discord.gg/anthropic
- GitHub Discussions：https://github.com/anthropics/claude-code/discussions

---

**课程制作**：老金
**最后更新**：2026年9月14日（已对照 Claude Code v2.1.270 release 增补安装、后台任务、插件、权限与安全说明；安装路径仍以「原生 + npm」双轨为准）
**版本**：V3.5（v2.1.270 release 校准补丁）
**许可**：本课程采用 MIT License；转载、复制或二次分发时必须保留版权声明与许可声明

---
