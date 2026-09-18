# MODULE: pipeline

## Responsibility
Compose capture, dsp and metrics into a measurement graph, run it, and hand the
results to storage. Owns the graph runtime, the configuration schema, and stage
scheduling.

Owns: the stage registry, graph execution order, buffer lifetime policy.
Does NOT own: any stage's implementation. It knows stage names, not stage internals.

## Public interface
<!-- GENERATED: do not edit by hand, see tools/api_surface.py -->
def run_graph(config: GraphConfig, payload: RunAudio) -> GraphResult
def validate_config(config: dict) -> GraphConfig
def registered_stages() -> list[str]
class GraphConfig(stages, parameters, device_family, firmware)
class GraphResult(run_id, metrics, artifacts, timings)
<!-- END GENERATED -->

## Invariants
- The pipeline depends on the **stage registry interface**, never on a concrete
  module. Stages register themselves; the pipeline resolves them by name from
  configuration. Adding a stage must not require editing this module.
- **The capture buffer is copied before it is handed to dsp.** Capture may reuse
  its buffer as soon as it returns. See ADR-017 for the ownership rule and the
  incident that produced it.
- Stage order is taken from configuration and is not reordered by the runtime,
  even when reordering would be faster. The baseline depends on order.
- A stage that raises aborts the graph. There is no partial-result path; a partial
  measurement is worse than no measurement.

## Dependencies
- ALLOWED: aicore.types, aicore.registry
- FORBIDDEN: direct imports of metrics, dsp, capture, fwbridge, storage

## Verification
    pytest modules/pipeline -q       # 2.4 s, uses fake stages only, no real DSP

## Change policy
- Adding a configuration field: additive, defaulted, no bump.
- Changing stage resolution or buffer ownership: MAJOR. Coordinate with every stage.
- Changing the abort-on-error policy: requires an ADR.

## Known failure modes
- A stage registered twice under the same name raises at import time. This is
  intentional: silent shadowing of a stage is far worse than a loud failure.
- Registration happens at import, so a stage module that is never imported is
  invisible. The entry-point list in configuration is the source of truth.
- Graph timings include stage import time on the first run of a process, which
  makes the first measurement of a session look slower than it is.

## Examples
```python
from modules.pipeline import run_graph, validate_config

config = validate_config({
    "stages": ["capture", "dsp", "metrics"],
    "parameters": {"dsp": {"agc_target_dbfs": -18}},
    "device_family": "DUT-7X",
    "firmware": "4.2",
})
result = run_graph(config, payload=None)
assert result.run_id
```

## Glossary references
GLOSSARY#frame-alignment, GLOSSARY#run

## Where things live
- Graph runtime: `modules/pipeline/runner.py`
- Config schema: `modules/pipeline/schema.py`
- Stage registry (shared): `aicore/registry.py`
