# ADR-031: Latency metric assumes a single dominant path

- Status: Accepted
- Date: 2025-09-18
- Deciders: audio-quality

## Context

The latency metric estimates end-to-end delay by cross-correlating the played
reference against the recorded return and taking the position of the correlation
peak. This is correct and robust when there is one acoustic path.

Two fixture configurations break the assumption:

1. **Reflective enclosures.** The DUT-7X test fixture has a hard rear wall about
   38 cm behind the device, producing a reflection at roughly 2.2 ms. When the
   direct path is attenuated - which happens at low playback levels or with the
   device rotated off-axis - the reflection can win the correlation and the
   reported latency jumps by one to three frames.

2. **Devices with an internal secondary path.** Some conferencing endpoints mix a
   locally-processed sidetone into the return. The sidetone arrives earlier than
   the acoustic path and the correlation locks onto it, reporting a latency that
   is real but is not the quantity we intended to measure.

Both failures are **quiet**. The metric returns a plausible number with a strong
correlation peak, and the run passes or fails against tolerance as though the
number meant what we think it means.

## Decision

Keep the single-peak estimator. Do not attempt multi-path decomposition in the
metrics module.

Instead:

- Document the assumption in the `metrics` contract under Known Failure Modes.
- Report the **peak-to-second-peak ratio** alongside the latency value. A ratio
  below 6 dB means the estimate is ambiguous and should not be trusted.
- Treat fixture geometry as a property of the measurement setup, recorded with
  the run, not as something the metric compensates for.

## Consequences

- Latency results on multi-path fixtures remain unreliable, and are now
  *identifiably* unreliable rather than silently wrong.
- Any regression triage that involves a latency change must check the
  peak-to-second-peak ratio before treating the change as real. A latency jump of
  exactly one to three frames with a low ratio is a fixture artifact, not a
  firmware regression.
- We accept that fixing this properly requires a deconvolution-based estimator,
  which is a larger piece of work and has not been scheduled.

## Related

- The frame convention for the reported index is in GLOSSARY#frame-alignment.
- Fixture geometry per family is recorded in the run metadata, not in this module.
