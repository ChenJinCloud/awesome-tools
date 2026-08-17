---
name: codex-closeout-archive
description: Close and archive Codex conversations by creating a concise traceable process asset in the current workspace or project folder where the skill is invoked. Use when the user asks to end, close, archive, harvest, or preserve a Codex thread, conversation, decision trail, outputs, evidence paths, or final state across any workspace.
---

# Codex Closeout Archive

Use this skill when the user explicitly asks to close, archive, end, harvest, or preserve a Codex conversation. It turns the conversation into a lightweight process asset, then archives the conversation.

The user's explicit closeout request is the assetization decision. Do not re-litigate whether the thread deserves preservation once this skill has been invoked; every closeout creates a concise process asset.

## Why This Skill Exists

Codex threads often contain the real work: intent shifts, user corrections, evidence paths, file changes, external-source checks, and final decisions. If the thread is only archived in the app, the next conversation can lose why decisions changed.

This skill preserves the reusable trail without copying the whole transcript. It protects:

- Traceability: future work can find the original session, files, and evidence.
- Decision continuity: key turns and corrections survive across threads.
- Low-friction closeout: every ending produces one useful artifact, not a large archive system.

Do not use this skill merely because a conversation has become quiet or because an agent wants tidy closure. Use it when closeout, archive, harvest, or preservation is the user's requested next state.

## Non-Negotiables

- Create a process asset every time this skill is used.
- Use the current workspace or project folder where the skill is invoked as the destination by default.
- Keep the timeline concise: usually 5-12 key turns.
- Preserve key turns, user corrections, decisions, output files, and evidence paths.
- Do not paste a full raw transcript, full Slack or DM content, credentials, or sensitive exports into the asset.
- Do not delete, move, or rewrite original Codex session files.
- After the asset is written and verified, archive the current conversation unless the user asks to prepare the asset without ending the thread.

## Workflow

### 1. Resolve The Destination

The destination contract is location-based: write the process asset into the current workspace or project folder where the user invoked the skill. This makes closeout portable across projects: if the user uses the skill under project A, archive the chat into project A; if they use it under folder B, archive the chat into folder B.

Prefer, in order:

1. A destination folder explicitly named by the user in the closeout request.
2. The current working directory from the live thread environment or session metadata.
3. The current repo or workspace root only when it is the same project folder the user is operating from.
4. A durable project folder required by local `AGENTS.md` or equivalent workspace instructions, only when those instructions explicitly define where closeout/process assets must live.

Do not search broadly for a "more related" project folder outside the current workspace. Ask one concise question only if the current folder cannot be determined or local instructions conflict with the user's requested destination.

If the destination folder has a durable record system, follow its nearest `AGENTS.md` or equivalent project instructions before writing, while keeping the asset inside that same destination project.

Use a filename like:

```text
<topic-slug>__codex-process-asset__YYYY-MM-DD.md
```

If no topic slug is obvious, use:

```text
codex-closeout__YYYY-MM-DD.md
```

### 2. Locate Evidence

Record evidence paths before writing the asset.

Look for:

- Current workspace path.
- Current or archived Codex session JSONL path.
- Thread id from the JSONL `session_meta` payload when available.
- Files created, edited, moved, or verified during the conversation.
- External systems read or written, with links or query names when safe to preserve.

The session file is commonly under:

```text
~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
~/.codex/archived_sessions/rollout-*.jsonl
```

On Windows, `~` usually resolves to the user's profile directory.

If the current live session is not yet visible on disk, write that explicitly:

```text
Codex session evidence: current live thread; JSONL not located at closeout time.
```

Optional helper:

```bash
python scripts/extract_session_events.py --latest
python scripts/extract_session_events.py --session "/path/to/rollout.jsonl"
```

Use the helper only to get a raw event inventory. Curate the final timeline yourself.

### 3. Write The Process Asset

Use this structure:

```markdown
# <Title> Codex Process Asset

Date archived: YYYY-MM-DD
Archive time: YYYY-MM-DD HH:mm+TZ
Workspace: `<absolute path>`
Local project: `<absolute path>`
Codex session evidence: `<absolute path or live-thread note>`
Thread id: `<id or unknown>`

## 1. Asset Type

This file is a process asset. It preserves the Codex conversation's key evolution, not the full raw transcript.

## 2. Why This Was Preserved

- <why the closeout matters>
- <what future reader should recover from this asset>

## 3. Concise Timeline

| Time | Event | Meaning |
| --- | --- | --- |
| <time> | <key turn> | <why it mattered> |

## 4. Outputs And Evidence

| Type | Path / Link | Notes |
| --- | --- | --- |

## 5. Decisions And Corrections

- <final decision>
- <important user correction>
- <boundary clarified>

## 6. Open Follow-Ups

- <item or "None recorded">

## 7. Boundaries

- Raw private messages, credentials, and full Codex JSONL content were not copied.
- Original session files were left in place.

## 8. Retrieval Tags

- <tag>
```

Keep the prose compact. The asset should be useful to reread in one or two minutes.

### 4. Update Nearby Indexes

Update the smallest nearby discovery surface when it exists:

- `README.md` or `index.md` in the project folder, if it has an artifact table or source map.
- `CHANGELOG.md` in the project folder, if it exists.
- Any local run ledger or project index required by `AGENTS.md` or equivalent workspace policy.

Do not create a new folder only for closeouts unless no reasonable project folder exists.

### 5. Verify

Before finalizing:

- Confirm the process asset exists at the intended path.
- Search the asset for the session evidence path or live-thread note.
- Confirm any index or changelog update mentions the new asset.
- List the files changed.

### 6. Final Response And Archive

Reply briefly with:

- Process asset path.
- Any index or changelog files updated.
- Evidence path status.
- Any follow-up that remains open.

Then archive the current conversation. In Codex Desktop, emit the archive directive as the final line:

```text
::archive{reason="Closeout process asset created and conversation archived"}
```

Only skip the archive directive if the user asks to prepare a closeout without ending the thread.

## Examples

Use this skill for prompts like:

- "End this Codex thread and create a traceable process asset."
- "Archive this conversation, preserving the key decisions and evidence paths."
- "Close this thread with a concise process asset."
- "Run closeout and leave the output path and session evidence in the project folder."
