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

For translated or reposted blogs, show the H1 title, then the cover image, then two muted, right-aligned lines: publication date · reading time · category; original author · verified organization and role. Use source facts, never a fixed author identity. The renderer recognizes either `H1 → metadata → author → cover` or `H1 → cover → metadata → author` at the start of a Markdown file and emits this layout. The metadata line must begin with a Chinese year such as `2026 年`, and the author line must begin with `原作者：`.

## Blog translation and reposting

When asked to translate or repost a blog, preserve the original article and its provenance, then create a separate Chinese Markdown draft. The layout script does not translate content.

1. **Inspect the source.** Record the original URL, title, publication date, author, verified affiliation and role, and category. Mark an estimated reading time as approximate; do not invent missing facts. Compare the translated draft against the source for structure, numbers, terminology, quotations, links, and references. Resolve extraction placeholders such as `__WPA_HOLD_...`; none may appear in the finished article.
2. **Collect every image.** Inventory the cover and all in-article figures in source order. Download the actual assets, retain the URL-to-file mapping and captions or alt text, and confirm that each downloaded file is a usable image. A candidate URL alone is not a downloaded asset. Keep the figures at their original positions in the draft.
3. **Translate faithfully.** Preserve arguments, figures, qualifications, attribution, and the author's voice. Check uncertain technical terms against the source; label editorial additions as such. Retain the author's social links and source links to papers, code, and other references.
4. **Use the restrained layout.** Start with title, cover, then two muted right-aligned metadata lines. Keep the body primarily headings, paragraphs, lists, and original images; avoid proliferating cards and decoration. If a tinted “太长不看” summary is requested, use one subtle block there only.
5. **Compact the sources.** Close with “原文与参考资料”: original article first, then numbered references in source order. Put author, outlet, and year on the first line; place the complete original title on a smaller muted second line; use thin separators without repeated bright underlines. Preserve working URLs for papers and code. In Markdown, use a `## 参考资料` list followed by `## 原文链接` and one standalone Markdown link; for recognized blog drafts, the renderer formats these as one compact section. WeChat may sanitize links, so set the original-source link separately in the editor when needed and inspect its preview.
6. **Deliver according to authorization.** Inspect the local HTML for its cover, every figure, attribution, references, and stray placeholders. If asked to sync a draft, upload all images, set the cover and original-source link, and verify the WeChat preview and draft state. Publish only when authorized. An editor's note, column introduction, personal contact, or CTA belongs to an article only when requested; never hardcode one article's author, company, or contact into the general template.

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
