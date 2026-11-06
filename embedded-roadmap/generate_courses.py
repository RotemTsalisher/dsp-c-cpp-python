#!/usr/bin/env python3
"""Generate five embedded-roadmap courses (structure + lessons + spa index.html)."""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

from course_data import COURSES
from spa_builder import build_index, md

HOME = Path(__file__).resolve().parent.parent
SYLLABUS_SOURCE = Path(
    r"c:\Users\rotemt\.cursor\projects\c-Users-rotemt-OneDrive-Cardo-Systems-LTD-Desktop-SW-dsp-c-cpp-python\attachments\d6c521ed-30f0-4c03-822e-1fc114be90fe\embedded_systems_dsp_course_syllabuses_updated.md"
)


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:64]


def module_level(idx: int, total: int) -> str:
    if idx <= max(2, total // 5):
        return "Beginner"
    if idx >= total - 2:
        return "Advanced"
    return "Intermediate"


def lesson_body(course: dict, idx: int, title: str) -> str:
    hw = course["hardware"]
    con = course["constraints"]
    slug = course["slug"]
    n = idx + 1
    refs = "\n".join(f"- [{label}]({url})" for label, url in course["refs"][:3])

    lab_generic = textwrap.dedent(
        f"""
        ## Lab workflow (every module)
        1. Create a **Git branch** `module-{n:02d}` and a CCS / ESP-IDF / Arduino project folder tracked in-repo.
        2. Read the official sections cited in `references/` for this module's peripherals.
        3. Build, flash, and capture **UART log + one measurement** (scope, logic analyzer, or serial plot).
        4. Record expected vs observed results in your engineering notebook.
        5. If behavior diverges, follow the debugging checklist below before changing algorithm code.

        ## Step-by-step lab
        ### Prepare
        - Verify power, debugger connection, and that you can blink or print a heartbeat (regression sanity).
        - Document clock configuration and pin map in `README` snippet for this lab.

        ### Implement
        - Implement the module topic on **{hw}** using the approach taught in the lesson (register-level where required).
        - Keep ISRs minimal; move parsing and heavy work to the main loop or a worker task (FreeRTOS on ESP32-S3).

        ### Verify
        - Define at least **three test cases** (nominal, boundary, fault).
        - Compare against Python/MATLAB reference when the module is DSP-related.

        ### Measure
        - Time critical paths with a hardware timer or GPIO toggle + logic analyzer.
        - Estimate RAM/Flash from map file or `idf.py size` / CCS memory view.

        ## Expected results
        - UART (or serial plot) shows deterministic, repeatable measurements across power cycles.
        - No stack overflow, watchdog resets, or unexplained ADC saturation on nominal inputs.

        ## Common mistakes
        - Forgetting `volatile` on flags set in ISRs.
        - Running heavy printf inside ISRs (breaks latency budgets).
        - Misconfigured clock dividers (wrong baud, PWM frequency, or sample rate).
        - Floating-point on MSP430G2553 when fixed-point was required.

        ## Debugging guidance
        - Bisect: GPIO toggle at ISR entry/exit to see jitter and missed events.
        - Single-step from reset through clock init before enabling peripherals.
        - Capture registers after fault; compare with reset defaults in the datasheet.

        ## Official references
        {refs}

        ## Hardware constraints (always)
        {con}
        """
    ).strip()

    topic = textwrap.dedent(
        f"""
        ## Module {n}: {title}

        ### Learning objectives
        - Explain how **{title}** maps to registers, interrupts, and memory on **{hw}**.
        - Implement a buildable lab firmware feature for this module without relying on unverified abstractions.
        - Measure at least one timing or accuracy metric and relate it to real-time constraints.

        ### Concept overview
        This module follows the roadmap syllabus for `{slug}`.
        Treat the MCU as a **deterministic machine** with finite RAM and predictable peripheral behavior.
        When the syllabus calls for register-level understanding, open the family user's guide and locate the
        control/status registers for the peripheral you configure—do not guess bit meanings.

        ### Firmware structure hint
        ```
        src/
          board/        pin map, clock init
          drivers/      thin HAL you own (GPIO, UART, ADC, I2S, ...)
          app/          state machines, DSP blocks, CLI
          tests/        host-side golden vectors (optional)
        ```

        ### Documentation to cite in your report
        - Datasheet: electrical limits and pin functions.
        - User's guide: peripheral chapters for this module.
        - Board guide: which LaunchPad pins are routed to headers.

        {lab_generic}
        """
    ).strip()

    if course.get("algorithm_course"):
        topic = textwrap.dedent(
            f"""
            ## Module {n}: {title}

            ### Learning objectives
            - State the problem in terms of inputs, outputs, constraints, and edge cases.
            - Design in plain language and pseudocode before coding.
            - Implement Python POC, analyze complexity, then port to MSP430 C with fixed capacities.

            ### Mandatory exercise methodology
            1. Problem understanding
            2. Algorithm design + pseudocode
            3. Python proof of concept + tests
            4. Correctness reasoning (invariants / pre/postconditions)
            5. Time and space complexity (best / average / worst where meaningful)
            6. Data-structure justification vs at least one alternative
            7. Embedded C on MSP430G2553 (fixed-width types, bounded memory)
            8. Differential validation against Python vectors
            9. Measurement procedure (cycles, RAM, stack, Flash)
            10. Short engineering report

            ### Host vs target
            - Python under `python_poc/` for rapid iteration.
            - MSP430 firmware under `embedded_c/` with documented `MAX_*` limits.

            {lab_generic}
            """
        ).strip()

    if slug == "arduino-uno-r4-minima" and course.get("extra_notes") and n >= 6:
        topic += "\n\n### Audio / DSP note\n" + course["extra_notes"].strip()

    if slug == "esp32-s3-audio-dsp" and n in (9, 10, 11, 12, 13):
        topic += textwrap.dedent(
            """

            ### I2S lab checklist
            - Confirm BCLK, LRCLK/WS, SDATA, and power grounds for INMP441 / MAX98357A.
            - Start at 16 kHz mono; verify DMA descriptor chain before raising sample rate.
            - Log underrun/overrun counters from the driver.
            """
        )

    return topic


def ex(course: dict, mod_id: str, num: int, kind: str, title: str) -> dict:
    hw = course["hardware"]
    algo = course.get("algorithm_course")
    base_prompt = f"[{kind}] {title} — implement on {hw}."
    if algo:
        base_prompt = (
            f"[{kind}] {title}. Follow the 10-step algorithm methodology in the lesson. "
            "Do not read `solutions/` until you have Python and C vectors passing locally."
        )
    hint = "Check clock init and pin mux before debugging algorithm logic."
    if algo:
        hint = "Write three test vectors by hand (nominal, empty/boundary, adversarial) before coding C."
    solution = textwrap.dedent(
        f"""
        Approach:
        - Restate inputs/outputs/constraints in comments at top of file.
        - Implement smallest correct version first; measure; then optimize if budget requires.

        Verification:
        - Document expected serial output or GPIO pattern.
        - Attach map-file RAM/Flash snapshot for embedded targets.

        Why this matches the course:
        - Uses bounded memory, explicit peripheral setup, and measurement—not desktop assumptions.
        """
    ).strip()
    return {
        "id": f"{mod_id}-{num}",
        "prompt": base_prompt,
        "hints": hint,
        "solution": solution,
        "stretch": f"Add a self-test mode and compare against a Python/MATLAB reference for {title}.",
    }


def exercises_for_module(course: dict, mod_id: str, title: str) -> list[dict]:
    return [
        ex(course, mod_id, 1, "Exercise A", f"{title} — core implementation"),
        ex(course, mod_id, 2, "Exercise B", f"{title} — boundary and error handling"),
        ex(course, mod_id, 3, "Exercise C", f"{title} — performance or resource optimization"),
        ex(course, mod_id, 4, "Assignment", f"{title} — integrated mini-project with written report"),
    ]


def write_exercises_md(path: Path, course: dict, mod_num: int, title: str) -> None:
    algo = course.get("algorithm_course")
    lines = [
        f"# Module {mod_num:02d}: {title}",
        "",
        "Learner-facing exercises only — solutions are in `../solutions/`.",
        "",
    ]
    if algo:
        lines += [
            "Use the 10-step methodology from the lesson (problem → Python → complexity → MSP430 C → report).",
            "",
        ]
    for label, letter in [
        ("Exercise A (core)", "a"),
        ("Exercise B (boundaries)", "b"),
        ("Exercise C (optimize / measure)", "c"),
        ("Independent assignment", "assignment"),
    ]:
        lines += [
            f"## {label}",
            "",
            f"Implement the module topic **{title}** for **{course['hardware']}**.",
            "",
            "### Deliverables",
            "- Buildable project or clearly named source files",
            "- Test procedure with expected results",
            "- Short note on resources used (RAM/Flash/time) where applicable",
            "",
            "### Pass criteria",
            f"- Reproducible behavior across reset; documented edge case `{letter}-edge` handled safely",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_solutions_md(path: Path, mod_num: int, title: str) -> None:
    path.write_text(
        textwrap.dedent(
            f"""
            # Module {mod_num:02d} solutions — {title}

            > Keep this folder out of your daily workflow until you have a serious attempt.

            ## Exercise A
            Full reference implementation lives in the browser course (`index.html` → Reveal solution)
            and in `modules/{mod_num:02d}-*/code/` when starter/solution trees are added per lab.

            ### Why
            - Separates learner prompts from answers (syllabus requirement).

            ## Exercise B–C and assignment
            See module lesson for measurement procedure; solutions emphasize **correct peripheral setup**
            before algorithm tuning.

            ## Common mistakes addressed
            - ISR overload, missing volatile, incorrect clock tree, buffer overrun.
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )


def write_readme(course_dir: Path, course: dict) -> None:
    mods = course["modules"]
    rows = "\n".join(f"| {i+1:02d} | {t} | `modules/{i+1:02d}-{slugify(t)}/` |" for i, t in enumerate(mods))
    fps = "\n".join(f"- {p}" for p in course["final_projects"])
    extra = ""
    if course.get("extra_notes"):
        extra = "\n## Course-specific notes\n" + course["extra_notes"].strip() + "\n"
    text = textwrap.dedent(
        f"""
        # {course["title"]}

        **Hardware:** {course["hardware"]}
        **Prerequisites:** {course["prereq"]}
        **Toolchain:** {course["toolchain"]}

        ## Open the course
        - **Browser:** double-click `index.html` (progress saves in localStorage).
        - **Git-friendly:** read `modules/` lessons, work in `exercises/`, check `solutions/` only after attempting.

        ## Constraints
        {course["constraints"]}

        ## Module map
        | # | Module | Folder |
        |---|--------|--------|
        {rows}

        ## Final project options
        {fps}

        ## Regenerate browser bundle
        ```powershell
        cd embedded-roadmap
        python generate_courses.py
        ```

        ## References
        See `references/README.md` for datasheets and official manuals.
        {extra}
        """
    ).strip()
    course_dir.joinpath("README.md").write_text(text + "\n", encoding="utf-8")


def write_syllabus(course_dir: Path, course: dict) -> None:
    body = [
        f"# Syllabus — {course['title']}",
        "",
        f"**Hardware:** {course['hardware']}",
        "",
        "## Global requirements",
        "- 3 progressive exercises + 1 independent assignment per module",
        "- Labs with expected results, test procedures, debugging guidance",
        "- Solutions separate from learner-facing files",
        "- Git-friendly project layout with build/flash/test documented",
        "",
        "## Modules",
        "",
    ]
    for i, t in enumerate(course["modules"], start=1):
        body.append(f"{i}. **{t}**")
    body += ["", "## Final projects", ""]
    body += [f"- {p}" for p in course["final_projects"]]
    body.append("")
    course_dir.joinpath("syllabus.md").write_text("\n".join(body), encoding="utf-8")


def write_references(course_dir: Path, course: dict) -> None:
    course_dir.joinpath("references").mkdir(parents=True, exist_ok=True)
    lines = ["# References", "", "Use official documentation as source of truth.", ""]
    for label, url in course["refs"]:
        lines.append(f"- [{label}]({url})")
    lines.append("")
    if SYLLABUS_SOURCE.is_file():
        lines.append(f"Master roadmap: `{SYLLABUS_SOURCE.name}` (also copied rationale in repo root syllabus bundle).")
    course_dir.joinpath("references", "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_projects(course_dir: Path, course: dict) -> None:
    course_dir.joinpath("projects").mkdir(parents=True, exist_ok=True)
    lines = [
        "# Final projects",
        "",
        "Pick one option (or propose an equivalent with instructor/self review checklist).",
        "",
    ]
    for p in course["final_projects"]:
        lines += [
            f"## {p}",
            "",
            "### Requirements",
            "- Multi-file firmware architecture (drivers + app)",
            "- Documented pin map and clock configuration",
            "- Test plan with measured results",
            "- Known limitations and next steps",
            "",
        ]
    course_dir.joinpath("projects", "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_tools(course_dir: Path, course: dict) -> None:
    slug = course["slug"]
    course_dir.joinpath("tools").mkdir(parents=True, exist_ok=True)
    course_dir.joinpath("tools", "README.md").write_text(
        textwrap.dedent(
            f"""
            # Tools — {course["slug"]}

            - `../../embedded-roadmap/generate_courses.py` — regenerates `index.html` and module tree.
            - Add per-course scripts here (flash helpers, serial plotters, Python golden-vector generators).

            Suggested next additions:
            - `{slug}_serial_plot.py` — live UART CSV for scope-free bring-up
            - `{slug}_golden_vectors.py` — export test vectors for differential C/Python tests
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )


def write_algorithm_extras(course_dir: Path, mod_num: int, title: str) -> None:
    slug = slugify(title)
    poc = course_dir / "python_poc" / f"mod_{mod_num:02d}_{slug}"
    emb = course_dir / "embedded_c" / f"mod_{mod_num:02d}_{slug}"
    poc.mkdir(parents=True, exist_ok=True)
    emb.mkdir(parents=True, exist_ok=True)
    (poc / "README.md").write_text(
        f"# Python POC — module {mod_num:02d}\n\nStarter: implement `{title}` with tests in `test_mod_{mod_num:02d}.py`.\n",
        encoding="utf-8",
    )
    (poc / f"starter_mod_{mod_num:02d}.py").write_text(
        f'"""Starter POC — {title}. Fill in algorithm; run pytest."""\n\n\ndef solve(*args, **kwargs):\n    raise NotImplementedError\n',
        encoding="utf-8",
    )
    (emb / "README.md").write_text(
        f"# MSP430 C — module {mod_num:02d}\n\nPort the validated Python behavior using fixed `MAX_N` constants.\n",
        encoding="utf-8",
    )


def generate_course(course: dict) -> tuple[int, int]:
    course_dir = HOME / course["slug"]
    course_dir.mkdir(parents=True, exist_ok=True)

    spa_modules: list[dict] = []
    total_ex = 0

    for idx, title in enumerate(course["modules"]):
        mod_num = idx + 1
        mod_id = f"{mod_num:02d}"
        folder = f"{mod_id}-{slugify(title)}"
        mod_path = course_dir / "modules" / folder
        mod_path.mkdir(parents=True, exist_ok=True)

        lesson = lesson_body(course, idx, title)
        (mod_path / "lesson.md").write_text(lesson + "\n", encoding="utf-8")
        (mod_path / "lab_checklist.md").write_text(
            textwrap.dedent(
                """
                # Lab checklist
                - [ ] Branch created; build clean
                - [ ] Pin map documented
                - [ ] Three test cases executed
                - [ ] Measurement captured (time/RAM/Flash or analog metric)
                - [ ] Notebook updated with expected vs actual
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        ex_path = course_dir / "exercises" / f"{folder}.md"
        ex_path.parent.mkdir(parents=True, exist_ok=True)
        write_exercises_md(ex_path, course, mod_num, title)

        sol_path = course_dir / "solutions" / f"{folder}.md"
        sol_path.parent.mkdir(parents=True, exist_ok=True)
        write_solutions_md(sol_path, mod_num, title)

        if course.get("algorithm_course"):
            write_algorithm_extras(course_dir, mod_num, title)

        exercises = exercises_for_module(course, mod_id, title)
        total_ex += len(exercises)
        spa_modules.append(
            {
                "id": mod_id,
                "title": title,
                "level": module_level(idx, len(course["modules"])),
                "summary": f"{course['hardware']} — syllabus module {mod_num}.",
                "body": md(lesson),
                "exercises": exercises,
            }
        )

    write_readme(course_dir, course)
    write_syllabus(course_dir, course)
    write_references(course_dir, course)
    write_projects(course_dir, course)
    write_tools(course_dir, course)

    if course.get("algorithm_course"):
        (course_dir / "benchmarks").mkdir(exist_ok=True)
        (course_dir / "benchmarks" / "README.md").write_text(
            "# Benchmarks\n\nRecord timing, RAM, stack, and Flash per module in dated markdown reports.\n",
            encoding="utf-8",
        )

    build_index(
        course_dir / "index.html",
        title=course["title"],
        subtitle=f"{course['hardware']} · {course['module_count']} modules · hands-on labs",
        storage_key=course["storage_key"],
        modules=spa_modules,
    )

    # Per-course generator stub
    stub = textwrap.dedent(
        f'''#!/usr/bin/env python3
"""Regenerate index.html for {course["slug"]}."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "embedded-roadmap"
subprocess.check_call([sys.executable, str(ROOT / "generate_courses.py"), "{course["slug"]}"])
'''
    )
    course_dir.joinpath("generate_course.py").write_text(stub, encoding="utf-8")

    return len(course["modules"]), total_ex


def main() -> None:
    import sys

    selected = COURSES
    if len(sys.argv) > 1:
        want = set(sys.argv[1:])
        selected = [c for c in COURSES if c["slug"] in want]

    totals = []
    for course in selected:
        n_mod, n_ex = generate_course(course)
        totals.append((course["slug"], n_mod, n_ex))
        print(f"{course['slug']}: {n_mod} modules, {n_ex} exercises")

    # Copy master syllabus once
    roadmap_readme = HOME / "embedded-roadmap" / "README.md"
    roadmap_readme.write_text(
        textwrap.dedent(
            """
            # Embedded Systems & DSP Roadmap (five courses)

            Generated from `embedded_systems_dsp_course_syllabuses_updated.md`.

            | Course folder | Modules |
            |---------------|---------|
            | `msp430-embedded-c/` | 13 |
            | `msp430-embedded-dsp/` | 13 |
            | `arduino-uno-r4-minima/` | 13 |
            | `esp32-s3-audio-dsp/` | 13 |
            | `embedded-algorithms/` | 24 |

            ```powershell
            python generate_courses.py
            ```

            Recommended order: MSP430 C → MSP430 DSP → UNO R4 → ESP32-S3 → Algorithms (can overlap after module 4).
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    if SYLLABUS_SOURCE.is_file():
        dest = HOME / "embedded-roadmap" / "embedded_systems_dsp_course_syllabuses_updated.md"
        if not dest.exists() or dest.read_text(encoding="utf-8") != SYLLABUS_SOURCE.read_text(encoding="utf-8"):
            dest.write_text(SYLLABUS_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")

    print("Done:", totals)


if __name__ == "__main__":
    main()
