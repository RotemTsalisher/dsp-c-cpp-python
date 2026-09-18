"""Load the knowledge base into normalised Documents with provenance.

This is the only stage in the pipeline that touches the filesystem, and it is
pure: same input tree, same output. That property is what makes incremental
re-indexing possible later (Module 12) - if anything here stamped a timestamp
into the text, every rebuild would produce new content hashes.
"""
from __future__ import annotations

import re
import subprocess
from datetime import date, datetime
from pathlib import Path

from aicore.types import Document, Provenance

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")

# (glob, doc_type, authority). First match wins, so order matters.
CLASSIFICATION: list[tuple[str, str, str]] = [
    ("**/MODULE.md", "contract", "canonical"),
    ("docs/glossary.md", "glossary", "canonical"),
    ("docs/adr/*.md", "adr", "canonical"),
    ("docs/runbooks/*.md", "runbook", "canonical"),
    ("docs/triage/*.md", "triage", "historical"),
    ("modules/*/tests/**/*.py", "test", "canonical"),
    ("modules/**/*.py", "code", "canonical"),
    ("modules/**/*.[ch]", "code", "canonical"),
    ("vendor/**/*.md", "vendor", "external"),
]

SKIP_PARTS = {".git", "__pycache__", "node_modules", "build", "dist", ".venv"}


def classify(relative: Path) -> tuple[str, str] | None:
    posix = relative.as_posix()
    for pattern, doc_type, authority in CLASSIFICATION:
        if relative.match(pattern) or Path(posix).match(pattern):
            return doc_type, authority
    return None


def module_of(relative: Path) -> str:
    parts = relative.parts
    if "modules" in parts:
        index = parts.index("modules")
        if index + 1 < len(parts):
            return parts[index + 1]
    return "_shared"


def normalize(text: str) -> str:
    text = FRONT_MATTER.sub("", text)
    text = IMAGE.sub("", text)
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def git_updated(path: Path) -> date:
    """Last commit date, NOT file mtime.

    A fresh clone sets every mtime to now, which silently turns your entire
    recency signal into noise.
    """
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if out:
            return datetime.fromisoformat(out).date()
    except Exception:
        pass
    return date.fromtimestamp(path.stat().st_mtime)


def load_corpus(root: str | Path, *, use_git_dates: bool = True) -> list[Document]:
    root = Path(root)
    documents: list[Document] = []
    seen_hashes: dict[str, str] = {}

    for path in sorted(root.rglob("*")):           # sorted: determinism
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root)
        kind = classify(relative)
        if kind is None:
            continue
        doc_type, authority = kind

        text = normalize(path.read_text(encoding="utf-8", errors="replace"))
        if not text:
            continue

        content_hash = Document.make_content_hash(text)
        if content_hash in seen_hashes:            # exact duplicate, e.g. a vendored copy
            continue
        seen_hashes[content_hash] = relative.as_posix()

        documents.append(
            Document(
                doc_id=Document.make_doc_id(relative.as_posix()),
                text=text,
                content_hash=content_hash,
                prov=Provenance(
                    source=relative.as_posix(),
                    module=module_of(relative),
                    doc_type=doc_type,
                    authority=authority,
                    updated=git_updated(path) if use_git_dates else date.today(),
                ),
            )
        )
    return documents


def corpus_report(documents: list[Document]) -> dict:
    """Token and count breakdown. Sort by tokens, not by document count -
    one generated file can outweigh two hundred real documents."""
    from collections import Counter

    from aicore.llm import estimate_tokens

    by_type: Counter[str] = Counter()
    by_module: Counter[str] = Counter()
    by_authority: Counter[str] = Counter()
    for doc in documents:
        tokens = estimate_tokens(doc.text)
        by_type[doc.prov.doc_type] += tokens
        by_module[doc.prov.module] += tokens
        by_authority[doc.prov.authority] += tokens
    return {
        "documents": len(documents),
        "total_tokens": sum(by_type.values()),
        "tokens_by_doc_type": dict(by_type.most_common()),
        "tokens_by_module": dict(by_module.most_common()),
        "tokens_by_authority": dict(by_authority.most_common()),
        "largest": [
            (d.prov.source, estimate_tokens(d.text))
            for d in sorted(documents, key=lambda d: -estimate_tokens(d.text))[:5]
        ],
    }
