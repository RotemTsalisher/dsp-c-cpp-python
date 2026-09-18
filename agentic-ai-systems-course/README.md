# Agentic AI Systems Architecture

An advanced, hands-on course on designing AI-powered software systems: modular
decomposition for agent operability, vectorized knowledge bases, RAG as a
navigation layer, encapsulated sub-agents, and shipping AI features inside a real
product.

**41 modules · 173 exercises · naive baseline → production architecture**

## Open it

Double-click `index.html`. Any browser, no server, no build. Progress is saved in
`localStorage`, so you can close the tab and come back.

## Regenerate it

```bash
python generate_course.py     # writes index.html
```

`index.html` is generated - do not hand-edit it. All content lives in
`generate_course.py` in the `MODULES` list.

## Structure

| Part | Modules | What you build |
|---|---|---|
| 0 — Foundations | 00–02 | The naive whole-repo baseline, the experiment harness, context budgeting |
| 1 — Decomposition | 03–07 | Module contracts, generated interface surfaces, dependency fitness functions, a monolith split, parallel agents in worktrees |
| 2 — Vectorized knowledge | 08–12 | Corpus ingestion with provenance, structure- and AST-aware chunking, embedders, a vector store from scratch, incremental re-indexing and model migrations |
| 3 — RAG as GPS | 13–20 | The minimal loop, hybrid search with RRF, filtering and routing, query transformation, reranking and contextual retrieval, budgeted assembly with refusal, evaluation, and a failure-diagnosis lab |
| 4 — Encapsulated agents | 21–27 | An agent runtime with budgets and verification, tools as an API boundary, module agents, an orchestrator, specialist agents, the single-vs-multi experiment, failure classification and recovery |
| 5 — AI in a real product | 28–33 | Opportunity selection, NL→structured query, a grounded tuning advisor, agentic triage with a human gate, integration architecture, product evaluation |
| 6 — Production | 34–39 | Tracing and cost attribution, cost/latency engineering, security, reliability and human-in-the-loop, prompt and knowledge-base lifecycle, the capstone |
| ⚡ Drills | — | 12 short daily reps |

## The running project

Every module builds one system: **`acoustic-bench`**, a realistic audio
measurement and tuning platform. It starts as a 60k-line monolith and ends as a
decomposed, vectorized, agent-operated, evaluated system with three shipped AI
features. Nothing in the course is a standalone tutorial.

You are strongly encouraged to run a repository of your own in parallel (exercise
00-4). Your own code is the only place where you can tell a subtly wrong answer
from a right one, and that judgement is the entire evaluation signal in Parts 3
and 5.

## The starter kit

`starter/` is a runnable scaffold: provider-agnostic LLM and embedder interfaces,
two offline embedders, a 9-document sample knowledge base, a 20-task evaluation
set, a 26-case retrieval golden set, and 19 smoke tests.

```bash
cd starter
pip install -r requirements.txt
pytest -q            # 19 passed
```

**Everything in the course runs offline.** No API key is needed for any exercise,
because `FakeLLM` is scripted and deterministic and the embedders are local. Add a
real provider when you want to, not because the code forces you.

The starter deliberately omits chunking, the vector store, retrieval, agents, and
the evaluation harness. Those are the course.

## How the exercises work

Each exercise has a visible **Hint** and a **Reveal solution** button. Solutions
contain full working code plus the reasoning - read the reasoning, the code is the
easy part. Many exercises are debugging exercises with deliberately broken
implementations, and several ask you to measure a technique and then *reject* it
based on what you find.

## What you should end up with

- A system decomposed into modules with enforceable contracts
- A versioned, incrementally-maintained vector index with provenance
- A hybrid retrieval pipeline with reranking, budgeted assembly, and a refusal path
- Module agents with scoped context and tools, plus an orchestrator that verifies
- At least two AI features behind capability interfaces with deterministic fallbacks
- Golden sets and a CI gate that blocks per-case regressions and guardrail breaches
- Traces with full version context, cost attributed per outcome, and a prompt registry
- A `LOG.md` recording what actually worked on your system - including the things
  that did not

## Requirements

Python 3.9+, `numpy`, `pytest`. Everything else is optional and introduced where
it is needed.

## Audience

Experienced software engineers. It assumes you can program and that you have
called an LLM API; it does not assume you have built an agentic system. It is
written for someone who needs to design and defend one in production, so it
prioritises engineering reasoning and measurement over API walkthroughs.
