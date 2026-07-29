#!/usr/bin/env python3
"""Public safety scan for this repository.

The scanner reports only file, line, and rule id. It intentionally does not
print matching line contents because matches may contain private values.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ContentRule:
    rule_id: str
    pattern: re.Pattern[str]
    hint: str


@dataclass(frozen=True)
class PathRule:
    rule_id: str
    pattern: re.Pattern[str]
    hint: str


CONTENT_RULES = [
    ContentRule(
        "windows-user-path",
        re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE),
        "Remove machine-specific user paths.",
    ),
    ContentRule(
        "lifeos-path",
        re.compile(r"[A-Za-z]:\\chenjin-life-os(?:\\|\b)", re.IGNORECASE),
        "Do not publish private Life OS paths.",
    ),
    ContentRule(
        "wechat-export-root",
        re.compile(r"[A-Za-z]:\\[^\r\n]*(?:wechat_full_export|xwechat_files)", re.IGNORECASE),
        "Do not publish local WeChat export roots.",
    ),
    ContentRule(
        "wechat-account-id",
        re.compile(r"wxid_[A-Za-z0-9_-]{6,}"),
        "Do not publish WeChat account or contact IDs.",
    ),
    ContentRule(
        "chatroom-id",
        re.compile(r"\b\d{6,}@chatroom\b"),
        "Do not publish chatroom identifiers.",
    ),
    ContentRule(
        "github-token",
        re.compile(r"(?:gho|ghp|github_pat)_[A-Za-z0-9_]{20,}"),
        "Do not publish GitHub tokens.",
    ),
    ContentRule(
        "openai-style-token",
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
        "Do not publish API keys.",
    ),
    ContentRule(
        "key-value-secret",
        re.compile(
            r"(?i)\b(?:CHATLOG_DATA_KEY|WECHAT_DB_KEY|DATABASE_KEY|SECRET|TOKEN|PASSWORD)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{8,}"
        ),
        "Do not publish secret-looking key/value pairs.",
    ),
    ContentRule(
        "vc-helper-result",
        re.compile(r"vc-helper-\d{8,}.*\.json", re.IGNORECASE),
        "Do not publish key-helper result files.",
    ),
    ContentRule(
        "raw-export-prefixed-name",
        re.compile(r"\b(?:private|groups)__\d+__", re.IGNORECASE),
        "Do not publish raw export filenames that may identify conversations.",
    ),
]


PATH_RULES = [
    PathRule(
        "database-file",
        re.compile(r"\.(?:db|db-shm|db-wal|sqlite|sqlite3)$", re.IGNORECASE),
        "Do not commit local databases.",
    ),
    PathRule(
        "key-file",
        re.compile(r"\.(?:key|pem|p12|pfx)$", re.IGNORECASE),
        "Do not commit key material.",
    ),
    PathRule(
        "helper-log",
        re.compile(r"\.(?:log|out|err)(?:\.txt)?$", re.IGNORECASE),
        "Do not commit helper logs.",
    ),
    PathRule(
        "export-manifest",
        re.compile(r"(?:^|/)(?:manifest\.csv|summary\.json|private_index\.json)$", re.IGNORECASE),
        "Do not commit generated export metadata.",
    ),
    PathRule(
        "private-output-dir",
        re.compile(r"(?:^|/)(?:exports|work|logs|runs|private|groups|metadata)(?:/|$)", re.IGNORECASE),
        "Do not commit generated export directories.",
    ),
]


IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache"}


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def normalized_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scan(root: Path) -> list[dict[str, object]]:
    root = root.resolve()
    scanner_path = Path(__file__).resolve()
    hits: list[dict[str, object]] = []

    for path in iter_files(root):
        rel = normalized_relative(path, root)
        for rule in PATH_RULES:
            if rule.pattern.search(rel):
                hits.append({"file": rel, "line": None, "rule": rule.rule_id, "hint": rule.hint})

        if path.resolve() == scanner_path:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            for rule in CONTENT_RULES:
                if rule.pattern.search(line):
                    hits.append({"file": rel, "line": line_no, "rule": rule.rule_id, "hint": rule.hint})
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan repository files for private export artifacts.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--json", action="store_true", help="Emit compact JSON hits.")
    args = parser.parse_args()

    root = Path(args.root)
    hits = scan(root)
    if not hits:
        print("Public safety scan passed.")
        return 0

    if args.json:
        import json

        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        print("Public safety scan failed.")
        for hit in hits:
            line = "" if hit["line"] is None else f":{hit['line']}"
            print(f"- {hit['file']}{line} [{hit['rule']}] {hit['hint']}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
