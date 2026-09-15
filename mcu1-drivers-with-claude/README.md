# MCU1 Driver Development with Claude Code — Companion Course

**Parallel to:** [Mastering Microcontroller and Embedded Driver Development](https://www.udemy.com/course/mastering-microcontroller-with-peripheral-driver-development/) (FastBit Embedded Brain Academy)

## What This Is
An AI-accelerated companion course following the Udemy MCU1 driver development syllabus. For each peripheral driver you build in the Udemy lectures, this course teaches you how to use **Claude Code** to generate driver boilerplate, interpret datasheets, debug register-level code, and accelerate bare-metal development.

## Prerequisites
- Enrolled in the Udemy MCU1 course
- STM32F446RE Nucleo board
- STM32CubeIDE installed
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- STM32F446RE Reference Manual (RM0390)

## Modules (11 modules · 35 exercises)
| # | Topic | Udemy Parallel |
|---|-------|---------------|
| 00 | Setup & CLAUDE.md | Dev environment + Claude onboarding |
| 01 | MCU Architecture | Bus architecture, memory map, registers |
| 02 | GPIO Driver | GPIO init, read, write, toggle |
| 03 | Interrupts: EXTI & NVIC | External interrupts, priority config |
| 04 | SPI Driver | SPI init, TX/RX, interrupt mode |
| 05 | I2C Driver | I2C init, master TX/RX, addressing |
| 06 | USART Driver | USART init, TX/RX, baud rate calc |
| 07 | Clock Configuration | RCC, PLL, prescalers, HSI/HSE |
| 08 | Driver Library Integration | Layered architecture, API design |
| 09 | Capstone: Sensor Interface | Full sensor project using all drivers |
| drills | Daily Drills | Quick bare-metal reps |

## How to Use
1. Watch the Udemy lecture for a peripheral
2. Open `index.html` in your browser
3. Navigate to the matching module
4. Use Claude Code to generate, debug, and understand drivers

## Open the Course
Open `index.html` in any browser. Progress saves locally via localStorage.
