# Codex Closeout Archive

`codex-closeout-archive` is a Codex skill for closing a conversation with a compact, traceable process asset before archiving the thread.

It is designed for workflows where important context lives in the conversation itself: intent changes, user corrections, evidence paths, file outputs, decisions, and final state.

## What It Does

- Creates one concise Markdown process asset for each explicit closeout request.
- Captures the key timeline, decisions, output files, evidence paths, and open follow-ups.
- Avoids copying full raw transcripts, credentials, private messages, or sensitive exports.
- Uses nearby project indexes or changelogs when local workspace policy requires it.
- Archives the current Codex conversation after the asset is written and verified.

## Install

Copy this repository folder into your Codex skills directory:

```text
~/.codex/skills/codex-closeout-archive
```

Then start a new Codex thread or refresh skill discovery.

## Usage

Ask Codex to use the skill explicitly:

```text
Use $codex-closeout-archive to close this conversation with a concise process asset and archive it.
```

You can also ask in natural language:

```text
Close this thread and preserve the key decisions and evidence paths.
```

## Files

```text
SKILL.md
agents/openai.yaml
scripts/extract_session_events.py
tests/test_extract_session_events.py
```

## Helper Script

The helper script extracts a compact event inventory from Codex session JSONL files:

```bash
python scripts/extract_session_events.py --latest
python scripts/extract_session_events.py --session "/path/to/rollout.jsonl"
```

The helper output is only a starting point. The final process asset should be curated by the agent so it preserves the useful evolution without exposing private transcript content.

## Privacy Boundary

This skill is meant to preserve traceability, not to publish raw conversation data. Generated process assets should avoid:

- credentials, tokens, and secrets
- full private chat logs
- full Slack, email, or DM content
- sensitive third-party personal data
- unnecessary raw JSONL transcript excerpts

## Development

The helper script has a pytest suite covering event parsing, message filtering, and the CLI:

```bash
pip install -r requirements-dev.txt
pytest
```

CI runs this suite on every push and pull request (`.github/workflows/tests.yml`).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
