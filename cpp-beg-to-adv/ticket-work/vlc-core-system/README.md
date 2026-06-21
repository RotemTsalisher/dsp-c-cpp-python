# VoiceLink Core (VLC) — ticket exercise codebase

This tree is the **C++20 training implementation** of VoiceLink Core used by the ticket notebooks in `../entry-level/`, `../junior-level/`, and `../senior-level/`.

Each ticket ships with an **intentional defect** in a named module. Your job is to read the ticket, reproduce the failure with the per-ticket test runner, patch the listed source files, and re-run the same test until it prints `PASS`.

## Quick start

```powershell
cd vlc-core-system
cmake -S . -B build
cmake --build build --target vlc_ticket_test
.\build\Debug\vlc_ticket_test.exe --list
.\build\Debug\vlc_ticket_test.exe VLC-ENTRY-101
```

Exit code `0` means your fix satisfies that ticket. Exit code `1` means the defect is still present.

## Layout

| Path | Purpose |
|------|---------|
| `include/vlc/` | Public headers referenced by tickets |
| `src/` | Translation units that contain the bugs you fix |
| `tests/ticket_tests.cpp` | One automated check per ticket ID |
| `TICKET_CROSSWALK.md` | Ticket ID → file → symbol map |

## Constraints

Training stack — **no STL containers** (`vector`, `map`, …). Uses `<cmath>`, `<cstdint>`, `<thread>`, `<type_traits>`, `<numbers>`, `<utility>` where needed.

## Module map

| Module | Role |
|--------|------|
| `mono_mix.hpp` | Uplink stereo → mono downmix |
| `adc_counts.hpp` | ADC counts → volts |
| `heap_bins.hpp` | Heap PSD bin storage |
| `mic_gain_chain.hpp` | Fluent dB → linear gain |
| `wind_psd_scratch.hpp` | Fixed 64-bin wind PSD scratch |
| `quantize.hpp` | Constrained template quantizer (`requires`) |
| `telemetry_slice.hpp` | Worker thread + `join` telemetry slice |
| `source.hpp` / `notch_source.hpp` | Polymorphic sample source |
| `afe_registers.hpp` | `dsp::afe` 32-bit masked OR (`concept`) |
| `tap_gate.hpp` | Comb-tap gate via function pointer |
| `icodec.hpp` | `ICodec` + `NotchCodec` (virtual destructor) |
| `box_telemetry.hpp` | Non-virtual `Box` / `FancyBox` id (slicing lesson) |
| `lab_curve.hpp` | `ICurve` / `LabCurve` (explicit norm overload) |
| `stereo_psd.hpp` | Mono/stereo PSD merge (`operator+`) |
| `cal_amp.hpp` | Factory trim via `friend` |
| `uplink_service.hpp` | Thin façade over uplink helpers |

## Reference

- Ticket notebooks: `../entry-level/ticket_notebook.html`, etc.
- Crosswalk: `TICKET_CROSSWALK.md`
- Optional smoke binary: `vlc_demo` (builds everything; use per-ticket tests while fixing)
