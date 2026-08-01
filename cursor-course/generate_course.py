#!/usr/bin/env python3
"""Generate index.html — Cursor course for embedded DSP engineers."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"


def ex(n: str, prompt: str, hints: str, solution: str, stretch: str = "") -> dict:
    return {
        "id": n,
        "prompt": prompt,
        "hints": hints,
        "solution": solution,
        "stretch": stretch,
    }


def md(text: str) -> str:
    """Minimal markdown-ish to HTML for lesson bodies."""
    lines = text.strip().split("\n")
    out: list[str] = []
    in_pre = False
    in_ul = False
    for line in lines:
        if line.startswith("```"):
            if in_pre:
                out.append("</code></pre>")
                in_pre = False
            else:
                if in_ul:
                    out.append("</ul>")
                    in_ul = False
                lang = line[3:].strip() or "text"
                out.append(f'<pre class="code-block" data-lang="{html.escape(lang)}"><code>')
                in_pre = True
            continue
        if in_pre:
            out.append(html.escape(line))
            continue
        if line.startswith("## "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{html.escape(line[3:])}</h3>")
        elif line.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h4>{html.escape(line[4:])}</h4>")
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(line[2:])}</li>")
        elif line.strip() == "":
            if in_ul:
                out.append("</ul>")
                in_ul = False
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<p>{inline_md(line)}</p>")
    if in_ul:
        out.append("</ul>")
    if in_pre:
        out.append("</code></pre>")
    return "\n".join(out)


def inline_md(s: str) -> str:
    s = html.escape(s)
    parts = s.split("`")
    for i in range(1, len(parts), 2):
        parts[i] = f"<code>{parts[i]}</code>"
    return "".join(parts)


MODULES = [
    {
        "id": "00",
        "title": "Start Here: Mindset & Setup",
        "level": "Beginner",
        "summary": "Install Cursor, open a DSP-friendly repo, and learn how AI pair programming fits firmware work.",
        "body": md(
            """
## What you will become fluent in
Cursor is an IDE built on VS Code with **Chat**, **Inline Edit**, **Tab completion**, and an **Agent** that can edit files, run terminals, and use tools. For embedded DSP, your superpower is giving the agent **deterministic context**: register maps, Q-format rules, build commands, and test harnesses.

## Install & first launch
1. Download Cursor from [cursor.com](https://cursor.com).
2. Sign in and pick a model (Composer / Agent models change over time — use the default recommended tier for coding).
3. **File → Open Folder** on a small C or Python DSP sandbox (you will create one in Exercise 1).

## The three surfaces you will live in
- **Editor + Tab**: micro-edits, boilerplate, repetitive register structs.
- **Chat (Ask)**: explain ISR code, compare CMSIS-DSP vs your custom kernel, plan refactors without touching files.
- **Agent (Composer)**: multi-file features, tests, CMake fixes, git operations — with approval gates you control.

## Embedded DSP safety habits (use from day one)
- Never paste production keys, J-Link licenses, or customer binaries into prompts.
- Treat agent shell commands like a junior engineer: review before run on hardware scripts.
- Keep **golden vectors** (small `.csv` / `.npy`) in-repo so the agent can regression-test DSP.

### Key settings to locate now
Open **Cursor Settings** and find: **Rules**, **Models**, **Features → Agent**, **MCP**, **Beta / Labs** (names shift — search settings for "rules", "agent", "mcp").
"""
        ),
        "exercises": [
            ex(
                "00-1",
                "Create a folder `dsp-sandbox` with `src/`, `tests/`, `scripts/`, and `docs/`. Add a one-line `README.md` describing a fictional MCU + FPU target.",
                "Use Agent: \"Create minimal embedded DSP sandbox layout only, no large files.\"",
                """Layout:
```
dsp-sandbox/
  README.md
  src/
  tests/
  scripts/
  docs/
```
README example: \"Target: ARM Cortex-M4F @ 96 MHz, CMSIS-DSP optional, float32 FFT bring-up.\" """,
            ),
            ex(
                "00-2",
                "Open Cursor Settings and list (in your own notes) where **Project Rules**, **User Rules**, and **MCP** live.",
                "Settings search: rules, mcp, agent.",
                "Typical locations (UI labels vary by version):\n- Project rules: `.cursor/rules/*.mdc` in repo + Settings → Rules\n- User rules: global rules in Settings\n- MCP: Settings → MCP (or Cursor Settings → Features → MCP) plus per-project `mcp.json` where supported",
            ),
            ex(
                "00-3",
                "In Chat (Ask mode), ask: \"Explain fixed-point Q15 multiply in one paragraph and give a 3-line C example.\" Do not allow file edits.",
                "Use @Docs only if you have CMSIS docs indexed; otherwise plain Ask is fine.",
                "You should get: product needs >>15 scaling, saturation optional, example like `(int16_t)(((int32_t)a * b) >> 15)` with commentary on overflow.",
            ),
        ],
    },
    {
        "id": "01",
        "title": "UI Tour: Editor, Terminal, Source Control",
        "level": "Beginner",
        "summary": "Navigate like a pro: panels, multi-root, problems tab, and running `cmake`/`make` from integrated terminal.",
        "body": md(
            """
## VS Code DNA
Cursor inherits **Command Palette** (`Ctrl+Shift+P`), **Problems**, **Output**, **Debug**, and **Extensions**. Your embedded flow usually pins: **Terminal** (build/flash), **Problems** (compiler errors Agent must see), **Git**.

## Layout recipe for DSP firmware
- Left: file tree with `src/`, `tests/`, `third_party/` separated.
- Bottom: terminal running `cmake --build` or `west build`.
- Right or bottom: Chat/Agent panel docked where it does not cover `*.h` register maps.

## Command Palette tricks
- `Terminal: Create New Terminal`
- `Git: View History`
- `Preferences: Open User Settings (JSON)` — advanced tuning

## Let the Agent see compiler errors
After a failed build, select the error lines in terminal → **Add to Chat** (or copy). Agents fix faster with **exact** diagnostics than with \"build failed\" alone.
"""
        ),
        "exercises": [
            ex(
                "01-1",
                "Add `src/biquad.h` with an empty struct `BiquadState` and function prototype `void biquad_process(...)`. No implementation yet.",
                "Tab completion in the header after you type the struct name.",
                "Example header snippet:\n```c\n#pragma once\n#include <stdint.h>\ntypedef struct { float z1, z2; } BiquadState;\nvoid biquad_process(const float *in, float *out, uint32_t n, const float *coeffs, BiquadState *st);\n```",
            ),
            ex(
                "01-2",
                "Open integrated terminal, `cd` to your sandbox, run `echo Build placeholder` — then pin that terminal tab.",
                "Right-click terminal tab → rename to \"build\".",
                "Pinned terminal named `build` so Agent instructions can say \"use the build terminal\".",
            ),
            ex(
                "01-3",
                "Intentionally introduce a syntax error in a `.c` file, build if you have a build system — or rely on C/C++ extension squiggles. Copy **Problems** panel text into Chat and ask for a fix **explanation only**.",
                "This trains error-driven Ask workflow before Agent auto-fix.",
                "Chat should identify missing semicolon/brace/type mismatch without editing until you switch to Agent.",
            ),
        ],
    },
    {
        "id": "02",
        "title": "Tab Inline Completion (Copilot-style)",
        "level": "Beginner",
        "summary": "Use Tab for repetitive embedded patterns: DMA descriptors, CMSIS calls, Python numpy vector prep.",
        "body": md(
            """
## When Tab shines in DSP
- Expanding **repetitive** code: tap delay lines, cordic iterations, unrolled MAC loops (where you want consistency).
- Header guard + include blocks copied across drivers.
- Python: generating test vectors matching C array literals.

## When to refuse Tab
- Safety-critical register writes without comments.
- Changing **Q-format** or **shift** constants — verify manually.
- License headers — paste from your legal template instead.

## Steering Tab with context
Open related files (`coeffs.h`, `unit_test.c`) in background tabs — Tab uses recent context. For project-specific style, add a short rule (Module 05).
"""
        ),
        "exercises": [
            ex(
                "02-1",
                "In `tests/test_vectors.py`, start typing `import numpy as np` and a function `def tone(fs, f0, n):` — accept Tab suggestions to finish a sine generator.",
                "Type docstring first: \"Generate float32 sine for FFT golden vector.\"",
                "```python\nimport numpy as np\n\ndef tone(fs: float, f0: float, n: int) -> np.ndarray:\n    t = np.arange(n, dtype=np.float64) / fs\n    return np.sin(2 * np.pi * f0 * t).astype(np.float32)\n```",
            ),
            ex(
                "02-2",
                "In C, type `static inline int32_t q15_mul` and use Tab to suggest body; **edit** the shift to match your project's Q format.",
                "Comment `// Q15 * Q15 -> Q15` above function.",
                "Correct pattern uses `int32_t` accumulator and `>> 15`, with optional saturation helper your project defines.",
            ),
            ex(
                "02-3",
                "Write a 5-line comment block describing an ISR: \"ADC DMA half-complete, double buffer swap\". Use Tab to draft the ISR skeleton; delete any hardware-specific registers you have not verified.",
                "Rule: ISR skeleton only — no fictional register addresses in committed code.",
                "Skeleton with empty callbacks `on_half_complete()` / `on_full_complete()` and `// TODO: verify DR register flags on target silicon`.",
            ),
        ],
    },
    {
        "id": "03",
        "title": "Inline Edit (Cmd/Ctrl+K)",
        "level": "Beginner",
        "summary": "Surgical edits inside a selection: vectorize, add const correctness, convert float kernel to fixed-point.",
        "body": md(
            """
## Inline Edit pattern
1. Select function or lines.
2. `Ctrl+K` (Windows) / `Cmd+K` (macOS).
3. Instruction: precise, testable — \"Add `const` to read-only pointers, preserve MISRA-style naming.\"

## DSP examples
- \"Replace divide with multiply-by-reciprocal with comment showing precomputed `invN`.\"
- \"Add `restrict` only if C99 and project allows; else explain why not.\"
- Python: \"Convert list comprehension to numpy for speed, keep same dtype float32.\"

## Verify
Always re-run unit tests after Inline Edit — it does not have full Agent planning context.
"""
        ),
        "exercises": [
            ex(
                "03-1",
                "Select a loop that copies samples and Inline Edit: \"Use `memcpy` for byte-aligned float blocks; keep scalar tail for odd lengths.\"",
                "If no loop exists, create a naive for-loop first.",
                "Uses `memcpy` for `n/4*4` floats or byte count `len & ~3` pattern with documented alignment assumption.",
            ),
            ex(
                "03-2",
                "Inline Edit a Python test to use `np.testing.assert_allclose(rtol=1e-5)` comparing C output loaded from file.",
                "Mention path `tests/golden/out.bin` in prompt.",
                "Load with `np.fromfile(..., dtype=np.float32)` and assert length match.",
            ),
            ex(
                "03-3",
                "Inline Edit: add Doxygen-style brief to each function in one `.c` file without changing logic.",
                "Select whole file or each function separately for control.",
                "Each function gets `@brief`, `@param`, `@return` consistent with your team template.",
            ),
        ],
    },
    {
        "id": "04",
        "title": "Chat vs Agent vs Plan Mode",
        "level": "Beginner",
        "summary": "Pick the right mode: exploration, execution, or architecture planning before touching DMA code.",
        "body": md(
            """
## Ask / Chat
Best for: \"What does this NVIC line do?\", comparing filter topologies, reviewing stack usage estimates.

## Agent
Best for: implement feature + tests + wire CMake + run build. You approve tool use (terminal, writes).

## Plan Mode
Use when refactoring **cross-cutting** concerns: splitting `dsp/` from `bsp/`, introducing platform abstraction, migrating Q31 → float on FPU targets. Agent produces a plan; you iterate before execution.

## Embedded rule of thumb
| Task | Mode |
| Bootloader touch | Plan → small Agent steps with review |
| New CMSIS-DSP wrapper | Agent with tests |
| Understand aliasing in your ISR | Ask |
"""
        ),
        "exercises": [
            ex(
                "04-1",
                "Ask Chat to draw a **text** dataflow for double-buffered ADC → FFT → magnitude without writing files.",
                "Mention buffer sizes N, hop size H.",
                "Flow: ADC DMA fills A/B; on half/full flag compute FFT in worker context; publish magnitude array to consumer with seqlock or atomic index.",
            ),
            ex(
                "04-2",
                "Switch to **Plan Mode** (or ask Agent to plan only): \"Plan adding unit tests for `biquad_process` without editing yet.\" Approve nothing destructive.",
                "Require deliverables: test list, files to add, cmake target name.",
                "Plan lists: impulse response test, step response, sine sweep SNR threshold, file paths under `tests/`.",
            ),
            ex(
                "04-3",
                "Agent: implement **one** planned test file only (e.g. impulse response) and run it. Stop before refactoring production code.",
                "Tell Agent: minimal diff, no unrelated formatting.",
                "Single test binary or pytest wrapper invoking compiled test harness; Agent log shows command run + pass/fail.",
            ),
        ],
    },
    {
        "id": "05",
        "title": "Context: @ Files, Folders, Code, Docs, Web",
        "level": "Intermediate",
        "summary": "Precision context beats long prompts — critical for register maps and coefficient headers.",
        "body": md(
            """
## @ mentions
- `@src/filter.c` — single file
- `@src/` — folder (use sparingly; can burn context)
- `@Code` — symbols (when indexed)
- `@Docs` — vendor docs you added
- `@Git` — diffs, commits (great for review)

## DSP workflow
Pin **golden** references: `@tests/golden/fft_256_ref.npy` description in prompt, not always the binary itself.

## Anti-pattern
Attaching entire `third_party/CMSIS` — instead add a rule summarizing which CMSIS functions you allow.
"""
        ),
        "exercises": [
            ex(
                "05-1",
                "Ask with `@README.md` + `@src/biquad.h`: \"List missing pieces to ship a minimal biquad module.\"",
                "Create README if empty with target and build notes.",
                "Answer should mention: `.c` implementation, coeffs design doc, tests, cmake source list, maybe Q format note.",
            ),
            ex(
                "05-2",
                "Agent task: \"Using only `@tests/`, propose a python script layout to generate C arrays\" — no implementation until you approve plan in message.",
                "Keep scope to tests folder.",
                "Proposes `tests/gen_vectors.py` outputting `tests/generated/vectors.c` with `const float tap[] = {...};`",
            ),
            ex(
                "05-3",
                "Use @Git (or paste `git diff`) after a small change; ask Chat for a **review checklist** tuned to ISR safety.",
                "Change anything in a `.c` file first.",
                "Checklist covers: reentrancy, volatile MMIO, stack usage, FPU context save, priority inversion.",
            ),
        ],
    },
    {
        "id": "06",
        "title": "Project Rules (.mdc) for C/C++/DSP",
        "level": "Intermediate",
        "summary": "Encode MISRA-ish style, Q-format, CMSIS policy, and \"never touch bootloader\" as persistent rules.",
        "body": md(
            """
## `.cursor/rules/*.mdc`
Rules are markdown with YAML frontmatter:

```yaml
---
description: DSP fixed-point conventions
globs: **/*.{c,h,cpp,hpp}
alwaysApply: false
---
```

## What embedded teams put in rules
- Integer types (`stdint.h` only), forbid implicit narrowing
- ISR rules: no malloc, no printf, flag-only in ISR
- Naming: `Module_Action` for HAL, `dsp_` prefix for algorithms
- Build: always run `cmake --build build --target tests` after DSP changes
- Forbidden paths: `bootloader/**`, `cert/**`

## Keep rules short
Under ~50 lines each; split by concern. The agent reads many rules — verbosity hurts.
"""
        ),
        "exercises": [
            ex(
                "06-1",
                "Create `.cursor/rules/dsp-fixed-point.mdc` with globs for C/H and 8–15 lines: Q15 multiply, saturation function name, no float in ISR paths.",
                "Ask Agent if unsure about frontmatter fields.",
                "File includes frontmatter + bullets: use `dsp_q15_mul`, saturate via `dsp_sat_q15`, `#ifdef DSP_USE_FPU` for non-ISR.",
            ),
            ex(
                "06-2",
                "Create `alwaysApply: true` rule `00-global-safety.mdc`: no secrets, no force git push, review before flash scripts.",
                "One concern: safety.",
                "Always-apply rule with explicit never-commit patterns and hardware script approval.",
            ),
            ex(
                "06-3",
                "Add Python rule `globs: **/*.py` requiring numpy float32 for golden vectors and pytest for tests.",
                "Cross-link to tests folder in rule text.",
                "Rule says: golden vectors dtype float32; tests live in `tests/`; prefer `assert_allclose`.",
            ),
            ex(
                "06-4",
                "Prompt Agent: \"Add a biquad coeff helper violating our Q15 rule\" then confirm Agent **corrects** per rule or you fix rule gaps.",
                "Meta-exercise on rule enforcement.",
                "Either Agent refuses float in ISR path or rule updated to clarify allowed contexts.",
            ),
        ],
    },
    {
        "id": "07",
        "title": "AGENTS.md & Team Conventions",
        "level": "Intermediate",
        "summary": "Repository-level agent instructions for onboarding and consistent multi-engineer behavior.",
        "body": md(
            """
## AGENTS.md (repo root)
Some teams add `AGENTS.md` describing:
- How to build/flashing **simulator vs hardware**
- Where tests live
- Code owners mindset (don't edit vendor blobs)

## Pair with CODEOWNERS
Agent can split PRs aligned to ownership (see Module 16).

## Template sections
1. Build commands (Debug/Release)
2. Target matrix (M4F, H7, Linux host sim)
3. DSP numerical tolerances
4. PR checklist
"""
        ),
        "exercises": [
            ex(
                "07-1",
                "Draft `AGENTS.md` with **Build**, **Test**, **Flash** sections for a hypothetical `arm-none-eabi-gcc` CMake project.",
                "Keep commands copy-paste ready.",
                "Includes `cmake -B build -DCMAKE_TOOLCHAIN_FILE=cmake/arm-gcc.cmake`, `cmake --build build`, `ctest --test-dir build`, flash via `pyocd` placeholder.",
            ),
            ex(
                "07-2",
                "Ask Agent to read `AGENTS.md` and scaffold `CMakeLists.txt` host build for algorithm sim (no HAL).",
                "Single executable `biquad_sim`.",
                "Top-level CMake adds `src/biquad.c`, links math lib on UNIX, enables `-std=c99 -Wall -Wextra`.",
            ),
            ex(
                "07-3",
                "Add **Numerical tolerance** section: FFT SNR > 60 dB vs golden; max biquad coeff error 1e-6 float sim.",
                "These become acceptance criteria for later Agent tasks.",
                "Documented thresholds Agent can cite when writing tests.",
            ),
        ],
    },
    {
        "id": "08",
        "title": "Building, Problems Tab, Agent Fix Loops",
        "level": "Intermediate",
        "summary": "Close the loop: compile → paste errors → Agent patch → repeat until green.",
        "body": md(
            """
## The embedded fix loop
1. `cmake --build build 2>&1 | tee build.log`
2. Select failures → Add to Chat **or** tell Agent \"read terminal output\"
3. Agent edits **minimal** hunks
4. Rebuild before optimizing

## Cross-compile tips in prompts
State toolchain file, CPU flags (`-mfpu=fpv4-sp-d16`), and whether `double` is banned.

## Host vs target
Prefer **host unit tests** for DSP numerical parity; target tests for cycle counts / DMA integration.
"""
        ),
        "exercises": [
            ex(
                "08-1",
                "Introduce wrong prototype in header vs `.c`; run build; Agent fix with terminal output attached.",
                "One error at a time if learning.",
                "Matching signatures and `#include` order restored; build succeeds.",
            ),
            ex(
                "08-2",
                "Add `-Werror` in CMake for host build; Agent resolves first warning in `biquad.c`.",
                "Prompt: fix without suppressing globally.",
                "Local cast or const fix rather than blanket pragma unless rule allows.",
            ),
            ex(
                "08-3",
                "Create `scripts/build_host.sh` (or `.ps1`) wrapping configure+build; Agent must use script in future tasks ( mention in AGENTS.md).",
                "Idempotent script.",
                "Script exits non-zero on failure; documents env vars.",
            ),
        ],
    },
    {
        "id": "09",
        "title": "Testing: C host tests, pytest, golden vectors",
        "level": "Intermediate",
        "summary": "Make DSP testable: Python generates goldens, C compares, Agent maintains parity.",
        "body": md(
            """
## Layered testing pyramid for DSP firmware
1. **Pure C algorithm** on host (fast)
2. **Python reference** (numpy/scipy) for goldens
3. **Target-in-the-loop** (optional, slower)

## pytest + subprocess
Run compiled test binary from pytest, or use `ctypes`/`cffi` if you export a sim `.so`.

## Tell Agent acceptance criteria
\"Impulse response peak within 1 LSB of reference\" beats \"make tests pass\".
"""
        ),
        "exercises": [
            ex(
                "09-1",
                "Add host test `tests/test_biquad_impulse.c` with `main()` returning 0/1; compare first output sample to expected 1.0 for DC gain 1.",
                "Keep coeff simple (identity-like).",
                "Minimal test harness with `assert(fabs(out[0]-1.0) < 1e-5);` style checks.",
            ),
            ex(
                "09-2",
                "Python: `tests/test_biquad_pytest.py` runs C test exe via `subprocess.run` and asserts return code 0.",
                "Skip if exe missing with clear message.",
                "Uses `pytest.skip` when binary not built; documents build dep.",
            ),
            ex(
                "09-3",
                "Generate 256-point FFT golden: Python writes `tests/golden/fft_mag.bin`; C test reads file (host) and compares max error.",
                "Agent implements both sides in small steps.",
                "Document generation command in `tests/golden/README.md`.",
            ),
            ex(
                "09-4",
                "Ask Agent to add CI snippet (GitHub Actions) **host only** building and running tests — no hardware.",
                "yaml under `.github/workflows/dsp-host.yml`.",
                "Workflow: checkout, apt install cmake gcc, build, ctest/pytest.",
            ),
        ],
    },
    {
        "id": "10",
        "title": "Debugging: GDB, printf trace, Agent as debugger buddy",
        "level": "Intermediate",
        "summary": "Combine traditional embedded debug with Agent explaining faults and suggesting watch expressions.",
        "body": md(
            """
## Cursor + C/C++ extension debugging
- `launch.json` for J-Link / OpenOCD / pyOCD
- Conditional breakpoints on buffer index

## Agent role
Paste **HardFault** register dump or GDB backtrace — Ask mode explains **likely** causes; Agent can propose defensive checks in code.

## SWO / RTT
Ask Agent to stub an `log_rtt()` macro matching your SEGGER setup — you verify addresses.

## Don't
Agent cannot replace reading the Reference Manual — use it to accelerate hypothesis generation.
"""
        ),
        "exercises": [
            ex(
                "10-1",
                "Create `.vscode/launch.json` template for **host** gdb debugging `biquad_sim` (not hardware yet).",
                "Ask Agent; verify paths.",
                "Config with `program`, `args`, `cwd`, stop at `main`.",
            ),
            ex(
                "10-2",
                "Paste a fake backtrace (write one) into Chat; ask for ranked hypotheses and **one** defensive code change.",
                "Simulate null pointer in process loop.",
                "Suggests NULL checks, length validation, assert macros gated by `DEBUG`.",
            ),
            ex(
                "10-3",
                "Inline Edit: add optional `DSP_TRACE` macro expanding to `printf` on host only.",
                "Use `#ifdef HOST_BUILD`.",
                "`#ifdef HOST_BUILD` `#include <stdio.h>` `#define DSP_TRACE(fmt, ...) printf(fmt, ##__VA_ARGS__)` else empty.",
            ),
        ],
    },
    {
        "id": "11",
        "title": "Git Basics with Agent",
        "level": "Intermediate",
        "summary": "Status, diff, focused commits — agent follows your git safety rules.",
        "body": md(
            """
## Teach Agent your git etiquette via rules
- No `git add -A` unless asked
- Conventional commits or your team format
- Never force-push main

## Typical flow
1. You: \"Prepare commit for biquad tests only\"
2. Agent: status, diff, stage named files, propose message
3. You: approve commit

## `.gitignore` for DSP
Ignore `build/`, `*.o`, `*.bin` flash artifacts, large captures — but **keep** small goldens.
"""
        ),
        "exercises": [
            ex(
                "11-1",
                "Agent: show `git status` and `git diff` summary; do **not** commit until next exercise.",
                "Practice read-only git ops.",
                "Clean summary of tracked/untracked; highlights test additions vs junk.",
            ),
            ex(
                "11-2",
                "Commit only `src/biquad.c` and matching header with message `feat(dsp): add biquad process stub`.",
                "Explicit file list in prompt.",
                "Single-purpose commit; other dirty files remain unstaged.",
            ),
            ex(
                "11-3",
                "Add `.gitignore` for CMake artifacts; separate commit `chore: ignore build tree`.",
                "Two-commit discipline.",
                "Ignores `build/`, `cmake-build-*/`, `*.user`, optional `.vscode/` local settings if team policy says so.",
            ),
        ],
    },
    {
        "id": "12",
        "title": "Branches, PRs, and gh CLI",
        "level": "Advanced",
        "summary": "Feature branches, pull requests, CI checks — Agent as release engineer assistant.",
        "body": md(
            """
## Branch workflow
`main` protected → `feat/dsp-biquad-tests` → PR → review → merge.

## gh CLI
`gh pr create`, `gh pr checks`, `gh run view` — Agent can run if you allow shell.

## PR description quality
Ask Agent for Summary + Test plan bullets matching your team template.

## Embedded PR extras
Note: **flash size delta**, **CPU load**, **FPU context** impacts in description.
"""
        ),
        "exercises": [
            ex(
                "12-1",
                "Create branch `feat/dsp-host-tests` from main; verify with `git branch --show-current`.",
                "Agent can run git write commands with approval.",
                "On feature branch; working tree understood.",
            ),
            ex(
                "12-2",
                "Push branch and open draft PR with Summary/Test plan via `gh pr create --draft`.",
                "Needs remote; skip if no GitHub remote — practice message drafting instead.",
                "PR body includes build instructions and \"host-only CI\".",
            ),
            ex(
                "12-3",
                "Ask Agent to respond to a **mock review comment**: \"Add bound check on n samples\" — push fix commit.",
                "Edit code + commit + push.",
                "Early return or assert on `n==0` / max block size policy.",
            ),
        ],
    },
    {
        "id": "13",
        "title": "Splitting Work into Small PRs",
        "level": "Advanced",
        "summary": "Use split-to-prs mindset: independent reviewable slices for DSP + infra changes.",
        "body": md(
            """
## When to split
- PR touches **CMake**, **DSP core**, and **BSP** → three PRs
- Generated vectors separate from algorithm change

## Agent skill: split-to-prs
Ask: \"Propose split plan only\" before any git writes. Requires backup stash ref before moving hunks.

## Stacking
Foundation PR (headers + empty impl) → tests PR → optimization PR with perf notes.
"""
        ),
        "exercises": [
            ex(
                "13-1",
                "Make a messy working tree: CMake + biquad + python gen in one diff. Ask Agent for **split plan only** (titles + files per PR).",
                "No git mutations.",
                "Plan with 3 PRs: build infra, algorithm, test vectors.",
            ),
            ex(
                "13-2",
                "Execute first slice only: commit CMake + AGENTS.md; leave DSP code unstaged.",
                "Stage named paths only.",
                "First PR ready; other changes still local.",
            ),
            ex(
                "13-3",
                "Write Mermaid diagram in PR comment showing dependency between stacked PRs.",
                "Agent generates mermaid; you paste to PR.",
                "Graph: PR1 CMake → PR2 biquad → PR3 tests depending on PR2.",
            ),
        ],
    },
    {
        "id": "14",
        "title": "Git Worktrees for Parallel Bring-up",
        "level": "Advanced",
        "summary": "Work on `feat/fpu-fft` while hotfixing `release/1.2` without stashing chaos.",
        "body": md(
            """
## Worktrees 101
```bash
git worktree add ../dsp-fft-work feat/fpu-fft
git worktree add ../dsp-hotfix release/1.2
```
Open **separate Cursor windows** per worktree — agents stay isolated.

## DSP use cases
- Parallel: **optimization branch** vs **bugfix on shipping firmware**
- Long Agent job on feature worktree while you manually debug hardware in another

## Cleanup
`git worktree remove` when done; avoid deleting branch with unmerged work.
"""
        ),
        "exercises": [
            ex(
                "14-1",
                "Create a second worktree for a fake branch `exp/q31-biquad`; open it in new Cursor window.",
                "Document path in notes.",
                "Two folders side-by-side; independent `.git` worktree metadata.",
            ),
            ex(
                "14-2",
                "In worktree A, Agent adds Q15 biquad; in worktree B, float biquad — confirm no cross-contamination.",
                "Same repo, different branches.",
                "Build trees separate; git status isolated per worktree.",
            ),
            ex(
                "14-3",
                "Remove experimental worktree after merging or abandoning — Agent lists worktrees first.",
                "`git worktree list`.",
                "Clean list; only main worktree remains or expected set.",
            ),
        ],
    },
    {
        "id": "15",
        "title": "Agent Skills (SKILL.md)",
        "level": "Advanced",
        "summary": "Package team workflows: CMSIS-DSP integration, release notes, coefficient validation.",
        "body": md(
            """
## Skills location
- Personal: `~/.cursor/skills/your-skill/SKILL.md`
- Project: `.cursor/skills/your-skill/SKILL.md`
- **Never** commit to `~/.cursor/skills-cursor/` (reserved)

## SKILL.md frontmatter
```yaml
---
name: dsp-coeff-review
description: Validates biquad/IIR coefficients for stability and Q-format scaling. Use when changing filters or DSP coeffs.
---
```

## disable-model-invocation
Default `true` — invoke explicitly: \"Use dsp-coeff-review skill\".

## Embedded skill ideas
- Flash procedure checker
- Register map diff reviewer
- MISRA spot-check (not certification!)
"""
        ),
        "exercises": [
            ex(
                "15-1",
                "Create project skill `.cursor/skills/dsp-golden-vectors/SKILL.md` describing how to regenerate and commit goldens.",
                "Include trigger terms in description.",
                "Steps: run gen script, check file size limits, update README, run pytest.",
            ),
            ex(
                "15-2",
                "Invoke skill explicitly in Agent: \"Use dsp-golden-vectors skill to add a new sine wave golden.\"",
                "Observe skill-shaped behavior.",
                "Agent follows SKILL steps rather than improvising.",
            ),
            ex(
                "15-3",
                "Add optional `reference.md` with numpy snippet for FFT reference generation.",
                "Keep SKILL.md under 80 lines.",
                "Reference holds long code; SKILL links to it.",
            ),
        ],
    },
    {
        "id": "16",
        "title": "MCP: Extending the Agent",
        "level": "Advanced",
        "summary": "Connect GitHub, Linear, docs, or custom tools — with embedded-safe guardrails.",
        "body": md(
            """
## What MCP gives you
Model Context Protocol servers expose **tools** the Agent can call: issues, PRs, databases, internal APIs.

## Configure
Cursor Settings → MCP: add server (stdio or HTTP). Project-level configs may live in `.cursor/mcp.json` depending on version.

## Embedded guardrails
Use hooks (`beforeMCPExecution`) to block production flash tools from cloud agents.

## Practical MCP for firmware teams
- GitHub: PR status, issues
- Sentry: field crash logs
- Custom: read-only artifact server for benchmark results

## Automations note
Dashboard-backed MCP servers differ from local-only servers — cloud automations may only use eligible servers.
"""
        ),
        "exercises": [
            ex(
                "16-1",
                "List which MCP servers you have enabled (if any) and write one paragraph on **read-only** policy for production.",
                "No keys in course repo.",
                "Policy: CI triggers ok; flash/delete tools disabled for cloud; secrets via env not repo.",
            ),
            ex(
                "16-2",
                "If GitHub MCP available: Ask Agent to summarize open issues labeled `dsp` (or mock if unavailable).",
                "Fallback: use `gh issue list` in terminal.",
                "Structured summary with links/numbers.",
            ),
            ex(
                "16-3",
                "Design (on paper) a **read-only** MCP tool `get_benchmark_csv` returning last night's CMSIS-DSP bench — no hardware control.",
                "Write spec in `docs/mcp-benchmark-spec.md`.",
                "Spec: inputs run_id, outputs CSV text, auth token env var, rate limits.",
            ),
        ],
    },
    {
        "id": "17",
        "title": "Cursor Hooks (.cursor/hooks.json)",
        "level": "Advanced",
        "summary": "Audit and gate agent actions: shell, MCP, file edits — fail-closed for flash scripts.",
        "body": md(
            """
## hooks.json version 1
Events include: `beforeShellExecution`, `afterFileEdit`, `beforeSubmitPrompt`, `preToolUse`, `sessionStart`, ...

## Embedded examples
- **beforeShellExecution**: block `openocd` flash unless env `ALLOW_FLASH=1`
- **afterFileEdit**: run `clang-format` on touched `.c/.h`
- **beforeSubmitPrompt**: regex scan for AWS keys

## Project vs user hooks
Project: `.cursor/hooks.json` — share with team. User: `~/.cursor/hooks.json`.

## Fail open vs closed
Safety gates should **fail closed** (deny on error).
"""
        ),
        "exercises": [
            ex(
                "17-1",
                "Create `.cursor/hooks.json` with a stub `afterFileEdit` entry pointing to a script that echoes JSON ack (no-op pass-through).",
                "See Cursor hooks docs for schema version 1.",
                "Valid JSON listing hook command path under `.cursor/hooks/`.",
            ),
            ex(
                "17-2",
                "Implement `beforeShellExecution` hook denying commands matching `flash|openocd|pyocd` unless allow flag set.",
                "Document in AGENTS.md.",
                "Hook returns deny decision with user-visible reason string.",
            ),
            ex(
                "17-3",
                "Test: ask Agent to run a harmless `echo test` (allow) vs blocked flash command (deny).",
                "Observe hook interaction.",
                "Allow succeeds; flash blocked with clear message.",
            ),
        ],
    },
    {
        "id": "18",
        "title": "Cloud Agents & Background Work",
        "level": "Advanced",
        "summary": "Run agents while your laptop is closed — ideal for long refactors, CI fixes, doc sweeps.",
        "body": md(
            """
## Cloud / background agents
Use for: multi-file test generation, addressing review comments, rebasing stacks — **not** for secrets-heavy or hardware tasks.

## Prep repo for cloud
- Clear AGENTS.md build/test commands
- Rules forbidding destructive git
- Small reproducible host tests

## Handoff workflow
1. Push branch
2. Start cloud agent with scoped task
3. Review PR diff like any human contributor

## Security
Treat cloud agent like CI: read-only prod MCP, no flash hooks allowed.
"""
        ),
        "exercises": [
            ex(
                "18-1",
                "Write a cloud-safe task brief (paste into agent): \"Add host tests for biquad only; no git push; open PR when green.\"",
                "Bullet constraints and acceptance tests.",
                "Brief includes file scope, commands, tolerance, forbidden paths.",
            ),
            ex(
                "18-2",
                "Audit repo for secrets: Agent runs `git grep -i password` / scan `.env` patterns — fix `.gitignore`.",
                "No real secrets in sandbox.",
                "Clean scan or documented false positives.",
            ),
            ex(
                "18-3",
                "Simulate review: pull remote branch (or friend’s patch) and use Agent \"apply review feedback\" with small commits.",
                "Practice async collaboration.",
                "Incremental commits per review thread.",
            ),
        ],
    },
    {
        "id": "19",
        "title": "Cursor Automations",
        "level": "Advanced",
        "summary": "Scheduled/triggered agents: nightly golden regen, PR triage, Slack notifications.",
        "body": md(
            """
## Automations (product feature)
Explicit **Cursor Automations** — not generic GitHub Actions unless you choose that separately.

Triggers may include: git push, PR opened, schedule, Slack.

## Good automation tasks for DSP teams
- Regenerate goldens + open PR if diff detected
- Comment CPU cycle regression when benchmark artifact changes
- Label PRs touching `src/dsp/**`

## Finish in editor
Many automations need final trigger/channel picks in the Automations UI.
"""
        ),
        "exercises": [
            ex(
                "19-1",
                "Draft automation spec table: Name, Trigger, Tools, Instructions, Outcome — for \"nightly host DSP tests on main\".",
                "Plain language, no secrets.",
                "Table row set describing schedule + run pytest + open issue on fail.",
            ),
            ex(
                "19-2",
                "Draft second automation: on PR touching `**/*.c`, run Bugbot-like review instruction (manual invoke if no bot).",
                "Use review checklist from Module 20.",
                "Automation comment template with ISR checklist.",
            ),
            ex(
                "19-3",
                "List **defer to editor** fields (channels, repo scope) you cannot safely guess.",
                "PCD completeness mindset.",
                "Notes Slack channel IDs, org/repo pickers.",
            ),
        ],
    },
    {
        "id": "20",
        "title": "Subagents: Bugbot & Security Review",
        "level": "Advanced",
        "summary": "Dedicated review passes on diffs before merge — especially memory safety in C.",
        "body": md(
            """
## When to invoke
- Before merging DSP changes touching ISRs or DMA
- After large Agent-generated refactors

## Bugbot-style review
Ask explicitly: \"Bugbot on branch changes\" with focus areas (overflow, off-by-one in block processing).

## Security review
For tools talking to cloud, OTA, or crypto — not every IIR patch needs it.

## Your job
Triage findings: real bug vs noise — embedded static analysis already noisy.
"""
        ),
        "exercises": [
            ex(
                "20-1",
                "Run an explicit review pass on your last DSP commit (Agent with review instructions: off-by-one, Q format, ISR safety).",
                "Use diff scope, not whole repo.",
                "Written findings ranked P0/P1/P2.",
            ),
            ex(
                "20-2",
                "Fix one P1 finding (e.g. missing length check); commit with `fix(dsp): guard block length`.",
                "Show before/after in notes.",
                "Patch + test proving fix.",
            ),
            ex(
                "20-3",
                "Write `.cursor/rules/review-before-merge.mdc` reminding Agent to run review checklist when user says \"pre-merge\".",
                "Short rule.",
                "Trigger phrase + bullet checklist.",
            ),
        ],
    },
    {
        "id": "21",
        "title": "Multi-file Refactors & Codebase Search",
        "level": "Advanced",
        "summary": "Rename Q31 types, extract `dsp/` library, migrate CMSIS calls — Agent + ripgrep discipline.",
        "body": md(
            """
## Agent search tools
Agent uses ripgrep/glob — help it with unique symbols (`dsp_biquad_` prefix).

## Refactor recipe
1. Plan mode: impact analysis
2. Add compatibility `#define` shims
3. Migrate tests first
4. Remove shims in final PR

## Python/C boundary
Regenerate ctypes headers when changing exported sim API.
"""
        ),
        "exercises": [
            ex(
                "21-1",
                "Plan rename `BiquadState` → `dsp_biquad_state_t` across repo; Agent executes in two commits (typedef alias, then rename).",
                "Watch for break in tests.",
                "Intermediate typedef alias commit optional for smooth review.",
            ),
            ex(
                "21-2",
                "Extract `src/dsp/` and `src/platform/` — move files; fix includes; build green.",
                "Agent updates CMake lists.",
                "Includes updated without circular deps.",
            ),
            ex(
                "21-3",
                "Add ripgrep-friendly `#error` guard in header if wrong include path used (`platform/hal.h` from dsp).",
                "Document include graph in docs/architecture.md.",
                "Compile-time error message guides correct include.",
            ),
        ],
    },
    {
        "id": "22",
        "title": "Canvas, Docs, and Long-running Analysis",
        "level": "Advanced",
        "summary": "Use Canvas for visual bring-up timelines, filter response plots, benchmark dashboards.",
        "body": md(
            """
## Canvas
When Agent produces charts, benchmark tables, or architecture timelines, **Canvas** gives a side pane React app for exploration.

## DSP fits
- Bode plot exploration from exported CSV
- DMA timeline visualization
- Flash/RAM budget tables

## When to skip Canvas
Single-file fix — stay in editor.
"""
        ),
        "exercises": [
            ex(
                "22-1",
                "Export CSV `docs/bench/filter_cycles.csv` (fake data ok); ask Agent for Canvas-friendly summary table of cycles vs block size.",
                "Columns: block_size, cycles, sram_bytes.",
                "Table + brief analysis identifying knee in cache behavior.",
            ),
            ex(
                "22-2",
                "Maintain `docs/architecture.md` mermaid: ADC → DSP chain → comms; update after refactor.",
                "Keep in sync with code.",
                "Diagram matches module boundaries in repo.",
            ),
            ex(
                "22-3",
                "Ask Chat to critique architecture doc for **missing failure modes** (overflow, underrun).",
                "No file edits required.",
                "List adds watchdog, buffer underrun metric, clip detect.",
            ),
        ],
    },
    {
        "id": "23",
        "title": "Cursor SDK & Programmatic Agents (Overview)",
        "level": "Expert",
        "summary": "Run agents from CI or internal portals via @cursor/sdk — nightly DSP regression orchestration.",
        "body": md(
            """
## SDK use cases
- Kick agent on new golden diff in artifact store
- Auto-triage static analysis upload
- Internal \"DSP copilot\" web UI for your team

## Concepts
`Agent.create`, streaming runs, cancellation, MCP configuration per agent instance.

## Embedded caution
SDK agents inherit repo rules; run in isolated runners; no JTAG from cloud.

Deep reference: Cursor SDK skill docs when integrating.
"""
        ),
        "exercises": [
            ex(
                "23-1",
                "Write pseudo-code (Python) calling SDK: on artifact upload, spawn agent with prompt \"compare CSV to baseline thresholds\".",
                "No API keys in repo.",
                "Shows trigger, prompt template, exit criteria.",
            ),
            ex(
                "23-2",
                "Map which steps in your current manual workflow SDK could automate vs must stay human (flash, bench validation).",
                "Table in notes.",
                "Human: target timing, EMC, analog bring-up. Automate: host numerical, lint, doc sync.",
            ),
        ],
    },
    {
        "id": "24",
        "title": "Capstone: End-to-end DSP Feature Shipment",
        "level": "Expert",
        "summary": "Ship a mini feature: DC blocker IIR + tests + CI + PR + review — all Cursor workflows combined.",
        "body": md(
            """
## Capstone spec
Implement **DC blocker** (first-order high-pass) for float32 audio blocks:
- `src/dc_block.h`, `src/dc_block.c`
- Host tests vs Python reference
- CMake target + CI workflow
- Rules + skill + AGENTS.md updated
- PR with perf note (cycles estimated on host only)

## Acceptance
- Step response settles
- Sine at 1 kHz attenuated < 0.1 dB (config dependent — document)
- Agent git history clean, split if needed

## Expert bonus
Worktree for experimental Q15 version; hook blocking flash; MCP issue filed for follow-up target benchmark.
"""
        ),
        "exercises": [
            ex(
                "24-1",
                "Plan Mode: full work breakdown with PR slices, owners, and test matrix for DC blocker.",
                "Do not code until plan approved by you.",
                "WBS + PR list + risks (coeff precision, subnormal handling).",
            ),
            ex(
                "24-2",
                "Implement slice 1: algorithm + host unit tests only; green build.",
                "Agent allowed; minimal scope.",
                "Passes impulse/sine tests; documented coeff derivation.",
            ),
            ex(
                "24-3",
                "Implement slice 2: pytest goldens + CI; open PR; run review checklist.",
                "Include Test plan in PR body.",
                "CI badge green; review comments addressed.",
            ),
            ex(
                "24-4",
                "Expert: parallel Q15 experimental branch in worktree; document SNR tradeoff in Canvas or markdown report.",
                "Optional float vs fixed essay.",
                "Report with plots/tables and recommendation for MCU target.",
            ),
            ex(
                "24-5",
                "Write personal cheat sheet `docs/my-cursor-playbook.md`: modes, @ mentions, when hooks fire, top 5 prompts you use weekly.",
                "This is **your** operating manual.",
                "One-page dense reference tailored to your job.",
            ),
        ],
    },
]

# Extra micro-exercises sprinkled as "drills" module
DRILLS = {
    "id": "drills",
    "title": "Daily Drills (Quick reps)",
    "level": "All levels",
    "summary": "5-minute exercises to keep Cursor muscle memory warm.",
    "body": md(
        """
## How to use drills
Do one drill per day between modules. Repeat until automatic.

## Drill categories
- Tab / Inline Edit
- @ context
- Agent git hygiene
- Test-first prompts
"""
    ),
    "exercises": [
        ex("D-01", "Tab-complete a 10-line `const float` Hann window array in C.", "Start `static const float hann[10]`.", "Completed symmetric window values summing reasonably for 10-point." ),
        ex("D-02", "Ask: convert this time-domain IIR diff to direct form II equation — paste your biquad code.", "Single math question.", "Correct DFII state update equations."),
        ex("D-03", "Inline Edit `#pragma once` guard and include order in a messy header.", "Select all.", "IWYU-friendly order: stdint, project, extern C."),
        ex("D-04", "Agent: run only `ctest -R biquad` equivalent or your test binary — no other commands.", "Narrow tool scope.", "Only requested test executes."),
        ex("D-05", "@ folder `tests/` — ask what's missing for 90% coverage confidence.", "Review-only.", "Gap list: edge cases, NaN, denormals, block size 1, max block."),
        ex("D-06", "Write a one-sentence rule addition banning `malloc` in `src/dsp/**`.", "mdc globs.", "Rule file updated with glob `src/dsp/**`."),
        ex("D-07", "Compose git commit message for test-only change — Ask mode only.", "Conventional commits.", "Message like `test(dsp): add sine sweep case`."),
        ex("D-08", "Plan-only: estimate RAM for 256-pt complex FFT buffers (float32).", "Show formula.", "256*2*4 bytes for interleaved re/im plus twiddle table note."),
        ex("D-09", "Hook or rule: ensure `clang-format` mentioned for `.c` edits.", "Team policy.", "Documented formatting step post-edit."),
        ex("D-10", "Simulate HardFault: Ask what to log from CFSR register.", "Debug Ask.", "MemManage/BusFault/UsageFault bit meanings overview."),
    ],
}

MODULES.append(DRILLS)

CSS = """
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --surface2: #243044;
  --text: #e7ecf3;
  --muted: #9aa8bc;
  --accent: #3d9cf5;
  --accent2: #5eead4;
  --warn: #fbbf24;
  --ok: #4ade80;
  --border: #2d3a4f;
  --ex: #1e2a3d;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
}
a { color: var(--accent); }
.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  min-height: 100vh;
}
nav.sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1rem;
  overflow-y: auto;
  position: sticky;
  top: 0;
  height: 100vh;
}
nav.sidebar h1 {
  font-size: 1.05rem;
  margin: 0 0 0.25rem;
  line-height: 1.3;
}
nav.sidebar .sub {
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 1rem;
}
nav.sidebar input {
  width: 100%;
  padding: 0.45rem 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  margin-bottom: 0.75rem;
}
nav.sidebar ul { list-style: none; padding: 0; margin: 0; }
nav.sidebar li { margin-bottom: 0.15rem; }
nav.sidebar button.module-link {
  width: 100%;
  text-align: left;
  background: transparent;
  border: none;
  color: var(--text);
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
}
nav.sidebar button.module-link:hover { background: var(--surface2); }
nav.sidebar button.module-link.active {
  background: var(--accent);
  color: #061018;
  font-weight: 600;
}
nav.sidebar .level {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  margin-top: 0.75rem;
  margin-bottom: 0.25rem;
}
.progress-wrap {
  margin: 1rem 0;
  font-size: 0.75rem;
  color: var(--muted);
}
.progress-bar {
  height: 6px;
  background: var(--bg);
  border-radius: 99px;
  overflow: hidden;
  margin-top: 0.35rem;
}
.progress-bar > div {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  width: 0%;
  transition: width 0.3s ease;
}
main {
  padding: 1.5rem 2rem 4rem;
  max-width: 920px;
}
.hero {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}
.hero h2 { margin: 0 0 0.5rem; font-size: 1.75rem; }
.hero p { color: var(--muted); margin: 0; }
.badge {
  display: inline-block;
  font-size: 0.7rem;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  background: var(--surface2);
  color: var(--accent2);
  margin-right: 0.35rem;
}
.lesson h3 { margin-top: 1.5rem; color: var(--accent2); }
.lesson h4 { margin-top: 1rem; }
.lesson pre.code-block {
  background: #0a0e14;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  overflow-x: auto;
  font-size: 0.82rem;
}
.lesson code {
  background: var(--surface2);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
  font-size: 0.88em;
}
.exercise {
  background: var(--ex);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 8px;
  padding: 1rem 1.1rem;
  margin: 1.25rem 0;
}
.exercise header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.exercise h5 {
  margin: 0;
  font-size: 0.95rem;
}
.exercise .ex-id {
  font-size: 0.72rem;
  color: var(--muted);
  font-family: ui-monospace, monospace;
}
.exercise .prompt { margin: 0.75rem 0; }
.exercise .hint {
  font-size: 0.85rem;
  color: var(--muted);
  border-top: 1px dashed var(--border);
  padding-top: 0.65rem;
  margin-top: 0.65rem;
}
.exercise .actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.75rem;
}
button.btn {
  border: none;
  border-radius: 6px;
  padding: 0.45rem 0.85rem;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
}
button.btn-primary { background: var(--accent); color: #061018; }
button.btn-ghost { background: var(--surface2); color: var(--text); }
button.btn-ok { background: #166534; color: #ecfdf5; }
.exercise.done { border-left-color: var(--ok); opacity: 0.92; }
.solution {
  display: none;
  margin-top: 0.85rem;
  padding: 0.85rem;
  background: #0a0e14;
  border-radius: 6px;
  border: 1px solid var(--border);
  white-space: pre-wrap;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 0.8rem;
}
.solution.visible { display: block; }
.stretch {
  margin-top: 0.5rem;
  font-size: 0.82rem;
  color: var(--warn);
}
@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  nav.sidebar { position: relative; height: auto; }
}
"""

JS = r"""
const STORAGE_KEY = 'cursor-dsp-course-progress-v1';

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); }
  catch { return {}; }
}
function saveProgress(p) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
}

function countExercises(modules) {
  return modules.reduce((n, m) => n + (m.exercises?.length || 0), 0);
}

function renderModuleList(modules, activeId, filter) {
  const ul = document.getElementById('module-list');
  ul.innerHTML = '';
  const q = (filter || '').toLowerCase();
  modules.forEach(m => {
    const hay = (m.title + ' ' + m.summary + ' ' + m.level).toLowerCase();
    if (q && !hay.includes(q)) return;
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.className = 'module-link' + (m.id === activeId ? ' active' : '');
    btn.textContent = m.id === 'drills' ? '⚡ ' + m.title : m.id + ' · ' + m.title;
    btn.onclick = () => showModule(m.id);
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

function showModule(id) {
  const m = COURSE.modules.find(x => x.id === id) || COURSE.modules[0];
  history.replaceState(null, '', '#' + m.id);
  document.getElementById('module-title').textContent = m.title;
  document.getElementById('module-meta').innerHTML =
    `<span class="badge">${m.level}</span><span class="badge">Module ${m.id}</span>`;
  document.getElementById('module-summary').textContent = m.summary;
  document.getElementById('lesson-body').innerHTML = m.body;

  const exRoot = document.getElementById('exercises');
  exRoot.innerHTML = '';
  const progress = loadProgress();

  (m.exercises || []).forEach(ex => {
    const done = progress[ex.id];
    const el = document.createElement('article');
    el.className = 'exercise' + (done ? ' done' : '');
    el.dataset.exId = ex.id;

    el.innerHTML = `
      <header>
        <h5>Exercise</h5>
        <span class="ex-id">${ex.id}</span>
      </header>
      <p class="prompt">${escapeHtml(ex.prompt)}</p>
      ${ex.hints ? `<div class="hint"><strong>Hint:</strong> ${escapeHtml(ex.hints)}</div>` : ''}
      ${ex.stretch ? `<div class="stretch"><strong>Stretch:</strong> ${escapeHtml(ex.stretch)}</div>` : ''}
      <div class="actions">
        <button type="button" class="btn btn-primary btn-solution">Reveal solution</button>
        <button type="button" class="btn btn-ghost btn-hide">Hide solution</button>
        <button type="button" class="btn btn-ok btn-done">${done ? '✓ Completed' : 'Mark complete'}</button>
      </div>
      <div class="solution" role="region" aria-label="Solution">${escapeHtml(ex.solution)}</div>
    `;

    el.querySelector('.btn-solution').onclick = () => {
      el.querySelector('.solution').classList.add('visible');
    };
    el.querySelector('.btn-hide').onclick = () => {
      el.querySelector('.solution').classList.remove('visible');
    };
    el.querySelector('.btn-done').onclick = (ev) => {
      progress[ex.id] = true;
      saveProgress(progress);
      el.classList.add('done');
      ev.target.textContent = '✓ Completed';
      updateProgressBar();
    };

    exRoot.appendChild(el);
  });

  renderModuleList(COURSE.modules, m.id, document.getElementById('search').value);
  document.getElementById('exercise-count').textContent =
    (m.exercises || []).length + ' exercises in this module';
  updateProgressBar();
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function updateProgressBar() {
  const total = countExercises(COURSE.modules);
  const progress = loadProgress();
  const done = Object.keys(progress).filter(k => progress[k]).length;
  const pct = total ? Math.round((done / total) * 100) : 0;
  document.getElementById('progress-label').textContent = `${done} / ${total} exercises (${pct}%)`;
  document.getElementById('progress-fill').style.width = pct + '%';
}

function init() {
  const data = window.COURSE_DATA;
  window.COURSE = data;
  document.getElementById('course-title').textContent = data.title;
  document.getElementById('course-sub').textContent = data.subtitle;

  document.getElementById('search').oninput = (e) => {
    const id = (location.hash || '#00').slice(1);
    renderModuleList(COURSE.modules, id, e.target.value);
  };

  const startId = (location.hash || '#00').replace('#', '');
  showModule(COURSE.modules.some(m => m.id === startId) ? startId : '00');
  window.onhashchange = () => {
    const id = (location.hash || '#00').slice(1);
    if (COURSE.modules.some(m => m.id === id)) showModule(id);
  };
}

document.addEventListener('DOMContentLoaded', init);
"""


def build_html() -> str:
    data = {
        "title": "Cursor Zero to Hero for Embedded DSP Engineers",
        "subtitle": "C / C++ · Python · Firmware · Agent · Git · MCP · Skills · Hooks · Cloud · Automations",
        "version": "2026.08",
        "modules": MODULES,
    }
    total_ex = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(data, ensure_ascii=False)
    data_json = data_json.replace("</", "<\\/")  # avoid breaking script tag

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Cursor Zero to Hero — Embedded DSP Engineers</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="layout">
    <nav class="sidebar" aria-label="Course navigation">
      <h1 id="course-title">Loading…</h1>
      <p class="sub" id="course-sub"></p>
      <div class="progress-wrap">
        <span id="progress-label">0 / 0 exercises</span>
        <div class="progress-bar"><div id="progress-fill"></div></div>
      </div>
      <input type="search" id="search" placeholder="Filter modules…" aria-label="Filter modules" />
      <p class="level">Modules</p>
      <ul id="module-list"></ul>
    </nav>
    <main>
      <section class="hero">
        <h2 id="module-title">Welcome</h2>
        <div id="module-meta"></div>
        <p id="module-summary" style="margin-top:0.75rem;color:var(--muted);"></p>
        <p style="font-size:0.85rem;color:var(--muted);margin-top:1rem;">
          Open this file in any browser. Progress saves locally. Work in a real <code>dsp-sandbox</code> repo alongside the course.
          <strong>{total_ex} exercises</strong> · scratch → expert · embedded DSP context.
        </p>
      </section>
      <section class="lesson" id="lesson-body"></section>
      <section>
        <h3 style="color:var(--accent2);">Exercises</h3>
        <p id="exercise-count" style="color:var(--muted);font-size:0.9rem;"></p>
        <div id="exercises"></div>
      </section>
    </main>
  </div>
  <script>
    window.COURSE_DATA = {data_json};
  </script>
  <script>{JS}</script>
</body>
</html>
"""


if __name__ == "__main__":
    html_out = build_html()
    OUT.write_text(html_out, encoding="utf-8")
    n_mod = len(MODULES)
    n_ex = sum(len(m.get("exercises", [])) for m in MODULES)
    print(f"Wrote {OUT} — {n_mod} modules, {n_ex} exercises")
