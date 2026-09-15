#!/usr/bin/env python3
"""Companion: MCU1 Driver Development WITH Claude Code.
Parallel to Udemy 'Mastering Microcontroller and Embedded Driver Development' by FastBit."""
from __future__ import annotations
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent; OUT = ROOT / "index.html"
def ex(n,p,h,s,st=""): return {"id":n,"prompt":p,"hints":h,"solution":s,"stretch":st}
def md(text):
    lines=text.strip().split("\n");out=[];ip=False;iu=False
    for l in lines:
        if l.startswith("```"):
            if ip:out.append("</code></pre>");ip=False
            else:
                if iu:out.append("</ul>");iu=False
                out.append(f'<pre class="code-block" data-lang="{html.escape(l[3:].strip() or "text")}"><code>');ip=True
            continue
        if ip:out.append(html.escape(l));continue
        if l.startswith("## "):
            if iu:out.append("</ul>");iu=False
            out.append(f"<h3>{html.escape(l[3:])}</h3>")
        elif l.startswith("### "):
            if iu:out.append("</ul>");iu=False
            out.append(f"<h4>{html.escape(l[4:])}</h4>")
        elif l.startswith("- "):
            if not iu:out.append("<ul>");iu=True
            s=html.escape(l[2:]);pts=s.split("`")
            for i in range(1,len(pts),2):pts[i]=f"<code>{pts[i]}</code>"
            out.append(f"<li>{''.join(pts)}</li>")
        elif l.strip()=="":
            if iu:out.append("</ul>");iu=False
        else:
            if iu:out.append("</ul>");iu=False
            s=html.escape(l);pts=s.split("`")
            for i in range(1,len(pts),2):pts[i]=f"<code>{pts[i]}</code>"
            out.append(f"<p>{''.join(pts)}</p>")
    if iu:out.append("</ul>")
    if ip:out.append("</code></pre>")
    return "\n".join(out)

MODULES=[
{"id":"00","title":"How to Use This Companion","level":"Setup",
"summary":"Parallel to FastBit MCU1: Driver Development. Each module maps to a Udemy peripheral — use Claude Code to write drivers faster.",
"body":md("""
## This course runs alongside Udemy MCU1
FastBit's MCU1 course teaches you to write bare-metal drivers for GPIO, SPI, I2C, USART by reading the STM32 datasheet and reference manual. This companion teaches you to use **Claude Code** at every step:
- **Ask Claude to explain** datasheet sections you don't understand
- **Delegate register map headers** to Claude (boilerplate generation)
- **Write driver APIs** with Claude as pair programmer
- **Debug hardware issues** by feeding logic analyzer output to Claude
- **Automate testing** with Claude-generated test harnesses

## Setup
1. Enrolled in Udemy MCU1 course
2. STM32F407 Discovery board (or STM32F446RE Nucleo)
3. STM32CubeIDE installed
4. Claude Code CLI installed
5. Logic analyzer (optional, for SPI/I2C debugging)

## CLAUDE.md for driver development
```markdown
# STM32 Driver Development Project
## Target: STM32F407VGT6 Discovery Board
## Build: STM32CubeIDE project or arm-none-eabi-gcc
## Language: C99, bare metal, NO HAL library
## Convention: All drivers follow handle-based API pattern
## Registers: Access via struct pointer casts to base addresses
## Rule: Every register write must have a comment citing Reference Manual section
```

## Model selection for driver development
- **Datasheet explanation**: use the strongest reasoning model (default)
- **Register map struct generation**: any model works (boilerplate)
- **Bug diagnosis from logic analyzer**: strongest model (complex reasoning)
- **Test harness generation**: default model
"""),
"exercises":[
    ex("00-1","Create your driver project structure: drivers/inc/, drivers/src/, app/. Write CLAUDE.md with STM32F407 target info, bare-metal constraint, and 'cite Reference Manual section numbers' rule.","Structure matches the Udemy course's project layout.","Project created. CLAUDE.md enforces bare-metal, cite RM sections. Claude will reference actual register descriptions."),
    ex("00-2","Ask Claude: 'Explain the difference between HAL, LL, and bare-metal driver development for STM32. Why does the Udemy MCU1 course teach bare-metal?' No file edits.","Understanding the course philosophy.","Claude explains abstraction levels. Bare-metal: full control, deep understanding, portable knowledge across MCUs."),
]},
{"id":"01","title":"MCU Architecture & Memory Map","level":"Beginner",
"summary":"Udemy: MCU internals, bus architecture, memory map. Claude explains what the datasheet shows.",
"body":md("""
## Udemy parallel: Understanding MCU Architecture
The Udemy course walks through block diagrams, bus architecture (AHB, APB), and the memory map. Claude Code makes these **interactive**.

## Claude as datasheet interpreter
```
> Explain the STM32F407 bus architecture: AHB1, AHB2, APB1, APB2.
  Which peripherals are on which bus? Why does the bus matter for
  programming (clock enables, access speed)?
```

## Claude for memory map generation
```
> Create a header inc/stm32f407_memmap.h with #defines for all
  peripheral base addresses on STM32F407: GPIO (A-E), SPI (1-3),
  I2C (1-3), USART (1-6), RCC, EXTI, SYSCFG.
  Group by bus (AHB1, APB1, APB2). Add comments.
```

## Automation: register map headers
This is where delegation saves HOURS. The Udemy course has you look up addresses manually. Claude generates them from documentation.
"""),
"exercises":[
    ex("01-1","Delegate: 'Create drivers/inc/stm32f407.h with base address macros for ALL peripherals on AHB1 (GPIO A-I, CRC, RCC, DMA), APB1 (SPI2/3, USART2-5, I2C1-3, timers), APB2 (SPI1, USART1/6, EXTI, SYSCFG, timers). Group by bus. Comment each.'","Massive boilerplate delegation — saves hours.","Complete memory map header generated in seconds. What takes the Udemy student an hour to type, Claude generates instantly."),
    ex("01-2","Ask Claude to draw an ASCII block diagram of the STM32F407 showing: CPU core, AHB bus matrix, AHB-APB bridges, and which peripherals hang off each bus.","Visual understanding of bus architecture.","ASCII diagram showing the bus hierarchy. You understand WHY GPIO is on AHB1 (fast) and USART on APB (slower)."),
    ex("01-3","Ask Claude: 'I want to access GPIOD registers. Walk me through: what bus is it on, what clock must I enable, what's the base address, how do I cast it to a struct pointer.' Step by step.","Complete peripheral access walkthrough.","Step-by-step: GPIOD on AHB1 → enable RCC->AHB1ENR bit 3 → base 0x40020C00 → cast to GPIO_TypeDef*. Same process for ANY peripheral."),
]},
{"id":"02","title":"GPIO Driver: Register Structs","level":"Beginner",
"summary":"Udemy: GPIO registers, MODER, OTYPER, OSPEEDR, PUPDR. Claude generates the register struct and configuration API.",
"body":md("""
## Udemy parallel: GPIO Peripheral Registers
The Udemy course teaches each GPIO register in detail. Claude Code helps you **generate the struct** and **understand each field**.

## Claude for GPIO struct
```
> Create a GPIO_RegDef_t struct mapping all GPIO registers for STM32F407:
  MODER, OTYPER, OSPEEDR, PUPDR, IDR, ODR, BSRR, LCKR, AFR[2].
  Each field: volatile uint32_t. Add offset comments matching RM0090.
```

## Claude for pin configuration API design
```
> Design a GPIO driver API (header only, no implementation yet):
  - GPIO_Init(GPIO_Handle_t *pGPIOHandle)
  - GPIO_ReadPin(GPIO_RegDef_t *pGPIOx, uint8_t pinNumber)
  - GPIO_WritePin(GPIO_RegDef_t *pGPIOx, uint8_t pinNumber, uint8_t value)
  - GPIO_TogglePin(GPIO_RegDef_t *pGPIOx, uint8_t pinNumber)
  - GPIO_ClockControl(GPIO_RegDef_t *pGPIOx, uint8_t en)
  Use the handle pattern from the Udemy course.
```

## Skill: incremental delegation
1. First: delegate the register struct (boilerplate)
2. Then: delegate the API header (design)
3. Then: implement functions one by one WITH Claude explaining each
4. Finally: write tests to verify
"""),
"exercises":[
    ex("02-1","Delegate: 'Create drivers/inc/stm32f407_gpio.h with GPIO_RegDef_t struct, GPIO_PinConfig_t (pin number, mode, speed, pull-up/down, output type, alt function), GPIO_Handle_t, and all function prototypes. Add enums/macros for modes.'","Complete GPIO header delegation.","Full GPIO driver header matching the Udemy course's design. Register struct, config struct, handle struct, prototypes, enums. Generated in seconds."),
    ex("02-2","Now implement GPIO_ClockControl() yourself in drivers/src/stm32f407_gpio.c. Then ask Claude to review it: 'Check my GPIO_ClockControl implementation for correctness. Does it handle GPIOA through GPIOI correctly?'","Write first, then AI review.","You wrote the function. Claude reviews: checks all port cases, verifies RCC register bits, suggests improvements. Learning by doing + AI review."),
    ex("02-3","Delegate the remaining GPIO functions: GPIO_Init, GPIO_ReadPin, GPIO_WritePin, GPIO_TogglePin. But add to the prompt: 'Add a comment citing the Reference Manual section for each register access.'","Delegation with documentation requirement.","Functions implemented with RM section citations. e.g., '// See RM0090 Section 8.4.1 for MODER register'. Documentation built into the code."),
]},
{"id":"03","title":"GPIO Interrupts & NVIC","level":"Intermediate",
"summary":"Udemy: EXTI, NVIC, IRQ handling, callbacks. Claude explains the interrupt path and generates IRQ handlers.",
"body":md("""
## Udemy parallel: GPIO Interrupts
The interrupt path (GPIO → EXTI → NVIC → ISR → callback) is complex. Claude Code makes it **traceable**.

## Claude for interrupt path explanation
```
> Trace the complete interrupt path for a button press on PA0:
  1. GPIO pin change
  2. EXTI line 0 trigger
  3. EXTI pending register
  4. NVIC ISER enable
  5. Priority/preemption
  6. EXTI0_IRQHandler vector
  7. Your ISR code
  8. Pending bit clear
  Draw ASCII diagram.
```

## Claude for ISR generation
```
> Implement EXTI0_IRQHandler that:
  1. Checks EXTI pending register
  2. Clears the pending bit
  3. Calls a user callback (weak function pattern)
  Follow the same pattern the Udemy course uses.
```

## Debugging interrupts with Claude
When interrupts don't fire, paste your config into Claude:
```
> My EXTI interrupt isn't firing. Here's my config:
  [paste register values]
  Check: Is the clock enabled? EXTI line mapped? NVIC enabled?
  Rising/falling edge correct? Priority set?
```
"""),
"exercises":[
    ex("03-1","Ask Claude to trace the FULL interrupt path from button press to ISR execution, with register names and bit positions at each step. Save as docs/interrupt-path.md for your reference.","Complete interrupt reference.","Step-by-step interrupt path documented. Register names, bit positions, sequence. Reusable reference for any EXTI interrupt."),
    ex("03-2","Delegate: 'Add GPIO interrupt functions to the GPIO driver: GPIO_IRQConfig (enable/disable in NVIC), GPIO_IRQPriority, GPIO_IRQHandler (clear pending bit). Add the EXTI line to SYSCFG configuration.'","Interrupt API implementation.","Three functions added. NVIC and EXTI registers accessed correctly. Pending bit cleared in handler. Matches Udemy course pattern."),
    ex("03-3","Write a task brief for a complete button-LED interrupt project: PA0 button triggers EXTI0, toggles PD12 LED. Delegate headless. Review the code specifically checking: is the pending bit cleared? Is the priority set?","Domain-specific code review.","Project implemented. You review with domain knowledge: pending bit ✓, priority ✓, clock enables ✓, EXTI mapping ✓. Combination of delegation + expert review."),
]},
{"id":"04","title":"SPI Driver from Scratch","level":"Intermediate",
"summary":"Udemy: SPI protocol, registers, master/slave, full driver. Claude generates the register map and helps debug with logic analyzer.",
"body":md("""
## Udemy parallel: SPI Peripheral Driver
SPI is the first communication protocol in the course. Claude helps with **register map generation**, **protocol understanding**, and **logic analyzer debugging**.

## Claude for SPI protocol explanation
```
> Explain SPI communication for a beginner: MOSI, MISO, SCK, NSS.
  Full-duplex, clock polarity (CPOL), clock phase (CPHA).
  Draw timing diagrams in ASCII for Mode 0 and Mode 3.
```

## Claude for SPI register struct
```
> Create SPI_RegDef_t for STM32F407 SPI peripheral. Include:
  CR1, CR2, SR, DR, CRCPR, RXCRCR, TXCRCR, I2SCFGR, I2SPR.
  Add bit position macros for CR1 (BIDIMODE, DFF, SSM, SSI, etc.)
```

## Claude for logic analyzer output
When SPI isn't working, capture logic analyzer output and feed to Claude:
```
> Here is my SPI logic analyzer capture:
  SCK: 1MHz, idle high (CPOL=1)
  MOSI: 0xAA sent, but slave received 0x55
  What's wrong?
```
Answer: likely CPHA mismatch — data sampled on wrong edge.
"""),
"exercises":[
    ex("04-1","Delegate the SPI register struct and handle struct, plus ALL function prototypes matching the Udemy course API: SPI_Init, SPI_SendData, SPI_ReceiveData, SPI_IRQHandler, etc. Full header file.","SPI driver header delegation.","Complete SPI driver header. Register struct, config struct, handle struct, function prototypes, bit position macros. Matches Udemy course."),
    ex("04-2","Ask Claude to draw ASCII timing diagrams for all 4 SPI modes (CPOL/CPHA combinations). Save to docs/spi-modes.md. This is your reference for debugging SPI issues.","SPI timing reference generation.","4 ASCII timing diagrams showing SCK polarity and phase for each mode. Reference for the entire SPI section of the Udemy course."),
    ex("04-3","Delegate the SPI_Init and SPI_SendData implementations. Build and test with a loopback (connect MOSI to MISO). Ask Claude to explain what to check if data doesn't match.","SPI implementation + debugging guide.","SPI init configures CR1/CR2. SendData writes DR and waits for TXE. Loopback test verifies. Claude's debugging guide covers: clock enable, pin AF config, baud rate, data size."),
]},
{"id":"05","title":"I2C Driver from Scratch","level":"Advanced",
"summary":"Udemy: I2C protocol, master/slave, addressing, ACK/NACK, driver implementation. Claude explains the state machine.",
"body":md("""
## Udemy parallel: I2C Peripheral Driver
I2C is more complex than SPI: start/stop conditions, addressing, ACK/NACK, clock stretching. Claude Code helps with **state machine understanding** and **register-level debugging**.

## Claude for I2C protocol deep-dive
```
> Explain I2C communication step-by-step for a master write to slave:
  1. Start condition (SDA goes low while SCL high)
  2. 7-bit address + R/W bit
  3. ACK from slave
  4. Data byte
  5. ACK from slave
  6. Stop condition
  Show the bit-level timing and SDA/SCL states at each point.
```

## Claude for I2C driver state machine
```
> The STM32 I2C peripheral has multiple states (SR1/SR2 flags).
  Draw a state machine for master transmitter mode showing:
  SB → ADDR → TXE → BTF → STOP transitions and which flags to check.
```

## Claude for I2C debugging
I2C issues are notoriously hard to debug. Feed register state to Claude:
```
> My I2C master can't communicate with a sensor at address 0x68.
  SR1 = 0x0001 (SB set but ADDR never gets set).
  What are the possible causes?
```
"""),
"exercises":[
    ex("05-1","Delegate the I2C driver header: I2C_RegDef_t, I2C_Config_t (speed, address, ack control, FM duty cycle), I2C_Handle_t, function prototypes including interrupt-driven send/receive.","I2C header delegation.","Complete I2C driver header. More complex than GPIO/SPI due to addressing modes, speed configs, and interrupt-driven API."),
    ex("05-2","Ask Claude to create an I2C debugging checklist in docs/i2c-debug.md: what to check when I2C doesn't work (pull-ups, clock enable, AF config, address match, timing, busy flag).","Debugging reference for the hardest protocol.","Comprehensive I2C debug checklist. You'll reference this many times during the Udemy I2C exercises."),
    ex("05-3","Implement I2C_MasterSendData: start → address → data loop → stop. Ask Claude to review and specifically check: 'Is the ADDR flag cleared correctly? Is the ACK bit handled? Is STOP generated after last byte?'","Implementation + protocol-specific review.","Function implemented. Claude verifies critical I2C sequences that are easy to get wrong: ADDR clear (read SR1+SR2), ACK control, STOP timing."),
]},
{"id":"06","title":"USART Driver from Scratch","level":"Advanced",
"summary":"Udemy: USART/UART protocol, baud rate, parity, stop bits, full driver. Claude calculates baud rates and generates test code.",
"body":md("""
## Udemy parallel: USART Peripheral Driver
USART is the most commonly used debug interface. Claude Code helps with **baud rate calculations**, **protocol configuration**, and **test harnesses**.

## Claude for baud rate calculation
```
> Calculate the USART_BRR value for 115200 baud with APB1 clock at 16 MHz.
  Show the formula: USARTDIV = fck / (16 * baud)
  Show mantissa and fraction register values.
  Then create a function that does this calculation automatically.
```

## Claude for USART driver
```
> Implement USART_Init that configures: baud rate, word length,
  stop bits, parity, hardware flow control, mode (TX/RX/both).
  Use the STM32F407 USART registers: CR1, CR2, CR3, BRR.
```

## Automation: printf retargeting
```
> Implement _write() syscall that redirects printf to USART2.
  This gives us debug output on the ST-Link virtual COM port.
  Include blocking and interrupt-driven versions.
```
"""),
"exercises":[
    ex("06-1","Ask Claude to calculate BRR values for common baud rates (9600, 115200, 921600) at 16MHz and 42MHz APB clocks. Create a reference table and a BRR calculation function.","Baud rate mastery.","Table of BRR values + calculation function. You understand the formula, Claude does the arithmetic. Saved to docs/baud-rates.md."),
    ex("06-2","Delegate the complete USART driver: header + source. Include USART_Init, USART_SendData, USART_ReceiveData, USART_SendString, interrupt-driven TX/RX with callbacks.","Full USART driver delegation.","Complete driver matching Udemy course pattern. Handle-based API, interrupt support, callback mechanism. Ready for testing."),
    ex("06-3","Delegate a printf retargeting implementation that sends to USART2 (ST-Link COM port). Add a test program that prints 'Hello from STM32'. This is your debug output for the rest of the course.","Debug infrastructure.","_write() implemented. printf goes to USART2. You can now debug with printf — essential infrastructure for all remaining exercises."),
]},
{"id":"07","title":"Clock Configuration & RCC","level":"Advanced",
"summary":"Udemy: HSI, HSE, PLL, AHB/APB prescalers. Claude calculates clock trees and generates config code.",
"body":md("""
## Udemy parallel: Clock Configuration
The STM32 clock tree is complex: HSI → PLL → SYSCLK → AHB → APB1/APB2 with prescalers at each stage. Claude makes it **calculable**.

## Claude for clock tree calculation
```
> Calculate the PLL configuration for 168 MHz SYSCLK from 8 MHz HSE:
  PLLM, PLLN, PLLP values. Verify: VCO input must be 1-2 MHz,
  VCO output must be 100-432 MHz. Show all intermediate frequencies.
```

## Claude for RCC configuration code
```
> Implement a function that configures STM32F407 for 168 MHz:
  HSE → PLL → 168 MHz SYSCLK, AHB=168 MHz, APB1=42 MHz, APB2=84 MHz.
  Include flash latency and voltage regulator settings.
  Add comments showing frequency at each stage.
```
"""),
"exercises":[
    ex("07-1","Ask Claude to draw the STM32F407 clock tree in ASCII: HSI/HSE → PLL → SYSCLK → AHB prescaler → APB1/APB2 prescalers. Label all dividers and multiplexers.","Clock tree visualization.","ASCII clock tree diagram. Shows all paths from oscillators to peripherals. Reference for the Udemy clock section."),
    ex("07-2","Delegate: 'Create a clock configuration function for 168 MHz from HSE. Include all steps: enable HSE, wait for ready, configure PLL (M=8,N=336,P=2), set flash latency, switch sysclk, set prescalers.' Build.","Clock config delegation.","Complete clock setup function. Each step commented with reasoning. Flash latency set correctly (5 wait states at 168 MHz). APB prescalers correct."),
    ex("07-3","Ask Claude to create a clock diagnostic function that reads RCC registers and prints current SYSCLK, HCLK, PCLK1, PCLK2 frequencies. Use this to verify your clock config.","Runtime clock verification.","Diagnostic function reads CFGR, calculates frequencies from prescaler bits, prints via USART. Verify 168/168/42/84 MHz."),
]},
{"id":"08","title":"Integration: Full Driver Library","level":"Expert",
"summary":"Udemy: Combining all drivers into a reusable library. Claude helps with library architecture and testing.",
"body":md("""
## Udemy parallel: Complete Driver Library
The Udemy course builds toward a complete driver library. Claude Code helps with **architecture**, **testing**, and **documentation**.

## Library architecture
```
drivers/
  inc/
    stm32f407.h          — base addresses, register structs
    stm32f407_gpio.h     — GPIO driver API
    stm32f407_spi.h      — SPI driver API
    stm32f407_i2c.h      — I2C driver API
    stm32f407_usart.h    — USART driver API
    stm32f407_rcc.h      — Clock configuration
  src/
    stm32f407_gpio.c
    stm32f407_spi.c
    stm32f407_i2c.c
    stm32f407_usart.c
    stm32f407_rcc.c
```

## Claude for cross-driver testing
```
> Create a test program that exercises all drivers:
  1. Init clock to 168 MHz
  2. Init USART2 for debug printf
  3. Init GPIO for LED + button
  4. Init SPI1 in loopback
  5. Send test data via SPI, verify
  6. Print results via USART
```

## Automation: documentation generation
```
> Generate docs/api-reference.md with function signatures, parameter
  descriptions, and usage examples for every function in the driver library.
```
"""),
"exercises":[
    ex("08-1","Write a task brief for a complete integration test that exercises GPIO, SPI, and USART together. Include acceptance criteria: LED toggles, SPI loopback matches, USART prints 'ALL TESTS PASS'. Delegate headless.","Integration test via delegation.","Integration test runs all drivers. Each peripheral verified. Final output confirms all pass. Complex multi-peripheral test delegated in one shot."),
    ex("08-2","Delegate: 'Generate complete API documentation in docs/api-reference.md for the entire driver library. For each function: signature, parameter table, return value, usage example, and relevant RM section.'","Documentation generation.","Comprehensive API docs generated. Every function documented. This would take days manually — Claude does it in minutes."),
    ex("08-3","Ask Claude to review the entire driver library for: missing error handling, inconsistent naming, missing volatile qualifiers, and potential race conditions in interrupt handlers. Generate a findings report.","Full library code review.","Review report with findings ranked by severity. Inconsistencies found and cataloged. Race conditions in IRQ handlers identified. Actionable fixes listed."),
]},
{"id":"09","title":"Capstone: Sensor Interface Project","level":"Expert",
"summary":"Udemy: Final project combining all drivers. Delegate the entire project to Claude, review like a tech lead.",
"body":md("""
## Capstone: Complete Sensor Interface
Use all your drivers to interface with a real sensor (or simulated):
- I2C to read temperature sensor (e.g., DS18B20, LM75, or BME280)
- SPI to read accelerometer (e.g., ADXL345 or LIS3DSH on Discovery board)
- USART for debug output
- GPIO for LED status indication

## Full delegation workflow
1. Task brief in `tasks/sensor-project.md`
2. Verification checklist
3. Delegate headless
4. Review the complete diff
5. Test on hardware

## What you've learned
By the end of this companion course, you can:
- Read STM32 datasheets and translate them into driver code (with Claude accelerating boilerplate)
- Design handle-based driver APIs (the pattern the Udemy course teaches)
- Debug hardware protocols using Claude as a diagnostic assistant
- Delegate entire driver implementations and review them with domain expertise
- Automate testing and documentation generation
"""),
"exercises":[
    ex("09-1","Write a complete task brief for the sensor interface project: which sensors, which communication protocol for each, which pins, what the output should look like on USART. Include register addresses if known.","Capstone spec — your domain knowledge.","Complete spec with sensor selection, pin mapping, protocol config, expected output format. Your domain knowledge + Claude's implementation speed."),
    ex("09-2","Delegate the capstone headless. Go do something else. Come back and review the complete implementation: are I2C addresses correct? SPI mode correct? Register reads correct?","Full delegation + domain review.","Capstone implemented. You review with hardware knowledge from the Udemy course. The combination produces working firmware faster than either approach alone."),
    ex("09-3","Flash to hardware and test. If something doesn't work, paste the USART debug output or logic analyzer capture into Claude for diagnosis. Fix and re-test.","Real hardware debugging with AI assistance.","Hardware test. Any issues diagnosed via Claude + your hardware understanding. Working sensor interface project completed."),
]},
{"id":"drills","title":"Daily Drills","level":"All levels",
"summary":"Quick exercises pairing Udemy MCU1 topics with Claude Code skills.",
"body":md("""
## One drill per day alongside the Udemy MCU1 course.
"""),
"exercises":[
    ex("D-01","Ask Claude to explain one register from today's Udemy lecture in a different way than the instructor.","Alternative explanation.","Fresh perspective on the same register. Sometimes Claude's explanation clicks better."),
    ex("D-02","Delegate a register struct for the peripheral you're currently studying. Compare to what you'd write manually.","Boilerplate delegation.","Register struct generated. Compare quality and accuracy to manual work."),
    ex("D-03","Ask Claude to generate 3 quiz questions about today's peripheral. Answer them. Have Claude grade.","AI-generated quiz.","Quiz taken, graded, explanations provided. Active recall practice."),
    ex("D-04","Feed a 'broken' register configuration to Claude and ask it to find the bug. See if it catches it.","Debugging practice.","Claude identifies misconfigured bits. You learn to spot common register config errors."),
    ex("D-05","Add one new rule to CLAUDE.md based on a lesson learned today.","Handbook growth.","CLAUDE.md improves incrementally. Your AI worker gets better at driver development."),
    ex("D-06","Delegate a test function for the driver API you implemented today. Run it.","Testing discipline.","Test written and run. Every driver function has a test. Quality built in."),
]},
]

ACCENT="#7c3aed";ACCENT2="#a78bfa";STORAGE="mcu1-drivers-claude-v1"
TITLE="MCU1 Driver Development with Claude Code"
SUBTITLE="Parallel to FastBit MCU1 · GPIO · SPI · I2C · USART · Bare Metal · AI-Accelerated"

HTML_TEMPLATE=r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>"""+TITLE+r"""</title><style>:root{--bg:#0f1419;--surface:#1a2332;--surface2:#243044;--text:#e7ecf3;--muted:#9aa8bc;--accent:"""+ACCENT+r""";--accent2:"""+ACCENT2+r""";--warn:#fbbf24;--ok:#4ade80;--border:#2d3a4f;--ex:#1e2a3d;font-family:"Segoe UI",system-ui,sans-serif}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);line-height:1.55}a{color:var(--accent2)}.layout{display:grid;grid-template-columns:300px 1fr;min-height:100vh}nav.sidebar{background:var(--surface);border-right:1px solid var(--border);padding:1rem;overflow-y:auto;position:sticky;top:0;height:100vh}nav.sidebar h1{font-size:1.05rem;margin:0 0 .25rem;line-height:1.3}nav.sidebar .sub{font-size:.78rem;color:var(--muted);margin-bottom:1rem}nav.sidebar input{width:100%;padding:.45rem .6rem;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);margin-bottom:.75rem}nav.sidebar ul{list-style:none;padding:0;margin:0}nav.sidebar li{margin-bottom:.15rem}nav.sidebar button.module-link{width:100%;text-align:left;background:0 0;border:none;color:var(--text);padding:.35rem .5rem;border-radius:6px;cursor:pointer;font-size:.82rem}nav.sidebar button.module-link:hover{background:var(--surface2)}nav.sidebar button.module-link.active{background:var(--accent);color:#fff;font-weight:600}nav.sidebar .level{font-size:.65rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin-top:.75rem;margin-bottom:.25rem}.progress-wrap{margin:1rem 0;font-size:.75rem;color:var(--muted)}.progress-bar{height:6px;background:var(--bg);border-radius:99px;overflow:hidden;margin-top:.35rem}.progress-bar>div{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0;transition:width .3s ease}main{padding:1.5rem 2rem 4rem;max-width:920px}.hero{margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}.hero h2{margin:0 0 .5rem;font-size:1.75rem}.hero p{color:var(--muted);margin:0}.badge{display:inline-block;font-size:.7rem;padding:.15rem .45rem;border-radius:4px;background:var(--surface2);color:var(--accent2);margin-right:.35rem}.lesson h3{margin-top:1.5rem;color:var(--accent2)}.lesson h4{margin-top:1rem}.lesson pre.code-block{background:#0a0e14;border:1px solid var(--border);border-radius:8px;padding:.85rem 1rem;overflow-x:auto;font-size:.82rem}.lesson code{background:var(--surface2);padding:.1rem .35rem;border-radius:4px;font-size:.88em}.exercise{background:var(--ex);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;padding:1rem 1.1rem;margin:1.25rem 0}.exercise header{display:flex;justify-content:space-between;align-items:flex-start;gap:.75rem;flex-wrap:wrap}.exercise h5{margin:0;font-size:.95rem}.exercise .ex-id{font-size:.72rem;color:var(--muted);font-family:ui-monospace,monospace}.exercise .prompt{margin:.75rem 0}.exercise .hint{font-size:.85rem;color:var(--muted);border-top:1px dashed var(--border);padding-top:.65rem;margin-top:.65rem}.exercise .actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.75rem}button.btn{border:none;border-radius:6px;padding:.45rem .85rem;cursor:pointer;font-size:.82rem;font-weight:600}button.btn-primary{background:var(--accent);color:#fff}button.btn-ghost{background:var(--surface2);color:var(--text)}button.btn-ok{background:#166534;color:#ecfdf5}.exercise.done{border-left-color:var(--ok);opacity:.92}.solution{display:none;margin-top:.85rem;padding:.85rem;background:#0a0e14;border-radius:6px;border:1px solid var(--border);white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace;font-size:.8rem}.solution.visible{display:block}.stretch{margin-top:.5rem;font-size:.82rem;color:var(--warn)}@media(max-width:900px){.layout{grid-template-columns:1fr}nav.sidebar{position:relative;height:auto}}</style></head><body><div class="layout"><nav class="sidebar"><h1 id="course-title">Loading…</h1><p class="sub" id="course-sub"></p><div class="progress-wrap"><span id="progress-label">0/0</span><div class="progress-bar"><div id="progress-fill"></div></div></div><input type="search" id="search" placeholder="Filter…"/><p class="level">Modules</p><ul id="module-list"></ul></nav><main><section class="hero"><h2 id="module-title">Welcome</h2><div id="module-meta"></div><p id="module-summary" style="margin-top:.75rem;color:var(--muted)"></p><p style="font-size:.85rem;color:var(--muted);margin-top:1rem"><strong>%%TOTAL%% exercises</strong> · companion to Udemy MCU1 Driver Development</p></section><section class="lesson" id="lesson-body"></section><section><h3 style="color:var(--accent2)">Exercises</h3><p id="exercise-count" style="color:var(--muted);font-size:.9rem"></p><div id="exercises"></div></section></main></div><script>window.COURSE_DATA=%%DATA%%;</script><script>const SK='"""+STORAGE+r"""';function lp(){try{return JSON.parse(localStorage.getItem(SK)||'{}')}catch{return{}}}function sp(p){localStorage.setItem(SK,JSON.stringify(p))}function ce(ms){return ms.reduce((n,m)=>n+(m.exercises?.length||0),0)}function rl(ms,ai,f){const ul=document.getElementById('module-list');ul.innerHTML='';const q=(f||'').toLowerCase();ms.forEach(m=>{const h=(m.title+' '+m.summary+' '+m.level).toLowerCase();if(q&&!h.includes(q))return;const li=document.createElement('li');const b=document.createElement('button');b.className='module-link'+(m.id===ai?' active':'');b.textContent=m.id==='drills'?'⚡ '+m.title:m.id+' · '+m.title;b.onclick=()=>sm(m.id);li.appendChild(b);ul.appendChild(li)})}function sm(id){const m=C.modules.find(x=>x.id===id)||C.modules[0];history.replaceState(null,'','#'+m.id);document.getElementById('module-title').textContent=m.title;document.getElementById('module-meta').innerHTML=`<span class="badge">${m.level}</span><span class="badge">Module ${m.id}</span>`;document.getElementById('module-summary').textContent=m.summary;document.getElementById('lesson-body').innerHTML=m.body;const er=document.getElementById('exercises');er.innerHTML='';const p=lp();(m.exercises||[]).forEach(e=>{const d=p[e.id];const el=document.createElement('article');el.className='exercise'+(d?' done':'');el.innerHTML=`<header><h5>Exercise</h5><span class="ex-id">${e.id}</span></header><p class="prompt">${eh(e.prompt)}</p>${e.hints?`<div class="hint"><strong>Hint:</strong> ${eh(e.hints)}</div>`:''}${e.stretch?`<div class="stretch"><strong>Stretch:</strong> ${eh(e.stretch)}</div>`:''}<div class="actions"><button type="button" class="btn btn-primary btn-solution">Reveal solution</button><button type="button" class="btn btn-ghost btn-hide">Hide solution</button><button type="button" class="btn btn-ok btn-done">${d?'✓ Completed':'Mark complete'}</button></div><div class="solution">${eh(e.solution)}</div>`;el.querySelector('.btn-solution').onclick=()=>{el.querySelector('.solution').classList.add('visible')};el.querySelector('.btn-hide').onclick=()=>{el.querySelector('.solution').classList.remove('visible')};el.querySelector('.btn-done').onclick=ev=>{p[e.id]=true;sp(p);el.classList.add('done');ev.target.textContent='✓ Completed';ub()};er.appendChild(el)});rl(C.modules,m.id,document.getElementById('search').value);document.getElementById('exercise-count').textContent=(m.exercises||[]).length+' exercises';ub()}function eh(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}function ub(){const t=ce(C.modules);const p=lp();const d=Object.keys(p).filter(k=>p[k]).length;const pc=t?Math.round(d/t*100):0;document.getElementById('progress-label').textContent=`${d}/${t} (${pc}%)`;document.getElementById('progress-fill').style.width=pc+'%'}function init(){const d=window.COURSE_DATA;window.C=d;document.getElementById('course-title').textContent=d.title;document.getElementById('course-sub').textContent=d.subtitle;document.getElementById('search').oninput=e=>{const id=(location.hash||'#00').slice(1);rl(C.modules,id,e.target.value)};const si=(location.hash||'#00').replace('#','');sm(C.modules.some(m=>m.id===si)?si:'00');window.onhashchange=()=>{const id=(location.hash||'#00').slice(1);if(C.modules.some(m=>m.id===id))sm(id)}}document.addEventListener('DOMContentLoaded',init);</script></body></html>"""

def main():
    course={"title":TITLE,"subtitle":SUBTITLE,"version":"2026.09","modules":MODULES}
    total=sum(len(m.get("exercises",[]))for m in MODULES)
    page=HTML_TEMPLATE.replace("%%DATA%%",json.dumps(course,ensure_ascii=False)).replace("%%TOTAL%%",str(total))
    OUT.write_text(page,encoding="utf-8");print(f"Wrote {OUT} ({total} exercises, {len(MODULES)} modules)")

if __name__=="__main__":main()
