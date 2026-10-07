# Native X Post Capture

[English](capture-guide.md) | [简体中文](capture-guide.zh-CN.md)

Capture the loaded X page directly. The default layout is defined in [SKILL.md](../SKILL.md). Native padding can change; measure body bounds instead of assuming the column width equals text width. Preserve the native font family and colors while temporarily adjusting column width, font size, and line height.

## Browser and access recovery

Prefer Ego Lite and its TaskSpace workflow when available. Use Chrome when the user requests it or the preferred integration cannot perform the required capture. Use an existing connected CDP session when appropriate. Do not change the user's browser security settings to enable control.

If a separate Chrome debugging window is necessary, use a temporary profile and bind the debugging port to loopback only. Select the target `page` from the local `/json/list` response and connect to its `webSocketDebuggerUrl`; do not attach to extensions or background pages or copy login credentials. Reuse a window where the user has already completed verification.

After verification, check the actual URL, target article, and visible body. A title alone does not prove access. For a blank or loading page, navigate once again in the same page and wait for the body. If it still fails, report the actual state and preserve the window for recovery. Avoid repeated new windows. Login and CAPTCHA are user steps; hidden content behind verification is not ready for capture.

## Measurement and pagination

Read and record the original text and images before modifying styles. Identify the target `article` by its author and status link when multiple posts appear. Common body selectors include `[data-testid="tweetText"]` and body `[dir="auto"]`; inspect the actual DOM and exclude translation buttons and author labels.

Save the original inline styles of every modified element. Apply the layout settings, wait for `document.fonts.ready`, image decoding, and settled layout, then measure text with `Range.getClientRects()` or `getBoundingClientRect()`. Build a character-offset map across text nodes; do not assume a single text node. Preserve single line breaks and identify paragraphs separated by blank lines. Include images as indivisible blocks.

Use the midpoint of the gap between complete blocks as a candidate boundary. All values below are measured document coordinates; `start` includes the first-page author area, and `end` includes the real post footer.

```javascript
const capacity = 780;
const ranges = [];
let cursor = start;
while (end - cursor > capacity) {
  const cut = boundaries.filter(y => y > cursor && y - cursor <= capacity).at(-1);
  if (cut === undefined) throw new Error("Block exceeds page capacity / 单个区块超过截图容量");
  ranges.push({ start: cursor, end: cut });
  cursor = cut;
}
ranges.push({ start: cursor, end });
```

Sort `boundaries` in ascending order. Choose the last boundary that fits each time, rather than balancing pages. If a paragraph alone exceeds capacity, split at complete line boundaries with a small overlap and verify line coverage. Arrange oversized images separately. Preserve all text and image content; never cut glyphs or shrink the entire post to reach a fixed page count.

## Capture and restoration

Center each 600 × 800 CSS-pixel region horizontally on the post column. Start 12 CSS pixels above its range. Capture at device pixel ratio 2 to produce 1200 × 1600 PNGs directly; do not stretch exported images.

To prevent the next page's content from entering unused space on the current image, temporarily apply `clip-path: inset(...)` to the post for the current range. Remaining space uses the native page background. Ordinary navigation, recommendations, and controls may be temporarily hidden. Preserve the author, body, images, and actual metrics. Authentication and security overlays must remain visible until the user resolves them. Do not add a board or frame.

With Chrome CDP, use `Emulation.setDeviceMetricsOverride` for viewport and density and `Page.captureScreenshot` with a `clip` and `captureBeyondViewport: true`. Restore styles and call `Emulation.clearDeviceMetricsOverride` in `finally`, including on errors.

## Output checks

Compare the original and adjusted body strings, including order and line breaks. Every paragraph's complete bounds must belong to a capture range; verify line coverage separately for split paragraphs. Check image coverage, the first-page author, and final-page footer. Inspect each PNG for overlays, missing characters, and partial lines.

Verify actual dimensions of 1200 × 1600. If unused space on an earlier page is larger than the next complete block, repaginate. Natural whitespace on the final page is acceptable. Move incomplete screenshots to a debug directory rather than delivering them.

Save `capture-manifest.json` locally with input URL, actual URL, capture time, browser, viewport, pixel ratio, column width, text styles, crop ranges, output dimensions, and text/coverage verification results. Deliver ordered PNGs, a ZIP containing only finished PNGs, and a preview of the first image.
