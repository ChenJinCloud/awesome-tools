# 公众号排版

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个无额外依赖的 Codex Skill，可将 Markdown 转换为适合复制到微信公众号编辑器的内联 CSS HTML。默认配色沿用 chenjin.io 的视觉风格。

## 安装

将此文件夹复制到你的 Codex Skills 目录，或直接在本仓库使用。如需其他视觉风格，可修改 `scripts/render_wechat.py` 中的颜色常量。

## 使用

从仓库根目录运行：

```bash
python3 skills/wechat-public-account-format/scripts/render_wechat.py "/path/to/article.md"
```

默认在 Markdown 原稿旁生成 `<原文件名>-公众号版.html`；可通过 `--output` 指定位置，通过 `--title` 覆盖标题。

排版规则见 [SKILL.zh-CN.md](SKILL.zh-CN.md)，英文版见 [SKILL.md](SKILL.md)。

## 边界

脚本只生成本地 HTML，不上传图片、不保存公众号草稿，也不发表文章。公众号可能清洗粘贴的 HTML 和正文链接；请在编辑器中检查预览，并重新上传本地图片。
