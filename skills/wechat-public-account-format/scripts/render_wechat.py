#!/usr/bin/env python3
"""Render Markdown into copy-friendly WeChat Official Account HTML.

This is intentionally dependency-free so the skill works on a local machine
without a package install or network request.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


PALETTE = {
    "page_bg": "#EFF8F4",
    "headline": "#223939",
    "text": "#405B5B",
    "accent": "#2F8E7D",
    "accent_dark": "#2F7E6F",
    "card": "#E6F1EB",
    "soft": "#EEF6F1",
    "border": "#D0E1D8",
    "rose": "#B35F6B",
    "warm": "#A8754A",
}

BODY_SIZE = 14
H1_SIZE = 26
H2_SIZE = 20
H3_SIZE = 17
TABLE_SIZE = 12
LABEL_SIZE = 13


def esc(value: str, quote: bool = False) -> str:
    return html.escape(value, quote=quote)


def safe_url(value: str) -> str:
    value = value.strip()
    if re.match(r"^(https?://|mailto:|/|\.{0,2}/|[A-Za-z0-9_.-]+/)", value):
        return esc(value, quote=True)
    return "#"


def inline(text: str) -> str:
    """Render the small inline-Markdown subset useful for article copy."""
    held: list[str] = []

    def hold(value: str) -> str:
        token = f"__WPA_HOLD_{len(held)}__"
        held.append(value)
        return token

    text = text.replace("<br>", "__WPA_BR__").replace("<br/>", "__WPA_BR__").replace("<br />", "__WPA_BR__")

    image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")

    def image_repl(match: re.Match[str]) -> str:
        alt = esc(match.group(1), quote=True)
        src = safe_url(match.group(2))
        title = match.group(3)
        title_attr = f' title="{esc(title, quote=True)}"' if title else ""
        return hold(
            f'<img src="{src}" alt="{alt}"{title_attr} '
            'style="display:block;max-width:100%;height:auto;margin:20px auto;">'
        )

    text = image_pattern.sub(image_repl, text)

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")

    def link_repl(match: re.Match[str]) -> str:
        label = inline(match.group(1))
        href = safe_url(match.group(2))
        title = match.group(3)
        title_attr = f' title="{esc(title, quote=True)}"' if title else ""
        return hold(f'<a href="{href}"{title_attr} style="color:{PALETTE["accent"]};text-decoration:underline;">{label}</a>')

    text = link_pattern.sub(link_repl, text)
    text = esc(text, quote=False)
    text = text.replace("__WPA_BR__", "<br>")

    code_tick = chr(96)
    text = re.sub(
        re.escape(code_tick) + r"([^" + re.escape(code_tick) + r"]+)" + re.escape(code_tick),
        lambda match: f'<code style="padding:2px 5px;background-color:{PALETTE["soft"]};color:{PALETTE["headline"]};">{match.group(1)}</code>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"<em>\1</em>", text)

    for index, value in enumerate(held):
        text = text.replace(f"__WPA_HOLD_{index}__", value)
    return text


def split_table_row(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped_pipe = False
    for char in row:
        if char == "|" and not escaped_pipe:
            cells.append("".join(current).strip())
            current = []
            continue
        if char == "\\" and not escaped_pipe:
            escaped_pipe = True
            current.append(char)
            continue
        escaped_pipe = False
        current.append(char)
    cells.append("".join(current).strip())
    return cells


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return len(cells) >= 1 and all(re.match(r"^:?-{3,}:?$", cell.replace(" ", "")) for cell in cells)


def style_heading(level: int) -> str:
    sizes = {1: H1_SIZE, 2: H2_SIZE, 3: H3_SIZE}
    if level == 1:
        return (
            f"margin:0 0 18px;color:{PALETTE['headline']};font-size:{sizes[level]}px;"
            "line-height:1.35;font-weight:700;letter-spacing:.01em;"
        )
    if level == 2:
        return (
            f"margin:34px 0 14px;padding-bottom:8px;border-bottom:2px solid {PALETTE['accent']};"
            f"color:{PALETTE['headline']};font-size:{sizes[level]}px;line-height:1.45;font-weight:700;"
        )
    return (
        f"margin:24px 0 10px;color:{PALETTE['accent']};font-size:{sizes[level]}px;"
        "line-height:1.5;font-weight:700;"
    )


def render_callout(content: str) -> str:
    rendered = inline(content)
    rendered = rendered.replace(
        "<strong>核心动作：</strong>",
        f'<strong style="color:{PALETTE["accent_dark"]};font-size:{BODY_SIZE}px;">核心动作：</strong>',
        1,
    )
    rendered = rendered.replace(
        "<strong>核心动作:</strong>",
        f'<strong style="color:{PALETTE["accent_dark"]};font-size:{BODY_SIZE}px;">核心动作:</strong>',
        1,
    )
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="width:100%;border-collapse:collapse;margin:0 0 28px;">'
        "<tbody><tr>"
        f'<td style="padding:16px 18px;border-left:4px solid {PALETTE["accent"]};'
        f'background-color:{PALETTE["card"]};color:{PALETTE["text"]};'
        f'font-size:{BODY_SIZE}px;line-height:1.85;">'
        f'<span style="font-size:{BODY_SIZE}px;line-height:1.85;color:{PALETTE["text"]};">'
        f"{rendered}"
        "</span></td></tr></tbody></table>"
    )


def render_blockquote(lines: list[str]) -> str:
    content = " ".join(line.lstrip()[1:].strip() if line.lstrip().startswith(">") else line.strip() for line in lines)
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="width:100%;border-collapse:collapse;margin:22px 0;">'
        "<tbody><tr>"
        f'<td style="padding:14px 16px;border-left:4px solid {PALETTE["accent"]};'
        f'background-color:{PALETTE["soft"]};color:{PALETTE["text"]};'
        f'font-size:{BODY_SIZE}px;line-height:1.85;">'
        f'<span style="font-size:{BODY_SIZE}px;color:{PALETTE["text"]};">{inline(content)}</span>'
        "</td></tr></tbody></table>"
    )


def table_cell_html(cell: str) -> str:
    rendered = inline(cell)
    label_colors = (
        ("Strengths（优势）", PALETTE["accent"]),
        ("Weaknesses（劣势）", PALETTE["rose"]),
        ("Opportunities（机会）", "#668F77"),
        ("Threats（威胁）", PALETTE["warm"]),
    )
    for label, color in label_colors:
        if label in cell:
            rendered = rendered.replace(
                "<strong>",
                f'<strong style="color:{color};font-size:{LABEL_SIZE}px;">',
                1,
            )
            break
    return rendered


def render_table(header: list[str], rows: list[list[str]]) -> str:
    output = [
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="width:100%;border-collapse:collapse;table-layout:fixed;margin:0 0 26px;'
        f'font-size:{TABLE_SIZE}px;line-height:1.75;color:{PALETTE["text"]};">',
        "<thead><tr>",
    ]
    for cell in header:
        output.append(
            f'<th style="padding:10px 8px;border:1px solid {PALETTE["border"]};'
            f'background-color:{PALETTE["card"]};color:{PALETTE["headline"]};'
            f'text-align:left;font-weight:700;font-size:{TABLE_SIZE}px;">{inline(cell)}</th>'
        )
    output.append("</tr></thead><tbody>")
    for row in rows:
        output.append("<tr>")
        padded = row + [""] * max(0, len(header) - len(row))
        for cell in padded[: len(header)]:
            output.append(
                f'<td style="padding:10px 8px;border:1px solid {PALETTE["border"]};'
                f'vertical-align:top;font-size:{TABLE_SIZE}px;">'
                f'<span style="font-size:{TABLE_SIZE}px;color:{PALETTE["text"]};">{table_cell_html(cell)}</span></td>'
            )
        output.append("</tr>")
    output.append("</tbody></table>")
    return "".join(output)


def list_match(line: str) -> re.Match[str] | None:
    return re.match(r"^(\s*)([-+*]|\d+\.)\s+(.*)$", line)


def render_list_at(lines: list[str], start: int) -> tuple[str, int]:
    first = list_match(lines[start])
    if not first:
        return "", start
    base_indent = len(first.group(1).replace("\t", "    "))
    ordered = first.group(2)[0].isdigit()
    tag = "ol" if ordered else "ul"
    output = [
        f'<{tag} style="margin:0 0 20px;padding-left:1.45em;font-size:{BODY_SIZE}px;'
        f'line-height:1.85;color:{PALETTE["text"]};">'
    ]
    index = start
    while index < len(lines):
        match = list_match(lines[index])
        if not match:
            if lines[index].strip() == "":
                index += 1
                continue
            break
        indent = len(match.group(1).replace("\t", "    "))
        current_ordered = match.group(2)[0].isdigit()
        if indent < base_indent or (indent == base_indent and current_ordered != ordered):
            break
        if indent > base_indent:
            nested, index = render_list_at(lines, index)
            if output and output[-1].endswith("</li>"):
                output[-1] = output[-1][:-5] + nested + "</li>"
            continue
        content = match.group(3).strip()
        output.append(
            f'<li style="margin:7px 0;font-size:{BODY_SIZE}px;line-height:1.85;color:{PALETTE["text"]};">'
            f"{inline(content)}</li>"
        )
        index += 1
    output.append(f"</{tag}>")
    return "".join(output), index


def fence_match(line: str) -> re.Match[str] | None:
    backticks = chr(96) * 3
    return re.match(r"^\s*~~~(.*)$", line) or re.match(r"^\s*" + re.escape(backticks) + r"(.*)$", line)


def render_markdown(source: str, title_override: str | None = None) -> tuple[str, list[str]]:
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    warnings: list[str] = []
    parts: list[str] = []
    title = title_override or ""
    index = 0

    if lines and lines[0].strip() == "---":
        closing = next((pos for pos in range(1, len(lines)) if lines[pos].strip() == "---"), None)
        if closing is not None:
            lines = lines[closing + 1 :]

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        fence = fence_match(line)
        if fence:
            marker = "~~~" if line.lstrip().startswith("~~~") else chr(96) * 3
            language = fence.group(1).strip()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith(marker):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            lang_attr = f' data-language="{esc(language, quote=True)}"' if language else ""
            code = esc("\n".join(code_lines))
            parts.append(
                f'<pre{lang_attr} style="margin:22px 0;padding:14px;overflow-x:auto;'
                f'border:1px solid {PALETTE["border"]};border-radius:6px;background-color:{PALETTE["soft"]};'
                f'color:{PALETTE["headline"]};font-size:{TABLE_SIZE}px;line-height:1.7;">{code}</pre>'
            )
            continue

        heading = re.match(r"^\s*(#{1,3})\s+(.+?)\s*#*\s*$", line)
        if heading:
            level = len(heading.group(1))
            content = heading.group(2).strip()
            if level == 1 and not title:
                title = re.sub(r"[*_]", "", content)
            parts.append(f'<h{level} style="{style_heading(level)}">{inline(content)}</h{level}>')
            index += 1
            continue

        if index + 1 < len(lines) and "|" in line and is_table_separator(lines[index + 1]):
            header = split_table_row(line)
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                rows.append(split_table_row(lines[index]))
                index += 1
            if any("![" in cell for row in rows for cell in row):
                warnings.append("表格中包含图片；粘贴到公众号后可能需要重新上传。")
            parts.append(render_table(header, rows))
            continue

        if re.match(r"^\s*(---+|\*\s*\*\s*\*|___+)\s*$", line):
            parts.append(f'<hr style="margin:34px 0;border:0;border-top:1px solid {PALETTE["border"]};">')
            index += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and (lines[index].strip().startswith(">") or not lines[index].strip()):
                if lines[index].strip():
                    quote_lines.append(lines[index])
                index += 1
            parts.append(render_blockquote(quote_lines))
            continue

        if list_match(line):
            rendered, index = render_list_at(lines, index)
            parts.append(rendered)
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if (
                re.match(r"^\s*(#{1,3})\s+", candidate)
                or list_match(candidate)
                or candidate_stripped.startswith(">")
                or (index + 1 < len(lines) and "|" in candidate and is_table_separator(lines[index + 1]))
                or fence_match(candidate)
                or re.match(r"^\s*(---+|\*\s*\*\s*\*|___+)\s*$", candidate)
            ):
                break
            paragraph_lines.append(candidate_stripped)
            index += 1
        paragraph = " ".join(paragraph_lines)
        if paragraph.startswith("**核心动作：**") or paragraph.startswith("**核心动作:**"):
            parts.append(render_callout(paragraph))
        else:
            if "![" in paragraph:
                warnings.append("文中包含图片；本地路径或临时 URL 通常需要在公众号编辑器中重新上传。")
            parts.append(
                f'<p style="margin:0 0 14px;color:{PALETTE["text"]};'
                f'font-size:{BODY_SIZE}px;line-height:1.9;">{inline(paragraph)}</p>'
            )

    if not title:
        title = "未命名文章"
    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
</head>
<body style="margin:0;padding:0;background:{PALETTE['page_bg']};color:{PALETTE['headline']};font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;">
  <div role="article" style="box-sizing:border-box;max-width:677px;margin:0 auto;padding:28px 20px 48px;background:#FFFFFF;font-size:{BODY_SIZE}px;line-height:1.85;word-break:break-word;overflow-wrap:anywhere;">
    {''.join(parts)}
  </div>
</body>
</html>
"""
    return document, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Markdown to inline-style WeChat article HTML.")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("--output", type=Path, help="Output HTML path")
    parser.add_argument("--title", help="Override article title")
    args = parser.parse_args()

    source_path = args.input.expanduser().resolve()
    if not source_path.is_file():
        parser.error(f"Input file does not exist: {source_path}")
    if source_path.suffix.lower() != ".md":
        parser.error("Input file must have a .md extension")

    output_path = args.output.expanduser().resolve() if args.output else source_path.with_name(f"{source_path.stem}-公众号版.html")
    document, warnings = render_markdown(source_path.read_text(encoding="utf-8"), args.title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    print(f"Generated: {output_path}")
    for warning in sorted(set(warnings)):
        print(f"Warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
