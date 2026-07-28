# WeChat Chat Export

## What It Is

A local-first workflow for exporting WeChat chat records that are already present on the user's own computer. The workflow uses `chatlog_with_sns` / `chatlog`-compatible local APIs for querying and exporting records, plus optional platform-specific key acquisition when required.

This is a workflow record, not a bundled WeChat database, key, export, or private archive.

## Why It Is High Quality

- Local-first: raw chat data, keys, decrypted work directories, and helper logs stay on the user's machine.
- Verifiable: every export should produce a manifest, a summary, and count/hash checks.
- Layered: main export engine, key acquisition, local wrapper scripts, and personal evidence indexes are treated as separate layers.
- Recoverable: the workflow is suitable for Codex-style execution because it has clear prerequisites, stop conditions, and validation steps.
- Boundary-aware: it explicitly avoids unauthorized access, cloud upload of private chat data, and public storage of raw records or secrets.

## Best Use Cases

- Exporting your own WeChat records already visible in desktop WeChat.
- Refreshing a local archive after phone-to-computer chat migration.
- Building an evidence index with file paths, counts, hashes, and coverage status.
- Verifying whether a target conversation was included in a prior export.

## Source / Project Links

| Layer | Link | Current Role |
| --- | --- | --- |
| Main tool | <https://github.com/dake2482/chatlog_with_sns> | Current primary public source for the workflow; MIT-licensed when checked on 2026-07-28. |
| Historical upstream | <https://github.com/sjzar/chatlog> | Historical upstream. As checked on 2026-07-28, the repository keeps a removal notice and no longer provides usable source or binaries. |
| Optional Windows helper | <https://github.com/Jrebort/VC-weixin-export> | Release-only Windows helper source; README says it does not contain project source code. Treat as optional key acquisition support, not the main export engine. |

Always recheck current repository status, release notes, legal/compliance notices, and platform support before using the workflow.

## Setup Notes

1. Confirm the user is operating on their own data or has explicit authorization.
2. Confirm the target chat history is already available in desktop WeChat.
3. Prepare a local workspace with enough disk capacity.
4. Install or build the main tool from the current public source.
5. Identify the local WeChat data directory and account ID from the current machine, without hardcoding prior paths.
6. Acquire the database key using the current supported method for the user's platform.
7. Start a local-only `chatlog` HTTP service.
8. Export metadata and conversations.
9. Verify `manifest.csv`, `summary.json`, message counts, unmatched tables, and selected file hashes.
10. Stop the local service and keep private artifacts outside public notes or repositories.

## Boundaries And Risks

- Do not export other people's data without explicit authorization.
- Do not claim to recover messages that were never synced to the current computer.
- Do not upload raw databases, raw chat JSON, keys, helper logs, cookies, sessions, or decrypted work directories to GitHub or cloud tools.
- Do not publish local account IDs, private conversation aliases, contact identifiers, machine-specific paths, or export hashes if they identify private archives.
- Treat key acquisition and local decryption as compliance-sensitive and version-sensitive.

## My Usage Status

This entry records a public-safe version of a local workflow. Private machine paths, account IDs, contact aliases, raw exports, helper logs, and verification outputs are intentionally excluded.

## Recheck Before Use

- Whether `chatlog_with_sns` still supports the target WeChat version and OS.
- Whether the historical `sjzar/chatlog` repository status has changed.
- Whether any optional key helper is still available and trustworthy.
- Whether the user's desktop WeChat actually contains the target records.
- Whether local laws, platform terms, and authorization boundaries permit the intended export.
