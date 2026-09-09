# 打开方法论 Markdown 文档

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

当用户希望查看最新方法论文档，而不是在聊天中打印其内容时，使用此 Skill。

## 配置路径

为你自己的机器设置：

```text
KNOWLEDGE_BASE_ROOT=<你的知识库文件夹>
METHODOLOGY_SUBDIR=<可选的方法论文件夹>
MARKDOWN_READER_EXE=<你的 Markdown 阅读器可执行文件>
```

如果使用公开的阅读器项目，在这里记录其仓库。例如：

```text
MARKDOWN_READER_REPO=https://github.com/ChenJinCloud/md-reader
```

## 工作流

1. 如果已经配置方法论子文件夹，先搜索该文件夹。
2. 否则在知识库中搜索路径或文件名包含 `methodology` 或当地语言等效词的 Markdown 文件。
3. 选择最近修改的匹配项。
4. 使用配置好的 Markdown 阅读器打开。
5. 除非用户要求提取或审查文本，否则不要把文档粘贴到聊天中。

## PowerShell 模式

```powershell
$kb = "<KNOWLEDGE_BASE_ROOT>"
$reader = "<MARKDOWN_READER_EXE>"
$latest = Get-ChildItem $kb -Recurse -Filter *.md -File |
  Where-Object { $_.FullName -match "methodology|方法论" } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
if ($latest) { & $reader $latest.FullName } else { Write-Error "No methodology Markdown file found." }
```

## 约束

- 优先打开文件，而不是将内容复制到聊天中。
- 当用户明确要求“最新”时，避免追问是哪一个文件。
- 使用配置好的本地路径，不要硬编码个人路径。
