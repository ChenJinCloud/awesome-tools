# Awesome Tools

This repository is my public catalog of high-quality tools, workflows, and reusable agent skills.

The goal is not to collect every interesting link. Each entry should explain why the tool or solution is useful, where it fits, what boundary or risk matters, and whether I have actually used or verified it.

## Principles

- Prefer field-tested workflows over generic recommendations.
- Separate open-source source code, release-only helpers, local wrappers, and personal records.
- Keep private data, credentials, account IDs, raw exports, logs, and local machine paths out of this repository.
- Add enough context for a future agent or operator to reproduce the workflow safely.
- Mark fragile, compliance-sensitive, or version-sensitive tools explicitly.

## Structure

```text
catalog/
  wechat-chat-export.md
skills/
  wechat-chat-export/
    SKILL.md
    agents/openai.yaml
scripts/
  check-public-safety.ps1
```

## Current Entries

| Entry | Type | Status |
| --- | --- | --- |
| [WeChat Chat Export](catalog/wechat-chat-export.md) | Local data export workflow | Public-safe summary and Codex skill added |

## Skills

- [wechat-chat-export](skills/wechat-chat-export/SKILL.md): a Codex skill for building or running a local, authorization-bounded WeChat chat-record export workflow around `chatlog_with_sns` / compatible local APIs.

## Entry Template

Use this shape when adding a new tool or solution:

```markdown
# Name

## What It Is
## Why It Is High Quality
## Best Use Cases
## Source / Project Links
## Setup Notes
## Boundaries And Risks
## My Usage Status
## Recheck Before Use
```

## Public Safety

Before publishing changes, run:

```powershell
.\scripts\check-public-safety.ps1
```

The scan is intentionally conservative. It is not a substitute for human review.
