# ESP32-S3: Embedded Systems, DSP, and Digital Audio

        **Hardware:** ESP32-S3-DevKitC-1 (or documented equivalent; note PSRAM variant)
        **Prerequisites:** Embedded C/C++, pointers, and basic RTOS concepts helpful but introduced in-module.
        **Toolchain:** ESP-IDF primary; Arduino-ESP32 compared in selected labs.

        ## Open the course
        - **Browser:** double-click `index.html` (progress saves in localStorage).
        - **Git-friendly:** read `modules/` lessons, work in `exercises/`, check `solutions/` only after attempting.

        ## Constraints
        Dual-core Xtensa LX7, I2S + DMA. No general-purpose onboard DAC like original ESP32 — use INMP441 (I2S mic) and MAX98357A (I2S amp) or external codec. Verify board pins before wiring.

        ## Module map
        | # | Module | Folder |
        |---|--------|--------|
        | 01 | ESP32-S3 architecture and development environment | `modules/01-esp32-s3-architecture-and-development-environment/` |
| 02 | Embedded C/C++ and memory architecture | `modules/02-embedded-c-c-and-memory-architecture/` |
| 03 | GPIO, interrupts, and peripheral routing | `modules/03-gpio-interrupts-and-peripheral-routing/` |
| 04 | Timers and PWM | `modules/04-timers-and-pwm/` |
| 05 | FreeRTOS and multitasking | `modules/05-freertos-and-multitasking/` |
| 06 | ADC and analog interfacing | `modules/06-adc-and-analog-interfacing/` |
| 07 | UART, SPI, and I2C | `modules/07-uart-spi-and-i2c/` |
| 08 | DSP foundations on ESP32-S3 | `modules/08-dsp-foundations-on-esp32-s3/` |
| 09 | I2S digital audio interface | `modules/09-i2s-digital-audio-interface/` |
| 10 | DMA-based audio streaming | `modules/10-dma-based-audio-streaming/` |
| 11 | FIR, IIR, and FFT on ESP32-S3 | `modules/11-fir-iir-and-fft-on-esp32-s3/` |
| 12 | Advanced embedded audio processing | `modules/12-advanced-embedded-audio-processing/` |
| 13 | Final ESP32-S3 audio DSP project | `modules/13-final-esp32-s3-audio-dsp-project/` |

        ## Final project options
        - Real-time I2S digital audio effects processor
- Multi-band parametric equalizer
- FFT spectrum analyzer with I2S input
- I2S acquisition + Wi-Fi streaming

        ## Regenerate browser bundle
        ```powershell
        cd embedded-roadmap
        python generate_courses.py
        ```

        ## References
        See `references/README.md` for datasheets and official manuals.
