"""Smoke tests for the starter kit.

These assert the three properties every later exercise depends on:
  1. the offline LLM is deterministic and records its calls
  2. embedders produce L2-normalised vectors with stable, process-independent keys
  3. the corpus loads with complete provenance

If any of these fail, stop and fix them before starting Module 01.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from aicore.corpus import corpus_report, load_corpus
from aicore.embed import CachedEmbedder, HashEmbedder, TfidfEmbedder
from aicore.llm import FakeLLM, Message, estimate_tokens
from aicore.types import Chunk, Document

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
HARNESS = ROOT / "harness"
EXPECTED_DOCS = 9


# --------------------------------------------------------------------------
# LLM
# --------------------------------------------------------------------------
def test_fake_llm_is_deterministic_and_records_calls():
    llm = FakeLLM().on(r"tolerance", "The THD+N tolerance is expressed in percent. [1]")
    messages = [Message("system", "be grounded"), Message("user", "what is the tolerance unit?")]

    first = llm.complete(messages)
    second = llm.complete(messages)

    assert first.text == second.text
    assert len(llm.calls) == 2
    assert llm.calls[0]["input_tokens"] > 0
    assert first.input_tokens > 0 and first.output_tokens > 0


def test_fake_llm_default_is_a_refusal():
    # The default must be a refusal, not a plausible answer. A scripted model that
    # invents content when unscripted makes every trap-case test meaningless.
    response = FakeLLM().complete([Message("user", "anything unscripted")])
    assert response.text.startswith("NOT_IN_CONTEXT")


def test_fake_llm_can_emit_tool_calls():
    llm = FakeLLM().on(r"read the contract", tool=("read_file", {"path": "MODULE.md"}))
    response = llm.complete([Message("user", "please read the contract")])
    assert response.tool_calls and response.tool_calls[0].name == "read_file"


def test_token_estimate_distinguishes_code_from_prose():
    prose = "The tolerance for total harmonic distortion is expressed as a percentage."
    code = "if (agc->attack_ms <= 0) { return -EINVAL; } state->gain_q15 = (int16_t)(g * 32768);"
    assert estimate_tokens(prose) > 0
    # Code packs more tokens per character than prose of the same length.
    assert estimate_tokens(code) / len(code) > estimate_tokens(prose) / len(prose)


# --------------------------------------------------------------------------
# Embedders
# --------------------------------------------------------------------------
@pytest.mark.parametrize("embedder", [HashEmbedder(dim=128), TfidfEmbedder(dim=128)])
def test_vectors_are_l2_normalised(embedder):
    texts = ["short", "a considerably longer passage about automatic gain control behaviour"]
    if isinstance(embedder, TfidfEmbedder):
        embedder.fit(texts)
    vectors = embedder.embed(texts)
    assert vectors.shape == (2, 128)
    assert np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-4)


def test_embedding_is_stable_across_processes():
    # Python salts hash() per process. If an embedder used it, the vector for the
    # same text would differ after a restart and the index would be unqueryable.
    code = (
        "import sys, json, numpy as np;"
        "sys.path.insert(0, %r);"
        "from aicore.embed import HashEmbedder;"
        "print(json.dumps(HashEmbedder(dim=32).embed(['agc attack'])[0].tolist()))"
        % str(ROOT)
    )
    runs = [
        json.loads(subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout)
        for _ in range(2)
    ]
    assert np.allclose(runs[0], runs[1]), "embedding is not stable across processes"


def test_tfidf_requires_fit():
    with pytest.raises(RuntimeError, match="fit"):
        TfidfEmbedder().embed(["anything"])


class CountingEmbedder:
    """Spy that reports how many texts actually reached the inner embedder.

    Asserting on call counts is a much stronger cache test than comparing
    vectors: two embedders fitted on the same corpus produce identical output,
    so a stale-cache bug is invisible in the values.
    """

    def __init__(self, inner):
        self.inner = inner
        self.texts = 0
        self.dim = inner.dim
        self.name = inner.name

    def embed(self, texts, *, is_query=False):
        self.texts += len(texts)
        return self.inner.embed(texts, is_query=is_query)


def test_cached_embedder_avoids_recomputation(tmp_path):
    corpus = ["gain is linear", "frame index is in 128 sample frames", "q15 at the C boundary"]
    spy = CountingEmbedder(TfidfEmbedder(dim=64).fit(corpus))
    cached = CachedEmbedder(spy, tmp_path / "vectors.npz")

    cached.embed(corpus)
    after_first = spy.texts
    cached.embed(corpus)

    assert spy.texts == after_first, "cache miss on unchanged input"
    assert cached.hits == len(corpus)


def test_cache_key_includes_model_name(tmp_path):
    # Without the model name in the key, switching embedders serves vectors from
    # the old geometry: document vectors from one model, query vectors from
    # another, plausible scores, meaningless ranking, and no error anywhere.
    corpus = ["gain is linear", "frame index"]
    path = tmp_path / "vectors.npz"

    first = CountingEmbedder(TfidfEmbedder(dim=64).fit(corpus))
    CachedEmbedder(first, path).embed(["gain is linear"])
    assert first.texts == 1

    other = TfidfEmbedder(dim=64).fit(corpus)
    other.name = "different-embedder-v2"
    second = CountingEmbedder(other)
    CachedEmbedder(second, path).embed(["gain is linear"])

    assert second.texts == 1, "served a cached vector computed by a different embedder"


def test_cache_key_distinguishes_query_from_document(tmp_path):
    # Models with asymmetric prefixes embed the same text differently as a query
    # and as a document. One key for both silently mixes them.
    corpus = ["gain is linear"]
    spy = CountingEmbedder(TfidfEmbedder(dim=64).fit(corpus))
    cached = CachedEmbedder(spy, tmp_path / "vectors.npz")

    cached.embed(corpus, is_query=False)
    cached.embed(corpus, is_query=True)

    assert spy.texts == 2, "query and document embeddings shared a cache key"


# --------------------------------------------------------------------------
# Corpus
# --------------------------------------------------------------------------
def test_corpus_loads_with_full_provenance():
    docs = load_corpus(KB, use_git_dates=False)
    assert len(docs) == EXPECTED_DOCS, f"expected {EXPECTED_DOCS} documents, got {len(docs)}"

    for doc in docs:
        assert doc.doc_id and doc.content_hash
        assert doc.prov.source and doc.prov.module and doc.prov.doc_type and doc.prov.authority
        assert doc.prov.access == "internal"

    by_type = {d.prov.doc_type for d in docs}
    assert {"contract", "adr", "glossary", "triage", "runbook"} <= by_type

    modules = {d.prov.module for d in docs}
    assert {"metrics", "dsp", "pipeline", "_shared"} <= modules


def test_corpus_load_is_deterministic():
    first = load_corpus(KB, use_git_dates=False)
    second = load_corpus(KB, use_git_dates=False)
    assert [d.doc_id for d in first] == [d.doc_id for d in second]
    assert [d.content_hash for d in first] == [d.content_hash for d in second]


def test_doc_id_survives_edits_but_content_hash_does_not():
    # doc_id keyed on path -> citations stay valid across edits.
    # content_hash keyed on text -> incremental re-indexing knows what changed.
    a = Document.make_doc_id("modules/metrics/MODULE.md")
    b = Document.make_doc_id("modules/metrics/MODULE.md")
    assert a == b
    assert Document.make_content_hash("v1") != Document.make_content_hash("v2")


def test_chunk_ids_are_content_addressed():
    first = Chunk.make_chunk_id("abc123", 4, Document.make_content_hash("original"))
    edited = Chunk.make_chunk_id("abc123", 4, Document.make_content_hash("edited"))
    assert first != edited, "chunk id must change when content changes"


def test_superseded_adr_is_present_and_findable():
    # Module 08 needs a real conflict in the corpus: ADR-009 is superseded by
    # ADR-017 and is more verbose on the shared topic, so pure similarity
    # search ranks the wrong one first.
    docs = {d.prov.source: d for d in load_corpus(KB, use_git_dates=False)}
    old = docs["docs/adr/ADR-009-capture-buffer-sharing.md"]
    new = docs["docs/adr/ADR-017-buffer-ownership.md"]
    assert "SUPERSEDED" in old.text
    assert "supersedes ADR-009" in new.text


def test_corpus_report_is_sorted_by_tokens():
    report = corpus_report(load_corpus(KB, use_git_dates=False))
    assert report["documents"] == EXPECTED_DOCS
    assert report["total_tokens"] > 0
    sizes = [tokens for _, tokens in report["largest"]]
    assert sizes == sorted(sizes, reverse=True)


# --------------------------------------------------------------------------
# Evaluation data
# --------------------------------------------------------------------------
def test_task_set_is_wellformed():
    tasks = [json.loads(line) for line in (HARNESS / "tasks.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(tasks) == 20
    assert {t["category"] for t in tasks} == {"locate", "explain", "change", "trap"}
    assert all(t["oracle"]["type"] in {"contains_all", "contains_any", "file_set", "must_refuse"} for t in tasks)

    traps = [t for t in tasks if t["category"] == "trap"]
    assert len(traps) >= 3, "an eval set without trap cases measures confidence, not correctness"
    assert all(t["oracle"]["type"] == "must_refuse" for t in traps)


def test_golden_set_has_all_segments_and_enough_traps():
    cases = [json.loads(line) for line in (HARNESS / "retrieval_golden.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    segments = {c["segment"] for c in cases}
    assert {"conceptual", "identifier", "exact_string", "numeric", "multi_hop", "trap"} <= segments

    traps = [c for c in cases if not c["answerable"]]
    assert len(traps) / len(cases) >= 0.15, "trap cases should be at least 15% of the golden set"

    sources = {d.prov.source for d in load_corpus(KB, use_git_dates=False)}
    for case in cases:
        if case["answerable"]:
            assert case["expect_source"] in sources, f"{case['id']} points at a missing document"
