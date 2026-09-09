# Agent OS 项目操作

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

在 Agent OS 治理项目内部工作时使用此 Skill。它比 `agent-os-global` 范围更窄：只有当 Agent OS 项目本身是操作目标时才使用。

## 必需的本地文件

请替换为你的项目实际使用的名称：

- 项目 `README.md`
- `source-of-truth-map.md`
- `permission-matrix.md`
- `agent-behavior-contract.md`
- `CHANGELOG.md`
- `run-ledger.md`
- 验证脚本（如果存在）

## 流程

1. 阅读项目入口和事实源映射。
2. 写入前阅读权限政策。
3. 将任务分类为绿色、黄色或红色。
4. 进行最小但有用的修改。
5. 黄色工作需要更新项目变更日志和运行台账。
6. 运行项目验证脚本，或模拟其验证过程。
7. 报告修改文件、验证结果和剩余风险。

## 停止条件

除非用户明确批准了具体动作，否则必须在删除、安装工具、启用 Hook、启用 MCP、对外发送、修改凭证、修改权限或扩大写入范围前停止。
