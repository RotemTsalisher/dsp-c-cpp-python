# bench-ai starter kit

The scaffolding for the **Agentic AI Systems Architecture** course. It gives you
the parts that are infrastructure rather than lesson, so you can start building
the parts that are.

## What is here

```
aicore/          provider-agnostic LLM and embedder interfaces, offline implementations
  types.py       Document, Chunk, Provenance, Hit
  llm.py         LLM protocol, FakeLLM (scripted, deterministic), provider adapter
  embed.py       Embedder protocol, HashEmbedder, TfidfEmbedder, CachedEmbedder
  corpus.py      load the knowledge base with full provenance
kb/              9-document sample knowledge base for acoustic-bench
harness/         tasks.jsonl (20 tasks), retrieval_golden.jsonl (26 cases)
tests/           smoke tests - these must pass before Module 01
```

## What is deliberately NOT here

Chunking, the vector store, retrieval, fusion, reranking, assembly, agents, the
orchestrator, and the evaluation harness. Those are the course. Building them is
the point, and the solutions are behind the Reveal buttons when you want them.

## Setup

```bash
git init bench-ai && cd bench-ai
cp -r <course-folder>/starter/* .
python -m venv .venv && . .venv/Scripts/activate   # Windows; bin/activate elsewhere
pip install -r requirements.txt
pytest -q          # 19 passed
echo "# Experiment log" > LOG.md
git add -A && git commit -m "starter kit"
```

Everything runs offline. No API key is required for any exercise, at any point in
the course.

## Going online

```bash
export BENCH_AI_PROVIDER=openai       # aicore.llm.get_llm()
export BENCH_AI_MODEL=gpt-4.1-mini
export BENCH_AI_EMBEDDER=openai       # aicore.embed.get_embedder()
export BENCH_AI_EMBED_MODEL=text-embedding-3-small
pip install openai
```

Nothing outside `aicore/llm.py` and `aicore/embed.py` imports a provider SDK, and
nothing should. That single indirection is what makes fallbacks, cost accounting,
model routing, shadow mode, and offline tests possible later.

## The two offline embedders, and why there are two

`HashEmbedder` is a bag of words. It is **not semantic**: "clipping" and
"saturation" are orthogonal to it, and `agc_attack_ms` shares nothing with "AGC
attack time". It exists so you can feel what semantics buys before you pay for it.

`TfidfEmbedder` uses character n-grams with idf. It is genuinely useful offline:
strong on identifiers and typos, weak on synonymy. That split is the empirical
argument for hybrid search in Module 14, discoverable on your laptop.

Both are L2-normalised and both use `blake2b` rather than Python's `hash()`,
which is salted per process and would make any persisted index unqueryable after
a restart.

## The sample knowledge base

Nine documents describing `acoustic-bench`, a fictional but realistic audio
measurement platform:

| Document | Why it is in the corpus |
|---|---|
| `modules/metrics/MODULE.md` | A complete module contract with invariants and examples |
| `modules/dsp/MODULE.md` | A contract with a tunable-parameter table and safe ranges |
| `modules/pipeline/MODULE.md` | An orchestrating module with a registry dependency |
| `docs/glossary.md` | The shared conventions that cause silent bugs when violated |
| `docs/adr/ADR-009-...` | **Superseded.** More verbose than its replacement on purpose |
| `docs/adr/ADR-017-...` | Supersedes ADR-009; the authority-conflict case |
| `docs/adr/ADR-031-...` | A metric that fails quietly; the "confident wrong number" case |
| `docs/triage/2026-03-...` | Tuning knowledge that must NOT transfer across device families |
| `docs/runbooks/rerun-baseline.md` | Procedural knowledge, a different retrieval shape |

The corpus is small enough to read in twenty minutes and is worth reading before
Module 01. Several exercises depend on knowing what is *not* in it.

## Evaluation data

`harness/tasks.jsonl` - 20 end-to-end tasks in four categories. The **trap**
category is unanswerable from this corpus and the correct behaviour is refusal.
An eval set without trap cases measures confidence, not correctness.

`harness/retrieval_golden.jsonl` - 26 retrieval cases across six segments, keyed
by `expect_source` and `expect_contains` rather than by chunk id, because you have
not built a chunker yet. In Module 19 you resolve these to chunk ids and add your
own hand-labelled cases.

## Planted problems

Two things in here are deliberately wrong, and both are load-bearing for exercises:

1. **ADR-009 is superseded by ADR-017** and is more verbose on the shared topic,
   so a pure-similarity search ranks the obsolete document first. Module 08.
2. **The AEC tail length is not documented anywhere.** The `dsp` contract says so
   explicitly. Any system that answers `T-18` with a number is confabulating.
   Modules 13 and 18.

## Layout you will grow into

```
bench-ai/
  aicore/         given
  kb/             given (replace with your own repo's docs when ready)
  harness/        given data; you write metrics.py, oracle.py, run_eval.py, budget.py
  modules/        Part 1  - contracts, manifests, module code
  tools/          Part 1  - manifest, api_surface, deps, ratchet
  rag/            Part 3  - chunking, store, bm25, fusion, rerank, assemble
  agents/         Part 4  - runtime, tools, module agents, orchestrator
  features/       Part 5  - ask_bench, advisor, triage
  obs/            Part 6  - spans, cost, redaction
  prompts/        Part 6  - versioned prompt registry
  eval/           Part 5-6 - golden sets and gates
  LOG.md          every experiment: what changed, before, after
```

## LOG.md

Start it on day one. Three lines per experiment: what you changed, what the number
was before, what it is after. By the capstone this file is worth more than the
code - it is the only record of which techniques actually worked on *your* system,
and several of them will not be the ones you expected.
