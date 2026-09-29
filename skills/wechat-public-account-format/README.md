# WeChat Official Account Formatting

[English](README.md) | [简体中文](README.zh-CN.md)

A dependency-free Codex skill that converts Markdown into inline-CSS HTML for the WeChat Official Account editor. Its default colors follow the chenjin.io visual style.

## Install

Copy this folder to your Codex skills directory, or use it directly from this repository. Adjust the color constants in `scripts/render_wechat.py` if you want another visual style.

## Use

From the repository root:

```bash
python3 skills/wechat-public-account-format/scripts/render_wechat.py "/path/to/article.md"
```

The renderer writes `<source-stem>-公众号版.html` next to the Markdown source unless `--output` is supplied. Use `--title` to override the title.

See [SKILL.md](SKILL.md) for formatting rules and [the Chinese instructions](SKILL.zh-CN.md).

## Boundaries

The script creates a local HTML file. It does not upload images, save a WeChat draft, or publish an article. WeChat can sanitize pasted HTML and remove body links, so check the editor preview and upload local images there.
