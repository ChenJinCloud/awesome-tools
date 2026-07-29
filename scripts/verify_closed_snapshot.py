#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_iso(value: str | None) -> float | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(text).timestamp()


def tree_stats(root: Path) -> dict[str, Any]:
    files = 0
    bytes_total = 0
    newest_mtime = 0.0
    relative_files: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        stat = path.stat()
        files += 1
        bytes_total += stat.st_size
        newest_mtime = max(newest_mtime, stat.st_mtime)
        relative_files.append(path.relative_to(root).as_posix())
    return {
        "files": files,
        "bytes": bytes_total,
        "newest_mtime": newest_mtime,
        "relative_files": relative_files,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sample_hashes(source: Path, snapshot: Path, relative_files: list[str], sample_size: int) -> dict[str, Any]:
    checked = 0
    mismatches = 0
    missing = 0
    for rel in sorted(relative_files)[:sample_size]:
        src = source / rel
        dst = snapshot / rel
        if not src.exists() or not dst.exists():
            missing += 1
            continue
        checked += 1
        if sha256(src) != sha256(dst):
            mismatches += 1
    return {"checked": checked, "missing": missing, "mismatches": mismatches}


def parse_robocopy_log(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"provided": False, "status": "unknown", "reason": "no robocopy log provided"}
    if not path.exists():
        return {"provided": True, "status": "incomplete", "reason": "robocopy log not found"}
    text = path.read_text(encoding="utf-8", errors="replace")
    has_summary = bool(re.search(r"\b(?:Files|Dirs|Directories)\b", text, re.IGNORECASE))
    failed_values = [int(value) for value in re.findall(r"(?i)(?:FAILED|Failed)\s*[:=]?\s*(\d+)", text)]
    mismatch_values = [int(value) for value in re.findall(r"(?i)(?:MISMATCH|Mismatch)\s*[:=]?\s*(\d+)", text)]
    if failed_values and any(value > 0 for value in failed_values):
        return {"provided": True, "status": "incomplete", "reason": "robocopy log reports failures"}
    if mismatch_values and any(value > 0 for value in mismatch_values):
        return {"provided": True, "status": "incomplete", "reason": "robocopy log reports mismatches"}
    if not has_summary:
        return {"provided": True, "status": "unknown", "reason": "normal completion summary not found"}
    return {"provided": True, "status": "ok", "reason": "no failures or mismatches detected in parsed log"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only verification for a closed-state WeChat data snapshot.")
    parser.add_argument("--source", required=True, help="Original local data root.")
    parser.add_argument("--snapshot", required=True, help="Closed-state snapshot root.")
    parser.add_argument("--out", required=True, help="Private local JSON status output.")
    parser.add_argument("--robocopy-log", help="Optional robocopy log to parse.")
    parser.add_argument("--snapshot-start", help="Optional ISO timestamp for detecting source changes after copy started.")
    parser.add_argument("--required-relative", action="append", default=["db_storage", "msg"])
    parser.add_argument("--sample-size", type=int, default=25)
    args = parser.parse_args()

    source = Path(args.source).resolve()
    snapshot = Path(args.snapshot).resolve()
    out = Path(args.out).resolve()
    reasons: list[str] = []

    if not source.exists():
        reasons.append("source root does not exist")
    if not snapshot.exists():
        reasons.append("snapshot root does not exist")
    if reasons:
        result = {"status": "incomplete", "reasons": reasons}
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    source_stats = tree_stats(source)
    snapshot_stats = tree_stats(snapshot)
    source_set = set(source_stats["relative_files"])
    snapshot_set = set(snapshot_stats["relative_files"])
    missing_files = len(source_set - snapshot_set)
    extra_files = len(snapshot_set - source_set)
    required_missing = [rel for rel in args.required_relative if not (snapshot / rel).exists()]
    hash_stats = sample_hashes(source, snapshot, list(source_set & snapshot_set), args.sample_size)
    log_status = parse_robocopy_log(Path(args.robocopy_log).resolve() if args.robocopy_log else None)
    snapshot_start = parse_iso(args.snapshot_start)
    source_changed_after_start = False
    if snapshot_start is not None:
        source_changed_after_start = source_stats["newest_mtime"] > snapshot_start

    if source_stats["files"] != snapshot_stats["files"]:
        reasons.append("source and snapshot file counts differ")
    if source_stats["bytes"] != snapshot_stats["bytes"]:
        reasons.append("source and snapshot byte totals differ")
    if missing_files:
        reasons.append("snapshot is missing files present in source")
    if required_missing:
        reasons.append("snapshot is missing required relative paths")
    if hash_stats["missing"] or hash_stats["mismatches"]:
        reasons.append("sample hash check found missing files or mismatches")
    if log_status["status"] == "incomplete":
        reasons.append(str(log_status["reason"]))
    if source_changed_after_start:
        reasons.append("source contains files newer than snapshot-start boundary")

    if reasons:
        status = "incomplete"
    elif log_status["status"] != "ok":
        status = "unknown"
        reasons.append(str(log_status["reason"]))
    else:
        status = "verified"

    result = {
        "status": status,
        "reasons": reasons,
        "source_files": source_stats["files"],
        "snapshot_files": snapshot_stats["files"],
        "source_bytes": source_stats["bytes"],
        "snapshot_bytes": snapshot_stats["bytes"],
        "missing_files": missing_files,
        "extra_files": extra_files,
        "required_missing": required_missing,
        "sample_hashes": hash_stats,
        "robocopy_log": log_status,
        "source_changed_after_snapshot_start": source_changed_after_start,
        "privacy_note": "This private result may reveal local archive shape. Do not commit it.",
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "verified" else 2


if __name__ == "__main__":
    raise SystemExit(main())
