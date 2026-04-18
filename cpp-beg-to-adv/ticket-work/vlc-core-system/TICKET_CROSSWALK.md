# Ticket ↔ VLC core system crosswalk

Use this table to map **QA ticket text** to **headers / symbols** in `vlc-core-system`. Canonical implementation uses **snake_case**; **camelCase** and `dsp::afe::maskedOr` exist as thin aliases where tickets use those spellings.

## Entry (`../entry-level/ticket_notebook.html`)

| Ticket ID | Ticket component / API name | Code location | Notes |
|-----------|----------------------------|---------------|--------|
| VLC-ENTRY-101 | `monoMixDown`, `uplink_mix.cpp` | `include/vlc/mono_mix.hpp`, `src/mono_mix.cpp` | Logic lives as `mono_mix_down`; alias `monoMixDown`. |
| VLC-ENTRY-102 | `countsToVolts` | `include/vlc/adc_counts.hpp`, `src/adc_counts.cpp` | Canonical `counts_to_volts`; alias `countsToVolts`. |
| VLC-ENTRY-103 | `HeapBins` | `include/vlc/heap_bins.hpp`, `src/heap_bins.cpp` | Destructor + `delete[]` present. |
| VLC-ENTRY-104 | `MicGainChain::setDb` | `include/vlc/mic_gain_chain.hpp`, `src/mic_gain_chain.cpp` | Canonical `set_db`; inline `setDb` chains. |
| VLC-ENTRY-105 | `WindPsdScratch::writeBin` | `include/vlc/wind_psd_scratch.hpp`, `src/wind_psd_scratch.cpp` | Canonical `write_bin`; `writeBin` alias. Writer is **non-const**. |

## Junior (`../junior-level/ticket_notebook.html`)

| Ticket ID | Ticket component / API name | Code location | Notes |
|-----------|----------------------------|---------------|--------|
| VLC-JR-201 | `quantizeSample`, `dsp/quantize.h` | `include/vlc/quantize.hpp` | `quantize_sample` + alias `quantizeSample`; `requires std::is_arithmetic_v<T>`. |
| VLC-JR-202 | `TelemetrySlice::runOnce` | `include/vlc/telemetry_slice.hpp`, `src/telemetry_slice.cpp` | `run_telemetry_slice_once` + struct `TelemetrySlice::runOnce`. |
| VLC-JR-203 | `Source::next` virtual, `NotchSource` | `include/vlc/source.hpp`, `include/vlc/notch_source.hpp`, `src/notch_source.cpp` | **Fixed model:** `Source::next` is **pure virtual** (stricter than ticket snippet’s defaulting base). |
| VLC-JR-204 | `dsp::afe::maskedOr` | `include/vlc/afe_registers.hpp` | Implementations in `vlc::dsp::afe::masked_or`; ticket spelling `::dsp::afe::maskedOr` forwards. Inside `using namespace vlc`, qualify **`::dsp::afe::maskedOr`** to avoid ambiguity with `vlc::dsp`. |
| VLC-JR-205 | `gateTap`, `TapPred`, `overNoiseFloor` | `include/vlc/tap_gate.hpp`, `src/tap_gate.cpp` | Canonical `gate_tap`, `over_noise_floor`; camelCase aliases. |

## Senior (`../senior-level/ticket_notebook.html`)

| Ticket ID | Ticket component / API name | Code location | Notes |
|-----------|----------------------------|---------------|--------|
| VLC-SR-301 | `ICodec`, virtual destructor, `NotchCodec` | `include/vlc/icodec.hpp`, `src/icodec.cpp` | `virtual ~ICodec() = default`; `NotchCodec final`. |
| VLC-SR-302 | `Box`, `FancyBox`, telemetry | `include/vlc/box_telemetry.hpp` | Non-virtual `id()`; demonstrates slicing / static binding. |
| VLC-SR-303 | `ICurve`, `LabCurve::eval` | `include/vlc/lab_curve.hpp`, `src/lab_curve.cpp` | One-arg virtual delegates to `eval(x, false)`; two-arg matches ticket math `norm ? 2x : x`. |
| VLC-SR-304 | `StereoPsd`, `operator+`, `stereo_psd.cpp` | `include/vlc/stereo_psd.hpp`, `src/stereo_psd.cpp` | `friend` `operator+`; uses `energy()` / `right()`. |
| VLC-SR-305 | `CalAmp`, `GainBase`, `setFactoryTrim` | `include/vlc/cal_amp.hpp`, `src/cal_amp.cpp` | `set_factory_trim` + `setFactoryTrim` both friends with same semantics. |

## Smoke test

`src/main.cpp` exercises both canonical and ticket-style entry points where applicable. Build with CMake per `README.md`.
