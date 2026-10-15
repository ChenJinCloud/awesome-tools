# Visual baseline v0.1

[English](visual-system.md) | [简体中文](visual-system.zh-CN.md)

This baseline records the user's choices from the personal introduction card refined on 2026-10-15. Apply its palette and visual treatment across original brand cards, and choose the layout for each piece of content.

| Token | Value | Use |
| --- | --- | --- |
| Paper | `#F2F1EC` | Warm moon-white canvas |
| Ink | `#223939` | Dark teal text and top bar |
| Jade | `#527C6D` | Metrics, bullet points, small accents |
| Muted | `#6B7972` | Secondary copy |
| Card | `#FBFCF8` | Raised result cards |
| Line | `#D8DFD5` | Subtle footer rule |

## Type and spacing

Use a clear local Chinese sans-serif with moderate heading weights. The introduction example uses PingFang SC, with local CJK fallbacks. Metrics use Helvetica Neue or another clear local sans-serif; the small domain signature may use Georgia. Font availability varies by machine. Add an authorized local font when the available fallbacks cannot render the content.

On the 1080 × 1440 canvas, the introduction has 76 px side margins, a 136 px name, a 38 px role, 29 px topic copy, 48 px metrics, and 20 px metric labels. These values belong to this layout. The content template uses a 62 px title and 34 px body text. Keep full paragraphs readable at phone width; paginate rather than treating these sizes as limits for every layout.

## Established treatments

- Full-width 18 px dark teal top bar.
- Soft result cards with 18 px corners and a low-contrast shadow. Each card contains one number and its label. Keep time ranges and `+` qualifiers.
- Muted jade round bullets for parallel topics; align them with the first line of text.
- Natural portraits with restrained cropping, 26 px corners, and soft depth. Preserve the supplied face and lighting.
- Direct project headings without empty section labels. The user explicitly removed “增长现场”.

The left-copy/right-portrait composition and four equal result cards suit the introduction. Use suitable text, image, or chart layouts for other subjects. Page numbers help a multi-page sequence; a single introduction card does not require one.

## References and what was adopted

- [chenjin.io](https://chenjin.io/): moon-white and teal identity, restrained reading experience.
- [Gingiris](https://gingiris.com/zh): prominent result values with clear metric labels.
- [Ambi](https://www.ambi.ai/en): warm paper, lighter type, natural imagery, and soft depth.

These are visual references, not bundled designs. The package does not include their fonts, images, logos, or website code. The user's original card and later corrections determine this baseline.
