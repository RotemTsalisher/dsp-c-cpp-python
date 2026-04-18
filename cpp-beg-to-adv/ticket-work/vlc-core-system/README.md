# VoiceLink Core (VLC) — reference system under test

This tree is the **C++20 reference implementation** that matches the **VoiceLink Core** product narrative used in `../entry-level/`, `../junior-level/`, and `../senior-level/` ticket notebooks.

- **Ticket mapping:** see **`TICKET_CROSSWALK.md`** (every HTML ticket ↔ file ↔ symbol, including camelCase aliases).
- **Build:** `cmake -S . -B build && cmake --build build` (then run `vlc_demo` or link `vlc_core` into your own harness).
- **Constraints:** Training stack — **no STL containers** (`vector`, `map`, …). Uses `<cmath>`, `<cstdint>`, `<thread>`, `<type_traits>`, `<numbers>`, `<utility>` where needed.
- **Layout:** `include/vlc/` public headers, `src/` translation units. Tickets map to modules by name (e.g. `mono_mix`, `heap_bins`, `icodec`).

This version is intended as a **coherent, compiling baseline** you can browse while closing tickets; individual tickets in the HTML notebooks may describe defects that were already fixed here, or hypothetical regressions—use the notebook solution as the authoritative “after” for each scenario.

## Module map (headers under `include/vlc/`)

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
