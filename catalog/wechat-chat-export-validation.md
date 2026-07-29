# WeChat Chat Export Validation Status

Updated: 2026-07-29

## Public Status

The public repository now contains reusable workflow support:

- `scripts/probe_chatlog.py` for local loopback readiness probing.
- `scripts/export_chatlog.py` for exporting through a chatlog-compatible local API and creating `manifest.csv` plus `summary.json`.
- `scripts/verify_closed_snapshot.py` for read-only source-versus-snapshot checks before exporting from a copied data tree.
- `scripts/check_public_safety.py` plus `scripts/test_public_safety.py` for public-safety scanning.

## Validation Boundary

No raw WeChat data, private account identifiers, local paths, database keys, helper logs, decrypted work folders, private aliases, export hashes, or generated private validation outputs are published in this repository.

This repository has not published an end-to-end validation note from a current local WeChat data copy. A future validation note should state only:

- tool or commit version used;
- generic local result status;
- whether readiness, export, manifest, summary, and snapshot checks passed;
- known limitations;
- validation date.

It must not include private paths, private counts, account IDs, contact IDs, aliases, hashes, raw records, or copied message content.

## Current Limitation

The full private end-to-end run still requires an authorized local data source and private local evidence. Until that run is performed and sanitized, this public status should be treated as workflow-ready but not public-evidence-validated.
