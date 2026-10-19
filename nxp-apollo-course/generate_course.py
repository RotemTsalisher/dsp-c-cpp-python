#!/usr/bin/env python3
"""Generate index.html — Apollo NXP handover course (HiFi4 + Cortex-M33)."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"


def ex(n: str, prompt: str, hints: str, solution: str, stretch: str = "") -> dict:
    return {
        "id": n,
        "prompt": prompt,
        "hints": hints,
        "solution": solution,
        "stretch": stretch,
    }


def md(text: str) -> str:
    """Minimal markdown-ish to HTML for lesson bodies."""
    lines = text.strip().split("\n")
    out: list[str] = []
    in_pre = False
    in_ul = False
    in_table = False
    for line in lines:
        if line.startswith("```"):
            if in_table:
                out.append("</code></pre>")
                in_table = False
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
        if line.startswith("|"):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_table:
                out.append('<pre class="code-block" data-lang="text"><code>')
                in_table = True
            out.append(html.escape(line))
            continue
        if line.startswith("## "):
            if in_table:
                out.append("</code></pre>")
                in_table = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{html.escape(line[3:])}</h3>")
        elif line.startswith("### "):
            if in_table:
                out.append("</code></pre>")
                in_table = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h4>{html.escape(line[4:])}</h4>")
        elif line.startswith("- "):
            if in_table:
                out.append("</code></pre>")
                in_table = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(line[2:])}</li>")
        elif line.strip() == "":
            if in_table:
                out.append("</code></pre>")
                in_table = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
        else:
            if in_table:
                out.append("</code></pre>")
                in_table = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<p>{inline_md(line)}</p>")
    if in_table:
        out.append("</code></pre>")
    if in_ul:
        out.append("</ul>")
    if in_pre:
        out.append("</code></pre>")
    return "\n".join(out)


def inline_md(s: str) -> str:
    s = html.escape(s)
    parts = s.split("`")
    for i in range(1, len(parts), 2):
        parts[i] = f"<code>{parts[i]}</code>"
    s = "".join(parts)
    bits = s.split("**")
    out = []
    for i, bit in enumerate(bits):
        if i % 2 == 1:
            out.append(f"<strong>{bit}</strong>")
        else:
            out.append(bit)
    return "".join(out)


from course_modules import load

MODULES, DRILLS = load(ex, md)
MODULES.append(DRILLS)


CSS = """
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --surface2: #243044;
  --text: #e7ecf3;
  --muted: #9aa8bc;
  --accent: #3d9cf5;
  --accent2: #5eead4;
  --warn: #fbbf24;
  --ok: #4ade80;
  --border: #2d3a4f;
  --ex: #1e2a3d;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
}
a { color: var(--accent); }
.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  min-height: 100vh;
}
nav.sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1rem;
  overflow-y: auto;
  position: sticky;
  top: 0;
  height: 100vh;
}
nav.sidebar h1 {
  font-size: 1.05rem;
  margin: 0 0 0.25rem;
  line-height: 1.3;
}
nav.sidebar .sub {
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 1rem;
}
nav.sidebar input {
  width: 100%;
  padding: 0.45rem 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  margin-bottom: 0.75rem;
}
nav.sidebar ul { list-style: none; padding: 0; margin: 0; }
nav.sidebar li { margin-bottom: 0.15rem; }
nav.sidebar button.module-link {
  width: 100%;
  text-align: left;
  background: transparent;
  border: none;
  color: var(--text);
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
}
nav.sidebar button.module-link:hover { background: var(--surface2); }
nav.sidebar button.module-link.active {
  background: var(--accent);
  color: #061018;
  font-weight: 600;
}
nav.sidebar .level {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  margin-top: 0.75rem;
  margin-bottom: 0.25rem;
}
.progress-wrap {
  margin: 1rem 0;
  font-size: 0.75rem;
  color: var(--muted);
}
.progress-bar {
  height: 6px;
  background: var(--bg);
  border-radius: 99px;
  overflow: hidden;
  margin-top: 0.35rem;
}
.progress-bar > div {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  width: 0%;
  transition: width 0.3s ease;
}
main {
  padding: 1.5rem 2rem 4rem;
  max-width: 920px;
}
.hero {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}
.hero h2 { margin: 0 0 0.5rem; font-size: 1.75rem; }
.hero p { color: var(--muted); margin: 0; }
.badge {
  display: inline-block;
  font-size: 0.7rem;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  background: var(--surface2);
  color: var(--accent2);
  margin-right: 0.35rem;
}
.lesson h3 { margin-top: 1.5rem; color: var(--accent2); }
.lesson h4 { margin-top: 1rem; }
.lesson pre.code-block {
  background: #0a0e14;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  overflow-x: auto;
  font-size: 0.82rem;
}
.lesson code {
  background: var(--surface2);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
  font-size: 0.88em;
}
.exercise {
  background: var(--ex);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 8px;
  padding: 1rem 1.1rem;
  margin: 1.25rem 0;
}
.exercise header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.exercise h5 {
  margin: 0;
  font-size: 0.95rem;
}
.exercise .ex-id {
  font-size: 0.72rem;
  color: var(--muted);
  font-family: ui-monospace, monospace;
}
.exercise .prompt { margin: 0.75rem 0; }
.exercise .hint {
  font-size: 0.85rem;
  color: var(--muted);
  border-top: 1px dashed var(--border);
  padding-top: 0.65rem;
  margin-top: 0.65rem;
}
.exercise .actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.75rem;
}
button.btn {
  border: none;
  border-radius: 6px;
  padding: 0.45rem 0.85rem;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
}
button.btn-primary { background: var(--accent); color: #061018; }
button.btn-ghost { background: var(--surface2); color: var(--text); }
button.btn-ok { background: #166534; color: #ecfdf5; }
.exercise.done { border-left-color: var(--ok); opacity: 0.92; }
.solution {
  display: none;
  margin-top: 0.85rem;
  padding: 0.85rem;
  background: #0a0e14;
  border-radius: 6px;
  border: 1px solid var(--border);
  white-space: pre-wrap;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 0.8rem;
}
.solution.visible { display: block; }
.stretch {
  margin-top: 0.5rem;
  font-size: 0.82rem;
  color: var(--warn);
}
@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  nav.sidebar { position: relative; height: auto; }
}
"""

JS = r"""
const STORAGE_KEY = 'nxp-apollo-handover-progress-v1';

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); }
  catch { return {}; }
}
function saveProgress(p) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
}

function countExercises(modules) {
  return modules.reduce((n, m) => n + (m.exercises?.length || 0), 0);
}

function renderModuleList(modules, activeId, filter) {
  const ul = document.getElementById('module-list');
  ul.innerHTML = '';
  const q = (filter || '').toLowerCase();
  modules.forEach(m => {
    const hay = (m.title + ' ' + m.summary + ' ' + m.level).toLowerCase();
    if (q && !hay.includes(q)) return;
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.className = 'module-link' + (m.id === activeId ? ' active' : '');
    btn.textContent = m.id === 'drills' ? '⚡ ' + m.title : m.id + ' · ' + m.title;
    btn.onclick = () => showModule(m.id);
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

function showModule(id) {
  const m = COURSE.modules.find(x => x.id === id) || COURSE.modules[0];
  history.replaceState(null, '', '#' + m.id);
  document.getElementById('module-title').textContent = m.title;
  document.getElementById('module-meta').innerHTML =
    `<span class="badge">${m.level}</span><span class="badge">Module ${m.id}</span>`;
  document.getElementById('module-summary').textContent = m.summary;
  document.getElementById('lesson-body').innerHTML = m.body;

  const exRoot = document.getElementById('exercises');
  exRoot.innerHTML = '';
  const progress = loadProgress();

  (m.exercises || []).forEach(ex => {
    const done = progress[ex.id];
    const el = document.createElement('article');
    el.className = 'exercise' + (done ? ' done' : '');
    el.dataset.exId = ex.id;

    el.innerHTML = `
      <header>
        <h5>Exercise</h5>
        <span class="ex-id">${ex.id}</span>
      </header>
      <p class="prompt">${escapeHtml(ex.prompt)}</p>
      ${ex.hints ? `<div class="hint"><strong>Hint:</strong> ${escapeHtml(ex.hints)}</div>` : ''}
      ${ex.stretch ? `<div class="stretch"><strong>Stretch:</strong> ${escapeHtml(ex.stretch)}</div>` : ''}
      <div class="actions">
        <button type="button" class="btn btn-primary btn-solution">Reveal solution</button>
        <button type="button" class="btn btn-ghost btn-hide">Hide solution</button>
        <button type="button" class="btn btn-ok btn-done">${done ? '✓ Completed' : 'Mark complete'}</button>
      </div>
      <div class="solution" role="region" aria-label="Solution">${escapeHtml(ex.solution)}</div>
    `;

    el.querySelector('.btn-solution').onclick = () => {
      el.querySelector('.solution').classList.add('visible');
    };
    el.querySelector('.btn-hide').onclick = () => {
      el.querySelector('.solution').classList.remove('visible');
    };
    el.querySelector('.btn-done').onclick = (ev) => {
      progress[ex.id] = true;
      saveProgress(progress);
      el.classList.add('done');
      ev.target.textContent = '✓ Completed';
      updateProgressBar();
    };

    exRoot.appendChild(el);
  });

  renderModuleList(COURSE.modules, m.id, document.getElementById('search').value);
  document.getElementById('exercise-count').textContent =
    (m.exercises || []).length + ' exercises in this module';
  updateProgressBar();
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function updateProgressBar() {
  const total = countExercises(COURSE.modules);
  const progress = loadProgress();
  const done = Object.keys(progress).filter(k => progress[k]).length;
  const pct = total ? Math.round((done / total) * 100) : 0;
  document.getElementById('progress-label').textContent = `${done} / ${total} exercises (${pct}%)`;
  document.getElementById('progress-fill').style.width = pct + '%';
}

function init() {
  const data = window.COURSE_DATA;
  window.COURSE = data;
  document.getElementById('course-title').textContent = data.title;
  document.getElementById('course-sub').textContent = data.subtitle;

  document.getElementById('search').oninput = (e) => {
    const id = (location.hash || '#00').slice(1);
    renderModuleList(COURSE.modules, id, e.target.value);
  };

  const startId = (location.hash || '#00').replace('#', '');
  showModule(COURSE.modules.some(m => m.id === startId) ? startId : '00');
  window.onhashchange = () => {
    const id = (location.hash || '#00').slice(1);
    if (COURSE.modules.some(m => m.id === id)) showModule(id);
  };
}

document.addEventListener('DOMContentLoaded', init);
"""


def build_html() -> str:
    data = {
        "title": "Apollo NXP Handover",
        "subtitle": "RT685 · HiFi4 audio · Cortex-M33 mesh · AFW · Opus · G.723.1 · read-only firmware",
        "version": "2026.10",
        "modules": MODULES,
    }
    total_ex = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(data, ensure_ascii=False)
    data_json = data_json.replace("</", "<\\/")  # avoid breaking script tag

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Apollo NXP Handover — HiFi4 and Cortex-M33</title>
  <style>{CSS}</style>
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
          Open this file in any browser. Progress saves in this browser only.
          The Apollo firmware tree stays read-only: write answers in a notebook, then reveal.
          <strong>{total_ex} exercises</strong> · HiFi4 + Cortex-M33 · boot, audio graph, mesh.
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
  <script>{JS}</script>
</body>
</html>
"""


if __name__ == "__main__":
    html_out = build_html()
    OUT.write_text(html_out, encoding="utf-8")
    n_mod = len(MODULES)
    n_ex = sum(len(m.get("exercises", [])) for m in MODULES)
    print(f"Wrote {OUT} — {n_mod} modules, {n_ex} exercises")
