---
name: wechat-public-account-format
description: Convert local Markdown to chenjin.io-styled, inline-CSS HTML for the WeChat Official Account editor.
---

# WeChat Official Account Formatting

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

Convert a local Markdown draft into an HTML article that can be copied into the WeChat Official Account editor. Use it for long-form articles, tutorials, retrospectives, knowledge cards, and Markdown tables.

## Output

- Do not modify or overwrite the source Markdown.
- By default, write an HTML file next to it named `<source-stem>-公众号版.html`.
- Use inline CSS only: no external stylesheets, JavaScript, or web fonts.
- Generate a local article by default. Only sync it to a WeChat draft when the user explicitly asks for that separate action. Never treat a generated file, draft, preview, and published article as the same state.

## Style

The default palette follows the chenjin.io visual style:

- pale mint page background `#EFF8F4`;
- dark teal heading and body `#223939`;
- primary accent `#2F8E7D` and dark accent `#2F7E6F`;
- pale green cards `#E6F1EB`, soft green blocks `#EEF6F1`, and borders `#D0E1D8`;
- rose `#B35F6B` and warm brown `#A8754A` for secondary labels.

Default font sizes: body, paragraphs, and list items 14px; H1 26px; H2 20px; H3 17px; table text 12px; category labels 13px.

Set font size on each `p` and `li` rather than depending on inheritance. Set table font size on each `th` and `td`. Render paragraphs beginning with `**核心动作：**` as single-cell highlighted callouts. Keep tables readable and avoid complex nested layouts.

## Run

From the repository root:

```bash
python3 skills/wechat-public-account-format/scripts/render_wechat.py \
  "/path/to/article.md"
```

Choose a destination or override the article title if needed:

```bash
python3 skills/wechat-public-account-format/scripts/render_wechat.py \
  "/path/to/article.md" \
  --output "/path/to/article-公众号版.html" \
  --title "Article title"
```

The dependency-free renderer supports headings, paragraphs, emphasis, inline code, links, images, ordered and unordered lists, blockquotes, horizontal rules, fenced code, and Markdown tables.

## Boundaries

- Format the source; do not silently rewrite its claims, translate it, or add opinions.
- Preserve image references. Local image paths usually need to be uploaded again inside the WeChat editor.
- Preserve safe links, but expect WeChat to sanitize pasted HTML and possibly remove outgoing links from article body. Check the platform preview and set the original-source link separately when appropriate.
- If WeChat changes font sizes on paste, adjust them in the editor and inspect the preview.
- Do not publish an article unless the user specifically authorized publication.

## Review

1. Confirm the HTML exists and the source Markdown is unchanged.
2. Check that the HTML has no scripts, external CSS, or web-font dependencies.
3. Check that headings, callouts, tables, quotes, references, and image positions remain readable.
4. Open the HTML locally before copying it into a WeChat draft, then inspect the platform preview after pasting.
