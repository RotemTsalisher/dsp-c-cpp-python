#!/usr/bin/env python3
"""Generate index.html — MCU2 Peripherals with Claude Code companion course.
Parallel to FastBit MCU2: Timers, PWM, CAN, Low Power, RTC with HAL."""
from __future__ import annotations

import html as H
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"


def ex(n, p, h, s):
    return {"id": n, "prompt": p, "hints": h, "solution": s, "stretch": ""}


def md(text):
    lines = text.strip().split("\n")
    out = []
    ip = False
    iu = False
    for l in lines:
        if l.startswith("```"):
            if ip:
                out.append("</code></pre>")
                ip = False
            else:
                if iu:
                    out.append("</ul>")
                    iu = False
                out.append('<pre class="code-block"><code>')
                ip = True
            continue
        if ip:
            out.append(H.escape(l))
            continue
        if l.startswith("## "):
            if iu:
                out.append("</ul>")
                iu = False
            out.append(f"<h3>{H.escape(l[3:])}</h3>")
        elif l.startswith("- "):
            if not iu:
                out.append("<ul>")
                iu = True
            out.append(f"<li>{H.escape(l[2:])}</li>")
        elif l.strip() == "":
            if iu:
                out.append("</ul>")
                iu = False
        else:
            if iu:
                out.append("</ul>")
                iu = False
            out.append(f"<p>{H.escape(l)}</p>")
    if iu:
        out.append("</ul>")
    if ip:
        out.append("</code></pre>")
    return "\n".join(out)


MODULES = [
    {
        "id": "00",
        "title": "How to Use This Companion",
        "level": "Setup",
        "summary": "Parallel to FastBit MCU2. Each module maps to a Udemy peripheral — use Claude Code with HAL driver development.",
        "body": md("""
## This course runs alongside Udemy MCU2
FastBit MCU2 teaches Timers, PWM, CAN, Low Power, and RTC using STM32 HAL APIs. This companion teaches Claude Code usage at every step: understand HAL internals, generate configs, debug protocols, automate testing.

## Setup
- Enrolled in Udemy MCU2
- STM32F446RE Nucleo board
- STM32CubeIDE + Claude Code CLI
- CAN transceivers (for CAN exercises)

## CLAUDE.md additions for MCU2
- Target: STM32F446RE Nucleo
- Framework: STM32 HAL (NOT bare metal)
- Build: STM32CubeIDE project
- Rule: explain HAL function internals when using them
- Rule: show timer/baud calculations with formula

## Model selection
- Timer/baud calculations: any model (math)
- CAN protocol explanation: strongest model (complex reasoning)
- HAL config generation: default model
"""),
        "exercises": [
            ex("00-1", "Create CLAUDE.md for MCU2: STM32F446RE, HAL framework, explain internals rule, show calculation formulas rule.",
               "HAL-based project.", "CLAUDE.md with HAL rules. Claude explains what HAL functions do under the hood."),
            ex("00-2", "Ask Claude: Explain STM32 HAL architecture — handle structs, init, callbacks, MSP. How does it differ from bare-metal MCU1?",
               "HAL understanding.", "Claude explains layers, __weak callbacks, HAL_Init, MSP (MCU Support Package), tick timer. Contrasts with MCU1 bare-metal."),
        ],
    },
    {
        "id": "01",
        "title": "Clocks & PLL Configuration",
        "level": "Beginner",
        "summary": "Udemy: HSI, HSE, PLL, prescalers. Claude calculates clock trees and generates SystemClock_Config.",
        "body": md("""
## Udemy parallel: Clock and PLL Programming
Claude calculates PLL parameters and generates SystemClock_Config with comments at every stage.

## Key formula
SYSCLK = (HSE / PLLM) * PLLN / PLLP
APB1 max 45 MHz, APB2 max 90 MHz on F446RE.
"""),
        "exercises": [
            ex("01-1", "Ask Claude to calculate PLL for 180 MHz from 8 MHz HSE on F446RE. Show all intermediate frequencies and verify VCO constraints (100-432 MHz).",
               "Clock math.", "M=8, N=360, P=2. VCO_in=1MHz, VCO_out=360MHz, SYSCLK=180MHz. APB1=45MHz (div4), APB2=90MHz (div2)."),
            ex("01-2", "Delegate: SystemClock_Config function with step-by-step comments showing frequency at each stage. Include flash latency.",
               "Clock config delegation.", "Function with comments: HSE to PLL to SYSCLK to AHB to APB1/APB2. Flash 5 wait states at 180 MHz."),
        ],
    },
    {
        "id": "02",
        "title": "Basic Timers: Polling & Interrupts",
        "level": "Beginner",
        "summary": "Udemy: TIM6/TIM7, timebase, interrupts. Claude does prescaler/ARR math.",
        "body": md("""
## Udemy parallel: Basic Timer Programming
Timer frequency = TIM_CLK / ((PSC+1) * (ARR+1))

Claude solves for PSC and ARR given desired frequency and timer clock. Shows multiple valid solutions with trade-off analysis.
"""),
        "exercises": [
            ex("02-1", "Ask Claude to solve PSC/ARR for 1 Hz, 100 Hz, 1 kHz, 10 kHz from 90 MHz. Show multiple solutions with resolution trade-offs.",
               "Timer math.", "Table with PSC/ARR combos. Higher PSC = lower counter resolution. Multiple valid solutions per frequency."),
            ex("02-2", "Delegate: Timer interrupt program toggling LED at 500ms. Include HAL_TIM_PeriodElapsedCallback.",
               "Timer interrupt.", "PSC/ARR for 2 Hz. HAL_TIM_Base_Start_IT. Callback toggles LED. Complete and correct."),
            ex("02-3", "Delegate: Reusable timer calculator function — input frequency and clock, output optimal PSC/ARR.",
               "Utility function.", "Calculator minimizes error. Reusable throughout the course."),
        ],
    },
    {
        "id": "03",
        "title": "Input Capture & Output Compare",
        "level": "Intermediate",
        "summary": "Udemy: GP timer input capture (frequency measurement) and output compare (PWM). Claude explains capture mechanism and generates configs.",
        "body": md("""
## Udemy parallel: Input Capture + Output Compare
Input capture: measure external signal frequency via edge timestamps.
Output compare: generate precise waveforms and PWM.

Claude draws timing diagrams and calculates capture values.
"""),
        "exercises": [
            ex("03-1", "Ask Claude to explain input capture with ASCII timing diagram: edge then CCR latch then interrupt then delta then frequency.",
               "Input capture mechanism.", "Timing diagram with two edges, CCR values, period calculation. Overflow handling explained."),
            ex("03-2", "Delegate: Frequency meter on TIM2 CH1 (PA0). Print measured frequency via USART. Handle overflow.",
               "Frequency measurement.", "Complete freq meter with HAL input capture callbacks. Overflow detection. Prints Hz."),
            ex("03-3", "Delegate: 20 kHz PWM on TIM4 CH1 with function to set duty 0-100%. Test with breathing LED.",
               "PWM generation.", "PSC/ARR for 20 kHz. CCR setter function. Breathing LED ramp. HAL PWM start correct."),
        ],
    },
    {
        "id": "04",
        "title": "CAN Protocol Fundamentals",
        "level": "Advanced",
        "summary": "Udemy: CAN theory, frames, arbitration, signaling, transceivers. Claude draws frame diagrams and explains arbitration.",
        "body": md("""
## Udemy parallel: CAN Bus Fundamentals
CAN is the most complex protocol in MCU2. Claude provides:
- Frame structure diagrams (standard + extended)
- Bit-by-bit arbitration traces
- Bit timing calculations with sample point verification
- Error handling explanation
"""),
        "exercises": [
            ex("04-1", "Ask Claude to draw CAN standard frame and extended frame in ASCII. Label every field with bit count.",
               "CAN frame visualization.", "Two diagrams: SOF, ID[10:0], RTR, IDE, DLC, Data[0-8], CRC, ACK, EOF. Extended adds SRR, IDE, ID[28:18]."),
            ex("04-2", "Ask Claude: Node A (ID 0x100) and Node B (ID 0x200) transmit simultaneously. Trace arbitration bit-by-bit.",
               "Arbitration understanding.", "Bit-by-bit trace. ID bits compared. 0x100 < 0x200 so A wins at bit 9. B detects recessive-when-driving-dominant, backs off."),
            ex("04-3", "Ask Claude to calculate CAN bit timing for 500 kbps from 45 MHz APB1. SJW, BS1, BS2, prescaler. Verify 75-87.5% sample point.",
               "Bit timing math.", "Prescaler=5, BS1=6, BS2=2. Time quantum = 111ns. Bit time = 9 TQ = 1us = 1 Mbps. For 500k: prescaler=10. Sample at 77.8%."),
        ],
    },
    {
        "id": "05",
        "title": "bxCAN Programming & Filtering",
        "level": "Advanced",
        "summary": "Udemy: STM32 bxCAN, filter banks, loopback, normal mode, two-board exercises. Claude generates filter configs and loopback tests.",
        "body": md("""
## Udemy parallel: bxCAN Peripheral
The bxCAN filter bank system is the most confusing part. Claude explains mask mode vs list mode, generates filter configurations, and creates loopback tests.
"""),
        "exercises": [
            ex("05-1", "Delegate: CAN loopback test -- init at 500 kbps, send frame with 8 bytes, receive in loopback, verify match. Print via USART.",
               "CAN loopback.", "Init, accept-all filter, TX, RX, compare. Loopback passes. Foundation for normal-mode testing."),
            ex("05-2", "Delegate: CAN filter config -- mask mode for IDs 0x100-0x1FF, list mode for 0x200 and 0x300 specifically. Explain each filter bank.",
               "CAN filtering.", "Two filter banks configured. Mask mode: ID=0x100, mask=0x700 (match 0x1xx). List mode: exact match 0x200, 0x300. Comments explain."),
            ex("05-3", "Ask Claude to create a CAN debugging checklist: what to check when CAN does not work (clock, pins, transceiver, bit timing, filter, mode).",
               "CAN debug reference.", "Checklist: RCC enable, GPIO AF, transceiver wiring, bit timing match, filter not blocking, normal mode entered. Save to docs/."),
        ],
    },
    {
        "id": "06",
        "title": "Low Power Modes",
        "level": "Advanced",
        "summary": "Udemy: Sleep, Stop, Standby, WFI/WFE, wake-up sources. Claude explains power states and generates safe transitions.",
        "body": md("""
## Udemy parallel: Low Power Modes
Sleep/Stop/Standby trade off between power and wake-up capability. Claude creates comparison tables and generates safe mode entry/exit code.
"""),
        "exercises": [
            ex("06-1", "Ask Claude: Create power mode comparison table -- Mode, CPU, SRAM, Peripherals, Clocks, Wake sources, Current, Recovery time.",
               "Power mode reference.", "Table: Sleep (any IRQ wakes, ~mA), Stop (EXTI wakes, ~uA, SRAM retained), Standby (RTC/WKUP wakes, ~nA, SRAM lost)."),
            ex("06-2", "Delegate: Enter Sleep on button, wake on EXTI. Print sleep duration. Then enter Stop mode, wake on EXTI, reconfigure clocks.",
               "Low power implementation.", "Two modes demonstrated. Clock reconfiguration after Stop mode (critical -- PLL needs restart)."),
        ],
    },
    {
        "id": "07",
        "title": "RTC: Real-Time Clock",
        "level": "Advanced",
        "summary": "Udemy: RTC calendar, alarms, timestamps, wake-up timer. Claude handles BCD conversion and alarm config.",
        "body": md("""
## Udemy parallel: RTC
RTC uses BCD format and has complex alarm configuration. Claude generates conversion utilities and alarm setup code.
"""),
        "exercises": [
            ex("07-1", "Delegate: BCD conversion functions (decimal_to_bcd, bcd_to_decimal) + RTC init setting current date/time + print via USART every second.",
               "RTC setup.", "Conversion utils + RTC init + periodic time print. BCD explained in comments."),
            ex("07-2", "Delegate: RTC Alarm A at 08:00:00 daily. Callback toggles LED. Also: RTC wake-up from Standby mode.",
               "RTC alarm + wake-up.", "Alarm configured, callback works, Standby wake-up via RTC demonstrated. Full RTC feature set."),
        ],
    },
    {
        "id": "08",
        "title": "Capstone: Smart Sensor Node",
        "level": "Expert",
        "summary": "Combine all MCU2 peripherals: timer-triggered sampling, PWM status, CAN output, low-power sleep, RTC timestamp.",
        "body": md("""
## Capstone: Smart Sensor Node
Timer triggers ADC sample every second. Data sent via CAN with RTC timestamp. Between samples, MCU sleeps. LED brightness via PWM indicates signal level.

Tests: timers, PWM, CAN, low power, RTC -- everything from MCU2.
"""),
        "exercises": [
            ex("08-1", "Write complete task brief: all peripherals, timing, CAN frame format (ID, DLC, data layout with timestamp), power budget.",
               "Capstone spec.", "Brief covers every peripheral, frame format, sleep strategy. Your domain knowledge from the Udemy course."),
            ex("08-2", "Delegate headless. Review: timer period, CAN frame format, sleep entry/exit, clock reconfiguration after Stop, RTC read.",
               "Full delegation + domain review.", "All peripherals working together. Domain-specific review catches integration issues."),
        ],
    },
    {
        "id": "drills",
        "title": "Daily Drills",
        "level": "All",
        "summary": "Quick MCU2 exercises with Claude Code.",
        "body": md("## One drill per day alongside the Udemy MCU2 course."),
        "exercises": [
            ex("D-01", "Ask Claude to calculate timer values for a random frequency. Verify.", "Timer math drill.", "Quick calc, verified."),
            ex("D-02", "Ask Claude to explain one HAL function in terms of register writes.", "HAL internals.", "HAL decoded to registers."),
            ex("D-03", "Ask Claude to generate a CAN frame exercise. Decode manually, verify.", "CAN practice.", "Frame decoded, verified."),
            ex("D-04", "Add one peripheral rule to CLAUDE.md from today's lesson.", "Handbook growth.", "CLAUDE.md grows daily."),
        ],
    },
]

ACCENT = "#0891b2"
ACCENT2 = "#22d3ee"
STORAGE_KEY = "mcu2-peripherals-claude-v1"
TITLE = "MCU2 Peripherals with Claude Code"
SUBTITLE = "Parallel to FastBit MCU2 · Timers · PWM · CAN · Low Power · RTC · HAL"


def main():
    # Read MCU1 index.html as template, swap in our data
    mcu1_html = (ROOT.parent / "mcu1-drivers-with-claude" / "index.html").read_text(encoding="utf-8")

    course = {"title": TITLE, "subtitle": SUBTITLE, "version": "2026.09", "modules": MODULES}
    total = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(course, ensure_ascii=False)

    # Replace course data
    html_out = re.sub(
        r"(window\.COURSE_DATA\s*=\s*)\{.*?\}(;\s*</script>)",
        lambda m: m.group(1) + data_json + m.group(2),
        mcu1_html,
        count=1,
        flags=re.DOTALL,
    )

    # Replace storage key, colors, title
    html_out = html_out.replace("mcu1-drivers-claude-v1", STORAGE_KEY)
    html_out = html_out.replace("#7c3aed", ACCENT)
    html_out = html_out.replace("#a78bfa", ACCENT2)
    html_out = re.sub(r"<title>.*?</title>", f"<title>{H.escape(TITLE)}</title>", html_out)

    OUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT} — {len(MODULES)} modules, {total} exercises")


if __name__ == "__main__":
    main()
