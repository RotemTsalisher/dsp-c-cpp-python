# 📚 All Courses — Learning Path

> Logical order from foundations to expert. Courses you've finished, courses in progress, and AI companion courses that run alongside them.

---

## Phase 1: Language Foundations

### 1. ✅ C — Beginner to Advanced
**Folder:** `c-beg-to-adv/`
**Status:** Course walkthrough done (22 topics). Workbooks batch-01 done (14 exercises). Batch-02 in progress (up to exercise-8 Levinson-Durbin).

- `course-walkthrough/` — 22 completed topics (data types → pointers → structs → files)
- `workbooks/batch-01/` — 14 exercises (done)
- `workbooks/batch-02/` — DSP-flavored C exercises (in progress)
- `ticket-work/` — applied projects (DSP core system)

### 2. ✅ C++ — Beginner to Advanced
**Folder:** `cpp-beg-to-adv/`
**Status:** Core curriculum done (14 workbooks completed). Advanced topics in progress (STL, DAFX projects).

- `workbooks-done/` — 14 completed workbooks (basics → templates → friends → milestones)
- `workbooks/first-half-curriculum/` — curriculum workbook
- `progress/` — advanced topics (virtual, abstract classes, dynamic cast, operator overloading)
- `STL/` — vectors, lists, maps, algorithms
- `homework-set-1/`, `homework-set-concepts/` — concept exercises
- `dafx-projects/` — digital audio effects projects
- `ticket-work/`, `ticket-work-2/` — applied projects (VLC core, AFE core)
- `everyday-practice-*/` — daily practice sets

### 3. 🔧 C++ with GCC (Build & Toolchain)
**Folder:** `cpp-with-gcc/`
**Status:** Milestones and workbooks done.

- Workbooks 5–6, milestones 1–2, static/inheritance, HelloWorld

### 4. 📘 Python Basics
**Folder:** `python/`
**Status:** Basics covered.

- `virtual-env-and-basics/` — environment setup
- `HelloWorld/` — first scripts
- `jsons-and-modules/` — data handling and modules

### 5. 📘 SQLite
**Folder:** `SQLite/`
**Status:** Explored.

- Database basics with test.db

---

## Phase 2: Embedded Systems

### 6. 🔲 Embedded C Fundamentals
**Folder:** `embedded/`
**Status:** Workbook exercises done (bitwise operations focus).

- `bitwise-workbook/`, `bitwis-two-workbook/` — bit manipulation mastery
- `workbook-set-one/` — general embedded C

> **AI Companion:** `embedded-c-with-claude/` — 14 modules, 47 exercises
> Parallel to Udemy "Microcontroller Embedded C Programming: Absolute Beginners"

### 7. 🔲 MCU1: Bare-Metal Driver Development
**AI Companion:** `mcu1-drivers-with-claude/` — 11 modules, 35 exercises
Parallel to Udemy "Mastering Microcontroller and Embedded Driver Development"

- GPIO, SPI, I2C, USART, interrupts, clock config — bare metal on STM32F446RE

### 8. 🔲 MCU2: Advanced Peripherals (HAL)
**AI Companion:** `mcu2-peripherals-with-claude/` — 10 modules, 26 exercises
Parallel to Udemy "Mastering Microcontroller: Timers, PWM, CAN, Low Power (MCU2)"

- Timers, PWM, CAN bus, low power modes, RTC — HAL-based on STM32F446RE

### 9. 🔲 RTOS: FreeRTOS on STM32
**AI Companion:** `rtos-with-claude/` — 9 modules, 26 exercises
Parallel to Udemy "Mastering RTOS: Hands on FreeRTOS and STM32Fx with Debugging"

- Tasks, queues, semaphores, mutexes, software timers, memory management, debugging

---

## Phase 3: DSP & Audio

### 10. ✅ Topics in DSP
**Folder:** `topics-in-dsp/`
**Status:** Workbooks done.

- `workbooks-done/loudness-study-guide-2.html` — loudness analysis
- `workbooks-done/psychoacoustics-mastery-v3.html` — psychoacoustic modeling

### 11. 📘 PSD to LPC Guide
**Folder:** `psd_to_lpc_guide/`
**Status:** Reference material.

- Power Spectral Density → Linear Prediction Coefficients
- Levinson-Durbin algorithm (PDF + HTML guide)
- Fading FIR, LPC-to-FIR conversion

### 12. 📘 Audio Framework & VST Development
**Folder:** `audio-framework-vst/`
**Status:** Course available.

- 5-part HTML course: repository setup → fundamentals → first VST → testing → projects
- `index.html` — interactive course browser

### 13. 🔲 DSP Interview Prep — Level 1
**Folder:** `DSP_AI_Prep_1/`
**Status:** Available.

- 8 modules: C/C++ foundations → DSP & fixed-point → architecture & SIMD → embedded real-time → communications & ML → mock interview → expert drills
- `index.html` — interactive course browser

### 14. 🔲 DSP Interview Prep — Level 2
**Folder:** `DSP_AI_Prep_2/`
**Status:** Available.

- 11 modules: advanced C/C++ → performance engineering → SIMD lab → fixed-point advanced → architecture deep dive → hard DSP problems → ML inference → digital comms → coding interview → bilingual communication → final expert exam
- `index.html` — interactive course browser

---

## Phase 4: AI-Powered Development (Take These Alongside Any Phase)

### 15. 🟢 Cursor Zero to Hero
**Folder:** `cursor-course/`
**Status:** Available — 27 modules, 93 exercises.

- IDE mastery: Tab → Chat → Agent → Plan mode
- Project rules (.mdc), AGENTS.md, MCP, hooks, skills
- Git workflows, CI/CD, worktrees, cloud agents, automations
- **Model selection & AI worker advantages** (Module 25)
- DSP-focused throughout (biquad, FFT, golden vectors)

### 16. 🟢 Claude Code Zero to Hero
**Folder:** `claude-code-course/`
**Status:** Available — 22 modules, 92 exercises.

- Terminal-native CLI: `>` prompt, diff-accept, y/Y/n permissions
- CLAUDE.md persistent memory, /init, /compact, /cost, /model
- Headless mode (-p), SSH/Docker/tmux, CI/CD integration
- **Model selection & AI worker advantages** (Module 20)
- SDK for programmatic automation

### 17. 🟢 Claude Code Delegator — "Works FOR Me"
**Folder:** `claude-code-delegator-course/`
**Status:** Available — 21 modules, 89 exercises.

- You = tech lead, Claude = autonomous worker
- Task briefs, verification scripts, CLAUDE.md as employee handbook
- Headless delegation, batch operations, orchestration pipelines
- CI/CD integration, scheduled tasks, PR workflows
- **Model selection for delegation & AI mastery** (Module 19)
- Capstone: ship a feature writing ZERO implementation code

---

## Recommended Learning Order

```
START HERE
    │
    ├─── C Beginner to Advanced ──────────── [✅ Done / In Progress]
    │         │
    │         ├── Embedded C ─────────────── [+ AI: embedded-c-with-claude]
    │         │       │
    │         │       ├── MCU1 Drivers ───── [+ AI: mcu1-drivers-with-claude]
    │         │       │       │
    │         │       │       ├── MCU2 Peripherals [+ AI: mcu2-peripherals-with-claude]
    │         │       │       │       │
    │         │       │       │       └── RTOS FreeRTOS [+ AI: rtos-with-claude]
    │         │       │       │
    │         │       │       └── DSP Interview Prep 1 → Prep 2
    │         │       │
    │         │       └── Topics in DSP / PSD-to-LPC
    │         │
    │         └── C++ Beginner to Advanced ─ [✅ Done / In Progress]
    │                   │
    │                   ├── C++ with GCC ─── [✅ Done]
    │                   │
    │                   └── Audio Framework & VST
    │
    ├─── Python Basics ──────────────────── [✅ Done]
    │
    └─── AI Courses (take alongside ANY phase above)
              │
              ├── Cursor Zero to Hero ────── [Start here for IDE AI]
              │
              ├── Claude Code Zero to Hero ─ [Start here for terminal AI]
              │
              └── Claude Code Delegator ──── [After Claude Code basics]
```

---

## Quick Stats

| Category | Courses | Total Exercises |
|----------|---------|----------------|
| AI Coding Tools | 3 | 274 |
| Udemy Companions | 4 | 134 |
| DSP Interview Prep | 2 | (HTML courses) |
| Language Foundations | 4 | (workbook-based) |
| Embedded | 1 | (workbook-based) |
| DSP & Audio | 3 | (mixed format) |
| **Total** | **17 courses** | **408+ exercises** |

---

*Last updated: September 2026*
