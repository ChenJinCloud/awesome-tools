---
name: wechat-public-account-format
description: Convert local Markdown into chenjin.io-styled, inline-CSS HTML that is optimized for copying into the WeChat Official Account editor.
---

# 公众号排版（chenjin.io）

将本地 Markdown 原稿转换为可以直接复制到微信公众号后台的 HTML 成品。适用于公众号文章、个人复盘、OKR、教程、知识卡片和带表格的长文。

## 默认输出

- 不修改、不覆盖原始 Markdown。
- 默认在原稿同目录生成“原文件名-公众号版.html”。
- HTML 只使用内联样式，不依赖外部 CSS、JavaScript 或在线字体。
- 用户明确要求“同步到草稿箱”时，才进一步讨论公众号 API；默认只生成可复制版本，不自动发布。

## 视觉与字号规范

默认沿用 chenjin.io 当前本地设计系统：

- 月白/浅青背景：#EFF8F4
- 青黛标题与正文：#223939
- 翠涛主强调色：#2F8E7D
- 深翠涛文字：#2F7E6F
- 月白淡区块：#E6F1EB
- 薄荷淡区块：#EEF6F1
- 松花淡边框：#D0E1D8
- 胭脂辅助色：#B35F6B
- 暖棕辅助色：#A8754A

默认字号：

- 正文、段落、列表：14px
- 主标题：26px
- 一级标题：20px
- 二级标题：17px
- 表格文字：12px
- 表格中的分类标签：13px

关键兼容规则：

- 正文字号必须写在每个 p、li 元素上，不依赖外层继承。
- 表格字号必须写在每个 th、td 元素上。
- 常见 SWOT 分类标签使用翠涛、胭脂、松绿和暖棕辅助色，保持信息层级但不喧宾夺主。
- 以“**核心动作：**”开头的段落转换为单格表格色块，并把背景色、文字色、字号都写到单元格和文字节点上。
- 表格使用内联边框和背景色；复杂嵌套布局应改为可读的表格或普通区块。

## 执行方式

优先使用配套脚本：

~~~bash
python3 /Users/jinchen/.codex/skills/wechat-public-account-format/scripts/render_wechat.py \
  "/path/to/article.md"
~~~

可选参数：

~~~bash
python3 /Users/jinchen/.codex/skills/wechat-public-account-format/scripts/render_wechat.py \
  "/path/to/article.md" \
  --output "/path/to/article-公众号版.html" \
  --title "文章标题"
~~~

脚本支持常见 Markdown 标题、段落、粗体、斜体、行内代码、链接、图片、无序/有序列表、引用、水平线和 Markdown 表格。

## 处理边界

- 只做结构化排版，不擅自改写原文、补充观点或翻译内容。
- 图片保留原引用并给出兼容性提醒：本地图片路径通常不能随 HTML 一起粘贴进公众号，需要在公众号编辑器中重新上传。
- 外部链接保留为安全链接；不把脚本、外部样式或跟踪代码带入成品。
- 公众号后台会对粘贴内容做二次清洗，最终以后台预览为准；如需完全固定字号，可在粘贴后全选并在编辑器中统一设置字号。
- 不把“生成 HTML”“保存草稿”“预览”和“正式发布”混为同一状态。

## 验收

生成后检查：

1. 输出文件存在，且原始 Markdown 的修改时间和内容未被改变。
2. HTML 没有 link、script、外部 CSS 或外部字体依赖。
3. 正文 p、li 都有明确字号；表格 th、td 都有明确字号。
4. 标题、核心动作色块、表格、引用和附录等主要结构完整。
5. 用浏览器打开输出文件预览，再复制到公众号草稿箱校对。
