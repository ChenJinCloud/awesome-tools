#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, build_opener

from probe_chatlog import probe


OPENER = build_opener(ProxyHandler({}))


def fetch_bytes(base_url: str, path: str, params: dict[str, str] | None = None, timeout: int = 300) -> bytes:
    url = base_url.rstrip("/") + path
    if params:
        url += "?" + urlencode(params)
    try:
        with OPENER.open(url, timeout=timeout) as resp:
            return resp.read()
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {path}: {body[:200]}") from exc
    except URLError as exc:
        raise RuntimeError(f"Request failed for {path}: {exc}") from exc


def fetch_json(base_url: str, path: str, params: dict[str, str] | None = None, timeout: int = 300) -> Any:
    return json.loads(fetch_bytes(base_url, path, params, timeout).decode("utf-8-sig"))


def save_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def items_from(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return [item for item in payload["items"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def safe_part(value: str, fallback: str, limit: int = 80) -> str:
    text = str(value or "").strip() or fallback
    text = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "_", text)
    text = re.sub(r"\s+", " ", text).strip(" ._")
    return (text or fallback)[:limit]


def md5_text(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def classify_talker(talker: str) -> str:
    return "group" if talker.endswith("@chatroom") else "private"


def add_talker(talkers: dict[str, dict[str, Any]], talker: str, source: str, display: str = "") -> None:
    if not talker:
        return
    entry = talkers.setdefault(
        talker,
        {
            "talker": talker,
            "display": "",
            "sources": set(),
            "session_order": None,
        },
    )
    entry["sources"].add(source)
    if display and not entry["display"]:
        entry["display"] = display


def build_talkers(contacts: Any, chatrooms: Any, sessions: Any, selected: list[str]) -> list[dict[str, Any]]:
    talkers: dict[str, dict[str, Any]] = {}
    for contact in items_from(contacts):
        talker = contact.get("userName") or contact.get("UserName")
        display = contact.get("remark") or contact.get("nickName") or contact.get("alias") or ""
        add_talker(talkers, str(talker or ""), "contact", str(display or ""))
    for room in items_from(chatrooms):
        talker = room.get("name") or room.get("Name")
        display = room.get("remark") or room.get("nickName") or ""
        add_talker(talkers, str(talker or ""), "chatroom", str(display or ""))
    for index, session in enumerate(items_from(sessions)):
        talker = session.get("userName") or session.get("UserName")
        display = session.get("nickName") or ""
        add_talker(talkers, str(talker or ""), "session", str(display or ""))
        if talker and talkers[str(talker)]["session_order"] is None:
            talkers[str(talker)]["session_order"] = index

    if selected:
        for talker in selected:
            add_talker(talkers, talker, "explicit")
        values = [talkers[talker] for talker in selected if talker in talkers]
    else:
        values = list(talkers.values())

    for item in values:
        item["sources"] = sorted(item["sources"])
        item["type"] = classify_talker(item["talker"])
    values.sort(
        key=lambda item: (
            0 if item["type"] == "private" else 1,
            item["session_order"] if item["session_order"] is not None else 999999,
            safe_part(item.get("display") or item["talker"], "unnamed").casefold(),
        )
    )
    return values


def message_table_stats(work_dir: Path | None) -> dict[str, int]:
    if work_dir is None:
        return {}
    msg_dir = work_dir / "db_storage" / "message"
    stats: dict[str, int] = {}
    for db_path in sorted(msg_dir.glob("message_*.db")):
        try:
            con = sqlite3.connect(str(db_path))
            try:
                tables = [
                    row[0]
                    for row in con.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'"
                    )
                ]
                for table in tables:
                    digest = table[4:]
                    row = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()
                    stats[digest] = stats.get(digest, 0) + int(row[0] or 0)
            finally:
                con.close()
        except sqlite3.Error as exc:
            print(f"[warn] cannot read message table stats from {db_path.name}: {exc}", file=sys.stderr)
    return stats


def count_json_array(path: Path) -> int | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return len(data) if isinstance(data, list) else None
    except Exception:
        return None


def require_verified_snapshot(path: Path | None) -> None:
    if path is None:
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") != "verified":
        raise RuntimeError(
            "snapshot verification status is not verified; "
            "run verify_closed_snapshot.py and use a verified source before export"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export local chatlog conversations with manifest and summary outputs.")
    parser.add_argument("--base-url", default="http://127.0.0.1:5030")
    parser.add_argument("--out-dir", required=True, help="Private local output directory. Do not place inside a public repo.")
    parser.add_argument("--work-dir", help="Optional decrypted work directory for unmatched message-table checks.")
    parser.add_argument("--talker", action="append", default=[], help="Optional internal talker id. Repeat for multiple.")
    parser.add_argument("--limit-talkers", type=int, default=0, help="Debug limit; 0 means no limit.")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--require-verified-snapshot", help="Path to verify_closed_snapshot.py status JSON.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    require_verified_snapshot(Path(args.require_verified_snapshot).resolve() if args.require_verified_snapshot else None)

    readiness = probe(args.base_url, timeout=10)
    if readiness.status != "ready":
        raise RuntimeError(f"chatlog service is not ready: {readiness.to_dict()}")

    started = time.strftime("%Y%m%d-%H%M%S")
    out_root = out_dir / started
    private_dir = out_root / "private"
    group_dir = out_root / "groups"
    metadata_dir = out_root / "metadata"
    out_root.mkdir(parents=True, exist_ok=True)

    metadata_specs = [
        ("contacts", "/api/v1/contact", {"format": "json", "limit": "0"}),
        ("chatrooms", "/api/v1/chatroom", {"format": "json", "limit": "0"}),
        ("sessions", "/api/v1/session", {"format": "json", "limit": "0"}),
    ]
    loaded: dict[str, Any] = {}
    for name, endpoint, params in metadata_specs:
        try:
            data = fetch_bytes(args.base_url, endpoint, params, timeout=args.timeout)
            save_bytes(metadata_dir / f"{name}.json", data)
            loaded[name] = json.loads(data.decode("utf-8-sig"))
            print(f"[metadata] saved {name}.json")
        except Exception as exc:
            print(f"[warn] metadata {name} failed: {exc}", file=sys.stderr)

    talkers = build_talkers(
        loaded.get("contacts", {}),
        loaded.get("chatrooms", {}),
        loaded.get("sessions", {}),
        args.talker,
    )
    if args.limit_talkers:
        talkers = talkers[: args.limit_talkers]

    table_stats = message_table_stats(Path(args.work_dir).resolve() if args.work_dir else None)
    known_hashes = {md5_text(item["talker"]) for item in talkers}
    unmatched_count: int | None = None
    if table_stats:
        unmatched_count = len(set(table_stats) - known_hashes)

    private_index: dict[str, Any] = {}
    manifest_path = out_root / "manifest.csv"
    fields = [
        "index",
        "type",
        "local_label",
        "sources",
        "raw_rows",
        "exported_messages",
        "bytes",
        "file",
        "status",
        "error",
    ]
    failures = 0
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as mf:
        writer = csv.DictWriter(mf, fieldnames=fields)
        writer.writeheader()
        for idx, item in enumerate(talkers, start=1):
            label = f"{item['type']}_{idx:05d}"
            target_dir = private_dir if item["type"] == "private" else group_dir
            dest = target_dir / f"{label}.json"
            digest = md5_text(item["talker"])
            private_index[label] = {
                "talker": item["talker"],
                "display": item.get("display", ""),
                "type": item["type"],
                "sources": item["sources"],
            }
            row = {
                "index": idx,
                "type": item["type"],
                "local_label": label,
                "sources": ";".join(item["sources"]),
                "raw_rows": table_stats.get(digest, "") if table_stats else "",
                "exported_messages": "",
                "bytes": "",
                "file": dest.relative_to(out_root).as_posix(),
                "status": "pending",
                "error": "",
            }
            try:
                data = fetch_bytes(
                    args.base_url,
                    "/api/v1/chatlog",
                    {"time": "all", "talker": item["talker"], "format": "json", "limit": "0"},
                    timeout=args.timeout,
                )
                save_bytes(dest, data)
                row["bytes"] = len(data)
                count = count_json_array(dest)
                row["exported_messages"] = "" if count is None else count
                row["status"] = "ok"
            except Exception as exc:
                failures += 1
                row["status"] = "error"
                row["error"] = str(exc)[:300]
            writer.writerow(row)
            mf.flush()
            print(f"[{idx}/{len(talkers)}] {row['status']} {label}")

    (metadata_dir / "private_index.json").write_text(
        json.dumps(private_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    summary = {
        "export_root": str(out_root),
        "talkers_exported": len(talkers),
        "private_count": sum(1 for item in talkers if item["type"] == "private"),
        "group_count": sum(1 for item in talkers if item["type"] == "group"),
        "failures": failures,
        "unmatched_message_table_hashes": unmatched_count,
        "unmatched_message_table_check": "checked" if table_stats else "not_checked",
        "manifest": str(manifest_path),
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "public_safety_note": "Output may contain private chat data and identifiers. Do not commit it.",
    }
    (out_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[done] " + json.dumps(summary, ensure_ascii=False))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
