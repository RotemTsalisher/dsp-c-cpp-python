"""Source of truth for the five embedded-systems roadmap courses (syllabus-aligned)."""
from __future__ import annotations

HOME = "C:/Users/rotemt/OneDrive - Cardo Systems LTD/Desktop/SW/dsp-c-cpp-python"

COURSES: list[dict] = [
    {
        "slug": "msp430-embedded-c",
        "title": "TI MSP430: Embedded C and Microcontroller Programming",
        "hardware": "TI MSP-EXP430G2 LaunchPad (MSP430G2553)",
        "prereq": "Basic programming (variables, functions, loops). No prior MCU experience required.",
        "toolchain": "Code Composer Studio (CCS) or msp430-gcc; MSP430 Driver Library optional for comparison labs only.",
        "module_count": 13,
        "final_projects": [
            "Sensor monitor / UART data logger",
            "PWM motor controller with external driver",
            "Serial command controller",
            "Timer-driven measurement system",
        ],
        "constraints": (
            "MSP430G2553: 16-bit MCU, up to 16 MHz, 16 KB Flash, 512 B RAM, 10-bit ADC, "
            "Timer_A and USCI. No hardware FPU, no onboard DAC. Do not assume newer MSP430 features."
        ),
        "refs": [
            ("MSP430G2553 datasheet (SLAS735)", "https://www.ti.com/lit/ds/slas735j/slas735j.pdf"),
            ("MSP430x2xx User's Guide (SLAU144)", "https://www.ti.com/lit/ug/slau144i/slau144i.pdf"),
            ("MSP-EXP430G2 LaunchPad User's Guide (SLAU422)", "https://www.ti.com/lit/ug/slau422d/slau422d.pdf"),
            ("Code Composer Studio", "https://www.ti.com/tool/CCSTUDIO"),
        ],
        "modules": [
            "Embedded systems and MSP430 architecture",
            "Toolchain and debugging workflow",
            "GPIO and digital electronics",
            "Clock system and low-power modes",
            "Interrupts and event handling",
            "Timer_A and timing systems",
            "ADC10 and analog interfacing",
            "PWM and actuator control",
            "UART communication",
            "SPI and I2C communication",
            "Memory, watchdog, and reliability",
            "Firmware architecture and real-time programming",
            "Integration and final project",
        ],
        "storage_key": "msp430-embedded-c-v1",
    },
    {
        "slug": "msp430-embedded-dsp",
        "title": "TI MSP430: Embedded Digital Signal Processing",
        "hardware": "MSP-EXP430G2 LaunchPad (MSP430G2553)",
        "prereq": "MSP430 embedded C course (or equivalent GPIO, timers, ADC, interrupts).",
        "toolchain": "CCS / msp430-gcc; Python or MATLAB for reference algorithms.",
        "module_count": 13,
        "final_projects": [
            "Fixed-point FIR filter on live ADC input",
            "Tone detector with goertzel or DFT bin",
            "Small-window FFT analyzer",
            "Low-frequency signal monitor / classifier",
        ],
        "constraints": (
            "512 B RAM, 10-bit ADC, no FPU. Keep FFT sizes and buffers realistic (often N≤64). "
            "External DAC only when a lab explicitly requires analog output."
        ),
        "refs": [
            ("MSP430G2553 datasheet (SLAS735)", "https://www.ti.com/lit/ds/slas735j/slas735j.pdf"),
            ("SLAU144 User's Guide — ADC10, Timer_A", "https://www.ti.com/lit/ug/slau144i/slau144i.pdf"),
            ("Oppenheim & Schafer — DTSP (reference)", "https://ocw.mit.edu/resources/res-6-007-signals-and-systems-spring-2011/"),
        ],
        "modules": [
            "Embedded DSP foundations",
            "Discrete-time signals and systems",
            "ADC-based signal acquisition",
            "Fixed-point arithmetic",
            "Time-domain signal analysis",
            "DFT and spectral analysis",
            "Small FFT implementations",
            "FIR filters",
            "IIR filters",
            "Practical embedded DSP algorithms",
            "Real-time acquisition and processing",
            "DSP optimization and validation",
            "Final embedded DSP project",
        ],
        "storage_key": "msp430-embedded-dsp-v1",
    },
    {
        "slug": "arduino-uno-r4-minima",
        "title": "Arduino UNO R4 Minima: Embedded Systems and DSP",
        "hardware": "Arduino UNO R4 Minima (Renesas RA4M1, Cortex-M4 + FPU)",
        "prereq": "C/C++ basics and comfortable use of Arduino IDE or arduino-cli.",
        "toolchain": "Arduino IDE 2.x or arduino-cli; optional Renesas FSP / bare-register labs documented per module.",
        "module_count": 13,
        "final_projects": [
            "Analog audio I/O with external front-end + DSP block",
            "Programmable waveform generator (DAC + reconstruction filter)",
            "FIR/IIR processor on live ADC stream",
            "Real-time spectrum analyzer",
        ],
        "constraints": (
            "RA4M1: 48 MHz, 256 KB Flash, 32 KB SRAM, 12-bit ADC, 12-bit DAC. "
            "Not an audio codec board — external mic preamp, conditioning, and output stage required for audio labs. "
            "Verify I2S pin routing before promising hands-on SSIE labs."
        ),
        "refs": [
            ("UNO R4 Minima product page", "https://docs.arduino.cc/hardware/uno-r4-minima/"),
            ("RA4M1 Group datasheet", "https://www.renesas.com/en/products/microcontrollers-microprocessors/ra-cortex-m-mcus/ra4m1-32-bit-microcontrollers"),
            ("Arduino Core for Renesas UNO R4", "https://github.com/arduino/ArduinoCore-renesas"),
        ],
        "modules": [
            "Arduino and RA4M1 architecture",
            "Embedded C/C++",
            "GPIO and digital logic",
            "Timers, counters, and PWM",
            "Interrupts and event handling",
            "ADC, DAC, and analog interfacing",
            "UART, SPI, and I2C",
            "Memory and data structures",
            "ARM Cortex-M4 and low-level programming",
            "DMA and data movement",
            "Real-time firmware architecture",
            "Debugging, testing, and optimization",
            "Final embedded systems project",
        ],
        "storage_key": "arduino-uno-r4-v1",
        "extra_notes": """
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
""",
    },
    {
        "slug": "esp32-s3-audio-dsp",
        "title": "ESP32-S3: Embedded Systems, DSP, and Digital Audio",
        "hardware": "ESP32-S3-DevKitC-1 (or documented equivalent; note PSRAM variant)",
        "prereq": "Embedded C/C++, pointers, and basic RTOS concepts helpful but introduced in-module.",
        "toolchain": "ESP-IDF primary; Arduino-ESP32 compared in selected labs.",
        "module_count": 13,
        "final_projects": [
            "Real-time I2S digital audio effects processor",
            "Multi-band parametric equalizer",
            "FFT spectrum analyzer with I2S input",
            "I2S acquisition + Wi-Fi streaming",
        ],
        "constraints": (
            "Dual-core Xtensa LX7, I2S + DMA. No general-purpose onboard DAC like original ESP32 — "
            "use INMP441 (I2S mic) and MAX98357A (I2S amp) or external codec. Verify board pins before wiring."
        ),
        "refs": [
            ("ESP32-S3 Technical Reference", "https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf"),
            ("ESP-IDF Programming Guide", "https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/"),
            ("ESP32-S3 DevKitC-1", "https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html"),
        ],
        "modules": [
            "ESP32-S3 architecture and development environment",
            "Embedded C/C++ and memory architecture",
            "GPIO, interrupts, and peripheral routing",
            "Timers and PWM",
            "FreeRTOS and multitasking",
            "ADC and analog interfacing",
            "UART, SPI, and I2C",
            "DSP foundations on ESP32-S3",
            "I2S digital audio interface",
            "DMA-based audio streaming",
            "FIR, IIR, and FFT on ESP32-S3",
            "Advanced embedded audio processing",
            "Final ESP32-S3 audio DSP project",
        ],
        "storage_key": "esp32-s3-audio-v1",
    },
    {
        "slug": "embedded-algorithms",
        "title": "Algorithm Development for Embedded Systems (C/C++)",
        "hardware": "MSP-EXP430G2 LaunchPad (MSP430G2553); host PC for Python/C++ exercises",
        "prereq": "Second-year EE coding level; no prior formal algorithms or Big-O course.",
        "toolchain": "Python 3 for POC; MSP430 C (CCS/gcc); host C++20 for STL modules.",
        "module_count": 24,
        "final_projects": [
            "Reusable MSP430 algorithm library with benchmark and test reports",
        ],
        "constraints": (
            "512 B RAM, 16 KB Flash, no FPU. Every major exercise follows: problem → design → Python POC → "
            "complexity analysis → embedded C → differential validation → measurement → engineering report."
        ),
        "refs": [
            ("CLRS (Introduction to Algorithms) — library reference", "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/"),
            ("MSP430G2553 datasheet", "https://www.ti.com/lit/ds/slas735j/slas735j.pdf"),
            ("SEI CERT C Coding Standard", "https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard"),
        ],
        "modules": [
            "Introduction to algorithm development",
            "Mathematical foundations for algorithms",
            "Understanding algorithm complexity",
            "Problem-solving methods and correctness",
            "Arrays and memory representation",
            "Strings and character processing",
            "Pointers, linked lists, stacks, and queues",
            "Hash tables, heaps, and priority queues",
            "Searching algorithms",
            "Sorting algorithms: foundations",
            "Advanced sorting algorithms",
            "Recursion and backtracking",
            "Bit manipulation and bitwise algorithms",
            "Divide and conquer",
            "Greedy algorithms",
            "Dynamic programming",
            "Graph representations and algorithms",
            "Common algorithmic problem-solving patterns",
            "Embedded C for algorithm developers",
            "Fixed-point arithmetic and numerical algorithms",
            "Real-time and streaming algorithms",
            "Optimization for embedded targets",
            "Testing, verification, and engineering quality",
            "Final engineering project: embedded algorithm library",
        ],
        "storage_key": "embedded-algorithms-v1",
        "algorithm_course": True,
    },
]
