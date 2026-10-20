# 课程练习材料

这里的项目、人物、订单和产品规则都是为本课程编写的虚构样例。可以直接拿来跟练，再换成你有权使用的工作材料。

| 今天练什么 | 材料 | 对应课程 |
|---|---|---|
| 修复空列表的进度计算 | [进度计算练习](progress-lab/README.md) | [Claude Code 02](../docs/claude-code/02-基础使用完整指南.md#先修一个小-bug空任务列表为什么显示-nan)、[Codex CX-02](../docs/codex/CX-02-Codex-App桌面工作流完整指南.md#先用-app-修一个小-bug) |
| 把零散记录写成周报 | [工作记录](office-lab/work-notes.md) | [WorkBuddy WB-01](../docs/workbuddy/WB-01-WorkBuddy项目介绍完整指南.md#13-把任务交给它) |
| 去重、处理缺失值、汇总净收入 | [订单样例 CSV](office-lab/orders.csv) | [WorkBuddy WB-03](../docs/workbuddy/WB-03-WorkBuddy专家与专家团完整指南.md#13-第一次实战让数据分析师帮你看表格) |
| 从新旧资料中找有依据的答案 | [旧版说明](office-lab/guide-v1.md)、[生效说明](office-lab/guide-v2.md)、[讨论草稿](office-lab/guide-draft.md) | [WorkBuddy WB-06](../docs/workbuddy/WB-06-WorkBuddy知识库完整指南.md#第二步同一个问题查三份资料) |
| 完成带评估的 AI Coding 实操 | [10 个练习与 5 条 Agent 评估流程](ai-coding-lab/README.md) | [一页速查卡](../docs/ai-coding/速查卡.md) |

先保留原始材料，在自己新建的练习目录中操作。办公练习只需要保存或粘贴文本；进度计算练习需要本机能运行 `node --version`。Codex App 的 Review 跟练还需要 Git 和本地初始提交，CX-02 已给出步骤。不需要真实客户数据、付费连接器或部署服务。

`progress-lab` 故意保留了一个 Bug，第一次测试失败是练习起点。照课程修好后再运行测试，才能看到前后的变化。

所有样例采用仓库的 [MIT License](../LICENSE)。
