# Arduino UNO R4 Minima: Embedded Systems and DSP

        **Hardware:** Arduino UNO R4 Minima (Renesas RA4M1, Cortex-M4 + FPU)
        **Prerequisites:** C/C++ basics and comfortable use of Arduino IDE or arduino-cli.
        **Toolchain:** Arduino IDE 2.x or arduino-cli; optional Renesas FSP / bare-register labs documented per module.

        ## Open the course
        - **Browser:** double-click `index.html` (progress saves in localStorage).
        - **Git-friendly:** read `modules/` lessons, work in `exercises/`, check `solutions/` only after attempting.

        ## Constraints
        RA4M1: 48 MHz, 256 KB Flash, 32 KB SRAM, 12-bit ADC, 12-bit DAC. Not an audio codec board — external mic preamp, conditioning, and output stage required for audio labs. Verify I2S pin routing before promising hands-on SSIE labs.

        ## Module map
        | # | Module | Folder |
        |---|--------|--------|
        | 01 | Arduino and RA4M1 architecture | `modules/01-arduino-and-ra4m1-architecture/` |
| 02 | Embedded C/C++ | `modules/02-embedded-c-c/` |
| 03 | GPIO and digital logic | `modules/03-gpio-and-digital-logic/` |
| 04 | Timers, counters, and PWM | `modules/04-timers-counters-and-pwm/` |
| 05 | Interrupts and event handling | `modules/05-interrupts-and-event-handling/` |
| 06 | ADC, DAC, and analog interfacing | `modules/06-adc-dac-and-analog-interfacing/` |
| 07 | UART, SPI, and I2C | `modules/07-uart-spi-and-i2c/` |
| 08 | Memory and data structures | `modules/08-memory-and-data-structures/` |
| 09 | ARM Cortex-M4 and low-level programming | `modules/09-arm-cortex-m4-and-low-level-programming/` |
| 10 | DMA and data movement | `modules/10-dma-and-data-movement/` |
| 11 | Real-time firmware architecture | `modules/11-real-time-firmware-architecture/` |
| 12 | Debugging, testing, and optimization | `modules/12-debugging-testing-and-optimization/` |
| 13 | Final embedded systems project | `modules/13-final-embedded-systems-project/` |

        ## Final project options
        - Analog audio I/O with external front-end + DSP block
- Programmable waveform generator (DAC + reconstruction filter)
- FIR/IIR processor on live ADC stream
- Real-time spectrum analyzer

        ## Regenerate browser bundle
        ```powershell
        cd embedded-roadmap
        python generate_courses.py
        ```

        ## References
        See `references/README.md` for datasheets and official manuals.

## Course-specific notes
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
