# RTOS with Claude Code — FreeRTOS Companion Course

**Parallel to:** [Mastering RTOS: Hands on FreeRTOS and STM32Fx with Debugging](https://www.udemy.com/course/mastering-rtos-hands-on-with-freertos-arduino-and-stm32fx/) (FastBit Embedded Brain Academy)

## What This Is
An AI-accelerated companion course following the Udemy FreeRTOS syllabus. For each RTOS concept (tasks, queues, semaphores, memory management), this course teaches you how to use **Claude Code** to visualize scheduling, generate task code, analyze synchronization, and debug concurrency issues.

## Prerequisites
- Completed MCU1/MCU2 courses (or equivalent STM32 experience)
- STM32F4 board (Discovery or Nucleo)
- STM32CubeIDE with FreeRTOS middleware
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- SEGGER SystemView (optional, for trace visualization)

## Modules (9 modules · 26 exercises)
| # | Topic | Udemy Parallel |
|---|-------|---------------|
| 00 | Setup & CLAUDE.md | FreeRTOS project + Claude onboarding |
| 01 | RTOS Concepts & Task States | Scheduling, preemption, state machine |
| 02 | Task Creation & Stack Sizing | xTaskCreate, vTaskDelay, stack estimation |
| 03 | Queues (IPC) | Producer-consumer pipelines, queue sizing |
| 04 | Semaphores & Mutexes | Synchronization, priority inversion |
| 05 | Software Timers & Events | Watchdog patterns, event groups |
| 06 | Memory & Debugging | Heap schemes, stack analysis, crash diagnosis |
| 07 | Capstone: Multi-Task Sensor System | All RTOS concepts integrated |
| drills | Daily Drills | Quick RTOS reps |

## How to Use
1. Watch the Udemy lecture for an RTOS concept
2. Open `index.html` in your browser
3. Navigate to the matching module
4. Use Claude Code to visualize, implement, and debug RTOS patterns

## Open the Course
Open `index.html` in any browser. Progress saves locally via localStorage.
