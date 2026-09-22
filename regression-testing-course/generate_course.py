#!/usr/bin/env python3
"""Generate index.html — Regression Testing: Theory & Practice.
Concept-heavy course with practical setup exercises in Python, C, C++, MATLAB."""
from __future__ import annotations

import html as H
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"


def ex(n, prompt, hints, solution, stretch=""):
    return {"id": n, "prompt": prompt, "hints": hints, "solution": solution, "stretch": stretch}


def md(text):
    lines = text.strip().split("\n")
    out = []
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
                out.append(f'<pre class="code-block" data-lang="{H.escape(lang)}"><code>')
                in_pre = True
            continue
        if in_pre:
            out.append(H.escape(line))
            continue
        if line.startswith("## "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{H.escape(line[3:])}</h3>")
        elif line.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h4>{H.escape(line[4:])}</h4>")
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


def inline_md(s):
    s = H.escape(s)
    parts = s.split("`")
    for i in range(1, len(parts), 2):
        parts[i] = f"<code>{parts[i]}</code>"
    return "".join(parts)


# ═══════════════════════════════════════════════════════════════════════
# MODULES
# ═══════════════════════════════════════════════════════════════════════

MODULES = [
    # ────────────────────── PHASE 1: FOUNDATIONS ──────────────────────
    {
        "id": "00",
        "title": "How to Use This Course",
        "level": "Setup",
        "summary": "Course framing, language pragmatism, and a minimal toolbox for the exercises.",
        "body": md("""
## Who this course is for
Anyone who writes software they will still be maintaining next month. You do NOT need prior testing experience. If you have ever changed code and worried you might have broken something, this course is for you.

## What you will actually learn
- What a regression test is (from absolute scratch)
- Why regression tests exist and what they prevent
- The typical categories: bug-fix, refactor, numerical, performance, API
- How to write regression tests in Python, C, C++, and MATLAB
- How to integrate them into CI and how to bisect regressions when they happen

## Language philosophy
This course is language-pragmatic. When something is easiest in Python (setup, quick demos), we use Python. When we talk about embedded DSP goldens, we use C. When it is a numerical example, we may use MATLAB. Use the tool that lets you learn the concept fastest.

## Minimal toolbox
- Python 3.10+ with `pytest` and `numpy` (fastest to set up)
- A C compiler (gcc or clang) — for embedded / DSP examples
- MATLAB (optional) — for numerical examples where it is clearer
- A C++ compiler with Catch2 or doctest (optional) — for the C++ module
- Git — for the bisect module

## Setup one-liners
```bash
python -m pip install --user pytest numpy
gcc --version
git --version
```

## What a "module" looks like here
Each module has: a concept discussion (the theory), followed by exercises. Exercises are designed to make the concept stick, not to be busywork. Reveal solutions only after you have tried.
"""),
        "exercises": [
            ex(
                "00-1",
                "Install pytest and numpy. Verify with: `python -c 'import pytest, numpy; print(pytest.__version__, numpy.__version__)'`",
                "Use pip: `python -m pip install --user pytest numpy`.",
                "You see two version strings printed. You are ready for the practical modules.",
            ),
            ex(
                "00-2",
                "Create a folder `regression-lab/` with subfolders `python/`, `c/`, `matlab/`, `cpp/`, `goldens/`. This is where every exercise's code will live.",
                "Just `mkdir -p regression-lab/{python,c,matlab,cpp,goldens}` on Unix, or the PowerShell equivalent.",
                "You have a clean lab directory ready. Every exercise from here on writes files into one of these subfolders.",
            ),
            ex(
                "00-3",
                "In your own words (2-3 sentences) write what you currently think a regression test is. Save to `regression-lab/before-and-after.md` under a heading `Before the course`. We will revisit this in the capstone.",
                "There are no wrong answers here — this is a baseline.",
                "You wrote your current understanding. This is intentional: at the end of the course you write again under `After the course` and compare. This is how you know you learned something concrete.",
            ),
        ],
    },
    {
        "id": "01",
        "title": "What Is a Regression Test? (Absolute Scratch)",
        "level": "Beginner",
        "summary": "Start with zero assumptions: what the words mean, what the test does, and what a 'regression' actually is.",
        "body": md("""
## Break the name apart
- **Regression**: something that used to work, no longer works. A step backward.
- **Test**: a piece of code that verifies another piece of code behaves as expected.
- **Regression test**: a test whose purpose is to catch a regression — that is, to make sure something that used to work still works.

That is the entire definition. Everything else in this course is elaboration.

## The simplest possible example
You have a function:
```python
def add(a, b):
    return a + b
```
You write a test:
```python
def test_add_positive():
    assert add(2, 3) == 5
```
Someone later "optimizes" `add` and breaks it:
```python
def add(a, b):
    return a - b   # oops
```
You run the test suite. The test fails. The regression is caught **before** it hits production. That is regression testing in one screen.

## The key phrase: "used to work"
A regression test is written because you already know how the code SHOULD behave. Either:
- The behavior is a specification (documented contract)
- The behavior was observed and recorded (a "golden" reference)
- The behavior fixed a specific bug (bug-fix regression)

If nobody knows what the correct behavior is, no test — regression or otherwise — can help you.

## Regression tests vs "just tests"
In practice, most tests you write ARE regression tests. The distinction is one of **intent**:
- Any test written **after** the correct behavior is established acts as a regression guard.
- The label "regression test" often specifically means a test that was written **because** something broke and we want it to stay fixed.

For this course, we treat every test with a preservation intent as a regression test.

## What a regression test does NOT do
- It does not prove code is correct (only that specific cases still behave as expected)
- It does not find new bugs (it catches re-introduction of known bugs)
- It does not replace design or code review
- It does not tell you WHY something broke — only THAT something broke
"""),
        "exercises": [
            ex(
                "01-1",
                "Write the definition of 'regression test' from memory, in one sentence. Then compare to the module text. What did you leave out?",
                "Focus on the word 'regression' — going backward.",
                "A good sentence: 'A test that verifies previously-working behavior still works.' If you missed 'previously-working' you missed the whole point of the name.",
            ),
            ex(
                "01-2",
                "Given these three scenarios, mark each as regression / not-a-regression:\n(a) A new feature is added and does not work.\n(b) A fix to bug #42 was released last year, and now bug #42 is back.\n(c) The team decided the API should return `-1` instead of `null`, and the old test now fails.",
                "Which one involves behavior that USED to work and no longer does?",
                "(a) Not a regression — the feature never worked, it is just incomplete.\n(b) Regression — bug #42 was fixed, its return is the definition of regression.\n(c) Not a regression — behavior changed on purpose. The failing test needs to be updated, not the code.",
            ),
            ex(
                "01-3",
                "In `regression-lab/python/`, create `calc.py` with the buggy `add` from the module (`return a - b`). Then create `test_calc.py` with `def test_add(): assert calc.add(2, 3) == 5`. Run `pytest`. Observe the failure. Fix `calc.py`. Rerun. Observe the pass.",
                "This is the whole workflow in miniature: test → fail → fix → pass.",
                "The failing run tells you exactly what broke (expected 5, got -1). After fix, it passes. You just ran your first regression cycle end to end.",
            ),
            ex(
                "01-4",
                "Explain to yourself out loud (or write down): if the `add` function had NO test, and the buggy version was pushed, who would find the bug and when? Compare to how the test found it.",
                "Think about the cost gradient: local dev → CI → QA → production.",
                "Without the test, the bug reaches at least CI (if any downstream code fails), likely QA (if noticed), possibly production (if not noticed). With the test, it dies on the developer's laptop in seconds. Cost difference: seconds vs weeks.",
            ),
        ],
    },
    {
        "id": "02",
        "title": "Why Regression Tests Are Needed",
        "level": "Beginner",
        "summary": "The economic and human case for regression testing. Real-world consequences when it is absent.",
        "body": md("""
## The three unavoidable truths of software
1. **Software rots.** Not physically — but the environment around it changes (dependencies, OS, compilers, hardware) and unmaintained code stops working.
2. **Humans forget.** The developer who fixed bug #42 last year does not remember the details. The next developer touching that code has no idea the bug ever existed.
3. **Every change is risk.** Even a "trivial" one-line change can break something distant.

Regression tests exist because of these three truths. They are the institutional memory of "what should still work."

## The cost gradient
Where a bug is found determines its cost. A rule of thumb from industry studies:
| Where found | Relative cost |
|---|---|
| Developer's laptop | 1x |
| Code review / CI | 5x |
| QA / staging | 20x |
| Production (internal user) | 100x |
| Production (customer / field) | 1000x+ |

A regression test moves bug detection all the way to the leftmost column.

## Real-world stories
- **Ariane 5, 1996**: a floating-point conversion overflow (that had been guarded against on Ariane 4) was reused without regression testing on Ariane 5's different flight profile. Result: rocket destroyed at 40 seconds. Cost: $370M+.
- **Toyota unintended acceleration (2000s-2010s)**: throttle control regressions across firmware versions. Fatal outcomes. Massive recalls. Later: mandatory regression suites for automotive ECUs.
- **Knight Capital, 2012**: a code deployment reused an old flag with new meaning. No regression suite caught the mismatch. Result: $440M loss in 45 minutes. Company effectively destroyed.
- **Any embedded product recall**: nearly all firmware recalls trace to a regression that a test would have caught.

## The developer's daily case
Even if you never work on rockets or trading systems:
- **Refactor confidence**: a good regression suite lets you rewrite entire modules without fear.
- **Onboarding**: new team members learn the code by reading tests.
- **Documentation that cannot lie**: tests describe actual behavior, not aspirations.
- **Sleep**: knowing CI protects you means you can push on a Friday.

## The counterargument (and why it fails)
"We do not need tests, we have good developers."
- Good developers still forget things they wrote a year ago.
- Good developers still work with other developers who did not write the code.
- Good developers still work under deadline pressure and miss things.
- Regression tests are not a substitute for skill — they are a scaffolding that lets skilled people move faster with less fear.
"""),
        "exercises": [
            ex(
                "02-1",
                "Pick a project you have worked on. List 3 changes (from real memory) that COULD have caused regressions. For each, note: (a) was there a test that would have caught it? (b) how was the regression (if any) actually found?",
                "This is a personal audit — write in `regression-lab/audit.md`.",
                "Common pattern: 'refactored the DSP loop, broke fixed-point saturation on edge case, found by QA on device.' If a regression test on saturation edge cases existed, it would have caught the issue in minutes.",
            ),
            ex(
                "02-2",
                "For a hypothetical bug found on a customer device: estimate the total cost (developer time to reproduce, QA time to verify, engineering time to hotfix, support time for calls, reputation cost). Compare to the cost of writing one regression test.",
                "Even conservative estimates make the case obvious.",
                "Customer-found bug: easily 40+ engineer hours + support cost + reputation. Regression test: 15 minutes to write. The ROI is 100x or more for even a single caught regression.",
            ),
            ex(
                "02-3",
                "Read the summary of one of: Ariane 5, Toyota UA, or Knight Capital. In one paragraph, describe what regression test would have caught the issue.",
                "Any Wikipedia summary is enough.",
                "Example (Ariane 5): 'A test running the Ariane 5 flight profile through the reused inertial code would have triggered the overflow on the ground.' The absence of a targeted regression suite is the direct root cause.",
            ),
        ],
    },
    {
        "id": "03",
        "title": "Tests vs Assertions vs Unit vs Integration vs Regression",
        "level": "Beginner",
        "summary": "The vocabulary is confusing. Here is the clean map so you know exactly what you are writing.",
        "body": md("""
## The vocabulary trap
People use these terms interchangeably. They should not. Here is the clean map.

## Assertion
A runtime check inside production code that a condition must hold.
```c
assert(buffer != NULL);
assert(n > 0 && n <= MAX_N);
```
- Fires during execution
- Aborts (or logs) on violation
- Purpose: catch impossible states
- NOT a test — it is a guard

## Unit test
A test of one small unit (function, class) in isolation, with no external dependencies.
```python
def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10
```
- Runs at test time (not production)
- Fast (milliseconds)
- Isolated (no I/O, no network, no other units)

## Integration test
A test of multiple units working together, possibly with real I/O.
```python
def test_pipeline_end_to_end():
    audio_in = load_wav("input.wav")
    processed = pipeline.process(audio_in)
    audio_out = save_and_reload(processed)
    assert audio_out.sample_rate == 48000
```
- Slower (may involve files, network, other processes)
- Broader coverage per test
- Harder to isolate the cause when they fail

## System / end-to-end test
The full product exercised from the outside as a user would use it.
- Slowest
- Most realistic
- Hardest to debug when they fail

## Regression test
A test — of any of the above kinds — whose PURPOSE is to prevent a specific regression.
- The category is defined by INTENT, not by mechanism.
- A unit test can be a regression test. An integration test can be a regression test.
- The tag "regression test" often specifically means: written after a bug was fixed, to guard the fix.

## The overlap diagram (in text)
```
[Assertions] --- run in production, catch impossible states
[Unit tests]     ─┐
[Integration]     ├── all can be REGRESSION tests, by intent
[System tests]   ─┘
```

## Why the distinction matters
When someone says "add regression tests for this fix," they usually mean:
- Write a unit test (fastest, cheapest, sufficient in most cases)
- That reproduces the specific bug
- With a name that makes the intent clear
- So the fix is guarded forever

They do not mean: build a full end-to-end system test. That is overkill for a single bug.
"""),
        "exercises": [
            ex(
                "03-1",
                "Categorize each as assertion / unit / integration / system:\n(a) `assert(ptr != NULL)` inside a driver function\n(b) A pytest that reads two files and compares their contents\n(c) A pytest that calls one function with 5 inputs and checks 5 outputs\n(d) A shell script that boots a device, sends audio, records output, and verifies SNR",
                "Think about scope and what is being exercised.",
                "(a) Assertion — runtime guard in prod code.\n(b) Integration — involves file I/O.\n(c) Unit — one function, no I/O.\n(d) System / end-to-end — full product exercised as a user.",
            ),
            ex(
                "03-2",
                "Take this assertion inside production code: `assert(gain >= 0.0f && gain <= 1.0f);`. Convert it into a proper unit test in `regression-lab/python/test_gain.py` that verifies a `set_gain(g)` function rejects out-of-range values.",
                "Assertion = guard. Unit test = external verification.",
                "```python\nimport pytest\nfrom audio import set_gain\n\ndef test_gain_accepts_valid():\n    set_gain(0.0); set_gain(0.5); set_gain(1.0)\n\ndef test_gain_rejects_negative():\n    with pytest.raises(ValueError):\n        set_gain(-0.1)\n\ndef test_gain_rejects_above_one():\n    with pytest.raises(ValueError):\n        set_gain(1.1)\n```",
            ),
            ex(
                "03-3",
                "You fix a bug where `add(1.0, 2.0)` returned 2.9999... instead of 3.0 due to a subtraction ordering issue. Write the regression test's DOCSTRING (just the docstring / comment) that captures: what bug it guards, when it was fixed, and where to find more info.",
                "Naming and comments make future maintainers understand WHY this test exists.",
                "```python\ndef test_add_returns_exact_when_both_integer_valued():\n    \"\"\"Regression for bug #123 (fixed 2026-09).\n    Prior implementation used (a - (-b)) which introduced\n    floating-point rounding for integer-valued inputs.\n    See docs/bugs/123-add-rounding.md for full analysis.\"\"\"\n    assert add(1.0, 2.0) == 3.0\n```\nWhy it matters: the future you (or a teammate) can immediately understand the intent without archaeology.",
            ),
        ],
    },
    {
        "id": "04",
        "title": "The Regression Test Lifecycle",
        "level": "Beginner",
        "summary": "Bug → red test → green code → guarded forever. And what to do when behavior legitimately changes.",
        "body": md("""
## The canonical lifecycle
```
1. Bug reported / discovered
2. Write a test that reproduces the bug (RED — it fails)
3. Fix the code (GREEN — the test passes)
4. Commit test + fix together
5. The test lives in the suite forever
6. Every CI run guards against the bug returning
```

## Why write the test BEFORE the fix
- **Proves the bug is real and reproducible** — you have not misunderstood the report
- **Proves the fix actually fixes it** — you saw the test go red, then green
- **Documents the failing case exactly** — the test IS the reproducer forever
- If you only write the fix, you might convince yourself it works when it does not

## Naming the regression test
Give it a name that a future engineer can decode without hunting:
```python
# Good — self-documenting
def test_biquad_no_denormal_when_input_zero_for_long_time():
def test_regression_issue_456_gain_reset_after_pause():
def test_bug_2026_09_uart_baud_rate_calculation():

# Bad — will be a mystery in six months
def test_biquad2():
def test_new_case():
def test_fix():
```

## What happens when behavior legitimately changes
Someday, someone will WANT to change the guarded behavior. Then:
1. The regression test will fail (correctly!)
2. The team must decide: is the change intentional? Is the OLD behavior still required somewhere?
3. If the change is intentional and no consumer depends on old behavior:
   - Update the test to reflect the new expectation
   - Document why in the commit message
   - Keep the test — it now guards the NEW behavior
4. If the change is a mistake or someone still depends on old behavior:
   - Revert the change
   - The test did its job — it caught an unintended regression

## The anti-pattern: deleting the test to make it pass
This is the single most common failure mode. Someone changes production code, the regression test fails, they DELETE the test to unblock the build. The bug returns silently a year later.

The rule: a red regression test is a **decision point**, not an obstacle. Either the code is wrong, or the behavior legitimately changed. In the second case, update the test — do not delete it without thought.

## When to actually delete a regression test
- The behavior is no longer relevant (module removed)
- The test was flaky and provided no value (fix the flakiness first — see Module 22)
- The scenario is now covered by a broader, better test (and you note this in the commit)

Deletion should always be a deliberate, documented choice.
"""),
        "exercises": [
            ex(
                "04-1",
                "Walk through the full lifecycle for a made-up bug. Write a short script (in `regression-lab/python/`):\n(1) buggy `divide(a, b)` that returns `a * b`\n(2) `test_divide.py` that expects `divide(10, 2) == 5` and fails\n(3) fix `divide` to be `a / b`\n(4) rerun — passes",
                "You are practicing RED → GREEN with your own hands.",
                "You saw the failure with `divide` returning 20 instead of 5. You fixed it. Rerun: passes. This is the shortest possible full lifecycle demo.",
            ),
            ex(
                "04-2",
                "You wrote `test_biquad2()` last year. Today you cannot remember what it protects. What is the RIGHT thing to do? What is the WRONG thing to do?",
                "There is a healthy answer and a lazy answer.",
                "Right: read the test carefully, git-blame the file to find the commit and PR, understand the intent, then RENAME the test to something descriptive (`test_biquad_stable_when_a2_is_negative` or similar). Wrong: delete it because you do not remember, or leave it named `biquad2` for the next person to face the same confusion.",
            ),
            ex(
                "04-3",
                "Someone changed the DC blocker's alpha default from 0.995 to 0.98. Your regression test that expected certain output for alpha=0.995 fails. Describe the three possible situations and the correct action for each.",
                "Situations differ in whether the change was intentional and whether other consumers depend on the old value.",
                "(A) Change was accidental → revert the code, test stays. (B) Change was intentional and nobody depends on old value → update the test's expected outputs and commit alongside the code change with an explanation. (C) Change was intentional but a consumer depends on the old value → make alpha configurable so both consumers are happy, keep the original test, add a new test for the new default.",
            ),
            ex(
                "04-4",
                "You inherit a repo with a test named `test_new_thing_from_meeting_thursday`. You have no idea what meeting. The test does something odd. What is your workflow to figure out whether to keep it, rename it, or delete it?",
                "Git blame + repo archaeology.",
                "1. `git log -p -- path/to/test_file` — find when this test was added. 2. Read the commit message and diff. 3. Look at the PR (if you have GitHub history). 4. Look for related issue numbers. 5. Talk to the original author if reachable. 6. Only after this: rename to something self-documenting or delete with a note. Never delete just because the name is bad.",
            ),
        ],
    },
    # ────────────────────── PHASE 2: CONCEPTS ──────────────────────
    {
        "id": "05",
        "title": "Test Anatomy: Arrange / Act / Assert",
        "level": "Intermediate",
        "summary": "Every good test has three phases. When you can see them clearly, tests become readable and fixable.",
        "body": md("""
## The three phases of every test
```
ARRANGE  — set up the world the code needs
ACT      — call the code under test
ASSERT   — verify the result
```
Also known in BDD as **Given / When / Then**. Same thing.

## In Python (pytest)
```python
def test_moving_average_smooths_step():
    # ARRANGE
    signal = [0.0]*10 + [1.0]*10
    window = 4

    # ACT
    result = moving_average(signal, window)

    # ASSERT
    assert result[9] < result[13] < result[15]
    assert abs(result[19] - 1.0) < 1e-6
```
Comments not required in practice, but the structure IS required.

## In C
```c
void test_saturate_high_clip(void) {
    // ARRANGE
    int32_t x = 1000000;
    int32_t max = 32767;

    // ACT
    int32_t y = saturate_i16(x, max);

    // ASSERT
    assert(y == max);
}
```

## Why AAA matters
When a test fails, you look at it and instantly know:
- **Setup problem?** — read the ARRANGE
- **Wrong result?** — the ACT is the one line to trace
- **Wrong expectation?** — the ASSERT is where to look

Mixed-up tests take minutes to diagnose. AAA tests take seconds.

## Anti-patterns to avoid
### The "kitchen sink" test
```python
def test_everything():
    setup_a(); assert cond_a()
    setup_b(); assert cond_b()
    setup_c(); assert cond_c()
    # 40 more lines
```
When it fails, you have no idea which of the 40 things broke.

### Multiple ACTs
```python
def test_confusing():
    x = compute(1)
    y = compute(2)
    z = compute(3)
    assert x + y + z == 6
```
Which `compute` call is wrong when the assert fails? Split into three tests.

### Assertions before the ACT
```python
def test_backwards():
    assert setup_step()  # this is really part of ARRANGE
    result = compute()
    assert result == expected
```
Confusing. Setup validation belongs in a fixture or explicit precondition, not mixed with test assertions.

## When one ACT is legitimately multi-step
Sometimes the "action" is a sequence:
```python
def test_pipeline_recovers_after_underrun():
    # ARRANGE
    pipe = Pipeline()

    # ACT (multi-step but ONE logical action)
    pipe.start()
    pipe.force_underrun()
    pipe.recover()

    # ASSERT
    assert pipe.status == "running"
```
This is fine. The three lines in ACT are all part of the one behavior being tested.
"""),
        "exercises": [
            ex(
                "05-1",
                "In `regression-lab/python/test_aaa.py`, write a test for a `clamp(x, lo, hi)` function following AAA. Use comments to mark each phase.",
                "Simple function, clear phases.",
                "```python\ndef test_clamp_returns_hi_when_x_above_range():\n    # ARRANGE\n    x, lo, hi = 100, 0, 10\n\n    # ACT\n    result = clamp(x, lo, hi)\n\n    # ASSERT\n    assert result == 10\n```",
            ),
            ex(
                "05-2",
                "Rewrite this messy test into AAA form (three separate tests):\n```python\ndef test_stuff():\n    a = f(1); b = f(2); c = f(3)\n    assert a == 1\n    assert b == 4\n    assert c == 9\n```",
                "Each assertion targets a different call — that means three tests, not one.",
                "```python\ndef test_f_returns_1_for_1():\n    assert f(1) == 1\n\ndef test_f_returns_4_for_2():\n    assert f(2) == 4\n\ndef test_f_returns_9_for_3():\n    assert f(3) == 9\n```\nBenefit: when `f(2)` breaks, only that test fails, and its name tells you exactly what broke.",
            ),
            ex(
                "05-3",
                "Look at a real test in a project you know. Can you identify the three phases without comments? If not, that is a signal — the test needs restructuring.",
                "Read for structure, not for correctness.",
                "Most legacy tests mix phases or skip ARRANGE (using globals). If you cannot see AAA at a glance, the test is a candidate for refactoring — even if it currently works.",
            ),
        ],
    },
    {
        "id": "06",
        "title": "Golden Values, Golden Vectors, Snapshots",
        "level": "Intermediate",
        "summary": "How to test code whose 'correct answer' is a long array, a file, or a complex data structure.",
        "body": md("""
## The problem
Some functions return a single number:
```python
assert add(2, 3) == 5
```
Easy. But others return a 1024-sample array, a filtered image, or a serialized config file. You cannot inline the expected value in the test — it is too big.

## The solution: goldens
Store the "known correct" output in a file (called a **golden** file, **snapshot**, or **fixture**). The test compares the current output to the golden.
```
signal_in.bin  →  process()  →  actual_out.bin
                                       ↓ compare
                              golden_out.bin
```

## Three golden formats
### Inline (small)
```python
def test_fir_impulse():
    coeffs = [0.25, 0.5, 0.25]
    impulse = [1.0] + [0.0]*10
    expected = [0.25, 0.5, 0.25] + [0.0]*8
    assert_allclose(fir(coeffs, impulse), expected, atol=1e-6)
```
For small vectors (< ~20 elements), just write them inline.

### File-based (large numerical)
```python
def test_fir_1024_sine():
    signal = np.fromfile("goldens/sine_1k.bin", dtype=np.float32)
    expected = np.fromfile("goldens/fir_sine_1k_out.bin", dtype=np.float32)
    actual = fir(coeffs, signal)
    np.testing.assert_allclose(actual, expected, atol=1e-6)
```
Golden files live in the repo. Version-controlled. Documented in a README.

### Snapshot (structured / text)
```python
def test_config_dump():
    cfg = build_config()
    snapshot = json.dumps(cfg, indent=2, sort_keys=True)
    expected = Path("goldens/config_snapshot.json").read_text()
    assert snapshot == expected
```
For text-friendly outputs, plain string comparison works. Tools like `pytest-snapshot` or `syrupy` automate this.

## Generating goldens: one script, one command
```python
# goldens/gen_fir_sine.py
import numpy as np
from myproject.fir import fir, DEFAULT_COEFFS

sine = np.sin(2*np.pi*1000*np.arange(1024)/48000).astype(np.float32)
sine.tofile("goldens/sine_1k.bin")
out = fir(DEFAULT_COEFFS, sine)
out.tofile("goldens/fir_sine_1k_out.bin")
print("Regenerated FIR goldens")
```
Run this ONCE when the golden should be created or intentionally updated.

## The golden update workflow
1. You intentionally change algorithm behavior
2. Regression test fails (correctly — the golden no longer matches)
3. You inspect the diff between old and new output. Is the change correct?
4. If yes: rerun the golden generator, commit the new golden alongside the code change
5. Reviewer sees BOTH the code change and the golden change in one PR — they can verify the intent

**Never** update a golden just to "make the test pass." Always inspect the diff first.

## Storing goldens
- Small text/JSON goldens: commit directly to the repo
- Large binary goldens: commit if reasonable (< 1 MB each); use Git LFS if larger
- Every goldens folder needs a `README.md`: how to regenerate, what each file represents
- Do NOT put goldens in the same folder as source code — use `tests/goldens/` or `goldens/`

## Golden anti-patterns
- **Regenerating goldens without inspection** — defeats the purpose
- **Goldens with random data** — cannot re-verify manually; use deterministic inputs
- **Goldens without a generator script** — nobody can reproduce or update them
- **Version-controlled goldens that keep changing** — the underlying code is nondeterministic and needs fixing first
"""),
        "exercises": [
            ex(
                "06-1",
                "In `regression-lab/goldens/`, write `gen_moving_avg_golden.py`. It should: generate a 100-sample step signal, apply a 5-point moving average, save both input and output as `.npy` files. Run it.",
                "Use numpy: `np.save('step_in.npy', signal)` and `np.save('step_out.npy', filtered)`.",
                "```python\nimport numpy as np\n\ndef moving_avg(x, w):\n    return np.convolve(x, np.ones(w)/w, mode='same')\n\nstep = np.concatenate([np.zeros(50), np.ones(50)]).astype(np.float32)\nnp.save('step_in.npy', step)\nnp.save('step_out.npy', moving_avg(step, 5).astype(np.float32))\nprint('Regenerated moving-avg goldens')\n```",
            ),
            ex(
                "06-2",
                "Write `test_moving_avg.py` that loads both files, runs your implementation, and asserts `np.allclose` with `atol=1e-6`. Verify it passes.",
                "The golden is the ground truth here.",
                "```python\nimport numpy as np\nfrom moving_avg import moving_avg  # your implementation\n\ndef test_moving_avg_against_golden():\n    x = np.load('goldens/step_in.npy')\n    expected = np.load('goldens/step_out.npy')\n    actual = moving_avg(x, 5)\n    np.testing.assert_allclose(actual, expected, atol=1e-6)\n```",
            ),
            ex(
                "06-3",
                "Change your `moving_avg` implementation slightly (e.g., use window=6 instead of 5). Run the test — it should fail. Inspect the diff (print `actual - expected`). Now: is this failure real, or should the golden be updated?",
                "Practice reading the diff before deciding.",
                "It should fail because you changed the behavior. You should NOT regenerate the golden — you should revert your change (or, if the change was intentional, regenerate AND commit the reasoning). This is the golden update discipline.",
            ),
            ex(
                "06-4",
                "Write a `regression-lab/goldens/README.md`: what each file is, what generator produces it, when to regenerate. This is the golden hygiene doc your future self will thank you for.",
                "Every goldens folder needs one.",
                "The README should list: file names, dtype/shape, generating script, invariants (e.g., 'sample rate always 48000'), and the update procedure. Without this, in six months no one will know what these binaries mean.",
            ),
        ],
    },
    {
        "id": "07",
        "title": "Tolerances and Numerical Comparisons",
        "level": "Intermediate",
        "summary": "Floats do not equal floats. Choose absolute, relative, or ULP tolerances deliberately.",
        "body": md("""
## Why `assert a == b` fails for floats
```python
>>> 0.1 + 0.2 == 0.3
False
>>> 0.1 + 0.2
0.30000000000000004
```
Floats are approximations. Equality comparison is almost always wrong for computed floating-point values.

## The three tolerance strategies
### Absolute tolerance (atol)
"Values must be within X of each other."
```python
assert abs(actual - expected) < 1e-6
np.testing.assert_allclose(actual, expected, atol=1e-6)
```
Good when: values are in a known range (e.g., signal amplitudes in [-1, 1]).
Bad when: values span many orders of magnitude — 1e-6 is huge if the value is 1e-10.

### Relative tolerance (rtol)
"Values must agree to X percent."
```python
assert abs(actual - expected) / abs(expected) < 1e-6
np.testing.assert_allclose(actual, expected, rtol=1e-6)
```
Good when: values span a wide range.
Bad when: expected is zero (divide by zero) — always combine with atol as a floor.

### ULP-based (units in last place)
"Values must be within N floating-point steps of each other."
```python
import math
math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
```
Or with `numpy.testing.assert_array_almost_equal_nulp`. Most precise, most nuanced. Use when doing serious numerical work where you understand FP internals.

## The safe default
```python
np.testing.assert_allclose(actual, expected, rtol=1e-6, atol=1e-9)
```
Combines both. Handles the zero-crossing case (atol floor) and wide-range values (rtol scaling).

## Choosing tolerances for embedded DSP
- **Float32 vs float64 reference**: expect ~1e-7 relative error at best (float32 has ~7 decimal digits of precision)
- **Fixed-point (Q15)**: expect ~1 LSB error, tolerance ≈ 1 / 32768 ≈ 3e-5
- **After long IIR filters**: accumulated error can be much larger; measure it explicitly
- **After FFT round-trip**: tolerance scales with N and the input dynamic range

Rule of thumb: measure the actual error once, then set the tolerance a bit above that. Do not guess.

## Special values
```python
import math
assert math.isnan(result)  # NaN != NaN, so == does not work
assert math.isinf(result)
assert result == 0.0 and math.copysign(1.0, result) == 1.0  # positive zero
```
NaN comparisons in particular are a common bug: `nan == nan` is False.

## Comparing entire arrays
```python
import numpy as np
np.testing.assert_allclose(a, b, rtol=1e-6, atol=1e-9)
```
Prints exactly which elements differ and by how much. Much better than `assert (a == b).all()`.

## When the tolerance drifts
If you find yourself LOOSENING tolerances to make tests pass, stop. Options:
1. The reference is wrong (fix it)
2. The code has genuine numerical error you did not expect (fix that)
3. The test was too optimistic (loosen — but only after understanding why)

Never loosen "because the test was flaky." Numerics do not fluctuate. Flakiness means nondeterminism (Module 08), not floating-point.
"""),
        "exercises": [
            ex(
                "07-1",
                "Run in Python: `0.1 + 0.2 == 0.3`. Then use `math.isclose(0.1 + 0.2, 0.3)`. Explain the difference in your own words.",
                "This is the classic gotcha.",
                "`==` returns False because 0.1 and 0.2 have no exact binary representation. `math.isclose` uses a default relative tolerance of 1e-9 and returns True. Every floating-point comparison in tests should use `isclose` or `allclose`, not `==`.",
            ),
            ex(
                "07-2",
                "Choose an appropriate tolerance for each scenario. Justify:\n(a) Two float32 arrays that came from the same algorithm run twice with the same inputs\n(b) A float64 reference vs a float32 implementation of the same algorithm\n(c) A Q15 fixed-point implementation vs a float reference",
                "Think about where the error comes from.",
                "(a) Should be bit-exact (rtol=0, atol=0) if truly deterministic. If not exact, the algorithm is nondeterministic — that is a bug.\n(b) rtol≈1e-7, atol≈1e-9. Float32 has ~7 digits precision.\n(c) atol≈1/32768 ≈ 3e-5. One LSB is the fundamental quantization step in Q15.",
            ),
            ex(
                "07-3",
                "Write `regression-lab/python/test_tolerances.py`. Test that `np.sin(np.pi)` is close to 0 with atol=1e-15 (should fail — off by ~1.2e-16) and with atol=1e-14 (should pass). This teaches you what tolerance actually LOOKS like.",
                "`np.sin(np.pi)` is not exactly zero because `np.pi` is not exactly π.",
                "```python\nimport numpy as np\n\ndef test_sin_pi_close_to_zero():\n    assert abs(np.sin(np.pi)) < 1e-14  # passes\n    # assert abs(np.sin(np.pi)) < 1e-15  # would fail: ~1.22e-16\n```\nLesson: pick tolerances by measurement, not by wishful thinking.",
            ),
            ex(
                "07-4",
                "You are testing an IIR filter output. You run the test three times on the same inputs and get results that differ by 1e-12. Should you loosen tolerance to 1e-11? Justify.",
                "Deterministic code should be bit-exact between runs.",
                "No. Deterministic floating-point code produces bit-identical results across runs on the same machine. If you see differences, the code is nondeterministic (parallelism, uninitialized memory, non-associative order) — that is a real bug. Fix the nondeterminism, then set tolerance based on the algorithm vs reference, not the algorithm vs itself.",
            ),
        ],
    },
    {
        "id": "08",
        "title": "Test Isolation and Determinism",
        "level": "Intermediate",
        "summary": "A test must give the same answer every time. If it does not, it is not a test — it is a lottery.",
        "body": md("""
## The two requirements
1. **Isolated** — a test does not depend on any other test running before or after it.
2. **Deterministic** — a test gives the same result every time it runs, in isolation and in a suite, on any machine.

Violate either, and your suite becomes untrustworthy. Untrustworthy suites get ignored ("just rerun it"). Ignored suites do not catch regressions.

## Common sources of nondeterminism
### Time
```python
def test_bad():
    result = compute_with_timestamp()
    assert result.timestamp == "2026-01-01T00:00:00Z"  # fails at 00:00:01
```
Fix: freeze time with `freezegun`, mock `datetime.now()`, or inject clock as a dependency.

### Randomness
```python
def test_bad():
    x = random.random()
    y = process(x)
    assert y > 0.5  # passes sometimes
```
Fix: `random.seed(42)` at the start of the test, or make the function take the random source as an argument.

### Environment variables / files / network
```python
def test_bad():
    config = load_config()  # reads /etc/app.conf
    assert config.mode == "prod"  # depends on the machine
```
Fix: pass config path explicitly, use tmp directories, mock network.

### Order dependence
```python
GLOBAL_STATE = []

def test_a():
    GLOBAL_STATE.append("a")
    assert len(GLOBAL_STATE) == 1  # fails if test_b ran first

def test_b():
    GLOBAL_STATE.append("b")
    assert len(GLOBAL_STATE) == 1  # fails if test_a ran first
```
Fix: no globals in tests. Reset state in setup/teardown. Or better: no globals in the code either.

### Parallelism and shared resources
Two tests writing to the same file, port, or database concurrently. Fix: use `tmp_path` fixture (pytest), unique ports, per-test databases.

### Uninitialized memory (C)
```c
int buffer[100];  // uninitialized
process(buffer);  // reads garbage — different each run
```
Fix: always initialize. Use `memset` or `= {0}`.

## The pytest way (Python)
Pytest provides fixtures that give isolation for free:
- `tmp_path` — a unique temp directory per test
- `monkeypatch` — safely modify env vars, restored after test
- `capsys` — capture stdout/stderr per test

```python
def test_reads_from_isolated_temp(tmp_path):
    (tmp_path / "input.txt").write_text("hello")
    result = read_file(tmp_path / "input.txt")
    assert result == "hello"
```
No cleanup needed. No collision with other tests. Reproducible.

## The gold-standard property
> If you run any single test in isolation, it should give the same result as running it inside the full suite. In any order. On any machine. Every time.

If this is not true, the test is broken — even if it currently passes.

## Detecting flakiness
Run your suite N times. If any test's pass/fail changes, it is flaky.
```bash
for i in {1..20}; do pytest -q; done
```
Or use `pytest-randomly` to randomize order and shake out order-dependent tests.
"""),
        "exercises": [
            ex(
                "08-1",
                "In `regression-lab/python/test_flaky.py`, write a test that uses `random.random()` and asserts something like `assert random.random() > 0.5`. Run it 10 times with `pytest test_flaky.py`. Observe the flakiness. Then fix it with `random.seed(42)`. Run 10 times — passes deterministically.",
                "Feel the pain of nondeterminism firsthand.",
                "Before fix: passes ~half the time. After `random.seed(42)` at test start: deterministic (either always passes or always fails, based on the seeded value). Either outcome is better than 'sometimes.'",
            ),
            ex(
                "08-2",
                "Write two tests using a shared list `GLOBAL = []`. Each appends to it and asserts `len(GLOBAL) == 1`. Run them. Observe order-dependent failure. Fix using per-test state or a fixture.",
                "Shared mutable state = order-dependent bugs.",
                "The second test always fails because it sees length 2. Fix: use `@pytest.fixture` that returns a fresh list, or use `def setup_method(self)` in a test class. Rule: tests never share mutable state.",
            ),
            ex(
                "08-3",
                "Use pytest's `tmp_path` fixture. Write a test that writes a file to `tmp_path`, reads it back, and asserts contents match. Verify by running it twice — each run gets a fresh temp dir.",
                "`tmp_path` is a pathlib.Path unique per test.",
                "```python\ndef test_read_write_roundtrip(tmp_path):\n    p = tmp_path / \"data.txt\"\n    p.write_text(\"hello\")\n    assert p.read_text() == \"hello\"\n```\nEvery run gets a fresh dir — no interference, no cleanup.",
            ),
            ex(
                "08-4",
                "Look at a test suite you have written or use. Identify one test that depends on order, time, environment, or random. Describe how you would fix it without changing what it tests.",
                "This is the single most common test debt.",
                "Common fix: extract the nondeterministic dependency as an argument (`process(x, clock=fake_clock)`), or use a mocking library, or seed randomness. The test still verifies the same behavior — but now deterministically.",
            ),
        ],
    },
    {
        "id": "09",
        "title": "What Makes a Good Regression Test",
        "level": "Intermediate",
        "summary": "Seven criteria. Score every test against them.",
        "body": md("""
## The seven criteria
### 1. Fast
Runs in milliseconds. A slow suite gets skipped, and a skipped suite catches nothing.
- Target: full unit suite in < 30 seconds.
- If a test is inherently slow (e.g., end-to-end), separate it into a `slow` marker so devs can run fast tests during development.

### 2. Deterministic
Same input → same output, every time, on every machine. See Module 08.

### 3. Focused
One test asserts one behavior. If a test asserts three unrelated things, split it.

### 4. Independent
No test depends on another. Any test can run alone. Any order works.

### 5. Readable
The test tells you what it protects at a glance. Both:
- **Name** — describes the expectation
- **Body** — clear AAA structure

Bad: `test_biquad2()`. Good: `test_biquad_stable_when_pole_near_unit_circle()`.

### 6. Diagnostic
When it fails, you know immediately WHAT failed and WHY. Compare:
```python
# Bad — cryptic
assert result

# Good — self-explaining
assert result == expected, f"expected {expected}, got {result}"
```
Use `assert_allclose` (numpy) or `pytest`'s introspection — both give rich diffs.

### 7. Meaningful
The test protects behavior that MATTERS. A test that never catches anything is dead weight. Ask: "if this test failed, would I actually change something?" If no — delete it.

## The scoring rubric
| Criterion | Pass | Fail |
|---|---|---|
| Fast (< 100ms) | ✓ | ⨯ |
| Deterministic (100 runs identical) | ✓ | ⨯ |
| Focused (one behavior) | ✓ | ⨯ |
| Independent (no other test needed) | ✓ | ⨯ |
| Readable (name + AAA) | ✓ | ⨯ |
| Diagnostic (clear failure msg) | ✓ | ⨯ |
| Meaningful (protects real behavior) | ✓ | ⨯ |

A 7/7 test is a joy. A 4/7 test is technical debt. A 2/7 test hurts more than it helps.

## The productivity ROI
Every characteristic above is about **speed of diagnosis when things break**. A test suite exists to save you time. A poorly-written test costs more time to debug than it saves. Write tests as if you will fail them at 4pm on a Friday, tired, in a hurry.

## The FIRST acronym (mnemonic)
Another commonly cited version:
- **F**ast
- **I**ndependent
- **R**epeatable (deterministic)
- **S**elf-validating (assertion, not "look at the output")
- **T**imely (written close to the code, not months later)

Same ideas, easier to remember.
"""),
        "exercises": [
            ex(
                "09-1",
                "Take a test you have written recently. Score it 0-7 against the seven criteria. Note which criteria are failing.",
                "Be honest.",
                "Common weak criteria: readable (cryptic names), diagnostic (bare `assert result`), meaningful (test never actually caught anything). Note them and fix the top 1-2 for that test.",
            ),
            ex(
                "09-2",
                "Rewrite this bad test into a good one:\n```python\ndef test1():\n    x = [random.random() for _ in range(10)]\n    y = filter(x)\n    assert y\n```",
                "Multiple problems: nondeterministic, cryptic, no real assertion.",
                "```python\ndef test_filter_preserves_length():\n    # ARRANGE\n    input_signal = [0.1, 0.2, 0.3, 0.4, 0.5]\n\n    # ACT\n    output = filter(input_signal)\n\n    # ASSERT\n    assert len(output) == len(input_signal), \\\n        f'filter changed length: {len(input_signal)} -> {len(output)}'\n```\nDeterministic, focused, readable, diagnostic. Score jumped from ~2/7 to 7/7.",
            ),
            ex(
                "09-3",
                "Write a checklist in `regression-lab/test-review-checklist.md` that you (or a code reviewer) can use when reviewing any new test. Base it on the seven criteria plus AAA structure.",
                "This becomes YOUR standard.",
                "The checklist should have 8-10 yes/no items. Add it to your team's PR review template if applicable. Consistent standards produce consistent quality.",
            ),
        ],
    },
    # ────────────────────── PHASE 3: PRACTICAL SETUP ──────────────────────
    {
        "id": "10",
        "title": "Your First Regression Test in Python (pytest)",
        "level": "Intermediate",
        "summary": "The fastest possible path from zero to a passing regression suite.",
        "body": md("""
## Install (once)
```bash
python -m pip install --user pytest
```

## The simplest possible test file
Create `test_math.py`:
```python
def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2
```

## Run it
```bash
pytest
```
You see:
```
test_math.py::test_add_positive PASSED
test_math.py::test_add_negative PASSED
============ 2 passed in 0.02s ============
```

## Rules pytest follows automatically
- Files named `test_*.py` or `*_test.py` are test files
- Functions named `test_*` are tests
- `assert` is the assertion — no special syntax
- Failing asserts print a rich diff automatically

## Useful pytest commands
```bash
pytest                     # run everything
pytest test_math.py        # one file
pytest -k "add"            # tests whose name contains 'add'
pytest -v                  # verbose
pytest -x                  # stop at first failure
pytest --tb=short          # short traceback
pytest -q                  # quiet
pytest -s                  # do not capture prints (helpful for debugging)
```

## Adding a fixture (test setup)
```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_sum_of_sample(sample_data):
    assert sum(sample_data) == 15
```
Fixtures give tests clean, isolated setup. Pytest passes them in automatically by name.

## Parametrizing (many cases, one function)
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, -1, -2),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```
One function → three tests. Table-driven testing at its cleanest.

## Marking slow tests
```python
@pytest.mark.slow
def test_full_pipeline():
    ...
```
```bash
pytest -m "not slow"    # skip slow tests during dev
pytest -m "slow"        # only slow tests
```

## Project layout
```
myproject/
  src/
    myproject/
      __init__.py
      calc.py
  tests/
    test_calc.py
  pytest.ini            # optional config
```
Run `pytest` from repo root. Pytest auto-discovers `tests/`.

## The bare minimum you need
- `pip install pytest`
- Create `test_x.py` with `def test_something(): assert ...`
- Run `pytest`

That is it. Every other feature (fixtures, parametrize, marks) is convenience — the core is asserts in test functions.
"""),
        "exercises": [
            ex(
                "10-1",
                "In `regression-lab/python/`, create `calculator.py` with `add`, `sub`, `mul` functions. Create `test_calculator.py` with at least 3 tests. Run `pytest`. Verify all pass.",
                "Follow the exact structure from the module.",
                "```python\n# calculator.py\ndef add(a, b): return a + b\ndef sub(a, b): return a - b\ndef mul(a, b): return a * b\n\n# test_calculator.py\nimport calculator\ndef test_add(): assert calculator.add(2, 3) == 5\ndef test_sub(): assert calculator.sub(5, 3) == 2\ndef test_mul(): assert calculator.mul(4, 3) == 12\n```\nRunning `pytest`: 3 passed.",
            ),
            ex(
                "10-2",
                "Break one function intentionally (e.g., `add` returns `a - b`). Rerun pytest. Read the failure output carefully — it shows the exact expected vs actual. Fix, rerun, verify green.",
                "This is the RED / GREEN loop.",
                "Pytest output: `assert -1 == 5` with visible expected vs actual. After fix: `3 passed`. You just ran your first real regression cycle in pytest.",
            ),
            ex(
                "10-3",
                "Convert `test_add`, `test_sub`, `test_mul` into a single parametrized test using `@pytest.mark.parametrize`. Verify the same three cases run.",
                "One function, table of cases.",
                "```python\nimport pytest\nimport calculator\n\n@pytest.mark.parametrize(\"fn,a,b,expected\", [\n    (calculator.add, 2, 3, 5),\n    (calculator.sub, 5, 3, 2),\n    (calculator.mul, 4, 3, 12),\n])\ndef test_operations(fn, a, b, expected):\n    assert fn(a, b) == expected\n```\nStill 3 tests, but future cases are one-line additions.",
            ),
            ex(
                "10-4",
                "Add a fixture that returns a `Calculator` object (imagine one with state, like a running total). Write two tests that use the fixture. Confirm each test gets a FRESH calculator.",
                "Fixtures are per-test by default.",
                "```python\n@pytest.fixture\ndef calc():\n    return Calculator()\n\ndef test_add_updates_total(calc):\n    calc.add(5)\n    assert calc.total == 5\n\ndef test_isolated_fixture(calc):\n    assert calc.total == 0  # not polluted by previous test\n```\nThe second test's `calc.total == 0` proves isolation.",
            ),
        ],
    },
    {
        "id": "11",
        "title": "Regression Tests in C (Minimal Harness)",
        "level": "Intermediate",
        "summary": "C has no default test framework. A 20-line harness gets you 90% of the value.",
        "body": md("""
## The minimum viable C test harness
No framework needed. This works with any C compiler.

`test_calc.c`:
```c
#include <stdio.h>
#include <stdlib.h>
#include "calc.h"

static int failures = 0;

#define CHECK(cond) do { \\
    if (!(cond)) { \\
        fprintf(stderr, \"FAIL: %s (line %d)\\n\", #cond, __LINE__); \\
        failures++; \\
    } \\
} while(0)

static void test_add_positive(void) {
    CHECK(add(2, 3) == 5);
    CHECK(add(0, 0) == 0);
}

static void test_add_negative(void) {
    CHECK(add(-1, -1) == -2);
}

int main(void) {
    test_add_positive();
    test_add_negative();
    if (failures) {
        fprintf(stderr, \"\\n%d test(s) failed.\\n\", failures);
        return 1;
    }
    printf(\"All tests passed.\\n\");
    return 0;
}
```

Build and run:
```bash
gcc -std=c11 -Wall -Wextra -o test_calc test_calc.c calc.c
./test_calc
echo $?    # 0 = pass, 1 = fail
```

## Why this is enough for many projects
- Non-zero exit code on failure = CI-integrable
- File + line + failed expression on error = diagnosable
- Zero dependencies = works on any embedded toolchain
- 20 lines of infrastructure = no learning curve

## When to graduate to a framework
If you find yourself wanting:
- Test setup / teardown
- Grouping tests
- Better output formatting
- Parametrized tests

Then use **Unity** (Throw-The-Switch, MIT license, embedded-friendly) or **cmocka**. Both are single-header (or small) and easy to add.

## Unity example
```c
#include \"unity.h\"

void setUp(void) {}
void tearDown(void) {}

void test_add_positive(void) {
    TEST_ASSERT_EQUAL_INT(5, add(2, 3));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_add_positive);
    return UNITY_END();
}
```

## Testing floating-point in C
```c
#include <math.h>
#define FLT_TOL 1e-6f

CHECK(fabsf(actual - expected) < FLT_TOL);
```
Or Unity's `TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual)`.

## Testing arrays / vectors in C
For DSP goldens (Module 12), you compare arrays with a tolerance:
```c
static int arrays_close(const float *a, const float *b, size_t n, float tol) {
    for (size_t i = 0; i < n; ++i) {
        if (fabsf(a[i] - b[i]) > tol) return 0;
    }
    return 1;
}
CHECK(arrays_close(actual, expected, N, 1e-6f));
```

## Makefile integration
```makefile
test: test_calc
	./test_calc

test_calc: test_calc.o calc.o
	$(CC) $^ -o $@ -lm

.PHONY: test
```
```bash
make test    # runs all tests
```

## CI integration
Just run the binary and check exit code. Any CI can do this. That is the beauty of the C exit-code convention.
"""),
        "exercises": [
            ex(
                "11-1",
                "In `regression-lab/c/`, create `calc.h`, `calc.c` (with `add`, `sub`), and `test_calc.c` using the minimal harness. Compile and run.",
                "Copy the harness pattern from the module.",
                "Files created. `gcc test_calc.c calc.c -o test_calc && ./test_calc` prints 'All tests passed.' Exit code 0.",
            ),
            ex(
                "11-2",
                "Break `add` intentionally. Rerun. Observe the FAIL message with file and line. Fix. Rerun. Passes.",
                "The `#cond` in the macro is what prints the failed expression.",
                "Output: `FAIL: add(2, 3) == 5 (line NN)`. Then `1 test(s) failed.` Exit code 1. After fix: `All tests passed.` Exit 0.",
            ),
            ex(
                "11-3",
                "Add a floating-point function `float scale(float x, float g)` that returns `x * g`. Write a test using `fabsf(actual - expected) < 1e-6f`. Handle both positive and negative cases.",
                "Never use `==` for floats.",
                "```c\nstatic void test_scale(void) {\n    CHECK(fabsf(scale(2.0f, 0.5f) - 1.0f) < 1e-6f);\n    CHECK(fabsf(scale(-1.0f, 0.25f) - (-0.25f)) < 1e-6f);\n}\n```\nBuild with `-lm` for math functions.",
            ),
            ex(
                "11-4",
                "Add a Makefile target `test` that builds and runs the test binary. Verify `make test` works and returns exit code 0 on success, 1 on failure.",
                "See the Makefile example in the module.",
                "```makefile\ntest: test_calc\n\t./test_calc\n\ntest_calc: test_calc.c calc.c\n\t$(CC) $^ -o $@ -lm\n\n.PHONY: test\n```\n`make test` builds and runs. This target can now be called from CI.",
            ),
        ],
    },
    {
        "id": "12",
        "title": "Regression Tests for DSP (Cross-Language Golden Vectors)",
        "level": "Advanced",
        "summary": "The classic embedded pattern: Python computes the reference, C code must match within tolerance.",
        "body": md("""
## The DSP regression testing pattern
```
Python (reference, easy to trust)
    │
    ├─ generate input signal      → input.bin
    ├─ apply reference algorithm  → expected_output.bin
    │
C (production, must match)
    │
    ├─ read input.bin
    ├─ apply implementation
    ├─ read expected_output.bin
    └─ compare with tolerance → pass/fail
```

## Why this pattern is dominant
- **Python has trusted reference implementations** (scipy, numpy) for almost every DSP algorithm
- **C is what actually ships** on the embedded target
- **The compare-with-tolerance step catches numerical regressions** that a byte comparison would miss

## Step 1: Python golden generator
```python
# goldens/gen_fir_impulse.py
import numpy as np

fs = 48000
n = 1024

# Input: unit impulse
impulse = np.zeros(n, dtype=np.float32)
impulse[0] = 1.0

# Reference: 3-tap FIR with these coeffs
coeffs = np.array([0.25, 0.5, 0.25], dtype=np.float32)
expected = np.convolve(impulse, coeffs, mode='same').astype(np.float32)

impulse.tofile('goldens/impulse_in.bin')
expected.tofile('goldens/fir_impulse_out.bin')
np.array(coeffs, dtype=np.float32).tofile('goldens/fir_coeffs.bin')
print(f'Regenerated FIR impulse golden: n={n}')
```
Run once. Commit the .bin files.

## Step 2: C test that loads and compares
```c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include \"fir.h\"

#define N 1024
#define NUM_COEFFS 3
#define TOL 1e-6f

static int test_fir_impulse(void) {
    float coeffs[NUM_COEFFS], input[N], expected[N], actual[N];

    FILE *f;
    f = fopen(\"goldens/fir_coeffs.bin\", \"rb\");
    fread(coeffs, sizeof(float), NUM_COEFFS, f); fclose(f);

    f = fopen(\"goldens/impulse_in.bin\", \"rb\");
    fread(input, sizeof(float), N, f); fclose(f);

    f = fopen(\"goldens/fir_impulse_out.bin\", \"rb\");
    fread(expected, sizeof(float), N, f); fclose(f);

    fir_process(input, actual, N, coeffs, NUM_COEFFS);

    float max_err = 0.0f;
    for (int i = 0; i < N; ++i) {
        float err = fabsf(actual[i] - expected[i]);
        if (err > max_err) max_err = err;
    }

    printf(\"FIR impulse: max error = %e (tol %e)\\n\", max_err, TOL);
    return max_err < TOL ? 0 : 1;
}

int main(void) {
    return test_fir_impulse();
}
```

## Tolerance choice
| Reference format | Impl format | Typical tolerance |
|---|---|---|
| float64 (numpy default) | float32 | 1e-6 |
| float32 | float32 | 1e-6 (should be very tight) |
| float | Q15 | 1 / 32768 ≈ 3e-5 |
| float | Q31 | 1 / 2^31 ≈ 5e-10 |

Measure the actual error once, then set tolerance ~2-5x above measured max.

## Cross-checking with the golden generator
When the tolerance seems too loose:
1. Print `max_err` (as the C code above does)
2. If `max_err` is much smaller than TOL, tighten TOL
3. If `max_err` is close to TOL, the tolerance is honest — do not loosen without understanding

## MATLAB as reference generator
Same pattern, MATLAB replaces Python:
```matlab
% goldens/gen_fir_impulse.m
n = 1024;
impulse = zeros(n, 1, 'single');
impulse(1) = 1;
coeffs = single([0.25, 0.5, 0.25]);
expected = single(conv(impulse, coeffs, 'same'));

fid = fopen('goldens/impulse_in.bin', 'w'); fwrite(fid, impulse, 'single'); fclose(fid);
fid = fopen('goldens/fir_impulse_out.bin', 'w'); fwrite(fid, expected, 'single'); fclose(fid);
disp('Regenerated FIR impulse golden');
```

## The dual-source pattern
For extra confidence: generate the golden with TWO independent sources (numpy AND matlab, or numpy AND a hand-derived analytical formula) and confirm they agree. Then use one as the golden. This catches errors in the reference generator itself.

## What this pattern is worth
Every embedded DSP team that ships production silently relies on this pattern. A missing tolerance, a stale golden, a wrong dtype — any of these has caused real product recalls.
"""),
        "exercises": [
            ex(
                "12-1",
                "Write `goldens/gen_moving_avg.py`: generate a 100-sample chirp signal, apply a 5-point moving average using numpy, save both `.bin` files as float32.",
                "Use `np.linspace` and `np.sin` for the chirp.",
                "```python\nimport numpy as np\nn = 100; fs = 1000\nt = np.arange(n) / fs\nchirp = np.sin(2*np.pi*np.linspace(50, 200, n)*t).astype(np.float32)\nkernel = np.ones(5, dtype=np.float32) / 5\nexpected = np.convolve(chirp, kernel, mode='same').astype(np.float32)\nchirp.tofile('goldens/chirp_in.bin')\nexpected.tofile('goldens/mavg_out.bin')\n```",
            ),
            ex(
                "12-2",
                "Implement `moving_avg(const float *in, float *out, size_t n, size_t window)` in C (`regression-lab/c/moving_avg.c`). Write a test that loads the goldens, runs your C code, and compares with tolerance 1e-6.",
                "For edge cases at the borders, use zero-padding or match numpy's 'same' mode carefully.",
                "The tricky part is matching numpy's `mode='same'` — it centers the kernel. Your C implementation must handle boundary padding the same way. If your implementation is exact, max error will be ~1e-7 for float32; tolerance 1e-6 has good margin.",
            ),
            ex(
                "12-3",
                "Print the `max_err` from your C test. Is it near the tolerance or far below? Discuss what that tells you.",
                "Measured error tells you about the tolerance's honesty.",
                "If max_err is 1e-8 and TOL is 1e-6: TOL is loose — tighten it or add a comment explaining the margin. If max_err is 8e-7 and TOL is 1e-6: TOL is tight and honest. This measurement is how you make defensible tolerance decisions.",
            ),
            ex(
                "12-4",
                "Deliberately introduce a small bug in your C `moving_avg` (e.g., divide by window+1 instead of window). Rerun the test. Observe the max_err spike. Fix. Rerun. Passes.",
                "This is the actual value of the golden pattern.",
                "The buggy version shows a max_err ~ 0.15 or so — massively over the 1e-6 tolerance. The test flags a regression precisely. This is the same mechanism that would catch a production bug in a shipping filter.",
            ),
        ],
    },
    {
        "id": "13",
        "title": "Regression Tests in MATLAB",
        "level": "Intermediate",
        "summary": "MATLAB has a unit testing framework. Use it for numerical work where MATLAB is the native language.",
        "body": md("""
## When to use MATLAB tests
- Your reference algorithm lives in MATLAB
- The team already uses MATLAB for DSP prototyping
- You need to verify a Simulink model or generated code
- Numerical work where MATLAB's array operations are cleanest

For pure C or embedded, use the C harness (Module 11). For general-purpose testing, use pytest (Module 10). MATLAB tests are for MATLAB-heavy environments.

## Simplest form: assert-based script
```matlab
% test_biquad.m
b0 = 1; b1 = 0; b2 = 0; a1 = 0; a2 = 0;  % identity
x = [1 0 0 0 0];
y = my_biquad(x, b0, b1, b2, a1, a2);
assert(all(abs(y - x) < 1e-9), 'Identity biquad failed');
disp('test_biquad OK');
```
Run: `matlab -batch \"test_biquad\"` — exit code non-zero on assert failure.

## Class-based tests (matlab.unittest)
```matlab
% BiquadTest.m
classdef BiquadTest < matlab.unittest.TestCase
    methods(Test)
        function testIdentityPassesInput(testCase)
            x = [1 0 0 0 0];
            y = my_biquad(x, 1, 0, 0, 0, 0);
            testCase.verifyEqual(y, x, 'AbsTol', 1e-9);
        end

        function testDCGainIsExpected(testCase)
            x = ones(1, 100);
            y = my_biquad(x, 0.5, 0, 0, 0, 0);
            testCase.verifyEqual(y(end), 0.5, 'AbsTol', 1e-9);
        end
    end
end
```
Run: `runtests('BiquadTest')` or `matlab -batch \"runtests('BiquadTest')\"`.

## Numerical verify methods
```matlab
testCase.verifyEqual(actual, expected, 'AbsTol', 1e-6);
testCase.verifyEqual(actual, expected, 'RelTol', 1e-6);
testCase.verifyLessThan(actual, threshold);
testCase.verifyGreaterThan(actual, threshold);
testCase.verifySize(actual, [1 100]);
testCase.verifyClass(actual, 'single');
```

## Cross-language golden generation
When MATLAB is the reference generator (see Module 12), the pattern is:
```matlab
% gen_golden.m
input = single(...);
expected = single(reference_algo(input));

fid = fopen('goldens/in.bin', 'w'); fwrite(fid, input, 'single'); fclose(fid);
fid = fopen('goldens/out.bin', 'w'); fwrite(fid, expected, 'single'); fclose(fid);
```
Then C/C++/Python tests consume the .bin files.

## Running MATLAB tests from CI
```bash
matlab -batch \"results = runtests('BiquadTest'); assertSuccess(results)\"
```
Exit code non-zero if any test fails. CI-integrable.

Cost consideration: MATLAB is licensed. Open-source alternatives (Octave, Julia) work for many tests but have subtle numerical differences.

## When NOT to use MATLAB tests
- Your production code is in C/C++/Python and MATLAB is only for prototyping
- CI cannot license MATLAB
- The test is a general software test (use pytest instead)

For DSP prototype validation and Simulink coverage, MATLAB tests are the right tool. For shipping product regression, prefer testing in the language of the product.
"""),
        "exercises": [
            ex(
                "13-1",
                "In `regression-lab/matlab/`, write `test_scale.m` as a simple script: define a function `scale(x, g) = x .* g` (in `scale.m`), write assertions, and run `matlab -batch \"test_scale\"`. Verify pass and fail cases.",
                "Assert-based scripts are the fastest MATLAB test form.",
                "```matlab\n% scale.m\nfunction y = scale(x, g)\n    y = x .* g;\nend\n\n% test_scale.m\nx = [1 2 3];\nassert(all(abs(scale(x, 0.5) - [0.5 1 1.5]) < 1e-9));\ndisp('test_scale OK');\n```",
            ),
            ex(
                "13-2",
                "Convert your `test_scale` script into a `matlab.unittest.TestCase` class with at least 2 test methods. Run with `runtests('ScaleTest')`.",
                "Class-based tests give you a test runner and reporting.",
                "```matlab\nclassdef ScaleTest < matlab.unittest.TestCase\n    methods(Test)\n        function testPositive(tc)\n            tc.verifyEqual(scale([1 2 3], 0.5), [0.5 1 1.5], 'AbsTol', 1e-9);\n        end\n        function testZero(tc)\n            tc.verifyEqual(scale([1 2 3], 0), [0 0 0], 'AbsTol', 1e-12);\n        end\n    end\nend\n```",
            ),
            ex(
                "13-3",
                "If you have a Python + C project already, discuss (in `regression-lab/matlab/when-to-use.md`) whether adding MATLAB tests helps or hurts. When would it actually be worth the license and cross-language complexity?",
                "This is a decision-making exercise, not a code exercise.",
                "MATLAB tests add value when: (a) MATLAB IS the reference algorithm source, (b) team is MATLAB-heavy, (c) verifying Simulink code generation. They hurt when: (a) MATLAB is only for prototyping, (b) CI cannot license MATLAB, (c) tests could be done in Python with numpy just as easily.",
            ),
        ],
    },
    {
        "id": "14",
        "title": "Regression Tests in C++ (Catch2 or doctest)",
        "level": "Intermediate",
        "summary": "Header-only C++ frameworks that install by copying one file. Modern, ergonomic, fast.",
        "body": md("""
## The C++ landscape
Popular C++ test frameworks:
- **Catch2** — header-only (single-header available), expressive, no dependencies
- **doctest** — single-header, extremely fast to compile, embeddable inside prod code
- **GoogleTest** — Google's framework, powerful but heavier setup, requires build config
- **Boost.Test** — part of Boost, if you already use Boost

For a lab / small project, **doctest** is the fastest to get running. **Catch2** is the most widely used. Both are excellent.

## doctest (fastest to try)
Download `doctest.h` (single header). Create `test_calc.cpp`:
```cpp
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include \"doctest.h\"
#include \"calc.h\"

TEST_CASE(\"addition works for positive integers\") {
    CHECK(add(2, 3) == 5);
    CHECK(add(0, 0) == 0);
}

TEST_CASE(\"subtraction works for negatives\") {
    CHECK(sub(0, 5) == -5);
    REQUIRE(sub(5, 5) == 0);  // REQUIRE stops the test on failure
}
```
Build:
```bash
g++ -std=c++17 -Wall -o test_calc test_calc.cpp calc.cpp
./test_calc
```

## Catch2 (widely used)
Very similar API:
```cpp
#define CATCH_CONFIG_MAIN
#include \"catch.hpp\"

TEST_CASE(\"addition\") {
    REQUIRE(add(2, 3) == 5);
    SECTION(\"handles negatives\") {
        REQUIRE(add(-1, -1) == -2);
    }
}
```
`SECTION` gives you nested contexts — each SECTION runs in its own copy of the enclosing TEST_CASE state.

## CHECK vs REQUIRE
- **CHECK** (Catch2 and doctest) — records failure but continues the test
- **REQUIRE** — records failure and STOPS the test (like an assert-and-abort)

Use REQUIRE when subsequent assertions would be meaningless if the first failed (e.g., dereferencing a pointer after a null check).

## Floating-point in Catch2 / doctest
```cpp
#include \"doctest.h\"
CHECK(actual == doctest::Approx(expected).epsilon(1e-6));

// Catch2:
CHECK(actual == Catch::Approx(expected).margin(1e-6));
```
Or manual: `CHECK(std::abs(actual - expected) < 1e-6);`

## Parametrized tests
```cpp
TEST_CASE(\"add parametrized\") {
    struct Case { int a, b, exp; };
    for (const auto& c : std::vector<Case>{{2,3,5}, {-1,-1,-2}, {0,0,0}}) {
        CAPTURE(c.a, c.b);  // print on failure
        CHECK(add(c.a, c.b) == c.exp);
    }
}
```

## GoogleTest (heavier but powerful)
Requires CMake or Bazel integration. Best for large C++ projects.
```cpp
#include <gtest/gtest.h>

TEST(Calc, AddPositive) {
    EXPECT_EQ(add(2, 3), 5);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```
Fixtures, death tests, mocks (gmock) — full-featured. Learning curve is steeper.

## Recommendation for this course
Use **doctest** for the exercises. Single header, no build system complexity. If your team already uses Catch2 or GoogleTest, the API concepts transfer directly.

## Comparison with C harness
The minimal C harness (Module 11) is 20 lines and does the job for simple cases. C++ frameworks add:
- Nested contexts (SECTION)
- Automatic test discovery (no manual list in main)
- Rich output formatting
- Approx for floats built in

For C++ projects, use a framework. For pure C on constrained targets, the minimal harness is often better than pulling in dependencies.
"""),
        "exercises": [
            ex(
                "14-1",
                "Download doctest.h into `regression-lab/cpp/`. Write a `calc.h`/`calc.cpp` with `add` and `sub`. Write `test_calc.cpp` with 3 TEST_CASEs. Build and run.",
                "One header, no build system — just gcc with -std=c++17.",
                "```cpp\n#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN\n#include \"doctest.h\"\n#include \"calc.h\"\n\nTEST_CASE(\"add positive\") { CHECK(add(2,3) == 5); }\nTEST_CASE(\"add negative\") { CHECK(add(-1,-1) == -2); }\nTEST_CASE(\"sub\") { CHECK(sub(5,3) == 2); }\n```\n`g++ -std=c++17 test_calc.cpp calc.cpp -o test_calc && ./test_calc`.",
            ),
            ex(
                "14-2",
                "Add a floating-point function `scale(float x, float g)`. Test it with doctest::Approx. Choose a tolerance and justify it.",
                "Use `doctest::Approx(expected).epsilon(1e-6)`.",
                "```cpp\nTEST_CASE(\"scale float\") {\n    CHECK(scale(2.0f, 0.5f) == doctest::Approx(1.0f).epsilon(1e-6f));\n}\n```\nTolerance 1e-6 is safe for float32 with simple arithmetic. For repeated multiplication or long chains, measure actual error first.",
            ),
            ex(
                "14-3",
                "Compare your C harness from Module 11 with this C++ doctest version. In `regression-lab/cpp/compare.md`, list: what does doctest add? what does the minimal C harness do just as well? When would you pick each?",
                "Trade-offs matter — this is a real engineering choice.",
                "Doctest adds: auto discovery, better formatting, SECTIONs, Approx for floats, easier parametrization. C harness matches on: simplicity, zero deps, embedded-friendly, small binary size. Pick doctest for C++ projects. Pick C harness for constrained C-only embedded targets where dependencies are a burden.",
            ),
        ],
    },
    # ────────────────────── PHASE 4: REAL USE CASES ──────────────────────
    {
        "id": "15",
        "title": "Use Case: Bug-Fix Regression Tests",
        "level": "Advanced",
        "summary": "The most common and highest-value type. When a bug is fixed, a test is written to guard the fix forever.",
        "body": md("""
## The workflow
1. Bug is reported (issue #123, or verbally, or discovered in production)
2. **Before touching the fix**, write a test that reproduces the bug
3. Run the test — it fails (RED). You have proven the bug is real.
4. Fix the code
5. Rerun the test — it passes (GREEN). You have proven the fix works.
6. Commit test and fix together
7. The test lives forever in the suite

Every future run of CI now guards against this specific bug re-appearing.

## Why write the test first
- **Confirms the reproducer**: no ambiguity about what "the bug" is
- **Confirms the fix**: you saw the transition RED → GREEN with your own eyes
- **Prevents you from fooling yourself**: it is very easy to change code and convince yourself it works when it does not
- **Documents the bug forever**: the test IS the bug's minimal reproducer

## Naming and documentation
A bug-fix regression test's name should reference the issue and describe the behavior:
```python
def test_regression_issue_123_add_returns_exact_for_integer_floats():
    \"\"\"Guards fix for #123: add(1.0, 2.0) returned 2.9999... due to
    subtraction ordering. Fixed 2026-09-15. See docs/bugs/123.md.\"\"\"
    assert add(1.0, 2.0) == 3.0
```

Some teams prefer keeping the issue reference in the docstring, not the name. Either is fine — the key is that the future reader can find the context.

## The "smallest reproducer" principle
A bug-fix test should:
- Reproduce the EXACT bug with minimal setup
- Not test surrounding functionality (that is what other tests are for)
- Use hard-coded values from the bug report, not variables

Bad: a full pipeline test that happens to exercise the bug.
Good: a focused test that fails with the buggy code and passes with the fix, using minimum inputs.

## When the bug is intermittent
Sometimes the bug only appears with certain inputs, timing, or state. Then:
1. **Find the trigger**: what specific input/state reveals the bug?
2. **Reproduce deterministically**: eliminate the "sometimes" — see Module 08
3. **Then write the test** as above

An intermittent bug reproducer that "usually" fails is not a test. Fix the determinism first.

## When you cannot easily reproduce
Some bugs (memory corruption, timing, hardware) resist unit-test reproduction. Options:
- **Test the fix's contract**: if the bug was "buffer overflow at n>1000", test with n>1000 that the buffer is sized correctly
- **Test at a higher level**: integration or system test that exercises the failing scenario
- **Add an assertion**: as a runtime guard, complementing (not replacing) the fix

For very difficult bugs, a good post-mortem in the commit message becomes part of the documentation trail.

## The anti-pattern: fix without a test
Someone reports a bug. Developer fixes it. No test. Six months later, someone refactors that area and reintroduces the exact same bug. This is one of the most common failure modes in software.

Every bug fix should be accompanied by a regression test. If you truly cannot write one, document WHY in the commit message.
"""),
        "exercises": [
            ex(
                "15-1",
                "Take this fake bug report: 'divide(10, 0) crashes instead of raising an error.' Follow the full lifecycle in `regression-lab/python/`:\n(1) write the RED test\n(2) run pytest, see it fail (crash or wrong behavior)\n(3) fix `divide` to raise `ZeroDivisionError` (or a custom exception)\n(4) rerun, see GREEN",
                "In pytest, use `with pytest.raises(...)` to assert an exception.",
                "```python\nimport pytest\nfrom mymath import divide\n\ndef test_regression_bug_divide_by_zero_raises_error():\n    \"\"\"Guards fix: previously crashed instead of raising.\"\"\"\n    with pytest.raises(ZeroDivisionError):\n        divide(10, 0)\n```\nFix `divide`: `if b == 0: raise ZeroDivisionError('division by zero'); return a / b`.",
            ),
            ex(
                "15-2",
                "You inherit a codebase with 10 bug-fix commits from last year, none with tests. Design a systematic plan (in `regression-lab/plans/retrofit-tests.md`) for adding regression tests for those old bugs.",
                "Not every old bug can or should get a test — but many can.",
                "Plan should include: (1) read commit messages / issue trackers to understand each fix, (2) prioritize by risk / customer impact, (3) for each: write a test that would fail with the pre-fix code, (4) run against current code to confirm passes, (5) commit test with reference to original fix commit. Sensible cadence: 1-2 per week alongside normal work.",
            ),
            ex(
                "15-3",
                "Compare two approaches to naming a bug-fix regression test:\n(A) `test_add_integer_floats()`\n(B) `test_regression_issue_123_add_integer_floats()`\nWhat are the trade-offs?",
                "Both have merit. Think about future readers and search behavior.",
                "(A) is cleaner and reads like a normal test. Good if the docstring references #123. (B) is immediately searchable — grepping for 'issue_123' finds it — but adds noise. Team convention wins; the important thing is that the issue is discoverable somehow. Many teams use (A) with docstring reference, and add a `pytest` mark like `@pytest.mark.regression_123` for filtering.",
            ),
            ex(
                "15-4",
                "Someone on your team submits a PR titled 'fix null pointer in audio_process' with no test. What questions do you ask in the code review?",
                "This is a real workflow scenario.",
                "Questions: (1) Can you add a test that would have caught this? (2) If truly unable, why? (3) What was the root cause — is there a wider pattern? (4) Should this fix have an assertion as belt-and-braces? A good team culture treats 'fix without regression test' as an incomplete PR unless well justified.",
            ),
        ],
    },
    {
        "id": "16",
        "title": "Use Case: Refactor Regression Tests (Safety Net)",
        "level": "Advanced",
        "summary": "Tests written BEFORE refactoring, so you can restructure with confidence that behavior is preserved.",
        "body": md("""
## The refactor problem
Refactoring = restructuring code WITHOUT changing behavior. But how do you PROVE behavior is unchanged?
- Reading the diff? Slow and error-prone.
- Manual testing? Won't cover edge cases.
- Trust? Wrong answer.

The answer: regression tests written BEFORE the refactor.

## The safety net workflow
```
1. Identify the module you want to refactor
2. Write regression tests that lock down current behavior
   - Include edge cases, boundary conditions, error paths
   - Use goldens for complex outputs
3. Run the tests — all green
4. Now REFACTOR freely
5. Rerun tests after each incremental change
   - Red = you broke something → back off
   - Green = safe to continue
6. When done, the test suite proves behavior is unchanged
```

## Characterization tests
When you inherit a codebase with no tests, and you want to refactor:
1. Write tests that describe WHAT THE CODE CURRENTLY DOES
   - Even if the current behavior is weird or partially wrong
2. These are called **characterization tests**
3. They give you a safety net to refactor
4. Once refactored, you can incrementally fix the weird behavior — each fix guarded by its own regression test

Michael Feathers' book *Working Effectively with Legacy Code* is the classic reference for this pattern.

## What to test before refactoring
Cover these categories:
- **Happy paths**: normal inputs, normal outputs
- **Edge cases**: empty inputs, max-size inputs, zero, negative, boundary values
- **Error paths**: what happens on bad input?
- **Golden outputs**: for complex return values, snapshot them
- **Side effects**: if the function writes files or state, test that
- **Performance**: if timing matters, benchmark before AND after

## The rule
> If it is not in the tests, the refactor is allowed to change it.

Anything you do not test, you cannot guarantee. So the coverage of your pre-refactor tests defines the "contract" you are preserving.

## When refactor tests catch real bugs
Sometimes writing tests BEFORE a refactor reveals bugs the code always had. Now you have a decision:
- Fix the bug now, before refactoring → cleaner but bigger PR
- Test the current (buggy) behavior, refactor with that safety net, then fix in a separate PR → smaller PRs, clearer history

For anything non-trivial, the second approach usually wins. It keeps your refactor PR truly a refactor (behavior identical) and separates it from the intentional bug fix.

## Small commits, run tests every one
Refactor in tiny steps. After each:
```bash
git add -p && pytest
```
Passes → commit → continue. Fails → figure out what you broke immediately, while the change is fresh.

Big-bang refactors without tests running between steps are how projects break in ways nobody understands.

## Post-refactor: delete or update tests?
After the refactor, some tests may no longer make sense (they tested the OLD structure). Options:
- **Delete** if they tested internal implementation details that legitimately no longer exist
- **Rewrite** if the behavior is still worth testing but the API is now different
- **Keep as-is** if they still capture user-visible behavior

The rule: keep tests that describe WHAT the code does for its users. Delete tests that describe HOW the code is internally structured.
"""),
        "exercises": [
            ex(
                "16-1",
                "Take this function (in `regression-lab/python/legacy.py`):\n```python\ndef process(data):\n    result = []\n    for x in data:\n        if x > 0:\n            result.append(x * 2)\n        elif x < 0:\n            result.append(-x)\n        else:\n            result.append(1)\n    return result\n```\nWrite 5 regression tests that lock down its behavior (happy path, negatives, zero, empty input, mixed).",
                "Cover the branches and edge cases you can see.",
                "```python\ndef test_positive_doubled(): assert process([1, 2, 3]) == [2, 4, 6]\ndef test_negative_absolute(): assert process([-1, -2, -3]) == [1, 2, 3]\ndef test_zero_becomes_one(): assert process([0]) == [1]\ndef test_empty(): assert process([]) == []\ndef test_mixed(): assert process([-1, 0, 1]) == [1, 1, 2]\n```",
            ),
            ex(
                "16-2",
                "Now refactor `process` using a list comprehension or a dict-dispatch — any restructure that keeps behavior identical. Run your 5 tests after each small change. Do not touch the tests.",
                "The tests are your safety net.",
                "```python\ndef process(data):\n    def transform(x):\n        if x > 0: return x * 2\n        if x < 0: return -x\n        return 1\n    return [transform(x) for x in data]\n```\nAll 5 tests still pass. Behavior preserved. Structure improved.",
            ),
            ex(
                "16-3",
                "Deliberately break behavior mid-refactor (e.g., handle zero as `0` instead of `1`). Run tests — one fails. Read the failure message. Fix and continue. This teaches you what refactor-safety feels like.",
                "The failing test tells you exactly what you broke.",
                "`test_zero_becomes_one` fails with clear message. You immediately know: the zero-handling case is broken. Revert or fix that specific branch. This is why refactoring WITH tests is so much faster than refactoring without them.",
            ),
            ex(
                "16-4",
                "Discuss in `regression-lab/refactor-notes.md`: 'What is the minimum test coverage before I feel safe refactoring a critical module?' There is no single right answer — this is about calibrating YOUR intuition.",
                "Depends on the module's criticality and your risk tolerance.",
                "Typical calibrations: (a) All public functions have at least happy-path + one edge case, (b) All branches (if/else/switch) are exercised, (c) Error paths and error messages are tested, (d) Any known-tricky behavior has a specific test. If you have all these, you can refactor confidently. Less than this = you are gambling.",
            ),
        ],
    },
    {
        "id": "17",
        "title": "Use Case: Numerical (DSP) Regression",
        "level": "Advanced",
        "summary": "The specific challenge of guarding signal-processing outputs, where 'correct' is fuzzy but 'unchanged' is precise.",
        "body": md("""
## Why DSP tests are their own thing
DSP output is often a long array of floats. There is no single expected value. The correct behavior is:
- Numerically close to a reference within tolerance
- Stable across builds (no bit-drift)
- Preserves signal properties (SNR, phase, delay)

Testing DSP requires all the tools from Modules 06 (goldens), 07 (tolerances), and 12 (cross-language goldens).

## The four DSP regression test types
### 1. Reference comparison
Reference: numpy, scipy, MATLAB, or hand analytical.
Test: production output vs reference, within tolerance.
Example: your FIR output vs `np.convolve`.

### 2. Property-based
Assert mathematical properties without pinning exact values.
- Impulse response: `output[0] == coeffs[0]` (and so on)
- Linearity: `filter(a*x + b*y) == a*filter(x) + b*filter(y)` (within tolerance)
- Energy preservation: `sum(x^2) == sum(y^2)` for lossless transforms
- DC gain: `filter(ones) → ones * expected_gain`

### 3. Golden signal
Capture a specific input/output pair (Module 12) and verify byte-exact or tolerance-close over time.
Best for catching **any** drift in the numerical output.

### 4. Regression on measured metrics
For "meaningful" test signals, measure a metric (SNR, THD, peak-to-average ratio) and assert it is above/below a threshold.
Example: white noise input → filter output → SNR ratio > 40 dB.

## Choosing the right type
| Situation | Best type |
|---|---|
| Algorithm has known-correct output | Reference comparison |
| Algorithm should preserve a mathematical property | Property-based |
| Output is complex and you want to freeze it exactly | Golden signal |
| Testing a subjective quality (audio quality, distortion) | Metric-based |

Most DSP suites use a MIX of all four.

## The tolerance discipline (DSP-specific)
- **Float32 vs float64 reference**: expect ~1e-7 rel error
- **Fixed-point (Q15/Q31) vs float**: LSB-level tolerance, ~1/(2^N)
- **After N cascaded biquads**: error accumulates; measure it
- **After FFT**: error scales with sqrt(N) or log(N) depending on radix
- **After nonlinear operations (log, exp)**: error can be much larger; be generous but justified

Rule: measure once, set tolerance ~2-3x above measured max. Comment WHY.

## Handling intentional numerical changes
DSP algorithms evolve. Someone finds a better rounding strategy, or fixes a saturation edge case. Your golden fails.

Process:
1. Look at the diff: `plot(actual - expected)` in Python. Where does it differ? By how much?
2. Is the change theoretically justified? (Better rounding is good; random drift is bad.)
3. If justified: regenerate the golden, commit both golden and code together
4. If not justified: investigate — someone may have introduced a bug

## Long-signal tests
For 10-second stereo tests, exact goldens are large (~1 MB per test). Options:
- Store the golden but use Git LFS
- Instead of storing the golden, store the FFT of the golden (much smaller for band-limited signals)
- Store a hash of the golden — verify by regenerating and hashing, without storing megabytes
- Use property-based tests instead (SNR, THD, etc.) with no stored golden

Trade-off: exact goldens are strict (catch tiny drifts); property tests are looser but robust to intentional numerical refinements.

## The reality
Every embedded audio / DSP team that ships production has SOME regression suite for numerics. The teams that skip it ship silent audio bugs to customers. This is not optional at scale.
"""),
        "exercises": [
            ex(
                "17-1",
                "In `regression-lab/python/test_dsp_property.py`, write a property-based test for a biquad filter (or any filter you have): assert that DC input (all ones) produces steady-state DC gain matching a known formula.",
                "For a biquad y = b0*x + b1*x-1 + b2*x-2 - a1*y-1 - a2*y-2, DC gain = (b0+b1+b2)/(1+a1+a2).",
                "```python\ndef test_biquad_dc_gain():\n    b0, b1, b2, a1, a2 = 0.25, 0.5, 0.25, 0.0, 0.0\n    x = np.ones(1000, dtype=np.float32)\n    y = biquad(x, b0, b1, b2, a1, a2)\n    expected_gain = (b0 + b1 + b2) / (1 + a1 + a2)\n    assert abs(y[-1] - expected_gain) < 1e-6\n```\nThis test does not pin an exact output vector — it validates a mathematical property. Robust to numerical refinements.",
            ),
            ex(
                "17-2",
                "Write a golden-based test for the same biquad (100-sample chirp input). Store the golden as `.npy`. Compare with tolerance 1e-6. If your biquad is a straightforward implementation, tolerance should be tight.",
                "Combine Modules 06 (goldens) and 07 (tolerances).",
                "```python\ndef test_biquad_against_golden():\n    x = np.load('goldens/chirp_in.npy')\n    expected = np.load('goldens/biquad_chirp_out.npy')\n    actual = biquad(x, ...)\n    np.testing.assert_allclose(actual, expected, atol=1e-6)\n```\nGolden test catches ANY numerical drift. Property test catches conceptual bugs. Both together = strong safety net.",
            ),
            ex(
                "17-3",
                "For a real DSP function you have (or a made-up one), estimate: what tolerance is honest? Run it multiple times, measure actual error vs reference. Set tolerance ~2x above measured max. Justify in a comment.",
                "Tolerance = measured error + margin. Not made up.",
                "Process: (1) run production impl and reference, (2) `max(abs(actual - expected))` = measured max, (3) set tolerance = 2 * measured max. Comment: `// tolerance justified: measured max = 4.7e-7 on chirp input`. Now the tolerance has a paper trail.",
            ),
            ex(
                "17-4",
                "Discuss: your team wants to change a filter's coefficient rounding to reduce quantization noise. Old golden test fails. What is the process?",
                "This is a very common real-world scenario.",
                "(1) Verify the change is theoretically better (not just different). (2) Compute the DIFFERENCE between old and new goldens; check magnitude and shape. (3) If it looks like reduced noise (small, low-freq, or uncorrelated), likely a real improvement. (4) Regenerate the golden. (5) Commit BOTH the code change AND the new golden in ONE PR, with a description explaining the rationale. (6) Reviewer sees code diff + golden diff together and can approve or push back.",
            ),
        ],
    },
    {
        "id": "18",
        "title": "Use Case: Performance Regression",
        "level": "Advanced",
        "summary": "Not just correctness — speed matters. Guarding against 'the same result, but 10x slower' takes different tools.",
        "body": md("""
## The problem
Someone refactors your inner loop. All correctness tests pass. But it is 4x slower. Runtime tests would not catch this.

Performance regression tests measure TIME or CYCLES, and fail if a threshold is exceeded.

## The setup
```python
import time
import statistics

def benchmark(fn, iters=100):
    times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return statistics.median(times)  # robust to outliers

def test_fir_performance():
    baseline_seconds = 0.010   # measured, documented
    tolerance_multiplier = 1.5  # allow 50% slower before failing

    def do_work():
        fir(coeffs, big_signal)

    median = benchmark(do_work)
    assert median < baseline_seconds * tolerance_multiplier, \\
        f'FIR too slow: {median:.4f}s (baseline {baseline_seconds}s)'
```

## Why medians, not means
Timing is noisy — background processes, thermal throttling, cache state. **Median** or **best-of-N** are much more stable than mean. Never use a single-run measurement.

## The threshold tension
- **Tight threshold** (e.g., 1.1x baseline) → catches small regressions but fails on noise
- **Loose threshold** (e.g., 3x baseline) → stable but misses moderate regressions

Reality: performance tests must be somewhat loose OR run on dedicated benchmark hardware. On shared CI runners, 2x is a typical tolerance.

## Cycle counting on embedded (better than wall-clock)
For microcontrollers, wall-clock is meaningless. Use hardware cycle counters (ARM DWT->CYCCNT, or SysTick):
```c
uint32_t start = DWT->CYCCNT;
fir_process(input, output, N, coeffs, NC);
uint32_t cycles = DWT->CYCCNT - start;
assert(cycles < 15000);  // measured budget
```
Cycle counts are deterministic (mostly) on embedded — no CPU frequency scaling, no OS noise. Threshold can be tight.

## Baseline management
The baseline should be:
- **Measured**, not guessed
- **Committed with the test**, so future comparisons are anchored
- **Documented**: what machine, what compiler, what date

When the baseline legitimately needs to change (e.g., new hardware, intentional optimization):
- Update the baseline in the same PR as the code change
- Document WHY the baseline moved

## The N-run trick to eliminate flakiness
```python
def test_no_slower_than_baseline():
    baseline_ms = 10.0
    tolerance = 2.0
    trials = 5  # take best of 5

    times = []
    for _ in range(trials):
        t0 = time.perf_counter()
        do_work()
        times.append((time.perf_counter() - t0) * 1000)

    best = min(times)  # best-case is most reproducible
    assert best < baseline_ms * tolerance
```
Best-of-N reduces false alarms from transient system noise.

## Regression vs benchmark
- **Regression test**: pass/fail against a threshold, runs in CI
- **Benchmark**: continuous measurement of speed over time, historical tracking

Both are useful. A regression test catches "someone made it 3x slower yesterday." A benchmark dashboard catches "it has been getting 2% slower every month for a year."

## When to write a performance regression test
- The function is on a hot path (audio callback, ISR)
- It was recently optimized and you want to freeze that optimization
- Customer-facing latency matters (real-time DSP)

Do NOT write performance tests for every function — noise makes them low-value for cold-path code.

## The trap: comparing across machines
A benchmark that passes on your laptop may fail on CI (different CPU) or vice versa. Options:
- Scale threshold by machine (fragile)
- Use cycle counts on embedded (better)
- Use ratio tests: `time(fn_new) / time(fn_baseline_reference) < 1.5` (compares against a same-machine reference each run)

The ratio approach is robust: same machine, same conditions, compare relative speed.
"""),
        "exercises": [
            ex(
                "18-1",
                "In `regression-lab/python/test_perf.py`, write a benchmark test for any simple function you have (or write a `sum_squares(n)` for large n). Measure baseline, set threshold at 2x baseline, assert median < threshold.",
                "Use `time.perf_counter` and `statistics.median`.",
                "```python\nimport time, statistics\ndef bench(fn, iters=50):\n    return statistics.median([\n        (time.perf_counter(), fn(), time.perf_counter())[2]\n        - (time.perf_counter(), fn(), time.perf_counter())[0]\n        for _ in range(iters)\n    ])\n\ndef test_sum_squares_perf():\n    baseline = 0.005  # measured\n    def work(): return sum(i*i for i in range(100_000))\n    median = bench(work, iters=50)\n    assert median < baseline * 2\n```\nSimpler version acceptable — the key is median + threshold.",
            ),
            ex(
                "18-2",
                "Deliberately make your function slower (add a `time.sleep(0.001)` or a redundant loop). Rerun the perf test. Should fail. Fix. Should pass.",
                "This is the perf-regression cycle.",
                "Failure output includes the actual time vs threshold. You see the regression clearly. Remove the sleep — passes. This is exactly what a real perf-regression test does when someone accidentally slows down a hot path.",
            ),
            ex(
                "18-3",
                "For a C function on an embedded target (real or hypothetical): sketch a cycle-count-based regression test using DWT->CYCCNT. Note the trade-offs vs Python wall-clock timing.",
                "Cycle counts are deterministic on bare-metal ARM.",
                "```c\nuint32_t start = DWT->CYCCNT;\nfir_process(in, out, N, coeffs, NC);\nuint32_t cycles = DWT->CYCCNT - start;\nCHECK(cycles < 15000);\n```\nAdvantages: deterministic (no OS noise), tight thresholds possible, exact reproducibility. Disadvantages: requires hardware or accurate simulator, more setup than Python.",
            ),
            ex(
                "18-4",
                "Discuss in `regression-lab/perf-strategy.md`: which functions in a hypothetical DSP project would you write perf regression tests for, and which would you skip? Justify.",
                "Not everything deserves a perf test — noise makes them low-value for cold-path code.",
                "Write perf tests for: audio callbacks, ISRs, tight inner loops, functions called per-frame. Skip: initialization, configuration, one-time setup, error handlers. Rule of thumb: if the function runs 1000+ times per second in production, it deserves a perf test. If it runs once per boot, skip.",
            ),
        ],
    },
    {
        "id": "19",
        "title": "Use Case: API / Contract Regression",
        "level": "Advanced",
        "summary": "Preserving the public interface: argument names, types, return shapes. What third-party callers see.",
        "body": md("""
## The API contract
When your code is USED by others (another team, external customer, downstream service), the public API is a **contract**. Breaking it silently breaks consumers.

API regression tests guard the contract.

## What "the API" includes
- Function names, argument names, argument order, defaults
- Argument types and return types
- Exception types thrown
- Return value shapes (dict keys, tuple order, array dtype/shape)
- Behavior invariants documented in the API

## Simple API regression test
```python
import inspect
from myapi import process

def test_process_signature():
    sig = inspect.signature(process)
    assert list(sig.parameters.keys()) == ['input', 'sample_rate', 'options']
    assert sig.parameters['sample_rate'].default == 48000
```
Now if someone renames or reorders arguments, the test fails.

## Return-shape regression
```python
def test_process_returns_expected_shape():
    result = process(...)
    assert isinstance(result, dict)
    assert set(result.keys()) == {'output', 'peak', 'rms'}
    assert isinstance(result['output'], np.ndarray)
    assert result['output'].dtype == np.float32
```

## Exception contract
```python
def test_process_raises_valueerror_on_bad_sample_rate():
    with pytest.raises(ValueError):
        process(..., sample_rate=-1)
```
The type of exception is part of the contract.

## Snapshot-based API surface tests
For large APIs, snapshot the entire signature:
```python
def test_api_surface_snapshot():
    from mymodule import __all__
    signatures = {name: str(inspect.signature(getattr(mymodule, name)))
                  for name in __all__}
    expected = json.loads(Path('api_snapshot.json').read_text())
    assert signatures == expected
```
Any API change fails the test. Reviewer sees exactly what changed.

## For C libraries
C APIs are locked by header files. The tests are:
- **Header stability**: `diff include/public.h old_public.h` in CI — must be empty
- **ABI stability**: tools like `libabigail` compare compiled binary signatures
- **Symbol stability**: `nm libfoo.so` — the exported symbol list must not change

## For CLI tools
- **Argument parsing**: test that `--foo bar` still works and does the same thing
- **Output format**: snapshot the output of `mycli --help`
- **Exit codes**: `mycli invalid` → non-zero, matches documented code

## Semantic versioning discipline
API changes should be reflected in version numbers:
- **Patch** (1.2.3 → 1.2.4): no API change, bug fix or performance only
- **Minor** (1.2.3 → 1.3.0): additive API change (new functions), no removal
- **Major** (1.2.3 → 2.0.0): breaking change

API regression tests should be tied to these transitions. Between patches, tests should never break. Between minors, only ADDITIVE changes to snapshots are OK. Between majors, the snapshot legitimately updates — but reviewers must sign off.

## The trap: over-testing internals
Do NOT snapshot the entire codebase's internal signatures. Only snapshot the PUBLIC API — the surface external callers depend on. Otherwise your tests break every time you refactor internals, defeating the purpose.

Where "public" is: exported symbols in `__all__` (Python), public headers in `include/` (C), public methods in a class, documented endpoints in a service.
"""),
        "exercises": [
            ex(
                "19-1",
                "Take a function you have written. In `regression-lab/python/test_api.py`, use `inspect.signature` to write a test that asserts its argument names, order, and defaults.",
                "`inspect.signature(fn).parameters` gives you an ordered dict.",
                "```python\nimport inspect\nfrom mymath import divide\n\ndef test_divide_signature():\n    sig = inspect.signature(divide)\n    params = list(sig.parameters.keys())\n    assert params == ['a', 'b']\n    assert sig.parameters['b'].default == inspect.Parameter.empty\n```\nNow renaming `a` to `x` fails the test — reviewer sees the API break.",
            ),
            ex(
                "19-2",
                "Write a return-shape test for a function that returns a dict or tuple. Assert both the structure AND the types of the values.",
                "For dicts, check keys AND types. For arrays, check dtype AND shape.",
                "```python\ndef test_stats_return_shape():\n    result = compute_stats([1.0, 2.0, 3.0])\n    assert set(result.keys()) == {'mean', 'std', 'n'}\n    assert isinstance(result['mean'], float)\n    assert isinstance(result['n'], int)\n```",
            ),
            ex(
                "19-3",
                "Discuss in `regression-lab/api-vs-internal.md`: what makes an API 'public' vs 'internal'? Give 3 examples of things you SHOULD test for API stability, and 3 things you should NOT test (because they are internal).",
                "The line is fuzzy but real.",
                "PUBLIC (test): exported functions in `__init__.py`, documented CLI flags, HTTP endpoint schemas, public class methods. INTERNAL (do not test at API level): private methods starting with _, module-internal helpers, refactorable implementation details, temporary caches. Rule: if a consumer would notice a change, it is public. If only YOU would notice, it is internal.",
            ),
        ],
    },
    # ────────────────────── PHASE 5: AUTOMATION ──────────────────────
    {
        "id": "20",
        "title": "CI/CD Integration",
        "level": "Advanced",
        "summary": "Run your regression suite on every push. No test that runs only 'when I remember' can catch regressions.",
        "body": md("""
## The CI principle
A test suite that runs on a developer's laptop is worth ~30% of what it could be. The other 70% comes from running it AUTOMATICALLY on every push, every PR, every merge.

## Minimum viable CI: GitHub Actions
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pytest numpy
      - run: pytest -v
```
Commit this. On the next push, tests run in GitHub's cloud. Red X on the commit if any test fails.

## What CI adds beyond local testing
- **Enforced**: cannot merge if red (with branch protection)
- **Consistent environment**: same OS, same Python version, same deps every time
- **Multi-platform**: one workflow can test on Linux, macOS, Windows in parallel
- **History**: every run is logged; you can bisect regressions across time
- **Peer visibility**: reviewers see green/red before approving

## The essential features of good CI
### Fail fast
```yaml
- run: pytest -x    # stop at first failure
```
Or run linting before tests — cheaper failures first.

### Parallelism
Run test files in parallel with `pytest-xdist`:
```yaml
- run: pytest -n auto
```

### Cache dependencies
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```
Speeds up runs by minutes.

### Multiple platforms
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python: ['3.10', '3.11', '3.12']
runs-on: ${{ matrix.os }}
```

### Artifacts (logs, coverage)
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: junit.xml
```

## For C projects
```yaml
- run: |
    make test
    ./build/test_all
```
Or with CMake:
```yaml
- run: |
    cmake -B build
    cmake --build build
    ctest --test-dir build --output-on-failure
```

## For embedded (cross-compile in CI)
```yaml
- run: |
    sudo apt install gcc-arm-none-eabi
    make TARGET=cortex-m4 test-host   # host-side tests
    make TARGET=cortex-m4 build       # cross-compile, artifact only
```
Cross-compiled firmware builds in CI — hardware tests still need a physical device or simulator.

## Branch protection: the enforcement mechanism
In GitHub: Settings → Branches → Protect `main`:
- Require status checks (CI) before merging
- Require review before merging
- Disallow direct pushes

Now nobody can push a red commit to main. Regression tests actually protect the codebase.

## The failure mode: green tests that mean nothing
CI is only useful if the tests are:
- Non-trivial (not just `assert True`)
- Meaningful (protect real behavior)
- Trusted (not routinely ignored due to flakiness)

Every organization has some legacy tests that are "green because they were disabled after failing." Audit yours periodically. See Module 22 (flaky tests) and Module 23 (suite hygiene).

## Notification discipline
- On failure: notify the author (Slack, email)
- Do NOT spam the channel for every push — signal fatigue
- Do notify on `main` branch failures — those need immediate attention

## The workflow, end to end
1. Developer pushes a branch
2. CI runs tests in ~2 minutes
3. If green: PR reviewer sees green check, reviews code
4. If red: developer sees failure, fixes locally, force-pushes
5. Once green + approved: merge
6. Post-merge CI on `main` runs — if red, someone is paged

No regression escapes this flow. That is the whole point of CI.
"""),
        "exercises": [
            ex(
                "20-1",
                "Create `.github/workflows/tests.yml` for a Python project (real or fake). Include: checkout, Python setup, install pytest, run pytest. Commit and push. Watch CI run in GitHub's Actions tab.",
                "The YAML from the module is a starting point.",
                "First green CI is a milestone. From here on, every push runs your tests automatically. This is the single highest-leverage change you can make to a project's quality.",
            ),
            ex(
                "20-2",
                "Add branch protection to your `main` branch requiring CI to pass. Try to merge a PR with a failing test — GitHub blocks the merge. Fix the test, push, watch it merge.",
                "Settings → Branches → Add rule → Require status checks.",
                "Merge blocked with 'Required status checks have not passed.' After fix, checks pass, merge button enabled. This is the mechanism that MAKES regression tests actually protect main.",
            ),
            ex(
                "20-3",
                "Add caching for pip to your workflow. Measure the CI run time before and after. Note the speedup.",
                "Cache action stores dependencies between runs.",
                "First run with cache: cache miss, same as before. Second run: cache hit, dependencies restored in seconds. On a project with many deps, this saves minutes per CI run.",
            ),
            ex(
                "20-4",
                "For a C project (make-based), write a workflow that installs gcc, runs make test, and asserts exit code 0. Compare complexity to the Python workflow.",
                "Same principle, different toolchain.",
                "```yaml\nsteps:\n  - uses: actions/checkout@v4\n  - run: sudo apt install -y gcc make\n  - run: make test\n```\nComparable simplicity. C in CI is not harder than Python — the concepts transfer directly.",
            ),
        ],
    },
    {
        "id": "21",
        "title": "Bisecting a Regression (git bisect)",
        "level": "Advanced",
        "summary": "A bug appeared. Between commits A and Z, something broke. Bisect finds the exact commit in log(N) steps.",
        "body": md("""
## The problem
- Commit A (last week) — feature X worked
- Commit Z (today) — feature X broken
- Between them: 200 commits

Manually checking each: 200 tries. With bisect: ~8 tries (log2(200)).

## The manual workflow
```bash
git bisect start
git bisect bad                    # current commit is broken
git bisect good <commit-A-hash>   # last known good

# git checks out a commit in the middle
# you test — does feature X work?
git bisect good     # if it works
# or
git bisect bad      # if it does not

# repeat until git says 'X is the first bad commit'

git bisect reset    # done
```

## The automated workflow (with regression tests)
This is where regression tests SHINE. If you have a test that reliably fails on broken commits and passes on good ones:
```bash
git bisect start
git bisect bad
git bisect good <commit-A-hash>
git bisect run pytest test_that_shows_the_bug.py
```
Git bisects automatically. On big repos with slow tests, this can take minutes instead of hours.

## The `git bisect run` script
Any command that:
- Exits 0 if the commit is "good"
- Exits 1-124 or 126-127 if "bad"
- Exits 125 if it cannot be tested (build broken, skip)

Works with git bisect run. Examples:
```bash
git bisect run pytest -xvs test_regression.py::test_specific_case
git bisect run bash scripts/reproduce_bug.sh
git bisect run make test
```

## Real workflow
```bash
# You discovered the bug. Write a minimal reproducer FIRST.
cat > repro.sh << 'EOF'
#!/bin/bash
make test-fir > /dev/null 2>&1
grep -q "FAIL: fir_test" build/test.log || exit 0  # good if no FAIL
exit 1  # bad if FAIL
EOF
chmod +x repro.sh

# Now bisect
git bisect start HEAD v1.2.3
git bisect run ./repro.sh

# Git prints:
# abc1234 is the first bad commit
# Author: ...
# Date:   ...
# Message: refactor FIR loop unrolling
```
You now know the exact commit that introduced the regression. Time to investigate.

## Handling flaky tests during bisect
If the reproducer is flaky (sometimes passes, sometimes fails), bisect will produce garbage. Options:
- Fix the flakiness FIRST (best)
- Run the test N times per commit and use majority vote
- Use a stricter test that is deterministic

## Combining bisect with automated reverts
Once you have the bad commit:
```bash
git revert abc1234
git push
```
Now the regression is undone. You can fix it properly in a follow-up.

## Bisect on old regressions (weeks / months later)
Bisect can go back arbitrarily far. But older commits may have build issues, dependency mismatches, or removed test infrastructure. Common pain:
- Old commit's build depends on a Python version you no longer have
- Old commit's tests were written before a dependency existed
- Old commit's reproducer script does not exist yet

Solution: adapt the reproducer to work on OLD commits (avoid new dependencies).

## The moral
Bisect + regression tests = superpower. You do not need to be smart about finding regressions. You need a reproducer and 5 minutes.

The teams that suffer weeks of "when did this break?" investigations are the ones without good regression tests AND without bisect discipline.

## Alternatives to git bisect
- **Automated bisection services** (some CI systems): every commit is tested, so you already know which commit introduced a failure — no manual bisect needed
- **CI history**: if you have build history, look for the first red build
- **Log analysis**: sometimes a specific error message narrows things faster than bisect

For anything nontrivial, bisect is still the most reliable tool.
"""),
        "exercises": [
            ex(
                "21-1",
                "Create a small git repo with 10 commits, each modifying a `calc.py`. On commit 5, deliberately introduce a bug in `add`. Commit through 10 without noticing. Now use `git bisect` manually (mark good/bad) to find commit 5. Time yourself.",
                "This is the classic manual bisect exercise.",
                "You mark HEAD as bad, commit 1 as good. Git checks out ~commit 5. You test. Repeat. In ~4 steps, git identifies commit 5. Feel the log2 speedup vs manually checking all 10.",
            ),
            ex(
                "21-2",
                "Write a pytest test that fails on the buggy `add` but passes on correct versions. Use `git bisect run pytest test_add.py` to automate the process from Exercise 21-1. Compare to manual bisect.",
                "The `run` subcommand makes bisect automatic given a reliable reproducer.",
                "```bash\ngit bisect start HEAD~10 HEAD\ngit bisect run pytest test_add.py\n```\nGit walks the history, running pytest at each candidate. In seconds, prints 'commit 5 is first bad.' No manual intervention.",
            ),
            ex(
                "21-3",
                "Discuss in `regression-lab/bisect-notes.md`: what makes a good bisect reproducer? Why must it be deterministic? What happens if it is flaky?",
                "This is the crux of practical bisect.",
                "Good reproducer: exits 0 on good, non-zero on bad, deterministically. Runs in seconds. Independent of environment state. If flaky, bisect will misclassify some commits, giving a wrong answer. If slow, bisect takes hours. Investing in a fast, reliable reproducer BEFORE bisecting pays for itself 10x.",
            ),
        ],
    },
    {
        "id": "22",
        "title": "Flaky Tests and How to Fix Them",
        "level": "Advanced",
        "summary": "A test that sometimes passes and sometimes fails is worse than no test. It teaches your team to ignore failures.",
        "body": md("""
## Why flaky tests are worse than missing tests
- **Missing test**: you know you have no coverage. You do not trust that area. Correct mental model.
- **Flaky test**: you think you have coverage. But when it fails, everyone shrugs and reruns CI. Real failures get ignored. Bugs slip through.

Flaky tests actively damage a team's testing culture. Fix them ruthlessly.

## The five common causes
### 1. Nondeterminism in the code
Random numbers, timestamps, hash iteration order, uninitialized memory.
Fix: seed randomness, mock time, sort collections, initialize.

### 2. Test order dependence
Global state leaks between tests.
Fix: no globals in tests. Isolate. Use `pytest-randomly` to shake these out.

### 3. Timing / race conditions
Test starts a background task, then checks a result before the task finishes.
Fix: use synchronization primitives (Events, callbacks), not `time.sleep(0.1)`.

### 4. Resource contention
Multiple tests write to the same file, port, or database. When they run in parallel, they collide.
Fix: `tmp_path` fixtures, unique ports, per-test resources.

### 5. Environmental drift
Test passes on your machine, fails in CI. Different OS, different Python version, different filesystem.
Fix: pin versions, avoid OS-specific paths, test in the CI environment.

## Detecting flaky tests
Run the suite N times:
```bash
for i in {1..50}; do
  pytest -q --tb=no || echo "FAIL run $i"
done
```
Or use a dedicated tool:
```bash
pytest --count=50 test_suspect.py::test_flaky_candidate   # pytest-repeat
```
Any test that varies is flaky.

## Detecting order dependence
```bash
pip install pytest-randomly
pytest    # runs in random order every time
```
Tests that pass sometimes and fail sometimes based on order are order-dependent.

## Debugging a flaky test
1. **Reproduce it** — run in a loop until it fails, capture the failure
2. **Compare passing vs failing runs** — what differs? Timing? Order? Data?
3. **Add logging** — print state at every step to see divergence
4. **Isolate** — comment out other tests, isolate to smallest failing case
5. **Understand ROOT cause** — do not just add a retry

## The anti-fix: retry until pass
Some CI systems have retry-on-failure. This HIDES flakiness. The test becomes silently green even when it detects real bugs.

Retries are ONLY acceptable for provably-external flakiness (e.g., network calls to third-party services) and even then, log every retry so you can see the trend.

## Quarantine, then fix
When you detect a flaky test, immediately:
1. Mark it as flaky (pytest: `@pytest.mark.flaky` with a skip decorator)
2. Move it to a quarantine bucket that does NOT fail the build
3. File a ticket to actually fix it
4. Do NOT delete — quarantine keeps it visible

Then on a schedule (weekly / monthly), work through the quarantine and fix or delete each test.

## Prevention
- Write tests with determinism in mind (Module 08)
- Run `pytest-randomly` in CI to catch order dependence early
- Do not use `time.sleep(...)` in tests unless you can prove it is the only option
- Do not use globals
- Test in CI-like environments locally when possible

## The cultural signal
Teams that tolerate flaky tests are teams whose test suite becomes ignored. Teams that treat flakiness as urgent build a suite everyone trusts. This is a leadership / cultural issue, not a technical one.

## Real story
A team had 12 flaky tests. Developers routinely reran CI on failure. One day, a real regression caused a production incident. Investigation: the regression test that SHOULD have caught it had failed on the introducing PR. Everyone had ignored it as "the usual flakiness." Cost: several days of debugging and a customer-facing outage. Fix: dedicated flakiness sprint, quarantine, systematic fixing.

This happens everywhere. Do not let it happen to you.
"""),
        "exercises": [
            ex(
                "22-1",
                "Write a deliberately flaky test using `random.random()` without seeding. Run it 20 times. Count failures. This teaches you to feel flakiness firsthand.",
                "The point is to observe the pattern.",
                "Typical run: 40-60% failure rate. Every rerun gives a different answer. You can immediately see why this destroys trust in a test suite — nobody knows what a red mark actually means.",
            ),
            ex(
                "22-2",
                "Fix the flakiness by seeding `random.seed(42)` at the start of the test. Rerun 20 times. Same result every time. Discuss why this specific fix works.",
                "Determinism = reproducibility.",
                "With seeded random, the sequence is identical every run. The test either always passes or always fails. If it fails, you have a real bug to investigate. If it passes, you have real evidence the code works for that specific case.",
            ),
            ex(
                "22-3",
                "Install `pytest-randomly` and run your test suite. Any tests that were order-dependent will start failing. This is the recommended way to catch order-dependence bugs.",
                "`pip install pytest-randomly` then just run pytest.",
                "If your tests are properly isolated, results are unchanged. If any test depended on order (globals, shared state, module-level side effects), you will see new failures. Fix those tests — they were already buggy, you just did not know.",
            ),
            ex(
                "22-4",
                "Write a policy document `regression-lab/flakiness-policy.md`: how does your team handle a newly detected flaky test? Who quarantines? What is the SLA for fixing? What is the escalation?",
                "There is no universal right answer — this is about creating team discipline.",
                "Sample policy: (1) Flaky test → immediate quarantine + ticket filed. (2) Ticket priority = P1. (3) Assigned to test author, or code owner if author unavailable. (4) Fix or delete within 1 week. (5) If not fixed in 1 week, escalate to tech lead. (6) Quarantine bucket audited monthly. Teams that follow policies like this have low flakiness. Teams that do not accumulate technical debt.",
            ),
        ],
    },
    {
        "id": "23",
        "title": "Test Suite Maintenance & Hygiene",
        "level": "Advanced",
        "summary": "A suite is a live system. Prune, refactor, document. Coverage is not quality.",
        "body": md("""
## Suites rot
Over years, test suites accumulate:
- Obsolete tests for removed features
- Duplicated tests covering the same thing
- Slow tests everyone skips
- Commented-out tests nobody remembers why
- Cryptic names from urgent fixes

Left unchecked, the suite becomes an obstacle rather than a safety net.

## The audit checklist
Once a quarter (or before major work), audit:
- **Runtime**: is the suite still fast enough? If unit suite > 60 seconds, split slow ones out.
- **Coverage**: measure with `pytest --cov` — but do not chase 100% blindly (see below).
- **Skipped tests**: `pytest -rs` shows skips. Why are they skipped? Fix or delete.
- **Failing tests**: any tests currently failing? Xfail vs actually broken?
- **Test names**: any tests you cannot understand at a glance? Rename.
- **Duplication**: are three tests doing basically the same thing?
- **Flakiness**: any tests known to be flaky? Quarantine and fix (Module 22).

## Coverage vs quality
Coverage tells you what code is EXECUTED by tests. It does NOT tell you if the tests are meaningful.
```python
def test_add_covers_everything():
    add(1, 2)   # 100% line coverage of add() — but no assertion!
```
This test passes and gives 100% coverage on `add`. It also catches no bugs.

Use coverage as a **floor** (low coverage = definitely missing tests) not as a **ceiling** (high coverage != good tests).

## Deleting tests
Legitimate reasons to delete:
- Feature removed → tests for it are dead code
- Test is a superset of another (redundant coverage)
- Test proved to be worthless (never caught a real bug, low coverage value)
- Test was flaky and not worth fixing

Illegitimate reasons:
- "It fails and I do not know why" — investigate first (Module 04)
- "It is slow" — first try to speed it up
- "I do not understand what it does" — rename and document instead

Every deletion should have a commit message explaining WHY.

## Refactoring tests
Same principles as production code:
- Extract common setup into fixtures
- Rename for clarity
- Split long tests into focused ones
- Merge trivial duplicates
- Improve failure messages

Do not refactor tests in the same PR as production changes — separate concerns.

## Documenting the suite
```
tests/
  README.md          # how to run, what conventions
  goldens/README.md  # what each golden is, how to regen
  slow/              # tests > 1 second — separate from fast suite
  regression/        # bug-fix regression tests
  smoke/             # quick sanity checks
```

The `tests/README.md` should answer:
- How do I run tests?
- What conventions do we follow (naming, structure)?
- How do I add a new test?
- How do I run only fast tests? Only slow?
- How do I regenerate goldens?
- Who owns the flaky test policy?

## Marking and categorization
```python
@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.regression_2026_09
def test_something():
    ...
```
Then:
```bash
pytest -m "not slow"                    # fast tests only
pytest -m "integration"                 # integration tests only
pytest -m "regression_2026_09"          # specific bug guard set
```

## The "why did we add this" problem
Every test should be traceable to a reason:
- Bug fix (link to issue)
- New feature (link to PR)
- Refactor safety net (link to design doc)
- Property invariant (documented in code)

Tests without traceable origin become mysterious. They eventually get deleted OR they linger unloved for years. Neither is good.

## The 80/20 of hygiene
If you do only THREE things:
1. **Delete truly dead tests** (feature removed, redundant coverage)
2. **Rename cryptic tests** to describe what they protect
3. **Quarantine and fix flakies** aggressively

You will have a healthy suite. Everything else is refinement.

## When to add a whole new test file
- New module → new test file
- New category of tests → new file (e.g., `test_performance.py`)
- Existing file > 500 lines → split by concern

Do NOT split just because the file is getting long. Split by cohesion.
"""),
        "exercises": [
            ex(
                "23-1",
                "Take a real test suite (yours or a project you know). Run `pytest --collect-only` to list all tests. Skim the names. Count how many you cannot immediately understand what they protect. This is your rename backlog.",
                "Just observe — do not fix yet.",
                "Typical result: 20-40% of tests in a legacy suite have unclear names. That is your priority list for the rename pass. Just knowing this number is the first step.",
            ),
            ex(
                "23-2",
                "Run `pytest --cov=your_module` (with pytest-cov installed). Look at the coverage report. Find one uncovered function. Now: is it uncovered because it is trivial, dead code, or genuinely untested? Decide the action for each case.",
                "Coverage is a starting question, not an answer.",
                "Trivial (e.g., simple getter): may not need a test. Dead: delete the code. Untested: add a test. The report is a menu of investigations, not a to-do list. Blindly writing tests to boost coverage number = bad.",
            ),
            ex(
                "23-3",
                "Write a `tests/README.md` for your `regression-lab/`. Include: how to run, how to add a new test, where goldens live, what conventions you follow (naming, AAA structure).",
                "This is the doc your future self needs.",
                "A 20-line README that answers 'how do I add a test here?' saves hours of future confusion. Include example commands (`pytest`, `pytest -k pattern`), file layout conventions, and any project-specific patterns (like the goldens regeneration workflow).",
            ),
            ex(
                "23-4",
                "Design a quarterly test-suite hygiene sprint. In `regression-lab/hygiene-sprint.md`, write: what activities happen, who does them, how much time budget, what deliverables.",
                "Ongoing hygiene is a practice, not a one-off.",
                "Sample: 1 week per quarter, dedicated. Activities: audit flakies (2 days), rename cryptic tests (2 days), delete dead tests (1 day). Deliverables: shortened runtime by X%, flakiness count down to zero, all tests have understandable names. Assign a rotating owner. Publish a before/after report.",
            ),
        ],
    },
    # ────────────────────── PHASE 6: CAPSTONE ──────────────────────
    {
        "id": "24",
        "title": "Capstone: Build a Full Regression Suite",
        "level": "Expert",
        "summary": "Take a small module. Apply every concept in the course. Ship it with CI, goldens, docs, and confidence.",
        "body": md("""
## The capstone challenge
Pick a small module (yours or built for this course). Build a COMPLETE regression suite for it, applying every concept from the course.

Suggested module: a DC blocker filter (`dc_block.c` + `dc_block.h`) — simple enough to fully test, real enough to matter.

## The deliverables
### 1. The module itself
`regression-lab/capstone/dc_block.{c,h,py}` — a straightforward implementation. If you already have one from another course, reuse it.

### 2. Bug-fix regression test
Introduce a bug intentionally, write a test that catches it, fix, document.

### 3. Refactor safety-net tests
5+ tests that lock down behavior. Refactor the implementation while all tests stay green.

### 4. Numerical (golden) regression test
Python generates reference. C (or Python) implementation must match within tolerance. Golden files committed with a README.

### 5. Performance regression test
Measure baseline. Assert within 2x threshold.

### 6. API regression test
Signature snapshot for the public interface.

### 7. CI integration
`.github/workflows/tests.yml` that runs everything on push. Branch protection enabled.

### 8. Documentation
`tests/README.md` describing: how to run, what each test category protects, how to regenerate goldens, how to update baselines.

## The acceptance criteria (self-scored)
Score each 1-3 (basic / good / excellent):
- [ ] All 5 test types present and passing
- [ ] Every test follows AAA structure
- [ ] Tolerances are measured and justified in comments
- [ ] Golden generator script works and is documented
- [ ] Performance baseline is measured and committed
- [ ] Suite runs in < 10 seconds
- [ ] Zero flaky tests (verified by 20 consecutive runs)
- [ ] CI is green and blocks merges on failure
- [ ] `tests/README.md` explains everything a new team member needs
- [ ] Every test name is understandable without reading the body

Target: ≥ 24/30 total. Below 20/30 → address the weak areas before calling it done.

## The reflective exercise
After finishing, revisit `regression-lab/before-and-after.md` (from Module 00). Write your NEW definition of a regression test under a heading "After the course". Compare to your original.

## Where to take this next
- **Apply to a real project**: pick one production module, spend a week retrofitting a full suite. Measure how it changes your confidence in that module.
- **Team practice**: run a workshop teaching this pattern to teammates. Their questions will refine your understanding.
- **Build a template**: create a project scaffold with pre-configured pytest, CI, goldens folder, and README. Reuse for every new project.

## The mindset shift
You started the course thinking "regression tests are extra work I should probably do." You leave thinking "regression tests are the infrastructure that lets me change code without fear." That is the shift. Everything else was mechanics.
"""),
        "exercises": [
            ex(
                "24-1",
                "Implement the DC blocker (`y[n] = x[n] - x[n-1] + alpha*y[n-1]`) in your language of choice. In `regression-lab/capstone/`. This is the code under test.",
                "The DSP formula for a first-order DC blocker with pole at alpha (0 < alpha < 1).",
                "```python\n# regression-lab/capstone/dc_block.py\ndef dc_block(x, alpha=0.995):\n    y = [0.0] * len(x)\n    prev_x = 0.0\n    for n in range(len(x)):\n        y[n] = x[n] - prev_x + (alpha * (y[n-1] if n > 0 else 0.0))\n        prev_x = x[n]\n    return y\n```\nSimple. Testable. Real algorithm.",
            ),
            ex(
                "24-2",
                "Write 5 tests locking down behavior: (1) impulse response first samples, (2) DC input settles toward zero, (3) length preservation, (4) empty input, (5) alpha=0 behaves as differentiator. All AAA structure.",
                "Cover the branches and properties you can see.",
                "Five focused tests, all following AAA. Each name describes what it protects. If future refactor breaks any of these, the failing test tells the story immediately. This is your safety net.",
            ),
            ex(
                "24-3",
                "Generate a numerical golden: 100-sample DC-biased sine wave input → apply reference DC blocker in Python → save both `.npy` files. Write a golden-comparison test with tolerance 1e-6.",
                "The pattern from Module 12.",
                "Python reference and production impl agree within 1e-6. This test catches any numerical drift — including subtle refactor breakages the property tests might miss.",
            ),
            ex(
                "24-4",
                "Add a performance test: measure baseline (median of 50 runs), assert `< baseline * 2`. Introduce an artificial slowdown, watch it fail. Remove slowdown, watch it pass.",
                "Use `time.perf_counter` and `statistics.median`.",
                "Perf test in place. If you (or a teammate) accidentally makes the DC blocker 4x slower, this test fires. It caught the regression before customers did.",
            ),
            ex(
                "24-5",
                "Add API regression test: use `inspect.signature` (or the C-equivalent header diff) to snapshot the public function's signature. Rename a parameter — watch the test fail.",
                "Guards the contract, not just behavior.",
                "Signature captured. Rename `alpha` to `pole` — test fails immediately. This forces API changes to be intentional and reviewed, not accidental.",
            ),
            ex(
                "24-6",
                "Set up CI: `.github/workflows/tests.yml` that runs your full capstone suite on push. Enable branch protection. Verify a red PR cannot be merged.",
                "This makes the whole suite real — not just theoretical.",
                "CI green on your main branch. Red PRs blocked. The entire regression suite you built now protects the module on every change from every contributor. This is production-quality practice.",
            ),
            ex(
                "24-7",
                "Write `regression-lab/capstone/tests/README.md`: how to run each test category, how to regenerate goldens, how to update baselines. Then revisit `before-and-after.md` — write your NEW definition of a regression test.",
                "Documentation + reflection. Ship it.",
                "README is discoverable and complete. Your 'After' definition should mention: preservation of behavior, categories (bug-fix / refactor / numerical / performance / API), the RED-GREEN discipline, the role of CI. Compare to 'Before' — you now speak the language.",
            ),
        ],
    },
    # ────────────────────── DRILLS ──────────────────────
    {
        "id": "drills",
        "title": "Daily Drills",
        "level": "All levels",
        "summary": "Quick reps to build regression-testing muscle memory. One per day.",
        "body": md("""
## How to use drills
One drill per day between (or after) modules. Each is small — 5-10 minutes. Repetition builds fluency.
"""),
        "exercises": [
            ex("D-01", "Write a one-sentence definition of 'regression test'. Compare to yesterday's. Refine.", "Repetition sharpens definitions.", "Progressively cleaner definitions over time. Notice which nuances stick."),
            ex("D-02", "Pick a function you use today. Ask: could I write a regression test for it in 2 minutes? Try it.", "Muscle memory for test setup.", "Some functions test in 2 minutes; others reveal setup complexity. Both are useful data."),
            ex("D-03", "In pytest, write a parametrized test with 3 cases in under 5 minutes.", "Fluency in the API.", "Parametrize becomes second-nature. You write it without checking docs."),
            ex("D-04", "Take an assertion in production code. Convert it to a proper test.", "Assertion → test conversion drill.", "Runtime guards get external verification. Better test suite, same production code."),
            ex("D-05", "Read one test in your codebase. Score it against the 7 criteria (Module 09).", "Critical reading practice.", "Most tests score 4-5/7. Notice the pattern — this is your team's baseline."),
            ex("D-06", "Regenerate a golden file (any project). Inspect the diff. Was it justified?", "Golden-update discipline.", "Sometimes the diff is nothing (bit-exact). Sometimes it is huge — investigate."),
            ex("D-07", "Run your test suite 5 times. Any flaky tests? Investigate the top one.", "Flakiness detection habit.", "You either find zero (great) or start a quarantine list (also great)."),
            ex("D-08", "Write a git bisect run script for a fake bug in a small repo. Confirm it identifies the commit.", "Bisect fluency.", "Bisect becomes a routine tool, not a heroic effort."),
            ex("D-09", "Add one new test to your suite today. Name it descriptively. Follow AAA.", "Habitual test-writing.", "Suite grows by ~250 tests per year at 1/day. Compounding coverage."),
            ex("D-10", "Look at your CI dashboard. When did tests last take > 60 seconds? Investigate if yes.", "Suite hygiene habit.", "You catch runtime creep before it becomes a problem."),
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════
# HTML SHELL
# ═══════════════════════════════════════════════════════════════════════

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Regression Testing — Theory & Practice</title>
  <style>
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --surface2: #243044;
  --text: #e7ecf3;
  --muted: #9aa8bc;
  --accent: #14b8a6;
  --accent2: #5eead4;
  --warn: #fbbf24;
  --ok: #4ade80;
  --border: #2d3a4f;
  --ex: #1e2a3d;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); line-height: 1.55; }
a { color: var(--accent); }
.layout { display: grid; grid-template-columns: 300px 1fr; min-height: 100vh; }
nav.sidebar {
  background: var(--surface); border-right: 1px solid var(--border);
  padding: 1rem; overflow-y: auto; position: sticky; top: 0; height: 100vh;
}
nav.sidebar h1 { font-size: 1.05rem; margin: 0 0 0.25rem; line-height: 1.3; }
nav.sidebar .sub { font-size: 0.78rem; color: var(--muted); margin-bottom: 1rem; }
nav.sidebar input {
  width: 100%; padding: 0.45rem 0.6rem; border-radius: 6px;
  border: 1px solid var(--border); background: var(--bg); color: var(--text); margin-bottom: 0.75rem;
}
nav.sidebar ul { list-style: none; padding: 0; margin: 0; }
nav.sidebar li { margin-bottom: 0.15rem; }
nav.sidebar button.module-link {
  width: 100%; text-align: left; background: transparent; border: none;
  color: var(--text); padding: 0.35rem 0.5rem; border-radius: 6px;
  cursor: pointer; font-size: 0.82rem;
}
nav.sidebar button.module-link:hover { background: var(--surface2); }
nav.sidebar button.module-link.active { background: var(--accent); color: #061018; font-weight: 600; }
nav.sidebar .level {
  font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.04em;
  color: var(--muted); margin-top: 0.75rem; margin-bottom: 0.25rem;
}
.progress-wrap { margin: 1rem 0; font-size: 0.75rem; color: var(--muted); }
.progress-bar { height: 6px; background: var(--bg); border-radius: 99px; overflow: hidden; margin-top: 0.35rem; }
.progress-bar > div {
  height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2));
  width: 0%; transition: width 0.3s ease;
}
main { padding: 1.5rem 2rem 4rem; max-width: 920px; }
.hero { margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
.hero h2 { margin: 0 0 0.5rem; font-size: 1.75rem; }
.hero p { color: var(--muted); margin: 0; }
.badge {
  display: inline-block; font-size: 0.7rem; padding: 0.15rem 0.45rem;
  border-radius: 4px; background: var(--surface2); color: var(--accent2); margin-right: 0.35rem;
}
.lesson h3 { margin-top: 1.5rem; color: var(--accent2); }
.lesson h4 { margin-top: 1rem; }
.lesson pre.code-block {
  background: #0a0e14; border: 1px solid var(--border); border-radius: 8px;
  padding: 0.85rem 1rem; overflow-x: auto; font-size: 0.82rem;
}
.lesson code { background: var(--surface2); padding: 0.1rem 0.35rem; border-radius: 4px; font-size: 0.88em; }
.exercise {
  background: var(--ex); border: 1px solid var(--border); border-left: 4px solid var(--accent);
  border-radius: 8px; padding: 1rem 1.1rem; margin: 1.25rem 0;
}
.exercise header { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.75rem; flex-wrap: wrap; }
.exercise h5 { margin: 0; font-size: 0.95rem; }
.exercise .ex-id { font-size: 0.72rem; color: var(--muted); font-family: ui-monospace, monospace; }
.exercise .prompt { margin: 0.75rem 0; }
.exercise .hint {
  font-size: 0.85rem; color: var(--muted); border-top: 1px dashed var(--border);
  padding-top: 0.65rem; margin-top: 0.65rem;
}
.exercise .actions { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }
button.btn { border: none; border-radius: 6px; padding: 0.45rem 0.85rem; cursor: pointer; font-size: 0.82rem; font-weight: 600; }
button.btn-primary { background: var(--accent); color: #061018; }
button.btn-ghost { background: var(--surface2); color: var(--text); }
button.btn-ok { background: #166534; color: #ecfdf5; }
.exercise.done { border-left-color: var(--ok); opacity: 0.92; }
.solution {
  display: none; margin-top: 0.85rem; padding: 0.85rem; background: #0a0e14;
  border-radius: 6px; border: 1px solid var(--border); white-space: pre-wrap;
  font-family: ui-monospace, Consolas, monospace; font-size: 0.8rem;
}
.solution.visible { display: block; }
.stretch { margin-top: 0.5rem; font-size: 0.82rem; color: var(--warn); }
@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  nav.sidebar { position: relative; height: auto; }
}
  </style>
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
          Open this file in any browser. Progress saves locally in <code>regression-lab/</code>.
          <strong>%%TOTAL%% exercises</strong> · concepts → practice → capstone · Python / C / C++ / MATLAB.
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
    window.COURSE_DATA = %%DATA%%;
  </script>
  <script>
const STORAGE_KEY = 'regression-testing-course-v1';

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); }
  catch { return {}; }
}
function saveProgress(p) { localStorage.setItem(STORAGE_KEY, JSON.stringify(p)); }
function countExercises(modules) { return modules.reduce((n, m) => n + (m.exercises?.length || 0), 0); }

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

    el.querySelector('.btn-solution').onclick = () => { el.querySelector('.solution').classList.add('visible'); };
    el.querySelector('.btn-hide').onclick = () => { el.querySelector('.solution').classList.remove('visible'); };
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
  </script>
</body>
</html>
"""


def main():
    course = {
        "title": "Regression Testing — Theory & Practice",
        "subtitle": "Concepts · Python · C · C++ · MATLAB · Goldens · CI · Bisect · Flakies · Capstone",
        "version": "2026.09",
        "modules": MODULES,
    }
    total = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(course, ensure_ascii=False)
    page = HTML_TEMPLATE.replace("%%DATA%%", data_json).replace("%%TOTAL%%", str(total))
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT} — {len(MODULES)} modules, {total} exercises")


if __name__ == "__main__":
    main()
