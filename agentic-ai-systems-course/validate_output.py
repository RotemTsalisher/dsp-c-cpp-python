#!/usr/bin/env python3
"""Sanity-check the generated index.html.

Run after `python generate_course.py`. Catches the failure modes a hand-written
markdown renderer actually has: unbalanced tags, markdown that leaked through
unrendered, and content that silently lost its formatting.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent / "index.html"
FENCE = "`" * 3


def load() -> dict:
    text = HTML.read_text(encoding="utf-8")
    match = re.search(r"window\.COURSE_DATA = (.*?);\n  </script>", text, re.S)
    if not match:
        raise SystemExit("could not find COURSE_DATA in index.html")
    return json.loads(match.group(1).replace("<\\/", "</"))


def fragments(data: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for module in data["modules"]:
        out.append((f"body:{module['id']}", module["body"]))
        for exercise in module["exercises"]:
            for field in ("prompt", "hints", "solution", "stretch"):
                if exercise.get(field):
                    out.append((f"{field}:{exercise['id']}", exercise[field]))
    return out


PAIRS = [("<pre", "</pre>"), ("<table>", "</table>"), ("<ul>", "</ul>"), ("<ol>", "</ol>")]
PRE_BLOCK = re.compile(r"<pre class=\"code-block\".*?</pre>", re.S)
CODE_SPAN = re.compile(r"<code>.*?</code>", re.S)


def prose_only(frag: str) -> str:
    """Strip code blocks and inline code.

    Asterisks and backticks inside code are content, not markup - `alpha * cos`
    and a regex matching a fence are both correct output, not leaked markdown.
    """
    return CODE_SPAN.sub("", PRE_BLOCK.sub("", frag))


def check(name: str, frag: str) -> list[str]:
    problems = []
    for open_tag, close_tag in PAIRS:
        if frag.count(open_tag) != frag.count(close_tag):
            problems.append(f"unbalanced {open_tag}")
    if re.search(r"<p>[^<]*\|\s*-{2,}", frag):
        problems.append("table separator rendered as a paragraph")
    if re.search(r"<p>[^<]*\*\*[^*]+\*\*", frag):
        problems.append("unrendered bold in a paragraph")

    outside = prose_only(frag)
    if FENCE in outside:
        problems.append("literal code fence leaked outside a code block")
    if re.search(r"<p>#{1,6} ", outside):
        problems.append("unrendered heading in a paragraph")
    if re.search(r"(?<![\*\w])\*[^*\n]+\*(?![\*\w])", outside):
        problems.append("unrendered italic emphasis")
    return problems


def check_dom_contract(text: str) -> list[str]:
    """Every id the JS reaches for must exist in the static HTML.

    This is the failure that produces a blank page with a console error and no
    other symptom - exactly the kind of thing that survives a code review and
    dies on first open.
    """
    problems = []
    body = text.split("<script>")[0]
    for element_id in sorted(set(re.findall(r"getElementById\('([\w-]+)'\)", text))):
        if f'id="{element_id}"' not in body:
            problems.append(f"JS references #{element_id}, which is not in the HTML")
    for handler in ("showModule", "renderModuleList", "updateProgressBar", "init"):
        if f"function {handler}" not in text:
            problems.append(f"missing JS function {handler}")
    if "DOMContentLoaded" not in text:
        problems.append("no DOMContentLoaded hook - the page would never initialise")
    return problems


def main() -> int:
    data = load()
    frags = fragments(data)

    issues = [(name, problem) for name, frag in frags for problem in check(name, frag)]

    modules = len(data["modules"])
    exercises = sum(len(m["exercises"]) for m in data["modules"])
    tables = sum(f.count("<table>") for _, f in frags)
    blocks = sum(f.count('<pre class="code-block"') for _, f in frags)
    bold = sum(f.count("<strong>") for _, f in frags)

    print(f"modules           {modules}")
    print(f"exercises         {exercises}")
    print(f"fragments checked {len(frags)}")
    print(f"tables            {tables}")
    print(f"code blocks       {blocks}")
    print(f"bold spans        {bold}")

    # Structural expectations that would silently break navigation.
    ids = [m["id"] for m in data["modules"]]
    if len(set(ids)) != len(ids):
        issues.append(("*", "duplicate module ids"))
    exercise_ids = [e["id"] for m in data["modules"] for e in m["exercises"]]
    if len(set(exercise_ids)) != len(exercise_ids):
        issues.append(("*", "duplicate exercise ids - progress tracking would collide"))
    if any(not m.get("part") for m in data["modules"]):
        issues.append(("*", "module without a part - sidebar grouping breaks"))
    if any(not m["exercises"] for m in data["modules"]):
        issues.append(("*", "module with no exercises"))
    for problem in check_dom_contract(HTML.read_text(encoding="utf-8")):
        issues.append(("dom", problem))

    print(f"\nissues            {len(issues)}")
    for name, problem in issues[:30]:
        print(f"  {name}: {problem}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
