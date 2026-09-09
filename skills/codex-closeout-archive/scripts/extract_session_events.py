#!/usr/bin/env python3
"""Extract a compact event inventory from a Codex session JSONL file. / 从 Codex 会话 JSONL 文件中提取精简事件清单。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable


DEFAULT_ROOTS = [
    Path.home() / ".codex" / "sessions",
    Path.home() / ".codex" / "archived_sessions",
]


def iter_session_files() -> Iterable[Path]:
    for root in DEFAULT_ROOTS:
        if root.exists():
            yield from root.rglob("rollout-*.jsonl")


def latest_session() -> Path:
    files = list(iter_session_files())
    if not files:
        raise SystemExit("No Codex session files found under ~/.codex. / 未在 ~/.codex 下找到 Codex 会话文件。")
    return max(files, key=lambda p: p.stat().st_mtime)


def short(text: str, limit: int) -> str:
    text = " ".join(text.replace("\r", "\n").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""

    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts)


def load_events(path: Path, max_chars: int, include_system: bool) -> tuple[dict[str, Any], list[dict[str, str]]]:
    meta: dict[str, Any] = {}
    events: list[dict[str, str]] = []

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue

            timestamp = str(row.get("timestamp", ""))
            row_type = row.get("type")
            payload = row.get("payload") or {}

            if row_type == "session_meta" and isinstance(payload, dict):
                meta = payload
                continue

            if row_type != "response_item" or not isinstance(payload, dict):
                continue

            item_type = payload.get("type")

            if item_type == "message":
                role = str(payload.get("role", ""))
                if role in {"system", "developer"} and not include_system:
                    continue
                text = content_text(payload.get("content"))
                if text.lstrip().startswith("<environment_context>") and not include_system:
                    continue
                if not text:
                    continue
                phase = payload.get("phase")
                kind = f"{role}"
                if phase:
                    kind += f"/{phase}"
                events.append(
                    {
                        "time": timestamp,
                        "kind": kind,
                        "summary": short(text, max_chars),
                    }
                )
                continue

            if item_type == "function_call":
                name = str(payload.get("name", "function_call"))
                namespace = payload.get("namespace")
                label = f"tool:{namespace}.{name}" if namespace else f"tool:{name}"
                args = payload.get("arguments", "")
                if not isinstance(args, str):
                    args = json.dumps(args, ensure_ascii=False)
                events.append(
                    {
                        "time": timestamp,
                        "kind": label,
                        "summary": short(args, max_chars),
                    }
                )
                continue

            if item_type and str(item_type).endswith("_call"):
                name = str(payload.get("name") or item_type)
                args = payload.get("arguments", "")
                if not isinstance(args, str):
                    args = json.dumps(args, ensure_ascii=False)
                events.append(
                    {
                        "time": timestamp,
                        "kind": f"tool:{name}",
                        "summary": short(args, max_chars),
                    }
                )

    return meta, events


def render(path: Path, meta: dict[str, Any], events: list[dict[str, str]]) -> str:
    lines = [
        "# Codex Session Event Inventory / Codex 会话事件清单",
        "",
        f"Session file: `{path}` / 会话文件",
        f"Thread id: `{meta.get('id', 'unknown')}` / 任务 ID",
        f"Started: `{meta.get('timestamp', 'unknown')}` / 开始时间",
        f"CWD: `{meta.get('cwd', 'unknown')}` / 工作目录",
        "",
        "| Time / 时间 | Kind / 类型 | Summary / 摘要 |",
        "| --- | --- | --- |",
    ]

    for event in events:
        summary = event["summary"].replace("|", "\\|")
        lines.append(f"| {event['time']} | {event['kind']} | {summary} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--session", type=Path, help="Path to a Codex rollout JSONL file. / Codex rollout JSONL 文件路径。")
    group.add_argument("--latest", action="store_true", help="Use the latest modified rollout JSONL file. / 使用最后修改的 rollout JSONL 文件。")
    parser.add_argument("--out", type=Path, help="Optional markdown output path. / 可选的 Markdown 输出路径。")
    parser.add_argument("--max-chars", type=int, default=220, help="Max characters per event summary. / 每条事件摘要的最大字符数。")
    parser.add_argument("--include-system", action="store_true", help="Include system/developer/environment messages. / 包含系统、开发者和环境消息。")
    args = parser.parse_args()

    path = latest_session() if args.latest else args.session
    path = path.expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Session file not found: {path}")

    meta, events = load_events(path, args.max_chars, args.include_system)
    output = render(path, meta, events)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        try:
            if hasattr(sys.stdout, "buffer"):
                sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
            else:
                os.write(1, output.encode("utf-8", errors="replace"))
        except BrokenPipeError:
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
