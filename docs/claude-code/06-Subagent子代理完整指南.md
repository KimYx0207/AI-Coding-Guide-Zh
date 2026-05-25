# Subagent 子代理完整指南：官方 Subagents、Task 委派与社区代理资源

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：1-2小时
> - **难度等级**：⭐⭐⭐ 中级
> - **更新日期**：2026年4月
> - **适用版本**：Claude Code v2.1.150（验证于 2026-05-25）

---

## 📚 本课学习目标

<p align="center"><img src="../../images/official/claude-code-agent-view-dark.png" alt="Claude Code 官方 Agent View 深色界面：Needs input、Working、Completed 分组" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-product-ui.jpg" alt="Claude Code 官方 CLI 任务界面：任务执行、文件变更与终端状态" width="720"/></p>

完成本课学习后，你将能够：

1. **理解子代理的概念**：知道 Subagent 是什么、怎么工作的
2. **掌握官方子代理入口**：知道 `.claude/agents/`、`/agents`、Task 委派各自负责什么
3. **分清官方能力与社区资源**：明确 VoltAgent 之类的第三方代理包不是 Claude Code 官方内置
4. **提升开发效率**：在实际项目中合理使用多代理并行协作

---

## 术语表

| 术语 | 英文全称 | 通俗解释 |
|------|----------|----------|
| **Subagent** | Sub-agent | 子代理，Claude Code 通过 Agent 工具启动的专业化 AI 代理 |
| **VoltAgent** | - | 社区维护的 awesome-claude-code-subagents 开源项目 |
| **Agent Definition** | - | `.md` 格式的代理定义文件，描述代理的角色、能力和行为规范 |
| **Agent 工具** | Agent Tool | Claude Code 内置工具，用于启动子代理执行独立任务；旧资料可能写作 Task |
| **并行调用** | Parallel Invocation | 同时启动多个子代理处理不同任务，提高效率 |

---

## ⚠️ 重要提醒：Token 消耗

<p align="center"><img src="../../images/official/claude-code-agent-view.png" alt="Claude Code 官方 Agent View 多后台会话界面" width="720"/></p>

> 使用多 Agent 并行调用的 **token 消耗量巨大**。每启动一个子代理都会消耗独立的上下文窗口。
> 建议按需调用，不要一次性启动太多代理。

---

# 第一部分：官方快速上手

## 🎯 官方主路径：先理解，再扩展

官方 Subagents 的最小闭环不是“先去装一个第三方代理包”，而是：

1. **知道 Claude Code 可以用 Agent 工具委派子任务**
2. **知道项目级 / 用户级子代理定义文件放在哪里**
3. **知道如何在当前项目里启用和查看它们**

### 你需要记住的 3 个入口

| 入口 | 作用 | 什么时候用 |
|------|------|-----------|
| **Agent 工具** | 把一个子任务委派给独立上下文窗口 | 日常并行处理 |
| **`.claude/agents/`** | 项目级子代理定义目录 | 当前仓库专用代理 |
| **`~/.claude/agents/`** | 用户级子代理定义目录 | 跨项目复用代理 |

### 官方最小示例

```text
请开一个 reviewer 子代理，检查这次改动的回归风险和缺失测试。
```

```text
并行开两个子代理：
1. 一个检查后端接口变更
2. 一个检查前端样式回归
```

### 查看与管理

- 在 Claude Code 里用 `/agents` 查看当前已启用的子代理
- 项目级定义优先于用户级定义
- 子代理最适合做**边界清晰、可独立完成**的任务，不适合把主流程完全拆碎

---

# 第二部分：社区代理资源（VoltAgent 等）

> 这一部分讲的是**第三方社区资源**，不是 Claude Code 官方内置目录。

## 方法一：交互式脚本安装（社区方案）

```bash
git clone https://github.com/VoltAgent/awesome-claude-code-subagents.git
cd awesome-claude-code-subagents
./install-agents.sh
```

## 方法二：独立快捷安装（社区方案）

```bash
curl -sO https://raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/install-agents.sh
chmod +x install-agents.sh
./install-agents.sh
```

## 方法三：手动安装（社区方案）

1. **确定存放路径**：
   - **全局可用**：将代理文件放入 `~/.claude/agents/`
   - **项目专用**：将代理文件放入当前项目根目录下的 `.claude/agents/`
2. **复制文件**：从社区仓库中选择需要的 `.md` 代理定义文件，放到对应目录。

## 💡 使用小贴士

- **如何查看**：安装完成后，在 Claude Code 中输入 `/agents`
- **如何调用**：优先用自然语言描述任务边界，再让 Claude 选择是否委派
- **优先级规则**：项目特定代理优先于全局代理

---

# 第三部分：VoltAgent 代理目录总览

> 以下目录是 VoltAgent 提供的社区代理集合，适合“缺能力再补能力”，不建议当成官方默认菜单来理解。

---

## 1. 核心开发 (Core Development)

*插件包：`voltagent-core-dev`* — 处理日常编码任务的基础专家。

| 代理 | 说明 |
|------|------|
| [api-designer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/api-designer.md) | REST 和 GraphQL API 架构师 |
| [backend-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/backend-developer.md) | 可扩展 API 的服务器端专家 |
| [electron-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/electron-pro.md) | 桌面应用程序专家 |
| [frontend-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/frontend-developer.md) | React、Vue 和 Angular 的 UI/UX 专家 |
| [fullstack-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/fullstack-developer.md) | 端到端功能开发 |
| [graphql-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/graphql-architect.md) | GraphQL Schema 和 Federation 专家 |
| [microservices-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/microservices-architect.md) | 分布式系统设计师 |
| [mobile-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/mobile-developer.md) | 跨平台移动专家 |
| [ui-designer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/ui-designer.md) | 视觉设计和交互专家 |
| [websocket-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/websocket-engineer.md) | 实时通信专家 |
| [wordpress-master](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-dev/wordpress-master.md) | WordPress 开发和优化专家 |

---

## 2. 语言专家 (Language Specialists)

*插件包：`voltagent-lang`* — 具备特定编程语言和框架深厚知识的专家。

| 代理 | 说明 |
|------|------|
| [typescript-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/typescript-pro.md) | TypeScript 专家 |
| [python-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/python-pro.md) | Python 生态系统大师 |
| [rust-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/rust-engineer.md) | 系统编程专家 |
| [golang-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/golang-pro.md) | Go 并发专家 |
| [java-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/java-architect.md) | 企业级 Java 专家 |
| [javascript-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/javascript-pro.md) | JavaScript 开发专家 |
| [react-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/react-expert.md) | React 18+ 现代模式专家 |
| [vue-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/vue-expert.md) | Vue 3 Composition API 专家 |
| [angular-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/angular-architect.md) | Angular 15+ 企业模式专家 |
| [nextjs-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/nextjs-developer.md) | Next.js 14+ 全栈专家 |
| [swift-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/swift-expert.md) | iOS 和 macOS 专家 |
| [kotlin-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/kotlin-expert.md) | 现代 JVM 语言专家 |
| [cpp-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/cpp-pro.md) | C++ 性能专家 |
| [csharp-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/csharp-developer.md) | .NET 生态系统专家 |
| [php-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/php-pro.md) | PHP Web 开发专家 |
| [sql-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/sql-pro.md) | 数据库查询专家 |
| [django-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/django-developer.md) | Django 4+ Web 开发专家 |
| [laravel-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/laravel-expert.md) | Laravel 10+ PHP 框架专家 |
| [rails-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/rails-expert.md) | Rails 8.1 快速开发专家 |
| [spring-boot-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/spring-boot-engineer.md) | Spring Boot 3+ 微服务专家 |
| [flutter-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/flutter-expert.md) | Flutter 3+ 跨平台移动开发专家 |
| [elixir-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/elixir-expert.md) | Elixir 和 OTP 容错系统专家 |
| [dotnet-core-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/dotnet-core-expert.md) | .NET 8 跨平台专家 |
| [dotnet-framework-4.8-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/dotnet-framework-4.8-expert.md) | .NET Framework 传统企业专家 |
| [powershell-5.1-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/powershell-5.1-expert.md) | Windows PowerShell 5.1 自动化专家 |
| [powershell-7-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-languages/powershell-7-expert.md) | 跨平台 PowerShell 7+ 自动化专家 |

---

## 3. 基础设施 (Infrastructure)

*插件包：`voltagent-infra`* — 负责 DevOps、云计算和系统部署。

| 代理 | 说明 |
|------|------|
| [cloud-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/cloud-architect.md) | AWS/GCP/Azure 专家 |
| [devops-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/devops-engineer.md) | CI/CD 和自动化专家 |
| [kubernetes-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/kubernetes-expert.md) | 容器编排大师 |
| [terraform-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/terraform-engineer.md) | 基础设施即代码专家 |
| [database-admin](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/database-admin.md) | 数据库管理专家 |
| [sre](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/sre.md) | 站点可靠性工程专家 |
| [deployment-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/deployment-engineer.md) | 部署自动化专家 |
| [azure-infra-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/azure-infra-engineer.md) | Azure 基础架构专家 |
| [network-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/network-engineer.md) | 网络基础设施专家 |
| [platform-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/platform-engineer.md) | 平台架构专家 |
| [security-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/security-engineer.md) | 基础设施安全专家 |
| [incident-responder](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/incident-responder.md) | 系统事件响应专家 |
| [devops-incident-responder](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/devops-incident-responder.md) | DevOps 事件管理 |
| [windows-infra-admin](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/03-infrastructure/windows-infra-admin.md) | AD、DNS、DHCP 和 GPO 自动化专家 |

---

## 4. 质量与安全 (Quality & Security)

*插件包：`voltagent-qa-sec`* — 负责测试、安全审计和代码质量保证。

| 代理 | 说明 |
|------|------|
| [code-reviewer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/code-reviewer.md) | 代码质量守护者 |
| [security-auditor](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/security-auditor.md) | 安全漏洞专家 |
| [qa-automation-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/qa-automation-engineer.md) | 测试自动化专家 |
| [performance-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/performance-engineer.md) | 性能优化专家 |
| [debugging-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/debugging-expert.md) | 高级调试专家 |
| [error-detective](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/error-detective.md) | 错误分析和解决专家 |
| [penetration-tester](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/penetration-tester.md) | 道德黑客专家 |
| [architecture-reviewer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/architecture-reviewer.md) | 架构评审专家 |
| [accessibility-tester](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/accessibility-tester.md) | A11y 合规专家 |
| [chaos-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/chaos-engineer.md) | 系统弹性测试专家 |
| [compliance-auditor](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/compliance-auditor.md) | 监管合规专家 |
| [testing-automation-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/testing-automation-expert.md) | 测试自动化框架专家 |
| [ad-security-auditor](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/ad-security-auditor.md) | Active Directory 安全审核专家 |
| [powershell-security-hardener](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-qa-security/powershell-security-hardener.md) | PowerShell 安全加固专家 |

---

## 5. 数据与人工智能 (Data & AI)

*插件包：`voltagent-data-ai`* — 数据工程、机器学习和 AI 专家。

| 代理 | 说明 |
|------|------|
| [ai-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/ai-engineer.md) | 人工智能系统设计与部署专家 |
| [llm-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/llm-architect.md) | 大型语言模型架构师 |
| [ml-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/ml-engineer.md) | 机器学习系统专家 |
| [machine-learning-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/machine-learning-engineer.md) | 机器学习专家 |
| [data-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/data-engineer.md) | 数据管道架构师 |
| [data-scientist](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/data-scientist.md) | 分析和洞察专家 |
| [data-analyst](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/data-analyst.md) | 数据洞察与可视化专家 |
| [database-optimizer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/database-optimizer.md) | 数据库优化专家 |
| [postgres-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/postgres-pro.md) | PostgreSQL 数据库专家 |
| [mlops-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/mlops-engineer.md) | MLOps 和模型部署专家 |
| [nlp-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/nlp-engineer.md) | 自然语言处理工程师 |
| [prompt-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/prompt-engineer.md) | 提示优化专家 |

---

## 6. 开发者体验 (Developer Experience)

*插件包：`voltagent-dev-exp`* — 提升开发效率、工具链和文档。

| 代理 | 说明 |
|------|------|
| [refactoring-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/refactoring-expert.md) | 代码重构专家 |
| [documentation-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/documentation-engineer.md) | 技术文档专家 |
| [git-workflow-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/git-workflow-manager.md) | Git 工作流和分支专家 |
| [legacy-code-modernizer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/legacy-code-modernizer.md) | 遗留代码现代化专家 |
| [mcp-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/mcp-developer.md) | 模型上下文协议专家 |
| [build-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/build-engineer.md) | 构建系统专家 |
| [cli-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/cli-developer.md) | 命令行工具创建器 |
| [dependency-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/dependency-manager.md) | 软件包和依赖项专家 |
| [dx-optimizer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/dx-optimizer.md) | 开发者体验优化专家 |
| [tooling-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/tooling-engineer.md) | 开发工具专家 |
| [slack-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/slack-expert.md) | Slack 平台和 @slack/bolt 专家 |
| [powershell-ui-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/powershell-ui-architect.md) | PowerShell UI/UX 专家 |
| [powershell-module-architect](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-dev-experience/powershell-module-architect.md) | PowerShell 模块架构专家 |

---

## 7. 专业领域 (Specialized Domains)

*插件包：`voltagent-domains`* — 特定垂直领域技术专家。

| 代理 | 说明 |
|------|------|
| [blockchain-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/blockchain-developer.md) | Web3 和加密货币专家 |
| [game-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/game-developer.md) | 游戏开发专家 |
| [fintech-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/fintech-engineer.md) | 金融科技专家 |
| [iot-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/iot-engineer.md) | 物联网系统开发人员 |
| [embedded-systems-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/embedded-systems-engineer.md) | 嵌入式和实时系统专家 |
| [api-documenter](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/api-documenter.md) | API 文档专家 |
| [seo-specialist](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/seo-specialist.md) | 搜索引擎优化专家 |
| [mobile-app-developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/mobile-app-developer.md) | 移动应用专家 |
| [payment-integration-specialist](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/payment-integration-specialist.md) | 支付系统专家 |
| [quantitative-analyst](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/quantitative-analyst.md) | 量化分析专家 |
| [risk-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/risk-manager.md) | 风险评估和管理专家 |
| [m365-admin](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/m365-admin.md) | Microsoft 365 管理专家 |

---

## 8. 业务与产品 (Business & Product)

*插件包：`voltagent-biz`* — 产品管理、业务分析和敏捷流程。

| 代理 | 说明 |
|------|------|
| [product-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/product-manager.md) | 产品战略专家 |
| [business-analyst](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/business-analyst.md) | 需求专家 |
| [project-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/project-manager.md) | 项目管理专家 |
| [scrum-master](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/scrum-master.md) | 敏捷方法论专家 |
| [technical-writer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/technical-writer.md) | 技术文档专家 |
| [ux-researcher](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/ux-researcher.md) | 用户研究专家 |
| [customer-success-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/customer-success-manager.md) | 客户成功专家 |
| [sales-engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/sales-engineer.md) | 技术销售专家 |
| [legal-advisor](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/legal-advisor.md) | 法律和合规专家 |
| [content-marketing-specialist](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/content-marketing-specialist.md) | 内容营销专家 |

---

## 9. 元数据与编排 (Meta & Orchestration)

*插件包：`voltagent-meta`* — 负责代理之间的协调、任务分配和管理。

| 代理 | 说明 |
|------|------|
| [multi-agent-coordinator](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/multi-agent-coordinator.md) | 高级多智能体编排 |
| [workflow-orchestrator](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/workflow-orchestrator.md) | 复杂工作流自动化 |
| [agent-organizer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/agent-organizer.md) | 多代理协调器 |
| [agent-installer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/agent-installer.md) | 通过 GitHub 浏览并安装代理程序 |
| [context-manager](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/context-manager.md) | 上下文优化专家 |
| [task-dispatcher](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/task-dispatcher.md) | 任务分配专家 |
| [error-coordinator](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/error-coordinator.md) | 错误处理和恢复专家 |
| [performance-monitor](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/performance-monitor.md) | 代理性能优化 |
| [knowledge-synthesizer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/knowledge-synthesizer.md) | 知识聚合专家 |
| [it-ops-orchestrator](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/it-ops-orchestrator.md) | IT 运维工作流编排专家 |
| [pied-piper](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/09-meta-orchestration/pied-piper.md) | SDLC 工作流 AI 子代理团队协调 |

---

## 10. 研究与分析 (Research & Analysis)

*插件包：`voltagent-research`* — 负责搜索、市场调研和数据分析。

| 代理 | 说明 |
|------|------|
| [research-analyst](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/research-analyst.md) | 综合研究专家 |
| [competitive-analyst](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/competitive-analyst.md) | 竞争情报专家 |
| [market-researcher](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/market-researcher.md) | 市场分析和消费者洞察 |
| [search-expert](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/search-expert.md) | 高级信息检索专家 |
| [trend-analyst](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/trend-analyst.md) | 新兴趋势和预测专家 |
| [data-researcher](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/data-researcher.md) | 数据发现与分析专家 |

---

# 第四部分：Agent Teams 多代理团队协作 🆕

> **实验性功能**：Agent Teams 当前仍需显式开启实验开关后再使用，不应默认视为稳定主路径。

> **开启方式**：设置环境变量 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`，然后再进入相关工作流。

**一句话理解**：如果说普通 Subagent 是"你指派一个助手去干活"，那 Agent Teams 就是"你组建一个项目组，分工合作"。

## 核心概念

> **v2.1.139→v2.1.150 关键更新**：`claude agents` Agent View 已成为管理运行中、等待输入和已完成会话的重要入口；`claude agents --json` 可用于脚本化查看后台会话；`--cwd`、`--add-dir`、`--settings`、`--mcp-config`、`--plugin-dir`、`--permission-mode`、`--model`、`--effort` 等参数让后台会话更容易复用当前项目配置。Windows 与 worktree 场景的隔离和清理也有多轮修复。

| 概念 | 说明 | 类比 |
|------|------|------|
| **Team Lead** | 团队领导代理，负责分配任务和协调进度 | 项目经理 |
| **Teammate** | 团队成员代理，执行具体任务并汇报 | 开发工程师 |
| **TaskList** | 共享任务列表，所有成员可见进度和状态 | 看板 / Trello |
| **SendMessage** | 代理间通信机制，支持直接消息和广播 | 团队群聊 |

## 与普通 Subagent/Task 的区别

| 特性 | 普通 Subagent/Task | Agent Teams |
|------|-------------------|-------------|
| 协作模式 | 一对一（主代理 → 子代理） | 多对多（团队协作） |
| 任务管理 | 各自独立，互不感知 | 共享任务列表，实时同步 |
| 通信方式 | 子代理返回结果给主代理 | 团队成员间可互相通信 |
| 生命周期 | 任务完成即退出 | 持续运行直到团队解散 |
| 适用场景 | 独立子任务 | 复杂项目分工 |

## 典型使用场景

- **并行开发**：前端、后端、测试代理同时工作，通过 TaskList 共享进度
- **代码审查分工**：安全审查、性能审查、风格审查代理并行检查，汇总结果
- **大型重构**：多个模块同时修改，团队成员间协调接口变更

## 快速示例

```text
# 在 Claude Code 中，使用自然语言请求创建团队
You: 帮我组建一个团队，并行处理以下任务：
     1. 重构用户认证模块
     2. 编写 API 集成测试
     3. 更新相关文档
```

Team Lead 会自动将任务分配给不同的 Teammate，各成员独立工作并通过 SendMessage 同步关键信息。

> 💡 **何时用哪个？**
> - **简单独立任务**（翻译文件、生成测试）→ 普通 Subagent/Task，更轻量
> - **复杂协作项目**（多模块重构、全栈开发）→ Agent Teams，但前提是你愿意接受实验性行为和额外编排成本

---

## v2.1.133→v2.1.150 重要变更：worktree、Agent View 和子代理环境

### `worktree.baseRef`（v2.1.133）

当 Claude Code 为子代理或并行任务创建 git worktree 时，新 worktree 从哪里分叉？这个行为现在可以通过 `worktree.baseRef` 设置控制：

| 值 | 分叉来源 | 适用场景 |
|---|---|---|
| `fresh`（默认） | `origin/<default-branch>` | 确保从远程最新代码开始，适合协作项目 |
| `head` | 本地 `HEAD` | 基于你当前工作状态继续，适合单人项目 |

```json
// .claude/settings.json
{
  "worktree.baseRef": "head"
}
```

**注意**：默认值从旧行为（head）变更为 `fresh`。如果你发现新 worktree 丢失了本地未推送的更改，将 `baseRef` 设为 `head`。

### `CLAUDE_CODE_FORK_SUBAGENT`（v2.1.132+）

当 Skill 使用 `context: fork` 模式（即 Forked Context 子代理）时，子进程环境变量 `CLAUDE_CODE_FORK_SUBAGENT` 会被自动设为 `1`。你可以在脚本或 Hook 中检测这个变量来区分"主会话"和"fork 子代理"。

### 子代理 Skill 发现修复

v2.1.121 修复了子代理无法正确发现项目级 Skills 的问题。如果你之前遇到过"子代理看不到项目 Skills"的情况，升级到 v2.1.121+ 后应该已经解决。

---

> **下一步学习**：想深入了解如何自定义代理定义文件？请参考 [07-Skills定制完整指南](./07-Skills定制完整指南.md) 中关于 Agent 配置的部分。
