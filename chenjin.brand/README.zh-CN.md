# chenjin.brand

[English](README.md) | [简体中文](README.zh-CN.md)

陈今的个人品牌设计 Skill 集合，存放在 `ChenJinCloud/awesome-tools` 内。后续与个人 IP 品牌设计有关的 Skill 统一加入 `chenjin.brand/skills/`。

## Skills

| Skill | 用途 | 版本 |
| --- | --- | --- |
| [chenjin-brand-xiaohongshu](skills/chenjin-brand-xiaohongshu/SKILL.zh-CN.md) | 用代码制作小红书 3:4 竖图，包含个人介绍卡模板和内容页 | 0.1.0 |

第一版采用微暖月白背景、青黛文字和低饱和青绿强调。成绩圆角框配浅阴影，清单使用协调的圆点，优先保证阅读清楚。视觉基线来自 2026-10-15 个人介绍卡的逐轮调整。

## 使用

将单个 Skill 文件夹复制或链接到 Agent 的 Skill 目录。包内包含使用说明、模板、示例及 Python 渲染器。Codex 安装示例，在仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/chenjin.brand/skills/chenjin-brand-xiaohongshu" ~/.codex/skills/chenjin-brand-xiaohongshu
```

目标路径需要空闲，已有安装应保留。调用 `$chenjin-brand-xiaohongshu`，提供要排版的内容；需要人物照片时一并提供。

## 预览

![使用占位照片的个人介绍版式](skills/chenjin-brand-xiaohongshu/examples/intro-preview.png)

公开示例使用绘制的占位图。数字用于演示排版，不作为业绩声明。实际制作时使用当前文案和已授权的人像。

渲染器也支持普通内容页，见[输入格式](skills/chenjin-brand-xiaohongshu/references/input-schema.zh-CN.md)及[正文示例](skills/chenjin-brand-xiaohongshu/examples/content.zh-CN.json)。

## 加入新 Skill

每个包独立放在 `skills/<skill-name>/` 下，并加入本页索引。沿用父仓库约定，提供英文和简体中文说明。字体、照片与第三方插画保留各自权利；模板不附带参考站点的素材。
