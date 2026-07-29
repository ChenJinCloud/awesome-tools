# Public Review Checklist

Use this checklist before publishing any tool, workflow, validation note, or skill that came from a private local workflow.

## Blockers

Do not publish if any item below is present:

- raw chat content, exported JSON, message snippets, screenshots, or attachments;
- database keys, API keys, tokens, cookies, sessions, passwords, or credential file names;
- helper logs, stdout/stderr files, decrypted database work folders, or generated run metadata;
- machine-specific absolute paths;
- account IDs, contact IDs, chatroom IDs, private aliases, raw export filenames, or private display names;
- manifest, summary, private index, hash files, or validation outputs generated from private exports;
- exact private archive hashes, exact high-value private conversation counts, or other identifiers that can link back to a private archive.

## Required Checks

1. Run `python scripts/check_public_safety.py --root .`.
2. Run `python scripts/test_public_safety.py`.
3. Read the changed Markdown files manually for private aliases, local paths, contact IDs, raw counts, and copied message text.
4. Confirm `.gitignore` covers any generated output paths used during local testing.
5. Confirm any public validation note uses generic status language rather than private evidence.

## Safe Public Content

Acceptable public content includes:

- source repository links;
- generic workflow steps;
- privacy and authorization boundaries;
- script usage with placeholder paths;
- schema descriptions that do not include real private values;
- validation status such as `not yet publicly validated`, `private run completed`, or `blocked pending local data`, without private identifiers.
