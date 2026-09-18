# MODULE: metrics

## Responsibility
Convert captured audio into scalar quality numbers, and decide whether each
number is within tolerance for the device family under test.

Owns: metric definitions, tolerance tables, pass/fail decisions.
Does NOT own: audio capture, DSP processing, persistence, presentation.

## Public interface
<!-- GENERATED: do not edit by hand, see tools/api_surface.py -->
def compute(run: RunAudio, spec: MetricSpec) -> MetricResult
def compute_all(run: RunAudio, specs: list[MetricSpec]) -> list[MetricResult]
def list_metrics() -> list[MetricName]
def tolerance_for(metric: MetricName, family: DeviceFamily) -> Tolerance | None
class MetricResult(name, value, unit, frame_index, tolerance, passed)
class MetricSpec(name, window_frames, reference)
class Tolerance(metric, family, limit, comparator, unit)
<!-- END GENERATED -->

## Invariants
- `MetricResult.value` is always expressed in the unit named by `MetricResult.unit`.
  THD+N is in **percent**, never dB. SNR and AGC overshoot are in **dB**.
- Any gain value crossing this module's boundary is **linear**, never dB.
  See GLOSSARY#gain-linear.
- `frame_index` is counted in **128-sample frames at 48 kHz**, relative to the
  start of the processed region, not the start of the file.
  See GLOSSARY#frame-alignment.
- `compute()` is pure: no I/O, no global state, deterministic for identical input.
- A metric with no tolerance defined for a device family returns `passed=None`,
  never `False`. Absence of a rule is not a failure.

## Tunable parameters
| parameter            | unit    | min | max | tunable |
|----------------------|---------|-----|-----|---------|
| thd_n_tolerance      | percent | 0.1 | 5.0 | NO      |
| snr_tolerance        | dB      | 20  | 90  | NO      |
| agc_overshoot_tol    | dB      | 0.5 | 6.0 | NO      |

Tolerances are acceptance criteria, not tuning knobs. Widening a tolerance to
make a run pass is a symptom fix; fix the device, not the ruler.

## Dependencies
- ALLOWED: numpy, aicore.types
- FORBIDDEN: storage, api, capture, pipeline, fwbridge

`metrics` is a leaf. It receives its tolerance table as an argument; it does not
look one up. That inversion is what makes it independently testable.

## Verification
    pytest modules/metrics -q        # 0.8 s, no hardware, no network, no database

## Change policy
- Adding a metric: additive, no contract version bump.
- Changing a default tolerance: requires an ADR and a baseline re-run. It breaks
  every stored comparison.
- Changing a unit or the frame convention: MAJOR. Coordinate with storage and webui.

## Known failure modes
- THD+N is undefined below -60 dBFS input and returns NaN. Callers must handle it.
- The latency metric assumes a single dominant correlation peak. Multi-path
  fixtures break it - see ADR-031.
- `agc_overshoot_db` is measured over the first 500 ms after level change only.
  A late overshoot is not detected.

## Examples
```python
from modules.metrics import compute, MetricSpec
from aicore.types import RunAudio

result = compute(RunAudio.fixture("dut7_sweep"), MetricSpec("thd_n"))
assert result.unit == "percent"      # NOT dB - see Invariants
assert result.frame_index is None    # scalar metrics carry no frame index
assert 0.0 <= result.value <= 100.0
```

```python
from modules.metrics import tolerance_for

assert tolerance_for("thd_n", "DUT-9X") is None    # no rule for a new family
```

## Glossary references
GLOSSARY#gain-linear, GLOSSARY#frame-alignment, GLOSSARY#dbfs

## Where things live
- Metric implementations: `modules/metrics/compute.py`
- Tolerance tables and per-family overrides: `modules/metrics/tolerances.py`
- Fixtures: `modules/metrics/tests/fixtures/*.npy`
