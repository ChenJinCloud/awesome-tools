# 变更日志

[English](CHANGELOG.md) | [简体中文](CHANGELOG.zh-CN.md)

## 2026-08-07

- 添加 `LICENSE`（MIT）。仓库此前已公开但未声明许可证，因此复用和 Fork 缺少清晰的法律基础。
- 添加本 `CHANGELOG.md`，让外部用户可以看到公开软件包自身的版本历史，并与维护者私有 Life OS 中的 closeout 日志分开。
- 在 `README.md` 中说明项目采用 MIT 许可证。
- 添加 pytest 测试套件（`tests/test_extract_session_events.py`）覆盖 `extract_session_events.py`：文本截断与空白折叠、消息内容提取、系统/开发者/环境上下文过滤、函数调用和通用 `*_call` 事件捕获、畸形或空白行处理、Markdown 渲染，以及 CLI 文件输出和文件缺失错误路径。
- 添加 GitHub Actions 工作流（`.github/workflows/tests.yml`），在每次 Push 和 Pull Request 时运行测试套件。

## 2026-06-30

- 首次公开发布。从维护者本地的 `codex-closeout-archive` Skill 中提取，移除了特定机器的 Life OS 路由，并把目标位置解析泛化为仓库/工作区根目录或最近的 `AGENTS.md` 等效政策。
