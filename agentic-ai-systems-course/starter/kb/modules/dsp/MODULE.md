# MODULE: dsp

## Responsibility
Process audio blocks in real time: biquad filtering, automatic gain control,
noise suppression, and echo cancellation. Owns the kernel implementations and
the fixed-point conventions at the C boundary.

Owns: kernel implementations, Q-format rules, parameter defaults and safe ranges.
Does NOT own: capture, metric computation, tolerances, persistence.

## Public interface
<!-- GENERATED: do not edit by hand, see tools/api_surface.py -->
void biquad_process(const float *in, float *out, uint32_t n, const BiquadCoeffs *c, BiquadState *st)
void agc_process(const int16_t *in, int16_t *out, uint32_t n, const AgcParams *p, AgcState *st)
void ns_process(const int16_t *in, int16_t *out, uint32_t n, const NsParams *p, NsState *st)
void aec_process(const int16_t *near, const int16_t *far, int16_t *out, uint32_t n, AecState *st)
struct AgcParams { int16_t attack_ms; int16_t release_ms; int16_t target_dbfs; }
struct BiquadCoeffs { float b0, b1, b2, a1, a2; }
<!-- END GENERATED -->

## Invariants
- The C kernels take **Q15 int16** blocks. The Python binding converts; callers
  above the binding work in float. See GLOSSARY#q15.
- Gain values crossing the boundary are **linear**, never dB. See GLOSSARY#gain-linear.
- Block size is fixed at **128 samples at 48 kHz**. Kernels do not handle partial
  blocks; the pipeline pads.
- Kernels never allocate. All state is caller-provided and caller-owned.
- `agc_process` and `ns_process` may be chained in either order, but the chosen
  order must match the order used when the baseline was recorded.

## Tunable parameters
| parameter          | unit | min  | max  | default | tunable |
|--------------------|------|------|------|---------|---------|
| agc_attack_ms      | ms   | 1    | 50   | 12      | yes     |
| agc_release_ms     | ms   | 20   | 2000 | 250     | yes     |
| agc_target_dbfs    | dBFS | -30  | -6   | -18     | yes     |
| ns_gain_floor_db   | dB   | -30  | 0    | -12     | yes     |
| ns_overshoot_guard | -    | 0    | 1    | 1       | yes     |

The AGC attack-time constant `AGC_ATTACK_MS_DEFAULT` is defined in
`modules/dsp/agc_params.h` and is the single source of truth for the default.
Do not duplicate it in Python.

## Dependencies
- ALLOWED: aicore.types, numpy (binding layer only)
- FORBIDDEN: metrics, storage, api, capture, pipeline, fwbridge

## Verification
    ctest --test-dir build -R dsp     # 3.1 s, host build, no hardware
    pytest modules/dsp -q             # binding tests, 1.2 s

## Change policy
- Changing a kernel's numeric behaviour: requires a golden-vector diff and a
  baseline re-run across all device families.
- Changing a default parameter: requires an ADR. Defaults are shipped in firmware.
- Changing the block size or Q-format: MAJOR. Coordinate with capture and pipeline.

## Known failure modes
- At input levels below -45 dBFS the AGC ramp is dominated by quantisation and
  overshoot measurements become unreliable.
- `ns_process` at a gain floor below -24 dB introduces audible pumping on speech
  onsets. Reported repeatedly; no fix, use the guard.
- The AEC has no documented default tail length in this repository. Values differ
  per product and are configured at integration time. Do not guess one.

## Examples
```c
/* Q15 in, Q15 out. The caller owns the state; the kernel never allocates. */
AgcState st = {0};
AgcParams p = { .attack_ms = AGC_ATTACK_MS_DEFAULT, .release_ms = 250, .target_dbfs = -18 };
agc_process(in_q15, out_q15, 128, &p, &st);
```

## Glossary references
GLOSSARY#q15, GLOSSARY#gain-linear, GLOSSARY#dbfs, GLOSSARY#frame-alignment

## Where things live
- AGC parameter defaults: `modules/dsp/agc_params.h`
- AGC implementation: `modules/dsp/agc.c`
- Biquad: `modules/dsp/biquad.c`
- Python binding: `modules/dsp/binding.py`
