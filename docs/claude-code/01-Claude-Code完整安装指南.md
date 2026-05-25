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
> - **更新日期**：2026年4月
> - **适用版本**：Claude Code v2.1.150（验证于 2026-05-25）
> - **重要更新**：当前同时支持原生安装与标准 npm 安装；原生更省心，npm 路径仍然受支持且需要 Node.js 18+

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/claude-code-agent-view.png" alt="Claude Code 官方 Agent View：多后台会话状态" width="720"/></p>

完成本课学习后，你将能够：

1. **理解Claude Code的核心价值**：掌握Claude Code与传统AI编程工具的本质区别
2. **了解两条安装路径**：知道什么时候优先用原生安装，什么时候仍然可以走 npm 标准安装
3. **配置Anthropic服务**：获取并正确配置API密钥
4. **完成Claude Code安装**：掌握原生安装与 npm 标准安装两条主路径
5. **集成到主流IDE**：VS Code、Cursor、JetBrains等编辑器配置
6. **验证环境可用性**：通过Hello World测试确认所有组件正常工作
7. **掌握故障排查技能**：独立解决90%的常见安装问题
8. **了解从npm迁移**：如果你之前用npm安装过，如何迁移到原生版本

---

## 🗺️ 学习路径导航（先看这里！）

> 💡 **根据你的情况选择学习路径**：这是一篇3000+行的长教程，不用全看！根据你的目标选择路径。

### 路径A：快速上手（⏱️ 30分钟）

**适合人群**：急着体验Claude Code，想快速跑起来

**只看这些章节**（其他跳过）：

```
✅ 术语表（3分钟） - 快速了解关键概念
✅ 第3部分：API Key配置（10分钟）
✅ 第4部分：Claude Code原生安装（5分钟） - 一行命令搞定！
✅ 第5部分：启动与验证（12分钟）
```

**30分钟后你能达到**：成功启动Claude Code，运行Hello World示例

---

### 路径B：完整学习（⏱️ 2-3小时）

**适合人群**：想深入理解每个细节，掌握所有功能

**学习顺序**：从头到尾所有章节

**建议分段学习**：
- 第1阶段（1小时）：第1-4部分（理解+API Key+安装）
- 第2阶段（1小时）：第5-6部分（验证+IDE集成）
- 第3阶段（30分钟）：第7-8部分（故障排查+FAQ）

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
| **Node.js** | - | JavaScript 运行环境；如果你走 `npm install -g @anthropic-ai/claude-code` 这条标准安装路径，仍需要 18+ |
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

<p align="center"><img src="../../images/official/claude-code-product-ui.jpg" alt="Claude Code 官方任务界面：后台任务状态与输入区" width="720"/></p>

Claude Code 是 Anthropic 公司开发的**命令行AI编程助手**。与传统代码编辑器插件不同，它是一个独立运行的CLI工具，通过终端与开发者交互。

**核心特征：**

- **本地优先架构**：代码在你的电脑上处理，不上传到云端
- **全能AI助手**：基于Claude模型，理解复杂技术需求
- **工具整合能力**：可调用文件操作、终端命令、Web搜索等工具
- **对话式开发**：用自然语言描述需求，AI帮你生成和修改代码

**简单理解：**

把Claude Code想象成一个24小时在线的高级程序员。你用中文或英文告诉他需求，他能帮你写代码、改bug、搜资料、运行测试。**最大特点是通过命令行工作**，可以直接操作你的代码文件、运行系统命令，完全脚本化和自动化。

### 1.2 核心优势：为什么值得学习

#### 优势1：隐私与安全

传统在线AI工具需要你把代码上传到服务器分析。Claude Code不同：

- ✅ 代码文件留在本地，AI只读取你授权的文件
- ✅ 可在企业内网环境使用（配合私有Claude部署）
- ✅ 敏感项目（如金融、医疗系统）也能安全使用

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
2. **只用图形界面**：Claude Code需要熟悉命令行
3. **网络受限**：需要访问Anthropic API（国内需代理）

---

## 课前准备检查清单

> ⚠️ **2026年重大更新**：原生安装路径确实**不需要 Node.js**，但 npm 标准安装仍然存在，所以本章会同时教你两条路径。

在开始安装前,请确认以下内容已完成:

| 检查项                      | 状态            | 如果未完成                   |
| --------------------------- | --------------- | ---------------------------- |
| **操作系统兼容**      | [ ] 确认        | Windows 10+ / macOS 10.15+ / Linux |
| **ANTHROPIC_API_KEY** | [ ] 已配置      | 中转站或官网获取(见第三部分) |
| **终端可用**          | [ ] 能打开      | macOS用终端，Windows用PowerShell |
| **网络连接**          | [ ] 可访问外网  | 国内用户需代理(见附录)        |

**如果所有项都已完成,让我们开始吧!**

> 💡 **老金提示**：相比旧版本，你现在**省去了安装Node.js的40分钟**！原生安装器自带所有依赖，一条命令搞定！

---

## 第二部分：系统要求快速检查

> 💡 **本节目的**：快速确认你的电脑能不能运行Claude Code，3分钟搞定！

### 2.1 快速检查清单（核心3项）

在开始安装前，确认以下3项**核心要求**：

| 检查项 | 最低要求 | 如何检查 | 不符合怎么办 |
|--------|---------|---------|-------------|
| **操作系统** | Windows 10 / macOS 10.15+ / Linux | 查看系统版本 | 升级系统或换电脑 |
| **内存** | 4GB RAM | 右键"此电脑"→属性 | 不足4GB无法运行 |
| **网络** | 能访问外网 | 打开 google.com 试试 | 国内用户需要配置代理（见附录B） |

**快速验证命令：**

**所有平台通用：**
```bash
# 检查能否访问Anthropic API
ping api.anthropic.com
# 能ping通 → ✅ 网络OK
# ping不通 → ⚠️ 需要配置代理
```

**如果3项全部✅ → 恭喜，你的电脑满足要求，继续往下！**

**如果有❌ → 跳到附录A查看详细要求和解决方案。**

---

### 2.2 详细要求说明（可选阅读）

> ⚠️ **小白注意**：这部分是详细技术说明，如果上面快速检查都通过了，可以跳过直接看第三部分！

**操作系统详细兼容性：**

| 操作系统 | 最低版本 | 推荐版本 | 说明 |
|---------|---------|---------|------|
| Windows | Windows 10 | Windows 11 | 64位系统 |
| macOS | 10.15 Catalina | macOS 13+ | Intel/Apple Silicon都支持 |
| Linux | 内核3.10+ | 5.x+ | Ubuntu/Debian/Fedora等主流发行版 |

**硬件推荐（非强制）：**
- **CPU**：双核+（i3或同等性能即可）
- **内存**：8GB更佳（4GB也能用，大项目会慢点）
- **存储**：SSD更快（机械硬盘也行）

> 💡 **老金建议**：别被这些要求吓到！只要你电脑能正常开发写代码，就肯定能跑Claude Code。这些是"推荐配置"不是"必需配置"。
>
> **详细性能对比和配置建议** → 见附录A

---

## 第三部分：原生安装说明（⭐ 重要更新）

> 💡 **2026年重大变化**：Claude Code已切换到**原生安装器**！
>
> **好消息**：你**不再需要安装Node.js**了！官方从npm安装迁移到原生安装，安装过程从40分钟缩短到5分钟！
>
> ⏱️ **预计时间**：5分钟完成安装

### 3.1 为什么切换到原生安装？

**背景说明：**

截至 2026-04-05，Claude Code 官方文档的真实口径是：

- 仍然保留 **标准安装**：`npm install -g @anthropic-ai/claude-code`
- 同时提供 **原生二进制安装**（beta / 改进安装路径）
- 安装后建议运行 `claude doctor` 检查当前安装类型

因此，这里更准确的理解不是“npm 被删除了”，而是：

> Claude Code 从“只有 npm 一条路”，变成了“原生安装 + npm 标准安装并存”。

**原生安装 vs npm安装对比：**

| 对比项         | 原生安装 ⭐ | npm标准安装 |
| -------------- | ----------- | ----------------- |
| 需要Node.js    | ❌ 不需要    | ✅ 需要 18+      |
| 安装时间       | ⏱️ 5分钟     | ⏱️ 40分钟        |
| 自动更新       | ✅ 更接近官方默认体验  | ⚠️ 通常需你自己更新 |
| PATH配置       | ✅ 自动完成  | ⚠️ 经常出错     |
| 跨平台支持     | ✅ 完美      | ⚠️ 平台差异大   |
| 稳定性         | ✅ 生产级    | ⚠️ 依赖环境     |

**简单理解：**

现在更像是：

- **原生安装**：买成品，拿来即用
- **npm 安装**：标准件组装，兼容性更广，但需要你自己有 Node 环境

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
- ✅ 增量更新（只下载变化部分，省流量）
- ✅ 可配置更新策略（见高级配置）

**如何禁用自动更新？（可选）**

```bash
# 如果你想手动控制更新，可以设置环境变量
export CLAUDE_AUTO_UPDATE=false
```

> 💡 **老金建议**：大多数人保持默认开启就好，自动更新让你始终使用最新最安全的版本。

### 3.4 如果你之前用npm安装过？

**别担心！官方提供了迁移命令。**

如果你之前通过 `npm install -g @anthropic-ai/claude-code` 安装过，运行：

```bash
claude install
```

这会：
1. 下载并安装原生版本
2. 保留你的所有配置
3. 删除旧的npm版本

**详细迁移步骤** → 见附录：从npm迁移指南

---

## 第四部分：Anthropic 账号准备

> **💡 为什么现在就要准备API Key？**
>
> **小白常见疑问**："我还没装Claude Code，为什么先要API Key？"
>
> **答案很简单**：
> 1. Claude Code是AI助手，需要连接Anthropic的AI服务才能工作
> 2. API Key就像"通行证"，证明你有权使用AI服务
> 3. **提前准备好Key的好处**：装完Claude Code立即就能用，不用再等待
>
> **生活类比**：
> - Claude Code = 你新买的手机
> - API Key = SIM卡
> - 先办好SIM卡，手机到手插卡就能用！

> **💡 选择提示**：可选择使用**中转站**（更便宜、更稳定），或官方账号。
>
> - **中转站优势**：价格低（约官方1/3-1/2）、无需科学上网、支付方便
> - **官方账号优势**：更稳定、有免费额度、支持订阅
>
> 本课程同时讲解两种方式的配置方法。

### 4.1 注册 Anthropic 账号

**注册流程：**

1. **访问注册页面**：https://console.anthropic.com/
2. **点击"Sign Up"（注册）**
3. **选择注册方式**（三种任选其一）：

   - Google账号登录（推荐，最快）
   - 邮箱+密码注册
   - GitHub账号登录
4. **完善账号信息**：

   - 姓名：真实姓名或开发者昵称
   - 使用场景：选择"Personal Use"（个人使用）或"Business"（商业）
   - 主要编程语言：可多选
5. **手机验证（可能需要）**：

   - 支持中国大陆号码（+86）
   - 会收到6位数验证码短信
   - 如果未收到，可选择语音验证

> **注意**：国内手机号注册成功率约80%。如果多次失败，可尝试使用Google Voice虚拟号码、香港/台湾号码，或联系Anthropic支持。

### 4.2 API Key 获取步骤

**什么是API Key？**

API Key是一串密钥，作用类似密码，用于：

- 证明你有权使用Claude AI服务
- 追踪API调用次数（计费依据）
- 控制访问权限

**格式示例：**

```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**获取步骤：**

1. **进入API Keys页面**

   登录后点击左侧菜单：`Settings → API Keys`

   或直接访问：https://console.anthropic.com/settings/keys
2. **创建新Key**

   点击"Create Key"按钮，填写：

   - Key名称：例如"claude-code-laptop"（方便区分多个key）
   - 权限：选择"Full Access"（完全访问）
3. **复制并保存Key**

   ⚠️ **关键警告**：

   - Key只显示一次！关闭窗口后无法再看到
   - 必须立即复制并保存到安全位置
   - 不要分享给任何人

   **保存方法**：

   1. 创建文本文件 `anthropic-key.txt`
   2. 粘贴完整key
   3. 保存到电脑安全位置（如Documents文件夹）
4. **验证Key有效性**

   ```bash
   # macOS/Linux
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: 你的API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{
       "model": "claude-sonnet-4-6",
       "max_tokens": 1024,
       "messages": [{"role": "user", "content": "Hello"}]
     }'

   # 如果返回JSON响应(而不是错误),说明Key有效
   ```

   **Windows PowerShell测试：**

   ```powershell
   $headers = @{
       "x-api-key" = "你的API_KEY"
       "anthropic-version" = "2023-06-01"
       "content-type" = "application/json"
   }
   $body = '{"model":"claude-sonnet-4-6","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'
   Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" -Method POST -Headers $headers -Body $body
   ```

### 4.3 环境变量配置

**什么是环境变量？**

环境变量是操作系统级别的配置，让程序可以读取敏感信息（如API Key），而不需要写在代码里。

**好处：**

- ✅ 安全：不会意外提交到GitHub
- ✅ 灵活：不同电脑可用不同Key
- ✅ 标准：所有开发工具都支持

#### Windows配置方法

**推荐方法：PowerShell 7（最佳选择）**

```powershell
# 永久添加用户环境变量（PowerShell 7）
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-api03-你的key', 'User')

# 验证配置
$env:ANTHROPIC_API_KEY

# 重启PowerShell后生效
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

# 验证
echo $ANTHROPIC_API_KEY
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

> 💡 **什么是API中转站？** 中转站是第三方提供的API代理服务，将你的请求转发到Anthropic官方API。对于国内用户来说，中转站可以解决网络访问问题，通常价格也更低。

**中转站 vs 官方API对比：**

| 对比项 | 官方API | 中转站 |
|--------|---------|--------|
| 价格 | 官方定价 | 通常为官方的 1/3 ~ 1/2 |
| 网络要求 | 需要科学上网 | 无需科学上网 |
| 支付方式 | 信用卡（Visa/Master） | 支付宝/微信 |
| 稳定性 | 最稳定 | 取决于中转站质量 |
| 免费额度 | 新用户有 $5 额度 | 通常无免费额度 |

**配置方法：**

中转站会提供一个自定义的 API 地址（Base URL），你需要同时配置 `ANTHROPIC_API_KEY` 和 `ANTHROPIC_BASE_URL` 两个环境变量。

**Windows（PowerShell）：**

```powershell
# 设置中转站API Key（中转站提供的Key）
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', '你的中转站Key', 'User')

# 设置中转站API地址
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL', 'https://你的中转站地址/v1', 'User')

# 重启终端后验证
$env:ANTHROPIC_BASE_URL
```

**macOS/Linux：**

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export ANTHROPIC_API_KEY="你的中转站Key"
export ANTHROPIC_BASE_URL="https://你的中转站地址/v1"

# 使配置生效
source ~/.zshrc
```

**验证中转站是否生效：**

```bash
# 启动Claude Code后，观察是否能正常连接
claude

# 如果连接成功，说明中转站配置正确
# 如果报错，检查URL末尾是否需要 /v1
```

> ⚠️ **安全提醒**：选择中转站时注意甄别，优先选择口碑好、运营时间长的服务商。中转站可以看到你的API请求内容，避免传输高度敏感的数据。

### 4.4 计费与订阅

**Claude Code需要付费吗？**

两层计费：

1. **Claude Code工具本身**

   - ✅ 免费开源
   - 无需购买License
2. **Claude API使用费**

   - ⚠️ 按调用量计费
   - 类似手机话费（用多少付多少）

**Token是什么？**

Token是AI处理文本的最小单位，用于计费：

- 1 token ≈ 0.75个英文单词
- 1 token ≈ 1-2个汉字
- 1000 tokens ≈ 750字短文

> 💡 **成本说明**：
>
> Claude Code的使用成本取决于你的API调用量。具体计费方式和价格请查看：
> - **官方价格页面**：https://www.anthropic.com/pricing
> - **Console账单页面**：https://console.anthropic.com/ → Settings → Billing
>
> 建议在实际使用中监控自己的消耗情况，根据需求调整使用频率。

---

## 第五部分：Claude Code 原生安装（⭐ 核心重点）

> 💡 **本部分目标**：一行命令完成安装，5分钟搞定！
> ⏱️ **预计时间**：3-5分钟

### 5.1 安装方式概览

**原生安装提供3种方式**，任选其一即可：

| 安装方式       | 适用平台           | 命令                          | 推荐度 |
| -------------- | ------------------ | ----------------------------- | ------ |
| **脚本安装** ⭐ | macOS/Linux/WSL   | `curl ... | bash`         | ⭐⭐⭐⭐⭐ |
| **PowerShell**  | Windows           | `irm ... | iex`            | ⭐⭐⭐⭐⭐ |
| **Homebrew**    | macOS/Linux       | `brew install --cask`    | ⭐⭐⭐⭐   |
| **WinGet**      | Windows 10/11     | `winget install`         | ⭐⭐⭐⭐   |
| **NPM** ⚠️    | 全平台（需Node.js） | `npm install -g`         | ⭐⭐⭐     |

> 💡 **老金推荐**：
> - **Windows用户**：用PowerShell（最简单）
> - **Mac用户**：用脚本安装或Homebrew（都很快）
> - **Linux用户**：用脚本安装
> - **原生安装失败？**：试试 NPM 方式（见方式4），虽然官方标记为废弃，但仍然可以正常使用

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
| `curl -fsSL`             | 下载安装脚本（-f失败继续，-s静默，-S显示错误，-L跟随重定向） |
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
# 预期输出：Claude Code v2.1.x (native)
```

#### Windows PowerShell 安装

**步骤1：打开PowerShell**

- 按 `Win` 键
- 输入 `PowerShell`
- 按 `Ctrl + Shift + Enter`（以管理员身份运行）

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

> ⚠️ **重要说明**：当前官方文档仍保留 `npm install -g @anthropic-ai/claude-code` 这条标准安装路径，只是对新环境更鼓励优先尝试原生安装。你可以把 npm 安装理解成“兼容性更广的标准入口”，而不是“已经不能用的旧方式”。

**前提条件**：需要先安装 [Node.js](https://nodejs.org/) 18 或更高版本。

```bash
# 检查 Node.js 版本（需要 18+）
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
# 预期输出：Claude Code v2.1.x (npm)  ← 注意这里显示 npm 而非 native
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
| 需要 Node.js | ❌ 不需要 | ✅ 需要 18+ |
| 自动更新 | ✅ 内置 | ❌ 需手动 `npm update -g` |
| 安装大小 | ~80MB | ~80MB + Node.js |
| 官方支持 | ✅ 当前更推荐 | ✅ 仍受支持 |
| 适合场景 | 所有用户 | 原生安装失败时的备选 |

> 💡 **老金建议**：如果你是全新环境，优先试原生安装；如果你本来就有稳定的 Node 18+ 环境，或者原生安装在你机器上受阻，npm 仍然是完全合理的选择。装好之后也可以随时通过 `claude install` 迁移到原生版本。

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
# 如果显示版本号（如 Claude Code v2.1.x (native)），说明配置成功
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
# 预期输出：Claude Code v2.1.x (native)

# 检查帮助
claude --help
# 应该显示完整帮助信息

# 检查安装位置
where claude     # Windows
which claude     # macOS/Linux
```

**成功的标志：**
- ✅ 显示版本号（带 `native` 标识）
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

# Windows: 以管理员身份运行PowerShell
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

1. 点击"更多信息"
2. 点击"仍要运行"
3. 原因：原生安装器由Anthropic签名，SmartScreen可能不认识新签名

---

### 5.9 卸载 Claude Code

**如果你需要卸载：**

**macOS/Linux:**

```bash
# 删除可执行文件
rm ~/.local/bin/claude

# 删除配置和数据（可选）
rm -rf ~/.claude
```

**Windows:**

```powershell
# 删除可执行文件
Remove-Item -Force "$env:USERPROFILE\.local\bin\claude.exe"

# 删除配置和数据（可选）
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude"

# 从 PATH 中移除安装目录（可选）
# 通过 系统属性 → 环境变量 → 用户变量 Path → 删除 %USERPROFILE%\.local\bin
```

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

### 6.1 启动 Claude Code 的三种方式

**方式1：标准交互模式（最常用）**

```bash
# 在任意目录启动
claude

# 启动流程：
# 1. 检测当前目录
# 2. 加载CLAUDE.md（如果存在）
# 3. 进入交互式对话界面
```

**方式2：单次命令模式**

```bash
# 执行单个命令后退出
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

```
? Choose your theme:
  ❯ Light (浅色主题,适合白天)
    Dark (深色主题,适合夜晚)
    System (跟随系统设置,推荐)
```

使用 ↑/↓ 箭头键选择，按回车确认。

**主题说明：**

| 主题   | 特点               | 适用场景         |
| ------ | ------------------ | ---------------- |
| Light  | 浅色背景，深色文字 | 光线充足的环境   |
| Dark   | 深色背景，浅色文字 | 长时间编程，护眼 |
| System | 自动跟随系统       | 推荐选择         |

**配置步骤2：安全须知确认**

```
╭─────────────────────────────────────────────────────────╮
│                     Safety Notice                       │
├─────────────────────────────────────────────────────────┤
│  Claude Code will operate in the current directory:    │
│  /Users/yourname/projects/my-app                        │
│                                                         │
│  This means Claude can:                                 │
│  ✓ Read files in this directory and subdirectories     │
│  ✓ Create new files                                    │
│  ✓ Modify existing files (with your confirmation)      │
│  ✓ Run commands (with your confirmation)               │
│                                                         │
│  Claude will NOT:                                       │
│  ✗ Access files outside this directory                 │
│  ✗ Access your personal data                           │
│  ✗ Execute commands without permission                 │
╰─────────────────────────────────────────────────────────╯

? Do you understand and accept these conditions?
  ❯ Yes, I understand and accept
    No, exit and reconsider
```

**重要理解 - Claude Code的权限模型：**

1. **沙盒隔离** - 只能访问当前目录
2. **确认机制** - 危险操作需要你确认
3. **只读优先** - 默认只读，修改需授权
4. **审计日志** - 所有操作都有记录

**配置步骤3：目录信任确认**

```
? Trust this directory?
  /Users/yourname/projects/my-app

  ❯ Yes, trust this directory
    No, exit
    Trust this directory and all parent directories
```

**不要信任以下目录：**

- ✗ 下载目录（可能有恶意代码）
- ✗ 临时目录（不需要持久访问）
- ✗ 系统目录（危险！）
- ✗ 不明来源的代码目录

**配置步骤4：认证方式选择**

```
? How would you like to authenticate?

  ❯ API Key (recommended for API users)
    Use environment variable: ANTHROPIC_API_KEY
    Most flexible and secure

    Claude App Login (for Pro/Max subscribers)
    Login via browser
    Uses your subscription quota

    Manual Entry
    Enter API key now
    Stored in config file
```

**认证方式对比：**

| 方式     | 优点               | 缺点            | 推荐度     |
| -------- | ------------------ | --------------- | ---------- |
| 环境变量 | 最安全，跨项目共享 | 需要提前配置    | ⭐⭐⭐⭐⭐ |
| App登录  | 使用订阅配额       | 需要Pro/Max订阅 | ⭐⭐⭐⭐   |
| 手动输入 | 方便               | 不安全，易泄露  | ⭐⭐       |

**第三方平台与 AWS Bedrock（v2.1.92，摘自官方 release）**：[v2.1.92](https://github.com/anthropics/claude-code/releases/tag/v2.1.92) 写明，在登录界面选择 **「3rd-party platform」** 时，可使用 **interactive Bedrock setup wizard**，引导完成 *AWS authentication, region configuration, credential verification, and model pinning*。菜单文案与步骤顺序以你安装的 CLI 版本为准；与仅使用 API Key / `modelOverrides` 走 Bedrock 的路径是否等价，请按官方文档区分场景。

**配置步骤5：完成初始化**

```
╭─────────────────────────────────────────────────────────╮
│            Setup Complete! 🎉                           │
├─────────────────────────────────────────────────────────┤
│  Configuration summary:                                 │
│  ✓ Theme: System                                        │
│  ✓ Authentication: API Key (environment variable)      │
│  ✓ Trusted directory: /Users/yourname/projects/my-app  │
│  ✓ Model: claude-sonnet-4 (default)                    │
│                                                         │
│  Quick start:                                           │
│  • Type your message to chat with Claude               │
│  • Use /help to see available commands                 │
│  • Use /exit to quit                                    │
╰─────────────────────────────────────────────────────────╯

Claude Code v2.1.92
Working directory: /Users/yourname/projects/my-app

You: █
```

### 6.3 配置文件结构

Claude Code的配置分为**全局**和**项目**两级：

```
~/.claude/                      ← 全局配置目录
├── config.json                 ← 全局配置文件
├── auth-token.json             ← 认证令牌
├── trusted-directories.json    ← 信任的目录列表
├── cache/                      ← 缓存目录
└── logs/                       ← 日志目录

项目目录/.claude/              ← 项目级配置
├── config.json                 ← 项目配置（覆盖全局）
├── commands/                   ← 自定义命令
├── skills/                     ← 自定义技能
└── hooks/                      ← 自定义钩子
```

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
| `claude`                                | 默认启动（会询问权限） | 日常使用             |
| `claude --dangerously-skip-permissions` | 跳过权限询问           | 信任的项目，快速开发 |
| `claude -p "你的问题"`                  | 直接提问模式           | 快速查询，不需要对话 |
| `claude --headless`                     | 无界面模式             | 脚本自动化           |

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

**真实风险数据（eesel AI研究）：**

> 🚨 **震惊数据**：
> - **32%的开发者**使用此参数时遇到过**文件误修改**
> - **9%遇到过数据损失或损坏**
>
> **数据来源**：https://www.ksred.com/claude-code-dangerously-skip-permissions

**生活类比：**
- 不加参数 = 保姆做事前都问你"这样行吗？"（安全）
- 加这个参数 = 保姆直接干，不问你（快但危险）

**什么时候该用？**

✅ **推荐使用场景：**
- 你自己的个人项目（信任的代码）
- 快速开发，频繁修改（避免反复确认）
- 只读操作（查询、分析，不修改代码）
- 你已经很熟悉Claude Code的行为

❌ **绝对不要用：**
- 公司项目、开源项目（不是你一个人的代码）
- 第一次用Claude Code（还不了解它会干什么）
- 生产环境代码（一个错误可能造成事故）
- 包含敏感数据的项目（财务、用户隐私）

**安全使用建议（Anthropic官方）：**

1. **容器隔离**：在Docker容器中使用（无网络访问）
2. **白名单限制**：配置 `.claude/settings.json`（权限通过 `permissions.allow` 管理，详见 [官方权限文档](https://code.claude.com/docs/en/permissions)）
   ```json
   {
     "permissions": {
       "allow": [
         "Read",
         "Grep",
         "Glob",
         "Bash(npm test)",
         "Bash(git status)"
       ]
     }
   }
   ```
3. **Git保护**：确保代码已提交，随时可回滚

**使用示例：**

```bash
# ✅ 场景1：只读查询（安全）
claude --dangerously-skip-permissions -p "分析这个项目的依赖关系"

# ⚠️ 场景2：信任的个人项目（谨慎）
cd ~/my-toy-project
claude --dangerously-skip-permissions

# ❌ 场景3：公司项目（绝对不要）
cd ~/company-critical-project
claude --dangerously-skip-permissions  # 💀 别这么干！
```

> ⚠️ **老金的血泪建议**：
>
> **新手阶段（前1个月）**：**绝对不要加这个参数**！让AI每次操作都问你，你能学到它在做什么，还能避免误操作。
>
> **熟练阶段（1个月后）**：自己的学习项目可以加，但：
> - ✅ 代码先提交到Git
> - ✅ 不包含重要数据
> - ✅ 随时能删重来
>
> **专业阶段**：公司项目、开源项目**永远别加**！老金我见过太多人用这个参数把项目搞炸了，数据来源可不是瞎说的（32%误修改率）！
>
> **参考**：
> - 官方最佳实践：https://www.anthropic.com/engineering/claude-code-best-practices
> - 风险分析：https://claudelog.com/mechanics/dangerous-skip-permissions

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
- Cursor（可以通过Tasks集成，见第7章）

#### VS Code扩展安装（官方扩展已发布）

> ✅ **2026年2月最新**：Claude Code官方VS Code扩展已正式发布（Beta版）！

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

#### Cursor集成方式（需要手动安装）

**重要提示**：Cursor虽然基于VS Code，但Claude Code扩展**不能自动检测**Cursor为兼容IDE。

**解决方案（社区验证100%成功）：手动安装VSIX文件**

**步骤：**

1. **找到VSIX文件**
   - 位置：本地Claude Code安装目录
   - 或从VS Code Marketplace下载VSIX

2. **手动安装到Cursor**
   ```bash
   # 方法1：命令行安装
   cursor --install-extension /path/to/claude-code.vsix

   # 方法2：拖拽安装
   # 把VSIX文件拖到Cursor的扩展面板
   ```

3. **验证安装**
   - 重启Cursor
   - 左侧应出现Claude Code图标

**详细教程**：https://www.cursor-ide.com/blog/claude-code-cursor-extension-guide

**替代方案：Tasks集成（推荐新手）**

如果扩展安装失败，可以用Tasks方式（见第7.1节配置）：
1. 配置 `tasks.json`
2. 通过命令面板运行任务
3. 效果类似但更稳定

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

**快速7项测试，确认核心功能正常：**

```bash
# 测试1：版本检查
claude --version
# 预期输出：Claude Code v2.1.x (native)

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
快速测试能发现99%的配置问题，避免后续出错。

**操作步骤：**

```bash
# 步骤1：创建项目目录
mkdir ~/claude-hello-world
cd ~/claude-hello-world

# 步骤2：初始化Git仓库
git init

# 步骤3：让Claude创建项目结构
claude -p "请创建一个Python Hello World项目，包含：
1. hello.py - 打印 'Hello, Claude Code!'
2. README.md - 项目说明
3. .gitignore - Python标准忽略文件"

# 步骤4：验证文件是否创建
ls -la
# 预期看到：hello.py, README.md, .gitignore

# 步骤5：运行程序
python hello.py
# 预期输出：Hello, Claude Code!
```

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
| 版本信息 | `claude --version` | v2.1.x+ (native) | [ ] |
| 帮助文档 | `claude --help` | 显示命令列表 | [ ] |
| API Key | `echo $ANTHROPIC_API_KEY` | 显示完整Key | [ ] |
| 网络连通 | `ping api.anthropic.com` | 有响应 | [ ] |
| 文件操作 | Hello World项目 | 成功创建文件 | [ ] |
| 代码执行 | `python hello.py` | 正常输出 | [ ] |

**全部打勾 → 🎉 恭喜！Claude Code安装和配置完全成功！**

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

<p align="center"><img src="../../images/official/claude-code-vscode-interface.jpg" alt="Claude Code 官方 VS Code 扩展界面" width="720"/></p>

> 💡 **这一节讲什么**：配置VS Code/Cursor编辑器，让它能完美运行Claude Code命令。配置后你就能在编辑器里一键调用AI助手了。

#### 步骤1：VS Code基础配置

首先确保VS Code已安装最新版本：

```bash
# 检查VS Code版本
code --version

# 如果未安装，访问：https://code.visualstudio.com/
```

> ⚠️ **Cursor用户注意**：Cursor是基于VS Code魔改的编辑器，所有VS Code的配置在Cursor里都能用！如果你用Cursor，把下面的"VS Code"理解成"Cursor"就行。

#### 步骤2：配置集成终端

**这是什么？**
"集成终端"就是编辑器下方那个黑框框（或白框框），用来运行命令的地方。配置它就是告诉编辑器："用哪个翻译器来执行我的命令"。

**为什么要配置？**
不配置的话，编辑器可能用错误的"翻译器"（Shell），导致命令运行失败或报错。

**操作方法：**
打开设置（`Ctrl/Cmd + ,`），点击右上角"打开设置(JSON)"，添加：

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
      "command": "claude "Review ${relativeFile} and suggest improvements"",
      "problemMatcher": []
    },
    {
      "label": "Claude Code: 解释当前文件",
      "type": "shell",
      "command": "claude "Explain what ${relativeFile} does"",
      "problemMatcher": []
    },
    {
      "label": "Claude Code: 生成测试",
      "type": "shell",
      "command": "claude "Generate unit tests for ${relativeFile}"",
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
创建或编辑 `.vscode/keybindings.json`：

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

> 💡 **重要提示**：Cursor的所有配置和VS Code**完全相同**！上面第7.1节的配置，在Cursor里一字不差地照搬就行。

**唯一不同：打开设置文件的方法**

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

如果方法A找不到菜单（Cursor版本不同可能有差异），用这个方法**100%有效**：

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

**配置完成后，Cursor就能完美运行Claude Code了！**

Cursor的配置与VS Code完全相同，如果上面VSCode中配置过，可以直接复用上面的配置：

```bash
# 将VS Code配置复制到Cursor
# macOS/Linux:
cp -r ~/project/.vscode ~/project/.cursor

# Windows:
xcopy /E /I %USERPROFILE%\project\.vscode %USERPROFILE%\project\.cursor
```

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

**问题1：PowerShell执行策略限制**

```powershell
# 错误信息（原生安装时可能遇到）
claude : 无法加载文件，因为在此系统上禁止运行脚本。
```

**原因**：Windows默认安全策略禁止运行未签名脚本

**解决方案：**

```powershell
# 方法1：修改执行策略（管理员PowerShell）- 推荐
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 方法2：使用CMD而不是PowerShell
# Win+R → cmd

# 方法3：每次临时允许执行
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**问题2：Windows Defender误报**

```bash
# 症状：安装过程中文件被删除
# 原因：Windows Defender将claude.exe识别为潜在威胁

# 解决方案
# 1. 添加 Claude Code 安装目录到排除列表
#    Windows安全 → 病毒和威胁防护 → 排除项
#    添加：C:\Users\<用户名>\.local\bin

# 2. 临时禁用实时保护（不推荐）
```

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

# 原因：PATH未更新（原生安装应该自动配置）

# 解决方案：检查原生安装位置
ls ~/.local/bin/claude
# 或
ls /usr/local/bin/claude

# 如果文件存在，添加到PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**问题2：macOS Gatekeeper阻止**

```bash
# 症状
"claude" cannot be opened because the developer cannot be verified

# 解决方案
# 方法1：移除隔离属性
sudo xattr -r -d com.apple.quarantine ~/.local/bin/claude

# 方法2：在系统设置中允许
# 系统设置 → 隐私与安全性 → 点击"仍要打开"
```

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

# 方案3：手动下载安装包
# 访问 https://claude.ai/download 下载对应平台的安装包
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
claude --version
# 显示 (npm) 而不是 (native)
```

**解决方案：**

```bash
# 运行迁移命令
claude install

# 这会自动：
# 1. 检测到npm版本
# 2. 下载原生版本
# 3. 卸载npm版本
# 4. 配置PATH
```

### 8.3 网络连接问题

**问题：无法访问api.anthropic.com**

```bash
ping api.anthropic.com
# 请求超时
```

**解决方案：**

```bash
# 方案1：配置代理（推荐）
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
# Windows PowerShell：
$env:https_proxy="http://127.0.0.1:7890"
$env:http_proxy="http://127.0.0.1:7890"

# 方案2：修改DNS
# Windows：设置DNS为8.8.8.8或114.114.114.114
# macOS/Linux：编辑/etc/resolv.conf添加nameserver 8.8.8.8

# 方案3：使用API中转服务
# 设置自定义API端点（见第三部分API Key配置）
```

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

### 8.4 API Key 配置问题

**问题：环境变量未生效**

```bash
echo $ANTHROPIC_API_KEY
# 显示为空
```

**解决方案：**

```bash
# macOS/Linux：确认配置文件
cat ~/.zshrc | grep ANTHROPIC
# 应该看到：export ANTHROPIC_API_KEY="sk-ant-..."

# 如果没有，手动添加
echo 'export ANTHROPIC_API_KEY="你的key"' >> ~/.zshrc
source ~/.zshrc
```

**Windows：**

```powershell
# 检查是否配置
[System.Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY', 'User')

# 如果为空，重新配置
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-api03-你的key', 'User')

# 重启PowerShell
```

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

**正确格式检查（PowerShell 7）：**

```powershell
# Key应该满足：
# 1. 以"sk-ant-api03-"开头
# 2. 后面跟长串字母数字
# 3. 总长度约95字符
# 4. 无空格、无换行

# 验证长度
$env:ANTHROPIC_API_KEY.Length
# 应该输出：95左右

# 验证格式
$env:ANTHROPIC_API_KEY -match '^sk-ant-api03-[A-Za-z0-9_-]+$'
# 应该输出：True
```

**常见格式错误：**

```bash
❌ sk-ant-XXXXX （缺少api03）
❌ sk-XXXXX （缺少ant-api03）
❌ 有空格或换行符
❌ 复制时多复制/少复制字符
```

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

**A1：你可能在Cursor里运行的！**

- `code` 是 **VS Code** 的命令
- `cursor` 是 **Cursor** 的命令

**正确做法：**

- 在Cursor里运行：`cursor --version`
- 在VS Code里运行：`code --version`
- 查看Claude Code版本：`claude --version`

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

**你不用手动选**，按照第7.1节配置后，编辑器会自动选对的！

#### Q5：怎么知道我现在用的是哪个Shell？

**A5：打开终端运行这个命令：**

```bash
echo $SHELL
```

**看输出：**

- 显示 `/bin/zsh` → 你在用zsh
- 显示 `/bin/bash` → 你在用bash
- Windows显示 `powershell` → 你在用PowerShell

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

**通俗解释：**

- 不加参数 = AI做事前都问你"可以吗？"
- 加参数 = AI直接干，不问你

**老金建议：**

- 🟢 **新手（前2周）**：别加！让AI问你，你能学到它在做什么
- 🟡 **熟练后**：自己的小项目可以加，省时间
- 🔴 **重要项目**：永远别加！安全第一

详细说明见第6.5.2节。

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

**A13：99%是格式问题！**

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

**A14：不会！Claude Code只上传你让它处理的内容。**

**工作原理：**

1. 你问问题 → Claude Code读取相关文件
2. 把文件内容发给Anthropic API处理
3. 收到AI回复后显示给你

**隐私保护：**

- ✅ 只上传你明确要求处理的文件
- ✅ 你可以通过权限控制它能访问什么
- ✅ 不会后台扫描或上传整个项目

#### Q15：我不想让Claude Code访问某些文件，怎么办？

**A15：用 `.gitignore` 或 `.claudeignore` 排除！**

**方法1：.gitignore（推荐）**
Claude Code默认会忽略 `.gitignore` 里的文件。

**方法2：.claudeignore**
在项目根目录创建 `.claudeignore` 文件：

```
# 不让Claude访问的文件
.env
*.key
secrets/
config/production.json
```

---

### 9.5 网络与性能类

#### Q16：Claude Code响应很慢，怎么优化？

**A16：检查网络和上下文大小！**

**网络检查：**

```bash
# 测试到Anthropic的延迟
ping api.anthropic.com
# 延迟<500ms = 正常，>1000ms = 慢
```

**优化方法：**

1. ✅ 使用代理（国内用户必需）
2. ✅ 减少上下文（不要让AI读太多文件）
3. ✅ 使用 `.claudeignore` 排除无关文件

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

**A19：没配置ANTHROPIC_API_KEY环境变量！**

**快速检查：**

```bash
# 查看环境变量是否存在
echo $ANTHROPIC_API_KEY  # macOS/Linux
echo $env:ANTHROPIC_API_KEY  # Windows
```

**如果显示空 → 没配置，回到第四部分重新配置。**

#### Q20：我之前用npm安装过Claude Code，怎么办？

**A20：官方提供了迁移命令！**

```bash
# 一键迁移到原生版本
claude install
```

这个命令会：
1. 下载并安装原生版本
2. 保留你的所有配置
3. 自动卸载旧的npm版本

**验证迁移成功：**

```bash
claude --version
# 应显示：Claude Code v2.1.x (native)
# 而不是：(npm)
```

**如果迁移失败，手动卸载npm版本：**

```bash
npm uninstall -g @anthropic-ai/claude-code
# 然后重新运行原生安装
```

#### Q21：原生安装和npm安装有什么区别？

**A21：简单来说，原生安装更省心；npm 安装仍然是官方支持的标准路径。**

| 对比项         | 原生安装 ⭐ | npm标准安装 |
| -------------- | ----------- | ----------------- |
| 需要Node.js    | ❌ 不需要    | ✅ 需要 18+      |
| 安装时间       | ⏱️ 3-5分钟  | ⏱️ 30-40分钟    |
| 自动更新       | ✅ 更接近官方默认体验  | ⚠️ 通常需你手动更新 |
| PATH配置       | ✅ 自动完成  | ⚠️ 经常出错     |
| 稳定性         | ✅ 生产级    | ⚠️ 依赖环境     |

#### Q22：原生安装可以离线使用吗？

**A22：可以！安装后只需要网络访问API即可。**

- ✅ 安装时需要网络（下载安装包）
- ✅ 安装后可以离线使用（但需要能访问Anthropic API）
- ✅ 配合本地模型（如Ollama）可以完全离线

#### Q23：原生安装会占用多少空间？

**A23：大约100-200MB。**

- Windows: `~150MB` 在 `C:\Users\你的用户名\.local\bin\`
- macOS/Linux: `~100MB` 在 `~/.local/bin/` 和 `~/.claude/`

相比npm安装节省约50%空间。

#### Q24：我电脑上已经有Node.js了，还需要卸载吗？

**A24：不需要！可以共存。**

- ✅ Node.js可以继续用于其他项目
- ✅ Claude Code原生安装不影响Node.js
- ✅ 如果你不用Node.js做开发，可以考虑卸载节省空间

#### Q25：原生安装会自动更新吗？可以关闭吗？

**A25：默认自动更新，可以关闭。**

**查看更新状态：**

```bash
claude --version
# 查看当前版本
```

**禁用自动更新：**

```bash
# macOS/Linux
export CLAUDE_AUTO_UPDATE=false

# Windows PowerShell
$env:CLAUDE_AUTO_UPDATE="false"
```

**手动更新：**

```bash
claude install
# 重新运行安装命令即可更新
```

#### Q26：公司电脑安装需要管理员权限吗？

**A26：Windows需要，Mac/Linux不需要！**

**Windows：**
- ⚠️ 建议以管理员身份运行PowerShell
- 原因：需要写入 `AppData` 目录

**macOS/Linux：**
- ✅ 不需要sudo
- 安装到用户目录 `~/.local/bin/`

#### Q27：安装脚本安全吗？会不会有病毒？

**A27：官方脚本，经过签名和验证！**

**安全验证：**

1. 官方域名：`claude.ai/install.sh` 和 `claude.ai/install.ps1`
2. 代码签名：由Anthropic PBC签名
3. 开源透明：脚本内容可在GitHub公开查看

**如果你担心，可以先查看脚本：**

```bash
# 只下载不执行
curl -fsSL https://claude.ai/install.sh
# 阅读后觉得安全再执行
curl -fsSL https://claude.ai/install.sh | bash
```

#### Q28：我的问题不在这里，怎么办？

**A20：这样做：**

1. ✅ 运行 `claude --help` 查看官方帮助
2. ✅ 查看日志文件：`~/.claude/logs/` 找错误信息
3. ✅ 访问官方文档：https://docs.claude.ai/code
4. ✅ GitHub搜索类似问题：https://github.com/anthropics/claude-code/issues
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

### 8.5.3 effort：不是"另一个模型"，是思考深度

`/effort` 控制的是**推理强度**，不是换模型。

可用值（v2.1.105-113 起新增 `xhigh`）：

- `low`
- `medium`
- `high`
- **`xhigh`**（推荐 Opus 4.7 默认）
- `max`
- `auto`

| 级别 | 含义 | 适合场景 |
|------|------|----------|
| `low` | 更快、更省 | 简单问答、格式转换 |
| `medium` | 平衡 | 日常编码 |
| `high` | 更深推理 | 复杂调试、架构分析 |
| **`xhigh`** | **深度推理（推荐 Opus 4.7 默认）** | **深度重构、关键决策** |
| `max` | 最深推理 | 极复杂问题，成本最高 |
| `auto` | 回到模型默认 | 不想手动管时 |

**官方建议**：

- **Opus 4.7 用户推荐默认 `xhigh`**
- `low`/`medium` 适合 Sonnet/Haiku 模型日常使用
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

现在 `Opus 4.7` 和 `Sonnet 4.6` 都支持 1M 上下文，但是否可见、是否默认可用，取决于计划和部署方式。

#### 最简单的用法

```bash
/model opus[1m]
/model sonnet[1m]
```

或者：

```bash
/model claude-opus-4-7[1m]
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

如果你是团队管理员，想限制"用户能选什么"，用的是 `availableModels`。

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
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
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

- [ ] 操作系统兼容（Windows 10+ / macOS 10.15+ / Linux）
- [ ] 终端可用（PowerShell / Terminal / Bash）
- [ ] 至少2GB可用磁盘空间

**账号准备：**

- [ ] 注册了Anthropic账号（或使用中转站）
- [ ] 获取了API Key
- [ ] Key已保存到安全位置

**系统配置：**

- [ ] 环境变量ANTHROPIC_API_KEY已配置
- [ ] 终端能正确显示中文
- [ ] 网络能访问api.anthropic.com（或配置了代理）

**Claude Code安装：**

- [ ] Claude Code原生安装成功
- [ ] `claude --version` 显示正确版本（带native标识）
- [ ] `claude --help` 显示帮助信息

**功能验证：**

- [ ] 通过基础测试套件
- [ ] 完成Hello World项目
- [ ] IDE集成配置完成（可选）

**如果以上全部勾选，恭喜你已经完成准备工作！🎉**

> ⚠️ **2026年更新说明**：本课程现已更新为“原生安装 + npm 标准安装并存”的口径。如果你是从旧版教程过来的，请优先参考本章新的安装路径说明，不要再默认把 npm 视为唯一入口，也不要误以为 Node.js 已被完全移除。

---

## 附录

### A. 常用命令速查

```bash
# Claude Code版本和帮助
claude --version           # 查看版本（应显示native标识）
claude --help              # 查看帮助
claude /doctor             # 系统诊断

# Claude Code操作
claude                     # 进入交互模式
claude "你的问题"          # 单次提问
claude -p "问题"           # 打印模式（脚本友好）

# 更新Claude Code
claude install             # 重新安装/更新到最新版本

# 环境变量查看
$env:ANTHROPIC_API_KEY     # PowerShell 7（推荐）
echo $ANTHROPIC_API_KEY    # macOS/Linux
echo %ANTHROPIC_API_KEY%   # Windows CMD（不推荐）

# 网络测试
ping api.anthropic.com     # 测试连通性
curl -I https://api.anthropic.com  # 测试HTTPS访问

# 配置管理
claude config list         # 查看所有配置
claude config get <key>    # 查看特定配置
claude config set <key> <value>  # 设置配置
```

### B. 从npm迁移到原生安装

**如果你之前通过npm安装过Claude Code，请按以下步骤迁移：**

**步骤1：检查当前安装方式**

```bash
claude --version
# 如果显示 (npm) → 需要迁移
# 如果显示 (native) → 已经是原生版本
```

**步骤2：运行迁移命令**

```bash
claude install
```

**步骤3：验证迁移成功**

```bash
claude --version
# 应显示：Claude Code v2.1.x (native)
```

**步骤4：卸载npm版本（可选）**

```bash
npm uninstall -g @anthropic-ai/claude-code
```

**迁移时会保留：**
- ✅ 所有配置文件（`~/.claude/`）
- ✅ API Key配置
- ✅ 自定义命令和技能
- ✅ 信任目录设置

**特殊场景：使用nvm的用户**

如果你用nvm管理多个Node版本，可能需要手动处理：

```bash
# 1. 对每个Node版本卸载
nvm use 20
npm uninstall -g @anthropic-ai/claude-code

nvm use 22
npm uninstall -g @anthropic-ai/claude-code

# 2. 然后运行原生安装
claude install

# 3. 清理nvm shims
rm ~/.asdf/shims/claude  # 如果你用asdf
```

### C. 推荐学习资源

**Claude Code官方文档：**

- 英文：https://docs.anthropic.com/en/docs/claude-code
- 中文：https://code.claude.com/docs/en/

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
**最后更新**：2026年4月（已对照 GitHub v2.1.90 / v2.1.92 release 增补登录与 Bedrock 向导说明；安装路径仍以「原生 + npm」双轨为准）
**版本**：V3.1（v2.1.92 release 对齐补丁）
**许可**：本课程采用CC BY-NC-SA 4.0许可

---
