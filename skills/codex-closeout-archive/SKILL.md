---
name: codex-closeout-archive
description: Use when the user asks to close, archive, preserve, or harvest a Codex or agent conversation by creating a concise process asset with decisions, outputs, evidence paths, and follow-ups.
---

# Codex Closeout Archive

Use this skill only when the user explicitly asks to close, archive, end, harvest, or preserve a conversation. The purpose is to save the useful process trail without copying a full transcript.

## Why This Exists

Agent conversations often contain decisions, corrections, evidence paths, and output locations that are easy to lose. A closeout asset keeps the recoverable trail short and useful.

## Non-Negotiables

- Create one concise process asset when the skill is used.
- Preserve decisions, corrections, output files, evidence paths, and open follow-ups.
- Do not paste full transcripts, private messages, credentials, raw exports, or secrets.
- Do not delete or rewrite original session files.
- Archive the conversation only after the process asset is written and verified.

## Destination Rules

Configure:

```text
LIFE_OS_ROOT=<your durable record root>
CLOSEOUT_ROOT=<default closeout folder>
```

Prefer the most specific related project folder. Use the default closeout folder only when no project folder is clear.

Recommended filename:

```text
<topic-slug>__codex-process-asset__YYYY-MM-DD.md
```

## Process Asset Template

```markdown
# <Title> Codex Process Asset

Date archived: YYYY-MM-DD
Archive time: YYYY-MM-DD HH:mm+TZ
Workspace: `<absolute path or unknown>`
Local project: `<absolute path or unknown>`
Session evidence: `<session path or live-thread note>`
Thread id: `<id or unknown>`

## 1. Asset Type

This is a process asset. It preserves the key evolution, not the full transcript.

## 2. Why This Was Preserved

## 3. Concise Timeline

| Time | Event | Meaning |
| --- | --- | --- |

## 4. Outputs And Evidence

| Type | Path / Link | Notes |
| --- | --- | --- |

## 5. Decisions And Corrections

## 6. Open Follow-Ups

## 7. Boundaries

- Raw private messages, credentials, and full session logs were not copied.
- Original session files were left in place.

## 8. Retrieval Tags
```

## Verification

- Confirm the asset exists.
- Confirm it includes session evidence or a live-thread note.
- Confirm nearby index or changelog updates if your system requires them.
- Report changed files before archiving.
