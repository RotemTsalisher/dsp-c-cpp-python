## Module 10: Sorting algorithms: foundations

            ### Learning objectives
            - State the problem in terms of inputs, outputs, constraints, and edge cases.
            - Design in plain language and pseudocode before coding.
            - Implement Python POC, analyze complexity, then port to MSP430 C with fixed capacities.

            ### Mandatory exercise methodology
            1. Problem understanding
            2. Algorithm design + pseudocode
            3. Python proof of concept + tests
            4. Correctness reasoning (invariants / pre/postconditions)
            5. Time and space complexity (best / average / worst where meaningful)
            6. Data-structure justification vs at least one alternative
            7. Embedded C on MSP430G2553 (fixed-width types, bounded memory)
            8. Differential validation against Python vectors
            9. Measurement procedure (cycles, RAM, stack, Flash)
            10. Short engineering report

            ### Host vs target
            - Python under `python_poc/` for rapid iteration.
            - MSP430 firmware under `embedded_c/` with documented `MAX_*` limits.

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
        - Implement the module topic on **MSP-EXP430G2 LaunchPad (MSP430G2553); host PC for Python/C++ exercises** using the approach taught in the lesson (register-level where required).
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
        - [CLRS (Introduction to Algorithms) — library reference](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [MSP430G2553 datasheet](https://www.ti.com/lit/ds/slas735j/slas735j.pdf)
- [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)

        ## Hardware constraints (always)
        512 B RAM, 16 KB Flash, no FPU. Every major exercise follows: problem → design → Python POC → complexity analysis → embedded C → differential validation → measurement → engineering report.
