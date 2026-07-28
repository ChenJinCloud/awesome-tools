---
name: wechat-chat-export
description: Use when the user asks to export, refresh, inspect, verify, or build a local WeChat chat-record export workflow using chatlog_with_sns or compatible local APIs. Applies only to authorized local data already present on the user's computer. Keep raw chats, keys, helper logs, decrypted work folders, account IDs, and private paths out of public notes or repositories.
---

# WeChat Chat Export

Use this skill for local, authorization-bounded WeChat chat-record export work.

## Boundaries

- Only work on data the user owns or is explicitly authorized to process.
- Export can only cover records present on the local computer at export time.
- Do not promise recovery of server-side deleted, unsynced, or never-downloaded messages.
- Do not print, store, or publish database keys, credentials, raw chat bodies, helper logs, decrypted work directories, cookies, sessions, or private account identifiers.
- Keep public documentation generic: no machine-specific paths, account IDs, contact aliases, message hashes, or private export counts unless the user explicitly asks for a private local record.

## Source Layers

Use the layers separately:

| Layer | Default |
| --- | --- |
| Main export tool | `dake2482/chatlog_with_sns` |
| Historical upstream | `sjzar/chatlog`; verify current status before treating as usable |
| Optional Windows key helper | `Jrebort/VC-weixin-export`; release-only helper, not the main export engine |
| Local wrapper scripts | User- or project-specific helpers for starting the service, exporting all talks, and validating manifests |

Before downloading or building anything, recheck the current README, releases, license, and compliance notes for the selected upstream.

## Workflow

1. **Classify scope**
   - Confirm OS, CPU architecture, desktop WeChat version, account count, target conversations, output goal, and authorization.
   - Confirm the target chat history is visible in desktop WeChat.
   - If mobile records are not yet on the computer, stop export work and guide phone-to-computer migration or backup first.

2. **Prepare local workspace**
   - Use a local workspace with enough free disk space.
   - Keep raw exports, decrypted work folders, key files, and helper logs out of public repos and ordinary notes.
   - For public deliverables, record only tool links, generic steps, counts, coverage status, and non-identifying caveats.

3. **Prepare main tool**
   - Prefer the current `chatlog_with_sns` source or release if it supports the target OS and WeChat version.
   - Treat `sjzar/chatlog` as historical unless the current repository again provides usable code.
   - Build or install according to current upstream instructions rather than hardcoding old filenames.

4. **Find local WeChat data**
   - Discover the current data directory and account ID from the local machine.
   - Do not assume a Windows path or reuse another machine's account ID.
   - If multiple accounts exist, bind every export to one explicit account at a time.

5. **Acquire key**
   - Use the current supported key acquisition method for the platform.
   - On Windows, optional helper releases may be used only if the main workflow cannot acquire the key and the user accepts the local risk.
   - Never echo the key in chat, Markdown, terminal summaries, logs intended for sharing, or repository files.

6. **Start local service**
   - Start the `chatlog` HTTP service bound to localhost.
   - Verify the health endpoint before exporting.
   - Record service URL, account, data directory, and work directory only in private local run metadata if needed.

7. **Export**
   - Export contacts, chatrooms, sessions, and other available metadata.
   - Build a talker list from contacts, chatrooms, and sessions.
   - Export each conversation to JSON, separated into private and group outputs.
   - Produce `manifest.csv` with talker type, display name, exported message count, bytes, output file, status, and error.
   - Produce `summary.json` with export root, counts, unmatched message tables, manifest path, and finish time.

8. **Verify**
   - Check service health, manifest statuses, exported message totals, zero-message rows, and unmatched message table hashes.
   - For high-value conversations, verify by resolving aliases through contacts metadata, not by assuming display names are stable.
   - Hash selected output files for private local evidence records when needed.

9. **Close**
   - Stop the local service.
   - Keep raw data private.
   - For a public or shareable note, include only source links, generic workflow, non-sensitive counts if appropriate, and explicit limitations.

## Failure Handling

| Symptom | Likely Cause | Response |
| --- | --- | --- |
| Target messages missing | Not migrated or not downloaded on desktop WeChat | Stop and complete phone-to-computer migration first |
| Service starts but export fails | Wrong data directory, wrong account, wrong key, or decrypt still running | Recheck account/data/key binding and wait for decrypt completion |
| Manifest misses a known alias | Alias is not the internal talker ID | Resolve via contacts metadata |
| Public write contains private paths or IDs | Private run context leaked into documentation | Remove and rescan before publishing |
| Upstream repo changed | Tool source is version-sensitive | Re-read upstream README/releases before continuing |

## Acceptance Criteria

- Scope and authorization are explicit.
- Exported records come only from local desktop data.
- `manifest.csv` and `summary.json` exist for completed exports.
- Verification reports count mismatches, failures, and unmatched tables.
- No raw chats, keys, helper logs, decrypted work folders, account IDs, private paths, or contact identifiers are published.
