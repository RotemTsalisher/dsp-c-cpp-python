#!/usr/bin/env python3
"""Companion course: Embedded C Programming WITH Claude Code.
Parallel to Udemy 'Microcontroller Embedded C Programming: Absolute Beginners' by FastBit.
Every module maps to a Udemy section and teaches Claude Code usage for that topic."""
from __future__ import annotations
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"

def ex(n, prompt, hints, solution, stretch=""):
    return {"id": n, "prompt": prompt, "hints": hints, "solution": solution, "stretch": stretch}

def md(text):
    lines = text.strip().split("\n"); out = []; in_pre = False; in_ul = False
    for line in lines:
        if line.startswith("```"):
            if in_pre: out.append("</code></pre>"); in_pre = False
            else:
                if in_ul: out.append("</ul>"); in_ul = False
                lang = line[3:].strip() or "text"
                out.append(f'<pre class="code-block" data-lang="{html.escape(lang)}"><code>'); in_pre = True
            continue
        if in_pre: out.append(html.escape(line)); continue
        if line.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h3>{html.escape(line[3:])}</h3>")
        elif line.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h4>{html.escape(line[4:])}</h4>")
        elif line.startswith("- "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{ilm(line[2:])}</li>")
        elif line.strip() == "":
            if in_ul: out.append("</ul>"); in_ul = False
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<p>{ilm(line)}</p>")
    if in_ul: out.append("</ul>")
    if in_pre: out.append("</code></pre>")
    return "\n".join(out)

def ilm(s):
    s = html.escape(s); parts = s.split("`")
    for i in range(1, len(parts), 2): parts[i] = f"<code>{parts[i]}</code>"
    return "".join(parts)

MODULES = [
    {
        "id": "00", "title": "How to Use This Companion Course", "level": "Setup",
        "summary": "This course runs PARALLEL to the Udemy Embedded C course. Each module here maps to a Udemy section — use Claude Code to accelerate your learning.",
        "body": md("""
## What this course is
This is a **companion course** to FastBit's "Microcontroller Embedded C Programming: Absolute Beginners" on Udemy. It does NOT replace the Udemy course — it teaches you how to use **Claude Code** alongside each section to:
- **Understand** theory faster by asking Claude to explain concepts
- **Write** exercises using Claude Code as your AI pair programmer
- **Debug** your code when things go wrong
- **Delegate** repetitive coding tasks to Claude while you focus on learning
- **Automate** build-test loops so you spend time learning, not fighting toolchains

## Setup checklist
1. ✅ Enrolled in the Udemy Embedded C course
2. ✅ Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
3. ✅ STM32CubeIDE installed (as the Udemy course requires)
4. ✅ STM32F407 Discovery board (or simulator)
5. ✅ VS Code with Claude Code extension (optional but recommended)

## How to follow along
- Watch a Udemy section
- Open the matching module HERE
- Do the exercises using Claude Code
- You learn embedded C AND Claude Code delegation simultaneously

## CLAUDE.md for this course
Create this at your project root immediately:
```markdown
# Embedded C Learning Project
## Target: STM32F407 Discovery Board
## Build: arm-none-eabi-gcc or STM32CubeIDE
## Language: C99 only
## Convention: explain every line with comments for learning
## Rule: when writing code, add comments explaining WHY, not just WHAT
```

## Model selection tip
For **learning and explanation**: use the default model (best reasoning).
For **code generation**: default model works well.
For **quick boilerplate** (register definitions, struct layouts): a faster model is fine.
Claude Code lets you switch with `/model` — use the right model for the task.
"""),
        "exercises": [
            ex("00-1", "Install Claude Code and create your embedded C project folder with src/, inc/, and tests/. Write a CLAUDE.md that tells Claude this is an STM32F407 learning project using C99.", "Include build commands, target info, and 'explain everything' rule.", "CLAUDE.md created with target info, build command, and learning-focused rules (verbose comments, explain WHY)."),
            ex("00-2", "Ask Claude: 'Explain the difference between hosted C (PC) and freestanding C (embedded) in 5 bullet points. Do not create files.' Verify it stays read-only.", "This tests Claude as a tutor, not a coder.", "Claude explains: no OS, no standard library (partial), startup code needed, volatile MMIO, linker scripts. No files touched."),
            ex("00-3", "Run `/model` to see your current model. Then ask Claude a simple C question and run `/cost` after. Note the cost for one Q&A round — this builds budget awareness for the whole course.", "Cost awareness from day one.", "Model shown. Cost for one round: typically $0.01–0.05. Awareness built."),
        ],
    },
    {
        "id": "01", "title": "IDE Installation & First Program", "level": "Beginner",
        "summary": "Udemy §1-3: IDE setup and your first C program. Use Claude Code to understand the toolchain and write hello world.",
        "body": md("""
## Udemy parallel: Introduction + IDE Installation + First C Program
While the Udemy course walks you through installing STM32CubeIDE and writing your first printf, here you learn to use Claude Code as your **toolchain explainer** and **code writer**.

## Claude Code as toolchain tutor
Instead of just following IDE screenshots, ask Claude:
- "Explain what a cross-compiler is and why I need arm-none-eabi-gcc for STM32"
- "What does the linker do in an embedded build? Explain for a complete beginner."
- "What's the difference between STM32CubeIDE and a plain text editor + Makefile?"

## Claude Code as code writer
For your first program, try delegation:
```
claude -p "Create a minimal C program that prints 'Hello Embedded World' using printf. \
  Add comments explaining every line for a complete beginner. \
  Save to src/main.c" --allowedTools Read,Edit
```

## Skills building: IDE + Claude Code together
- Use STM32CubeIDE for **building and flashing** (hardware interaction)
- Use Claude Code for **writing, explaining, and debugging code** (AI acceleration)
- They complement each other — IDE handles hardware, Claude handles intelligence

## Automation opportunity
Write a CLAUDE.md build section so Claude always knows how to compile:
```
## Build
Host build (learning): gcc -std=c99 -Wall -o build/main src/main.c
Target build: use STM32CubeIDE project or arm-none-eabi-gcc
```
"""),
        "exercises": [
            ex("01-1", "Ask Claude to explain the STM32CubeIDE build process: what happens when you press Build? (preprocessor → compiler → assembler → linker → .elf). Ask for a diagram in ASCII art.", "Learning the build chain with AI help.", "Claude explains each stage with ASCII flow diagram. You understand the pipeline the Udemy course shows in screenshots."),
            ex("01-2", "Delegate: 'Create src/hello.c with a main() that prints Hello World. Add a comment above every line explaining what it does for a beginner. Build with gcc on host.' Let Claude write AND build.", "Your first delegated program.", "Claude creates the file with verbose comments, builds with gcc. Every line explained. You learned by reading Claude's annotated code."),
            ex("01-3", "Ask Claude to create a Makefile for host-build (gcc) and add it to CLAUDE.md as the build command. From now on, Claude will use `make` to build.", "Automation: standardize the build process early.", "Makefile created. CLAUDE.md updated. All future delegations use `make`. You set up infrastructure once, benefit forever."),
        ],
    },
    {
        "id": "02", "title": "Data Types, Variables & Declarations", "level": "Beginner",
        "summary": "Udemy §4-5: Data types, variables, addresses. Use Claude Code to explore sizes, ranges, and memory layout.",
        "body": md("""
## Udemy parallel: Data Types and Variables + Address of Variable
The Udemy course teaches char, int, float, double, sizeof, addresses. Here you use Claude Code to **explore interactively** and **generate exercises**.

## Claude as a C tutor: exploring types
```
> Explain the difference between int8_t, int16_t, int32_t and why
  embedded engineers prefer them over int, short, long. Give examples.
```
Claude explains exact-width types, portability, and why `stdint.h` matters for register access.

## Claude as exercise generator
```
> Create a program that prints the sizeof every integer type and
  every stdint.h type. Format as a table. Add comments.
```
Claude generates the exploration program — you run it and learn.

## Claude for memory layout visualization
```
> Create a program that declares variables of different types and
  prints their addresses. Show me how they're laid out in memory.
  Explain stack growth direction.
```

## Embedded-specific type awareness
In CLAUDE.md add:
```
## Types
- ALWAYS use stdint.h types (uint8_t, int32_t, etc.)
- NEVER use bare int, short, long for hardware-related code
- size_t for sizes and indices
```
Now Claude follows this rule in ALL future code it writes for you.
"""),
        "exercises": [
            ex("02-1", "Ask Claude to create a program that prints sizeof() for every C data type AND every stdint.h type, formatted as a table. Build and run on host. Compare to what the Udemy course shows.", "Learning by exploration, not just watching.", "Program prints type sizes. You see that int may be 4 bytes on host but 2 bytes on some targets — stdint.h solves this."),
            ex("02-2", "Ask Claude to create a program that demonstrates variable overflow: increment a uint8_t from 250 and print each step. Then do the same with int8_t from 125. Add comments explaining what happens.", "Overflow visualization — a critical embedded concept.", "Program shows unsigned wrap-around (255→0) and signed overflow (127→-128). Comments explain two's complement."),
            ex("02-3", "Ask Claude to create a program showing addresses of local variables, demonstrating stack layout. Ask it to explain the output with comments showing which direction the stack grows.", "Memory layout understanding via Claude.", "Program prints &a, &b, &c showing stack addresses. Claude explains growth direction and alignment."),
        ],
    },
    {
        "id": "03", "title": "Storage Classes & Functions", "level": "Beginner",
        "summary": "Udemy §6-7: auto, static, extern, register, functions. Use Claude Code to generate examples and explain scope.",
        "body": md("""
## Udemy parallel: Storage Classes + Functions
Storage classes (auto, static, extern, register) and functions are abstract concepts. Claude Code makes them concrete with **generated examples** and **instant explanations**.

## Claude as concept demonstrator
```
> Create a program that demonstrates the difference between a local
  static variable and a regular local variable inside a function
  called 10 times. Print the values each time.
```

## Claude for function design
Instead of writing functions from scratch while learning, delegate:
```
> Create a function uint32_t factorial(uint8_t n) with:
  - Input validation (n <= 20)
  - Comments explaining the algorithm
  - A main() that tests it with values 0, 1, 5, 10, 20
```

## Skill: building reusable knowledge
Every time Claude explains a concept well, ask it to save the explanation:
```
> Add a section to docs/notes.md explaining static vs auto vs extern
  with one-line summaries I can reference later.
```
This builds YOUR knowledge base as you go through the Udemy course.
"""),
        "exercises": [
            ex("03-1", "Ask Claude to create a program demonstrating all 4 storage classes with concrete examples. Each variable should be labeled with its storage class and a comment explaining its lifetime and scope.", "All storage classes in one program.", "Program with auto (default), static (persists), extern (cross-file), register (hint) variables. Comments explain lifetime and visibility."),
            ex("03-2", "Delegate: 'Create src/math_utils.c and src/math_utils.h with 5 basic math functions (add, subtract, multiply, divide with zero-check, modulo). Main tests all of them. Build and run.'", "Function library delegation.", "Two files created. Header with prototypes. Source with implementations. Main tests all. Build passes. You learned function organization by reading Claude's well-structured code."),
            ex("03-3", "Ask Claude to create a program that uses a static variable to count how many times a function is called, without using a global. Then ask it to explain why this is better than a global for embedded.", "Static for state — embedded pattern.", "Counter function uses static local. Claude explains: no namespace pollution, thread-safety considerations, linker section implications."),
        ],
    },
    {
        "id": "04", "title": "Microcontroller Hello World & Build Process", "level": "Beginner",
        "summary": "Udemy §8-9: MCU startup, build process, analyzing .elf and .map. Use Claude Code to understand the embedded build chain.",
        "body": md("""
## Udemy parallel: Microcontroller Hello World + Build Process
This is where embedded diverges from hosted C. The Udemy course shows startup code, vector tables, and .map files. Claude Code makes these **understandable**.

## Claude as build process explainer
```
> Explain the complete build process for an STM32F407 program:
  1. Preprocessing
  2. Compilation to assembly
  3. Assembly to object files
  4. Linking with startup code and linker script
  5. Output formats (.elf, .bin, .hex)
  Draw an ASCII diagram showing the flow.
```

## Claude for startup code analysis
```
> Explain what STM32 startup code does before main() is called.
  Cover: stack pointer init, .data copy, .bss zeroing, vector table,
  SystemInit, __libc_init_array. Explain each for a beginner.
```

## Claude for .map file reading
When you generate a .map file from your build, paste a section into Claude:
```
> Here is a section of my .map file. Explain what each line means:
  .text  0x08000000  0x1234  startup_stm32f407.o
  .data  0x20000000  0x0020  main.o
```

## Automation: build scripts
```
> Create scripts/build.sh that runs arm-none-eabi-gcc with appropriate
  flags for STM32F407. Include: -mcpu=cortex-m4, -mthumb, -mfpu=fpv4-sp-d16,
  -specs=nosys.specs. Add this to CLAUDE.md.
```
"""),
        "exercises": [
            ex("04-1", "Ask Claude to draw an ASCII diagram of the STM32F407 memory map: Flash (0x08000000), SRAM (0x20000000), peripherals (0x40000000). Label sizes. Compare to the Udemy course's diagram.", "Memory map understanding.", "ASCII diagram showing Flash, SRAM, peripheral regions with addresses and sizes. Matches the Udemy course content but generated interactively."),
            ex("04-2", "Ask Claude to explain what happens between power-on and main() on an STM32. Cover: vector table fetch, stack pointer load, Reset_Handler, .data/.bss init, SystemInit, main. Step by step.", "Startup sequence demystified.", "Step-by-step explanation of startup. You understand what the Udemy video shows but now can ask follow-up questions."),
            ex("04-3", "Delegate: 'Create a linker script cheatsheet in docs/linker-notes.md explaining MEMORY, SECTIONS, .text, .data, .bss, .rodata for STM32F407 in beginner-friendly language.' This becomes your reference.", "Building your own reference docs with Claude.", "Cheatsheet created. Reusable reference for the rest of the Udemy course. Claude explains what the Udemy video glosses over."),
        ],
    },
    {
        "id": "05", "title": "Pointers: The Embedded Superpower", "level": "Intermediate",
        "summary": "Udemy §13: Pointers, pointer arithmetic, casting. Use Claude Code to visualize memory and practice safely.",
        "body": md("""
## Udemy parallel: Pointers
Pointers are THE critical concept for embedded C. They're how you access hardware registers, DMA buffers, and memory-mapped peripherals. Claude Code helps you **practice without fear**.

## Claude as pointer visualizer
```
> Create a program that declares an int, a pointer to it, and a pointer
  to that pointer. Print all values and addresses in a formatted table
  showing the chain: value ← *p ← **pp. Add ASCII art showing memory.
```

## Claude for register access pattern
```
> Show me how to use a pointer to write to a memory-mapped register
  at address 0x40020014 (GPIOD ODR on STM32F407). Explain volatile,
  casting, and why we dereference. Step by step for a beginner.
```

## Claude for pointer arithmetic exploration
```
> Create a program that demonstrates pointer arithmetic with different
  types: char*, int*, double*. Show how p+1 moves by sizeof(type).
  Print addresses to prove it.
```

## Skill: asking Claude for analogies
```
> Explain pointers using a real-world analogy that a beginner would
  understand. Then explain pointer-to-pointer with the same analogy.
```
This is where AI tutoring shines — personalized explanations on demand.
"""),
        "exercises": [
            ex("05-1", "Ask Claude to create a program visualizing pointer relationships: variable, pointer, pointer-to-pointer. Print addresses and values in a formatted table. Build and run.", "Pointer chain visualization.", "Program prints a table showing: variable address, value, pointer holding that address, pointer-to-pointer. Chain is clear."),
            ex("05-2", "Ask Claude to create a program demonstrating how to read/write a 'simulated hardware register' using volatile uint32_t* on host (use a regular variable as the 'register'). Explain why volatile is needed.", "Register access pattern — THE embedded pointer pattern.", "Program shows: `volatile uint32_t *reg = &simulated_reg; *reg |= (1 << 5);` Pattern is what the Udemy course teaches for real GPIO."),
            ex("05-3", "Delegate: 'Create a mini library src/register_access.h with macros: REG_READ(addr), REG_WRITE(addr, val), REG_SET_BIT(addr, bit), REG_CLEAR_BIT(addr, bit). All using volatile pointers. Add a test program.'", "Register access library — reusable for the whole Udemy course.", "Macros created with volatile casts. Test program verifies each macro. This is real embedded infrastructure you'll use throughout."),
        ],
    },
    {
        "id": "06", "title": "Operators & Decision Making", "level": "Intermediate",
        "summary": "Udemy §12,15: Arithmetic, logical, relational, ternary operators and if/else/switch. Claude generates practice exercises.",
        "body": md("""
## Udemy parallel: Operators + Decision Making
Operators are straightforward but practice makes perfect. Claude Code generates **unlimited exercises** tailored to embedded contexts.

## Claude as exercise generator
```
> Generate 5 embedded-themed operator exercises. Each should involve:
  a register value, a bit operation, and a conditional check.
  Include expected output. I'll solve them, then check with you.
```

## Claude for operator precedence
```
> Show me 5 tricky operator precedence examples in C where the result
  is NOT what you'd expect. For each, show the expression, the actual
  result, and WHY (with parenthesized version).
```

## Automation: exercise-check pattern
1. Ask Claude to generate an exercise (without solution)
2. YOU solve it
3. Ask Claude to check your answer
4. If wrong, ask Claude to explain WHY

This is AI-accelerated learning: infinite practice with instant feedback.
"""),
        "exercises": [
            ex("06-1", "Ask Claude to generate 5 register-manipulation expressions using arithmetic and bitwise operators. Solve them on paper first. Then ask Claude to verify your answers.", "Practice with instant AI feedback.", "5 expressions like: `(0xFF & (reg >> 8))`, `(reg | (1 << 3)) & ~(1 << 7)`. You solved them, Claude verified. Instant feedback loop."),
            ex("06-2", "Ask Claude to create a program with a switch statement that decodes a 'status register' value into human-readable error messages. Each case should handle a different bit pattern.", "Decision-making applied to embedded registers.", "Switch on register bits. Each case maps to an error/status. Comments explain the bit patterns. Real embedded pattern."),
            ex("06-3", "Ask Claude to create 3 operator precedence 'trap' examples and explain each. Then ask it to add these as warnings to your docs/c-traps.md reference.", "Building a personal reference of C pitfalls.", "3 precedence traps documented with explanations. Reference file grows as you learn. Claude helps you build YOUR knowledge base."),
        ],
    },
    {
        "id": "07", "title": "Bitwise Operators & LED Exercise", "level": "Intermediate",
        "summary": "Udemy §16-18: Bitwise AND/OR/XOR/NOT/shift, LED GPIO control. Claude Code makes bit manipulation visual and testable.",
        "body": md("""
## Udemy parallel: Bitwise Operators + Embedded C LED Exercise + Shift Operators
This is the CORE of embedded C. Every register interaction uses bitwise operators. Claude Code makes bit manipulation **visual and verifiable**.

## Claude as bit visualizer
```
> Create a program that takes a uint32_t value and prints it in binary,
  hex, and decimal. Then show the result of: AND with mask, OR with mask,
  XOR toggle, NOT, left shift, right shift. Print each step in binary.
```

## Claude for GPIO LED exercise
The Udemy course has you toggle LEDs via GPIO registers. Claude can:
```
> Explain exactly how to turn on LED on PD12 of STM32F407 Discovery:
  1. Enable GPIOD clock (RCC->AHB1ENR)
  2. Set PD12 as output (GPIOD->MODER)
  3. Set PD12 high (GPIOD->ODR)
  Show the exact register addresses and bit positions.
```

## Claude for bit manipulation practice
```
> Generate 10 bit manipulation exercises typical of embedded interviews:
  set bit N, clear bit N, toggle bit N, check if bit N is set,
  extract bits [M:N], set bits [M:N] to a value. Give me the problems
  first (no solutions). I'll solve them.
```

## Automation: bit operation macros
```
> Create inc/bit_ops.h with macros: SET_BIT(reg,n), CLEAR_BIT(reg,n),
  TOGGLE_BIT(reg,n), CHECK_BIT(reg,n), EXTRACT_BITS(val,high,low).
  Test program verifies each. Add to CLAUDE.md as standard include.
```
"""),
        "exercises": [
            ex("07-1", "Ask Claude to create a 'bit visualizer' program: input a uint32_t and operation (AND/OR/XOR/NOT/SHIFT), print before and after in binary. Build and test with GPIO-relevant values.", "Bit operations made visual.", "Interactive bit visualizer. You input register values and see results in binary. Perfect companion to the Udemy LED exercises."),
            ex("07-2", "Delegate: 'Create inc/stm32f407_gpio.h with #define macros for GPIOD base address, MODER, ODR, IDR register offsets, and pin positions for PD12-PD15 (the 4 LEDs on Discovery board). Add a comment map.'", "Register map header — real embedded infrastructure.", "Header with address definitions. Comments show bit positions. This is what the Udemy course teaches you to use — Claude generates the boilerplate."),
            ex("07-3", "Ask Claude to generate 10 bit manipulation problems (no solutions). Solve them on paper. Then ask Claude to grade your answers and explain any mistakes.", "Embedded interview prep via AI tutoring.", "10 problems → you solve → Claude grades → explanations for mistakes. This is targeted practice the Udemy course can't provide."),
        ],
    },
    {
        "id": "08", "title": "Looping & Control Flow", "level": "Intermediate",
        "summary": "Udemy §19: for, while, do-while. Use Claude Code to generate embedded-context loop exercises and debug infinite loops.",
        "body": md("""
## Udemy parallel: Looping
Loops in embedded C often mean: polling registers, processing buffers, delay loops, DMA transfers. Claude Code generates **embedded-context** loop exercises.

## Claude for embedded loop patterns
```
> Create examples of each embedded loop pattern:
  1. Polling a status register until a flag is set (while)
  2. Processing N samples in a buffer (for)
  3. Retry with timeout (do-while with counter)
  4. Infinite main loop with state machine (while(1))
  Add comments explaining when each pattern is used in firmware.
```

## Claude for loop debugging
```
> This loop doesn't terminate. Find the bug:
  for(int i = 0; i < 10; +i) { ... }
  Explain the difference between +i and ++i.
```

## Automation: loop-based test generators
```
> Create a test that loops through all uint8_t values (0-255)
  and verifies my bit manipulation macros work correctly for each.
  This is exhaustive testing — only feasible with auto-generated code.
```
"""),
        "exercises": [
            ex("08-1", "Ask Claude to create a program with all 4 embedded loop patterns (polling, buffer processing, retry-with-timeout, main loop). Each in its own function with comments explaining the real-world use case.", "Loop patterns catalog for embedded.", "Four functions demonstrating four patterns. Comments explain: 'This is how you wait for SPI transfer complete', 'This is how you process ADC samples', etc."),
            ex("08-2", "Delegate: 'Create a test harness that exhaustively tests my SET_BIT, CLEAR_BIT, TOGGLE_BIT macros for all 32 bit positions on a uint32_t. Report pass/fail for each.' Build and run.", "Exhaustive testing via loop + delegation.", "Test loops through 32 bit positions, verifies each macro. 96 tests total. All pass (or Claude fixes failures). You didn't write a single test — Claude did."),
            ex("08-3", "Give Claude a buggy loop (e.g., wrong increment, wrong condition) and ask it to diagnose WITHOUT running the code. See if it catches the bug from reading alone.", "AI debugging practice.", "Claude identifies the bug (e.g., `+i` instead of `++i`, `<=` causing overflow). You learn common loop bugs."),
        ],
    },
    {
        "id": "09", "title": "Const, Volatile & Type Qualifiers", "level": "Advanced",
        "summary": "Udemy §20-22: const correctness, volatile for MMIO, const volatile. Claude explains the WHY behind these critical qualifiers.",
        "body": md("""
## Udemy parallel: const + volatile + Pin Read
These qualifiers are **essential** for embedded C and often misunderstood. Claude Code explains them with **compiler-output examples**.

## Claude for volatile understanding
```
> Create two versions of a register-polling loop: one WITH volatile,
  one WITHOUT. Show the assembly output (or explain how the compiler
  optimizes away the read without volatile). This is critical for
  embedded correctness.
```

## Claude for const correctness
```
> Explain every combination: const int*, int* const, const int* const.
  Give an embedded example for each (read-only register, fixed pointer
  to register, ROM constant). Create a test showing compile errors
  when you violate const.
```

## Claude for const volatile
```
> When would you use 'const volatile uint32_t*' in embedded C?
  Give 3 real examples. Explain why BOTH qualifiers are needed.
```
Answer: read-only status registers, hardware counters, timer capture values.

## CLAUDE.md rule
```
## Qualifiers
- ALL memory-mapped register pointers MUST be volatile
- ALL input-only buffer pointers MUST be const
- const volatile for read-only hardware registers
```
"""),
        "exercises": [
            ex("09-1", "Ask Claude to create a program demonstrating the danger of missing volatile: a loop that reads a 'register' (simulated with a variable modified by a signal handler or second thread). Show it works with volatile and breaks without.", "volatile is not optional in embedded.", "Two versions: with volatile (works), without volatile (compiler optimizes away the read, loop never exits). Critical embedded lesson."),
            ex("09-2", "Ask Claude to create a 'const correctness quiz': 5 pointer declarations, you identify what's const (pointer, pointee, both). Then Claude reveals answers.", "const correctness drill.", "5 declarations like `const int * const p`. You parse each. Claude grades. This is an embedded interview classic."),
            ex("09-3", "Add const and volatile rules to CLAUDE.md. Then delegate a task that involves register pointers. Verify Claude applies volatile correctly without being told.", "Automated rule enforcement for qualifiers.", "CLAUDE.md updated. Delegated task produces code with volatile on register pointers. Rule enforced automatically."),
        ],
    },
    {
        "id": "10", "title": "Structures, Unions & Bit Fields", "level": "Advanced",
        "summary": "Udemy §23-26: Structs for register maps, unions for type punning, bit fields for peripherals. Claude generates real STM32 register structures.",
        "body": md("""
## Udemy parallel: Structures + Unions + Bit Fields + Usage in Embedded
This is where C meets hardware. Structures map to register blocks. Bit fields map to register bits. Claude Code generates **real register map structures**.

## Claude for register struct generation
```
> Create a C struct that maps to the STM32F407 GPIO peripheral registers.
  Include: MODER, OTYPER, OSPEEDR, PUPDR, IDR, ODR, BSRR, LCKR, AFRL, AFRH.
  Each field should be volatile uint32_t. Add offset comments.
  Then show how to use it: GPIO_TypeDef *GPIOD = (GPIO_TypeDef*)0x40020C00;
```

## Claude for bit field explanation
```
> Create a bit field struct for the GPIO MODER register (32 bits,
  16 fields of 2 bits each for pins 0-15). Show how to set pin 12
  to output mode using the bit field vs using raw bit manipulation.
  Compare readability.
```

## Claude for union type punning
```
> Show how to use a union to interpret a 32-bit register value as:
  1. A uint32_t (raw value)
  2. A struct with individual bit fields
  3. An array of 4 uint8_t (byte access)
  Explain when each view is useful in embedded.
```

## Automation: register map generation
```
> Read the STM32F407 reference manual section for USART registers
  and generate a complete USART_TypeDef struct with all registers.
  Add this to inc/stm32f407_usart.h.
```
Claude can generate entire register map headers from documentation.
"""),
        "exercises": [
            ex("10-1", "Delegate: 'Create inc/stm32f407_gpio_regs.h with a GPIO_TypeDef struct mapping all GPIO registers for STM32F407. Include base addresses for GPIOA through GPIOE. Add usage example in comments.'", "Real register map generation.", "Complete GPIO register struct with all 10 registers. Base address macros. Usage example showing `GPIOD->ODR |= (1<<12)`. Real infrastructure."),
            ex("10-2", "Ask Claude to create a program demonstrating union type punning: interpret a 'register value' as raw uint32_t, as a bit field struct, and as 4 bytes. Print all three views.", "Union for register interpretation.", "Three views of the same 32-bit value. Claude explains when each is useful: raw for speed, bit field for readability, byte for serialization."),
            ex("10-3", "Ask Claude to explain struct padding and alignment issues on ARM Cortex-M4. Create a program showing sizeof with and without __attribute__((packed)). Explain when packing matters for register maps.", "Padding and alignment — advanced embedded C.", "Program shows padded vs packed struct sizes. Claude explains: register maps MUST match hardware layout, packing ensures no gaps."),
        ],
    },
    {
        "id": "11", "title": "Arrays, Strings & Preprocessor", "level": "Advanced",
        "summary": "Udemy §27-29: Arrays, strings, and preprocessor directives. Claude generates lookup tables, string handlers, and macro libraries.",
        "body": md("""
## Udemy parallel: Arrays + Strings + Preprocessor Directives
Arrays are buffers. Strings are messages. Preprocessor is configuration. Claude Code generates these **at scale**.

## Claude for lookup table generation
```
> Generate a const uint16_t sine_table[256] with one full sine wave
  period, scaled to 0-4095 (12-bit DAC range). Add a comment showing
  the formula used.
```
This would take you 30 minutes manually. Claude does it in 5 seconds.

## Claude for embedded string handling
```
> Create safe string functions for embedded: my_strlen, my_strcpy_safe
  (with buffer size), my_strcmp. No standard library. Add tests.
  These must be ISR-safe (no malloc, no printf inside).
```

## Claude for preprocessor mastery
```
> Create a configuration header inc/project_config.h using preprocessor:
  - #define for board version (V1, V2)
  - Conditional compilation for debug/release
  - Static assert macro for compile-time checks
  - Stringify and concatenation macros for register names
```

## Skill: code generation at scale
Ask Claude to generate large arrays, lookup tables, and configuration headers. This is where AI delegation saves the most time — boilerplate generation.
"""),
        "exercises": [
            ex("11-1", "Delegate: 'Generate a const float32 raised-cosine lookup table with 1024 entries in inc/cosine_table.h. Include the generation formula in a comment. Add a test that verifies table[0], table[256], table[512], table[768].'", "Lookup table generation — AI at its best.", "1024-entry table generated instantly. Test verifies key values. Manual creation would take an hour."),
            ex("11-2", "Delegate: 'Create inc/project_config.h with preprocessor-based configuration: DEBUG/RELEASE mode, BOARD_VERSION (V1/V2), LED_PIN selection per board version, compile-time size assertion macro. Comment each section.'", "Configuration infrastructure via delegation.", "Config header with conditional compilation. Board-specific settings. Debug/release toggles. Real embedded project infrastructure."),
            ex("11-3", "Ask Claude to create 5 preprocessor 'gotcha' examples (macro pitfalls) and explain each. Add to docs/c-traps.md.", "Preprocessor pitfalls reference.", "5 gotchas: missing parentheses in macros, double evaluation, stringification surprises, include guard mistakes, #if vs #ifdef. Knowledge base grows."),
        ],
    },
    {
        "id": "12", "title": "Capstone: LED + Keypad Project", "level": "Expert",
        "summary": "Udemy final sections: LED toggle + keypad interfacing. Delegate the ENTIRE project to Claude, review like a tech lead.",
        "body": md("""
## Udemy parallel: Embedded C Coding Exercise for LED + Keypad Interfacing
The Udemy course ends with practical projects. Here you delegate them ENTIRELY to Claude Code and review the output.

## Full delegation workflow
1. Write task brief `tasks/led-keypad.md`
2. Write verification script `scripts/verify_led_keypad.sh`
3. Delegate headless
4. Review the result
5. Merge

## Task brief template for capstone
```markdown
# Task: LED Toggle via Keypad

## Deliverables
- src/main.c — main application
- inc/gpio.h — GPIO configuration functions
- inc/keypad.h — 4x4 keypad scanner
- src/gpio.c, src/keypad.c — implementations

## Specifications
- STM32F407 Discovery board
- 4 LEDs on PD12-PD15
- 4x4 matrix keypad on GPIOE
- Key '1' toggles LED1, '2' toggles LED2, etc.
- Debounce: 50ms delay after key detect

## Constraints
- C99, no HAL library, bare metal register access
- All registers via volatile pointer casts
- stdint.h types only
- Every function commented for learning
```

## The ultimate test of this companion course
Can you write a spec good enough that Claude implements the capstone correctly on the first try? If yes — you've mastered both Embedded C concepts AND AI delegation.
"""),
        "exercises": [
            ex("12-1", "Write `tasks/led-toggle.md`: a complete task brief for a bare-metal LED toggle program on STM32F407. Include register addresses, bit positions, and acceptance criteria. Do NOT involve Claude.", "Spec writing is YOUR skill.", "Complete task brief. You know the registers because you learned them in the Udemy course. Claude doesn't need to know — YOUR spec is the knowledge."),
            ex("12-2", "Delegate the LED toggle task headless. Then review the code: does it set RCC->AHB1ENR correctly? Does it configure GPIOD->MODER for output? Does it write to GPIOD->ODR?", "Delegation + domain-specific review.", "Claude implements. You review with domain knowledge from the Udemy course. The combination is powerful: you understand the hardware, Claude writes the code."),
            ex("12-3", "Write a task brief for the full keypad scanner. Include the scanning algorithm (row drive, column read). Delegate. Review. This is your graduation exercise.", "Full capstone delegation.", "Keypad scanner implemented. Matrix scanning algorithm correct. Debounce included. You specified it, Claude built it, you verified it. Course complete."),
        ],
    },
    {
        "id": "drills", "title": "Daily Drills", "level": "All levels",
        "summary": "5-minute exercises pairing Udemy topics with Claude Code usage.",
        "body": md("""
## How to use drills
One drill per day while going through the Udemy course. Each drill connects a C concept to a Claude Code skill.
"""),
        "exercises": [
            ex("D-01", "Ask Claude to quiz you on data type sizes for ARM Cortex-M4. 5 questions, you answer, Claude grades.", "Type knowledge drill.", "Quick quiz and grade. Reinforces what the Udemy course teaches."),
            ex("D-02", "Ask Claude to generate a bit manipulation problem. Solve on paper. Ask Claude to verify.", "Bit ops practice.", "One problem, solved, verified. 2 minutes."),
            ex("D-03", "Ask Claude to explain one concept from today's Udemy lecture in a different way than the instructor.", "Alternative explanations.", "Different perspective. Sometimes Claude's explanation clicks better."),
            ex("D-04", "Delegate a small task from today's Udemy exercises headless. Review the output.", "Delegation speed drill.", "Small task delegated and reviewed in under 3 minutes."),
            ex("D-05", "Add one new rule to CLAUDE.md based on what you learned today.", "Growing your AI worker's handbook.", "CLAUDE.md improves daily. Claude gets better at following your project conventions."),
            ex("D-06", "Run `/cost` and note your daily Claude Code spending. Are you using it efficiently?", "Cost awareness.", "Daily cost tracked. Awareness of what interactions cost the most."),
            ex("D-07", "Ask Claude to create a one-page cheat sheet for today's Udemy topic. Save to docs/.", "Building your reference library.", "Cheat sheet added to docs/. Reference library grows throughout the course."),
            ex("D-08", "Write a task brief for tomorrow's Udemy exercise BEFORE watching the lecture. See how your spec quality improves.", "Pre-lecture spec writing.", "Brief written. After lecture, compare: did you spec correctly? Spec quality improves over time."),
        ],
    },
]

ACCENT = "#16a34a"; ACCENT2 = "#4ade80"; STORAGE = "embedded-c-with-claude-v1"
TITLE = "Embedded C with Claude Code — Udemy Companion"
SUBTITLE = "Parallel to FastBit Embedded C · AI-Accelerated Learning · Delegation · Automation"

# ── HTML template (shared pattern) ────────────────────────────────────
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>""" + TITLE + r"""</title>
<style>
:root{--bg:#0f1419;--surface:#1a2332;--surface2:#243044;--text:#e7ecf3;--muted:#9aa8bc;--accent:""" + ACCENT + r""";--accent2:""" + ACCENT2 + r""";--warn:#fbbf24;--ok:#4ade80;--border:#2d3a4f;--ex:#1e2a3d;font-family:"Segoe UI",system-ui,sans-serif}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);line-height:1.55}a{color:var(--accent2)}.layout{display:grid;grid-template-columns:300px 1fr;min-height:100vh}nav.sidebar{background:var(--surface);border-right:1px solid var(--border);padding:1rem;overflow-y:auto;position:sticky;top:0;height:100vh}nav.sidebar h1{font-size:1.05rem;margin:0 0 .25rem;line-height:1.3}nav.sidebar .sub{font-size:.78rem;color:var(--muted);margin-bottom:1rem}nav.sidebar input{width:100%;padding:.45rem .6rem;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);margin-bottom:.75rem}nav.sidebar ul{list-style:none;padding:0;margin:0}nav.sidebar li{margin-bottom:.15rem}nav.sidebar button.module-link{width:100%;text-align:left;background:0 0;border:none;color:var(--text);padding:.35rem .5rem;border-radius:6px;cursor:pointer;font-size:.82rem}nav.sidebar button.module-link:hover{background:var(--surface2)}nav.sidebar button.module-link.active{background:var(--accent);color:#061018;font-weight:600}nav.sidebar .level{font-size:.65rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin-top:.75rem;margin-bottom:.25rem}.progress-wrap{margin:1rem 0;font-size:.75rem;color:var(--muted)}.progress-bar{height:6px;background:var(--bg);border-radius:99px;overflow:hidden;margin-top:.35rem}.progress-bar>div{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0;transition:width .3s ease}main{padding:1.5rem 2rem 4rem;max-width:920px}.hero{margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}.hero h2{margin:0 0 .5rem;font-size:1.75rem}.hero p{color:var(--muted);margin:0}.badge{display:inline-block;font-size:.7rem;padding:.15rem .45rem;border-radius:4px;background:var(--surface2);color:var(--accent2);margin-right:.35rem}.lesson h3{margin-top:1.5rem;color:var(--accent2)}.lesson h4{margin-top:1rem}.lesson pre.code-block{background:#0a0e14;border:1px solid var(--border);border-radius:8px;padding:.85rem 1rem;overflow-x:auto;font-size:.82rem}.lesson code{background:var(--surface2);padding:.1rem .35rem;border-radius:4px;font-size:.88em}.exercise{background:var(--ex);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;padding:1rem 1.1rem;margin:1.25rem 0}.exercise header{display:flex;justify-content:space-between;align-items:flex-start;gap:.75rem;flex-wrap:wrap}.exercise h5{margin:0;font-size:.95rem}.exercise .ex-id{font-size:.72rem;color:var(--muted);font-family:ui-monospace,monospace}.exercise .prompt{margin:.75rem 0}.exercise .hint{font-size:.85rem;color:var(--muted);border-top:1px dashed var(--border);padding-top:.65rem;margin-top:.65rem}.exercise .actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.75rem}button.btn{border:none;border-radius:6px;padding:.45rem .85rem;cursor:pointer;font-size:.82rem;font-weight:600}button.btn-primary{background:var(--accent);color:#fff}button.btn-ghost{background:var(--surface2);color:var(--text)}button.btn-ok{background:#166534;color:#ecfdf5}.exercise.done{border-left-color:var(--ok);opacity:.92}.solution{display:none;margin-top:.85rem;padding:.85rem;background:#0a0e14;border-radius:6px;border:1px solid var(--border);white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace;font-size:.8rem}.solution.visible{display:block}.stretch{margin-top:.5rem;font-size:.82rem;color:var(--warn)}@media(max-width:900px){.layout{grid-template-columns:1fr}nav.sidebar{position:relative;height:auto}}</style></head><body><div class="layout"><nav class="sidebar" aria-label="Course navigation"><h1 id="course-title">Loading…</h1><p class="sub" id="course-sub"></p><div class="progress-wrap"><span id="progress-label">0 / 0 exercises</span><div class="progress-bar"><div id="progress-fill"></div></div></div><input type="search" id="search" placeholder="Filter modules…" aria-label="Filter modules"/><p class="level">Modules</p><ul id="module-list"></ul></nav><main><section class="hero"><h2 id="module-title">Welcome</h2><div id="module-meta"></div><p id="module-summary" style="margin-top:.75rem;color:var(--muted)"></p><p style="font-size:.85rem;color:var(--muted);margin-top:1rem">Open this file in any browser. Progress saves locally. <strong>%%TOTAL%% exercises</strong> · companion to Udemy Embedded C course.</p></section><section class="lesson" id="lesson-body"></section><section><h3 style="color:var(--accent2)">Exercises</h3><p id="exercise-count" style="color:var(--muted);font-size:.9rem"></p><div id="exercises"></div></section></main></div><script>window.COURSE_DATA=%%DATA%%;</script><script>
const SK='""" + STORAGE + r"""';function lp(){try{return JSON.parse(localStorage.getItem(SK)||'{}')}catch{return{}}}function sp(p){localStorage.setItem(SK,JSON.stringify(p))}function ce(ms){return ms.reduce((n,m)=>n+(m.exercises?.length||0),0)}function rl(ms,ai,f){const ul=document.getElementById('module-list');ul.innerHTML='';const q=(f||'').toLowerCase();ms.forEach(m=>{const h=(m.title+' '+m.summary+' '+m.level).toLowerCase();if(q&&!h.includes(q))return;const li=document.createElement('li');const b=document.createElement('button');b.className='module-link'+(m.id===ai?' active':'');b.textContent=m.id==='drills'?'⚡ '+m.title:m.id+' · '+m.title;b.onclick=()=>sm(m.id);li.appendChild(b);ul.appendChild(li)})}function sm(id){const m=C.modules.find(x=>x.id===id)||C.modules[0];history.replaceState(null,'','#'+m.id);document.getElementById('module-title').textContent=m.title;document.getElementById('module-meta').innerHTML=`<span class="badge">${m.level}</span><span class="badge">Module ${m.id}</span>`;document.getElementById('module-summary').textContent=m.summary;document.getElementById('lesson-body').innerHTML=m.body;const er=document.getElementById('exercises');er.innerHTML='';const p=lp();(m.exercises||[]).forEach(e=>{const d=p[e.id];const el=document.createElement('article');el.className='exercise'+(d?' done':'');el.innerHTML=`<header><h5>Exercise</h5><span class="ex-id">${e.id}</span></header><p class="prompt">${eh(e.prompt)}</p>${e.hints?`<div class="hint"><strong>Hint:</strong> ${eh(e.hints)}</div>`:''}${e.stretch?`<div class="stretch"><strong>Stretch:</strong> ${eh(e.stretch)}</div>`:''}<div class="actions"><button type="button" class="btn btn-primary btn-solution">Reveal solution</button><button type="button" class="btn btn-ghost btn-hide">Hide solution</button><button type="button" class="btn btn-ok btn-done">${d?'✓ Completed':'Mark complete'}</button></div><div class="solution" role="region">${eh(e.solution)}</div>`;el.querySelector('.btn-solution').onclick=()=>{el.querySelector('.solution').classList.add('visible')};el.querySelector('.btn-hide').onclick=()=>{el.querySelector('.solution').classList.remove('visible')};el.querySelector('.btn-done').onclick=ev=>{p[e.id]=true;sp(p);el.classList.add('done');ev.target.textContent='✓ Completed';ub()};er.appendChild(el)});rl(C.modules,m.id,document.getElementById('search').value);document.getElementById('exercise-count').textContent=(m.exercises||[]).length+' exercises in this module';ub()}function eh(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}function ub(){const t=ce(C.modules);const p=lp();const d=Object.keys(p).filter(k=>p[k]).length;const pc=t?Math.round(d/t*100):0;document.getElementById('progress-label').textContent=`${d} / ${t} exercises (${pc}%)`;document.getElementById('progress-fill').style.width=pc+'%'}function init(){const d=window.COURSE_DATA;window.C=d;document.getElementById('course-title').textContent=d.title;document.getElementById('course-sub').textContent=d.subtitle;document.getElementById('search').oninput=e=>{const id=(location.hash||'#00').slice(1);rl(C.modules,id,e.target.value)};const si=(location.hash||'#00').replace('#','');sm(C.modules.some(m=>m.id===si)?si:'00');window.onhashchange=()=>{const id=(location.hash||'#00').slice(1);if(C.modules.some(m=>m.id===id))sm(id)}}document.addEventListener('DOMContentLoaded',init);
</script></body></html>"""

def main():
    course = {"title": TITLE, "subtitle": SUBTITLE, "version": "2026.09", "modules": MODULES}
    total = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(course, ensure_ascii=False)
    page = HTML_TEMPLATE.replace("%%DATA%%", data_json).replace("%%TOTAL%%", str(total))
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT}  ({total} exercises across {len(MODULES)} modules)")

if __name__ == "__main__":
    main()
