# ADR-009: Share the capture buffer with downstream stages

- Status: **SUPERSEDED by ADR-017**
- Date: 2024-06-11
- Deciders: platform, dsp

> This decision is retained for history. It describes how the system used to
> work and must not be used to justify current behaviour. If you are reading
> this to answer a question about how buffers are handled today, read ADR-017.

## Context

The measurement pipeline acquires audio from the sound card into a buffer owned
by the capture stage, then passes it to the DSP stage and then to metrics. At the
block sizes we use (128 samples at 48 kHz), a full copy per block was measured at
roughly 4% of total pipeline CPU on the reference host.

We were optimising for throughput on long sweeps, where a 30-second measurement
involves around 11,000 blocks, and the copy appeared to be pure overhead. The DSP
kernels do not write to their input buffer, so sharing looked safe by inspection.

## Decision

The capture stage passes a **reference** to its internal buffer to downstream
stages. Downstream stages must treat the buffer as read-only and must not retain
a reference beyond the duration of their `run()` call.

## Consequences

- Saves approximately 4% pipeline CPU and one allocation per block.
- Creates an unwritten contract: every downstream stage must finish with the
  buffer before capture reuses it. This is not expressible in the type system
  and is not checked anywhere.
- Any stage that becomes asynchronous, buffers internally, or hands the data to
  another thread will read data that capture has already overwritten.

## Notes

At the time this was written, all stages were synchronous and single-threaded,
which made the unwritten contract look like a safe assumption rather than a
temporal coupling waiting to be exercised.
