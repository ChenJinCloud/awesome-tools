---
name: x-post-3x4-capture
description: Capture a rendered X post as clear 3:4 portrait PNGs for Xiaohongshu, preserving the native post appearance and splitting long content at paragraph boundaries.
---

# X Post 3:4 Capture

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

Use this skill when the user supplies an X post URL or asks for native X screenshots suitable for Xiaohongshu. Capture the actual rendered post. Keep the original author, avatar, handle, text, images, timestamp, and displayed metrics. Do not add a frame, cover page, title, watermark, page number, or decorative background. Do not recreate the post using SVG, HTML templates, or image generation.

Read [the capture guide](references/capture-guide.md) before measuring or capturing. A browser capable of inspecting layout and capturing precise regions is required; this package contains instructions, not a standalone browser runner.

## Workflow

1. Use the user's chosen browser. Otherwise use the available browser workflow; prefer Ego Lite when available. Verify the target post is visible, expand truncated text, and wait for fonts and images. Login or verification must be completed by the user. Reuse their verified window and inspect the actual post again.
2. Record the original text and order. Temporarily adjust the native post layout to the defaults below, retaining its font family and colors. Measure actual text margins because X's layout can change.
3. Fill each page with as many complete paragraphs or images as fit. Choose the last eligible boundary within the page capacity. Do not distribute content evenly across a predetermined number of pages. The first image contains the author and starts the body immediately; the final image includes the actual post footer.
4. Capture native page regions at 2× density, then restore all temporary styles and viewport changes even if capture fails.
5. Verify text equality, complete paragraph or line coverage, image coverage, and actual PNG dimensions. Visually inspect every image. Deliver numbered PNGs, a ZIP containing only finished PNGs, and a first-image preview.

## Default layout

| Setting | CSS pixels | PNG pixels |
| --- | --- | --- |
| Image | 600 × 800 | 1200 × 1600 |
| Device pixel ratio | 2 | — |
| Native post column, including its padding | About 580 | About 1160 |
| Actual body margin on each side | About 26 | About 52 |
| Body font size | 16 | 32 |
| Body line height | 20 | 40 |
| Top allowance | 12 | 24 |
| Maximum content height per image | 780 | 1560 |

Honor explicit user overrides. Keep the portrait 3:4 ratio. A paragraph longer than one page may split between complete lines with a small overlap; verify coverage. Handle an oversized image separately without silently cropping away its content. Do not shrink the entire post to force a page count.

## Completion evidence

Save a local `capture-manifest.json` with the input and actual URLs, capture time, browser, viewport, density, layout settings, crop ranges, output dimensions, and text/coverage check results. Put failed captures in a separate debug directory. Save revisions to a new output directory.

A loading screen, authentication overlay, or post hidden behind verification is an incomplete capture. Report the observed blocker and preserve the browser for recovery. Never hide authentication overlays to make a screenshot appear successful. This skill does not authorize posting to Xiaohongshu or X.
