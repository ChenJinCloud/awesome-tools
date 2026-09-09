# Awesome Tools

[English](README.md) | [简体中文](README.zh-CN.md)

这是我的公开工具目录，收录经过筛选的高质量工具、工作流和可复用的 Agent Skills。

这个仓库的目标不是收集所有看起来有趣的链接。每个条目都应该说明工具或方案为什么有用、适合放在什么位置、需要注意哪些边界或风险，以及我是否实际使用或验证过它。

## 原则

- 优先收录经过实际检验的工作流，而不是泛泛推荐。
- 区分开源源码、仅用于发布的辅助工具、本地封装和个人记录。
- 不在此仓库中保存私有数据、凭证、账号 ID、原始导出、日志或本机绝对路径。
- 提供足够的上下文，让未来的 Agent 或执行者能够安全地复现工作流。
- 明确标记脆弱、合规敏感或依赖特定版本的工具。

## 目录结构

```text
catalog/
  chatlog-with-sns.md
  macos-wechat-export-capability.md
  personal-system-skills.md
  wechat-chat-export.md
  wechat-chat-export-validation.md
docs/
  public-review-checklist.md
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
  wechat-chat-export/
scripts/
  check-public-safety.ps1
  check_public_safety.py
  export_chatlog.py
  probe_chatlog.py
  test_public_safety.py
  verify_closed_snapshot.py
```

## 当前条目

| 条目 | 类型 | 状态 |
| --- | --- | --- |
| [`chatlog_with_sns`](catalog/chatlog-with-sns.md) | 上游本地微信工具 | 已研究；使用前仍需重新检查兼容性和长期维护情况 |
| [个人系统 Skills](catalog/personal-system-skills.md) | Agent Skill 合集 | 已加入经过脱敏、适合公开的 Skill 集合 |
| [微信聊天记录导出](catalog/wechat-chat-export.md) | 本地数据导出工作流 | 已加入适合公开的说明和 Codex Skill |
| [微信导出验证状态](catalog/wechat-chat-export-validation.md) | 验证说明 | 只记录当前公开仓库状态；不公开原始验证数据 |
| [macOS 微信聊天记录导出能力](catalog/macos-wechat-export-capability.md) | 私有本地导出能力 | 已验证结果；实现保持私有 |

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
- [wechat-chat-export](skills/wechat-chat-export/SKILL.md)：围绕 `chatlog_with_sns` 或兼容的本地 API，构建或运行具有明确授权边界的微信聊天记录导出工作流。

## 微信导出脚本流程

这些脚本用于私有的本地执行。不要把生成的输出放入这个公开仓库。

1. 探测本地服务：

```bash
python scripts/probe_chatlog.py --base-url http://127.0.0.1:5030
```

2. 如果从复制的数据目录导出，先验证关闭状态下的快照：

```bash
python scripts/verify_closed_snapshot.py \
  --source <private-source-root> \
  --snapshot <private-snapshot-root> \
  --robocopy-log <private-copy-log> \
  --out <private-status-json>
```

3. 导出并生成清单和摘要：

```bash
python scripts/export_chatlog.py \
  --base-url http://127.0.0.1:5030 \
  --out-dir <private-output-dir> \
  --require-verified-snapshot <private-status-json>
```

导出封装会生成原始会话文件、元数据、私有索引、`manifest.csv` 和 `summary.json`。所有生成的输出都应当视为私有数据。

## Issue 状态

| Issue | 状态 |
| --- | --- |
| #1 导出封装 | 已通过 `scripts/export_chatlog.py` 实现；模拟 API 测试通过。 |
| #2 就绪检查 | 已通过 `scripts/probe_chatlog.py` 实现；非 loopback 地址会被阻止。 |
| #3 端到端验证 | 仍需使用经过授权的私有本地数据运行；公开状态说明已加入仓库。 |
| #4 隐私控制 | 已通过 `scripts/check_public_safety.py`、测试覆盖、`.gitignore` 和人工检查清单加强。 |
| #5 关闭状态快照 | 已通过 `scripts/verify_closed_snapshot.py` 和 `--require-verified-snapshot` 导出门禁实现。 |

## 条目模板

新增工具或方案时使用以下结构：

```markdown
# 名称

## 它是什么
## 为什么质量较高
## 最适合的使用场景
## 来源与项目链接
## 配置说明
## 边界与风险
## 我的使用状态
## 使用前需要重新检查的事项
```

## 公开安全检查

发布变更前运行：

```powershell
.\scripts\check-public-safety.ps1
```

或者：

```bash
python scripts/check_public_safety.py --root .
python scripts/test_public_safety.py
```

扫描规则有意设置得较为保守，但不能替代人工审查。
