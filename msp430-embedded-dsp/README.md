# TI MSP430: Embedded Digital Signal Processing

        **Hardware:** MSP-EXP430G2 LaunchPad (MSP430G2553)
        **Prerequisites:** MSP430 embedded C course (or equivalent GPIO, timers, ADC, interrupts).
        **Toolchain:** CCS / msp430-gcc; Python or MATLAB for reference algorithms.

        ## Open the course
        - **Browser:** double-click `index.html` (progress saves in localStorage).
        - **Git-friendly:** read `modules/` lessons, work in `exercises/`, check `solutions/` only after attempting.

        ## Constraints
        512 B RAM, 10-bit ADC, no FPU. Keep FFT sizes and buffers realistic (often N≤64). External DAC only when a lab explicitly requires analog output.

        ## Module map
        | # | Module | Folder |
        |---|--------|--------|
        | 01 | Embedded DSP foundations | `modules/01-embedded-dsp-foundations/` |
| 02 | Discrete-time signals and systems | `modules/02-discrete-time-signals-and-systems/` |
| 03 | ADC-based signal acquisition | `modules/03-adc-based-signal-acquisition/` |
| 04 | Fixed-point arithmetic | `modules/04-fixed-point-arithmetic/` |
| 05 | Time-domain signal analysis | `modules/05-time-domain-signal-analysis/` |
| 06 | DFT and spectral analysis | `modules/06-dft-and-spectral-analysis/` |
| 07 | Small FFT implementations | `modules/07-small-fft-implementations/` |
| 08 | FIR filters | `modules/08-fir-filters/` |
| 09 | IIR filters | `modules/09-iir-filters/` |
| 10 | Practical embedded DSP algorithms | `modules/10-practical-embedded-dsp-algorithms/` |
| 11 | Real-time acquisition and processing | `modules/11-real-time-acquisition-and-processing/` |
| 12 | DSP optimization and validation | `modules/12-dsp-optimization-and-validation/` |
| 13 | Final embedded DSP project | `modules/13-final-embedded-dsp-project/` |

        ## Final project options
        - Fixed-point FIR filter on live ADC input
- Tone detector with goertzel or DFT bin
- Small-window FFT analyzer
- Low-frequency signal monitor / classifier

        ## Regenerate browser bundle
        ```powershell
        cd embedded-roadmap
        python generate_courses.py
        ```

        ## References
        See `references/README.md` for datasheets and official manuals.
