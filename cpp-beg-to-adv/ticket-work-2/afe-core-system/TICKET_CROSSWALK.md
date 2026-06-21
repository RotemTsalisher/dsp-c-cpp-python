# Ticket ↔ AFE core system crosswalk

**Test runner:** from `afe-core-system/`, build `afe_ticket_test` and run `.\build\Debug\afe_ticket_test.exe <TICKET-ID>`.

## Entry (`../entry-level/ticket_notebook.html`)

| Ticket ID | Symptom | Fix these files | Primary symbol |
|-----------|---------|-----------------|----------------|
| AFE-ENTRY-101 | Crash risk deleting encoder through `IEncoder*` | `include/afe/iencoder.hpp` | `IEncoder::~IEncoder` |
| AFE-ENTRY-102 | Duplex lane id lost in routing | `include/afe/route_channel.hpp`, `src/route_channel.cpp` | `route_channel_by_value` |
| AFE-ENTRY-103 | Response curve doubles through interface pointer | `src/response_curve.cpp` | `ResponseCurve::eval(double)` |
| AFE-ENTRY-104 | Stereo comb `operator+` drops right channel | `src/stereo_comb.cpp` | `operator+(StereoComb, StereoComb)` |
| AFE-ENTRY-105 | Factory calibration write is a no-op | `src/calibrated_gain.cpp` | `set_factory_cal` |

## Mid (`../mid-level/ticket_notebook.html`)

| Ticket ID | Symptom | Fix these files | Primary symbol |
|-----------|---------|-----------------|----------------|
| AFE-MID-201 | 16-bit field accepted in masked OR | `include/afe/register_mask.hpp` | `masked_or` |
| AFE-MID-202 | PSD bin worker never updates output | `src/psd_worker.cpp` | `run_psd_bin_once` |
| AFE-MID-203 | Tone silent through `WaveSource*` | `include/afe/wave_source.hpp` | `WaveSource::next_sample` |
| AFE-MID-204 | Fold negated deltas wrong sign/magnitude | `include/afe/fold_accumulator.hpp` | `fold_negated_from_zero` |
| AFE-MID-205 | Tap sifter ignores predicate | `src/tap_sifter.cpp` | `sift_tap` |

## Staff (`../staff-level/ticket_notebook.html`)

| Ticket ID | Symptom | Fix these files | Primary symbol |
|-----------|---------|-----------------|----------------|
| AFE-STAFF-301 | Signed add overflows at `INT_MAX` | `src/safe_add.cpp` | `safe_add_i32` |
| AFE-STAFF-302 | Plugin export header wrong ABI size | `include/afe/export_layout.hpp` | `PluginExportHeader` layout |
| AFE-STAFF-303 | Audit token never stored | `src/audit_gate.cpp` | `set_audit_token` |
| AFE-STAFF-304 | API revision below contract | `src/api_revision.cpp` | `api_revision` |
| AFE-STAFF-305 | Mono-mix energy wrong after comb merge | `src/stereo_comb.cpp` | `operator+(StereoComb, StereoComb)` |

## Notes

- Do **not** edit `tests/ticket_tests.cpp` unless a ticket explicitly says so.
- Canonical code uses **snake_case**; tickets may reference camelCase aliases in prose only.
