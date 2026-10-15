#!/usr/bin/env python3
"""Build editable brand cards and export them with Ego Lite. / 生成并导出品牌竖图。"""

import argparse
import base64
import functools
import hashlib
import html
import http.server
import json
import mimetypes
from pathlib import Path
import shutil
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]


def text(value):
    return html.escape(str(value)).replace("\n", "<br>")


def image_uri(path):
    path = Path(path)
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in {"image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml"}:
        raise ValueError("Unsupported image format / 不支持的图片格式")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def document(body, css, title, scale):
    scale_css = ""
    if scale != 1:
        scale_css = (f"body{{width:{1080*scale}px;height:{1440*scale}px;overflow:hidden}}"
                     f".poster{{transform:scale({scale});transform-origin:top left}}")
    return (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{text(title)}</title><style>{css}\n{scale_css}</style></head>'
            f'<body>{body}</body></html>')


def footer(label, brand):
    return (f'<footer class="footer"><p data-check>{text(label)}</p>'
            f'<span class="brand" data-check>{text(brand)}</span></footer>')


def intro(data, base, portrait_override):
    metrics = data.get("metrics", [])
    topics = data.get("topics", [])
    if len(metrics) != 4:
        raise ValueError("The intro template needs four metrics / 介绍模板需要四项成绩")
    if not 1 <= len(topics) <= 3:
        raise ValueError("Use one to three topics in the intro / 介绍卡容纳一至三个话题")
    portrait = portrait_override or data.get("portrait")
    uri = image_uri((base / portrait).resolve()) if portrait else image_uri(ROOT / "assets/portrait-placeholder.svg")
    metric_html = "".join(
        f'<div class="metric" data-boundary><strong class="number" data-check>{text(m["value"])}</strong>'
        f'<span class="metric-caption" data-check>{text(m["label"])}</span></div>' for m in metrics)
    topic_html = "".join(f'<li data-check>{text(t)}</li>' for t in topics)
    return (f'<main class="poster intro-page">'
            f'<section class="hero"><div class="intro">'
            f'<p class="hello" data-check>{text(data.get("hello", "你好，我是"))}</p>'
            f'<h1 data-check style="font-size:{int(data.get("name_size", 136))}px">{text(data["name"])}</h1>'
            f'<p class="role" data-check>{text(data["role"])}</p>'
            f'<p class="summary" data-check>{text(data.get("summary", ""))}</p></div>'
            f'<div class="portrait"><img src="{uri}" alt="{text(data.get("portrait_alt", "Portrait / 人物照片"))}"></div></section>'
            f'<section class="proof"><h2 data-check>{text(data["project"])}</h2>'
            f'<div class="metrics">{metric_html}</div></section>'
            f'<section class="topics"><h2 data-check>{text(data.get("topics_title", "我会在这里，和你聊："))}</h2>'
            f'<ul>{topic_html}</ul></section>'
            f'{footer(data.get("footer", ""), data.get("brand", "chenjin.io"))}</main>')


def content_page(page, data, base, index, count):
    blocks = page.get("blocks", [])
    if not blocks:
        raise ValueError("Content pages must contain body text / 内容页必须有正文")
    if sum(b.get("type") == "quote" for b in blocks) > 1:
        raise ValueError("Use at most one quote block per page / 每页最多一处强调引用")
    parts = []
    for block in blocks:
        kind = block.get("type", "paragraph")
        if kind == "paragraph":
            parts.append(f'<p data-check>{text(block["text"])}</p>')
        elif kind == "heading":
            parts.append(f'<h2 data-check>{text(block["text"])}</h2>')
        elif kind == "bullets":
            items = "".join(f'<li data-check>{text(t)}</li>' for t in block["items"])
            parts.append(f'<ul class="content-list">{items}</ul>')
        elif kind == "quote":
            parts.append(f'<blockquote data-check>{text(block["text"])}</blockquote>')
        elif kind == "image":
            uri = image_uri((base / block["path"]).resolve())
            parts.append(f'<figure><img src="{uri}" alt="{text(block.get("alt", ""))}">'
                         f'<figcaption data-check>{text(block.get("caption", ""))}</figcaption></figure>')
        else:
            raise ValueError(f"Unknown block type / 未知内容类型: {kind}")
    label = data.get("footer", "")
    if count > 1:
        label = f"{label}  {index}/{count}".strip()
    return (f'<main class="poster content-page"><h1 class="content-heading" data-check>{text(page["title"])}</h1>'
            f'<section class="content-body" data-boundary>{"".join(parts)}</section>'
            f'{footer(label, data.get("brand", "chenjin.io"))}</main>')


def write_index(out, files, has_png):
    cards = []
    for file in files:
        name = file.with_suffix(".png").name
        media = f'<img src="{name}" alt="{file.stem}">' if has_png else f'<iframe src="{file.name}" title="{file.stem}"></iframe>'
        cards.append(f'<article>{media}<p><a href="{file.name}">Editable HTML / 可编辑源码</a>'
                     + (f' · <a href="{name}">PNG</a>' if has_png else '') + '</p></article>')
    (out / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>Card preview / 竖图预览</title>'
                                  '<style>body{margin:28px;background:#e8e8e3;font:16px sans-serif}'
                                  'main{display:flex;flex-wrap:wrap;gap:28px}article{width:min(540px,100%)}'
                                  'img{display:block;width:100%}iframe{width:1080px;height:1440px;border:0;'
                                  'transform:scale(.5);transform-origin:top left;margin-bottom:-720px}'
                                  'a{color:#223939}</style><main>' + ''.join(cards) + '</main>', encoding="utf-8")


def browser_export(out, files, scale, space_id, keep_space):
    if not shutil.which("ego-browser"):
        raise RuntimeError("ego-browser is unavailable; HTML is saved / 未找到 ego-browser，HTML 已保存")

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_):
            pass

    handler = functools.partial(QuietHandler, directory=str(out))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    config = {"out": str(out), "files": [f.name for f in files], "scale": scale,
              "space": space_id, "keep": keep_space, "port": server.server_port}
    script = "const cfg=" + json.dumps(config) + ";\n" + r'''
const task = await taskSpace(cfg.space ?? "Chenjin brand card export");
const report = {status:"failed", spaceId:task.spaceId, pages:[]};
console.log("SPACE_ID="+task.spaceId);
try {
  const managed = await task.pages();
  const page = managed.length ? task.page(managed[0].label) : await task.newPage();
  for (const file of cfg.files) {
    await page.goto(`http://127.0.0.1:${cfg.port}/${file}`);
    await page.evaluate(async()=>{
      await document.fonts.ready;
      await Promise.all([...document.images].map(i=>i.decode()));
    });
    const check = await page.evaluate(()=>{
      const canvas=document.querySelector(".poster").getBoundingClientRect();
      const errors=[];
      for(const e of document.querySelectorAll("[data-check],.content-body")) {
        const r=e.getBoundingClientRect();
        const parent=e.parentElement.closest("[data-boundary]");
        const bounds=parent ? parent.getBoundingClientRect() : canvas;
        if(e.scrollWidth>e.clientWidth+2 || (e.matches(".content-body") && e.scrollHeight>e.clientHeight+2) ||
           r.right>bounds.right+1 || r.bottom>bounds.bottom+1 ||
           r.left<bounds.left-1 || r.top<bounds.top-1) errors.push(e.innerText);
      }
      const metrics=document.querySelector(".metrics");
      const topics=document.querySelector(".topics h2");
      const body=document.querySelector(".content-body");
      const heading=document.querySelector(".content-heading");
      const end=document.querySelector(".topics li:last-child") || body;
      const footer=document.querySelector(".footer");
      if(metrics && topics && metrics.getBoundingClientRect().bottom>topics.getBoundingClientRect().top-12) errors.push("metrics/topics overlap");
      if(body && heading && heading.getBoundingClientRect().bottom>body.getBoundingClientRect().top-16) errors.push("title/body overlap");
      if(end && footer && end.getBoundingClientRect().bottom>footer.getBoundingClientRect().top-16) errors.push("footer overlap");
      return {width:canvas.width,height:canvas.height,errors,text:document.querySelector("main").innerText,
              fontStack:getComputedStyle(document.body).fontFamily};
    });
    report.pages.push({file,...check});
    if(check.errors.length) throw new Error("Content overflow / 内容越界: "+check.errors.join(" | "));
    await page.screenshot({path:`${cfg.out}/${file.replace(/\.html$/,".png")}`,
                          clip:{x:0,y:0,width:1080*cfg.scale,height:1440*cfg.scale},fullPage:true});
  }
  report.status="exported";
  if(!cfg.keep) await task.finish({keep:[]});
} catch(error) {
  report.error=String(error);
  process.exitCode=1;
}
console.log("REPORT_JSON="+JSON.stringify(report));
'''
    try:
        result = subprocess.run(["ego-browser", "nodejs"], input=script, text=True, capture_output=True)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
    lines = (result.stdout + "\n" + result.stderr).splitlines()
    for line in lines:
        if line.startswith("SPACE_ID="):
            print(line)
    reports = [line[len("REPORT_JSON="):] for line in lines if line.startswith("REPORT_JSON=")]
    if reports:
        report = json.loads(reports[-1])
    else:
        report = {"status": "failed", "error": result.stderr.strip() or result.stdout.strip()}
    if result.returncode and report.get("status") == "exported":
        report["status"] = "failed"
        report["error"] = result.stderr.strip()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input JSON / 输入 JSON")
    parser.add_argument("--output", required=True, type=Path, help="New output folder / 新输出目录")
    parser.add_argument("--portrait", type=Path, help="Override portrait / 替换照片")
    parser.add_argument("--scale", type=int, choices=[1, 2], default=1, help="Render scale / 渲染倍率")
    parser.add_argument("--space", type=int, help="Existing Ego Lite space ID / 已有 Space ID")
    parser.add_argument("--keep-space", action="store_true", help="Keep space for iteration / 保留 Space 继续迭代")
    parser.add_argument("--sources-only", action="store_true", help="Build HTML only / 只生成 HTML")
    args = parser.parse_args()
    source = args.source.resolve()
    out = args.output.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Choose a new empty output directory / 请使用新的空输出目录")
    data = json.loads(source.read_text(encoding="utf-8"))
    css = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
    mode = data.get("mode", "content")
    if mode == "intro":
        bodies = [(data["name"], intro(data, source.parent, args.portrait.resolve() if args.portrait else None))]
    elif mode == "content":
        pages = data.get("pages", [])
        if not pages:
            raise ValueError("At least one page is required / 至少需要一页")
        bodies = [(p["title"], content_page(p, data, source.parent, i+1, len(pages))) for i, p in enumerate(pages)]
    else:
        raise ValueError("Use intro or content mode / 模式应为 intro 或 content")
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out / "source.json")
    (out / "styles.css").write_text(css, encoding="utf-8")
    files = []
    for index, (title, body) in enumerate(bodies, 1):
        file = out / f"card-{index:02d}.html"
        file.write_text(document(body, css, title, args.scale), encoding="utf-8")
        files.append(file)
    write_index(out, files, False)
    report = {"status": "sources-only", "scale": args.scale,
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "mode": mode}
    if not args.sources_only:
        try:
            report.update(browser_export(out, files, args.scale, args.space, args.keep_space))
        except Exception as error:
            report.update(status="failed", error=str(error))
        if report["status"] == "exported":
            write_index(out, files, True)
    (out / "render-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{report['status']}: {out}")
    if report["status"] == "failed":
        print(report.get("error", ""), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Error / 错误: {error}", file=sys.stderr)
        sys.exit(1)
