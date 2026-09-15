#!/usr/bin/env python3
"""Generate index.html — RTOS with Claude Code companion course.
Parallel to FastBit RTOS: FreeRTOS on STM32Fx with debugging."""
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
        "summary": "Parallel to FastBit RTOS course. Use Claude Code to understand scheduling, generate task code, debug priorities.",
        "body": md("""
## This course runs alongside Udemy Mastering RTOS
FreeRTOS on STM32F4. Claude explains scheduling, generates task patterns, debugs priority issues, automates RTOS testing.

## Setup
- Enrolled in Udemy RTOS course
- STM32F4 board + STM32CubeIDE with FreeRTOS middleware
- Claude Code CLI
- SEGGER SystemView (optional)

## CLAUDE.md for RTOS
- Framework: FreeRTOS
- Rule: verify stack sizes before creating tasks
- Rule: warn about priority inversion risks
- Rule: use configASSERT for development builds
- Rule: explain task state transitions in code comments

## Model selection for RTOS
- Scheduling explanations: strongest model (abstract reasoning)
- Task boilerplate: any model (repetitive pattern)
- Priority inversion analysis: strongest model (subtle bugs)
- SystemView trace analysis: strongest model (complex data)
"""),
        "exercises": [
            ex("00-1", "Create CLAUDE.md with FreeRTOS rules: verify stack sizes, warn about priority inversion, use configASSERT, explain state transitions.",
               "RTOS worker rules.", "CLAUDE.md with RTOS-specific rules. Claude warns about common pitfalls automatically."),
            ex("00-2", "Ask Claude: RTOS vs bare-metal super-loop -- when is each appropriate? Give 3 examples for each.",
               "RTOS mindset.", "RTOS: concurrent I/O, mixed timing, complex state. Bare-metal: simple, resource-constrained, hard real-time single-path."),
        ],
    },
    {
        "id": "01",
        "title": "RTOS Concepts & Task States",
        "level": "Beginner",
        "summary": "Udemy: Scheduling, task states, context switching. Claude visualizes the scheduler and state machine.",
        "body": md("""
## Udemy parallel: RTOS Fundamentals
Task states (Ready, Running, Blocked, Suspended) and preemptive scheduling are abstract. Claude makes them concrete with timelines and state diagrams.

## Claude for scheduler visualization
Ask Claude to draw a timeline showing 3 tasks with different priorities, showing preemption, blocking, and ready-queue behavior.
"""),
        "exercises": [
            ex("01-1", "Ask Claude to draw an ASCII timeline: 3 tasks (H/M/L priority), show preemption when H becomes ready while L runs.",
               "Scheduler visualization.", "Timeline showing tick-by-tick execution. Preemption visible: L running, H ready, L preempted, H runs."),
            ex("01-2", "Ask Claude for FreeRTOS task state diagram with ALL transitions labeled with API calls/events.",
               "State machine reference.", "Ready to Running (scheduler), Running to Blocked (vTaskDelay, xQueueReceive), Blocked to Ready (timeout, event)."),
            ex("01-3", "Delegate: 3-task demo showing preemption. Each prints name+timestamp. Priorities make preemption visible in output.",
               "Live scheduling demo.", "Output shows: LowTask runs, HighTask preempts, LowTask resumes. Visible in USART timestamps."),
        ],
    },
    {
        "id": "02",
        "title": "Task Creation & Stack Sizing",
        "level": "Beginner",
        "summary": "Udemy: xTaskCreate, vTaskDelay, priorities, stack. Claude estimates stack requirements and generates task boilerplate.",
        "body": md("""
## Udemy parallel: Task Creation
Correct stack size is critical -- too small = crash, too large = wasted RAM. Claude calculates based on task complexity.

## Stack estimation
Base context save: ~64 bytes (Cortex-M4)
Per function call frame: ~32 bytes
Per local variable: sizeof(type)
Library calls (printf): ~1024 bytes
Safety margin: 1.5x-2x
"""),
        "exercises": [
            ex("02-1", "Ask Claude to estimate stacks: a) LED blink (simple), b) USART logger (printf), c) DSP filter (large buffers).",
               "Stack math.", "LED: 128 words. Logger: 512 words (printf!). DSP: 256+ words (buffer-dependent). Formulas shown."),
            ex("02-2", "Delegate: 4-task project -- LED1 blink 500ms, LED2 blink 1s, button reader, USART logger. Correct priorities, stack sizes.",
               "Multi-task project.", "4 tasks with priorities: logger(3) > button(2) > LEDs(1). Stack sizes matched to task complexity."),
            ex("02-3", "Delegate: Stack overflow detection demo -- deliberately small stack + vApplicationStackOverflowHook. Show diagnosis.",
               "Overflow debugging.", "Hook catches overflow, prints task name. Essential RTOS debugging skill."),
        ],
    },
    {
        "id": "03",
        "title": "Queues: Inter-Task Communication",
        "level": "Intermediate",
        "summary": "Udemy: xQueueCreate, Send, Receive. Claude designs queue architectures and generates producer-consumer pipelines.",
        "body": md("""
## Udemy parallel: FreeRTOS Queues
Queues are THE primary IPC in FreeRTOS. Claude designs multi-stage pipelines with correct queue sizing.

## Queue sizing
Size = max burst rate x max consumer latency. If producer makes 10 items/sec and consumer takes 50ms per item, queue needs >= 1 item. But add margin for jitter.
"""),
        "exercises": [
            ex("03-1", "Ask Claude to design queue architecture: ADC(fast) to filter(medium) to logger(slow). Draw data flow, size each queue.",
               "Queue architecture.", "Flow diagram: ADC to raw_q(10) to filter to processed_q(5) to logger. Sizes based on rate analysis."),
            ex("03-2", "Delegate: 3-stage pipeline implementation. Producer generates sine wave samples, filter computes RMS, logger prints.",
               "Pipeline implementation.", "Three tasks, two queues. RMS calculated correctly. Pipeline runs continuously."),
            ex("03-3", "Ask Claude: Queue full -- block forever vs timeout vs return immediately. When to use each in embedded?",
               "Queue overflow strategies.", "Block forever: safety-critical data. Timeout: producer has other work. Immediate: ISR context (xQueueSendFromISR)."),
        ],
    },
    {
        "id": "04",
        "title": "Semaphores & Mutexes",
        "level": "Intermediate",
        "summary": "Udemy: Binary/counting semaphores, mutexes, priority inversion, inheritance. Claude explains pitfalls and generates safe patterns.",
        "body": md("""
## Udemy parallel: Synchronization
Where RTOS bugs hide. Claude explains priority inversion, demonstrates deadlocks, and generates correct synchronization patterns.

## Priority inversion
Task H waits on mutex held by Task L. Task M preempts L. H is blocked by M (which does not even use the resource!). Priority inheritance: L temporarily gets H's priority.
"""),
        "exercises": [
            ex("04-1", "Ask Claude to trace priority inversion: Task H(high), M(medium), L(low), shared mutex. Show timeline where M blocks H.",
               "Priority inversion.", "Timeline: L holds mutex, H blocks, M preempts L, H stuck behind M. Inheritance: L gets H priority, completes, H proceeds."),
            ex("04-2", "Delegate: Shared USART with mutex. 3 tasks print. Show garbled output WITHOUT mutex, clean WITH mutex.",
               "Mutex demo.", "Before: interleaved characters. After: clean messages. Visual proof of why mutexes matter."),
            ex("04-3", "Ask Claude: Top 5 RTOS synchronization bugs with detection methods. Save to docs/rtos-pitfalls.md.",
               "Bug catalog.", "Priority inversion, deadlock, missed signal, wrong semaphore type, ISR-unsafe API. Detection methods for each."),
        ],
    },
    {
        "id": "05",
        "title": "Software Timers & Events",
        "level": "Advanced",
        "summary": "Udemy: xTimerCreate, event groups, task notifications. Claude designs event-driven architectures.",
        "body": md("""
## Udemy parallel: Software Timers and Event Groups
Enable complex event-driven patterns without polling. Claude designs timer-based watchdogs and event-synchronized systems.
"""),
        "exercises": [
            ex("05-1", "Delegate: Multi-task watchdog via software timers. Each task resets its timer. Expiry logs stuck task name.",
               "Watchdog pattern.", "Each task has a software timer. Expiry callback identifies stuck task. Production-quality reliability pattern."),
            ex("05-2", "Delegate: Event group barrier -- 3 sensor tasks set bits, collector waits for ALL, then processes batch.",
               "Event synchronization.", "xEventGroupWaitBits with pdTRUE (waitForAll). Collector runs after all 3 sensors complete. Barrier pattern."),
        ],
    },
    {
        "id": "06",
        "title": "Memory & Debugging",
        "level": "Advanced",
        "summary": "Udemy: Heap schemes, stack analysis, SEGGER SystemView trace. Claude interprets traces and diagnoses crashes.",
        "body": md("""
## Udemy parallel: Memory Management and Debugging
Choosing the right heap scheme and debugging runtime issues are essential for reliable RTOS systems.

## Heap schemes
- heap_1: alloc only, no free (simplest)
- heap_2: free but no coalescence (fragmentation risk)
- heap_3: wraps stdlib malloc (non-deterministic)
- heap_4: coalescence (best general purpose)
- heap_5: scattered RAM regions
"""),
        "exercises": [
            ex("06-1", "Ask Claude: Heap 1-5 comparison table with columns: free support, fragmentation, deterministic, best use case.",
               "Heap reference.", "Table with clear guidance. heap_4 for most projects. heap_1 for static systems."),
            ex("06-2", "Delegate: Runtime health monitor -- print stack watermarks and heap free every 5 seconds. Add to capstone.",
               "RTOS monitoring.", "uxTaskGetStackHighWaterMark for each task. xPortGetFreeHeapSize. Catches issues before crash."),
            ex("06-3", "Ask Claude: System crashes after 2 hours -- step-by-step RTOS debugging methodology.",
               "Crash diagnosis.", "Steps: watermarks, malloc failed hook, interrupt priority vs configMAX_SYSCALL_INTERRUPT_PRIORITY, configASSERT, SystemView."),
        ],
    },
    {
        "id": "07",
        "title": "Capstone: Multi-Task Sensor System",
        "level": "Expert",
        "summary": "Combine all RTOS: tasks, queues, mutexes, timers, events in a complete acquisition + processing + display system.",
        "body": md("""
## Capstone
Sensor acquisition (timer-triggered), filter+threshold processing, USART display, event-driven alarm -- all synchronized with queues, protected by mutexes, monitored by software timer watchdog.

Tests every RTOS concept from the Udemy course in one integrated system.
"""),
        "exercises": [
            ex("07-1", "Write capstone task brief: all tasks, priorities, stack sizes, IPC (queues, mutexes), timing requirements.",
               "Architecture spec.", "Task table: Sensor(4,256w), Filter(3,512w), Display(2,512w), Alarm(4,256w), Watchdog(1,128w). Queue map. Mutex list."),
            ex("07-2", "Delegate headless. Review: priority assignment (no inversion?), mutex usage (all shared resources?), queue sizing (worst-case?).",
               "Delegation + RTOS review.", "Implementation reviewed for RTOS-specific correctness. Priority, synchronization, sizing all verified."),
            ex("07-3", "Add health monitor. Run 10 minutes. Verify: no stack overflow, no heap exhaustion, all tasks meeting timing.",
               "Stability test.", "10-min run stable. Watermarks show margin. Heap steady. All tasks meet deadlines."),
        ],
    },
    {
        "id": "drills",
        "title": "Daily Drills",
        "level": "All",
        "summary": "Quick RTOS exercises with Claude Code.",
        "body": md("## One drill per day alongside the Udemy RTOS course."),
        "exercises": [
            ex("D-01", "Ask Claude: quiz on task states. 3 questions.", "Recall.", "Quick quiz, graded."),
            ex("D-02", "Ask Claude to design a queue architecture for your scenario.", "Design drill.", "Architecture in 2 min."),
            ex("D-03", "Ask Claude to explain one RTOS pitfall. Add to docs/.", "Pitfall catalog.", "Reference grows."),
            ex("D-04", "Delegate a small task. Verify priorities and stack.", "Task drill.", "Quick create + verify."),
        ],
    },
]

ACCENT = "#ea580c"
ACCENT2 = "#fb923c"
STORAGE_KEY = "rtos-claude-v1"
TITLE = "RTOS with Claude Code — FreeRTOS Companion"
SUBTITLE = "Parallel to FastBit RTOS · FreeRTOS · Tasks · Queues · Semaphores · Debugging"


def main():
    mcu1_html = (ROOT.parent / "mcu1-drivers-with-claude" / "index.html").read_text(encoding="utf-8")

    course = {"title": TITLE, "subtitle": SUBTITLE, "version": "2026.09", "modules": MODULES}
    total = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(course, ensure_ascii=False)

    html_out = re.sub(
        r"(window\.COURSE_DATA\s*=\s*)\{.*?\}(;\s*</script>)",
        lambda m: m.group(1) + data_json + m.group(2),
        mcu1_html,
        count=1,
        flags=re.DOTALL,
    )

    html_out = html_out.replace("mcu1-drivers-claude-v1", STORAGE_KEY)
    html_out = html_out.replace("#7c3aed", ACCENT)
    html_out = html_out.replace("#a78bfa", ACCENT2)
    html_out = re.sub(r"<title>.*?</title>", f"<title>{H.escape(TITLE)}</title>", html_out)

    OUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT} — {len(MODULES)} modules, {total} exercises")


if __name__ == "__main__":
    main()
