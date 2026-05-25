# 11. 常见问题 (FAQ)

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **难度等级**：🟢 入门
> - **前置知识**：无
>
> **遇到问题？** 这里收集了社区最常见的问题和解决方案。用 `Ctrl+F`（或 `Cmd+F`）搜索关键词，快速定位你的问题
>
> **最常见的 5 个问题：** [Q1: 命令找不到](#q1-openclaw-命令找不到command-not-found) | [Q2: Node.js 版本不兼容](#q2-nodejs-版本不兼容) | [Q26: API Key 无效](#q26-api-调用报错-401-unauthorized) | [Q12: Gateway 启动失败](#q12-windows-上安装后-gateway-启动失败) | [Q16: WhatsApp 连接问题](#q16-whatsapp-扫码后频繁断开)

这篇 FAQ 收集了 OpenClaw 社区中最常见的问题和解决方案。按类别组织，方便你快速定位问题。

如果这里没有你遇到的问题，可以到 [GitHub Issues](https://github.com/openclaw/openclaw/issues) 提问，或加入 Discord 社区寻求帮助。

---

## 一、安装和配置问题

<p align="center"><img src="../../images/official/openclaw-model-picker.png" alt="OpenClaw 官方模型选择与配置界面" width="720"/></p>

<p align="center"><img src="../../images/official/openclaw-agents-ui.jpg" alt="OpenClaw 官方 Agent 与技能管理界面" width="720"/></p>

<p align="center"><img src="../../images/official/openclaw-quick-settings-browser-tools.png" alt="OpenClaw 官方 Control UI 设置与浏览器工具界面" width="720"/></p>

> 📌 **本节包含 15 个问题：**
> [Q1: 命令找不到](#q1-openclaw-命令找不到command-not-found) | [Q2: Node.js 版本不兼容](#q2-nodejs-版本不兼容) | [Q3: npm 权限错误](#q3-npm-install-报权限错误eacces) | [Q4: 中国网络安装慢](#q4-中国网络环境安装慢或失败) | [Q5: node-gyp 编译错误](#q5-安装时报-node-gyp-编译错误) | [Q6: onboard 报错](#q6-openclaw-onboard-引导向导报错) | [Q7: 配置文件位置](#q7-配置文件在哪里怎么手动编辑) | [Q8: 多 API Key 配置](#q8-多个-api-key-怎么配置) | [Q9: 配置优先级](#q9-环境变量和配置文件哪个优先) | [Q10: 升级后配置丢失](#q10-升级-openclaw-后配置丢失了) | [Q11: 版本回滚](#q11-升级后功能异常怎么回滚) | [Q12: Windows Gateway 失败](#q12-windows-上安装后-gateway-启动失败) | [Q13: macOS 安全提示](#q13-macos-上安装提示无法验证开发者) | [Q14: 端口被占用](#q14-安装完成但-openclaw-gateway-start-提示端口被占用) | [Q15: 完全卸载](#q15-怎么完全卸载-openclaw)

### Q1: `openclaw` 命令找不到（command not found）

**现象：** 安装完成后执行 `openclaw` 提示 `command not found` 或 `不是内部或外部命令`。

**原因：** npm 全局安装的 bin 目录没有加入系统 PATH 环境变量。

**解决方案：**

```bash
# 第一步：确认是否真的安装了
npm list -g openclaw

# 第二步：找到 npm 全局 bin 目录
npm config get prefix
# 输出类似 /usr/local 或 /home/user/.npm-global

# 第三步：把 bin 目录加入 PATH
# Linux / macOS
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell
# 把 npm prefix 路径加到系统环境变量 Path 中
# 或者直接用 npx openclaw 代替
npx openclaw --version
```

如果你用的是 `pnpm`，全局 bin 路径不同：

```bash
pnpm config get global-bin-dir
# 把输出的路径加入 PATH
```

### Q2: Node.js 版本不兼容

**现象：** 安装时报错 `engine "node" is incompatible` 或运行时出现语法错误。

**原因：** OpenClaw 当前官方建议使用 Node.js 24.x；22.19+ 仍然兼容。低于兼容线时，常见报错就是 `engine incompatible`、运行时语法错误或部分 API 不可用。

**解决方案：**

```bash
# 检查当前版本
node --version

# 如果低于 v22，用 nvm 升级
# 安装 nvm（如果还没装）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# 重新打开终端，然后：
nvm install 24
nvm use 24
nvm alias default 24  # 设为默认版本

# 验证
node --version  # 应该显示 v24.x.x
```

Windows 用户推荐用 [nvm-windows](https://github.com/coreybutler/nvm-windows)：

```powershell
nvm install 24
nvm use 24
```

### Q3: npm install 报权限错误（EACCES）

**现象：** `npm install -g openclaw` 时报 `EACCES: permission denied`。

**原因：** npm 全局目录的权限不对，当前用户没有写入权限。

**解决方案：**

```bash
# 方案一：修改 npm 全局目录（推荐）
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="~/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
npm install -g openclaw

# 方案二：用 sudo（不推荐，但能快速解决）
sudo npm install -g openclaw

# 方案三：用 nvm 管理 Node.js（最佳实践）
# nvm 安装的 Node.js 不需要 sudo
```

### Q4: 中国网络环境安装慢或失败

**现象：** `npm install` 卡住不动，或者下载速度极慢，最终超时失败。

**原因：** npm 默认从 `registry.npmjs.org` 下载，国内访问速度不稳定。

**解决方案：**

```bash
# 方案一：临时使用镜像（推荐）
npm install -g openclaw --registry=https://registry.npmmirror.com

# 方案二：永久切换镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw

# 方案三：使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install -g openclaw

# 验证镜像是否生效
npm config get registry
```

如果连 npm 镜像都访问不了，可以考虑 Docker 安装方式，提前拉取镜像：

```bash
# 使用 Docker Hub 镜像加速
docker pull openclaw/openclaw:latest
```

### Q5: 安装时报 `node-gyp` 编译错误

**现象：** 安装过程中出现 `gyp ERR!` 或 `node-gyp rebuild` 失败。

**原因：** 某些依赖包含原生 C++ 模块，需要编译工具链。

**解决方案：**

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install -y build-essential python3

# macOS
xcode-select --install

# Windows
# 以管理员身份运行 PowerShell
npm install -g windows-build-tools
# 或者安装 Visual Studio Build Tools
```

### Q6: `openclaw onboard` 引导向导报错

**现象：** 运行 `openclaw onboard` 后，终端卡在某一步不动了（光标闪烁但没有输出），或者直接报错退出并显示 `Error: network timeout` 或 `TypeError: Cannot read properties of undefined`。

**原因：** 可能是终端不支持交互式输入，或者网络问题导致无法验证 API Key。

**解决方案：**

```bash
# 方案一：确保用的是交互式终端（不是 IDE 内置终端）
# 打开系统自带的终端应用

# 方案二：跳过引导，手动配置
export OPENAI_API_KEY="sk-proj-xxxxx"
openclaw config set agents.defaults.model "openai/gpt-5.2"
openclaw gateway --port 18789

# 方案三：检查配置文件是否损坏
cat ~/.openclaw/openclaw.json
# 如果内容异常，删除后重新引导
rm ~/.openclaw/openclaw.json
openclaw onboard
```

### Q7: 配置文件在哪里？怎么手动编辑？

**现象：** 想直接编辑配置文件，但不知道在哪。

**说明：** OpenClaw 的所有配置都在 `~/.openclaw/` 目录下。

```bash
# 查看配置目录结构
ls -la ~/.openclaw/

# 主要文件：
# ~/.openclaw/openclaw.json    — 主配置文件（JSON5 格式）
# ~/.openclaw/workspace/      — 工作空间（记忆、技能等）
# ~/.openclaw/gateway/        — Gateway 运行时数据

# 用命令查看当前配置
openclaw config get

# 用命令修改配置（推荐，会自动验证格式）
openclaw config set <key> <value>

# 也可以直接编辑 JSON5 文件
nano ~/.openclaw/openclaw.json
```

### Q8: 多个 API Key 怎么配置？

**现象：** 想同时配置 OpenAI 和 Anthropic 的 Key，不知道怎么操作。

**解决方案：**

```bash
# 推荐：通过环境变量配置（优先级高于配置文件，更安全）
export OPENAI_API_KEY="sk-proj-xxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
export GEMINI_API_KEY="AIzaSy-xxxxx"

# 设置默认模型
openclaw config set agents.defaults.model "openai/gpt-5.2"

# OpenClaw 会自动读取环境变量，不需要在配置文件中写 Key
```

### Q9: 环境变量和配置文件哪个优先？

**说明：** 优先级从高到低：

```
命令行参数 > 环境变量 > ~/.openclaw/openclaw.json > 默认值
```

也就是说，如果你同时在环境变量和配置文件里设了 API Key，环境变量的值会生效。

### Q10: 升级 OpenClaw 后配置丢失了

**现象：** 更新到新版本后，之前的配置好像不见了。

**原因：** 正常情况下升级不会覆盖配置。但如果你用 Docker 部署且没有挂载数据卷，容器重建后数据会丢失。

**解决方案：**

```bash
# 升级前先备份
cp -r ~/.openclaw ~/.openclaw.backup

# npm 升级（配置不会丢）
npm update -g openclaw

# Docker 升级（确保挂载了数据卷）
# docker-compose.yml 中必须有：
# volumes:
#   - ./data:/root/.openclaw

# 如果配置真的丢了，从备份恢复
cp -r ~/.openclaw.backup ~/.openclaw
```

### Q11: 升级后功能异常怎么回滚？

**现象：** 执行 `npm update -g openclaw` 升级到新版本后，之前正常的功能出现报错、崩溃或行为异常，需要退回旧版本。

**解决方案：**

```bash
# 查看当前版本
openclaw --version

# 查看所有可用版本
npm view openclaw versions --json

# 回滚到指定版本
npm install -g openclaw@2026.3.28

# Docker 回滚
docker pull openclaw/openclaw:v2026.5.22
# 修改 docker-compose.yml 中的 image tag 后重启
```

### Q12: Windows 上安装后 Gateway 启动失败

**现象：** Windows 上执行 `openclaw gateway start` 后，终端窗口闪一下就关闭了（闪退），或者报错 `EADDRINUSE`、`EACCES` 等错误信息，Gateway 无法正常启动。

**原因：** Windows 的端口占用、防火墙或 WSL 兼容性问题。

**解决方案：**

```powershell
# 检查端口是否被占用
netstat -an | findstr 18789

# 如果被占用，换一个端口
openclaw config set gateway.port 18790

# 检查防火墙是否放行
# Windows Defender 防火墙 → 高级设置 → 入站规则 → 新建规则 → 端口 18789

# 推荐：在 WSL2 中运行 OpenClaw
wsl --install
# 在 WSL 中按 Linux 方式安装
```

### Q13: macOS 上安装提示"无法验证开发者"

**现象：** macOS 上首次运行 `openclaw` 命令时，系统弹出对话框提示「无法验证开发者」或「无法打开，因为 Apple 无法检查其是否包含恶意软件」，命令被阻止执行。

**解决方案：**

```bash
# 方案一：在系统偏好设置中允许
# 系统偏好设置 → 隐私与安全性 → 仍然允许

# 方案二：通过命令行移除隔离属性
xattr -d com.apple.quarantine $(which openclaw)
```

### Q14: 安装完成但 `openclaw gateway start` 提示端口被占用

**现象：** 报错 `EADDRINUSE: address already in use :::18789`。

**原因：** 端口 18789 已经被其他进程占用，或者上一次 Gateway 没有正常关闭。

**解决方案：**

```bash
# 找到占用端口的进程
# Linux / macOS
lsof -i :18789
# 记下 PID，然后 kill
kill -9 <PID>

# Windows
netstat -ano | findstr 18789
taskkill /PID <PID> /F

# 或者换一个端口
openclaw config set gateway.port 18790
openclaw gateway start
```

### Q15: 怎么完全卸载 OpenClaw？

**现象：** 不再使用 OpenClaw，想彻底从系统中移除所有相关文件（包括程序、配置和数据）。

**解决方案：**

```bash
# 停止 Gateway
openclaw gateway stop

# 卸载 npm 包
npm uninstall -g openclaw

# 删除配置和数据（谨慎操作，不可恢复）
rm -rf ~/.openclaw

# Docker 方式
docker compose down -v
docker rmi openclaw/openclaw:latest
```

---

## 二、消息平台问题

> 📌 **本节包含 10 个问题：**
> [Q16: WhatsApp 频繁断开](#q16-whatsapp-扫码后频繁断开) | [Q17: Telegram Bot 不响应](#q17-telegram-bot-不响应消息) | [Q18: Telegram 群组不回复](#q18-telegram-bot-在群组中不回复) | [Q19: Discord Bot 无法加入](#q19-discord-bot-无法加入服务器) | [Q20: 消息延迟严重](#q20-消息延迟严重发了好久才回复) | [Q21: rate limited](#q21-消息发送失败提示-rate-limited) | [Q22: 飞书收不到消息](#q22-飞书feishulark接入后收不到消息) | [Q23: 控制面板打不开](#q23-控制面板dashboard打不开) | [Q24: 多账号接入](#q24-同一个平台能接入多个账号吗) | [Q25: 图片文件处理](#q25-消息中的图片文件-ai-能处理吗)

### Q16: WhatsApp 扫码后频繁断开

**现象：** 扫码配对成功，但过一会儿就断开，需要反复扫码。

**原因：** WhatsApp Web 协议要求手机端保持在线。如果手机网络不稳定或 WhatsApp 应用被系统杀后台，连接就会断。

**解决方案：**

```bash
# 第一步：把 Gateway 安装为系统服务，保持持续运行
openclaw daemon

# 第二步：检查连接状态
openclaw channels status whatsapp

# 第三步：如果断开了，重新连接
openclaw channels logout whatsapp
openclaw channels login whatsapp

# 第四步：查看断开原因
openclaw logs --limit 50 | grep whatsapp
```

其他注意事项：
- 确保手机上的 WhatsApp 没有被省电模式限制后台运行
- 一个 WhatsApp 账号只能同时连接一个 Web 客户端，如果你在浏览器里也开了 WhatsApp Web，会冲突
- 建议用一个专门的手机号来跑 OpenClaw

### Q17: Telegram Bot 不响应消息

**现象：** 给 Telegram Bot 发消息，没有任何回复。

**原因：** 可能是 Bot Token 配置错误、Bot 没有接收消息的权限、或者 Gateway 没有正常运行。

**解决方案：**

```bash
# 第一步：确认 Gateway 在运行
openclaw status

# 第二步：确认 Bot Token 正确
openclaw config get channels.telegram.botToken
# 去 @BotFather 核对 Token 是否一致

# 第三步：确认 Bot 的隐私模式
# 在 @BotFather 中：
# /mybots → 选择你的 Bot → Bot Settings → Group Privacy → Turn off
# 关闭隐私模式后，Bot 才能接收群组中的所有消息

# 第四步：检查日志
openclaw logs --limit 50 | grep telegram

# 第五步：重新连接
openclaw channels logout telegram
openclaw channels login telegram
```

### Q18: Telegram Bot 在群组中不回复

**现象：** Bot 在私聊中正常回复，但在群组中不响应。

**原因：** Telegram Bot 默认开启隐私模式，在群组中只能收到 @提及 和 /命令。

**解决方案：**

1. 在 @BotFather 中关闭隐私模式（见 Q17）
2. 或者在群组中 @提及 Bot 来触发回复
3. 在群组配置中设置激活模式（通过聊天命令 `/activation mention` 或 `/activation always` 切换）

### Q19: Discord Bot 无法加入服务器

**现象：** 用邀请链接添加 Bot 时报错 `Missing Permissions`。

**原因：** Bot 的 OAuth2 权限配置不完整。

**解决方案：**

1. 去 [Discord Developer Portal](https://discord.com/developers/applications)
2. 选择你的应用 → OAuth2 → URL Generator
3. 勾选以下权限：
   - `bot`
   - `applications.commands`
   - `Send Messages`
   - `Read Message History`
   - `Embed Links`
   - `Attach Files`
4. 用生成的新链接重新邀请 Bot

```bash
# 配置 Discord Bot Token（注意：Discord 用的字段是 token，不是 botToken）
openclaw config set channels.discord.token "your-discord-bot-token"
openclaw channels logout discord
openclaw channels login discord
```

### Q20: 消息延迟严重（发了好久才回复）

**现象：** 发消息后要等 10 秒甚至更久才收到回复。

**原因：** 延迟可能来自多个环节 — 网络、模型 API 响应时间、消息队列积压。

**解决方案：**

```bash
# 第一步：排查是哪个环节慢
openclaw logs --limit 20
# 看日志中的时间戳，判断延迟发生在哪里

# 第二步：测试模型 API 延迟
openclaw health
# 如果 API 延迟高，考虑换模型或换提供商

# 第三步：检查是否有消息积压
openclaw sessions list

# 第四步：优化措施
# 使用更快的模型
openclaw config set agents.defaults.model "openai/gpt-5.2-mini"
# 减少系统提示词长度（Token 越少，响应越快）
# 精简 ~/.openclaw/workspace/SOUL.md 的内容
```

### Q21: 消息发送失败，提示 "rate limited"

**现象：** 发消息时报错 `429 Too Many Requests` 或 `rate limited`。

**原因：** 消息平台有发送频率限制。WhatsApp 尤其严格，短时间内发太多消息会被限流。

**解决方案：**

```bash
# 消息平台的限流是平台侧限制，OpenClaw 没有内置速率限制配置
# 解决方案：
# 1. 减少消息发送频率，避免触发平台限流
# 2. 等待限流解除后自动重试
# 3. 如果是 API 限流（429），参考 Q27 配置模型故障转移
```

### Q22: 飞书（Feishu/Lark）接入后收不到消息

**现象：** 飞书 Bot 配置完成，但收不到用户消息。

**原因：** 飞书的事件订阅配置不完整，或者回调地址不可达。

**解决方案：**

```bash
# 第一步：确认 Gateway 的公网地址可达
curl https://your-domain.com:18789/health

# 第二步：在飞书开放平台配置事件订阅
# 事件订阅 URL：https://your-domain.com:18789/webhook/feishu
# 需要订阅的事件：im.message.receive_v1

# 第三步：检查日志
openclaw logs --limit 50 | grep feishu

# 第四步：确认 Bot 权限
# 飞书开放平台 → 应用权限 → 确保开启了：
# - 获取与发送单聊、群组消息
# - 读取用户信息
```

### Q23: 控制面板（Dashboard）打不开

**现象：** 浏览器访问 `http://localhost:18789` 显示无法连接。

**原因：** Gateway 没有运行，或者端口被防火墙拦截。

**解决方案：**

```bash
# 第一步：确认 Gateway 在运行
openclaw status

# 如果没运行，启动它
openclaw gateway --port 18789

# 第二步：检查端口
# Linux / macOS
lsof -i :18789
# Windows
netstat -an | findstr 18789

# 第三步：如果是远程服务器，检查防火墙
# Ubuntu
sudo ufw allow 18789
# CentOS
sudo firewall-cmd --add-port=18789/tcp --permanent
sudo firewall-cmd --reload

# 第四步：重启 Gateway（停止后重新启动，或使用聊天命令 /restart）
openclaw gateway --port 18789
```

### Q24: 同一个平台能接入多个账号吗？

**说明：** 可以。OpenClaw 支持同一平台的多个 Channel 实例。

```bash
# 添加第二个 WhatsApp 账号
openclaw channels add whatsapp --name "work-whatsapp"
openclaw channels add whatsapp --name "personal-whatsapp"

# 查看所有 Channel
openclaw channels list
```

每个 Channel 独立运行，有自己的配对状态和消息队列。

### Q25: 消息中的图片/文件 AI 能处理吗？

**说明：** 取决于你使用的模型。支持多模态的模型（如 GPT-5.2、Claude Sonnet 4.6）可以处理图片。

```bash
# 多模态能力取决于你使用的模型，不需要额外配置
# 支持多模态的模型（如 GPT-5.2、Claude Sonnet 4.6）会自动处理图片
# 文件大小限制取决于消息平台本身的限制
```

不支持多模态的模型收到图片时，会提示用户发送文字。

---

## 三、模型和 AI 问题

> 📌 **本节包含 10 个问题：**
> [Q26: API 401 报错](#q26-api-调用报错-401-unauthorized) | [Q27: API 429 限流](#q27-报错-429-too-many-requestsapi-限流) | [Q28: 模型回复慢](#q28-模型回复很慢) | [Q29: Token 超限](#q29-token-超限报错context-length-exceeded) | [Q30: Ollama 连不上](#q30-ollama-本地模型连不上) | [Q31: 本地模型质量差](#q31-本地模型回复质量差) | [Q32: 国产模型配置](#q32-怎么使用国产模型通义千问kimi智谱等) | [Q33: 模型故障转移](#q33-怎么配置模型故障转移fallback) | [Q34: 控制 API 费用](#q34-api-费用太高怎么控制成本) | [Q35: 不同对话用不同模型](#q35-怎么让不同的对话用不同的模型)

### Q26: API 调用报错 401 Unauthorized

**现象：** 发消息后 AI 不回复，日志中出现 `401 Unauthorized` 或 `Invalid API Key`。

**原因：** API Key 无效、过期、或者余额不足。

**解决方案：**

```bash
# 第一步：检查 Key 是否配置正确
# 推荐通过环境变量设置：
echo $OPENAI_API_KEY
# 确认 Key 没有多余的空格或换行

# 第二步：测试 Key 是否有效
openclaw health
# 如果报错，说明 Key 有问题

# 第三步：去提供商后台检查
# OpenAI: https://platform.openai.com/account/api-keys
# Anthropic: https://console.anthropic.com/settings/keys
# 确认 Key 没有被撤销，账户余额充足

# 第四步：重新设置 Key
export OPENAI_API_KEY="sk-proj-new-key-here"
# 然后重启 Gateway
```

### Q27: 报错 429 Too Many Requests（API 限流）

**现象：** 高频使用时出现 `429` 错误，AI 间歇性不回复。

**原因：** 超过了模型提供商的 API 调用频率限制（RPM/TPM）。

**解决方案：**

```bash
# 方案一：启用模型故障转移（推荐）
# 在 ~/.openclaw/openclaw.json 中配置：
# {
#   "agents": {
#     "defaults": {
#       "model": {
#         "primary": "openai/gpt-5.2",
#         "fallbacks": ["anthropic/claude-sonnet-4-6", "openai/gpt-5.2-mini"]
#       }
#     }
#   }
# }

# 方案二：使用 OpenRouter（聚合多个提供商，限流更宽松）
export OPENROUTER_API_KEY="sk-or-xxxxx"
openclaw config set agents.defaults.model "openrouter/openai/gpt-5.2"

# 方案三：升级 API 账户等级（更高的 RPM/TPM 限制）
# 去各提供商控制台升级
```

### Q28: 模型回复很慢

**现象：** 发送消息后，AI 要等 10-30 秒甚至更久才开始回复。在终端日志中可以看到请求已发出，但响应迟迟不返回。

**原因：** 大模型本身推理就需要时间，加上网络延迟，响应时间会更长。

**解决方案：**

```bash
# 方案一：换用更快的小模型
openclaw config set agents.defaults.model "openai/gpt-5.2-mini"
# gpt-5.2-mini 速度是 gpt-5.2 的 3-5 倍，日常对话足够用

# 方案二：流式响应默认已启用
# OpenClaw 默认使用流式输出（边生成边发送），无需额外配置

# 方案三：减少系统提示词长度
# 精简 SOUL.md 中不必要的指令，精简 MEMORY.md 内容
openclaw agents list
# 查看当前 Agent 列表

# 方案四：使用本地模型（延迟最低）
ollama pull llama3.1:8b
openclaw config set models.providers.ollama.baseUrl "http://127.0.0.1:11434"
openclaw config set agents.defaults.model "ollama/llama3.1:8b"

# 方案五：检查网络延迟
ping api.openai.com
# 如果延迟高，考虑使用代理或换区域更近的提供商
```

### Q29: Token 超限报错（context length exceeded）

**现象：** 对话到一定长度后报错 `maximum context length exceeded` 或 `token limit`。

**原因：** 每个模型都有上下文窗口限制。对话历史 + 系统提示 + 记忆文件的总 Token 数超过了模型限制。

**解决方案：**

```bash
# 查看当前会话的 Token 使用情况
openclaw sessions list

# 方案一：使用 /compact 命令手动压缩上下文
# 在聊天界面中发送 /compact，OpenClaw 会自动压缩旧消息
# 也可以配置自动压缩阈值：
# 在 ~/.openclaw/openclaw.json 中设置：
# {
#   "agents": {
#     "defaults": {
#       "compaction": {
#         "reserveTokensFloor": 20000
#       }
#     }
#   }
# }
# reserveTokensFloor 越大，压缩越激进

# 方案二：使用上下文窗口更大的模型
# Claude Sonnet 4.6: 200K tokens
# Gemini 3.1 Pro: 1M tokens
# GPT-5.2: 128K tokens
openclaw config set agents.defaults.model "anthropic/claude-sonnet-4-6"

# 方案三：手动清理会话
openclaw sessions cleanup
# 或让 AI 总结后开新会话（在聊天界面发送 /new）
```

### Q30: Ollama 本地模型连不上

**现象：** 配置了 Ollama 但 OpenClaw 报错 `ECONNREFUSED` 或 `connection refused`。

**原因：** Ollama 服务没有启动，或者监听地址配置不对。

**解决方案：**

```bash
# 第一步：确认 Ollama 在运行
ollama serve
# 或者检查是否已经在后台运行
curl http://127.0.0.1:11434/api/tags

# 第二步：确认有可用的模型
ollama list
# 如果没有模型，先拉一个
ollama pull llama3.1:8b

# 第三步：配置 OpenClaw 连接 Ollama
openclaw config set models.providers.ollama.baseUrl "http://127.0.0.1:11434"
openclaw config set agents.defaults.model "ollama/llama3.1:8b"

# 第四步：如果 Ollama 和 OpenClaw 不在同一台机器
# 需要让 Ollama 监听所有网卡
OLLAMA_HOST=0.0.0.0 ollama serve
# 然后配置远程地址
openclaw config set models.providers.ollama.baseUrl "http://192.168.1.100:11434"
```

### Q31: 本地模型回复质量差

**现象：** 用 Ollama 跑本地模型，回复经常答非所问或质量很低。

**原因：** 小参数模型的能力有限，尤其是中文能力。

**解决方案：**

```bash
# 方案一：换用更大的模型（需要更多内存/显存）
ollama pull llama3.1:70b    # 需要 64GB+ 内存
ollama pull qwen2.5:14b     # 中文能力更好

# 方案二：调整模型参数（在 API 调用时传入，非配置文件）
# temperature 和 topP 等参数取决于模型提供商
# 本地模型可以在 Ollama 的 Modelfile 中设置默认参数
# 例如创建自定义 Modelfile：
# FROM llama3.1:8b
# PARAMETER temperature 0.7
# PARAMETER top_p 0.9

# 方案三：优化系统提示词
# 本地小模型对提示词更敏感，要写得简洁明确
# 在 SOUL.md 中精简指令，避免复杂的多步骤指令

# 方案四：混合策略 — 简单任务用本地模型，复杂任务用云端
# 通过模型故障转移实现：本地模型作为默认，复杂任务手动切换
# 在 ~/.openclaw/openclaw.json 中配置：
# {
#   "agents": {
#     "defaults": {
#       "model": {
#         "primary": "ollama/llama3.1:8b",
#         "fallbacks": ["openai/gpt-5.2"]
#       }
#     }
#   }
# }
```

### Q32: 怎么使用国产模型（通义千问、Kimi、智谱等）？

**解决方案：**

```bash
# 国产模型大多可以通过 OpenAI 兼容接口或 OpenRouter 接入

# 通义千问（阿里云 DashScope）— 通过 OpenAI 兼容接口
# 在 ~/.openclaw/openclaw.json 中配置：
# {
#   "models": {
#     "providers": {
#       "dashscope": {
#         "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1"
#       }
#     }
#   },
#   "agents": { "defaults": { "model": "dashscope/qwen-max" } }
# }
# API Key 通过环境变量设置（参考 DashScope 文档）

# Moonshot / Kimi — 通过 OpenAI 兼容接口
# baseUrl: "https://api.moonshot.cn/v1"

# DeepSeek — 通过 OpenAI 兼容接口
# baseUrl: "https://api.deepseek.com/v1"
# v2026.4.24+ 新增 DeepSeek V4 Flash（默认）和 V4 Pro 模型

# 最简单的方式：通过 OpenRouter 一站式接入所有国产模型
export OPENROUTER_API_KEY="sk-or-xxxxx"
openclaw config set agents.defaults.model "openrouter/deepseek/deepseek-chat"
```

国产模型的优势：不需要代理、中文能力强、价格便宜。推荐中国用户优先考虑。

### Q33: 怎么配置模型故障转移（Fallback）？

**说明：** 当主模型不可用时，自动切换到备用模型，保证服务不中断。

```bash
# 在 ~/.openclaw/openclaw.json 中配置 Fallback 链：
# {
#   "agents": {
#     "defaults": {
#       "model": {
#         "primary": "openai/gpt-5.2",
#         "fallbacks": [
#           "anthropic/claude-sonnet-4-6",
#           "openai/gpt-5.2-mini"
#         ]
#       }
#     }
#   }
# }
# 当主模型返回 5xx、超时或 429 限流时，自动按顺序尝试备用模型

# 查看 Fallback 状态
openclaw models fallbacks list
openclaw models status
```

### Q34: API 费用太高怎么控制成本？

**解决方案：**

```bash
# 方案一：在模型提供商控制台设置预算上限
# OpenAI: Settings > Limits 设置月度上限
# Anthropic: Plans & Billing 查看用量
# Google Cloud: 设置 API 配额和预算提醒
# OpenClaw 本身没有内置预算控制配置

# 方案二：使用更便宜的模型
# gpt-5.2-mini 价格是 gpt-5.2 的 1/10
openclaw config set agents.defaults.model "openai/gpt-5.2-mini"

# 方案三：精简记忆文件减少 Token 消耗
# MEMORY.md 建议控制在 500 行以内
# 精简 SOUL.md 系统提示词

# 方案四：查看系统状态
openclaw status

# 方案五：本地模型零成本
ollama pull llama3.1:8b
openclaw config set agents.defaults.model "ollama/llama3.1:8b"
```

### Q35: 怎么让不同的对话用不同的模型？

**说明：** 可以为不同的 Agent 配置不同的模型，通过在配置文件中为每个 Agent 指定独立的模型。

```bash
# 方案一：为不同 Agent 配置不同模型
# 在 ~/.openclaw/openclaw.json 中配置：
# {
#   "agents": {
#     "defaults": {
#       "model": "openai/gpt-5.2-mini"
#     },
#     "list": [
#       { "id": "coding", "model": "anthropic/claude-sonnet-4-6" },
#       { "id": "casual", "model": "openai/gpt-5.2-mini" }
#     ]
#   }
# }

# 方案二：使用模型别名快速切换
openclaw models aliases add code-review "anthropic/claude-opus-4-6"
openclaw models aliases add quick-chat "openai/gpt-5.2-mini"

# 方案三：通过 bindings 将不同 Channel 路由到不同 Agent
# 每个 Agent 使用各自配置的模型
# 详见 08-多Agent协作指南.md
```

---

## 四、技能和工具问题

> 📌 **本节包含 10 个问题：**
> [Q36: 技能不生效](#q36-技能skill不生效ai-不执行) | [Q37: 自定义技能报错](#q37-自定义技能报错) | [Q38: 工具执行失败](#q38-工具tool执行失败) | [Q39: 禁用工具](#q39-怎么禁用某个工具) | [Q40: 添加新工具](#q40-怎么给-ai-添加新工具) | [Q41: 技能中途中断](#q41-技能执行到一半中断了) | [Q42: 查看工具调用](#q42-怎么查看-ai-调用了哪些工具) | [Q43: 内置技能列表](#q43-内置技能列表在哪里看) | [Q44: 技能冲突](#q44-技能之间会冲突吗) | [Q45: 分享技能](#q45-怎么分享自定义技能给别人)

### Q36: 技能（Skill）不生效，AI 不执行

**现象：** 你发消息让 AI 执行某个技能（比如「帮我搜索 xxx」），但 AI 只是用文字回复了一段话，并没有真正调用工具去执行操作。日志中也看不到工具调用记录。

**原因：** 技能没有正确加载，或者触发条件不匹配。

**解决方案：**

```bash
# 第一步：检查技能是否已加载
openclaw skills list
# 确认目标技能在列表中且状态为 enabled

# 第二步：检查技能的触发关键词
openclaw skills info <skill-name>
# 看 triggers 字段，确认你的消息包含触发词

# 第三步：手动触发技能测试
openclaw skills check <skill-name> --input "测试消息"

# 第四步：重新加载技能
openclaw skills list
```

### Q37: 自定义技能报错

**现象：** 在 `~/.openclaw/workspace/skills/` 目录下创建了自定义技能的 `.md` 文件，但执行 `openclaw skills list` 时该技能未出现，或者出现 `skill parse error`、`invalid skill format` 等报错信息。

**原因：** 技能文件格式不对，或者引用了不存在的工具。

**解决方案：**

```bash
# 第一步：检查技能文件格式
openclaw skills check ~/.openclaw/workspace/skills/my-skill.md

# 第二步：确认引用的工具都存在
openclaw skills list
# 对照技能文件中引用的工具名称

# 技能文件的基本格式：
cat ~/.openclaw/workspace/skills/my-skill.md
```

正确的技能文件结构：

```markdown
---
name: my-custom-skill
description: 我的自定义技能
triggers:
  - "帮我做xxx"
  - "执行xxx"
tools:
  - file_read
  - file_write
  - web_search
---

## 指令

当用户要求做 xxx 时，按以下步骤执行：

1. 先搜索相关信息
2. 读取必要的文件
3. 生成结果并写入文件
```

### Q38: 工具（Tool）执行失败

**现象：** AI 回复中显示「正在调用 xxx 工具」，但随后报错 `tool execution failed`、`permission denied` 或 `tool not found`，操作没有完成。

**原因：** 工具缺少必要的权限或依赖。

**解决方案：**

```bash
# 第一步：检查工具状态
openclaw doctor
# 诊断安全和配置问题

# 第二步：测试单个工具
openclaw skills check <skill-name>

# 第三步：检查工具依赖
openclaw skills info <skill-name>
# 看 dependencies 字段，确认依赖都已安装

# 第四步：常见工具问题
# web_search 需要网络连接
# file_write 需要目标目录有写权限
# shell_exec 需要在配置中启用（默认禁用，出于安全考虑）
```

### Q39: 怎么禁用某个工具？

**说明：** 出于安全考虑，你可能想禁用某些危险工具。

```bash
# 工具权限通过沙箱模式控制
# 在 ~/.openclaw/openclaw.json 中配置沙箱：
# {
#   "agents": {
#     "defaults": {
#       "sandbox": { "mode": "all" }
#     }
#   }
# }
# sandbox.mode: "off"（默认，不限制）| "non-main"（限制非主 Agent）| "all"（限制所有 Agent）
# 沙箱模式会限制文件系统访问和命令执行

# 也可以在 SOUL.md 中明确告诉 AI 不要使用某些工具
# 例如："永远不要执行 shell 命令，不要删除文件"

# 查看当前工具权限配置
openclaw doctor
```

### Q40: 怎么给 AI 添加新工具？

**说明：** OpenClaw 支持通过 MCP（Model Context Protocol）协议接入外部工具。

```bash
# 方案一：使用内置的 MCP 服务器
openclaw plugins

# 方案二：接入第三方 MCP 服务器
# 在 ~/.openclaw/openclaw.json 中配置 MCP 服务器连接

# 方案三：自己写工具（TypeScript）
# 在 ~/.openclaw/workspace/tools/ 下创建工具文件
# 参考文档：https://docs.openclaw.ai/tools/custom
```

### Q41: 技能执行到一半中断了

**现象：** AI 在执行一个多步骤技能时（比如「搜索 → 读取文件 → 生成报告」），执行到中间某一步后突然停下来，不再继续后续步骤，也没有给出完成提示。

**原因：** 可能是 Token 限制导致输出被截断，或者某个中间步骤失败了。

**解决方案：**

```bash
# 第一步：查看会话日志，找到中断点
# 使用前台模式运行 Gateway 查看详细日志：
openclaw gateway --port 18789 --verbose

# 第二步：Token 限制导致截断的解决方案
# 不同模型有不同的最大输出限制（如 GPT-5.2 最大 32K tokens）
# 换用输出限制更大的模型，或精简系统提示词

# 第三步：让 AI 继续
# 直接发消息 "继续" 或 "请继续执行"

# 第四步：如果是工具执行失败导致的中断
openclaw skills check <failed-tool-name>
# 修复工具问题后重试
```

### Q42: 怎么查看 AI 调用了哪些工具？

**解决方案：**

```bash
# 查看最近会话的工具调用记录
openclaw sessions list

# 实时查看工具调用（调试模式）
openclaw logs --follow
# 日志中会显示每次工具调用的详细信息

# 查看系统状态
openclaw status
```

### Q43: 内置技能列表在哪里看？

**解决方案：**

```bash
# 列出所有技能（包括内置技能）
openclaw skills list

# 查看某个技能的详细说明
openclaw skills info <skill-name>
```

### Q44: 技能之间会冲突吗？

**说明：** 如果多个技能的触发条件重叠，可能会出现冲突。OpenClaw 会按优先级选择。

```bash
# 查看技能列表
openclaw skills list

# 查看特定技能的详细信息
openclaw skills info <skill-name>
```

### Q45: 怎么分享自定义技能给别人？

**解决方案：**

```bash
# 查看技能文件
openclaw skills list

# 技能文件位于 ~/.openclaw/workspace/skills/ 目录
# 可以直接复制 .md 文件来分享技能

# 查看社区技能库
# https://github.com/openclaw/openclaw-skills
```

---

## 五、部署和运维问题

> 📌 **本节包含 10 个问题：**
> [Q46: Docker 容器立即退出](#q46-docker-容器启动后立即退出) | [Q47: 容器内存过高](#q47-docker-容器内存占用过高) | [Q48: 数据卷备份](#q48-docker-数据卷怎么备份) | [Q49: 自动重启](#q49-gateway-进程崩溃后怎么自动重启) | [Q50: 查看日志](#q50-日志在哪里看怎么排查问题) | [Q51: 监控运行状态](#q51-怎么监控-openclaw-的运行状态) | [Q52: 磁盘空间清理](#q52-磁盘空间不足怎么清理) | [Q53: 多服务器部署](#q53-怎么在多台服务器上部署) | [Q54: 设置 HTTPS](#q54-怎么设置-https) | [Q55: 自动更新](#q55-怎么配置自动更新)

### Q46: Docker 容器启动后立即退出

**现象：** 执行 `docker compose up -d` 后，运行 `docker ps` 看不到 OpenClaw 容器，用 `docker ps -a` 查看发现容器状态为 `Exited (1)` 或其他非零退出码。

**原因：** 配置文件缺失、端口冲突、或者环境变量没设置。

**解决方案：**

```bash
# 第一步：查看容器退出日志
docker compose logs openclaw

# 第二步：常见原因排查
# 原因 1：配置文件不存在
ls ./data/openclaw.json  # 确认挂载的配置文件存在

# 原因 2：端口被占用
lsof -i :18789
# 如果被占用，修改 docker-compose.yml 中的端口映射

# 原因 3：环境变量缺失
# 确认 .env 文件存在且包含必要变量
cat .env

# 第三步：用前台模式启动，方便看日志
docker compose up  # 不加 -d
```

### Q47: Docker 容器内存占用过高

**现象：** 运行 `docker stats` 发现 OpenClaw 容器的内存使用量持续增长，从几百 MB 涨到好几 GB，甚至导致宿主机变卡或 OOM（Out of Memory）被系统杀掉。

**原因：** 连接了太多平台、会话数据积累、或者存在内存泄漏。

> v2026.4.20+ 默认启用了会话维护（Sessions/Maintenance）的条目上限和基于时间的自动清理，可以有效防止 OOM。如果你从旧版本升级，建议确认此特性已启用。

**解决方案：**

```bash
# 查看容器资源使用
docker stats openclaw

# 方案一：限制容器内存
# 在 docker-compose.yml 中添加：
# deploy:
#   resources:
#     limits:
#       memory: 1G

# 方案二：清理会话数据
docker exec openclaw openclaw sessions cleanup

# 方案三：减少同时连接的平台数量

# 方案四：定期重启容器（临时方案）
# 配置 crontab
# 0 4 * * * docker compose restart openclaw
```

### Q48: Docker 数据卷怎么备份？

**解决方案：**

```bash
# 方案一：直接备份挂载目录
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz ./data/

# 方案二：备份 Docker volume
docker run --rm \
  -v openclaw_data:/source \
  -v $(pwd):/backup \
  alpine tar -czf /backup/openclaw-data.tar.gz -C /source .

# 方案三：自动化备份脚本
# 建议配合 crontab 每天自动备份
# 0 3 * * * /path/to/backup-script.sh
```

### Q49: Gateway 进程崩溃后怎么自动重启？

**解决方案：**

```bash
# 方案一：安装为 systemd 服务（Linux 推荐）
openclaw daemon
# 这会创建 systemd service，崩溃后自动重启

# 查看服务状态
systemctl status openclaw-gateway

# 方案二：Docker 自动重启
# 在 docker-compose.yml 中设置：
# restart: unless-stopped

# 方案三：用 PM2 管理（Node.js 生态）
npm install -g pm2
pm2 start "openclaw gateway --port 18789" --name openclaw
pm2 save
pm2 startup  # 开机自启
```

### Q50: 日志在哪里看？怎么排查问题？

**解决方案：**

```bash
# 最直接的方式：前台运行 Gateway 并开启 --verbose
openclaw gateway --port 18789 --verbose
# 所有日志实时输出到终端

# 按关键词过滤（通过管道 grep）
# openclaw gateway --port 18789 --verbose 2>&1 | grep "error"

# Docker 环境
docker compose logs -f openclaw
docker compose logs --tail 100 openclaw

# 日志文件位置（取决于 logging 配置）
# 默认日志输出到 stdout/stderr
# 可以通过 logging.file 配置写入文件

# 调整日志级别（排查问题时用 debug）
openclaw config set logging.level "debug"
# 排查完记得改回来
openclaw config set logging.level "info"
```

### Q51: 怎么监控 OpenClaw 的运行状态？

**解决方案：**

```bash
# 内置健康检查
curl http://localhost:18789/health

# 查看详细状态
openclaw status

# 输出示例：
# Gateway: running (uptime: 3d 12h)
# Channels: 3 connected, 0 error
# Sessions: 42 active
# Memory: 256 MB
# CPU: 2%

# 配置外部监控（推荐 UptimeRobot 或类似服务）
# 监控 URL: http://your-server:18789/health
# 检查间隔: 5 分钟
```

### Q52: 磁盘空间不足怎么清理？

**解决方案：**

```bash
# 查看 OpenClaw 占用的磁盘空间
du -sh ~/.openclaw/
du -sh ~/.openclaw/*/  # 分目录查看

# 清理会话日志（最占空间的部分）
openclaw sessions cleanup

# 清理旧的记忆日志
find ~/.openclaw/workspace/memory/ -name "*.md" -mtime +60 -delete

# Docker 环境清理
docker system prune -f          # 清理无用镜像和容器
docker volume prune -f          # 清理无用数据卷（谨慎）

# 查看清理后的空间
du -sh ~/.openclaw/
```

### Q53: 怎么在多台服务器上部署？

**说明：** OpenClaw 目前是单实例架构，不支持原生集群部署。但你可以通过以下方式实现多节点：

```bash
# 方案一：每台服务器独立部署，连接不同的平台
# 服务器 A：负责 WhatsApp
# 服务器 B：负责 Telegram + Discord

# 方案二：用反向代理做负载均衡（实验性）
# Nginx 配置示例：
# upstream openclaw {
#     server 192.168.1.10:18789;
#     server 192.168.1.11:18789 backup;
# }

# 方案三：共享配置和记忆（通过 NFS 或对象存储）
# 把 ~/.openclaw/ 挂载到共享存储
```

### Q54: 怎么设置 HTTPS？

**解决方案：**

```bash
# 方案一：用反向代理（推荐）
# Nginx + Let's Encrypt
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d openclaw.yourdomain.com

# Nginx 配置
# server {
#     listen 443 ssl;
#     server_name openclaw.yourdomain.com;
#     location / {
#         proxy_pass http://127.0.0.1:18789;
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection "upgrade";
#     }
# }

# 方案二：OpenClaw 内置 TLS
# GatewayTlsConfig 只有 certPath 和 keyPath 两个字段，没有 enabled 开关
# 配置了证书路径即视为启用 TLS
openclaw config set gateway.tls.certPath "/path/to/cert.pem"
openclaw config set gateway.tls.keyPath "/path/to/key.pem"
# 重启 Gateway 使配置生效
openclaw gateway --port 18789
```

### Q55: 怎么配置自动更新？

**解决方案：**

```bash
# npm 方式：用 crontab 定期检查更新（更新后需要重启 Gateway）
# 0 2 * * 0 npm update -g openclaw && pkill -f "openclaw gateway" && openclaw gateway --port 18789 &

# Docker 方式：用 Watchtower 自动更新
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 86400 \
  openclaw

# 手动检查是否有新版本
openclaw --version
npm view openclaw version
```

---

## 六、记忆系统问题

> 📌 **本节包含 3 个问题：**
> [Q56: AI 不记得之前说的话](#q56-ai-不记得之前说的话) | [Q57: 记忆文件太大](#q57-记忆文件太大导致-token-超限) | [Q58: 多 Agent 共享记忆](#q58-怎么在多个-agent-之间共享记忆)

### Q56: AI 不记得之前说的话

**现象：** 你之前告诉 AI「我叫小明」或「我喜欢用 Python」，但下次对话时 AI 完全不记得这些信息，像是第一次跟你聊天一样。

**原因：** OpenClaw 的记忆是基于 Markdown 文件的。如果信息没有被写入记忆文件，下次会话就不会加载。

**解决方案：**

```bash
# 第一步：检查记忆文件是否存在
ls ~/.openclaw/workspace/memory/
cat ~/.openclaw/workspace/MEMORY.md

# 第二步：主动让 AI 记住
# 发消息："记住：我喜欢用 Python，不喜欢 Java"
# AI 会把这条信息写入 MEMORY.md

# 第三步：确认记忆刷新机制（compaction 时自动保存重要信息）
openclaw config get agents.defaults.compaction.memoryFlush
# 确保 memoryFlush.enabled 是 true

# 第四步：手动编辑记忆文件
nano ~/.openclaw/workspace/MEMORY.md
# 把重要信息直接写进去

# 第五步（v2026.4.12+）：启用 Active Memory 插件
# Active Memory 插件可自动召回、提升和整理记忆
# 通过 openclaw plugins 查看是否已启用
```

### Q57: 记忆文件太大导致 Token 超限

**现象：** 使用一段时间后，每次新对话刚开始就报错 `token limit exceeded`，或者发现 API 费用突然增加。检查发现 `~/.openclaw/workspace/MEMORY.md` 文件已经有几百甚至上千行。

**解决方案：**

```bash
# 查看记忆文件大小
wc -l ~/.openclaw/workspace/MEMORY.md
du -sh ~/.openclaw/workspace/memory/

# 方案一：精简 MEMORY.md
# 删除过时的、不再需要的信息
nano ~/.openclaw/workspace/MEMORY.md

# 方案二：手动归档旧日志（OpenClaw 没有内置自动清理配置）
mkdir -p ~/.openclaw/workspace/memory/archive
mv ~/.openclaw/workspace/memory/2025-*.md ~/.openclaw/workspace/memory/archive/
# 归档后运行 openclaw memory index 重建索引

# 方案三：控制 MEMORY.md 大小（建议 500 行 / 3000 tokens 以内）
# MEMORY.md 每次会话都会加载到上下文，太大会挤占对话空间
wc -l ~/.openclaw/workspace/MEMORY.md
```

### Q58: 怎么在多个 Agent 之间共享记忆？

**说明：** 默认情况下，所有 Agent 共享同一个 workspace 和记忆目录。如果你想隔离，在配置文件中为不同 Agent 指定独立的 workspace：

```jsonc
// ~/.openclaw/openclaw.json
{
  "agents": {
    "list": [
      {
        "id": "my-agent",
        "workspace": "~/.openclaw/workspace-my-agent"
      }
    ]
  }
}
```

每个 Agent 的 workspace 下有独立的 `MEMORY.md` 和 `memory/` 目录，实现完全隔离。如果需要共享部分记忆，可以用符号链接指向同一个 `MEMORY.md` 文件。

---

## 七、安全和隐私问题

> 📌 **本节包含 6 个问题：**
> [Q59: API Key 泄露风险](#q59-api-key-会不会泄露) | [Q60: 聊天记录存储](#q60-聊天记录存在哪里会被发送到第三方吗) | [Q61: Gateway Token](#q61-gateway-token-是什么必须设置吗) | [Q62: 限制对话权限](#q62-怎么限制谁能跟-ai-对话) | [Q63: 防止危险操作](#q63-怎么防止-ai-执行危险操作) | [Q64: 安全漏洞](#q64-openclaw-有已知的安全漏洞吗)

### Q59: API Key 会不会泄露？

**说明：** OpenClaw 把 API Key 存储在本地配置文件中（`~/.openclaw/openclaw.json`），不会上传到任何服务器。

**安全建议：**

```bash
# 检查配置文件权限
ls -la ~/.openclaw/openclaw.json
# 应该是 600（只有当前用户可读写）

# 修复权限
chmod 600 ~/.openclaw/openclaw.json

# 更安全的方式：用环境变量代替配置文件
export OPENAI_API_KEY="sk-proj-xxxxx"
# 把环境变量写入 ~/.bashrc 或 ~/.zshrc
# 不要把 Key 写入任何会被 git 追踪的文件
```

### Q60: 聊天记录存在哪里？会被发送到第三方吗？

**说明：** 聊天记录存储在本地 `~/.openclaw/` 目录中。消息内容只会发送到你配置的 AI 模型提供商（如 OpenAI、Anthropic）。

OpenClaw 本身不收集任何用户数据。但要注意：
- 你发给 AI 的消息会被模型提供商处理（参考各提供商的隐私政策）
- 如果你用 OpenRouter 等聚合服务，消息会经过中间层
- 本地模型（Ollama）的数据完全不出本机

### Q61: Gateway Token 是什么？必须设置吗？

**说明：** Gateway Token 是访问 OpenClaw Gateway 的认证凭证。如果不设置，任何知道你 Gateway 地址的人都能连接并发送消息。

```bash
# 必须设置！（注意：正确的配置路径是 gateway.auth.token）
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"

# 或者手动设置一个强密码
openclaw config set gateway.auth.token "your-strong-random-token-here"

# 通过环境变量设置
export OPENCLAW_GATEWAY_TOKEN="your-strong-random-token-here"
```

### Q62: 怎么限制谁能跟 AI 对话？

**解决方案：**

```bash
# 方案一：配对系统（默认开启）
# 陌生人发消息需要你手动批准
openclaw pairing list          # 查看待批准的联系人
openclaw pairing approve user1 # 批准
# 不批准的联系人会保持在待审列表中

# 方案二：白名单模式（通过 channels 配置 allowFrom）
# 在 ~/.openclaw/openclaw.json 中配置：
# {
#   "channels": {
#     "whatsapp": { "dmPolicy": "pairing", "allowFrom": ["+15555550123"] },
#     "telegram": { "dmPolicy": "pairing", "allowFrom": ["123456789"] }
#   }
# }

# 方案三：查看和管理配对状态
openclaw pairing list --approved
```

### Q63: 怎么防止 AI 执行危险操作？

**解决方案：**

```bash
# 第一步：启用沙箱模式限制工具执行
# sandbox.mode 可选值："off"（关闭）| "non-main"（非主 Agent 隔离）| "all"（全部隔离）
openclaw config set agents.defaults.sandbox.mode "all"

# 第二步：通过 SOUL.md 明确告诉 AI 哪些操作不能做
# 编辑 ~/.openclaw/workspace/SOUL.md，添加安全规则：
# ## 安全规则
# - 不要执行任何删除文件的操作
# - 不要执行 shell 命令，除非用户明确要求
# - 涉及文件修改前必须先确认

# 第三步：追踪所有操作（用 Git 管理 workspace）
cd ~/.openclaw/workspace && git init && git add . && git commit -m "snapshot"
# 之后可以用 git diff 查看 AI 做了什么改动

# 第四步：查看会话日志中的工具调用记录
# 会话日志在 ~/.openclaw/agents/main/sessions/*.jsonl
# 记录了所有工具调用，包括参数和结果
```

### Q64: OpenClaw 有已知的安全漏洞吗？

**说明：** OpenClaw 在 2026 年初曾披露过 CVE 安全漏洞，社区已经修复。v2026.4.x 系列持续加强了安全防护，主要包括：

- **SSRF 防护**（v2026.4.2+）：集中化的请求传输策略，阻止对私有网络的导航重定向
- **环境变量清理**（v2026.4.7+）：自动拦截危险的环境变量覆盖
- **Owner-Enforced Commands**（v2026.4.5+）：白名单修改需要所有者身份验证
- **Shell Wrapper 检测**（v2026.4.1+）：扩展了对 shell 包装命令的识别和 env-argv 注入拦截
- **Hook 失败模式**（v2026.4.5+）：Hook 崩溃时采用 fail-closed 策略，不会默认放行

建议：

```bash
# 始终保持最新版本
npm update -g openclaw

# 查看安全公告
# https://github.com/openclaw/openclaw/security/advisories

# 运行安全审计
openclaw security audit
openclaw security audit --deep  # 包含实时探测

# 检查当前版本是否有已知漏洞
openclaw --version
# 对照 GitHub Releases 页面的安全说明
```

---

## 八、中国用户特别提示

> 📌 **本节包含 3 个问题：**
> [Q65: API 访问不了](#q65-api-访问不了怎么办) | [Q66: WhatsApp 能否使用](#q66-whatsapp-在中国能用吗) | [Q67: npm 镜像问题](#q67-npm-镜像配置后还是装不上)

### Q65: API 访问不了怎么办？

**说明：** OpenAI、Anthropic、Google 的 API 在中国大陆无法直接访问。

**解决方案：**

```bash
# 方案一：使用代理
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
openclaw gateway --port 18789

# 方案二：使用 OpenRouter（一个 Key 用所有模型，通过环境变量设置 Key）
export OPENROUTER_API_KEY="sk-or-xxxxx"
openclaw config set agents.defaults.model "openrouter/openai/gpt-5.2"

# 方案三：使用国产模型（通过 OpenAI 兼容接口或 OpenRouter 接入）
# DeepSeek、Moonshot 等可配置为 OpenAI 兼容提供商：
# 在 ~/.openclaw/openclaw.json 中：
# { "models": { "providers": { "deepseek": { "baseUrl": "https://api.deepseek.com/v1" } } } }
# 然后设置环境变量和模型
openclaw config set agents.defaults.model "deepseek/deepseek-chat"

# 方案四：本地模型（完全不需要网络）
ollama pull qwen2.5:7b
openclaw config set agents.defaults.model "ollama/qwen2.5:7b"
```

### Q66: WhatsApp 在中国能用吗？

**说明：** WhatsApp 在中国大陆需要代理才能使用。

**替代方案：**
- Telegram（需要代理，但 Bot API 可以通过代理访问）
- 飞书 / Lark（国内原生支持，OpenClaw 通过扩展支持飞书 Channel）
- 注意：钉钉、微信公众号、个人微信均不受官方支持

```bash
# 配置飞书（推荐中国用户）
openclaw channels add feishu
# 按提示配置飞书开放平台的 App ID 和 App Secret
```

### Q67: npm 镜像配置后还是装不上

**解决方案：**

```bash
# 清除 npm 缓存
npm cache clean --force

# 确认镜像生效
npm config get registry
# 应该显示 https://registry.npmmirror.com

# 如果还是不行，试试直接下载
# 去 GitHub Releases 页面下载预编译包
# https://github.com/openclaw/openclaw/releases

# 或者用 Docker（镜像可以从国内源拉取）
docker pull openclaw/openclaw:latest
```

---

## 九、社区和贡献问题

> 📌 **本节包含 5 个问题：**
> [Q68: 报告 Bug](#q68-怎么报告-bug) | [Q69: 贡献代码](#q69-怎么贡献代码) | [Q70: 分享自定义技能](#q70-怎么创建和分享自定义技能) | [Q71: 中文社区](#q71-有中文社区吗) | [Q72: 文档反馈](#q72-文档有错误怎么反馈)

### Q68: 怎么报告 Bug？

**解决方案：**

1. 去 [GitHub Issues](https://github.com/openclaw/openclaw/issues) 页面
2. 点击 "New Issue"
3. 选择 "Bug Report" 模板
4. 填写以下信息：

```markdown
## 环境信息
- OpenClaw 版本：（openclaw --version）
- Node.js 版本：（node --version）
- 操作系统：
- 安装方式：npm / Docker

## 问题描述
简要描述遇到的问题

## 复现步骤
1. ...
2. ...
3. ...

## 期望行为
你期望发生什么

## 实际行为
实际发生了什么

## 日志
（openclaw logs --limit 50）
```

### Q69: 怎么贡献代码？

**流程：**

```bash
# 1. Fork 仓库
# 在 GitHub 上点击 Fork

# 2. 克隆到本地
git clone https://github.com/your-username/openclaw.git
cd openclaw

# 3. 创建功能分支
git checkout -b feat/my-new-feature

# 4. 安装依赖
npm install

# 5. 开发和测试
npm run dev
npm test

# 6. 提交代码
git add .
git commit -m "feat: add my new feature"

# 7. 推送并创建 PR
git push origin feat/my-new-feature
# 在 GitHub 上创建 Pull Request
```

### Q70: 怎么创建和分享自定义技能？

**解决方案：**

```bash
# 1. 创建技能文件
mkdir -p ~/.openclaw/workspace/skills
nano ~/.openclaw/workspace/skills/my-awesome-skill.md

# 2. 测试技能
openclaw skills list
openclaw skills check my-awesome-skill --input "测试"

# 3. 分享到社区
# 在 GitHub 上创建一个仓库，或者提交到 OpenClaw 的技能市场
# https://github.com/openclaw/openclaw-skills
```

### Q71: 有中文社区吗？

**说明：** 有的。

- GitHub Discussions（中英文都可以）：[github.com/openclaw/openclaw/discussions](https://github.com/openclaw/openclaw/discussions)
- Discord 社区（有中文频道）
- 微信群：关注 OpenClaw 公众号获取入群二维码

### Q72: 文档有错误怎么反馈？

**解决方案：**

- 直接在 GitHub 上提 Issue，标注 `docs` 标签
- 或者直接提 PR 修改文档
- OpenClaw 官方 Markdown 文档位于其 GitHub 仓库的 `docs/` 目录

---

## 十、其他常见问题

> 📌 **本节包含 7 个问题：**
> [Q73: 和 ChatGPT 的区别](#q73-openclaw-和-chatgpt-有什么区别) | [Q74: 支持哪些语言](#q74-openclaw-支持哪些语言) | [Q75: 多实例运行](#q75-一台机器能跑多个-openclaw-实例吗) | [Q76: 是否收费](#q76-openclaw-会收费吗) | [Q77: 查看所有配置](#q77-怎么查看当前的所有配置) | [Q78: Gateway 和 Agent 关系](#q78-gateway-和-agent-是什么关系) | [Q79: 获取帮助](#q79-遇到问题怎么获取帮助)

### Q73: OpenClaw 和 ChatGPT 有什么区别？

**说明：** 它们是完全不同的东西：

| 维度 | ChatGPT | OpenClaw |
|------|---------|----------|
| 本质 | AI 聊天产品 | AI Agent 框架 |
| 模型 | 只能用 OpenAI 的模型 | 支持多个主流提供商 |
| 平台 | 网页/App | WhatsApp/Telegram/Discord 等 |
| 工具 | 有限的插件 | 可扩展的工具和技能系统 |
| 记忆 | 平台管理 | 你自己控制（本地 Markdown） |
| 数据 | 存在 OpenAI 服务器 | 存在你自己的机器上 |
| 价格 | 订阅制 | 开源免费（API 费用另算） |

简单说：ChatGPT 是一个产品，OpenClaw 是一个让你构建自己 AI 助手的工具。

### Q74: OpenClaw 支持哪些语言？

**说明：** OpenClaw 本身是英文项目，但 AI 的回复语言取决于你使用的模型和系统提示词。

```bash
# 在 SOUL.md 中指定语言（编辑 ~/.openclaw/workspace/SOUL.md）
# 添加内容：
# ## 语言
# - 请始终用中文回复
# - 代码注释也使用中文
```

大多数主流模型（GPT-5.2、Claude、Gemini）都支持中文。本地模型推荐用 Qwen（通义千问）系列，中文能力最好。

### Q75: 一台机器能跑多个 OpenClaw 实例吗？

**解决方案：**

```bash
# 可以，但需要用不同的端口和数据目录

# 实例 1
OPENCLAW_HOME=~/.openclaw-1 openclaw config set gateway.port 18789
OPENCLAW_HOME=~/.openclaw-1 openclaw gateway --port 18789

# 实例 2
OPENCLAW_HOME=~/.openclaw-2 openclaw config set gateway.port 18790
OPENCLAW_HOME=~/.openclaw-2 openclaw gateway --port 18790

# Docker 方式更简单：跑多个容器，映射不同端口
```

### Q76: OpenClaw 会收费吗？

**说明：** OpenClaw 是开源项目（MIT 协议），永久免费。你需要付费的只有 AI 模型的 API 调用费用（如果你用云端模型的话）。用本地模型（Ollama）则完全零成本。

### Q77: 怎么查看当前的所有配置？

**解决方案：**

```bash
# 查看所有配置
openclaw config get

# 查看特定配置项
openclaw config get providers
openclaw config get channels
openclaw config get agents.defaults.model

# 导出完整配置（备份用）
# 直接备份配置文件
cp ~/.openclaw/openclaw.json my-config-backup.json

# 从备份恢复
cp my-config-backup.json ~/.openclaw/openclaw.json
```

### Q78: Gateway 和 Agent 是什么关系？

**说明：**

- **Gateway** 是消息网关，负责连接各个消息平台（WhatsApp、Telegram 等），接收和发送消息
- **Agent** 是 AI 智能体，负责理解消息、调用工具、生成回复

消息流程：`用户 → 消息平台 → Gateway → Agent → 模型 API → Agent → Gateway → 消息平台 → 用户`

Gateway 是基础设施层，Agent 是业务逻辑层。一个 Gateway 可以服务多个 Agent。

### Q79: 遇到问题怎么获取帮助？

**获取帮助的渠道（按推荐顺序）：**

1. 查看本 FAQ 文档
2. 查看[官方文档](https://docs.openclaw.ai)
3. 搜索 [GitHub Issues](https://github.com/openclaw/openclaw/issues)（可能别人遇到过同样的问题）
4. 在 [GitHub Discussions](https://github.com/openclaw/openclaw/discussions) 提问
5. 加入 Discord 社区实时交流

提问时请附上：
- OpenClaw 版本（`openclaw --version`）
- Node.js 版本（`node --version`）
- 操作系统信息
- 相关日志（前台运行 `openclaw gateway --port 18789 --verbose` 查看）

---

## 十一、版本升级与迁移（v2026.3.28 → v2026.5.22）

> 📌 **本节包含 4 个问题：**
> [Q80: 升级要点](#q80-从-v202632x-升级到-v202642x-有哪些注意事项) | [Q81: 反向代理配置变更](#q81-升级后反向代理配置需要改吗) | [Q82: 插件白名单变更](#q82-升级后-allowlist-相关操作报权限错误) | [Q83: 性能提升](#q83-升级后启动变快了是正常的吗)

### Q80: 从 v2026.3.2x 升级到 v2026.5.22 有哪些注意事项？

> **v2026.5.22 新增关注点**：除了 v2026.4.24 的 Google Meet、DeepSeek V4、浏览器坐标点击和模型目录 manifest 化之外，v2026.5.22 还重点改进 Gateway 启动性能、插件 metadata 缓存、Meeting Notes 外部插件、package shrinkwrap / runtime deps、`protobufjs` 8.4.0 安全更新，以及默认子 Agent bootstrap context 收窄。升级后如果发现模型、通道或插件行为变化，先运行 `openclaw doctor`，再对照当前 release notes。

**说明：** v2026.4.x 系列包含多项安全加固和功能改进。大部分配置向后兼容，但以下几点需要注意：

1. **Owner-Enforced Commands（v2026.4.5+）**：`/allowlist add` 和 `/allowlist remove` 现在需要 Owner 身份验证。如果你之前在自动化脚本中使用了这些命令，需要确保调用者具有 Owner 权限
2. **转发头安全检查（v2026.4.x+）**：如果你使用反向代理，Gateway 现在会检查转发头的一致性（详见 Q81）
3. **环境变量过滤（v2026.4.7+）**：Gateway 会自动拦截危险的环境变量覆盖，如果你的部署脚本依赖特定的环境变量传递，建议测试确认
4. **Hook 失败模式变更（v2026.4.5+）**：Hook 崩溃时从 fail-open 改为 fail-closed，如果你有自定义 Hook，升级后请确认它们运行正常
5. **Cron 状态拆分（v2026.4.20+）**：定时任务运行时状态拆分到独立的 `jobs-state.json` 文件，升级后首次启动会自动迁移

**升级步骤：**

```bash
# 1. 备份
cp -r ~/.openclaw ~/.openclaw.backup-$(date +%Y%m%d)

# 2. 升级
npm update -g openclaw

# 3. 验证
openclaw --version
openclaw doctor
openclaw security audit

# 4. 如果使用反向代理，检查转发头配置（见 Q81）
```

### Q81: 升级后反向代理配置需要改吗？

**说明：** 如果你通过 Nginx 等反向代理暴露 Gateway，v2026.4.x 的转发头安全检查可能影响你的配置。

**需要确认的事项：**

1. 反向代理的 `X-Forwarded-For` 头必须**覆盖**客户端值，不能**追加**

```nginx
# 正确：覆盖客户端的转发头
proxy_set_header X-Forwarded-For $remote_addr;

# 错误（旧写法）：追加模式，可能被客户端伪造
# proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

2. 如果使用 trusted-proxy 认证模式，`trustedProxies` 中不能填 loopback 地址（`127.0.0.1`、`::1`）
3. 如果 Gateway 和代理在同一台机器上通过 loopback 通信，改用 token/password 认证模式

### Q82: 升级后 /allowlist 相关操作报权限错误

**现象：** 升级到 v2026.4.5+ 后，执行 `/allowlist add` 或 `/allowlist remove` 时提示权限不足。

**原因：** 这是 v2026.4.5 引入的 Owner-Enforced Commands 特性。白名单修改现在需要 Gateway 所有者的实际身份验证，不再接受宽松的回退。

**解决方案：**

```bash
# 确保你通过已认证的 Owner 身份操作
# 1. 如果使用 Token 认证，确保连接时提供了正确的 Token
# 2. 如果使用配对系统，确保你是已配对的 Owner 用户
# 3. 通过 CLI 直接管理白名单
openclaw approvals get
openclaw approvals set <tool-name> --allow
```

### Q83: 升级后启动变快了，是正常的吗？

**说明：** 是的，这是正常现象。v2026.4.20+ 包含了显著的启动性能优化：

- **插件启动**：通过延迟加载和 manifest-backed 模型行，bundled 依赖加载时间降低 82-90%
- **Doctor 诊断**：插件延迟加载使冷启动时间降低约 74%
- **模型目录**：静态模型目录替代运行时加载，减少启动时的网络请求

这些优化在 v2026.4.24 中进一步改善（通过 provider 依赖的延迟加载和 manifest-backed model rows）。

---

> 教程到这里就结束了！如果这份教程帮到了你，给个 Star 支持一下！
