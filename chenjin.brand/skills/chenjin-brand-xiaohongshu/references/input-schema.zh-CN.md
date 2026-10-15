# 渲染器输入

[English](input-schema.md) | [简体中文](input-schema.zh-CN.md)

在 Skill 目录执行命令。渲染器使用 Python 标准库，导出 PNG 还需要可用的 `ego-browser` CLI 和浏览器运行环境。

## 个人介绍

从 [intro.zh-CN.json](../examples/intro.zh-CN.json) 或 [intro.en.json](../examples/intro.en.json) 开始。

- `mode` 为 `intro`。
- `name`、`role`、`project` 是必填字符串，需要固定换行时使用 `\n`。
- `name_size` 是可选的姓名字号，单位为 CSS 像素，默认 `136`；英文示例使用 `104`，以容纳更长的名字。
- `hello`、`summary`、`topics_title`、`footer`、`brand` 是可选文案，默认品牌署名为 `chenjin.io`。
- `portrait` 为可选本地图片路径，相对于输入 JSON 解析。未提供时使用明确的占位图。命令行 `--portrait` 可覆盖该路径；渲染器不下载远程图片。
- `portrait_alt` 为可选图片说明。
- `metrics` 恰好四项，每项有 `value` 和 `label`，标签可含 `\n`。示例数字仅用于排版演示。
- `topics` 为一至三个话题字符串。

模板容纳上述内容量。介绍更长或成绩更多时，另行设计版式或拆成多页。

## 内容页

从 [content.zh-CN.json](../examples/content.zh-CN.json) 或 [content.en.json](../examples/content.en.json) 开始。

- `mode` 为 `content`。
- `pages` 是非空数组，每页包含 `title` 和非空 `blocks`。
- `brand`、`footer` 是共用页脚文案，多页时自动加入页码。

正文块类型：

| 类型 | 字段 | 处理 |
| --- | --- | --- |
| `paragraph` | `text` | 清楚易读的普通段落 |
| `heading` | `text` | 正文内小标题 |
| `bullets` | `items`：字符串数组 | 低饱和青绿圆点 |
| `quote` | `text` | 每页最多一处强调块 |
| `image` | `path`，可选 `alt`、`caption` | 本地图片以 `contain` 完整显示，保留文字和图表 |

保留原有事实和内容，将输入明确分配到各页。内容越界时停止导出 PNG 并记录错误，重新分页或修改版式后再渲染。

## 命令与输出

```bash
python3 scripts/render.py examples/intro.zh-CN.json --output /path/to/new-output
python3 scripts/render.py examples/content.en.json --output /path/to/another-output --scale 2
python3 scripts/render.py examples/intro.zh-CN.json --output /path/to/source-preview --sources-only
```

使用新的输出目录。目标目录非空时停止，保留之前的版本。输出包括 `source.json`、CSS 副本、内嵌本地图片的可编辑 `card-01.html`、`index.html` 预览及 `render-report.json`。导出成功后添加同名 PNG。HTML 已内嵌 CSS，单张源码可独立使用。

`--scale 1` 输出 1080 × 1440 PNG，`--scale 2` 从 HTML 直接渲染 2160 × 2880 PNG，不放大已有位图。交付前核对实际尺寸，并逐张查看 PNG。

浏览器迭代时加 `--keep-space`，渲染器会打印 `SPACE_ID=...`。继续时传 `--space ID` 并使用新输出目录。成功后默认关闭 TaskSpace，传 `--keep-space` 时保留；失败时也保留供检查。任务结束后通过文档中的浏览器 API 关闭。用户接管浏览器时，交接并等待用户允许继续。

报告状态为 `sources-only`、`exported` 或 `failed`，记录内容哈希和浏览器边界检查。`exported` 后仍需目视检查 PNG；边界检查不判断构图，也不核实原文事实。
