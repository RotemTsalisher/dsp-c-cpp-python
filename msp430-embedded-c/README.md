# TI MSP430: Embedded C and Microcontroller Programming

        **Hardware:** TI MSP-EXP430G2 LaunchPad (MSP430G2553)
        **Prerequisites:** Basic programming (variables, functions, loops). No prior MCU experience required.
        **Toolchain:** Code Composer Studio (CCS) or msp430-gcc; MSP430 Driver Library optional for comparison labs only.

        ## Open the course
        - **Browser:** double-click `index.html` (progress saves in localStorage).
        - **Git-friendly:** read `modules/` lessons, work in `exercises/`, check `solutions/` only after attempting.

        ## Constraints
        MSP430G2553: 16-bit MCU, up to 16 MHz, 16 KB Flash, 512 B RAM, 10-bit ADC, Timer_A and USCI. No hardware FPU, no onboard DAC. Do not assume newer MSP430 features.

        ## Module map
        | # | Module | Folder |
        |---|--------|--------|
        | 01 | Embedded systems and MSP430 architecture | `modules/01-embedded-systems-and-msp430-architecture/` |
| 02 | Toolchain and debugging workflow | `modules/02-toolchain-and-debugging-workflow/` |
| 03 | GPIO and digital electronics | `modules/03-gpio-and-digital-electronics/` |
| 04 | Clock system and low-power modes | `modules/04-clock-system-and-low-power-modes/` |
| 05 | Interrupts and event handling | `modules/05-interrupts-and-event-handling/` |
| 06 | Timer_A and timing systems | `modules/06-timer-a-and-timing-systems/` |
| 07 | ADC10 and analog interfacing | `modules/07-adc10-and-analog-interfacing/` |
| 08 | PWM and actuator control | `modules/08-pwm-and-actuator-control/` |
| 09 | UART communication | `modules/09-uart-communication/` |
| 10 | SPI and I2C communication | `modules/10-spi-and-i2c-communication/` |
| 11 | Memory, watchdog, and reliability | `modules/11-memory-watchdog-and-reliability/` |
| 12 | Firmware architecture and real-time programming | `modules/12-firmware-architecture-and-real-time-programming/` |
| 13 | Integration and final project | `modules/13-integration-and-final-project/` |

        ## Final project options
        - Sensor monitor / UART data logger
- PWM motor controller with external driver
- Serial command controller
- Timer-driven measurement system

        ## Regenerate browser bundle
        ```powershell
        cd embedded-roadmap
        python generate_courses.py
        ```

        ## References
        See `references/README.md` for datasheets and official manuals.
