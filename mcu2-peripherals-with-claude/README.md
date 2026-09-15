# MCU2 Peripherals with Claude Code — Companion Course

**Parallel to:** [Mastering Microcontroller: Timers, PWM, CAN, Low Power (MCU2)](https://www.udemy.com/course/microcontroller-programming-stm32-timers-pwm-can-bus-protocol/) (FastBit Embedded Brain Academy)

## What This Is
An AI-accelerated companion course following the Udemy MCU2 peripheral programming syllabus. For each advanced peripheral (timers, PWM, CAN, low power, RTC), this course teaches you how to use **Claude Code** to calculate configurations, generate HAL-level code, debug protocols, and accelerate peripheral bring-up.

## Prerequisites
- Completed MCU1 course (or equivalent bare-metal experience)
- STM32F446RE Nucleo board
- STM32CubeIDE installed
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- CAN transceivers (for CAN bus exercises)

## Modules (10 modules · 26 exercises)
| # | Topic | Udemy Parallel |
|---|-------|---------------|
| 00 | Setup & CLAUDE.md | HAL project + Claude onboarding |
| 01 | Clocks & PLL | HSI, HSE, PLL, SystemClock_Config |
| 02 | Basic Timers | TIM6/TIM7, polling, interrupts, PSC/ARR math |
| 03 | Input Capture & Output Compare | Frequency measurement, PWM generation |
| 04 | CAN Protocol Fundamentals | Frames, arbitration, bit timing |
| 05 | bxCAN Programming & Filtering | Filter banks, loopback, normal mode |
| 06 | Low Power Modes | Sleep, Stop, Standby, WFI/WFE |
| 07 | RTC | Calendar, BCD conversion, alarms, wake-up |
| 08 | Capstone: Smart Sensor Node | Timer + CAN + RTC + Low Power |
| drills | Daily Drills | Quick MCU2 reps |

## How to Use
1. Watch the Udemy lecture for a peripheral
2. Open `index.html` in your browser
3. Navigate to the matching module
4. Use Claude Code to calculate, configure, and debug peripherals

## Open the Course
Open `index.html` in any browser. Progress saves locally via localStorage.
