# 更新日志（Changelog）

本项目所有重要变更均记录在此文件中。

---

## [v5.5] - 2026-10-03

- 纠正 v5.4 将 Mods 简介视为完整覆盖的记录；Claude Code 08 增加可照做的 Mods 工坊，05/11/导航同步概念与托管边界。修正 Ctrl+L 回滚、alwaysLoad 工具级例外、代码审查路由、后台停止、auto 分类器计费和云任务恢复；收尾同步托管读取/沙箱、IDE 上下文、自动记忆开关、插件依赖/评测与云任务错峰。
- Codex 补 ChatGPT 共享插件界面、MCP Events、Security Cloud 的入口与适用范围，以及 provider 凭据、模型目录、Guardian、输入审批和 Remote 排障。收尾补 MCP OAuth / OIDC、Touch ID、摘要兼容、网络撤权、任务管理、工作树占用与附图入口。
- OpenClaw 补 TOOLS.md 迁移、数据库升级/回滚、CLI 与服务运行时修复、ToolSearch/CodeMode、Room Teams、Swarms、Incognito、named roles 和停止/送达边界；收尾补统一技能搜索、自学习模式、只读配置与 include 备份、Ready workers 费用，以及 Sora / video-frames 退休路线。
- WorkBuddy 补原生移动 App、文件浏览器、专家创建/管理、语音输入、消息引用、连接器和定时任务步骤；保留正确的资料库主线，历史版本注明日期。
- 官方 Claude Code 2.1.288 隔离客户端的 Mods validate 与离线测试通过；未调用模型。核查清单区分逐章核查、功能简介、可操作练习和真实执行，不再由精选功能数量推断完整覆盖。真实账户、手机授权、付费服务和生产迁移仍未执行。

---

## [v5.4] - 2026-10-03

### 正文、功能与练习的第二轮复核

- 重新核对全部 50 篇教程和速查卡的当前入口、功能变化、重复 FAQ 与练习衔接，在既有核查清单加入四工具的功能覆盖矩阵；正确原文和注明日期的历史说明保留。
- Claude Code 修正不存在的 CLI 参数、日常 bypass 建议、MCP 本地配置及归档服务入口；补 AGENTS.md、mcp_tool、omitClaudeMd、Mods、账号资源同步、插件配置和企业供应商/遥测说明。语音步骤按当前录音、转写、提交和按键配置重写。
- Claude Code Notification 保留可选 title，无标题时使用默认值；格式化器采用参数列表，Git 检查使用 NUL 分隔文件名、拒绝把检查失败当通过，并返回合法的 PreToolUse ask 结构。SDK 区分可用工具池与免审批工具，删除无依据的固定并发上限。
- Codex Rules 改用内置 prefix_rule 注册并说明前缀和严格决策优先级；CLI 区分事件流与最终回答，补完整 JSON Schema。补当前模型与登录方式迁移、Worktree 创建/回流、手机接续、Browser/Computer Use、录制技能、Memories、Computer History、事件任务、Team Tasks、PR 插件及 Security Review；新 Cloud 补 Personal vault、共享、Tailscale 和申请式 OIDC。
- OpenClaw 修正初始化后重复启动 Gateway、通道命令和配对、旧 BlueBubbles 路径、技能元数据/加载作用域、记忆与路由残留；补当前技能库、Workshop、Active Memory、Standing Intent 和导入说明。9.4 部署示例继续锁定版本，9.8 的 Windows 迁移和会话返回机制单列；Docker 更新先选目标版本并备份，托管平台不再照抄缺少状态和认证的部署。
- WorkBuddy 按这轮取得的官方正文补技能三种添加方式、管理与开关、套餐与积分、网页注销及后果、定时通知和项目配置。连接器读写与 AI 用量分开说明；新定时摘要明确最近记录日、实际文件与可选通知的检查，Python 练习先进入目录再建立虚拟环境。

- Claude Code 逐段复核各章重复旁支：订阅/Console/API 认证、用量与快捷键、Skills 的完整文件头与刷新、合法 Hook 拒绝字段和日志输出、SDK 内容块与权限返回、App/Action 的安装关系、托管宿主策略和稀疏目录；没有把缺失成本数据、部署占位或合规草图写成已完成结果。

### 验证与未执行范围

- 对实际修改后的源文件执行本地链接、锚点、围栏、编码与公开合成练习检查；权限规则、结构化输出和通知/文件名/Git 失败路径使用离线解析器或 mock 验证。
- Skills 跨平台合成夹具 24/24、成本缺数据/有效数据检查 8/8；独立虚拟环境中的 pandas/openpyxl 参考 CSV→Excel 校验通过（420、3 行），不是 WorkBuddy App 实测。
- 官方功能核查与真实客户端执行分开记录。没有调用收费模型、使用真实账号授权、发布 Cloud 环境或启动生产容器；WorkBuddy 仍无法取得的价格、积分和部分页面保留具体原因。

---

## [v5.3] - 2026-10-03

### 安装、认证与命令

- Codex Windows 安装改走当前 ChatGPT 桌面入口与准确的 Store ID，补 Linux 预览版入口；区分配置 profile、权限 profile 与只读沙箱，修正 `exec` 参数及网络域名规则的生效条件。
- Claude Code 修正最低系统要求、自动更新变量、交互与打印模式、文件访问边界；Remote Control 补单会话模式和转录存储说明，Channels 与本地定时任务修正认证及恢复条件。
- OpenClaw Docker 安装补匹配版本的官方初始化步骤，手动 Compose 补监听、认证和 origin 配置；修正配置查询与消息平台命令示例，说明沙箱默认关闭及数据库迁移对回滚的限制。
- WorkBuddy 修正官网下载识别、网页登录、菜单与应用撤权入口；企业旧促销改为已结束的历史快照。

### 工作流与可运行示例

- Codex 云任务按当前 Work in / Cloud 的环境发布流程重写，区分新环境与 legacy 的代码审查集成；同步 Secrets 代理、Scheduled、MCP transport、导入及当前 CLI 参数。
- Claude Code 修正 Skills 预批准权限、插件管理和 Hooks 通知转义；SDK 按 Python 实际类型处理消息，计算器改为有限 AST 运算，GitHub Action 修正输入、OIDC 权限与报告缺失时的失败行为。
- OpenClaw 按 v2026.9.4 修正路由、模型、技能、记忆与定时命令；Agent 名单迁到 entries，共享工具策略放回顶层，压缩与媒体配置按现行 schema 修正。同步旧 QMD、SQLite 状态、认证目录与权限边界，Docker 示例保持明确参考版本；首次启动先生成缺失的 token 和进阶数据库密码，保留已有环境文件，再用 Compose 静默检查缺失或空值。
- WorkBuddy 区分定时任务、远程助理与连接器授权，补 CSV 练习和设计创意入口，删除未经证实的固定耗时、收费倍率、同步及企业权限保证。价格未重新核实的段落保留日期快照。

### 首页与迁移入口

- 首页靠前介绍 Meta_Kim 的可复用工作流，链接该项目现有中、英、日、韩说明；本教程仓库仍只有中文根 README。
- 修正 VoltAgent 子代理分类和角色名称、GitButler Agent 文档及 OpenClaw 支持入口；清理首页重复的旧轮次状态，区分参考版本、官方发布记录与本机核查。
- 新增逐章核查清单：50 篇教程及速查卡全部覆盖，47 篇教程和 1 张速查卡有必要修改；Codex 插件、Codex Review/PR、WorkBuddy 资料库核心主线核对后保留，未能核实的价格、页面及真实服务流程列明原因。

### 检查

- 新增离线教程检查与 Linux / Windows CI：核对公开 Markdown 的本地链接和章节锚点、围栏、编码，以及进度计算和订单练习。
- 进度练习源文件继续保留刻意的 `NaN` Bug；检查先确认预期失败，再在临时参考副本中验证四个原检查和 `3/8 = 38`，不把参考修复称为 AI 客户端实测。

---

## [v5.2] - 2026-09-14

### 学习体验

- README 改为先选任务、完成成果，再查完整目录；新增 12 类常见工作场景入口。Claude Code 入门路线调整为安装 → 小 Bug → 项目规则；Codex 保持 App 主线，WorkBuddy 调整为安装 → 周报 → 表格或资料问答。
- 新增 `examples/` 配套练习：两文件代码修错、虚构工作记录、7 行订单 CSV、三份不同状态的产品说明。对应章节补齐操作、结果对照、具体纠错和换条件练习，材料按仓库 MIT 许可提供。
- Claude Code 02 与 Codex CX-02 使用同一份进度计算练习，演示先复现错误、再修复和检查；公开样例刻意保留初始 Bug，便于读者观察前后变化。
- WorkBuddy WB-01 补周报的事实核对与 Word 草稿；WB-03 补去重、空值、真实零元和退款的计算口径；OpenClaw OC-03 补无需接消息平台的待办简报练习。相关导航同步，已有行业 Buddy、Worktree 和 Codex 功能修订继续沿用。

### 事实修正

- WorkBuddy WB-06 按官方资料库流程重写：区分“我的文档 / 团队空间”与外部知识库，讲清添加到任务、核对出处、新旧资料冲突和原文档修订。更正索引、检索收费、云端存储与“有引用就不会编造”等口径。
- OpenClaw v2026.9.4 的 Node.js 要求更正为 `>=24.16.0 <25 || >=26.1.0`，新装推荐 26.x；同步安装命令、环境表和 FAQ，拆开 Windows / WSL 命令，移除已失效的 `npm bin -g` 排障命令。
- 参考官方工作流、公开课程介绍与社区实战的方法，采用本课程原创材料讲解；没有复制第三方教程正文。读者试学与四产品真实客户端流程仍需分别验证，不以本地样例检查替代。

---

## [v5.1] - 2026-09-14

### 新增

- README 新增「配套开源项目（老金出品）」段，推荐 [Meta_Kim](https://github.com/KimYx0207/Meta_Kim)（给 Claude Code / Codex / OpenClaw / Cursor 加治理执行层，Apache-2.0）与 [Kim_Service](https://github.com/KimYx0207/Kim_Service)（Hook 与 Agent Skill 合集，MIT），并标注学到哪些章节之后装最合适。
- README 项目简介、「为什么放在一起」、核心特色、致谢改为四条线口径（v5.0 加入 WorkBuddy 后这几处仍写着「三类工具 / 三者 / 三线」）。

### 修改

- 四条主线完成本地版本修订（核查日：2026-09-14）：Claude Code v2.1.222 → **v2.1.270**、OpenClaw v2026.7.1-2 → **v2026.9.4**、Codex App 26.727 → **26.908**、Codex CLI 0.146.1 → **0.154.0**、WorkBuddy → **客户端 5.5.6**。同步 README 徽章、统计、版本说明和差异速览，保留旧版本时间线。
- Claude Code 补齐 2.1.223–2.1.250 区间中官方已发布的条目，更新默认模型变量、`/review` 别名、fork、`--restricted`、插件 archive / GitLab / validate / eval 入口和云供应商 `/loop` 支持。保留模型切换 hooks、MCP 托管策略、后台任务修复等主体更新；纠正 `keybindingFlavor` 的含义、`/diff` 已有命令与新侧栏的区别、`/advisor` 文本形式的引入版本、`/effort` 选择器按键。v2.1.270 修复只读 Git 命令意外请求权限。
- OpenClaw 课程按 v2026.9.4 补关键变化：升级链路重做（Doctor 失败回滚、隔离 candidate 预演、内置 triage agent）、**两条升级硬约束**（从 2026.8.2 升上来且无 service manager 须先跑一次 `openclaw update --no-restart`；失败回滚不覆盖数据库迁移，仍要求已验证的升级前备份）、全新安装快速通道、`openai/gpt-6-astra` 与 GPT Image 2.5、个人技能库与 Skill Workshop、统一 Plugins 工作区、掩码凭据请求与一次性自动化批准、公开只读会话分享（企业需默认关闭）、`OPENCLAW_CONFIG_READONLY=1`、Linux 桌面端（.deb / AppImage）。Docker 章节的版本锁定示例从 v2026.6.8 改到 v2026.9.4；FAQ 与安全章里旧的 `npm update -g openclaw` 统一改为 `openclaw update` 优先、npm 作退路，Q11 改为对升级前已验证的版本先做降级 dry-run，不再把 extended-stable 当通用回滚目标；换端口示例从 18889（落在教程自己标注的 CDP 端口池里）改为 19789；07 章「多语言记忆」按官方记录收窄为西班牙语、葡萄牙语两种；05 章把 v5.0 记在 v2026.7.x 名下的会议插件与 Wear OS companion 更正为 v2026.8.1。
- Codex 课程按 App 26.908 + CLI 0.154.0 补关键变化：App 侧 Pets 悬浮控件快速对话（`@` 带上下文、`$` 选 skill）、Windows 同时按下两个 Alt 键截 Appshot、Sources 面板直接打开文件、Codex Micro 插入文本；CLI 侧 **`codex mcp-server` 子命令与独立二进制已移除**（2026-09-05 移除，升级后老脚本会直接失败）、Full Access 下 Guardian 跳过纯确认类操作、Guardian 记录跨压缩/重启/fork 保留、MCP 审批按 app 账号隔离、实验性 worktrees（`--worktree` / `/worktree`）。
- WorkBuddy 课程按客户端 5.5.6 复核，三处直接影响照做的改动写进正文：**5.5.4 起「自动化」改名为「定时任务」**（WB-07 加前置提醒并改写入口措辞）、5.4.7 新增「订阅和用量」设置页（WB-01 / WB-02 / WB-10 的积分查询入口同步）、定价体系改版为体验/标准/高级/旗舰四档。另在版本提示中说明 5.5.5 创意设计与资料库引用、5.5.0 行业 Buddy 应用与腾讯文档编辑增强、5.4.0 Worktree 任务与 Git 分支切换、5.5.3 本地 Office 预览上限、5.5.4「允许锁屏运行」三档。
- 清理多章正文里的角色化自称（「老金我」→「我」）和「沉淀」等用词；OC-00 修正一处嵌套代码块围栏；OC-01 按官方 changelog 改写 v2026.4.22 / v2026.4.27 捆绑插件加载说明（原文「懒加载和 manifest 驱动」不准确，实际是原生 Jiti 加载已构建的 dist 模块，以及 `activation.onStartup` 显式声明）。

### 修复

- WorkBuddy 补齐行业 Buddy 的应用选择、授权范围、场景任务、输出核对及跨应用接续；WB-09 改按真实的 Agent / Plan / 仅问答入口教学，补 Worktree 从基础提交创建、并行分工、逐项审阅、本地提交合并与结束任务的完整练习。保留创意设计的既定范围说明；移除剩余的固定省积分比例和无依据退款断言。
- Codex CX-03 / CX-14 按 2026-09-14 官方资料逐项复核：命令表覆盖当前 24 个 App 入口，修正 `/status`、Goal 进度栏控制、Skills 与 slash 列表关系；补 Settings → Import、导入资产与后续设置、CLI `/import` 限制。对比章明确 Claude Desktop 同样提供可视化审查、worktree 与云端能力，区分 Local / Worktree 接续和云端环境。
- Claude Code：补全复制后会失效的 Markdown 示例围栏；修复 Hooks 配置嵌套、WorktreeCreate/Remove 契约和并行执行说明，统一静默输出与事件决策边界。实战日志改为从 stdin JSON 读取事件，先建目录，再安全编码写入 JSONL；修正企业章重复句和 print 模式成本上限说明。MCP 章节区分 2026-07-28 的按请求协商与旧版初始化握手，避免只更新协议日期。
- Codex：补中间版本的 Hooks / MCP 操作差量；修正插件安装子命令、旧线程刷新建议、连接应用账号的审批作用域，以及子代理控制权、文件权限与工作树隔离的区别。
- OpenClaw：修正不存在的 Docker 镜像标签和裸卷名备份；从容器挂载读取实际卷名，停写后归档，恢复时检查匹配镜像并拒绝已有容器或非空卷。区分 Gateway 双卷脚本与包含可选 PostgreSQL/Redis 的多服务脚本，恢复演练使用独立项目名；定时备份通过 `crontab -e` 追加，避免覆盖已有任务。生产示例固定镜像版本，并区分宿主机端口映射与容器监听地址。将“失败就自动回滚”收窄为通过兼容检查才恢复，主动降级先 dry-run。
- WorkBuddy：把未经证实的 QQ 邮箱事件触发界面改为定时邮件巡检；补锁屏运行的设置与在线前提；注明老会员过渡价资格，以及企业 9 月 30 日活动订单窗口与积分有效期的区别。移除 WB-01 / WB-02 / WB-03 / WB-10 中未经证实的专家团固定 3–5 倍消耗及费用排序，改为按实际任务与用量评估。
- **修正 WorkBuddy 价格数据错误**（本轮最值得修的一处）。原文写"专业版约 99 元/月、年度版约 119 元/年起"，与官方定价页实际不符：个人版是四档，标准版年付 840 元（不是 119 元），高级版 1,680 元/年，旗舰版 8,400 元/年。WB-10 按官方定价页整段重写为月付/连续包月/年付/连续包年/实得积分五列表，并补企业版两档、个人与企业加量包、老用户过渡价；WB-01 的同源简表一并更正。同时补两条原文缺失的采购硬约束：**专有云 100 席起购**、**企业限时双倍积分活动的下单窗口至 2026-09-30**（活动期后的新购、续费和扩容须重新核对赠送规则）。
- 修正 WorkBuddy 下载口径：官方文档的「历史版本下载」页只归档到 v5.1.2（2026-06-17），不是最新版下载口，WB-02 与 README 环境要求都改为从官网首页下载。
- 修正 README 中"WorkBuddy App 无 semver"的错误表述——该产品线有完整语义化版本与公开更新日志，来源改为 workbuddy.cn 官方更新日志。

### 说明

- 更正 v5.0 条目与 README 差异速览里 OpenClaw v2026.6.8 → v2026.7.1-2 的变化清单：原先列出的 State safety & recovery、durable channel delivery、session rewind、interactive MCP Apps、meeting plugins、Wear OS 等条目不属于该区间（按官方 release notes，会议插件、Wear OS companion、MCP Apps、会话回退分支均为 v2026.8.1），已按 v2026.7.1 官方 highlights 重写。
- 原先未完整取得的发布记录已补齐：Claude Code 2.1.223–2.1.250 区间内的 24 个已发布条目，及 Codex CLI 0.147.0–0.152.1 的 9 个正式版本。Codex 0.147.0 在聚合 changelog 中缺项，但 GitHub Release 与 npm 均确认已发布；0.142.0–0.146.1 继续沿用上一轮合并摘要。
- 各章原有的历史版本标注（例如"v2.1.133+ 起可以…"）是刻意保留的时间线记录，不属于漏改。

---

## [v5.0] - 2026-08-06

### 新增

- 项目升级为 Claude Code、OpenClaw、Codex、WorkBuddy 四教程结构，新增 `docs/workbuddy/` 系列共 11 篇（WB-00 阅读指南 + WB-01~WB-10 正文），把腾讯 WorkBuddy 作为第四条主线，面向办公人和国内团队，与另外三条开发者主线互补不冲突。
- WorkBuddy 系列围绕官方真实功能骨架组织：专家（人设+方法论+工具链）、专家团（团长自动拆解并行）、技能（技能市场一键装）、自动化（按时间规则执行）与远程指令、连接器（QQ 邮箱/腾讯文档/腾讯会议/企业微信等腾讯生态）五大核心概念，每篇带可跑通的工坊和卡住怎么办，专业术语第一次出现都解释。
- WorkBuddy 系列采用纯老金教学视角编写，零外部参考痕迹（无 URL、无"官方文档说"），价格、积分、菜单名一律标注"以本机 App 关于页和官网为准"。WB-10 含四工具横向对比（Claude Code/Codex/OpenClaw/WorkBuddy），强调共存不二选一。
- README 升格第四主线：标题、徽章、项目简介四工具对比表、新增 Part 4 目录、WorkBuddy 路线、Week 13-14 学习计划、统计 39→50 篇、版本表加 WorkBuddy 行、环境要求加 WorkBuddy 节、适用人群加办公人、免责声明加 WorkBuddy。

### 修复

- 修复上一次"AI 腔清洗"过度编辑造成的 172 处病句：清洗把"X 不是 Y，而是 Z"句式中的"不是 Y"机械删除，留下缺谓语残句。本轮逐处精准补回对比连词，分布在 docs/claude-code/（7 篇 12 处）、docs/codex/（14 篇 113 处）、docs/openclaw/（10 篇 47 处）。不改动其他字，不恢复作者人设词，经 rg 反向扫描 + 抽样人审复核零残留。

### 修改

- 课程稳定基线刷新到 Claude Code v2.1.222（从 v2.1.181）、Codex App 26.727 + CLI 0.146.1（从 26.609 + 0.141.0）、OpenClaw v2026.7.1-2（从 v2026.6.8，预发布线推进到 v2026.7.2-beta.7）。README 徽章、版本表、差异速览、免责声明同步更新。
- Claude Code 课程按 v2.1.222 补关键变化：Sonnet 5 成默认（1M 上下文）、Opus 5 成默认、"Default" 权限模式改名 "Manual"（v2.1.200）、ultraplan 移除（v2.1.222）、subagent 默认后台 + 嵌套深度 3、新 `/doctor` / `/commit-push-pr` / `/fork` / `/code-review` 命令、性能 79× transcript 缩小 / 7× 工具回合提速（v2.1.208）、Remote Control 不再允许仓库级开启、新 hooks（DirectoryAdded / EndConversation / Notification）、OTel `OTEL_LOG_USER_PROMPTS=1` 行为变化。
- Codex 课程按 App 26.727 + CLI 0.146.1 补关键变化：Codex 并入 ChatGPT 桌面 App（26.707）、GPT-5.6 Sol/Terra/Luna 全系（272K 上下文）、PR Chat、多仓库 diff 审查、本地项目多文件夹、Activity view、Chrome 扩展、多 Agent V2 稳定、`/import` 从 Claude Code + Cursor 迁移、远程插件默认开、MCP 交互式认证默认、新 `writes` 审批模式、Agent Plugins manifest + 新市场（Amazon Bedrock + Claude Code）、系统代理 PAC/WPAD、企业 in-app 更新管控。
- OpenClaw 课程按 v2026.7.1-2 补关键变化：新模型与提供商（Claude Sonnet 5 / Mythos 5、Featherless、ClawRouter，GPT-5.6 成为新装默认）、Control UI 与原生 macOS 聊天重做、对话式 onboarding（Crestodian 真跑 agent loop）、移动端离线缓存与语音（Apple Watch 完整语音、iOS 朗读回复）、会话分组与自动标题、启动与升级恢复（容器迁移先于 Gateway readiness、control-plane-safe 模式）；v2026.7.1-1 修复 Memory Core 启动冲突导致的 fatal restart loop、Codex progress replies 中途停、WSL state permissions，v2026.7.1-2 修复 npm 插件更新 singleton-array metadata。

---

## [v4.4] - 2026-06-18

### 修改

- 本轮把课程稳定基线更新到 Claude Code v2.1.181、OpenClaw v2026.6.8、Codex App 26.609 与 Codex CLI 0.141.0，并在 README 统一维护版本表和差异速览，避免每章重复堆同一批 release notes。
- Claude Code 课程补充 v2.1.169 -> v2.1.181 关键变化：`/config key=value`、`Tool(param:value)` 权限语法、嵌套 `.claude/skills` / agents / workflows 就近优先、subagent 多层委派、`enforceAvailableModels`、Remote Control presence file、Bun 1.4 与云盘写入修复。
- Codex 课程继续保持 App-first：按 App 26.609 补充 Developer mode / CDP 浏览器调试、composer `/init`、Migrate to Codex、Windows Computer Use per-app controls、Automations 审批模式继承，并把 CLI 0.139 -> 0.141 的 `/usage`、`/import`、`/delete`、远程执行与 PostToolUse blocking 收进 CX-12。
- OpenClaw 课程按 v2026.6.8 更新安装升级、模型/provider、搜索 opt-in、ClawHub pinned commit / policy checks、消息平台富文本、fail-closed 权限边界、SecretRef、agent run recovery、`/usage` 和 FAQ 排障口径。
- 内容组织原则：README 放总览，CHANGELOG 放完整变更，产品章节只放“会改变实操判断”的短更新卡；不复制整段发布记录到多个章节。

---

## [v4.3] - 2026-06-10

### 修改

- 完成一次面向读者的课程复核，继续以 Claude Code CLI、Codex App、OpenClaw 助手框架三条主线组织内容。
- OpenClaw 文档统一收敛模型、上下文窗口、价格和隐私表述：不再把具体模型名、固定窗口、固定价格或“全部本地”等说法写成默认结论，改为引导读者按当前模型目录、onboarding、provider 输出和部署方式确认。
- Codex 课程保持 App-first：项目指令、权限、Rules、Hooks、Review、Subagents、Automations 和 CLI 辅助章节按 App 工作流重新区分职责，减少与 Claude Code CLI 课程的语义重复。
- Claude Code 课程保持 CLI 主线，同时修正本地执行、模型上下文、企业受控 provider 和安全边界的表达。
- 清理多处重复命令块、示例配置和旧版说明，把完整命令留在主章节，辅助章节改为指向主章节，减少阅读负担。
- README 的公开表达改为更稳的课程说明：保留作者定位、学习路线和版本基线，弱化夸张营销词，让读者更容易判断自己该从哪里开始。
- 更新许可和来源说明，保留 MIT 协议下的版权、署名和原始仓库提示，方便引用、转载和二次分发时正确保留来源。

---

## [v4.2] - 2026-05-31

### 修改

- 全库稳定基线同步至 Claude Code v2.1.158、OpenClaw 稳定版 v2026.5.27、Codex App 26.527（Windows 包 26.527.3686.0）；OpenClaw v2026.5.28 beta / v2026.5.29-alpha.1 与 Codex CLI v0.136.0-alpha.1 仍按预发布处理，不作为教程默认基线
- README 重写项目定位、适用人群、学习路线和统计口径，统一表达为 39 篇完整教程 + 1 张速查卡、80 万+ Markdown 内容量、1500+ 实操示例和 250+ 问答条目；Codex 徽章、版本表和免责声明统一改为 App 主线
- Codex App 主线强化：CX-02 扩展为 App 桌面工作流主轴，补充 App 主控台认知、三条安全线、Local / Worktree / Cloud 选择表、任务模板、Review 逐项检查法、从零到 PR 实战和课程交叉验证口径
- Codex 专题继续补强：CX-03 增加 App 命令工作流配方与 `/review` 维度表；CX-09 增加 Automation 合格输出和失败收敛策略；CX-10 增加 Review 严重程度分级和提交前反向解释；CX-11 增加 App -> Cloud 交接包和 Cloud 回流风险表；CX-12 补充 CLI v0.134.0 -> v0.135.0 差量
- Codex 官方链接修正：将失效的 `/codex/review`、`/codex/automations`、`/codex/config` 口径改为当前可访问的 `/codex/app/review`、`/codex/app/automations`、`/codex/app/settings`、`/codex/cli/reference`
- Claude Code 教程补充 v2.1.134 -> v2.1.158 差量，覆盖 Opus 4.8、`/effort xhigh`、`/goal`、`/workflows`、Agent View、后台 shell 会话、`/reload-skills`、`disallowed-tools`、`MessageDisplay` hook、插件 marketplace、MCP 审批、auto mode、遥测和企业治理等内容
- OpenClaw 教程补充 v2026.4.24 -> v2026.5.27 差量，覆盖 Node.js 24 / 22.19+ 基线、Gateway ready 性能、Transcript 核心化、Control UI Activity、Talk / Discord voice、Meeting Notes、消息平台 durable delivery、模型目录、媒体处理、Docker runtime workspace templates 和安全边界
- 固化后续更新规则：版本迭代必须同时检查正文教程差量、README 版本表、文档头尾更新时间、官方链接和可复制命令，避免只改徽章或统计口径

---

## [v2.1.135] - 2026-05-10

### 修改

- 集中更新说明：README 和各教程不再维护独立更新日志、差量更新或版本基线块，统一以 `CHANGELOG.md` 作为唯一更新记录
- 清理 Claude Code、Codex、OpenClaw 教程中分散的版本更新附录、页脚版本历史和文首版本提示，减少多处说明漂移
- README 的更新日志区块改为“更新说明”入口，只保留当前项目介绍、目录和使用入口
- 合并 README 原有历史更新摘要：v4.1 全库审计与 v2.1.93→v2.1.133 内容增强、v4.0 Codex 系列新增、v3.x OpenClaw / Claude Code 同步修订、v2.0 Claude Code 2.1.52 适配、v1.0 初始发布记录

### 从 README 合并的历史摘要

- v4.1（2026-05-08）：完成全库审计与内容增强，修正 Codex 系列结构、Claude Code 权限配置路径、README 版本说明和第三方模型配置入口，并补充 Claude Code v2.1.93→v2.1.133 的 Monitor、Session Recap、Skills、Plugins、Hooks、MCP、Subagent、SDK、企业实战等变更
- v4.0（2026-05-07）：项目升级为 Claude Code、OpenClaw、Codex 三教程结构，新增 `docs/codex/` 系列，覆盖 Codex App 安装认证、桌面工作流、Commands、项目配置、MCP、Skills、Plugins、Subagents、Automations、Review / GitHub / PR、Web / Cloud / CLI 辅助、安全企业和 Claude Code 对比
- v3.3（2026-04-05）：OpenClaw README 徽章与统计表改为稳定版 v2026.3.28 口径，说明预发布与稳定版并存，并统一目录、贡献路线和版本基线表述
- v3.2（2026-04-05）：同步 Claude Code 安装、基础使用、MCP、Commands、Hooks、Subagents、Plugins、企业实战等章节，新增 Remote Control 与 Channels / 计划任务教程，修正 Hooks、Subagents、Plugins 和 OpenClaw 安装、模型、技能、FAQ 等章节口径
- v3.0（2026-02-25）：项目从 Claude Code 单教程扩展为 Claude Code 与 OpenClaw 双教程，新增 OpenClaw 阅读指南和 11 篇教程，重组 `docs/claude-code/` 与 `docs/openclaw/` 目录，并补充 Claude Code 权限、MCP、Agent SDK 等内容
- v2.0（2026-02-25）：适配 Claude Code 2.1.52，更新教程版本号、README 徽章、Hooks 工作树管理、`--worktree`、`/fast`、API 中转站配置，并修复旧版本标记和快速导航描述
- v1.0（2026-02-11）：发布 10 篇 Claude Code 初始教程，包含约 104,000 字内容、70+ 代码示例和 120 个 FAQ

---

## [v2.1.134] - 2026-05-10

### 修改

- Claude Code 02 基础使用：新增 `CLAUDE.md` 实操入口，并将模板调整为可验证、少改动、简单优先的项目协作规则
- Claude Code 03 Commands：将内置命令速查调整为练习后的参考内容，降低“命令解读表”阅读压力
- Codex CX-04：新增 `AGENTS.md` 实操入口，并补充参考来源与项目级协作规则模板
- OpenClaw 03 快速开始：强化“先跑通第一个对话”的实操目标，并将 Control UI 介绍后置
- OpenClaw 06 技能系统：新增低风险技能练习，帮助读者先看到技能对助手行为的影响
- 将多篇教程前置的差量更新 / 版本基线说明移动到文末附录，避免打断正文学习路径

---

## [v2.1.133] - 2026-05-08

### 变更

- **仓库更名为 `AI-Coding-Guide-Zh`**（原 `Claude-Code-x-OpenClaw-Guide-Zh`），更简洁、更包容
- 更新 README.md 所有仓库链接和徽章引用

### 新增

- **全库教程版本升级至 Claude Code v2.1.133**（从 v2.1.92/v2.1.119）
- **11 篇教程新增 v2.1.93→v2.1.133 功能内容**，覆盖以下重要变更：
  - effort 五级推理控制（新增 `xhigh`/`max`，Opus 4.7 推荐默认 `xhigh`）
  - MCP `alwaysLoad` 跳过 ToolSearch 懒加载
  - Hooks 接收 `effort.level` + `$CLAUDE_EFFORT` 环境变量
  - `PostToolUse` 可通过 `hookSpecificOutput.updatedToolOutput` 替换所有工具输出
  - `worktree.baseRef` 控制 worktree 分叉来源（`fresh`/`head`）
  - Monitor 后台监控工具
  - Session Recap（终端失焦后自动回顾）
  - 自定义主题（Plugin 声明 color palette）
  - `skillOverrides` 设置控制 Skill 可见性
  - `/skills` 搜索过滤、`/proactive` 命令（`/loop` 别名）
  - `parentSettingsBehavior` 企业托管设置合并策略
  - `claude project purge` 清理项目状态
  - `CLAUDE_CODE_SESSION_ID` / `CLAUDE_CODE_FORK_SUBAGENT` 环境变量
  - `--channels` 支持 Console auth 登录
  - Native binaries（CLI 迁移到原生二进制文件）
  - Opus 4.7 成为 Max/Team Premium 默认模型
- **新增 Codex 教程目录** `docs/codex/`，含 CX-11 对比指南

### 修改

- 01-安装指南：effort 说明更新为五级，模型名更新为 Opus 4.7
- 02-基础使用：新增 Monitor/Session Recap/自定义主题/Native binaries 章节
- 03-Commands：新增 v2.1.93→v2.1.133 命令增强，effort 五级对比
- 04-MCP：新增 `alwaysLoad` 配置说明，更新变更摘录至 v2.1.133
- 05-Hooks：更新变更摘录至 v2.1.133，修正 PostToolUse 输出机制说明
- 06-Subagent：新增 `worktree.baseRef`、`CLAUDE_CODE_FORK_SUBAGENT` 说明
- 07-Skills：新增 `skillOverrides` 和 `/skills` 搜索过滤
- 08-Plugins：新增自定义主题、`plugin prune`、`--plugin-url`、`.zip` 支持
- 09-SDK：新增 `CLAUDE_CODE_SESSION_ID`、`localSettings`、`mcp_authenticate`
- 11-企业实战：新增 `parentSettingsBehavior`、`claude project purge`、Bedrock service tier
- 12-Remote-Control：扩展 v2.1.121+ 和 v2.1.133 增强条目
- 13-Channels：更新 `--channels` 支持 Console auth
- README：版本徽章、功能描述、版本追踪表同步更新

---

## [v2.1.119] - 2026-04-26

### 新增

- **全库教程版本升级至 Claude Code v2.1.119 + OpenClaw v2026.4.24**
- 版本号、徽章、README 同步更新

---

## [v2.1.92] - 2026-04-29

### 修复

- 补齐 12/13 教程课程信息头（GitHub / 公众号 / X / 博客）
- 同步 Claude Code command 和 agent 文档
- 移除误提交的计划文件（findings.md、progress.md）

---

## [v2.1.78] - 2026-04-07

### 新增

- **新增 12-Remote Control 完整指南**
- **新增 13-Channels 与计划任务完整指南**
- 01-安装指南新增第 8.5 部分：模型配置完整章节（+379 行）
- 删除独立的 12-Claude-Code 模型配置完整指南.md（内容合并到安装指南）
- 同步更新快速导航卡：14 个教程 → 13 个，序号重排
- 对齐 Remote/Channels 教程序号与文件名（12/13）并修正全库链接

### 修复

- 教程版本对齐与口径修正
- 在输出格式代码块前添加空行，改进文档渲染

### 修改

- 更新配置文档：`allowedTools` 改为 `allow`

---

## [v2.1.69] - 2026-03-18

### 新增

- 补充 Claude Code v2.1.69→v2.1.78 新功能到全部教程
- 更新 README 和快速导航卡，同步 v2.1.78 新功能

---

## OpenClaw 重写 - 2026-02-26

### 新增

- OpenClaw 全套文档重写：修正技术口径，补足入门路径和排障说明
- 新增 06-Subagent 子代理教程 + 全站模型名更新

### 修复

- 全量审核修复 OpenClaw 教程 01-11 全部虚构配置
- 修正 OpenClaw 教程 10 处配置错误（验证 GitHub 源码）
- 修复 6 篇 OpenClaw 教程 28 处虚构配置 + GitHub 仓库名修正
- 安装指南新增 NPM 备选方案 + Windows PATH 详细排查
- 修正安装指南 Windows 路径 + Hooks 输出机制纠错

---

## 项目初始化 - 2026-02-25

### 新增

- **Claude Code x OpenClaw 中文教程** 发布，项目从单一工具教程扩展为双工具学习路径
- 初始化 Claude Code 中文教程项目
- 新增 Git Worktree 内置并行任务隔离功能文档
- 全面迭代教程适配 Claude Code v2.1.45
- 清除全部待办项 — Task/Subagent、权限系统、新 MCP 服务

### 修复

- 重写 07-Plugins 教程 — 清除 60+ 处虚假 CLI 命令
- 全面体检修复 — 7 个 CRITICAL + 5 个 WARNING
- 二次验证修复 5 篇文档 16 处确认错误
- 修复 03-Commands 指南嵌套代码块渲染问题
- 移除 02-基础使用指南中 `#` 前缀的错误描述

---

> 格式参考：基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)
