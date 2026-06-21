# Ticket ↔ VLC core system crosswalk

Each row maps a **QA ticket** to the **file(s) that contain the defect** and the **automated check** you run after patching.

**Test runner:** from `vlc-core-system/`, build `vlc_ticket_test` and run `.\build\Debug\vlc_ticket_test.exe <TICKET-ID>` (see `README.md`).

## Entry (`../entry-level/ticket_notebook.html`)

| Ticket ID | Symptom | Fix these files | Primary symbol |
|-----------|---------|-----------------|----------------|
| VLC-ENTRY-101 | Mono mix ~6 dB hot | `src/mono_mix.cpp` | `mono_mix_down` / `monoMixDown` |
| VLC-ENTRY-102 | ADC voltage ~2× high | `src/adc_counts.cpp` | `counts_to_volts` / `countsToVolts` |
| VLC-ENTRY-103 | Heap leak in soak | `src/heap_bins.cpp` | `HeapBins::~HeapBins` |
| VLC-ENTRY-104 | Fluent gain API won't chain | `src/mic_gain_chain.cpp`, `include/vlc/mic_gain_chain.hpp` | `MicGainChain::set_db` / `setDb` |
| VLC-ENTRY-105 | Wind PSD bin 0 stuck at zero | `src/wind_psd_scratch.cpp` | `WindPsdScratch::write_bin` / `writeBin` |

## Junior (`../junior-level/ticket_notebook.html`)

| Ticket ID | Symptom | Fix these files | Primary symbol |
|-----------|---------|-----------------|----------------|
| VLC-JR-201 | Quantizer accepts non-arithmetic types | `include/vlc/quantize.hpp` | `quantize_sample` / `quantizeSample` |
| VLC-JR-202 | Telemetry summary stale (no join) | `src/telemetry_slice.cpp` | `run_telemetry_slice_once` / `TelemetrySlice::runOnce` |
| VLC-JR-203 | Notch source silent through `Source*` | `include/vlc/source.hpp`, `include/vlc/notch_source.hpp` | `Source::next`, `NotchSource::next` |
| VLC-JR-204 | 16-bit field accepted in masked OR | `include/vlc/afe_registers.hpp` | `masked_or` / `::dsp::afe::maskedOr` |
| VLC-JR-205 | Tap gate ignores predicate | `src/tap_gate.cpp` | `gate_tap` / `gateTap`, `over_noise_floor` |

## Senior (`../senior-level/ticket_notebook.html`)

| Ticket ID | Symptom | Fix these files | Primary symbol |
|-----------|---------|-----------------|----------------|
| VLC-SR-301 | Crash deleting codec through base pointer | `include/vlc/icodec.hpp` | `ICodec::~ICodec` |
| VLC-SR-302 | Fancy route id lost (slicing) | `include/vlc/box_telemetry.hpp` | `route_box_by_value`, `Box` / `FancyBox` |
| VLC-SR-303 | Curve eval wrong through `ICurve*` | `src/lab_curve.cpp` | `LabCurve::eval(double)` |
| VLC-SR-304 | Stereo PSD `operator+` drops right channel | `src/stereo_psd.cpp` | `operator+(StereoPsd, StereoPsd)` |
| VLC-SR-305 | Factory trim write is a no-op | `src/cal_amp.cpp` | `set_factory_trim` / `setFactoryTrim` |

## Notes

- Canonical code uses **snake_case**; tickets may use **camelCase** aliases in headers.
- `::dsp::afe::maskedOr` forwards into `vlc::dsp::afe::masked_or`.
- Do **not** edit `tests/ticket_tests.cpp` unless a ticket explicitly tells you to — it is the verifier.
