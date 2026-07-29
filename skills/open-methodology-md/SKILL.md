---
name: open-methodology-md
description: Use to find the latest methodology Markdown document in a local knowledge base and open it with a configured Markdown reader.
---

# Open Methodology Markdown

Use this skill when the user asks to view the latest methodology document rather than print its contents in chat.

## Configure Paths

Set these for your own machine:

```text
KNOWLEDGE_BASE_ROOT=<your knowledge base folder>
METHODOLOGY_SUBDIR=<optional methodology folder>
MARKDOWN_READER_EXE=<your Markdown reader executable>
```

If you use a public reader project, record its repository here. Example:

```text
MARKDOWN_READER_REPO=https://github.com/ChenJinCloud/md-reader
```

## Workflow

1. Search the methodology subfolder first, if configured.
2. Otherwise search the knowledge base for Markdown files whose path or filename contains `methodology` or the local-language equivalent.
3. Pick the most recently modified match.
4. Open it with the configured Markdown reader.
5. Do not paste the document into chat unless the user asks for text extraction or review.

## PowerShell Pattern

```powershell
$kb = "<KNOWLEDGE_BASE_ROOT>"
$reader = "<MARKDOWN_READER_EXE>"
$latest = Get-ChildItem $kb -Recurse -Filter *.md -File |
  Where-Object { $_.FullName -match "methodology|方法论" } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
if ($latest) { & $reader $latest.FullName } else { Write-Error "No methodology Markdown file found." }
```

## Guardrails

- Prefer opening the file to copying content into chat.
- Avoid asking which file when "latest" is clearly requested.
- Use configured local paths, not hardcoded personal paths.
