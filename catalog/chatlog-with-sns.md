# chatlog_with_sns

Status: `researched`  
Last reviewed: 2026-08-16  
Primary source: <https://github.com/dake2482/chatlog_with_sns>

## What It Is

`chatlog_with_sns` is a local WeChat inspection and export tool derived from `chatlog`. Its current focus is WeChat 4.x data on macOS and Windows. It provides local search and export for chat messages, contacts, group chats, recent sessions, Moments, and WeChat Favorites, with HTTP APIs, a local web console, TUI/CLI access, and Streamable HTTP MCP support.

## Why It Is Useful

- It works against local desktop WeChat data instead of uploading private chats to a hosted service.
- Chat logs can be queried by time, talker, sender, and keyword.
- Results can be returned as JSON, CSV, XLSX, text, or other supported formats.
- Contact tags can be used to narrow resource and relationship research.
- Moments and WeChat Favorites are useful supplementary sources for finding context, links, and prior recommendations.
- The local HTTP API can be wrapped by other tools or queried through MCP.

## Maintenance Assessment

The repository had a concentrated development period from late 2025 through early 2026, including WeChat 4.x support, WAL handling, database browsing, MCP, media access, Moments, Favorites, and contact tags. The latest visible commits were on 2026-04-15, including a README refresh and the addition of Moments fallback matching, contact tags, and Favorites queries.

The project published its first release, `v0.1.0`, on 2026-04-06. The release specifically called out macOS WeChat 4.x Moments database support. The repository currently shows 57 commits, but no open Issues or Pull Requests and only one public release. This indicates recent development activity, but not yet a mature maintenance process or a clear long-term compatibility commitment.

Assessment: `recently active, usable for evaluation, long-term maintenance uncertain`.

## Relevance To WeChat Export Workflow

This is the primary upstream engine for the local WeChat workflow in this collection. The surrounding wrapper layer can use its local HTTP service for readiness checks, conversation exports, manifests, summaries, and private validation. The upstream tool handles local data access and querying; the wrapper layer handles repeatability, export bookkeeping, and public-safety boundaries.

## Current Validation Boundary

This entry is `researched`, not `tested`. The repository claims support for macOS WeChat 4.x, but compatibility with a specific local installation, account, key-acquisition path, and current database state still requires a small authorized local test before a full export. Multiple WeChat accounts must be processed separately.

Do not treat a successful service start as proof of complete coverage. Validate readiness, account binding, message counts, export manifests, failures, and representative high-value conversations before relying on the output.

## Privacy And Safety

Use this tool only with data that the operator owns or is explicitly authorized to process. Keep database keys, raw databases, decrypted working folders, raw chat exports, private indexes, account identifiers, contact identifiers, and helper logs outside public repositories and ordinary shareable notes. Keep the HTTP service bound to localhost unless a different exposure boundary has been deliberately reviewed.

## Links

- Repository: <https://github.com/dake2482/chatlog_with_sns>
- Commit history: <https://github.com/dake2482/chatlog_with_sns/commits/main>
- Releases: <https://github.com/dake2482/chatlog_with_sns/releases>
- Issues: <https://github.com/dake2482/chatlog_with_sns/issues>
- Pull requests: <https://github.com/dake2482/chatlog_with_sns/pulls>

## Recheck Before Use

- Whether the latest source still supports the target macOS and WeChat versions.
- Whether the current release or source build is more appropriate than an unpinned main branch.
- Whether key acquisition works for the selected account without exposing credentials or keys.
- Whether the target conversations are actually present in desktop WeChat.
- Whether the repository license and upstream terms permit any intended redistribution.
