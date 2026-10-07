# X 原帖截图

[English](capture-guide.md) | [简体中文](capture-guide.zh-CN.md)

此流程直接在已加载的 X 页面截图。普通正文的 SVG/HTML 渲染器不参与。

## 已验证的紧凑版参数

| 项目 | 浏览器 CSS 像素 | PNG 像素 |
| --- | --- | --- |
| 每张截图 | 600×800 | 1200×1600 |
| 像素密度 | 2 | — |
| 帖子列宽 | 约 580 | 约 1160 |
| 正文左右边距 | 约 26 | 约 52 |
| 正文字号 | 16 | 32 |
| 正文行距 | 20 | 40 |
| 顶部预留 | 12 | 24 |
| 单张内容最大高度 | 780 | 1560 |

列宽包含 X 自带的内边距。不同版本的 DOM 内边距可能变化，以实际正文边界测量为准。保持 X 原有字体族和颜色，仅临时调整列宽、字号及行距；不改变正文文本、段落顺序或真实数据。


## 浏览器与访问恢复

有 Ego Lite 时默认使用其 TaskSpace 工作流，相关 Skill 可用时遵循其操作说明。用户指定 Chrome 后，可使用 Chrome 控制工具；若控制接口不可用，可使用已连接的 Chrome CDP。不要为了开启控制而修改用户的 Chrome 安全设置。

需要启动独立 Chrome 调试窗口时，使用独立的临时用户目录，并将调试端口仅绑定到本机。使用 Node.js 的 `fetch` 读取本机 `/json/list`，从中选择目标帖子的 `page`，通过其 `webSocketDebuggerUrl` 调用 CDP。不连接后台页或扩展页，不复制用户的登录凭据。用户已经完成验证的窗口应复用。

验证完成后检查页面 URL、实际文章节点及可见正文，不能只依据标题或用户说“已完成”。空白页或 Loading 可在同一页面重新导航一次并等待正文。仍失败就报告实际状态，保留窗口供用户恢复，不连续开新窗口。登录和验证码由用户完成，原帖在验证遮罩后存在也不等于截图可用。

## 测量与分页

先读取原帖全文及图片，记录未经调整的正文。目标 `article` 必须对应输入 URL；页面有多个帖子时，通过作者与状态链接确定目标。正文常见选择器为 `[data-testid="tweetText"]`，已验证的另一版 DOM 使用正文 `[dir="auto"]`。根据实际页面确认选择器，不把翻译按钮或作者信息当成正文。

保存待修改元素的原始内联样式，再调整列宽和正文参数。等待 `document.fonts.ready`、图片解码以及页面完成布局后测量。用 `Range.getClientRects()` 或 `getBoundingClientRect()` 测量正文文本的实际边界；多个文本节点要先建立字符偏移映射，不能假设正文只有一个文本节点。段落通常以空行分隔，原有单换行保留。配图也加入不可截断的区块范围。

将相邻完整区块之间的空隙中点作为候选分界。下面的算法用于已测量的文档坐标，`start` 包含首张作者区域，`end` 包含帖尾真实信息。

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

`boundaries` 必须按文档坐标升序排列。每次取容量内最后一个分界，不按总页数平均分配。某段或配图独自超过容量时，文字可在完整行之间分张并保留少量重叠；配图根据实际尺寸单独安排。不能删段落、截断字形或缩小整帖来凑页数。

## 截图与恢复

截图区域横向居中于帖子列，每张为 600×800 CSS px，纵向从区块起点上方 12px 开始。使用 2 倍像素密度直接生成 1200×1600 PNG，不拉伸已生成图片。

为防止下一页内容出现在本页剩余空间中，可以临时对原帖应用 `clip-path: inset(...)`，只显示当前区间；留白来自原生页面背景。导航、推荐及普通界面控件可临时隐藏。作者、正文、配图及实际数据必须保留；登录或安全验证遮罩不能作为普通界面隐藏。裁切不创建底板或外框。

Chrome 可通过 `Emulation.setDeviceMetricsOverride` 设置视口及像素密度，使用 `Page.captureScreenshot` 的 `clip` 和 `captureBeyondViewport: true` 捕获文档区间。将样式恢复与 `Emulation.clearDeviceMetricsOverride` 放入 `finally`。发生错误也要恢复临时改动。

## 成品检查

逐段核对调整前后的正文字符串，确认措辞、顺序及空行保留。每个段落的完整文字边界必须被一个区间覆盖；超长段落按行分张时，单独验证行覆盖。检查图片区块、首张作者和末张真实信息，然后逐张查看 PNG，确认没有遮罩、漏字或半行文字。

检查每张 PNG 实际尺寸为 1200×1600。前页底部剩余空间大于下一完整区块的高度时，应重新分页；末页自然留白可以保留。把不完整截图移到调试目录，不交付为成品。

`capture-manifest.json` 保存原帖 URL、实际页面 URL和截图时间，记录浏览器、视口、像素密度、列宽、正文样式、区间及 PNG 尺寸，并记录正文一致性和覆盖检查结果。交付按顺序编号的 PNG、仅含成品 PNG 的 ZIP 和第一张预览。
