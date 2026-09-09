# 公开 Skill 仓库整合记录

[English](2026-08-17-public-skill-consolidation.md) | [简体中文](2026-08-17-public-skill-consolidation.zh-CN.md)

日期：2026-08-17

## 决定

`awesome-tools/skills/` 是可复用个人 Codex Skills 的公开权威源。下列独立仓库被整合到这里，以消除重复来源，同时保留完整、可分发的软件包。

## 来源映射

| 原仓库 | 已审查提交 | 权威目标位置 | 保留内容 |
| --- | --- | --- | --- |
| `ChenJinCloud/codex-closeout-archive` | `9b5bb6077cef2120ec1e2fa30b01eb070a3e4864` | `skills/codex-closeout-archive/` | Skill 指令、Agent 元数据、辅助脚本、测试、README、变更日志、依赖和 MIT 许可证 |
| `ChenJinCloud/universal-methodology-skill` | `868c74cb6e00b02b01109b378c5a4d14dc759abd` | `skills/universal-methodology/` | Skill 指令、Agent 元数据、完整推进参考卡和 MIT 许可证 |

## 版本处理

独立仓库比 `awesome-tools` 中较早的副本更完整，而本机已安装的软件包包含更新的指令。因此，整合后的软件包保留独立仓库的支持文件，同时采用当前已安装的 Skill 指令。Universal Methodology 记录为 v1.2。

`codex-closeout-archive` 保留 pytest 测试套件。根目录工作流 `.github/workflows/skill-tests.yml` 从新的 monorepo 路径运行这套测试。

## 安全与删除门禁

只有满足以下全部条件，才能删除原仓库：

- 目标文件已经提交并推送；
- closeout 测试套件和公开安全检查通过；
- 远端 `awesome-tools` 分支与已验证的本地提交一致；
- 没有引入凭证、私有记录、个人绝对路径或生成输出。

删除状态：已于 2026-08-17 完成。经验证的 `awesome-tools` 提交 `ee33b1fa5562cd1941ea29569c5663e7afb76157` 到达 `main` 后，两个独立仓库均被永久删除；后续 API 检查两个原仓库路径均返回 `404 Not Found`。
