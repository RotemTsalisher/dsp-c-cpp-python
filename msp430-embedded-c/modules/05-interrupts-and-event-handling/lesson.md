## Module 5: Interrupts and event handling

        ### Learning objectives
        - Explain how **Interrupts and event handling** maps to registers, interrupts, and memory on **TI MSP-EXP430G2 LaunchPad (MSP430G2553)**.
        - Implement a buildable lab firmware feature for this module without relying on unverified abstractions.
        - Measure at least one timing or accuracy metric and relate it to real-time constraints.

        ### Concept overview
        This module follows the roadmap syllabus for `msp430-embedded-c`.
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
        1. Create a **Git branch** `module-05` and a CCS / ESP-IDF / Arduino project folder tracked in-repo.
        2. Read the official sections cited in `references/` for this module's peripherals.
        3. Build, flash, and capture **UART log + one measurement** (scope, logic analyzer, or serial plot).
        4. Record expected vs observed results in your engineering notebook.
        5. If behavior diverges, follow the debugging checklist below before changing algorithm code.

        ## Step-by-step lab
        ### Prepare
        - Verify power, debugger connection, and that you can blink or print a heartbeat (regression sanity).
        - Document clock configuration and pin map in `README` snippet for this lab.

        ### Implement
        - Implement the module topic on **TI MSP-EXP430G2 LaunchPad (MSP430G2553)** using the approach taught in the lesson (register-level where required).
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
        - [MSP430G2553 datasheet (SLAS735)](https://www.ti.com/lit/ds/slas735j/slas735j.pdf)
- [MSP430x2xx User's Guide (SLAU144)](https://www.ti.com/lit/ug/slau144i/slau144i.pdf)
- [MSP-EXP430G2 LaunchPad User's Guide (SLAU422)](https://www.ti.com/lit/ug/slau422d/slau422d.pdf)

        ## Hardware constraints (always)
        MSP430G2553: 16-bit MCU, up to 16 MHz, 16 KB Flash, 512 B RAM, 10-bit ADC, Timer_A and USCI. No hardware FPU, no onboard DAC. Do not assume newer MSP430 features.
