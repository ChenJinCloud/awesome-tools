import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import extract_session_events as ese  # noqa: E402


def _write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


# --- short() ---------------------------------------------------------------


def test_short_no_truncation_when_within_limit():
    assert ese.short("hello world", 20) == "hello world"


def test_short_truncates_to_exact_limit_with_ellipsis():
    result = ese.short("a" * 30, 10)
    assert result == "aaaaaaa..."
    assert len(result) == 10


def test_short_collapses_whitespace_and_newlines():
    text = "line one\r\nline   two\n\nline three"
    assert ese.short(text, 200) == "line one line two line three"


# --- content_text() ---------------------------------------------------------


def test_content_text_from_plain_string():
    assert ese.content_text("hello") == "hello"


def test_content_text_from_list_of_text_items():
    content = [{"text": "first"}, {"text": "second"}]
    assert ese.content_text(content) == "first\nsecond"


def test_content_text_ignores_non_dict_and_non_text_items():
    content = ["raw string", {"type": "input_image"}, {"text": "kept"}]
    assert ese.content_text(content) == "kept"


def test_content_text_returns_empty_for_unsupported_type():
    assert ese.content_text(42) == ""
    assert ese.content_text(None) == ""


# --- load_events() -----------------------------------------------------------


def test_load_events_captures_session_meta(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [{"type": "session_meta", "payload": {"id": "abc123", "timestamp": "t0", "cwd": "/tmp"}}],
    )
    meta, events = ese.load_events(session, max_chars=220, include_system=False)
    assert meta == {"id": "abc123", "timestamp": "t0", "cwd": "/tmp"}
    assert events == []


def test_load_events_includes_user_and_assistant_messages(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [
            {"type": "response_item", "timestamp": "t1", "payload": {"type": "message", "role": "user", "content": "hi"}},
            {
                "type": "response_item",
                "timestamp": "t2",
                "payload": {"type": "message", "role": "assistant", "content": [{"text": "hello back"}]},
            },
        ],
    )
    _, events = ese.load_events(session, max_chars=220, include_system=False)
    assert [e["kind"] for e in events] == ["user", "assistant"]
    assert [e["summary"] for e in events] == ["hi", "hello back"]


def test_load_events_excludes_system_and_developer_by_default(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [
            {"type": "response_item", "timestamp": "t1", "payload": {"type": "message", "role": "system", "content": "sys prompt"}},
            {"type": "response_item", "timestamp": "t2", "payload": {"type": "message", "role": "developer", "content": "dev note"}},
            {"type": "response_item", "timestamp": "t3", "payload": {"type": "message", "role": "user", "content": "kept"}},
        ],
    )
    _, events = ese.load_events(session, max_chars=220, include_system=False)
    assert [e["kind"] for e in events] == ["user"]


def test_load_events_includes_system_when_requested(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [{"type": "response_item", "timestamp": "t1", "payload": {"type": "message", "role": "system", "content": "sys prompt"}}],
    )
    _, events = ese.load_events(session, max_chars=220, include_system=True)
    assert [e["kind"] for e in events] == ["system"]


def test_load_events_excludes_environment_context_block(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [
            {
                "type": "response_item",
                "timestamp": "t1",
                "payload": {"type": "message", "role": "user", "content": "<environment_context>cwd=/tmp</environment_context>"},
            }
        ],
    )
    _, events = ese.load_events(session, max_chars=220, include_system=False)
    assert events == []


def test_load_events_captures_function_call_with_namespace(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [
            {
                "type": "response_item",
                "timestamp": "t1",
                "payload": {"type": "function_call", "name": "read_file", "namespace": "fs", "arguments": {"path": "a.txt"}},
            }
        ],
    )
    _, events = ese.load_events(session, max_chars=220, include_system=False)
    assert events[0]["kind"] == "tool:fs.read_file"
    assert json.loads(events[0]["summary"]) == {"path": "a.txt"}


def test_load_events_captures_generic_call_suffix(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [{"type": "response_item", "timestamp": "t1", "payload": {"type": "web_search_call", "name": "web_search", "arguments": "query"}}],
    )
    _, events = ese.load_events(session, max_chars=220, include_system=False)
    assert events[0]["kind"] == "tool:web_search"
    assert events[0]["summary"] == "query"


def test_load_events_skips_malformed_json_and_blank_lines(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    session.write_text(
        '{"broken": \n\n'
        '{"type": "response_item", "timestamp": "t1", "payload": {"type": "message", "role": "user", "content": "ok"}}\n',
        encoding="utf-8",
    )
    _, events = ese.load_events(session, max_chars=220, include_system=False)
    assert [e["summary"] for e in events] == ["ok"]


# --- render() ------------------------------------------------------------------


def test_render_includes_meta_and_escapes_pipes(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    meta = {"id": "abc", "timestamp": "t0", "cwd": "/tmp"}
    events = [{"time": "t1", "kind": "user", "summary": "a | b"}]
    output = ese.render(session, meta, events)
    assert f"Session file: `{session}`" in output
    assert "Thread id: `abc`" in output
    assert "a \\| b" in output


# --- latest_session() -----------------------------------------------------------


def test_latest_session_raises_when_no_sessions_found(monkeypatch):
    monkeypatch.setattr(ese, "DEFAULT_ROOTS", [])
    with pytest.raises(SystemExit):
        ese.latest_session()


# --- CLI (subprocess, end to end) -----------------------------------------------


def test_cli_writes_expected_markdown_to_output_file(tmp_path):
    session = tmp_path / "rollout-test.jsonl"
    _write_jsonl(
        session,
        [
            {"type": "session_meta", "payload": {"id": "abc", "timestamp": "t0", "cwd": "/tmp"}},
            {"type": "response_item", "timestamp": "t1", "payload": {"type": "message", "role": "user", "content": "hi"}},
        ],
    )
    out = tmp_path / "out.md"
    script = REPO_ROOT / "scripts" / "extract_session_events.py"
    result = subprocess.run(
        [sys.executable, str(script), "--session", str(session), "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    content = out.read_text(encoding="utf-8")
    assert "Thread id: `abc`" in content
    assert "| t1 | user | hi |" in content


def test_cli_errors_on_missing_session_file(tmp_path):
    script = REPO_ROOT / "scripts" / "extract_session_events.py"
    missing = tmp_path / "does-not-exist.jsonl"
    result = subprocess.run(
        [sys.executable, str(script), "--session", str(missing)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "not found" in result.stderr
