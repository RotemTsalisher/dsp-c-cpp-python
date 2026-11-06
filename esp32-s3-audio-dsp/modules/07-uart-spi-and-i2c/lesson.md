## Module 7: UART, SPI, and I2C

        ### Learning objectives
        - Explain how **UART, SPI, and I2C** maps to registers, interrupts, and memory on **ESP32-S3-DevKitC-1 (or documented equivalent; note PSRAM variant)**.
        - Implement a buildable lab firmware feature for this module without relying on unverified abstractions.
        - Measure at least one timing or accuracy metric and relate it to real-time constraints.

        ### Concept overview
        This module follows the roadmap syllabus for `esp32-s3-audio-dsp`.
        Treat the MCU as a **deterministic machine** with finite RAM and predictable peripheral behavior.
        When the syllabus calls for register-level understanding, open the family user's guide and locate the
        control/status registers for the peripheral you configure—do not guess bit meanings.

        ### Firmware structure hint
        ```
        src/
          board/        pin map, clock init
          drivers/      thin HAL you own (GPIO, UART, ADC, I2S, ...)
          app/          state machines, DSP blocks, CLI
          tests/        host-side golden vectors (optional)
        ```

        ### Documentation to cite in your report
        - Datasheet: electrical limits and pin functions.
        - User's guide: peripheral chapters for this module.
        - Board guide: which LaunchPad pins are routed to headers.

        ## Lab workflow (every module)
        1. Create a **Git branch** `module-07` and a CCS / ESP-IDF / Arduino project folder tracked in-repo.
        2. Read the official sections cited in `references/` for this module's peripherals.
        3. Build, flash, and capture **UART log + one measurement** (scope, logic analyzer, or serial plot).
        4. Record expected vs observed results in your engineering notebook.
        5. If behavior diverges, follow the debugging checklist below before changing algorithm code.

        ## Step-by-step lab
        ### Prepare
        - Verify power, debugger connection, and that you can blink or print a heartbeat (regression sanity).
        - Document clock configuration and pin map in `README` snippet for this lab.

        ### Implement
        - Implement the module topic on **ESP32-S3-DevKitC-1 (or documented equivalent; note PSRAM variant)** using the approach taught in the lesson (register-level where required).
        - Keep ISRs minimal; move parsing and heavy work to the main loop or a worker task (FreeRTOS on ESP32-S3).

        ### Verify
        - Define at least **three test cases** (nominal, boundary, fault).
        - Compare against Python/MATLAB reference when the module is DSP-related.

        ### Measure
        - Time critical paths with a hardware timer or GPIO toggle + logic analyzer.
        - Estimate RAM/Flash from map file or `idf.py size` / CCS memory view.

        ## Expected results
        - UART (or serial plot) shows deterministic, repeatable measurements across power cycles.
        - No stack overflow, watchdog resets, or unexplained ADC saturation on nominal inputs.

        ## Common mistakes
        - Forgetting `volatile` on flags set in ISRs.
        - Running heavy printf inside ISRs (breaks latency budgets).
        - Misconfigured clock dividers (wrong baud, PWM frequency, or sample rate).
        - Floating-point on MSP430G2553 when fixed-point was required.

        ## Debugging guidance
        - Bisect: GPIO toggle at ISR entry/exit to see jitter and missed events.
        - Single-step from reset through clock init before enabling peripherals.
        - Capture registers after fault; compare with reset defaults in the datasheet.

        ## Official references
        - [ESP32-S3 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)
- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
- [ESP32-S3 DevKitC-1](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html)

        ## Hardware constraints (always)
        Dual-core Xtensa LX7, I2S + DMA. No general-purpose onboard DAC like original ESP32 — use INMP441 (I2S mic) and MAX98357A (I2S amp) or external codec. Verify board pins before wiring.

### Deep dive: UART, SPI, and I2C

Study the official manual chapter that matches this topic on your board.
For **ESP-IDF v5.x, `idf.py build flash monitor`**, map each signal to a pin before writing drivers.

### Key ideas
- Configure clocks before baud rates, ADC sample time, or PWM frequency.
- Keep interrupt service routines short; defer work to the main loop or task.
- Document assumptions (voltage, sample rate, buffer depth) in module README.

### Register / API map (fill while reading docs)
| Function | Register / API | Your notes |
|----------|----------------|------------|
| Enable clock to peripheral | | |
| Configure pins | | |
| Start operation | | |
| Status / flags | | |

## Lab steps
1. Clone module branch `module-07`.
2. Open `code/starter/` — complete TODOs for **UART, SPI, and I2C**.
3. Build and flash; capture serial log or scope trace.
4. Compare against `code/solution/` only after tests fail and you have hypotheses.
5. Write expected vs actual in `lab_checklist.md`.

### Test procedure — UART, SPI, and I2C
| Case | Input / action | Expected |
|------|----------------|----------|
| T1 nominal | Typical operating point | Stable output, no fault flags |
| T2 boundary | Min/max allowed value | Saturate or reject safely |
| T3 fault | Disconnect sensor / noise | Detectable error, no lock-up |
