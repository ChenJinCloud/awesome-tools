# Awesome Tools

[English](README.md) | [简体中文](README.zh-CN.md)

这是我的公开工具目录，收录经过筛选的高质量工具、工作流和可复用的 Agent Skills。

这个仓库的目标不是收集所有看起来有趣的链接。每个条目都应该说明工具或方案为什么有用、适合放在什么位置、需要注意哪些边界或风险，以及我是否实际使用或验证过它。

## 原则

- 优先收录经过实际检验的工作流，而不是泛泛推荐。
- 区分适合公开复用的内容、私有实现和个人记录。
- 不在此仓库中保存私有数据、凭证、账号标识、原始导出、日志或本机绝对路径。
- 提供足够的上下文，让未来的 Agent 或执行者能够安全理解相关用例。
- 明确标记脆弱、合规敏感或依赖特定版本的内容。

## 目录结构

```text
.github/
  workflows/
catalog/
  macos-wechat-export-capability.md
  personal-system-skills.md
docs/
  repository-consolidation/
  superpowers/
    plans/
    specs/
skills/
  agent-os-global/
  agent-os-operation/
  calm-mint-pencil-cover/
  codex-closeout-archive/
  creator-pricing/
  daily-log/
  open-methodology-md/
  universal-methodology/
```

## 当前条目

| 条目 | 类型 | 状态 |
| --- | --- | --- |
| [个人系统 Skills](catalog/personal-system-skills.md) | Agent Skill 合集 | 已加入经过脱敏、适合公开的 Skill 集合 |
| [私有微信归档能力与导出后用例](catalog/macos-wechat-export-capability.md) | 私有本地能力 | 只公开能力和实际导出后用例；实现保持私有 |

## Skills

`skills/` 是这些 Skill 包的公开权威源。除非某个 Skill 具有无法在本仓库中支持的独立发布生命周期，否则不应再维护第二个独立仓库。

- [agent-os-global](skills/agent-os-global/SKILL.md)：把本地 Agent OS 治理规则应用到非简单任务。
- [agent-os-operation](skills/agent-os-operation/SKILL.md)：运行或审查 Agent OS 治理项目。
- [calm-mint-pencil-cover](skills/calm-mint-pencil-cover/SKILL.md)：生成稳定的薄荷绿色铅笔风文章封面。
- [codex-closeout-archive](skills/codex-closeout-archive/SKILL.md)：把 Agent 对话保存成精简、可追溯的过程资产。
- [creator-pricing](skills/creator-pricing/SKILL.md)：评估创作者赞助报价和谈判方案。
- [daily-log](skills/daily-log/SKILL.md)：创建或更新每日日志及基础维护记录。
- [open-methodology-md](skills/open-methodology-md/SKILL.md)：在本地阅读器中打开最新的方法论 Markdown 文档。
- [universal-methodology](skills/universal-methodology/SKILL.md)：在执行前厘清模糊、高风险或具有复用价值的事项。

## 条目模板

新增工具、工作流或能力说明时使用以下结构：

```markdown
# 名称

## 它是什么
## 为什么有用
## 最适合的使用场景
## 来源与项目链接
## 边界与风险
## 我的使用状态
## 使用前需要重新检查的事项
```

## 公开边界

本仓库只保存适合公开复用的内容。私有实现、个人源数据、凭证、本机路径、原始导出和私有验证证据应保留在各自的私有系统中。
