---
name: chenjin-brand-xiaohongshu
description: Design or revise Chen Jin's original Xiaohongshu 3:4 portrait brand cards with HTML/CSS, preserving editable sources and exporting PNG. Use for personal introductions, viewpoints, tutorials, and project reflections that need layout design. Native X-post capture belongs to the screenshot workflow.
metadata:
  version: "0.1.0"
  updated: "2026-10-15"
---

# Chenjin Brand Cards

Produce readable 3:4 portrait cards in Chen Jin's established visual style. Default to a 1080 × 1440 CSS-pixel canvas. Export PNG and keep editable HTML/CSS plus structured content. Use the user's latest directions over this baseline.

Read [the visual baseline](references/visual-system.md) before designing. Read [the schema](references/input-schema.md) when using the bundled renderer.

## Decisions

- Identify the page's main job and reading order. A portrait and four results suit a personal introduction; ordinary content pages need their own structure.
- Preserve supplied names, metric qualifiers, dates, and attribution. Keep real photos unchanged; crop only when the subject remains intact. Example metrics are sample data, not reusable personal facts.
- Use warm moon-white `#F2F1EC`, dark teal `#223939`, and muted jade `#527C6D`. Soft cards and restrained shadows create depth. Colored round bullets clarify parallel items.
- Prefer direct headings. The introduction template goes straight from the project/role heading to the result cards; it omits the redundant label “增长现场”.
- The full-width dark top bar is the default series accent. Keep type legible at phone size and reduce decorative labels. Use local fonts; inspect Chinese glyphs in the actual PNG.
- For a content series, place real content below the first title and paginate at natural boundaries. Add pages when needed; do not shrink all text or mechanically slice a long screenshot.

## Build

Create a new output directory for each revision. The bundled renderer supports an `intro` template based on the approved card and a `content` template for explicit page layouts. Adapt the HTML/CSS for content that needs another arrangement; the template is a starting point.

```bash
python3 scripts/render.py examples/intro.zh-CN.json --output /path/to/new-output
python3 scripts/render.py examples/content.zh-CN.json --output /path/to/new-output
```

Use `--sources-only` to generate HTML without a browser, `--portrait /path/to/photo.jpg` to override the introduction portrait, or `--scale 2` to render 2160 × 2880 PNGs directly from HTML.

The renderer needs Python 3 and `ego-browser` for PNG export. If an Ego Lite TaskSpace already exists for this request, pass `--space ID`; use `--keep-space` while iterating. A failed export records its space ID for recovery. Reuse that space after a failure. Follow the browser's ownership and handoff state. If browser capture remains unavailable, deliver the sources and report the export failure; use another renderer only when the current task's routing instructions allow it.

The renderer checks bounds and writes a report. It stops on overflowing content rather than silently reducing the font size. Repartition the pages or adjust the layout, then export again.

## Review and deliver

Open every exported PNG. Check Chinese glyphs, photo crop, bullet alignment, section gaps, and metric labels. Compare text to the supplied content, including `+` signs and timeframe qualifiers. Fix the sources and rerender when needed.

Show the result and provide PNG and editable HTML links. Preserve the previous revision. Creating the cards does not authorize publishing them to Xiaohongshu or changing account settings.
