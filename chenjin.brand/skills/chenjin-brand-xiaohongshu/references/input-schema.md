# Renderer input

[English](input-schema.md) | [简体中文](input-schema.zh-CN.md)

Run commands from the skill directory. The renderer uses Python's standard library. PNG export also needs an installed and available `ego-browser` CLI and its browser runtime.

## Introduction

Start from [intro.en.json](../examples/intro.en.json) or [intro.zh-CN.json](../examples/intro.zh-CN.json).

- `mode`: `intro`.
- `name`, `role`, `project`: required strings. Use `\n` for intentional line breaks.
- `name_size`: optional name size in CSS pixels, default `136`; the English example uses `104` to fit its longer name.
- `hello`, `summary`, `topics_title`, `footer`, `brand`: optional copy. Default brand signature is `chenjin.io`.
- `portrait`: optional local image path, resolved relative to the input JSON. With no portrait, the renderer uses its intentional placeholder. `--portrait` overrides the input path. Remote image URLs are not downloaded.
- `portrait_alt`: optional image description.
- `metrics`: exactly four objects with `value` and `label`. A label can contain `\n`. Treat example values as layout demonstration data.
- `topics`: one to three strings.

The template supports this amount of content. For a longer biography or more metrics, design another layout or split the content into pages.

## Content pages

Start from [content.en.json](../examples/content.en.json) or [content.zh-CN.json](../examples/content.zh-CN.json).

- `mode`: `content`.
- `pages`: a nonempty list, each with a `title` and nonempty `blocks`.
- `brand`, `footer`: optional shared footer copy. Multiple pages add a page count automatically.

Block types:

| Type | Fields | Treatment |
| --- | --- | --- |
| `paragraph` | `text` | Readable body paragraph |
| `heading` | `text` | Subheading within the body |
| `bullets` | `items`: string list | Muted jade round bullets |
| `quote` | `text` | One emphasis block per page |
| `image` | `path`, optional `alt`, `caption` | Local image shown with `contain`; text and diagrams remain intact |

Keep all original facts and content while dividing the input into explicit pages. Overflow stops PNG export and is reported; repartition the pages or change the layout before rerendering.

## Commands and output

```bash
python3 scripts/render.py examples/intro.zh-CN.json --output /path/to/new-output
python3 scripts/render.py examples/content.en.json --output /path/to/another-output --scale 2
python3 scripts/render.py examples/intro.zh-CN.json --output /path/to/source-preview --sources-only
```

Use a fresh output directory. A nonempty destination is refused to preserve earlier revisions. Outputs contain `source.json`, a CSS copy, editable `card-01.html` files with embedded local images, an `index.html` preview, and `render-report.json`. Successful export adds matching PNGs. HTML sources embed the CSS, so an individual card remains portable.

`--scale 1` produces 1080 × 1440 PNGs; `--scale 2` renders the HTML at double size for 2160 × 2880 PNGs. It does not enlarge a previously exported bitmap. Inspect the actual output dimensions and every PNG before delivering.

For iterative browser work, use `--keep-space`; the renderer prints `SPACE_ID=...`. Continue with `--space ID` and a new output directory. A successful run closes the TaskSpace unless `--keep-space` is passed. A failed run retains the space for inspection. Close it when the task is complete through the documented browser API. If the user takes control, hand off and wait for them before resuming.

The export report states `sources-only`, `exported`, or `failed`. It records content hashes and browser layout checks. Review the PNG visually after `exported`; the checks do not judge composition or confirm the source facts.
