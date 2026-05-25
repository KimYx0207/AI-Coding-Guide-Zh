# Skills定制完整指南：打造专属AI能力包的实战手册

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **预计学时**：8-10小时
> - **难度等级**：⭐⭐ 入门级（有Claude Code基础即可）
> - **更新日期**：2026年4月
> - **适用版本**：Claude Code v2.1.150（验证于 2026-05-25）
> - **前置要求**：已完成Claude Code安装和Commands基础使用
> - **🆕 专属内容**：Hooks系统、Forked Sub-Agents、Hot Reloading

---

## 本课学习目标

<p align="center"><img src="../../images/official/claude-code-agent-view-dark.png" alt="Claude Code 官方 Agent View 深色界面：Needs input、Working、Completed 分组" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-agent-view.png" alt="Claude Code 官方 Agent View：多后台会话状态" width="720"/></p>

<p align="center"><img src="../../images/official/claude-code-product-ui.jpg" alt="Claude Code 官方 CLI 任务界面：任务执行、文件变更与终端状态" width="720"/></p>

完成本课学习后，你将能够：

1. **理解Skills的核心价值**：掌握Skills与Commands的本质区别和协作方式
2. **创建第一个Skill**：5分钟内完成最简单的Skill配置并看到效果
3. **掌握SKILL.md结构**：理解YAML Frontmatter和Markdown Body的编写规范
4. **掌握Skill目录结构**：理解scripts、templates等资源组织方式
5. **掌握渐进式披露机制**：理解元数据→指令→资源的三层加载逻辑
6. **利用Hot Reloading**：快速迭代Skill，修改后自动生效
7. **配置Sandbox安全**：正确设置文件系统、网络、内存等权限边界
8. **集成Python脚本**：实现自动化工具扩展Claude Code能力
9. **上传自定义Skill**：通过Web界面或API上传和管理Skill
10. **排查Skill故障**：独立解决90%的常见配置和执行问题
11. **实战案例分析**：深度理解企业级Skill架构设计

---

## 学习路径导航（先看这里！）

**根据你的情况选择学习路径**：这是一篇4000+行的长教程，不用全看！根据你的目标选择路径。

### 路径A：快速上手（30分钟）

**适合人群**：急着体验Skills，想快速创建一个看效果

**只看这些章节**（其他跳过）：

```
✅ 术语表（5分钟） - 快速了解Skill核心概念
✅ 第一部分1.1-1.2：Skills简介（5分钟） - 理解Skill是什么
✅ 第二部分：5分钟快速开始（15分钟） - 创建第一个Skill
✅ 第三部分3.1：SKILL.md基础（5分钟） - 最核心的配置
```

**30分钟后你能达到**：成功创建第一个Skill，Claude Code能识别并使用你的专属能力

---

### 路径B：完整学习（6-8小时）

**适合人群**：想深入理解Skills，掌握完整的开发能力

**学习顺序**：从头到尾所有章节

**建议分段学习**：
- 第1天（2小时）：第1-3部分（理解+目录结构）
- 第2天（2小时）：第4-5部分（提示词+脚本集成）
- 第3天（2小时）：第6-7部分（实战案例+故障排查）
- 第4天（1小时）：第8-9部分（FAQ+附录）

---

### 路径C：问题排查（10分钟）

**适合人群**：Skill配置出问题，需要快速解决

**直接跳到这些章节**：

```
🔧 第七部分：故障排查 - 按错误类型查找解决方案
🔧 第八部分：FAQ - 20个常见问题解答
```

**使用方法**：
1. 按 `Ctrl + F` 搜索你的错误信息关键词
2. 找到对应的Q&A
3. 按步骤解决

---

### 路径D：专项学习（30-60分钟/主题）

**适合人群**：已经会创建Skill，想学习特定功能

| 想学什么 | 看哪几节 | 预计时间 |
|----------|---------|---------|
| **提示词工程** | 第四部分 | 1小时 |
| **Python脚本集成** | 第五部分 | 1.5小时 |
| **多步骤工作流** | 第六部分6.1节 | 45分钟 |
| **数据驱动架构** | 第六部分6.2节 | 1小时 |
| **企业级Skill设计** | 第六部分6.3节 | 1小时 |

---

## 术语表（小白必读）

在开始之前，先了解这些关键术语。**用生活类比帮助理解**：

| 术语 | 英文全称 | 通俗解释 | 生活类比 |
|------|----------|----------|----------|
| **Skill** | - | Claude Code的"能力包"，封装领域知识和工具 | 手机上的APP（如微信、淘宝） |
| **SKILL.md** | - | Skill的核心定义文件（必需），包含YAML Frontmatter和Markdown Body | APP的完整说明书（安装信息+使用手册） |
| **YAML Frontmatter** | - | SKILL.md顶部的元数据区域（---包裹），定义name和description | APP的基本信息（名称、简介） |
| **Markdown Body** | - | SKILL.md中YAML后的指令部分，详细说明使用方法 | APP的详细操作手册 |
| **scripts/** | - | 脚本文件夹，存放可执行的工具程序 | APP的功能模块代码 |
| **templates/** | - | 模板文件夹，存放输出格式模板 | 文档模板库 |
| **Progressive Disclosure** | 渐进式披露 | 按需加载：元数据常驻内存，指令和资源按需加载 | 微信：先看图标，点开看功能，用时加载详情 |
| **Hot Reloading** | - | 修改SKILL.md后自动生效，无需重启 | APP热更新，改完立即生效 |
| **Sandbox** | 沙箱 | 隔离执行环境，限制文件/网络访问，保证安全 | APP的权限管理（只能访问相册） |
| **Commands** | 斜杠命令 | 显式触发的操作入口 | APP里的功能按钮 |
| **YAML** | YAML Ain't Markup Language | 配置文件格式，易读易写 | 填写表格（有固定格式） |
| **stdin/stdout** | Standard Input/Output | 脚本的数据输入输出通道 | 快递的收发窗口 |

---

## 第一部分：Skills简介（10分钟理解）

### 1.1 Skills是什么

**一句话理解**：Skills是Claude Code的"能力APP"，把特定领域的知识、规则、工具打包成可复用的模块，让AI瞬间变成该领域的专家。

#### 为什么需要Skills？

**没有Skills之前（每次都从零开始）**：

```
问题：AI没有记忆，每次对话都要重新说明

你：帮我写一篇公众号文章
Claude：好的，请问什么风格？字数多少？有什么特殊要求？

...下次对话...

你：再帮我写一篇
Claude：好的，请问什么风格？字数多少？（又从零开始问）
```

**有了Skills之后（专业知识即装即用）**：

```
解决方案：预置领域知识，AI直接变成专家

你：帮我写一篇公众号文章
Claude：[自动加载公众号写作Skill]
       [读取老金风格规范、爆款公式、质量标准]
       好的！基于V8.0爆款规律，我来帮你...
       [自动调用标题生成器、质量检测器]
```

**生活类比**：
- **没有Skills**：每次打车都要从零教司机认路
- **有Skills后**：安装了高德地图APP，司机直接导航到达（知识预装）

#### Skills的核心价值

| 对比维度 | 没有Skills | 有Skills后 |
|----------|-----------|------------|
| **知识积累** | 每次对话从零开始 | 领域知识预置，即用即专业 |
| **团队协作** | 每人都要教AI一遍 | 配置一次，全员共享 |
| **质量一致** | 输出质量随机 | 标准化流程，质量稳定 |
| **效率** | 大量时间在沟通需求 | 直接进入核心任务 |
| **可维护性** | 知识散落在聊天记录 | 集中管理，版本可控 |

### 1.2 Skills vs Commands：深度对比

**这是最常被问到的问题**：Skill和Command有什么区别？什么时候用哪个？

#### 一句话区分

- **Commands**：**触发器**，是用户交互的入口点（"按钮"）
- **Skills**：**能力包**，是知识和工具的集合（"APP"）

#### 详细对比表

| 对比维度 | Commands（斜杠命令） | Skills（能力包） |
|----------|---------------------|-----------------|
| **定位** | 触发器/入口点 | 能力包/知识库 |
| **复杂度** | 单个Markdown文件 | 多文件目录结构 |
| **触发方式** | 显式调用 `/command` | 自动识别 + 显式调用 |
| **状态管理** | 无状态 | 可以维护状态和配置 |
| **工具集成** | 有限（直接写在md里） | 强大（可集成Python/JS脚本） |
| **知识容量** | 几百到几千字 | 可达数万字 |
| **可维护性** | 简单直接 | 模块化分层 |
| **适用场景** | 单一任务 | 复杂工作流 |

#### 协作关系图

```
                    用户输入
                       │
                       ▼
           ┌────────────────────────┐
           │      CLAUDE.md         │ ← 全局上下文
           └────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌────────────────┐           ┌──────────────────┐
│   Commands     │ ←───────→ │     Skills       │
│  （触发层）     │   调用     │   （能力层）      │
│  /write        │           │ gongzhonghao-    │
│  /title-gen    │           │ writer/          │
└────────────────┘           └──────────────────┘
        │                             │
        ▼                             ▼
┌────────────────┐           ┌──────────────────┐
│ 简单任务直接   │           │ prompts/         │
│ 在Command里    │           │ scripts/         │
│ 完成          │           │ config/          │
└────────────────┘           │ templates/       │
                            └──────────────────┘
```

**协作模式示例**：`/write` 命令与公众号写作Skill

```markdown
# 01-write.md (Command层)
当用户输入 /write 时:
1. 读取 `.claude/skills/gongzhonghao-writer/prompts/baokuan-rules.md`
2. 调用 `scripts/title_generator.py` 生成标题
3. 应用 `prompts/laojin-style.md` 风格规范
4. 执行 `scripts/quality_detector.py` 质量检测
```

**最佳实践**：
- **简单任务**：直接用Command（如`/help`显示帮助）
- **复杂任务**：Command + Skill（Command是入口，Skill提供能力）

### 1.3 渐进式披露原理（Progressive Disclosure）

这是Skills系统的核心设计哲学，理解它能帮你更好地设计自己的Skill。

**核心思想**：只在用户需要时才展示复杂功能，避免信息过载。

#### 四层披露结构

**第一层：自动激活（用户无感）**
```
用户："帮我写一篇关于Claude Code的公众号文章"
Claude Code：[检测到"公众号"关键词，自动加载gongzhonghao-writer Skill]
           "好的，我来帮你写..."
```
用户完全不需要知道Skill的存在。

**第二层：显式调用（简单控制）**
```
用户：/write Claude Code新功能解析
Claude Code：[执行完整的写作工作流]
```
用户通过Slash命令明确触发，获得更可控的流程。

**第三层：深度定制（修改配置）**
```yaml
# SKILL.md的YAML Frontmatter部分
---
name: gongzhonghao-writer
description: 当用户提到"公众号"、"写文章"、"老金风格"等关键词时激活
---
```
用户可以修改触发条件和参数。

**第四层：完全控制（修改代码）**
```
用户可以:
- 修改SKILL.md的Markdown Body部分调整生成风格
- 编辑scripts/*.py改变处理逻辑
- 创建新的templates/定制输出格式
```

**设计优势**：
- 新手可以直接用，无需学习复杂配置
- 高级用户可以深度定制每个细节
- 团队可以将最佳实践沉淀到Skills中

### 1.4 什么时候该用Skills

**适合使用Skills的场景**：

| 场景类型 | 示例 | 为什么适合 |
|----------|------|-----------|
| **领域专业化** | 公众号写作、技术博客、学术论文 | 需要预置大量领域知识 |
| **知识积累** | 数据驱动的规则优化 | 需要持续迭代和版本管理 |
| **复杂工作流** | Research→写作→质检→发布 | 需要多步骤自动化 |
| **团队标准化** | 代码审查规范、文档模板 | 需要统一团队标准 |
| **可复用能力** | 跨项目共享的工具包 | 需要在多个项目使用 |

**不适合使用Skills的场景**：

| 场景类型 | 为什么不适合 | 替代方案 |
|----------|-------------|---------|
| **一次性任务** | 没有复用价值 | 直接在对话中描述 |
| **高度变化** | 每次都不同 | 灵活的Command |
| **无法标准化** | 完全依赖创意 | 保持AI自由发挥 |

---

## 第二部分：5分钟快速开始（立即见效）

**本节目的**：用最快速度创建第一个Skill，让你立即看到效果！

⏱️ **预计时间**：5-10分钟

### 2.1 创建你的第一个Skill

**为什么选这个示例？**

- ✅ 最简单，只需要1个文件夹 + 1个SKILL.md
- ✅ 效果直观，立即看到输出
- ✅ 无依赖，不需要安装任何东西
- ✅ 支持Hot Reloading（修改后自动生效）

**目标**：创建一个"代码注释生成器"Skill，自动为代码添加中文注释。

#### 步骤1：创建Skill文件夹

**这一步要做什么**：创建Skill的文件夹（文件夹名必须与skill名称一致）

**Windows系统（PowerShell）：**
```powershell
# 进入你的项目目录
cd C:\你的项目路径

# 创建Skill文件夹（名称必须小写，用连字符）
New-Item -ItemType Directory -Path ".claude\skills\code-commenter" -Force
```

**macOS/Linux系统：**
```bash
# 进入你的项目目录
cd ~/你的项目路径

# 创建Skill文件夹
mkdir -p .claude/skills/code-commenter
```

💡 **命名规范**：
- 文件夹名必须与YAML中的`name`字段一致
- 只能使用小写字母、数字、连字符（-）
- 不能有空格、下划线或特殊字符

#### 步骤2：创建SKILL.md文件

**这一步要做什么**：创建Skill的核心定义文件（YAML Frontmatter + Markdown Body）

**创建文件 `.claude/skills/code-commenter/SKILL.md`**：

**Windows（PowerShell）：**
```powershell
@'
---
name: code-commenter
description: 当用户要求"添加注释"、"代码注释"或"注释代码"时，自动为代码添加清晰的中文注释
---

# 代码注释生成器

## 角色定义
你是一位经验丰富的代码审查专家，擅长编写清晰、准确、有价值的代码注释。

## 何时激活
当用户说以下内容时激活本Skill：
- "帮我添加注释"
- "给这段代码加注释"
- "代码注释"
- "comment this code"

## 注释原则

### 1. 解释"为什么"而不是"是什么"
（示例代码：Python注释对比）
# ❌ 差的注释：循环遍历列表
for item in items:
    process(item)

# ✅ 好的注释：过滤掉已过期的订单，避免重复发货
for item in items:
    process(item)

### 2. 注释格式规范
- **函数/方法**：说明功能、参数、返回值、异常
- **复杂逻辑**：解释业务背景和设计决策
- **魔法数字**：说明数值含义（如：86400秒 = 24小时）

### 3. 语言要求
- 使用简洁的中文
- 避免废话和自明的注释
- 专业术语保持英文（如API、JWT、JSON）

## 输出格式
直接输出添加注释后的完整代码，不要额外解释或对话。
'@ | Out-File -FilePath ".claude\skills\code-commenter\SKILL.md" -Encoding utf8
```

**macOS/Linux：**
```bash
cat > .claude/skills/code-commenter/SKILL.md <<'EOF'
---
name: code-commenter
description: 当用户要求"添加注释"、"代码注释"或"注释代码"时，自动为代码添加清晰的中文注释
---

# 代码注释生成器

## 角色定义
你是一位经验丰富的代码审查专家，擅长编写清晰、准确、有价值的代码注释。

## 何时激活
当用户说以下内容时激活本Skill：
- "帮我添加注释"
- "给这段代码加注释"
- "代码注释"
- "comment this code"

## 注释原则

### 1. 解释"为什么"而不是"是什么"
（示例代码：Python注释对比）
# ❌ 差的注释：循环遍历列表
for item in items:
    process(item)

# ✅ 好的注释：过滤掉已过期的订单，避免重复发货
for item in items:
    process(item)

### 2. 注释格式规范
- **函数/方法**：说明功能、参数、返回值、异常
- **复杂逻辑**：解释业务背景和设计决策
- **魔法数字**：说明数值含义（如：86400秒 = 24小时）

### 3. 语言要求
- 使用简洁的中文
- 避免废话和自明的注释
- 专业术语保持英文（如API、JWT、JSON）

## 输出格式
直接输出添加注释后的完整代码，不要额外解释或对话。
EOF
```

💡 **SKILL.md结构说明**：
- **YAML Frontmatter**（`---`包裹）：
  - `name`：小写、无空格、可用连字符（如`code-commenter`）
  - `description`：清晰描述触发场景，Claude用此判断是否激活
- **Markdown Body**：详细指令，只在Skill被激活后加载
- 这实现了"渐进式披露"：元数据常驻内存，指令按需加载

#### 步骤3：验证Skill配置

**验证文件结构：**
```bash
# 查看Skill目录结构
tree .claude/skills/code-commenter/
# 或者用ls
ls -la .claude/skills/code-commenter/

# 预期输出：
# .claude/skills/code-commenter/
# └── SKILL.md
```

**验证YAML格式：**
```bash
# 查看SKILL.md前几行（YAML部分）
head -n 10 .claude/skills/code-commenter/SKILL.md

# 应该显示：
# ---
# name: code-commenter
# description: 当用户要求"添加注释"...
# ---
```

#### 步骤4：测试Skill（利用Hot Reloading）

**Windows（PowerShell）：**

```powershell
@'
# 代码注释生成规范

## 角色定义
你是一位经验丰富的代码审查专家，擅长编写清晰、准确、有价值的代码注释。

## 注释原则

### 1. 解释"为什么"而不是"是什么"
（示例代码：Python注释对比）
# ❌ 差的注释：循环遍历列表
for item in items:

# ✅ 好的注释：过滤掉已过期的订单，避免重复发货
for item in items:

### 2. 注释格式规范
- **函数/方法**：说明功能、参数、返回值
- **复杂逻辑**：解释业务背景和设计决策
- **魔法数字**：说明数值含义

### 3. 语言要求
- 使用简洁的中文
- 避免废话和重复
- 专业术语保持英文（如API、JSON）

## 输出格式
直接输出添加注释后的完整代码，不要额外解释。
'@ | Out-File -FilePath ".claude\skills\code-commenter\SKILL.md" -Encoding utf8
```

**macOS/Linux：**

```bash
cat > .claude/skills/code-commenter/SKILL.md << 'EOF'
---
name: code-commenter
description: 当用户要求"添加注释"、"代码注释"或"注释代码"时，自动为代码添加清晰的中文注释
---

# 代码注释生成器

## 角色定义
你是一位经验丰富的代码审查专家，擅长编写清晰、准确、有价值的代码注释。

## 何时激活
当用户说以下内容时激活本Skill：
- "帮我添加注释"
- "给这段代码加注释"
- "代码注释"
- "comment this code"

## 注释原则

### 1. 解释"为什么"而不是"是什么"
示例：
（Python代码对比）
# ❌ 差的注释：循环遍历列表
for item in items:

# ✅ 好的注释：过滤掉已过期的订单，避免重复发货
for item in items:

### 2. 注释格式规范
- **函数/方法**：说明功能、参数、返回值、异常
- **复杂逻辑**：解释业务背景和设计决策
- **魔法数字**：说明数值含义（如：86400秒 = 24小时）

### 3. 语言要求
- 使用简洁的中文
- 避免废话和自明的注释
- 专业术语保持英文（如API、JWT、JSON）

## 输出格式
直接输出添加注释后的完整代码，不要额外解释或对话。
EOF
```

#### 步骤4：验证Skill配置

**验证文件结构：**
```bash
# 查看Skill目录结构
tree .claude/skills/code-commenter/
# 或者用ls
ls -la .claude/skills/code-commenter/

# 预期输出：
# .claude/skills/code-commenter/
# └── SKILL.md
```

**验证YAML格式：**
```bash
# 查看SKILL.md前几行（YAML部分）
head -n 10 .claude/skills/code-commenter/SKILL.md
```

#### 步骤5：测试Skill

**启动Claude Code：**
```bash
claude
```

**测试触发：**
```
你：帮我给这段代码添加注释

def calculate_discount(price, user_level):
    if user_level == "vip":
        return price * 0.8
    elif user_level == "svip":
        return price * 0.7
    else:
        return price
```

**预期响应：**
```python
def calculate_discount(price, user_level):
    """
    根据用户等级计算折扣后的价格

    Args:
        price: 原始价格
        user_level: 用户等级（vip/svip/普通）

    Returns:
        折扣后的价格
    """
    # VIP用户享受8折优惠
    if user_level == "vip":
        return price * 0.8
    # SVIP用户享受7折优惠
    elif user_level == "svip":
        return price * 0.7
    # 普通用户无折扣
    else:
        return price
```

🎯 **Hot Reloading体验**：修改SKILL.md后，无需重启Claude Code，下次对话时修改会自动生效！

### 2.2 验证Skill工作正常

**完整验证清单**：

- [ ] `.claude/skills/code-commenter/` 目录存在
- [ ] `SKILL.md` 文件格式正确（YAML Frontmatter + Markdown Body）
- [ ] 说"添加注释"等关键词时Claude能识别
- [ ] 生成的注释符合规范
- [ ] 修改SKILL.md后自动生效（Hot Reloading）

### 2.3 恭喜完成！

如果上面的测试都成功了，你已经创建了第一个可用的Skill！

**下一步建议**：
- 继续学习第三部分，了解完整的目录结构
- 尝试为你的工作领域创建专属Skill

---

## 第三部分：目录结构详解

**本节目的**：深入理解Skill的标准目录结构，为创建复杂Skill打基础。

### 3.1 标准目录结构

Skills采用**约定优于配置**的目录结构，每个Skill都是 `.claude/skills/` 下的一个独立目录：

```
.claude/skills/[skill-name]/
├── SKILL.md                # [必需] Skill核心定义文件（身份证+说明书）
├── scripts/                # [可选] 工具脚本目录（功能模块）
│   ├── processor.py        # Python处理脚本
│   ├── validator.js        # JavaScript验证脚本
│   └── utils/              # 工具函数
├── templates/              # [可选] 模板文件目录
│   ├── output-template.md  # 输出模板
│   └── report-template.md  # 报告模板
├── config/                 # [可选] 配置文件目录
│   └── settings.json       # 运行时配置
├── docs/                   # [可选] 内部文档
│   └── design.md           # 设计文档
└── data/                   # [可选] 数据文件
    └── knowledge-base.json # 知识库数据
```

#### 各目录用途说明

| 目录/文件 | 是否必需 | 用途 | 生活类比 |
|-----------|---------|------|----------|
| `SKILL.md` | ✅ 必需 | 定义Skill元信息(YAML)+详细指令(Markdown) | APP的安装包信息+完整说明书 |
| `scripts/` | 可选 | 可执行的工具脚本 | APP的功能代码 |
| `templates/` | 可选 | 输出内容的模板 | 文档模板 |
| `config/` | 可选 | 运行时配置参数 | APP的设置选项 |
| `docs/` | 可选 | 开发者内部文档 | 开发手册 |
| `data/` | 可选 | 静态数据文件 | 离线数据包 |

🎯 **重要说明**：当前版本不再使用`skill.yaml`和`prompts/`文件夹，所有内容统一到`SKILL.md`文件中！

### 3.2 SKILL.md配置详解

`SKILL.md` 是Skill的核心定义文件，由两部分组成：**YAML Frontmatter**（元数据）和**Markdown Body**（详细指令）。

#### YAML Frontmatter字段表

| 字段名 | 类型 | 是否必填 | 默认值 | 说明 |
|--------|------|---------|--------|------|
| `name` | string | 推荐 | 目录名 | Skill名称，同时作为`/`斜杠命令（小写、连字符分隔，最多64字符） |
| `description` | string | 推荐 | - | 简短描述（最多1024字符），Claude用此判断是否自动激活 |
| `context` | string | 可选 | - | 设为`fork`时在独立子代理上下文中运行（Forked Context） |
| `model` | string | 可选 | 继承 | 指定运行模型（如`opus`、`sonnet`、`haiku`） |
| `agent` | string | 可选 | - | 指定代理类型（如`Explore`） |
| `allowed-tools` | string | 可选 | 全部 | 限制可用工具列表（逗号分隔，如`Read, Grep, Glob`） |
| `user-invocable` | boolean | 可选 | true | 是否允许用户通过`/`命令手动调用 |
| `disable-model-invocation` | boolean | 可选 | false | 设为true时禁止Claude自动激活，只能手动`/`调用 |
| `argument-hint` | string | 可选 | - | 参数提示（如`[filename] [format]`） |

#### 最小配置示例

```yaml
---
# 最简单的SKILL.md（只有2个必填字段）
name: code-commenter
description: 当用户要求"添加注释"或"代码注释"时自动为代码添加清晰的中文注释
---

# 这里开始是Markdown Body部分
(详细指令内容...)
```

#### 完整配置示例（公众号写作助手）

```yaml
---
name: gongzhonghao-writer
description: 当用户提到"公众号"、"写文章"、"老金风格"等关键词时，自动激活AI写作助手系统
---

# 公众号写作助手 Skill

## 技能概述
本Skill提供数据驱动的AI公众号写作能力，包括：
- 爆款标题生成（5大公式）
- 老金风格文章创作
- 9维度质量检测
- 选题自动过滤

## 角色定义
你是一位经验丰富的公众号写作专家，擅长创作高质量、高传播性的内容。

## 核心能力
1. **爆款公式生成**：基于5大公式生成高转化标题
2. **9维度质量检测**：AI腔、自然度、真诚度等全面检测
3. **智能选题过滤**：三层架构判断是否值得写作

## 工作流程
(详细工作流程说明...)

## 输出规范
(输出格式要求...)
```

💡 **关键变化**：
- **YAML Frontmatter**：`name`和`description`为核心字段，还支持`context`、`model`、`allowed-tools`等可选字段
- **Markdown Body**：所有详细指令、规则、流程都在这里编写
- **不再需要**：`version`、`author`、`triggers`、`prompt_files`等旧版配置

### 3.3 Markdown Body编写规范

Markdown Body是SKILL.md的核心部分，包含所有详细指令。推荐遵循以下结构：

#### 推荐结构模板

```markdown
# [Skill名称]

## 一、角色定义
[AI的角色定位和专业背景]

## 二、核心能力
[列出3-5个核心能力]

## 三、工作流程
### 步骤1：[步骤名称]
[详细说明]

### 步骤2：[步骤名称]
[详细说明]

## 四、规则约束
[必须遵守的规则]

## 五、输出格式
[定义输出结构和格式]

## 六、示例展示
[好/坏示例对比]
```

#### 编写原则

1. **层次清晰**：使用多级标题组织内容
2. **简洁明确**：每段只讲一个要点
3. **可操作性强**：提供具体步骤而非抽象概念
4. **示例驱动**：用具体例子说明抽象规则

### 3.4 三种复杂度级别对比

根据你的需求，Skill可以从简单到复杂：

| 维度 | 简单Skill | 中等Skill | 复杂Skill |
|------|----------|----------|----------|
| **文件数** | 1个（SKILL.md） | 3-5个 | 10+个 |
| **总大小** | <5KB | 5-50KB | >50KB |
| **SKILL.md** | <100行 | 100-500行 | 500+行 |
| **scripts** | 0个 | 1-2个 | 5+个 |
| **config** | 无 | 1个JSON | 多个配置文件 |
| **适用场景** | 单一任务 | 多步骤流程 | 企业级系统 |
| **示例** | 代码注释器 | API文档生成器 | 公众号写作助手 |
| **维护难度** | 低 | 中 | 高 |

**建议**：
- 新手从简单Skill开始
- 随着需求增长逐步扩展
- 不要过度设计

### 3.5 核心特性详解

🎯 **掌握这些特性能让你的Skill开发事半功倍！**

#### Hot Reloading（热重载）

**功能说明**：修改SKILL.md后，无需重启Claude Code，下次对话时修改会自动生效。

**工作原理**：
```
用户修改SKILL.md
    ↓
Claude Code检测到文件变化
    ↓
自动重新加载Skill定义
    ↓
下次对话时应用新规则
```

**使用体验**：

```bash
# 传统方式（2.10之前）
1. 修改skill.yaml或prompts/*.md
2. 退出Claude Code
3. 重新启动claude
4. 测试修改

# Hot Reloading方式
1. 修改SKILL.md
2. 直接测试，立即生效 ✨
```

**注意事项**：
- YAML Frontmatter的修改会立即生效
- Markdown Body的修改会在下次对话时生效
- 如果修改未生效，可以尝试开始新对话或使用`/compact`压缩上下文后重试

#### Sandbox安全机制

**功能说明**：Claude Code提供OS级别的沙箱隔离，限制文件系统写入和网络访问。

> **重要**：Sandbox是Claude Code的全局安全功能（通过`/sandbox`命令启用），不是SKILL.md的frontmatter字段。它对所有Bash工具调用生效，包括Skill中的脚本执行。

**启用方式**：

```bash
# 在Claude Code会话中启用沙箱
/sandbox
```

**隔离能力**：

| 维度 | 说明 |
|------|------|
| **文件系统** | 只能写入启动目录及子目录，读取不受限 |
| **网络** | 只能连接已批准的服务器，阻止未授权的外部连接 |
| **OS级执行** | 基于Linux bubblewrap / macOS seatbelt的内核级隔离 |

**对Skill脚本的影响**：
- 当Sandbox启用时，Skill中`scripts/`目录的脚本也受沙箱限制
- 脚本无法写入项目目录之外的路径
- 脚本无法访问未批准的网络地址

#### 渐进式披露机制（详解）

**三层披露结构**：

```
第一层：元数据常驻
├─ YAML Frontmatter的name和description
├─ 始终在内存中，用于自动激活判断
└─ 极小的内存占用（<100字节）

第二层：指令按需加载
├─ Markdown Body在Skill激活时才加载
├─ 可以包含数千行的详细指令
└─ 用完即释放，不占用常驻内存

第三层：资源按需调用
├─ scripts/中的脚本只在调用时执行
├─ templates/中的模板只在渲染时读取
└─ config/中的配置只在需要时加载
```

**性能优势对比**：

| 方式 | 旧版本（skill.yaml+prompts/） | 新版本（SKILL.md） |
|------|---------------------------|------------------|
| **内存占用** | 所有prompts常驻 | 只加载元数据 |
| **激活速度** | 需要读取多个文件 | 读取单个文件 |
| **修改生效** | 需要重启 | Hot Reloading |
| **维护成本** | 多文件同步 | 单文件管理 |

---

## 第四部分：SKILL.md提示词工程

**本节目的**：掌握在SKILL.md中组织提示词的技巧和最佳实践。

🎯 **重要说明**：不再使用独立的`prompts/`文件夹，所有提示词内容统一写在SKILL.md的Markdown Body中！

### 4.1 提示词组织方式

**方式1：按功能分章节组织**（推荐）

```markdown
# 公众号写作助手

## 一、角色定义
你是一位经验丰富的公众号写作专家...

## 二、核心能力
1. 爆款标题生成
2. 老金风格创作
3. 质量检测

## 三、标题生成规范
### 公式1：工具推荐型
[详细说明...]

### 公式2：教程型
[详细说明...]

## 四、写作风格规范
### 语言特点
### 结构要求
### 禁忌事项

## 五、质量检测标准
[9维度检测标准...]
```

**方式2：按工作流阶段组织**

```markdown
# API文档生成器

## 阶段1：需求分析
[分析API结构和参数...]

## 阶段2：文档生成
[生成各部分文档...]

## 阶段3：质量检查
[检查文档完整性和准确性...]
```

### 4.2 章节命名规范

| 命名类型 | 命名模式 | 示例 | 适用场景 |
|---------|---------|------|---------|
| 数字序号 | `## 一、xxx` | `## 一、角色定义` | 主要章节 |
| 功能描述 | `## {功能}规范` | `## 标题生成规范` | 功能说明 |
| 层级结构 | `### {子功能}` | `### 公式1：工具推荐型` | 子功能划分 |
| 版本标记 | `## V{版本}变更` | `## V8.0新特性` | 版本演进 |

**最佳实践**：
1. 使用清晰的中文标题（面向中文AI）
2. 保持层次不超过3级
3. 章节长度适中（建议<500行）

### 4.3 提示词结构模板

一个完整的SKILL.md应该包含以下结构：

```markdown
---
name: skill-name
description: 简短描述
---

# [Skill名称]

## 一、角色定义
[定义AI扮演的角色和背景]

## 二、核心能力
[列出3-5个核心能力]

## 三、工作流程
### 步骤1：[步骤名称]
[详细说明和操作指南]

### 步骤2：[步骤名称]
[详细说明和操作指南]

## 四、规则约束
[定义必须遵守的规则]

## 五、示例展示
[提供具体的好/坏示例]

## 六、输出格式
[定义输出的结构和格式]
```

**实际示例**：

```markdown
---
name: title-generator
description: 当用户需要生成公众号标题时，自动应用5大爆款公式
---

# 标题生成Skill

## 一、角色定义
你是一位爆款标题专家，擅长创作高点击率的公众号标题，精通5大爆款公式。

## 二、核心能力
1. **工具推荐型**：品牌词+数字+推荐词
2. **教程型**：动作词+品牌词+场景
3. **问题解决型**：痛点+解决方案
4. **数据型**：数据+洞察
5. **案例型**：真实案例+收获

## 三、工作流程
### 步骤1：分析主题
- 提取核心关键词
- 确定目标受众
- 识别品牌词

### 步骤2：应用公式
为每个公式生成1-2个标题

### 步骤3：评分排序
按以下标准评分：
- 吸引力（30分）
- 相关性（30分）
- 可信度（20分）
- 可行动性（20分）

## 四、规则约束
1. 标题字数：15-30字
2. 必须包含品牌词（如Claude、Cursor）
3. 使用数字增加可信度
4. 避免标题党和虚假承诺

## 五、示例展示

**✅ 好的标题**：
- "Claude Code 3个隐藏技巧，让你的开发效率翻倍"（工具推荐型）
- "手把手教你用Cursor，从入门到精通只需2小时"（教程型）

**❌ 差的标题**：
- "这个工具太厉害了！"（没有具体信息）
- "99%的人不知道的秘密"（标题党）

## 六、输出格式
【推荐标题1】标题内容
公式：使用的标题公式
评分：XX分
推荐理由：为什么这个标题好

【备选标题2-5】...
```

### 4.4 提示词版本管理

**在SKILL.md中记录版本历史**：

```markdown
---
name: gongzhonghao-writer
description: 公众号写作助手V9.0
---

# 公众号写作助手 V9.0

## 版本历史

### V9.0.0 (2025-01-18) - 当前版本适配
**重大变更**：
- 不再使用skill.yaml，改为SKILL.md
- 删除prompts/文件夹，所有提示词统一到Markdown Body
- 新增Hot Reloading支持

**新增**：
- Sandbox安全机制
- 渐进式披露机制

### V8.1.0 (2025-12-15) - 数据驱动升级
**新增**：
- 三层架构选题过滤
- 自动配置同步机制

### V8.0.0 (2025-11-20) - 自然表达革命
**核心变更**：
- 从"表演角色"转向"自然表达"
- "自然比完美更重要"的理念

---

## 一、角色定义
[当前版本的角色定义...]
```

💡 **建议**：在SKILL.md开头用专门章节记录版本历史，便于追踪变更。

### 4.5 提示词优化技巧

**技巧1：使用代码块增强可读性**

```markdown
## 标题公式

### 工具推荐型
[品牌词] + [数字] + [推荐词]

示例：Claude Code 5个必装插件，让你的开发效率翻倍

### 教程型
[动作词] + [品牌词] + [场景]

示例：手把手教你用Cursor，从入门到精通
```

**技巧2：用好表格对比**

```markdown
| 版本 | 自然度 | AI腔 | 真诚度 |
|------|--------|------|--------|
| V7.0 | 60分 | 40分 | 50分 |
| V8.0 | 85分 | 15分 | 80分 |
```

**技巧3：分步骤展示**

```markdown
## 写作流程

**步骤1**：选题过滤
- 判断时效性
- 评估爆款潜力
- 决定是否值得写

**步骤2**：Research（如需要）
- 搜索最新信息
- 整理关键数据
- 验证事实准确性

**步骤3**：创作文章
- 应用老金风格
- 遵循爆款规律
- 控制AI腔<20分
```

---

## 第五部分：Python脚本集成

**本节目的**：学习如何将Python脚本集成到Skill中，扩展Claude Code的能力。

### 5.1 为什么需要脚本

**脚本能做什么Claude Code做不到的事？**

| 任务类型 | Claude Code原生 | 脚本增强 |
|----------|----------------|---------|
| 文本分析 | ❌ 只能模糊判断 | ✅ 精确的NLP分析 |
| 数据计算 | ⚠️ 可能出错 | ✅ 100%准确计算 |
| 文件批处理 | ⚠️ 效率低 | ✅ 高效批量处理 |
| API调用 | ⚠️ 格式不确定 | ✅ 标准化输出 |
| 复杂校验 | ❌ 难以保证一致 | ✅ 确定性校验 |

### 5.2 脚本模板

**标准Python脚本模板**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本名称 V版本号 - 简短描述

详细功能说明...

用法:
    python script.py <input> [options]

参数:
    input    必需，输入数据
    --json   可选，输出JSON格式

版本历史:
- V1.0.0 (2025-01-01): 初始版本
"""

import sys
import io
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


# ==================================================
# 数据类定义
# ==================================================

@dataclass
class ProcessResult:
    """处理结果数据类"""
    success: bool
    data: Dict[str, Any]
    message: str
    errors: list


# ==================================================
# 核心处理类
# ==================================================

class Processor:
    """处理器类"""

    def __init__(self, config: Optional[Dict] = None):
        """初始化处理器"""
        self.config = config or {}

    def process(self, input_data: str) -> ProcessResult:
        """
        处理输入数据

        Args:
            input_data: 输入数据

        Returns:
            ProcessResult: 处理结果
        """
        try:
            # 1. 验证输入
            if not input_data or not input_data.strip():
                return ProcessResult(
                    success=False,
                    data={},
                    message="输入数据为空",
                    errors=["输入不能为空"]
                )

            # 2. 核心处理逻辑
            result_data = self._core_process(input_data)

            # 3. 返回成功结果
            return ProcessResult(
                success=True,
                data=result_data,
                message="处理成功",
                errors=[]
            )

        except Exception as e:
            return ProcessResult(
                success=False,
                data={},
                message=f"处理失败: {str(e)}",
                errors=[str(e)]
            )

    def _core_process(self, data: str) -> Dict:
        """核心处理逻辑（子类可覆盖）"""
        # 在这里实现具体逻辑
        return {"processed": data}

    def generate_report(self, result: ProcessResult) -> str:
        """生成可读报告"""
        lines = [
            "=" * 60,
            "处理报告",
            "=" * 60,
            "",
            f"状态: {'成功' if result.success else '失败'}",
            f"消息: {result.message}",
            "",
        ]

        if result.data:
            lines.append("-" * 60)
            lines.append("处理结果:")
            for key, value in result.data.items():
                lines.append(f"  {key}: {value}")

        if result.errors:
            lines.append("")
            lines.append("错误信息:")
            for error in result.errors:
                lines.append(f"  - {error}")

        lines.extend(["", "=" * 60])
        return "\n".join(lines)


# ==================================================
# 命令行入口
# ==================================================

def main():
    """命令行入口函数"""
    # 设置UTF-8输出（Windows兼容）
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8'
    )

    # 参数验证
    if len(sys.argv) < 2:
        print("用法: python script.py <input> [--json]")
        print("")
        print("示例:")
        print("  python script.py '测试输入'")
        print("  python script.py '测试' --json")
        sys.exit(1)

    # 解析参数
    input_data = sys.argv[1]
    output_json = "--json" in sys.argv

    # 执行处理
    processor = Processor()
    result = processor.process(input_data)

    # 输出结果
    if output_json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(processor.generate_report(result))

    # 返回状态码
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
```

### 5.3 在Command中调用脚本

**调用方式**：

```markdown
# 在Command中调用脚本示例

### 步骤X：执行质量检测

**调用脚本**：
```bash
cd ".claude/skills/gongzhonghao-writer/scripts" && python quality_detector.py "文章内容" --json
```

**脚本参数说明**：
- 第一个参数：要检测的内容
- `--json`：输出JSON格式（便于解析）

**预期输出**：
````json
{
  "success": true,
  "data": {
    "ai_score": 15,
    "natural_score": 85,
    "passed": true
  },
  "message": "检测通过"
}
```
````

### 5.4 参数传递方式

| 方式 | 适用场景 | 示例 |
|------|---------|------|
| 命令行参数 | 简单参数 | `python script.py "topic"` |
| 标准输入 | 大量文本 | `echo "content" \| python script.py` |
| 文件传递 | 复杂数据 | `python script.py --input file.json` |
| 环境变量 | 配置信息 | `API_KEY=xxx python script.py` |

### 5.5 结果解析规范

**标准输出格式（JSON）**：

```json
{
  "success": true,
  "data": {
    "result_key": "result_value"
  },
  "message": "处理成功",
  "errors": []
}
```

**Claude Code解析模式**：

```markdown
当脚本执行完成后，解析输出：

1. **检查执行状态**
   - 返回码为0：执行成功
   - 返回码非0：执行失败，查看错误信息

2. **解析JSON输出**
   - 检查 `success` 字段
   - 提取 `data` 中的结果
   - 如有 `errors`，记录错误信息

3. **应用到后续步骤**
   - 使用解析结果继续工作流
```

---

## 第六部分：实战案例分析

**本部分的**：通过分析真实的企业级Skill，学习高级设计模式。

### 6.1 多步骤工作流设计

**案例：公众号写作流程（8步自动化）**

```
步骤0：选题过滤
    │
    │ worth_writing?
    │
    ├──→ No ──→ 结束，给出建议
    │
    ▼ Yes
步骤1：读取规范
    │
    ▼
步骤2：智能判断（是否需要Research）
    │
    │ need_research?
    │
    ├──────────┬──────────┤
    │          │          │
    ▼          ▼
步骤3      跳过
(Research)
    │          │
    └────┬─────┘
         │
         ▼
步骤4：创作文章
         │
    ┌────┴────┐
    │         │
    ▼         ▼
步骤5     步骤7
(标题)    (质量检测)
    │         │
    └────┬────┘
         │
         ▼
步骤6：保存 ←── 条件：质量检测通过
         │
         ▼
步骤8：发文前检查
```

**工作流定义原则**：

1. **单一职责**：每个步骤只做一件事
2. **明确输入输出**：步骤间数据传递清晰
3. **可断点恢复**：失败后可以从断点继续
4. **可观测**：每个步骤都有状态反馈

### 6.2 数据驱动架构

**公众号写作助手的数据驱动流程**：

```
数据收集 → 数据分析 → 自动同步 → 配置更新 → 脚本生效
    │          │          │          │          │
    │          │          │          │          ▼
    │          │          │          │      质检/标题
    │          │          │          │      脚本使用
    │          │          │          │      新配置
    │          │          │          │
    │          │          │          ▼
    │          │          │   formulas_config.json
    │          │          │   brands_config.json
    │          │          │   quality_config.json
    │          │          │
    │          │          ▼
    │          │   sync_config.py
    │          │   （自动同步脚本）
    │          │
    │          ▼
    │   rule_validation_report.json
    │   （分析报告）
    │
    ▼
wechat_articles.json
（原始数据）
```

**配置文件示例（formulas_config.json）**：

```json
{
  "version": "8.0",
  "last_updated": "2025-12-17",
  "formulas": {
    "tool_recommendation": {
      "name": "工具推荐型",
      "pattern": "[品牌词] + [数字] + [推荐词]",
      "effectiveness": 5.25,
      "example": "Claude Code 5个必装插件，让你的开发效率翻倍"
    },
    "tutorial": {
      "name": "教程词型",
      "pattern": "[动作词] + [品牌词] + [场景]",
      "effectiveness": 1.95,
      "example": "手把手教你用Cursor，从入门到精通"
    }
  }
}
```

### 6.3 企业级Skill目录结构

**公众号写作助手完整结构（V9.0 当前版本适配）**：

```
.claude/skills/gongzhonghao-writer/
├── SKILL.md                              (核心定义文件：YAML + Markdown)
├── scripts/
│   ├── core/
│   │   ├── quality_detector.py           (质量检测)
│   │   ├── title_generator.py            (标题生成)
│   │   ├── title_scorer.py               (标题评分)
│   │   ├── topic_filter.py               (选题过滤)
│   │   └── pre_publish_checker.py        (发布检查)
│   ├── collectors/
│   │   └── collect_time_range.py         (数据收集)
│   └── utils/
│       └── fix_feishu_format.py          (格式修复)
├── config/
│   ├── formulas_config.json              (公式配置)
│   ├── brands_config.json                (品牌配置)
│   ├── quality_config.json               (质检配置)
│   └── sync_config.py                    (同步脚本)
├── instructions/
│   └── workflow.md                       (详细指令)
└── DATA_DRIVEN_WORKFLOW.md               (数据驱动文档)
```

**SKILL.md结构示例**：

```markdown
---
name: gongzhonghao-writer
description: 当用户提到"公众号"、"写文章"、"老金风格"等关键词时，自动激活AI写作助手系统
---

# 公众号写作助手 V9.0

## 版本历史
[版本演进记录...]

## 一、角色定义
你是一位经验丰富的公众号写作专家...

## 二、核心能力
1. 爆款标题生成（5大公式）
2. 老金风格文章创作
3. 9维度质量检测
4. 选题自动过滤

## 三、工作流程
### 步骤1：选题过滤
[三层架构判断...]

### 步骤2：智能判断Research
[是否需要Research...]

### 步骤3：创作文章
[应用老金风格...]

### 步骤4：标题生成
[5大公式...]

### 步骤5：质量检测
[9维度检测...]

## 四、规则约束
[爆款规律、质量标准...]

## 五、工具调用
- 质量检测：`python scripts/core/quality_detector.py`
- 标题生成：`python scripts/core/title_generator.py`
- 选题过滤：`python scripts/core/topic_filter.py`

## 六、配置文件
- formulas_config.json：爆款公式配置
- brands_config.json：品牌词库
- quality_config.json：质检标准
```

**关键设计点（V9.0更新）**：

1. **单文件入口**：SKILL.md替代skill.yaml+prompts/，简化管理
2. **Hot Reloading**：修改SKILL.md后立即生效
3. **脚本分类**：core（核心）、collectors（收集）、utils（工具）
4. **配置驱动**：所有可变参数放在config/目录
5. **渐进式披露**：YAML Frontmatter常驻，Markdown Body按需加载

---

## 第七部分：故障排查

**本部分的**：快速解决Skill配置和运行中的常见问题。

### 7.1 常见错误及解决方案

#### 错误1：Skill未激活

**症状**：输入触发词没有反应

**可能原因**：
1. `SKILL.md` 文件格式错误
2. `description` 配置不当
3. 文件路径不正确

**解决方案**：

```bash
# 1. 检查SKILL.md格式
head -n 5 .claude/skills/你的skill/SKILL.md

# 应该显示：
# ---
# name: skill-name
# description: 触发描述
# ---

# 2. 验证YAML Frontmatter格式（在线工具）
# 访问 https://www.yamllint.com/ 粘贴YAML部分检查

# 3. 检查description是否清晰
# description应该明确说明何时激活，例如：
# ✅ "当用户要求'添加注释'或'代码注释'时激活"
# ❌ "代码注释工具"（太模糊）

# 4. 验证文件路径
ls -la .claude/skills/你的skill/
# 应该看到 SKILL.md 文件

# 5. 测试触发词
# 在Claude Code中输入description中的关键词
```

#### 错误2：提示词未生效

**症状**：AI回复不符合Skill风格

**可能原因**：
1. Markdown Body格式错误
2. 指令不够明确
3. Hot Reloading未生效

**解决方案**：

```bash
# 1. 检查SKILL.md完整格式
cat .claude/skills/你的skill/SKILL.md

# 应该包含：
# --- (YAML开始)
# name: xxx
# description: xxx
# --- (YAML结束)
#
# # 标题 (Markdown开始)
# ## 章节
# 内容...

# 2. 验证Markdown Body结构
# 确保使用了清晰的标题结构：
# ## 一、角色定义
# ## 二、工作流程
# ## 三、规则约束

# 3. 测试Hot Reloading
# 修改SKILL.md后，发送新消息测试
# 如果未生效，尝试开始新对话或使用 /compact 压缩上下文

# 4. 检查指令明确性
# 在SKILL.md中使用明确的指令：
# ✅ "你必须使用简洁的中文，避免AI腔"
# ❌ "建议使用自然语言"（太弱）
```

#### 错误3：脚本执行失败

**症状**：调用脚本时报错

**可能原因**：
1. Python路径问题
2. 脚本权限问题
3. 依赖包未安装

**解决方案**：

```bash
# 1. 检查Python是否可用
python --version
# 或
python3 --version

# 2. 检查脚本权限（macOS/Linux）
chmod +x .claude/skills/你的skill/scripts/*.py

# 3. 安装依赖
pip install -r .claude/skills/你的skill/requirements.txt

# 4. 手动测试脚本
cd .claude/skills/你的skill/scripts
python 脚本名.py "测试输入"
```

#### 错误4：YAML解析错误

**症状**：加载时报语法错误

**可能原因**：
1. YAML Frontmatter格式错误
2. `---`分隔符缺失或多余
3. 特殊字符未转义

**解决方案**：

```yaml
# ❌ 错误：缺少结束的---
---
name: my-skill
description: 测试

# ❌ 错误：冒号后没有空格
name:"我的Skill"

# ✅ 正确：完整的YAML Frontmatter
---
name: my-skill
description: 当用户需要时激活
---

# 这里开始是Markdown Body

# Skill标题
内容...
```

**验证YAML格式**：

```bash
# 方法1：使用在线工具
# 访问 https://www.yamllint.com/
# 复制YAML Frontmatter部分（不包括---分隔符）进行验证

# 方法2：使用Python验证
python3 -c "
import yaml
import sys

with open('.claude/skills/你的skill/SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取YAML部分
yaml_start = content.find('---')
yaml_end = content.find('---', yaml_start + 3)
yaml_content = content[yaml_start+3:yaml_end].strip()

try:
    yaml.safe_load(yaml_content)
    print('✅ YAML格式正确')
except yaml.YAMLError as e:
    print(f'❌ YAML错误: {e}')
    sys.exit(1)
"
```

### 7.2 调试技巧

**技巧1：验证SKILL.md结构**

```bash
# 检查SKILL.md基本结构
cat .claude/skills/你的skill/SKILL.md | head -n 20

# 应该看到：
# ---
# name: xxx
# description: xxx
# ---
# (空行)
# # Markdown标题
# 内容...
```

**技巧2：测试Hot Reloading**

```bash
# 1. 修改SKILL.md
# 添加或修改一些指令

# 2. 在Claude Code中发送新消息
# 不需要重启，修改会自动生效

# 3. 验证修改是否生效
# 检查AI是否应用了新的指令

# 如果未生效，尝试开始新对话或：
/compact
```

**技巧3：手动测试脚本**

```bash
# 直接运行脚本看输出
cd .claude/skills/你的skill/scripts
python 脚本名.py "测试输入" --json

# 检查返回码
echo $?  # 0表示成功，非0表示失败
```

**技巧4：检查文件编码**

```bash
# 确保文件是UTF-8编码
file .claude/skills/你的skill/SKILL.md
# 应显示：UTF-8 Unicode text
```

**技巧5：查看Skill加载日志**

在Claude Code中输入：
```
请列出当前已加载的所有Skills
```

这会显示所有被识别的Skills及其基本信息。

---

### 7.3 v2.1.129+ 新增：`skillOverrides` 设置

当你的项目或团队安装了大量 Skills 时，有些可能暂时不想用。从 **v2.1.129** 起，Claude Code 支持 `skillOverrides` 设置来控制每个 Skill 的可见性。

#### 三种覆盖状态

| 值 | 效果 |
|---|---|
| `off` | 完全隐藏该 Skill（等同于不存在） |
| `user-invocable-only` | 只保留 `/` 手动调用，禁止 Claude 自动激活 |
| `name-only` | 只在 `/skills` 列表中显示名称，不加载任何指令 |

#### 配置位置

`skillOverrides` 写在 settings 文件中（项目级 `.claude/settings.json` 或用户级 `~/.claude/settings.json`）：

```json
{
  "skillOverrides": {
    "gongzhonghao-writer": "user-invocable-only",
    "legacy-helper": "off",
    "experimental-tool": "name-only"
  }
}
```

**适用场景**：
- 团队有几十个 Skills，但某个项目只想用其中几个 → 把其余设为 `off`
- 某个 Skill 自动激活太频繁，但不舍得删 → 改为 `user-invocable-only`
- 排查 Skill 冲突时，临时关闭部分 Skill

### 7.4 `/skills` 搜索过滤

当你安装了大量 Skills 时，直接输入 `/skills` 列表会很长。在较新版本中，`/skills` 支持搜索过滤：

```text
/skills <关键词>
```

例如 `/skills comment` 会过滤出名称或描述中包含 "comment" 的 Skill。这在管理十几个以上 Skill 时非常有用。

---

## 第八部分：FAQ（20个常见问题）

### Q1：Skill和Command有什么区别？
**A**：Command是"按钮"（触发器），Skill是"APP"（能力包）。Command用于显式触发，Skill用于封装知识和工具。两者通常配合使用：Command作为入口，Skill提供能力。

### Q2：必须要SKILL.md吗？
**A**：是的，`SKILL.md` 是Skill的唯一必需文件。没有它Claude Code无法识别这是一个Skill。

### Q3：SKILL.md可以是任意大小吗？
**A**：理论上可以，但建议控制在1000行以内。太大的SKILL.md会影响加载速度和AI理解。如果内容很多，考虑使用scripts/、config/等资源文件夹。

### Q4：scripts支持哪些语言？
**A**：主要支持Python和Bash。推荐Python，因为生态好、跨平台、易维护。JavaScript也可以，但不如Python常用。

### Q5：如何让Skill自动激活？
**A**：在SKILL.md的YAML Frontmatter中配置`description`字段。Claude Code会根据description判断何时激活。例如：
```yaml
---
description: 当用户要求"添加注释"或"代码注释"时激活
---
```

### Q6：可以有多个Skill吗？
**A**：可以。每个Skill是 `.claude/skills/` 下的独立目录，可以有任意多个。

### Q7：Skill之间会冲突吗？
**A**：如果description中描述的触发场景重复可能会冲突。建议每个Skill使用独特的触发场景描述。

### Q8：如何更新Skill版本？
**A**：在SKILL.md的Markdown Body开头添加"版本历史"章节，记录每次变更。例如：
```markdown
## 版本历史

### V2.0.0 (2025-01-18)
- 适配当前版本新特性
- 改为SKILL.md单文件结构

### V1.0.0 (2025-01-01)
- 初始版本
```

### Q9：SKILL.md多大合适？
**A**：建议单个SKILL.md不超过1000行。太长会影响加载速度和AI理解。大的Skill应该考虑拆分成多个子Skill或使用scripts/。

### Q10：如何调试Skill？
**A**：
1. 验证YAML Frontmatter格式
2. 手动运行scripts/中的脚本测试
3. 检查description是否清晰
4. 查看Claude Code的Skill加载日志

### Q11：Hot Reloading不生效怎么办？
**A**：
1. 确认修改的是SKILL.md而不是其他文件
2. 检查YAML Frontmatter格式是否正确
3. 尝试使用`/compact`压缩上下文后重试
4. 最后手段：重启Claude Code

### Q12：如何处理中文路径问题？
**A**：Windows上尽量避免中文路径。如果必须使用，确保SKILL.md文件编码为UTF-8（带BOM或不带BOM都可以，但要一致）。

### Q13：Skill可以调用MCP吗？
**A**：可以。在SKILL.md的Markdown Body中可以引用MCP工具。Claude Code会自动识别并调用。

### Q14：如何共享Skill给团队？
**A**：将整个 `.claude/skills/你的skill/` 目录提交到Git仓库。团队成员克隆后即可使用。

### Q15：Skill可以跨项目使用吗？
**A**：可以。将Skill放在全局配置目录（~/.claude/skills/）即可在所有项目中使用。

### Q16：如何回退到旧版本Skill？
**A**：使用Git回退到旧版本的提交，或者在SKILL.md的版本历史中查看旧版本的内容。

### Q17：SKILL.md中可以使用变量吗？
**A**：SKILL.md 支持一个特殊内置变量 `${CLAUDE_SKILL_DIR}`，其他自定义模板变量不支持。

**`${CLAUDE_SKILL_DIR}` 变量说明**：

- **含义**：指向当前 Skill 文件（SKILL.md）所在的目录路径
- **用途**：在 SKILL.md 正文中引用同目录下的其他文件（模板、配置、示例等）
- **示例**：

```markdown
请阅读 ${CLAUDE_SKILL_DIR}/templates/code-review.md 中的代码审查模板
请参考 ${CLAUDE_SKILL_DIR}/config/rules.yaml 中的规则配置
```

- **优势**：使 Skill 可以组织为包含多个文件的目录结构，而不是将所有内容塞进一个 SKILL.md
- 如果需要更复杂的动态内容，使用 scripts/ 中的脚本生成

### Q18：如何测试Skill是否正常工作？
**A**：
1. 检查SKILL.md文件结构是否完整（YAML + Markdown）
2. 验证YAML Frontmatter格式
3. 手动测试scripts/中的脚本
4. 在Claude Code中测试触发词

### Q19：Skill加载很慢怎么办？
**A**：
1. 减少SKILL.md的行数
2. 优化scripts/中的脚本性能
3. 检查是否有不必要的config/文件

### Q20：如何学习更高级的Skill开发？
**A**：
1. 阅读公众号写作助手项目中的 SKILL.md 正文
2. 参考官方Skill示例
3. 实践中不断迭代优化
4. 理解渐进式披露和Hot Reloading机制

---

## 第九部分：附录

### 附录A：Skill目录快速创建脚本

**macOS/Linux一键创建脚本**：

```bash
#!/bin/bash
# create-skill.sh - Skill目录结构一键创建
# 用法: ./create-skill.sh <skill-name>

SKILL_NAME=$1

if [ -z "$SKILL_NAME" ]; then
    echo "用法: $0 <skill-name>"
    exit 1
fi

SKILL_DIR=".claude/skills/${SKILL_NAME}"

echo "创建Skill目录: ${SKILL_NAME}"

# 创建目录结构
mkdir -p "${SKILL_DIR}/scripts"
mkdir -p "${SKILL_DIR}/templates"
mkdir -p "${SKILL_DIR}/config"

# 创建SKILL.md
cat > "${SKILL_DIR}/SKILL.md" << EOF
---
name: ${SKILL_NAME}
description: 请填写Skill的触发场景描述
---

# ${SKILL_NAME}

## 版本历史

### V1.0.0 ($(date +%Y-%m-%d))
- 初始版本

---

## 一、角色定义
[定义AI扮演的角色和背景]

## 二、核心能力
[列出3-5个核心能力]

## 三、工作流程
### 步骤1：[步骤名称]
[详细说明和操作指南]

### 步骤2：[步骤名称]
[详细说明和操作指南]

## 四、规则约束
[定义必须遵守的规则]

## 五、示例展示
[提供具体的好/坏示例]

## 六、输出格式
[定义输出的结构和格式]
EOF

# 创建README
cat > "${SKILL_DIR}/README.md" << EOF
# ${SKILL_NAME}

**版本**: 1.0.0
**创建时间**: $(date +%Y-%m-%d)

## 功能说明
请填写功能说明

## 使用方法
请填写使用方法

## 目录结构
- SKILL.md: 核心定义文件
- scripts/: 可执行脚本
- templates/: 输出模板
- config/: 配置文件
EOF

echo "✅ Skill创建完成: ${SKILL_DIR}"
echo ""
echo "下一步:"
echo "1. 编辑 ${SKILL_DIR}/SKILL.md"
echo "2. 填写description字段"
echo "3. 编写Markdown Body内容"
```

### 附录B：SKILL.md完整模板

```markdown
---
name: skill-name
description: 当用户提到[关键词1]、[关键词2]或[关键词3]时，自动激活本Skill提供[核心能力]
---

# Skill名称

## 版本历史

### V1.0.0 (YYYY-MM-DD)
**变更内容**：
- 初始版本
- 实现核心功能

---

## 一、角色定义
你是一位[专业领域]专家，擅长[核心能力]。

## 二、核心能力
1. **能力1**：[描述]
2. **能力2**：[描述]
3. **能力3**：[描述]

## 三、工作流程

### 步骤1：[步骤名称]
**输入**：[输入要求]
**处理**：[处理逻辑]
**输出**：[输出格式]

### 步骤2：[步骤名称]
[详细说明...]

## 四、规则约束

### 必须遵守
1. [规则1]
2. [规则2]

### 禁止事项
1. [禁止1]
2. [禁止2]

## 五、示例展示

### ✅ 好的示例
[展示正确用法...]

### ❌ 差的示例
[展示错误用法...]

## 六、输出格式
[定义输出结构...]

## 七、工具调用（如有）
- 工具1：`调用命令`
- 工具2：`调用命令`

## 八、配置文件（如有）
- config1.json：[用途]
- config2.json：[用途]
```

### 附录C：YAML Frontmatter快速参考

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `name` | string | ✅ | Skill名称（小写、连字符） | `code-commenter` |
| `description` | string | ✅ | 触发场景描述 | `当用户要求"添加注释"时激活` |

**最佳实践**：
- name使用kebab-case（小写+连字符）
- description应该明确说明触发条件
- description中包含关键词会提高自动激活准确率

### 附录D：常用脚本示例

**示例1：简单文本处理**

```python
#!/usr/bin/env python3
"""简单文本处理脚本"""
import sys

def process(text):
    # 处理逻辑
    return text.upper()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python script.py <text>")
        sys.exit(1)

    result = process(sys.argv[1])
    print(result)
```

**示例2：JSON输出**

```python
#!/usr/bin/env python3
"""带JSON输出的脚本"""
import sys
import json

def analyze(text):
    return {
        "length": len(text),
        "words": len(text.split()),
        "success": True
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "缺少参数"}))
        sys.exit(1)

    result = analyze(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

**恭喜完成Skills定制教程！**

现在你已经掌握了创建和管理Claude Code Skills的核心技能。

**下一步建议**：
1. 为你的工作领域创建一个实用的Skill
2. 参考公众号写作助手的SKILL.md架构设计更复杂的Skill
3. 与团队分享你的Skill，收集反馈持续优化
4. 深入理解Hot Reloading和渐进式披露机制
5. 如果团队已经积累了大量 Skills，可以进一步研究 [SkillClaw](https://github.com/AMAP-ML/SkillClaw)：它关注跨用户、长期使用轨迹驱动的 skill 去重、合并、提质和共享，论文见 [arXiv:2604.08377](https://arxiv.org/abs/2604.08377)
