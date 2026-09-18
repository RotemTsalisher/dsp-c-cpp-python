"""Core data types shared by every stage of the pipeline.

These are deliberately small and frozen. Everything downstream - chunking,
embedding, retrieval, assembly, agents - depends on this module and on nothing
else, which is what keeps `_shared` a leaf in the dependency graph.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Provenance:
    """Where a piece of knowledge came from, and how much to trust it.

    Every field here exists because some later stage needs it:
      module     -> retrieval scoping (Module 15) and agent isolation (Module 23)
      doc_type   -> metadata filtering
      authority  -> conflict resolution when sources disagree (Module 08)
      updated    -> recency weighting and staleness reporting (Module 12)
      access     -> enforced at index time AND query time (Module 36)
    """

    source: str
    module: str
    doc_type: str          # contract | adr | code | test | runbook | triage | vendor | glossary
    authority: str         # canonical | derived | historical | external | untrusted
    updated: date
    version: str = ""
    anchor: str = ""
    lang: str = "en"
    access: str = "internal"


@dataclass(frozen=True)
class Document:
    """A normalised source document.

    doc_id is derived from the PATH so it survives edits (citations stay valid).
    content_hash is derived from the TEXT so incremental re-indexing can tell
    what actually changed. Conflating the two is the root of most duplicate-chunk
    bugs - see Module 12.
    """

    doc_id: str
    text: str
    prov: Provenance
    content_hash: str = ""

    @staticmethod
    def make_doc_id(relative_path: str) -> str:
        return hashlib.sha256(relative_path.encode()).hexdigest()[:16]

    @staticmethod
    def make_content_hash(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()


@dataclass(frozen=True)
class Chunk:
    """The unit of retrieval AND the unit of context.

    chunk_id is content-addressed (`doc_id:ordinal:hash8`) so that inserting a
    paragraph does not invalidate every citation downstream of it.
    """

    chunk_id: str
    doc_id: str
    text: str
    prov: Provenance
    ordinal: int = 0
    heading_path: tuple[str, ...] = field(default_factory=tuple)
    token_count: int = 0

    @staticmethod
    def make_chunk_id(doc_id: str, ordinal: int, content_hash: str) -> str:
        return f"{doc_id}:{ordinal}:{content_hash[:8]}"


@dataclass
class Hit:
    """A retrieval result. `score` is comparable only within one retriever."""

    chunk: Chunk
    score: float
    rank: int = 0
    channel: str = ""      # "vector" | "bm25" | "fused" | "reranked"
