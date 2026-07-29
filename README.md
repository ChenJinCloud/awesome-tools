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
  wechat-chat-export-validation.md
docs/
  public-review-checklist.md
skills/
  wechat-chat-export/
    SKILL.md
    agents/openai.yaml
scripts/
  check-public-safety.ps1
  check_public_safety.py
  export_chatlog.py
  probe_chatlog.py
  test_public_safety.py
  verify_closed_snapshot.py
```

## Current Entries

| Entry | Type | Status |
| --- | --- | --- |
| [WeChat Chat Export](catalog/wechat-chat-export.md) | Local data export workflow | Public-safe summary and Codex skill added |
| [WeChat Export Validation Status](catalog/wechat-chat-export-validation.md) | Validation note | Current public repo status only; no public raw validation data |

## Skills

- [wechat-chat-export](skills/wechat-chat-export/SKILL.md): a Codex skill for building or running a local, authorization-bounded WeChat chat-record export workflow around `chatlog_with_sns` / compatible local APIs.

## WeChat Export Script Flow

The scripts are designed for private local execution. Do not place generated outputs inside this public repository.

1. Probe a local service:

```bash
python scripts/probe_chatlog.py --base-url http://127.0.0.1:5030
```

2. If exporting from a copied data tree, verify the closed-state snapshot first:

```bash
python scripts/verify_closed_snapshot.py \
  --source <private-source-root> \
  --snapshot <private-snapshot-root> \
  --robocopy-log <private-copy-log> \
  --out <private-status-json>
```

3. Export with manifest and summary outputs:

```bash
python scripts/export_chatlog.py \
  --base-url http://127.0.0.1:5030 \
  --out-dir <private-output-dir> \
  --require-verified-snapshot <private-status-json>
```

The export wrapper creates raw conversation files, metadata, a private index, `manifest.csv`, and `summary.json`. Treat all generated outputs as private.

## Issue Status

| Issue | Status |
| --- | --- |
| #1 export wrapper | Implemented through `scripts/export_chatlog.py`; mock API test passes. |
| #2 readiness check | Implemented through `scripts/probe_chatlog.py`; non-loopback URLs are blocked. |
| #3 end-to-end validation | Still requires a private authorized local data run; public status note added. |
| #4 privacy controls | Strengthened through `scripts/check_public_safety.py`, test coverage, `.gitignore`, and the manual checklist. |
| #5 closed-state snapshot | Implemented through `scripts/verify_closed_snapshot.py` and `--require-verified-snapshot` export gate. |

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

or:

```bash
python scripts/check_public_safety.py --root .
python scripts/test_public_safety.py
```

The scan is intentionally conservative. It is not a substitute for human review.
