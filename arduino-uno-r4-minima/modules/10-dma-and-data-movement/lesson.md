## Module 10: DMA and data movement

        ### Learning objectives
        - Explain how **DMA and data movement** maps to registers, interrupts, and memory on **Arduino UNO R4 Minima (Renesas RA4M1, Cortex-M4 + FPU)**.
        - Implement a buildable lab firmware feature for this module without relying on unverified abstractions.
        - Measure at least one timing or accuracy metric and relate it to real-time constraints.

        ### Concept overview
        This module follows the roadmap syllabus for `arduino-uno-r4-minima`.
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
        1. Create a **Git branch** `module-10` and a CCS / ESP-IDF / Arduino project folder tracked in-repo.
        2. Read the official sections cited in `references/` for this module's peripherals.
        3. Build, flash, and capture **UART log + one measurement** (scope, logic analyzer, or serial plot).
        4. Record expected vs observed results in your engineering notebook.
        5. If behavior diverges, follow the debugging checklist below before changing algorithm code.

        ## Step-by-step lab
        ### Prepare
        - Verify power, debugger connection, and that you can blink or print a heartbeat (regression sanity).
        - Document clock configuration and pin map in `README` snippet for this lab.

        ### Implement
        - Implement the module topic on **Arduino UNO R4 Minima (Renesas RA4M1, Cortex-M4 + FPU)** using the approach taught in the lesson (register-level where required).
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
        - [UNO R4 Minima product page](https://docs.arduino.cc/hardware/uno-r4-minima/)
- [RA4M1 Group datasheet](https://www.renesas.com/en/products/microcontrollers-microprocessors/ra-cortex-m-mcus/ra4m1-32-bit-microcontrollers)
- [Arduino Core for Renesas UNO R4](https://github.com/arduino/ArduinoCore-renesas)

        ## Hardware constraints (always)
        RA4M1: 48 MHz, 256 KB Flash, 32 KB SRAM, 12-bit ADC, 12-bit DAC. Not an audio codec board — external mic preamp, conditioning, and output stage required for audio labs. Verify I2S pin routing before promising hands-on SSIE labs.

### Audio / DSP note
### Embedded DSP and audio progression (within this course)
Discrete-time signals, LUT oscillators, convolution/correlation, FIR/IIR/biquads, DFT/FFT with windowing,
fixed- vs floating-point profiling, real-time buffering and latency measurement, gain/EQ/envelope basics.

### Required external analog audio labs
1. Electret mic bias + op-amp preamp (gain, noise, clipping).
2. ADC conditioning: AC coupling, mid-supply bias, anti-alias LPF, input protection.
3. DAC reconstruction LPF + buffer; measure ripple and frequency response.
4. Output stage to small speaker — never drive headphones/speaker directly from DAC pin.

### I2S on UNO R4 Minima
Teach I2S framing and investigate RA4M1 SSIE in documentation; hands-on I2S only after pin/toolchain verification.
