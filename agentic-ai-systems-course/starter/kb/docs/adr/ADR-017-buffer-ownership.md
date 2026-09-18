# ADR-017: The pipeline copies the capture buffer before handing it downstream

- Status: **Accepted** (supersedes ADR-009)
- Date: 2025-02-03
- Deciders: platform, dsp, audio-quality

## Context

ADR-009 had downstream stages receive a reference to the capture stage's internal
buffer, saving a copy per block. That worked while every stage was synchronous.

In January 2025 the noise-suppression stage gained an internal lookahead of two
blocks, so that it could see a transient before deciding its gain. The lookahead
retained a reference to its input past the end of its `run()` call. Capture,
meanwhile, reused its buffer immediately on return.

The result was a **data race with no crash**. The NS stage read blocks that had
been partially overwritten with newer audio. The corrupted samples were valid
audio, just from the wrong moment, so nothing raised and nothing looked obviously
wrong. It surfaced as intermittent THD+N failures on roughly one run in twenty,
on long sweeps only, and only on hosts where the capture callback ran on a
separate thread.

It took eleven days to diagnose. The measurement that finally identified it was
noticing that failures correlated with sweep length rather than with any
parameter, which pointed at buffer reuse rather than at signal processing.

## Decision

The pipeline **copies** the capture buffer before handing it to any downstream
stage. Ownership of the copy transfers to the pipeline, and the pipeline
guarantees its lifetime for the duration of the graph execution.

Buffer ownership is now stated explicitly in the `pipeline` module contract as an
invariant, not left as an unwritten assumption.

## Consequences

- Costs approximately 4% pipeline CPU, which we accept. Measurement correctness
  dominates measurement throughput; a fast wrong number has negative value.
- Stages may now retain references to their input for the duration of the graph,
  which is what made the NS lookahead possible.
- The temporal coupling introduced by ADR-009 is removed. A new stage cannot
  reintroduce the bug by being asynchronous.
- ADR-009 is superseded. Any code or documentation still describing buffer
  sharing is describing a system that no longer exists.

## The general lesson

The 4% we saved in ADR-009 was real and measurable. The cost was an **invisible
temporal coupling** - a rule that lived in nobody's interface and in one person's
memory. It stayed free for eight months and then cost eleven days.

Prefer explicit ownership over shared references at module boundaries, and when
you do take a coupling for performance, write it into the contract where the next
person will read it.
