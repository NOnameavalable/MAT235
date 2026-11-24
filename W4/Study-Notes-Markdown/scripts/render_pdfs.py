#!/usr/bin/env python3
"""
Render Study-Notes.md and Answers-and-Practice.md to PDF with 1:1 visual fidelity
to the Antigravity IDE / VS Code / GitHub Markdown + KaTeX preview.
"""

import json
import os
import re
import subprocess
import tempfile
from urllib.parse import quote
from markdown_it import MarkdownIt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODE_BIN = "/Users/stevenli/.nvm/versions/node/v24.20.0/bin/node"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KATEX_JS = "/Applications/Antigravity IDE.app/Contents/Resources/app/node_modules/katex/dist/katex.min.js"
KATEX_CSS = "/Applications/Antigravity IDE.app/Contents/Resources/app/node_modules/katex/dist/katex.min.css"


def file_url(path: str) -> str:
    return "file://" + quote(os.path.abspath(path))


def github_slug(text: str) -> str:
    # Strip HTML tags if any
    s = re.sub(r"<[^>]+>", "", text).strip().lower()
    # Remove punctuation except word chars, spaces, and hyphens
    s = re.sub(r"[^\w\s-]", "", s)
    # GitHub replaces each space character with a hyphen (preserving double hyphens from ' — ')
    s = s.replace(" ", "-")
    return s


def render_katex_batch(expressions):
    """
    Render a list of {"math": str, "display": bool} dicts using KaTeX in Node.js.
    """
    node_script = r"""
const fs = require('fs');
const katex = require(process.argv[2]);
const items = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const out = items.map((item, idx) => {
  try {
    return {
      html: katex.renderToString(item.math, {
        displayMode: item.display,
        throwOnError: false,
        strict: false,
        trust: true
      }),
      error: null
    };
  } catch (err) {
    return {
      html: item.math,
      error: String(err)
    };
  }
});
fs.writeFileSync(process.argv[4], JSON.stringify(out), 'utf8');
"""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f_in:
        json.dump(expressions, f_in)
        in_path = f_in.name
    out_path = in_path + ".out.json"
    js_path = in_path + ".js"
    with open(js_path, "w", encoding="utf-8") as f_js:
        f_js.write(node_script)

    try:
        subprocess.run([NODE_BIN, js_path, KATEX_JS, in_path, out_path], check=True)
        with open(out_path, "r", encoding="utf-8") as f_out:
            return json.load(f_out)
    finally:
        for p in (in_path, out_path, js_path):
            if os.path.exists(p):
                os.remove(p)


def convert_md_to_html(md_path: str) -> str:
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # For Study-Notes.md, replace each PT's "A complete answer must include." and
    # "Common mistakes." subsections with a clean handwriting workspace in the PDF.
    if os.path.basename(md_path) == "Study-Notes.md":
        md_text = re.sub(
            r"\*\*A complete answer must include\.\*\*[\s\S]*?(?=(?:\n\*\*Concept C-\d+ Practice Index:\*\*|\n---|\Z))",
            '<div class="pt-workspace" style="height: 220px;"></div>\n',
            md_text,
        )
    elif os.path.basename(md_path) == "Answers-and-Practice.md":
        # Replace solutions and final answers in Sections B and C with blank handwriting workspace
        md_text = re.sub(
            r"^- \*\*(?:Complete working(?: and justifications)?|Complete reasoning & verification):\*\*[\s\S]*?(?=\n---)",
            '<div class="pt-workspace" style="height: 180px;"></div>\n',
            md_text,
            flags=re.M,
        )

    # 1. Protect fenced code blocks and inline code spans
    code_store = []

    def save_code(m):
        idx = len(code_store)
        code_store.append(m.group(0))
        return f"CODESPANPLACEHOLDER{idx:05d}END"

    # Fenced code blocks first, then inline backticks
    md_text = re.sub(r"```[\s\S]*?```", save_code, md_text)
    md_text = re.sub(r"`[^`\n]+`", save_code, md_text)

    # 2. Extract display math $$...$$ and inline math $...$
    math_items = []

    def save_display_math(m):
        idx = len(math_items)
        math_items.append({"math": m.group(1).strip(), "display": True})
        return f"KATEXMATHPLACEHOLDER{idx:05d}END"

    def save_inline_math(m):
        idx = len(math_items)
        math_items.append({"math": m.group(1).strip(), "display": False})
        return f"KATEXMATHPLACEHOLDER{idx:05d}END"

    md_text = re.sub(r"\$\$([\s\S]*?)\$\$", save_display_math, md_text)
    md_text = re.sub(r"(?<!\\)\$((?:\\\$|[^$\n])+?)(?<!\\)\$", save_inline_math, md_text)

    # Render all math via KaTeX
    rendered_math = render_katex_batch(math_items)
    for idx, res in enumerate(rendered_math):
        if res["error"] or "katex-error" in res["html"]:
            print(f"[WARNING] KaTeX issue in {os.path.basename(md_path)} item #{idx}: {math_items[idx]['math'][:60]}")

    # 3. Restore code spans before markdown-it parsing
    for idx, original_code in enumerate(code_store):
        md_text = md_text.replace(f"CODESPANPLACEHOLDER{idx:05d}END", original_code)

    # 4. Parse Markdown to HTML using markdown-it with GFM tables and strikethrough
    md_parser = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table").enable("strikethrough")
    html_body = md_parser.render(md_text)

    # 5. Transform GitHub-style alerts: <blockquote>\n<p>[!WARNING]\n...</p>\n</blockquote>
    alert_icons = {
        "WARNING": '<svg class="octicon" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
        "NOTE": '<svg class="octicon" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>',
        "IMPORTANT": '<svg class="octicon" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
        "TIP": '<svg class="octicon" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg>',
        "CAUTION": '<svg class="octicon" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M4.47.22A.749.749 0 0 1 5 0h6c.199 0 .389.079.53.22l4.25 4.25c.141.14.22.331.22.53v6a.749.749 0 0 1-.22.53l-4.25 4.25A.749.749 0 0 1 11 16H5a.749.749 0 0 1-.53-.22L.22 11.53A.749.749 0 0 1 0 11V5c0-.199.079-.389.22-.53Zm.84 1.28L1.5 5.31v5.38l3.81 3.81h5.38l3.81-3.81V5.31L10.69 1.5ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 4Zm0 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>',
    }

    def replace_alert(m):
        kind = m.group(1).upper()
        rest = m.group(2).lstrip()
        icon = alert_icons.get(kind, alert_icons["NOTE"])
        title = kind.capitalize()
        return (
            f'<div class="markdown-alert markdown-alert-{kind.lower()}">\n'
            f'<p class="markdown-alert-title">{icon}{title}</p>\n'
            f"<p>{rest}"
        )

    html_body = re.sub(
        r"<blockquote>\s*<p>\[!(WARNING|NOTE|IMPORTANT|TIP|CAUTION)\]\s*([\s\S]*?)</blockquote>",
        lambda m: replace_alert(m) + "</div>",
        html_body,
    )

    # 6. Add GitHub-compatible id attributes to headings (while math placeholders are still intact
    # or using the raw heading text with math symbols restored as plain text)
    def add_heading_id(m):
        tag = m.group(1)
        inner = m.group(2)
        # Reconstruct raw text for slugify by replacing any math placeholder with its raw TeX
        raw_inner = inner
        for p_m in re.finditer(r"KATEXMATHPLACEHOLDER(\d{5})END", raw_inner):
            p_idx = int(p_m.group(1))
            raw_inner = raw_inner.replace(p_m.group(0), math_items[p_idx]["math"])
        slug = github_slug(raw_inner)
        return f'<{tag} id="{slug}">{inner}</{tag}>'

    html_body = re.sub(r"<(h[1-6])>([\s\S]*?)</\1>", add_heading_id, html_body)

    # 7. Resolve relative image paths (figures/...) to file:// URLs
    def fix_img_src(m):
        prefix, src, suffix = m.group(1), m.group(2), m.group(3)
        if not src.startswith(("http://", "https://", "file://", "data:")):
            abs_img = os.path.join(os.path.dirname(md_path), src)
            src = file_url(abs_img)
        return f"{prefix}{src}{suffix}"

    html_body = re.sub(r'(<img\s+[^>]*src=")([^"]+)(")', fix_img_src, html_body)

    # 8. Restore pre-rendered KaTeX HTML
    for idx, res in enumerate(rendered_math):
        html_body = html_body.replace(f"KATEXMATHPLACEHOLDER{idx:05d}END", res["html"])

    katex_css_url = file_url(KATEX_CSS)

    # Full HTML with exact Antigravity IDE / VS Code / GitHub Markdown styling
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{os.path.basename(md_path)}</title>
<link rel="stylesheet" href="{katex_css_url}">
<style>
  @page {{
    size: letter;
    margin: 14mm 15mm 14mm 15mm;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  html, body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI", system-ui, "Ubuntu", "Droid Sans", "Helvetica Neue", Arial, sans-serif;
    font-size: 13.5px;
    line-height: 1.58;
    color: #1f2328;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
    word-wrap: break-word;
  }}
  h1, h2, h3, h4, h5, h6 {{
    margin-top: 22px;
    margin-bottom: 12px;
    font-weight: 600;
    line-height: 1.25;
    color: #1f2328;
    break-after: avoid;
    page-break-after: avoid;
  }}
  h1 {{
    font-size: 1.9em;
    margin-top: 0;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #d0d7de;
  }}
  h2 {{
    font-size: 1.45em;
    padding-bottom: 0.28em;
    border-bottom: 1px solid #d0d7de;
  }}
  h3 {{
    font-size: 1.2em;
  }}
  h4 {{
    font-size: 1.02em;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 12px;
  }}
  ul, ol {{
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 2em;
  }}
  li {{
    margin-bottom: 4px;
  }}
  li > p {{
    margin-bottom: 6px;
  }}
  ul ul, ul ol, ol ul, ol ol {{
    margin-top: 4px;
    margin-bottom: 4px;
  }}
  hr {{
    height: 1px;
    padding: 0;
    margin: 20px 0;
    background-color: #d0d7de;
    border: 0;
  }}
  a {{
    color: #0969da;
    text-decoration: none;
  }}
  code {{
    font-family: "SF Mono", Monaco, Menlo, Consolas, "Ubuntu Mono", "Liberation Mono", "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 0.88em;
    padding: 0.18em 0.38em;
    margin: 0;
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 5px;
  }}
  pre {{
    font-family: "SF Mono", Monaco, Menlo, Consolas, monospace;
    font-size: 0.88em;
    padding: 12px 14px;
    overflow: auto;
    line-height: 1.45;
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    margin-bottom: 14px;
  }}
  pre code {{
    background: none;
    padding: 0;
    font-size: 100%;
  }}
  blockquote {{
    margin: 0 0 12px 0;
    padding: 2px 14px;
    color: #4d5562;
    border-left: 4px solid #d0d7de;
    background-color: #f8f9fb;
    border-radius: 0 4px 4px 0;
  }}
  blockquote > :first-child {{
    margin-top: 0;
  }}
  blockquote > :last-child {{
    margin-bottom: 0;
  }}
  .markdown-alert {{
    padding: 10px 14px;
    margin-bottom: 14px;
    color: inherit;
    border-left: 4px solid #d0d7de;
    background-color: #f8f9fb;
    border-radius: 0 6px 6px 0;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .markdown-alert > :last-child {{
    margin-bottom: 0;
  }}
  .markdown-alert-title {{
    display: flex;
    font-weight: 600;
    align-items: center;
    line-height: 1;
    margin-bottom: 8px;
  }}
  .markdown-alert-title svg.octicon {{
    margin-right: 8px;
    fill: currentColor;
  }}
  .markdown-alert-warning {{
    border-left-color: #9a6700;
    background-color: #fff8c5;
  }}
  .markdown-alert-warning .markdown-alert-title {{
    color: #9a6700;
  }}
  .markdown-alert-note {{
    border-left-color: #0969da;
    background-color: #ddf4ff;
  }}
  .markdown-alert-note .markdown-alert-title {{
    color: #0969da;
  }}
  table {{
    border-spacing: 0;
    border-collapse: collapse;
    margin-top: 0;
    margin-bottom: 16px;
    width: 100%;
    font-size: 12.6px;
    line-height: 1.45;
  }}
  thead {{
    display: table-header-group;
  }}
  tr {{
    background-color: #ffffff;
    border-top: 1px solid #d0d7de;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  tr:nth-child(2n) {{
    background-color: #f6f8fa;
  }}
  th, td {{
    padding: 6px 10px;
    border: 1px solid #d0d7de;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    font-weight: 600;
    background-color: #f0f3f6;
  }}
  img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 8px auto 4px auto;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .katex-display {{
    margin: 0.75em 0;
    overflow-x: visible;
    overflow-y: hidden;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .katex {{
    font-size: 1.04em;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    return full_html


def render_md_to_pdf(md_filename: str):
    md_path = os.path.join(BASE_DIR, md_filename)
    pdf_filename = os.path.splitext(md_filename)[0] + ".pdf"
    pdf_path = os.path.join(BASE_DIR, pdf_filename)

    print(f"Converting {md_filename} -> {pdf_filename} ...")
    html_content = convert_md_to_html(md_path)

    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=BASE_DIR, delete=False, encoding="utf-8") as tmp_html:
        tmp_html.write(html_content)
        tmp_html_path = tmp_html.name

    try:
        cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--allow-file-access-from-files",
            f"--print-to-pdf={pdf_path}",
            file_url(tmp_html_path),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Successfully generated: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
    finally:
        if os.path.exists(tmp_html_path):
            os.remove(tmp_html_path)


if __name__ == "__main__":
    for name in ("Study-Notes.md", "Answers-and-Practice.md"):
        render_md_to_pdf(name)
