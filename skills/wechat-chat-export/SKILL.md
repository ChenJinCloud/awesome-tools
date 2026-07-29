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
| Public wrapper scripts | `scripts/probe_chatlog.py`, `scripts/export_chatlog.py`, `scripts/verify_closed_snapshot.py` |

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
   - If exporting from a copied data tree, verify the source-versus-snapshot status before starting the local service.

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
   - Verify readiness with a harmless API probe rather than assuming a dedicated health endpoint exists:
     `python scripts/probe_chatlog.py --base-url http://127.0.0.1:5030`
   - Treat `ready`, `decrypting`, `not_ready`, and `unsafe_target` as different states. Continue only on `ready`.
   - Record service URL, account, data directory, and work directory only in private local run metadata if needed.

7. **Export**
   - Use `scripts/export_chatlog.py` against an already-running local service:
     `python scripts/export_chatlog.py --base-url http://127.0.0.1:5030 --out-dir <private-output-dir>`
   - If the source is a copied snapshot, pass `--require-verified-snapshot <private-status-json>`.
   - The wrapper exports contacts, chatrooms, sessions, and conversations into private local output folders.
   - `manifest.csv` uses synthetic local labels such as `private_00001` instead of real talker IDs or contact names.
   - A private `metadata/private_index.json` maps local labels to real IDs and display names. Do not publish it.
   - `summary.json` records aggregate counts, failures, unmatched message table check status, manifest path, and finish time.

8. **Verify**
   - Check readiness result, manifest statuses, exported message totals, zero-message rows, failures, and unmatched message table status.
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
| Snapshot status is incomplete or unknown | Copy is missing files, log lacks completion proof, or source changed during copy | Do not export from that snapshot until a verified status JSON exists |

## Closed Snapshot Verification

Before using a copied WeChat data tree as the export source, run a read-only comparison:

```bash
python scripts/verify_closed_snapshot.py \
  --source <private-source-root> \
  --snapshot <private-closed-snapshot-root> \
  --robocopy-log <private-copy-log> \
  --out <private-status-json>
```

Proceed only if the output JSON has `"status": "verified"`. Treat `incomplete` and `unknown` as stop states.

## Public Safety

Before committing or publishing changes derived from private export work:

```bash
python scripts/check_public_safety.py --root .
python scripts/test_public_safety.py
```

Then manually review changed files with `docs/public-review-checklist.md`.

## Acceptance Criteria

- Scope and authorization are explicit.
- Exported records come only from local desktop data.
- `manifest.csv` and `summary.json` exist for completed exports.
- Verification reports count mismatches, failures, and unmatched tables.
- Readiness is verified by a loopback harmless API probe, not by an assumed health endpoint.
- Copied snapshots are exported only after `verify_closed_snapshot.py` returns `verified`.
- No raw chats, keys, helper logs, decrypted work folders, account IDs, private paths, or contact identifiers are published.
