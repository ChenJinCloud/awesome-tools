# Changelog

## 2026-08-07

- Added `LICENSE` (MIT). The repo was public with no declared license, which meant reuse or forking had no clear legal basis.
- Added this `CHANGELOG.md` so the public package's own version history is visible to external users, separate from the maintainer's private Life OS closeout logs.
- Documented in `README.md` that the project is MIT licensed.
- Added a pytest suite (`tests/test_extract_session_events.py`) covering `extract_session_events.py`: text truncation/whitespace collapsing, message content extraction, system/developer/environment-context filtering, function-call and generic `*_call` event capture, malformed/blank line handling, markdown rendering, and the CLI's file-output and missing-file-error paths.
- Added a GitHub Actions workflow (`.github/workflows/tests.yml`) that runs the test suite on every push and pull request.

## 2026-06-30

- Initial public release. Extracted from the maintainer's local `codex-closeout-archive` skill, with machine-specific Life OS routing removed and destination resolution generalized (repo/workspace root, or the nearest `AGENTS.md`-equivalent policy).
