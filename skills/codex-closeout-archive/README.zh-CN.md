# Codex Closeout Archive

[English](README.md) | [简体中文](README.zh-CN.md)

`codex-closeout-archive` 是一个 Codex Skill，用于在归档任务前，为即将结束的对话生成精简、可追溯的过程资产。

它适用于重要上下文存在于对话本身的工作流，包括意图变化、用户纠正、证据路径、文件输出、决定和最终状态。

## 它能做什么

- 为每次明确的 closeout 请求创建一份精简的 Markdown 过程资产。
- 捕获关键时间线、决定、输出文件、证据路径和未完成事项。
- 避免复制完整原始对话、凭证、私有消息或敏感导出。
- 在本地工作区政策要求时，更新附近的项目索引或变更日志。
- 在过程资产写入并验证后归档当前 Codex 对话。

## 安装

将此仓库文件夹复制到 Codex Skills 目录：

```text
~/.codex/skills/codex-closeout-archive
```

然后新建 Codex 任务，或刷新 Skill 发现。

## 使用

明确要求 Codex 使用此 Skill：

```text
使用 $codex-closeout-archive，以一份精简的过程资产结束并归档这段对话。
```

也可以使用自然语言：

```text
结束这个任务，并保存关键决定和证据路径。
```

## 文件

```text
SKILL.md
agents/openai.yaml
scripts/extract_session_events.py
tests/test_extract_session_events.py
```

## 辅助脚本

辅助脚本从 Codex 会话 JSONL 文件中提取精简的事件清单：

```bash
python scripts/extract_session_events.py --latest
python scripts/extract_session_events.py --session "/path/to/rollout.jsonl"
```

辅助输出只是起点。最终过程资产应由 Agent 筛选，以保留有用的演变过程，同时避免暴露私有对话内容。

## 隐私边界

此 Skill 用于保留可追溯性，而不是公开原始对话数据。生成的过程资产应避免包含：

- 凭证、Token 和密钥；
- 完整私有聊天记录；
- 完整 Slack、邮件或私信内容；
- 敏感的第三方个人数据；
- 不必要的原始 JSONL 对话片段。

## 开发

辅助脚本包含 pytest 测试套件，覆盖事件解析、消息过滤和 CLI：

```bash
pip install -r requirements-dev.txt
pytest
```

CI 会在每次 Push 和 Pull Request 时运行测试套件（`.github/workflows/tests.yml`）。

## 变更日志

参见 [CHANGELOG.zh-CN.md](CHANGELOG.zh-CN.md)。

## 许可证

MIT。参见 [LICENSE](LICENSE)。
