# Glossary

Shared vocabulary for acoustic-bench. Every module contract references the
entries it depends on by anchor. These are the conventions that, when violated,
produce code that compiles, passes its tests, and is quietly wrong - which is
the most expensive failure class in this system.

## gain-linear
All gain values crossing a module boundary are **linear floats**, never decibels.
dB appears only in metric output and in the user interface, and is always
labelled as such by `MetricResult.unit`.

Boundary assertion: `assert 0.0 <= g <= 16.0`. A linear gain above 16 is +24 dB,
which no signal path in this product legitimately requests - so a value above it
is almost certainly a dB value that was passed through unconverted.

Depended on by: dsp, capture, metrics, api.

## q15
The C kernels in `dsp` operate on **Q15 int16** samples: a signed 16-bit integer
interpreted as a fraction in [-1, 1), with 15 fractional bits. Conversion happens
in the Python binding layer and nowhere else.

Boundary assertion: the binding checks `block.dtype == np.int16` and that at
least one sample exceeds +/-1024 in magnitude - a float buffer that was cast
rather than scaled collapses to near-zero integers and is otherwise silent.

Depended on by: dsp, pipeline.

## frame-alignment
Frame indices returned by `metrics` are counted in **frames of 128 samples at
48 kHz** (2.667 ms per frame), and are relative to the start of the **processed**
region, not the start of the recorded file. The processed region excludes the
leading silence trimmed by capture.

Boundary assertion: storage rejects any frame index above
`duration_s * 48000 / 128 * 1.01`.

Depended on by: metrics, storage, webui.

## dbfs
Levels expressed in dBFS are relative to full scale, where 0 dBFS is a full-scale
sine, not a full-scale square. A signal at -18 dBFS therefore has an RMS of
0.126 relative to full scale.

Depended on by: dsp, metrics, capture.

## run
A **run** is one execution of a measurement graph against one device under test,
with one parameter set and one firmware version. It is the unit of storage, the
unit of comparison, and the unit a baseline is defined over. A run is immutable
once written; re-measuring produces a new run.

Depended on by: storage, api, pipeline, webui.

## baseline
A **baseline** is a named run designated as the reference for a device family and
firmware. Regression detection compares a new run's metrics against its baseline
run's metrics, per metric, using the tolerance for that family.

Changing which run is the baseline invalidates every stored comparison that
referenced the previous one. It requires an ADR.

Depended on by: storage, metrics, api.

## device family
A **device family** groups hardware that shares an acoustic design and therefore
shares tolerances and tuning. `DUT-7X` and `DUT-5` are different families and
their tuning does **not** transfer, even when the symptom looks identical. Tuning
advice derived from one family must be explicitly qualified when applied to another.

Depended on by: metrics, storage, api, fwbridge.
