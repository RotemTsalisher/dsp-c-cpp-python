"""Build spa-course index.html (same shell as cursor-course)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

CURSOR_GEN = Path(__file__).resolve().parent.parent / "cursor-course" / "generate_course.py"


def _load_css_js() -> tuple[str, str]:
    text = CURSOR_GEN.read_text(encoding="utf-8")
    css_m = re.search(r'^CSS = """\r?\n(.*?\r?\n)"""', text, re.DOTALL | re.MULTILINE)
    js_m = re.search(r'^JS = r"""\r?\n(.*?\r?\n)"""', text, re.DOTALL | re.MULTILINE)
    if not css_m or not js_m:
        raise RuntimeError("Could not extract CSS/JS from cursor-course/generate_course.py")
    return css_m.group(1), js_m.group(1)


def md(text: str) -> str:
    lines = text.strip().split("\n")
    out: list[str] = []
    in_pre = False
    in_ul = False

    def ilm(s: str) -> str:
        s = html.escape(s)
        parts = s.split("`")
        for i in range(1, len(parts), 2):
            parts[i] = f"<code>{parts[i]}</code>"
        return "".join(parts)

    for line in lines:
        if line.startswith("```"):
            if in_pre:
                out.append("</code></pre>")
                in_pre = False
            else:
                if in_ul:
                    out.append("</ul>")
                    in_ul = False
                lang = line[3:].strip() or "text"
                out.append(f'<pre class="code-block" data-lang="{html.escape(lang)}"><code>')
                in_pre = True
            continue
        if in_pre:
            out.append(html.escape(line))
            continue
        if line.startswith("## "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{html.escape(line[3:])}</h3>")
        elif line.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h4>{html.escape(line[4:])}</h4>")
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{ilm(line[2:])}</li>")
        elif line.strip() == "":
            if in_ul:
                out.append("</ul>")
                in_ul = False
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<p>{ilm(line)}</p>")
    if in_ul:
        out.append("</ul>")
    if in_pre:
        out.append("</code></pre>")
    return "\n".join(out)


def build_index(
    out_path: Path,
    *,
    title: str,
    subtitle: str,
    storage_key: str,
    modules: list[dict],
    version: str = "2026.11",
) -> None:
    css, js = _load_css_js()
    js = js.replace(
        "const STORAGE_KEY = 'cursor-dsp-course-progress-v1';",
        f"const STORAGE_KEY = '{storage_key}';",
    )
    data = {
        "title": title,
        "subtitle": subtitle,
        "version": version,
        "modules": modules,
    }
    total_ex = sum(len(m.get("exercises", [])) for m in modules)
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page_title = html.escape(title)
    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <style>{css}</style>
</head>
<body>
  <div class="layout">
    <nav class="sidebar" aria-label="Course navigation">
      <h1 id="course-title">Loading…</h1>
      <p class="sub" id="course-sub"></p>
      <div class="progress-wrap">
        <span id="progress-label">0 / 0 exercises</span>
        <div class="progress-bar"><div id="progress-fill"></div></div>
      </div>
      <input type="search" id="search" placeholder="Filter modules…" aria-label="Filter modules" />
      <p class="level">Modules</p>
      <ul id="module-list"></ul>
    </nav>
    <main>
      <section class="hero">
        <h2 id="module-title">Welcome</h2>
        <div id="module-meta"></div>
        <p id="module-summary" style="margin-top:0.75rem;color:var(--muted);"></p>
        <p style="font-size:0.85rem;color:var(--muted);margin-top:1rem;">
          Open this file in any browser. Progress saves locally. Markdown labs live under <code>modules/</code>;
          Git-friendly exercises under <code>exercises/</code> (solutions in <code>solutions/</code>, not mixed in).
          <strong>{total_ex} exercises</strong> in this browser course view.
        </p>
      </section>
      <section class="lesson" id="lesson-body"></section>
      <section>
        <h3 style="color:var(--accent2);">Exercises</h3>
        <p id="exercise-count" style="color:var(--muted);font-size:0.9rem;"></p>
        <div id="exercises"></div>
      </section>
    </main>
  </div>
  <script>
    window.COURSE_DATA = {data_json};
  </script>
  <script>{js}</script>
</body>
</html>
"""
    out_path.write_text(html_out, encoding="utf-8")
