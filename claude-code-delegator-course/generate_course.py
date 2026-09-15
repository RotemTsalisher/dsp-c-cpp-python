#!/usr/bin/env python3
"""Generate index.html — 'Claude Code Works For Me' delegation course.
Mindset: you are the tech lead. Claude is the autonomous worker.
You define tasks, set guardrails, and review output — not type prompts."""
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
                out.append(
                    f'<pre class="code-block" data-lang="{html.escape(lang)}"><code>'
                )
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODULES — "Claude Code works FOR me" delegation paradigm
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MODULES = [
    # ══════════════════════════════════════════════════════════════════════
    # PRE-SETUP
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "00",
        "title": "Setting Up Your Worker",
        "level": "Pre-Setup",
        "summary": "Install Claude Code — not as your tool, but as your autonomous team member who needs an environment to work in.",
        "body": md("""
## The mindset from line one
You are not installing a coding assistant. You are **onboarding a junior developer** onto your team. This developer:
- Can read any file in the project
- Can write code and propose changes
- Can run builds and tests
- Works 24/7 if you set up headless/CI
- Follows written instructions (CLAUDE.md) to the letter
- Never gets tired, never forgets the rules you wrote down

Your job from now on: **write good instructions, define clear acceptance criteria, and review the output.**

## Install the worker's environment
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

## Authenticate (one time)
```bash
claude
```
Follow the browser auth flow. This gives your worker access to Anthropic's models.

## Optional: VS Code extension
The extension is not for you to "use" Claude — it's a **monitoring window** where you can observe what Claude is doing. Think of it as watching your junior's screen.

## Model selection for delegation
When delegating, you choose the AI model upfront:
- **Fastest model**: bulk edits, documentation, simple formatting — cheap, fast
- **Default model**: feature implementation, bug fixes, test writing — balanced
- **Strongest model**: architecture review, safety analysis, concurrency debugging — expensive but thorough
You'll master this in Module 19.

## The project is the workspace
```bash
mkdir dsp-sandbox && cd dsp-sandbox
mkdir src tests scripts docs
echo "# DSP Library — Cortex-M4F target" > README.md
git init && git add -A && git commit -m "chore: init project"
```
This is the repo your worker will operate in. Everything it needs to know goes in files — not in your head.
"""),
        "exercises": [
            ex(
                "00-1",
                "Install Claude Code CLI and verify with `claude --version`. Frame this mentally: you are provisioning a workstation for a new team member.",
                "Same install as any course — but the mindset is different.",
                "Claude Code installed. You didn't install a 'tool' — you set up a worker's environment.",
            ),
            ex(
                "00-2",
                "Create the `dsp-sandbox` project with src/, tests/, scripts/, docs/. Initialize git. Commit. This is the repo your worker will operate in — make it clean.",
                "A clean repo is a clear workspace for your worker.",
                "Clean repo with initial commit. Your worker has a blank slate to operate in.",
            ),
            ex(
                "00-3",
                "Write a `README.md` with: project purpose, target hardware, build instructions (even if placeholder). This is the first thing your worker reads — make it useful.",
                "README is onboarding documentation for your worker.",
                "README has project context a new team member would need: what the project does, target platform, how to build.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # BEGINNER — The Delegation Mindset
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "01",
        "title": "The Mindset Shift: You're the Tech Lead",
        "level": "Beginner",
        "summary": "Stop thinking 'I use Claude Code.' Start thinking 'Claude Code implements my specifications.'",
        "body": md("""
## Two ways to think about AI coding tools

### ❌ "I'm working with Claude Code"
- You sit at the terminal typing prompts
- You iterate back-and-forth in conversation
- You accept/reject each diff manually
- Claude is a fancy autocomplete you babysit
- You are the **implementer**, Claude is the assistant

### ✅ "Claude Code works for me"
- You write a specification
- Claude implements it autonomously
- You review the finished result (like a PR review)
- Tests are your acceptance criteria — not manual inspection
- You are the **tech lead**, Claude is the implementer

## What changes in practice
| Old (assistant) | New (delegation) |
|---|---|
| "Add const to this pointer" | CLAUDE.md: "All input pointers must be const" |
| "Build and fix the errors" | Headless script runs build-fix loop unattended |
| Accepting diffs one by one | Reviewing a finished branch diff |
| Manual session per task | Scripted tasks triggered by events |
| You type the prompt | A script sends the prompt |
| You press y/n | `--allowedTools` pre-authorizes actions |

## The tech lead's job
1. **Specify**: what to build, constraints, acceptance criteria
2. **Delegate**: write the task brief, let Claude execute
3. **Review**: check the output against your criteria
4. **Iterate**: if not good enough, refine the spec — not the code

## You stop writing code. You start writing specifications.
"""),
        "exercises": [
            ex(
                "01-1",
                "Open Claude Code interactively. Ask: 'Create src/biquad.h with a BiquadState struct and biquad_process prototype.' Accept the result. Now CLOSE the session. Look at what you just did — you were the implementer guiding a tool. That's the OLD way.",
                "Do it the old way first so you feel the difference later.",
                "You created a file by hand-holding Claude through the process. Interactive, manual, babysitting. This is what we're moving AWAY from.",
            ),
            ex(
                "01-2",
                "Now do it the NEW way. Write a file `tasks/biquad-module.md` with a complete specification: struct fields, function signatures, constraints (C99, no malloc, const correctness), test criteria (impulse response check). Do NOT open Claude Code yet.",
                "Write the spec FIRST, before involving Claude at all.",
                "A markdown spec file that a human junior developer could also implement from. Clear, complete, testable. Claude hasn't been involved yet.",
            ),
            ex(
                "01-3",
                "Now delegate: run `claude -p 'Read tasks/biquad-module.md and implement everything specified. Build with gcc -std=c99 -Wall -Werror. Run tests. Report pass/fail.' --allowedTools Read,Edit,Bash` — headless, no babysitting.",
                "One command. Claude does everything. You review after.",
                "Claude read your spec, implemented, built, tested. You weren't in the loop. You review the result like a PR — not each individual edit.",
            ),
            ex(
                "01-4",
                "Review Claude's output. Run `git diff` to see everything it changed. Judge: did it meet your specification? If not, the problem is your spec — not Claude. Refine the spec file and re-run.",
                "When the output is wrong, fix the spec — not the code.",
                "You're reviewing a diff, not babysitting edits. If something's wrong, you update tasks/biquad-module.md and re-delegate. You never touch the implementation.",
            ),
        ],
    },
    {
        "id": "02",
        "title": "Writing Task Briefs, Not Prompts",
        "level": "Beginner",
        "summary": "A task brief is a complete specification document — not a chat message. Claude executes it autonomously.",
        "body": md("""
## Task brief vs prompt
A **prompt** is what you type in a conversation: "Add a function to..."
A **task brief** is a **document** that fully specifies what you want built:

```markdown
# Task: DC Blocker Module

## Deliverables
- src/dc_block.h — header with DcBlockState struct and function prototypes
- src/dc_block.c — implementation
- tests/test_dc_block.c — host test with main()

## Specifications
- First-order DC blocker: y[n] = x[n] - x[n-1] + alpha * y[n-1]
- Alpha = 0.995 (default, configurable at init)
- Block processing: void dc_block_process(const float *in, float *out,
  uint32_t n, DcBlockState *st)
- State struct holds: previous input sample, previous output sample

## Constraints
- C99 only
- No dynamic allocation
- All input pointers: const
- Functions prefixed: dsp_dc_block_

## Acceptance Criteria
- Build clean with: gcc -std=c99 -Wall -Wextra -Werror
- Test: impulse response settles to zero within 1000 samples
- Test: DC input (constant value) produces near-zero output after settling
- Test: 1 kHz sine at 48 kHz sample rate passes with < 0.01 dB attenuation

## Build Command
gcc -std=c99 -Wall -Wextra -Werror -o build/test_dc \\
    src/dc_block.c tests/test_dc_block.c -lm && ./build/test_dc
```

## Why this works
- Claude has **everything** it needs in one document
- No back-and-forth conversation needed
- The acceptance criteria are **testable** — not subjective
- You can re-use this brief for different implementations (float vs Q15)
- Any developer (human or AI) could implement from this spec

## Save task briefs in your repo
```
tasks/
  dc-blocker.md
  fir-filter.md
  biquad-cascade.md
  energy-meter.md
```
These become your project's **backlog** — not Jira tickets, but implementation-ready specs.
"""),
        "exercises": [
            ex(
                "02-1",
                "Create `tasks/dc-blocker.md` with a complete task brief following the template above. Include: deliverables, specifications, constraints, acceptance criteria, and build command. Do NOT involve Claude in writing this.",
                "You are the architect. The spec is YOUR job.",
                "A complete task brief a junior developer could implement from. Every section filled in. Acceptance criteria are testable commands, not prose.",
            ),
            ex(
                "02-2",
                "Delegate the task to Claude headless: `claude -p 'Read tasks/dc-blocker.md and implement everything specified. Follow all constraints. Build and run tests. Report results.' --allowedTools Read,Edit,Bash`",
                "One command. Walk away.",
                "Claude reads the brief, creates all files, builds, tests, reports. You review after — not during.",
            ),
            ex(
                "02-3",
                "Write a SECOND task brief `tasks/fir-filter.md` for a 3-tap FIR filter module. Make the acceptance criteria even more specific: exact expected output values for a unit impulse with coefficients {0.25, 0.5, 0.25}.",
                "More specific = better autonomous results.",
                "Brief includes exact numerical expectations: output[0]=0.25, output[1]=0.5, output[2]=0.25, output[3]=0.0. No ambiguity.",
            ),
            ex(
                "02-4",
                "Delegate both tasks in sequence: run the DC blocker brief, then the FIR brief. Review both results with `git diff`. Score them: did they meet the spec?",
                "Two delegations, one review session. You're the reviewer now.",
                "Both modules implemented. You review the combined diff like a PR. Grade: specs met or not. If not, refine the brief.",
            ),
        ],
    },
    {
        "id": "03",
        "title": "CLAUDE.md: The Employee Handbook",
        "level": "Beginner",
        "summary": "CLAUDE.md is not 'memory' — it's the company policy document your worker reads on day one of every shift.",
        "body": md("""
## Reframing CLAUDE.md
In the interactive course, CLAUDE.md is "project memory." In the delegation course, it's the **employee handbook** — the permanent rules your worker must follow on every task, without you repeating yourself.

## What goes in the handbook
```markdown
# DSP Audio Library — Worker Instructions

## Your Role
You are implementing DSP algorithms for an ARM Cortex-M4F target.
Follow these instructions on EVERY task. Do not deviate.

## Code Standards (non-negotiable)
- Language: C99 only. No C++ features.
- Types: stdint.h only. Never use bare `int` for sizes.
- Naming: all functions prefixed `dsp_`. Structs suffixed `_t`.
- Pointers: `const` on every read-only pointer. No exceptions.
- Allocation: ZERO dynamic allocation. Fixed buffers only.
- ISR safety: no printf, no malloc, no blocking calls in ISR paths.

## Build (always verify your work)
- Build: `make` or `gcc -std=c99 -Wall -Wextra -Werror`
- Test: `make test` or run test binaries individually
- EVERY change must build clean with -Werror before you consider it done.

## Test Policy (non-negotiable)
- Every new function needs a test in tests/
- Golden vectors in tests/golden/ as float32 binary files
- Tolerance: 1e-6 for float; 1 LSB for Q15
- A task is NOT done until all tests pass.

## Git (how you deliver work)
- Work on a feature branch: feat/task-name
- Conventional commits: type(scope): description
- One commit per logical unit of work
- NEVER commit to main directly
- NEVER force-push

## Forbidden (instant rejection)
- Do not modify third_party/ under any circumstances
- Do not add dependencies without explicit approval
- Do not commit .bin, .elf, or flash artifacts
- Do not use floating point in files under src/fixed/
```

## The key difference
Interactive CLAUDE.md: "Here's what I want Claude to remember."
Delegation CLAUDE.md: "Here are the rules. Follow them. Every time. Without being told."

## Subdirectory handbooks
- `src/dsp/CLAUDE.md` — DSP-specific rules (Q format, no float in fixed module)
- `tests/CLAUDE.md` — test conventions (assert macros, golden comparison)
- `scripts/CLAUDE.md` — scripting rules (Python 3.9+, type hints required)
"""),
        "exercises": [
            ex(
                "03-1",
                "Rewrite your CLAUDE.md from scratch using the 'employee handbook' framing. Start with 'Your Role' and include sections for: Code Standards, Build, Test Policy, Git, and Forbidden. Make every rule imperative ('You MUST', 'NEVER', 'ALWAYS').",
                "Write it like you're onboarding a junior who needs explicit instructions.",
                "Handbook-style CLAUDE.md with imperative rules. Not 'we use dsp_ prefix' but 'You MUST prefix all functions with dsp_. No exceptions.'",
            ),
            ex(
                "03-2",
                "Create `tests/CLAUDE.md` as a department-specific handbook: 'When working in this directory: use assert macros from test_utils.h, compare against golden files, name all test functions test_*, report pass/fail to stdout.'",
                "Subdirectory handbook — local rules for local work.",
                "tests/CLAUDE.md with rules specific to test code. When Claude works on test files, it follows BOTH the root handbook AND this local one.",
            ),
            ex(
                "03-3",
                "Test the handbook: delegate a task via headless mode and check if Claude followed EVERY rule in CLAUDE.md. Create a checklist from your handbook and manually verify each item.",
                "Audit your worker's compliance.",
                "Checklist: dsp_ prefix? ✓ const pointers? ✓ No malloc? ✓ Tests pass? ✓ Build clean with -Werror? ✓ Conventional commit? ✓ — If any fail, your handbook needs clearer wording.",
            ),
            ex(
                "03-4",
                "Intentionally delegate a task that SHOULD violate a rule (e.g., 'Add a variable-length buffer in src/dsp/gain.c'). See if Claude refuses based on the handbook or if it complies. If it complies, strengthen the handbook wording and re-test.",
                "Stress-test the handbook. Find gaps.",
                "If Claude complies with a forbidden pattern, the handbook wording is weak. Strengthen: 'You MUST NOT use malloc, calloc, realloc, or any heap allocation in src/. This is a hard constraint. Violation means the task is failed.'",
            ),
        ],
    },
    {
        "id": "04",
        "title": "Acceptance Criteria: Define Done Before Delegating",
        "level": "Beginner",
        "summary": "If you can't test it automatically, you can't delegate it. Write acceptance criteria that a machine can verify.",
        "body": md("""
## The #1 rule of delegation
**If your acceptance criteria require a human to evaluate, you're not delegating — you're babysitting.**

## Bad vs good acceptance criteria
### ❌ Bad (subjective, requires human judgment)
- "Code should be clean"
- "Good performance"
- "Properly tested"
- "Follow best practices"

### ✅ Good (testable by machine)
- "Build passes with `gcc -std=c99 -Wall -Wextra -Werror -pedantic`"
- "All tests in `tests/` pass with exit code 0"
- "Output matches golden vector within max absolute error 1e-6"
- "No function exceeds 50 lines (check with `wc -l`)"
- "Zero `malloc` calls in `src/dsp/` (verify with `grep -r malloc src/dsp/`)"
- "`git diff --stat` shows only files listed in task brief"

## The verification script pattern
For every task brief, write a verification script:
```bash
#!/bin/bash
# scripts/verify_dc_blocker.sh
set -e

echo "=== Build ==="
make clean && make

echo "=== Tests ==="
./build/test_dc_block

echo "=== Constraint checks ==="
# No malloc in src/dsp/
if grep -r "malloc\|calloc\|realloc" src/dsp/; then
    echo "FAIL: dynamic allocation found in src/dsp/"
    exit 1
fi

# All functions prefixed dsp_
if grep -rn "^[a-zA-Z].*(" src/dsp/*.c | grep -v "^.*:.*dsp_" | grep -v "^.*:.*#"; then
    echo "FAIL: functions without dsp_ prefix found"
    exit 1
fi

echo "=== ALL CHECKS PASSED ==="
```

## The delegation command becomes
```bash
claude -p "Read tasks/dc-blocker.md and implement. \
  When done, run scripts/verify_dc_blocker.sh. \
  If any check fails, fix and re-run until all pass." \
  --allowedTools Read,Edit,Bash
```

## You don't review code. You review test results.
"""),
        "exercises": [
            ex(
                "04-1",
                "Take your DC blocker task brief and convert all prose acceptance criteria into testable commands. Each criterion should be a shell command with exit code 0 = pass, non-zero = fail.",
                "Every criterion must be machine-checkable.",
                "Examples: `./build/test_dc_block` (exit 0), `! grep -r malloc src/dsp/` (exit 0 if no match), `gcc -Werror ...` (exit 0 if clean).",
            ),
            ex(
                "04-2",
                "Write `scripts/verify_dc_blocker.sh` that runs ALL acceptance criteria in sequence. If any fails, the script exits non-zero. Make it executable (`chmod +x`).",
                "One script = full verification.",
                "Script runs build, tests, constraint checks. Reports each check. Exits non-zero on first failure. This is your automated reviewer.",
            ),
            ex(
                "04-3",
                "Delegate with verification: `claude -p 'Read tasks/dc-blocker.md. Implement. Run scripts/verify_dc_blocker.sh. Fix any failures. Repeat until all checks pass.' --allowedTools Read,Edit,Bash`",
                "Claude implements AND verifies. You review the final result.",
                "Claude iterates: implement → verify → fail → fix → verify → pass. You see only the final result.",
            ),
            ex(
                "04-4",
                "After Claude finishes, run `scripts/verify_dc_blocker.sh` YOURSELF to independently confirm. Trust but verify.",
                "Run the same verification Claude ran. Confirm independently.",
                "All checks pass when YOU run them. This confirms Claude's work is correct — not just Claude's self-report.",
            ),
        ],
    },
    {
        "id": "05",
        "title": "Review, Don't Co-Author",
        "level": "Beginner",
        "summary": "Your job is PR review — not pair programming. Read diffs, check specs, approve or send back.",
        "body": md("""
## The review workflow
After Claude finishes a delegated task:

### Step 1: Check the verification script
```bash
scripts/verify_dc_blocker.sh
# All green? Move to step 2.
```

### Step 2: Review the diff
```bash
git diff main...feat/dc-blocker
```
Or if Claude committed:
```bash
git log --oneline main..feat/dc-blocker
git diff main...feat/dc-blocker
```

### Step 3: Check against the task brief
Open `tasks/dc-blocker.md` side-by-side with the diff. For each deliverable:
- ✓ File exists?
- ✓ API matches spec?
- ✓ Constraints followed?
- ✓ Tests cover acceptance criteria?

### Step 4: Approve or send back
**Approve**: merge the branch, move to next task.
**Send back**: write specific feedback in a file, re-delegate:
```bash
echo "- dc_block_init is missing alpha parameter" >> tasks/dc-blocker-feedback.md
echo "- test_dc_block.c doesn't test DC input case" >> tasks/dc-blocker-feedback.md

claude -p "Read tasks/dc-blocker.md and tasks/dc-blocker-feedback.md. \
  Fix all feedback items. Run scripts/verify_dc_blocker.sh." \
  --allowedTools Read,Edit,Bash
```

## What you DON'T do
- You don't open files and edit them yourself
- You don't sit in an interactive session fixing things
- You don't type "change line 42 to..."
- If something's wrong, you write it as feedback and re-delegate

## You are the reviewer. Claude is the author. Stay in your lane.
"""),
        "exercises": [
            ex(
                "05-1",
                "After a delegated task completes, review the result using ONLY `git diff` and the verification script. Do not open any source file in an editor. Make your judgment from the diff and test results alone.",
                "Diff + test results = your review interface.",
                "You reviewed like a senior engineer on GitHub: read diff, check test output, approve or request changes. No editor needed.",
            ),
            ex(
                "05-2",
                "Find something wrong in Claude's output (there's almost always something). Write the feedback in `tasks/feedback.md` as bullet points. Do NOT fix it yourself. Re-delegate to Claude with the feedback file.",
                "Feedback → re-delegate. Never fix it yourself.",
                "Feedback file created. Claude re-ran with feedback. Fixed the issue. You reviewed again. This is the delegation loop.",
            ),
            ex(
                "05-3",
                "Deliberately write a BAD task brief (vague, missing acceptance criteria). Delegate it. When the result is poor, recognize that the problem is YOUR brief — not Claude. Rewrite the brief and re-delegate.",
                "Bad specs produce bad output. That's your fault, not Claude's.",
                "First result: poor quality (ambiguous code, missing tests). Second result after better brief: meets spec. The lesson: invest time in specs, not in editing AI output.",
            ),
            ex(
                "05-4",
                "Create a `reviews/` folder. After each review, write a brief review log: `reviews/dc-blocker-review.md` with date, pass/fail per criterion, and feedback given. This is your project management trail.",
                "Documentation of the review process.",
                "Review log tracks: what was delegated, what passed, what failed, what feedback was given. This becomes your management record.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # INTERMEDIATE — Autonomous Workflows
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "06",
        "title": "Headless Mode: Claude Works While You Don't",
        "level": "Intermediate",
        "summary": "Headless is the default interface for delegation — not the advanced feature. Interactive mode is for debugging.",
        "body": md("""
## Reframing headless mode
In the interactive course, headless is an "advanced topic."
In the delegation course, **headless is the primary interface**.

Interactive mode is only for:
- Debugging a failed delegation
- Exploring a new codebase before writing your first spec
- Asking Claude to explain something you don't understand

For actual work: **always headless**.

## The standard delegation command
```bash
claude -p "Read tasks/TASK_NAME.md. Implement everything specified. \
  Run the verification script. Fix any failures. \
  Commit to branch feat/TASK_NAME with conventional commits." \
  --allowedTools Read,Edit,Bash
```

## --allowedTools is your permission policy
You are not pressing y/n per command. You set the policy upfront:
- `Read` — Claude can read files (always include this)
- `Edit` — Claude can create/modify files
- `Bash` — Claude can run shell commands (build, test, git)
- `Read,Edit` — no shell commands (safest for code-only tasks)
- `Read,Edit,Bash` — full autonomy (for build-test-fix tasks)

## Output capture
```bash
# Capture output for review
claude -p "..." --allowedTools Read,Edit,Bash > logs/task_output.log 2>&1

# Check exit code
echo $?  # 0 = success
```

## The manager's workflow
1. Write task brief (5 minutes)
2. Write/update verification script (5 minutes)
3. Run delegation command (30 seconds)
4. Do other work while Claude implements (15-60 minutes)
5. Review result (10 minutes)

Total YOUR time: ~20 minutes for a feature that takes an hour to implement.
"""),
        "exercises": [
            ex(
                "06-1",
                "Delegate a new task entirely headless: write `tasks/gain-function.md` specifying a float32 gain function, write `scripts/verify_gain.sh`, then run the headless command. Capture output to `logs/gain.log`. Do not open an interactive session at all.",
                "Pure delegation workflow. No interactive session.",
                "Task brief → verification script → headless command → log captured. You wrote the spec and reviewed the result. Everything in between was Claude's job.",
            ),
            ex(
                "06-2",
                "Run the same task with `--allowedTools Read,Edit` (no Bash). Claude can write code but can't build or test. Review what it produced. Then run verification yourself. Compare quality to full-autonomy mode.",
                "Restricted autonomy experiment.",
                "Without Bash, Claude can't build-test-fix. The code may have errors it couldn't catch. Full autonomy (Read,Edit,Bash) produces better results because Claude can self-verify.",
            ),
            ex(
                "06-3",
                "Time yourself: how long does it take to write a task brief and verification script vs how long would it take to implement the feature yourself? Log both times in `docs/time-log.md`.",
                "ROI measurement.",
                "Spec writing: 10-15 min. Manual implementation: 30-60 min. Even if Claude needs a re-delegation, total time is less. The ROI improves with practice.",
            ),
            ex(
                "06-4",
                "Delegate three small tasks in sequence using a shell loop:\n`for task in gain peak-detect rms; do claude -p \"Read tasks/${task}.md. Implement. Verify.\" --allowedTools Read,Edit,Bash; done`\nYou wrote the specs. Claude implements all three. You review all three.",
                "Batch delegation. Three tasks, one review session.",
                "Three modules implemented from three specs. You review all three diffs at once. This is management-level throughput.",
            ),
        ],
    },
    {
        "id": "07",
        "title": "Shell Scripts: Packaging Tasks for Delegation",
        "level": "Intermediate",
        "summary": "Wrap delegation in reusable scripts — standardized task execution, logging, and verification.",
        "body": md("""
## The delegation script pattern
Instead of typing headless commands each time, create reusable scripts:

```bash
#!/bin/bash
# scripts/delegate.sh — standard task delegation wrapper
set -euo pipefail

TASK=$1
BRANCH="feat/${TASK}"
LOG="logs/${TASK}-$(date +%Y%m%d-%H%M%S).log"

echo "=== Delegating: ${TASK} ==="
echo "Branch: ${BRANCH}"
echo "Log: ${LOG}"

mkdir -p logs

# Create feature branch
git checkout -b "${BRANCH}" main 2>/dev/null || git checkout "${BRANCH}"

# Delegate
claude -p "Read tasks/${TASK}.md. Implement everything specified. \
  Follow CLAUDE.md rules strictly. \
  Build and test. Fix any failures. \
  Commit with conventional messages." \
  --allowedTools Read,Edit,Bash > "${LOG}" 2>&1

EXIT=$?
echo "=== Claude exit code: ${EXIT} ==="

# Run verification
if [ -f "scripts/verify_${TASK}.sh" ]; then
    echo "=== Running verification ==="
    bash "scripts/verify_${TASK}.sh"
else
    echo "WARNING: No verification script for ${TASK}"
fi

echo "=== Review: git diff main...${BRANCH} ==="
```

## Usage
```bash
./scripts/delegate.sh dc-blocker
./scripts/delegate.sh fir-filter
./scripts/delegate.sh biquad-cascade
```

## The manager's toolkit
```
scripts/
  delegate.sh          — standard delegation wrapper
  delegate-review.sh   — run delegation + open diff for review
  verify_dc_blocker.sh — DC blocker specific checks
  verify_fir.sh        — FIR filter specific checks
  verify_all.sh        — run ALL verification scripts
```
"""),
        "exercises": [
            ex(
                "07-1",
                "Create `scripts/delegate.sh` following the template above. Make it take a task name argument, create a feature branch, run Claude headless, capture logs, and run the verification script.",
                "Your standard delegation infrastructure.",
                "Script created and tested. Takes task name, creates branch, delegates, logs, verifies. Reusable for any task.",
            ),
            ex(
                "07-2",
                "Create `scripts/verify_all.sh` that finds and runs every `scripts/verify_*.sh` file. This is your 'run all acceptance tests' command.",
                "Aggregate verification.",
                "Script globs verify_*.sh, runs each, reports pass/fail for each, exits non-zero if any fail.",
            ),
            ex(
                "07-3",
                "Delegate a task using your new script: `./scripts/delegate.sh peak-detect`. Review the log file it created. Review the branch diff.",
                "First delegation through the standard pipeline.",
                "Task delegated via script. Log captured in logs/. Branch created. Diff reviewable. The process is standardized.",
            ),
            ex(
                "07-4",
                "Create `scripts/delegate-batch.sh` that takes multiple task names and delegates them sequentially: `./scripts/delegate-batch.sh gain fir dc-blocker`. Each gets its own branch and log.",
                "Batch delegation automation.",
                "Three tasks delegated in sequence. Three branches. Three logs. One review session for all three.",
            ),
        ],
    },
    {
        "id": "08",
        "title": "Git Branch Workflows: Claude Gets a Branch, You Get a PR",
        "level": "Intermediate",
        "summary": "Claude works on feature branches. You review the branch like a PR. Merge when satisfied.",
        "body": md("""
## The branch-per-task model
Every delegated task gets its own branch:
```
main (protected — Claude never touches this)
├── feat/dc-blocker (Claude's work)
├── feat/fir-filter (Claude's work)
├── feat/biquad-cascade (Claude's work)
└── feat/energy-meter (Claude's work)
```

## Your CLAUDE.md git rules
```markdown
## Git (mandatory)
- Work on the branch you are given. NEVER switch branches.
- NEVER commit to main.
- NEVER force-push.
- Conventional commits: type(scope): description
- Commit after each logical unit of work (not one giant commit).
- Commit messages must describe WHAT changed, not that an AI did it.
```

## The review workflow
```bash
# See what Claude did
git log --oneline main..feat/dc-blocker
git diff main...feat/dc-blocker

# If approved
git checkout main
git merge feat/dc-blocker
git branch -d feat/dc-blocker

# If needs work — write feedback, re-delegate
echo "Fix: missing bounds check on n parameter" > tasks/dc-blocker-feedback.md
git checkout feat/dc-blocker
claude -p "Read tasks/dc-blocker-feedback.md. Fix all items. Build. Test. Commit." \
  --allowedTools Read,Edit,Bash
```

## If you use GitHub
```bash
# Claude pushes the branch
# You review the PR in GitHub's UI
git push origin feat/dc-blocker
gh pr create --base main --head feat/dc-blocker \
  --title "feat(dsp): DC blocker module" \
  --body "Implements tasks/dc-blocker.md"
```
Now your team can review Claude's work in the normal PR workflow.
"""),
        "exercises": [
            ex(
                "08-1",
                "Add git rules to your CLAUDE.md handbook (never commit to main, conventional commits, work on given branch only). Then delegate a task that includes git operations. Verify Claude followed the git rules.",
                "Git discipline is part of the handbook.",
                "Claude committed to the feature branch (not main). Used conventional commits. No force-push. Rules followed.",
            ),
            ex(
                "08-2",
                "After a delegated task: review the branch using `git log --oneline` and `git diff main...`. Make your merge/reject decision from these alone. If approved, merge to main.",
                "Branch review = your PR review.",
                "You reviewed commits and diff. Approved. Merged to main. Clean history. This is how you'd review a human junior's PR.",
            ),
            ex(
                "08-3",
                "Reject a branch: write feedback, re-delegate on the same branch. Verify Claude applies the feedback and adds new commits (not force-push).",
                "Feedback loop via re-delegation.",
                "New commits added to the branch addressing feedback. History is clean (no rewrite). Re-review passes.",
            ),
            ex(
                "08-4",
                "If you have a GitHub remote: push the branch and open a PR with `gh pr create`. Review it in GitHub's UI. This is indistinguishable from a human contributor's PR.",
                "Claude's work in the normal team review workflow.",
                "PR on GitHub with clean commits, proper title/body. Reviewable by any team member. No one can tell it was implemented by an AI (nor does it matter).",
            ),
        ],
    },
    {
        "id": "09",
        "title": "Test Suites as Quality Gates",
        "level": "Intermediate",
        "summary": "Tests are not 'nice to have' — they're the ONLY way to verify delegated work at scale.",
        "body": md("""
## Without tests, delegation doesn't work
If you delegate a task and the only way to verify it is to read the code line-by-line, you haven't delegated anything — you've just outsourced typing.

## The quality gate hierarchy
```
Level 1: Build passes with -Werror (catches syntax, types, warnings)
Level 2: Unit tests pass (catches logic errors)
Level 3: Golden vector comparison (catches numerical errors)
Level 4: Constraint checks (catches policy violations)
Level 5: Integration tests (catches interface errors)
```
Each level is automated. Each level catches a category of bug.

## Your verification script IS your quality gate
```bash
#!/bin/bash
set -e

# Level 1: Build
make clean && make CFLAGS="-Wall -Wextra -Werror"

# Level 2: Unit tests
for test in build/test_*; do
    echo "Running $test..."
    ./$test
done

# Level 3: Golden comparison
python3 tests/compare_goldens.py

# Level 4: Constraint checks
./scripts/check_constraints.sh

echo "ALL QUALITY GATES PASSED"
```

## Invest in tests BEFORE delegating
The time you spend writing acceptance tests is the time you DON'T spend reviewing code. A good test suite lets you delegate with confidence.

## The golden rule
**If you can't write an automated test for it, you can't delegate it to Claude.**
"""),
        "exercises": [
            ex(
                "09-1",
                "Create `scripts/quality_gate.sh` that runs all five levels of quality checks for your project. Run it manually to verify it works on your current codebase.",
                "Build your quality gate before delegating.",
                "Script runs: build (-Werror), unit tests, golden comparison (if applicable), constraint checks (no malloc, naming prefix). All pass on current code.",
            ),
            ex(
                "09-2",
                "Write a Python golden vector generator `tests/gen_golden_dc.py` that creates a reference output for the DC blocker using numpy/scipy. Save as binary. Then write the C comparison test.",
                "Golden vectors are the ultimate delegated-work verifier.",
                "Python generates reference. C test loads and compares. Max error < 1e-6. This catches numerical bugs Claude might introduce without you reading the code.",
            ),
            ex(
                "09-3",
                "Create `scripts/check_constraints.sh` that verifies: no malloc in src/dsp/, all functions prefixed dsp_, no files modified outside allowed paths. Use grep and find.",
                "Automated policy enforcement.",
                "Script checks constraints that CLAUDE.md specifies. This is the machine-enforced version of your handbook. Claude can't cheat past this.",
            ),
            ex(
                "09-4",
                "Delegate a task where you ONLY look at the quality gate results — don't read ANY of Claude's code. Trust the gates. If all pass, merge. This is pure delegation.",
                "Trust your tests. Don't read the code.",
                "Quality gates all pass. You merged without reading a single line of implementation. This is the goal: trust tests, not manual review.",
            ),
        ],
    },
    {
        "id": "10",
        "title": "Batch Operations: One Spec, Many Files",
        "level": "Intermediate",
        "summary": "Delegate repetitive tasks across your entire codebase — Claude iterates, you review once.",
        "body": md("""
## When to use batch delegation
- "Add Doxygen comments to EVERY function in src/"
- "Add `const` correctness to ALL pointer parameters in src/"
- "Create a test file for EVERY module that doesn't have one"
- "Replace magic number 256 with DSP_BLOCK_SIZE in all files"
- "Add bounds checking to every function that takes a length parameter"

These are tasks you'd never do manually because they're tedious. But Claude doesn't get bored.

## Batch task brief pattern
```markdown
# Batch Task: Add Doxygen Comments

## Scope
Every .c and .h file in src/

## For each function, add:
- @brief — one-line description
- @param — for each parameter, with [in]/[out]/[in,out]
- @return — return value description
- @note — if any ISR/threading constraints apply

## Constraints
- Do NOT change any code logic
- Do NOT reformat code
- Only add comment blocks

## Verify
gcc -std=c99 -Wall -Wextra -Werror (build must still pass)
```

## Delegation
```bash
claude -p "Read tasks/batch-doxygen.md. Apply to every file in src/. \
  Build after ALL changes to verify nothing broke." \
  --allowedTools Read,Edit,Bash
```

## Review
```bash
git diff --stat  # see which files changed
git diff         # see all changes (should be comment-only)
```
"""),
        "exercises": [
            ex(
                "10-1",
                "Write `tasks/batch-const-correctness.md`: add `const` to all read-only pointer parameters across all files in `src/`. Constraint: do NOT change any logic. Verify: build with -Werror. Delegate headless.",
                "Cross-codebase mechanical fix via delegation.",
                "Claude adds const to every applicable pointer across all source files. Build still passes. Diff shows only const additions — no logic changes.",
            ),
            ex(
                "10-2",
                "Write `tasks/batch-missing-tests.md`: for every .c file in src/ that doesn't have a corresponding test in tests/, create one with at least a basic smoke test. Delegate headless.",
                "Gap-filling across the codebase.",
                "New test files created for modules lacking tests. Each test is basic but functional. Build and run all tests pass.",
            ),
            ex(
                "10-3",
                "Write `tasks/batch-magic-numbers.md`: find and replace all magic numbers in src/ with named constants in `src/dsp_config.h`. Delegate and review the diff.",
                "Refactoring at scale.",
                "New config header with named constants. All magic numbers replaced. Build passes. Diff is large but mechanical.",
            ),
            ex(
                "10-4",
                "Delegate a batch task that spans BOTH code and documentation: 'For every public function in src/, ensure it has a Doxygen comment AND an entry in docs/api.md.' This is a two-file-per-function task that would take hours manually.",
                "Coordinated batch: code + docs.",
                "Every function gets Doxygen AND API doc entry. Cross-referenced. Build passes. API doc is comprehensive. Hours of work done in minutes.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # ADVANCED — Systems & Pipelines
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "11",
        "title": "CI/CD: Claude as a Pipeline Worker",
        "level": "Advanced",
        "summary": "Claude runs in your CI pipeline — fixing warnings, regenerating files, reviewing PRs — automatically triggered.",
        "body": md("""
## Claude in CI: event-driven delegation
Instead of YOU running headless commands, your CI pipeline does it:

### On push: auto-fix warnings
```yaml
name: Claude Auto-Fix
on: push
jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '18' }
      - run: npm install -g @anthropic-ai/claude-code
      - name: Fix warnings
        run: |
          claude -p "Fix all compiler warnings in src/. \
            Build with make. Do not change test files." \
            --allowedTools Read,Edit,Bash
      - name: Commit fixes
        run: |
          git diff --exit-code || {
            git config user.name "claude-worker"
            git config user.email "claude@ci"
            git add -A
            git commit -m "fix: auto-resolve compiler warnings"
            git push
          }
```

### On PR: automated review
```yaml
name: Claude PR Review
on: pull_request
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: npm install -g @anthropic-ai/claude-code
      - name: Review
        run: |
          git diff origin/main...HEAD | \
          claude -p "Review this diff for: buffer overflows, \
            off-by-one errors, missing bounds checks, \
            const correctness violations. \
            Output findings as a markdown list." \
            --allowedTools Read > review.md
      - name: Post review
        run: gh pr comment ${{ github.event.number }} -F review.md
```

## Safety rules for CI delegation
- **NEVER give Bash access to PR review jobs** (untrusted code!)
- Auto-fix jobs: restrict to specific directories
- Always require human merge approval
- Treat Claude's CI commits like any bot commit: reviewable
"""),
        "exercises": [
            ex(
                "11-1",
                "Write `.github/workflows/claude-fix.yml` that on push to main runs Claude headless to fix warnings and auto-commit. Include safety: only touch src/, never force-push.",
                "Auto-fix CI pipeline.",
                "YAML workflow with checkout, Claude install, headless fix with scoped prompt, conditional commit+push. Only src/ files touched.",
            ),
            ex(
                "11-2",
                "Write `.github/workflows/claude-review.yml` that on pull_request pipes the diff to Claude with Read-only tools and posts findings as a PR comment.",
                "Automated PR review via CI.",
                "Read-only review (no Edit, no Bash). Findings posted as PR comment via gh. Safe for untrusted PRs.",
            ),
            ex(
                "11-3",
                "Write `.github/workflows/claude-golden-regen.yml` that on schedule (weekly cron) regenerates golden vectors, runs tests, and opens a PR if there are changes.",
                "Scheduled maintenance delegation.",
                "Cron trigger, Claude regenerates goldens with Edit+Bash, tests pass, PR opened if diff. Fully automated maintenance.",
            ),
            ex(
                "11-4",
                "Create a `docs/ci-delegation-policy.md` documenting: which CI jobs use Claude, what tools each has, what branches they can touch, who reviews their output.",
                "Governance document for CI delegation.",
                "Policy doc with job inventory, tool permissions, branch protections, review requirements. This is your delegation governance.",
            ),
        ],
    },
    {
        "id": "12",
        "title": "Scheduled Tasks: Nightly, Weekly, On-Event",
        "level": "Advanced",
        "summary": "Set up recurring Claude tasks — maintenance that runs itself, problems that fix themselves.",
        "body": md("""
## Recurring delegation patterns

### Nightly: build health check
```bash
# cron: 0 2 * * * /path/to/scripts/nightly_build.sh
#!/bin/bash
cd /path/to/project
git checkout main && git pull

claude -p "Build the project with make. Run all tests. \
  Report: build status, test results, warnings count. \
  If any test fails, create a file issues/nightly-$(date +%Y%m%d).md \
  with diagnosis and suggested fix." \
  --allowedTools Read,Edit,Bash > logs/nightly-$(date +%Y%m%d).log 2>&1

# Email or Slack notification
if [ $? -ne 0 ]; then
    echo "Nightly build FAILED" | mail -s "Build Alert" team@company.com
fi
```

### Weekly: code health sweep
```bash
# cron: 0 3 * * 1 /path/to/scripts/weekly_sweep.sh
claude -p "Analyze the entire src/ directory for: \
  unused includes, missing const qualifiers, functions over 50 lines, \
  TODO comments older than the last tag. \
  Write report to reports/weekly-$(date +%Y%m%d).md." \
  --allowedTools Read,Edit > logs/weekly-$(date +%Y%m%d).log 2>&1
```

### On-event: test failure triage
```bash
# Called by CI when tests fail
claude -p "The test $FAILED_TEST failed with output: $TEST_OUTPUT. \
  Read the relevant source files. Diagnose the root cause. \
  Write diagnosis to issues/triage-$(date +%s).md." \
  --allowedTools Read,Edit
```

## Your role: design the schedule, review the reports
You don't run these. Cron runs them. Claude does the work. You read the reports in the morning.
"""),
        "exercises": [
            ex(
                "12-1",
                "Write `scripts/nightly_health.sh` that runs Claude headless to build, test, and generate a health report in `reports/`. Add a date-stamped filename. Run it manually once to verify.",
                "Nightly health check script.",
                "Script builds, tests, generates report. Date-stamped log and report. Ready to add to cron.",
            ),
            ex(
                "12-2",
                "Write `scripts/weekly_sweep.sh` that runs Claude Read-only to analyze code quality and write a report. No code changes — analysis only.",
                "Weekly analysis report — read-only delegation.",
                "Report identifies: unused includes, long functions, stale TODOs, missing tests. No code changed. Information only.",
            ),
            ex(
                "12-3",
                "Create a `docs/schedule.md` documenting all recurring tasks: what runs, when, what it does, where reports go, who reviews them.",
                "Operations manual for recurring delegation.",
                "Schedule doc with: nightly build check (2am), weekly sweep (Monday 3am), report locations, review responsibility.",
            ),
            ex(
                "12-4",
                "Set up the nightly script as an actual cron job (or Windows Task Scheduler). Let it run overnight. Check the report in the morning.",
                "Real automation — Claude works while you sleep.",
                "Report exists in the morning. Build health known. Issues documented. You did nothing after setup.",
            ),
        ],
    },
    {
        "id": "13",
        "title": "Multi-Task Orchestration",
        "level": "Advanced",
        "summary": "Multiple delegated tasks with dependencies — Claude implements in the right order, you review the pipeline.",
        "body": md("""
## Task dependency chains
Real projects have ordered tasks:
```
Task A: Create config header (dsp_config.h)
  └─ Task B: Implement DC blocker (depends on config)
       └─ Task C: Implement biquad (depends on config + references DC block pattern)
            └─ Task D: Integration test (depends on all above)
```

## The orchestration script
```bash
#!/bin/bash
# scripts/orchestrate_dsp_pipeline.sh
set -e

echo "=== Phase 1: Infrastructure ==="
./scripts/delegate.sh config-header

echo "=== Phase 2: Core modules (parallel-safe) ==="
./scripts/delegate.sh dc-blocker
./scripts/delegate.sh fir-filter

echo "=== Phase 3: Advanced modules ==="
./scripts/delegate.sh biquad-cascade

echo "=== Phase 4: Integration ==="
./scripts/delegate.sh integration-tests

echo "=== Phase 5: Verification ==="
./scripts/verify_all.sh

echo "=== ALL PHASES COMPLETE ==="
git log --oneline main..HEAD
```

## Each task gets its own brief
```
tasks/
  01-config-header.md
  02-dc-blocker.md
  03-fir-filter.md
  04-biquad-cascade.md
  05-integration-tests.md
```

## Merge strategy
Option A: Single feature branch — all tasks commit sequentially.
Option B: Branch per task — merge to main in order.

## Your role: architect the pipeline, run it, review the end result.
"""),
        "exercises": [
            ex(
                "13-1",
                "Create a pipeline of 3 dependent tasks: (1) config header, (2) utility functions that use the config, (3) tests that use both. Write task briefs for each with explicit dependency notes.",
                "Design the dependency chain as task briefs.",
                "Three briefs. Each references what the previous one should have created. Dependencies documented.",
            ),
            ex(
                "13-2",
                "Write `scripts/orchestrate.sh` that delegates all three tasks in order, verifying each before proceeding to the next. If any fails, the pipeline stops.",
                "Orchestration script with gate checks.",
                "Script delegates task 1, verifies, then task 2, verifies, then task 3, verifies. Stops on first failure.",
            ),
            ex(
                "13-3",
                "Run the full pipeline. Don't intervene. Review only the final result: does the combined output meet all specs?",
                "End-to-end delegated pipeline.",
                "Three tasks implemented in order. All verifications pass. Combined diff is clean. You reviewed once at the end.",
            ),
            ex(
                "13-4",
                "A task in the middle fails. Write feedback, re-run ONLY that task (not the whole pipeline). Verify the fix doesn't break the subsequent task.",
                "Partial pipeline re-execution.",
                "Middle task re-delegated with feedback. Fixed. Subsequent task still works. Pipeline integrity maintained.",
            ),
        ],
    },
    {
        "id": "14",
        "title": "SDK: Programmatic Task Dispatch",
        "level": "Advanced",
        "summary": "Trigger Claude from Python/TypeScript code — event-driven delegation for real systems.",
        "body": md("""
## From scripts to programs
Shell scripts are fine for simple automation. But real systems need:
- Conditional logic (if this, delegate that)
- Dynamic prompt generation (fill in template with runtime data)
- Result parsing (extract metrics from Claude's output)
- Error handling (retry, escalate, notify)

## Python delegation wrapper
```python
#!/usr/bin/env python3
import subprocess, json, sys
from pathlib import Path
from datetime import datetime

def delegate(task_name: str, extra_instructions: str = "") -> dict:
    brief = Path(f"tasks/{task_name}.md").read_text()
    prompt = f"Read and implement tasks/{task_name}.md. {extra_instructions} " \\
             f"Follow CLAUDE.md strictly. Build and test. Report results."

    result = subprocess.run(
        ["claude", "-p", prompt, "--allowedTools", "Read,Edit,Bash",
         "--output-format", "json"],
        capture_output=True, text=True, timeout=600
    )

    log_path = Path(f"logs/{task_name}-{datetime.now():%Y%m%d-%H%M%S}.log")
    log_path.parent.mkdir(exist_ok=True)
    log_path.write_text(result.stdout + "\\n" + result.stderr)

    return {
        "task": task_name,
        "exit_code": result.returncode,
        "log": str(log_path),
    }

def verify(task_name: str) -> bool:
    script = Path(f"scripts/verify_{task_name}.sh")
    if not script.exists():
        print(f"WARNING: No verification for {task_name}")
        return True
    return subprocess.run(["bash", str(script)]).returncode == 0

if __name__ == "__main__":
    task = sys.argv[1]
    print(f"Delegating: {task}")
    result = delegate(task)
    print(f"Exit code: {result['exit_code']}")

    if verify(task.replace('-', '_')):
        print("VERIFIED: All checks passed")
    else:
        print("FAILED: Verification failed")
        sys.exit(1)
```

## Usage
```bash
python3 scripts/delegate.py dc-blocker
python3 scripts/delegate.py fir-filter --extra "Optimize for ARM NEON"
```

## Event-driven delegation
```python
# On new artifact in S3:
if new_golden_uploaded():
    delegate("regenerate-tests",
             extra="New golden vector uploaded. Update tests.")

# On CI failure:
if ci_failed(build_log):
    delegate("diagnose-failure",
             extra=f"Build log: {build_log}")
```
"""),
        "exercises": [
            ex(
                "14-1",
                "Create `scripts/delegate.py` following the template above. Test it by delegating a simple task. Verify it captures logs and exit codes.",
                "Python delegation wrapper.",
                "Script delegates, captures output, logs to file, returns exit code. Reusable foundation for programmatic delegation.",
            ),
            ex(
                "14-2",
                "Add a `verify()` function that runs the corresponding verification script. The delegate script should: delegate → verify → report pass/fail.",
                "Integrated delegation + verification.",
                "delegate.py: delegates task, runs verification, reports combined result. One command for full task lifecycle.",
            ),
            ex(
                "14-3",
                "Create `scripts/orchestrate.py` that reads a `tasks/pipeline.json` file listing tasks in order with dependencies, and executes them sequentially using delegate.py logic.",
                "Programmatic orchestration from config file.",
                "pipeline.json defines task order. orchestrate.py reads it, delegates each, verifies each, stops on failure. Configuration-driven.",
            ),
            ex(
                "14-4",
                "Add retry logic: if a task fails verification, re-delegate with feedback up to 2 times before giving up. Log each attempt.",
                "Resilient delegation with auto-retry.",
                "On verification failure: write feedback, re-delegate, re-verify. Up to 2 retries. Each attempt logged. Final status reported.",
            ),
        ],
    },
    {
        "id": "15",
        "title": "CLAUDE.md Hierarchy: Department-Level Instructions",
        "level": "Advanced",
        "summary": "Root handbook + subdirectory handbooks = organizational structure for your autonomous worker.",
        "body": md("""
## Organizational structure via CLAUDE.md hierarchy
```
CLAUDE.md                    (company-wide policy)
├── src/CLAUDE.md            (engineering department)
│   ├── src/dsp/CLAUDE.md    (DSP team rules)
│   └── src/platform/CLAUDE.md (platform team rules)
├── tests/CLAUDE.md          (QA department)
└── scripts/CLAUDE.md        (devops department)
```

## Root CLAUDE.md — company policy
```markdown
# Company Policy
- C99 only. No exceptions.
- stdint.h types everywhere.
- Build must pass with -Werror.
- Every commit uses conventional format.
```

## src/dsp/CLAUDE.md — DSP team rules
```markdown
# DSP Team Rules (ADDITIONAL to root)
- All functions prefixed dsp_
- No dynamic allocation
- No floating point in files under fixed/
- Block processing only — no sample-by-sample APIs
- Every function must handle n=0 gracefully (return immediately)
```

## tests/CLAUDE.md — QA department rules
```markdown
# Test Department Rules (ADDITIONAL to root)
- Test files named test_MODULE.c
- Use assert macros from test_utils.h
- Every test prints PASS or FAIL to stdout
- Golden vectors in tests/golden/ as float32 binary
- Tolerance: 1e-6 float, 1 LSB fixed-point
```

## Why hierarchy matters for delegation
When you delegate "add a function to src/dsp/fir.c", Claude reads:
1. Root CLAUDE.md (company policy)
2. src/CLAUDE.md (engineering rules)
3. src/dsp/CLAUDE.md (DSP-specific rules)

All three apply. Claude follows the **union** of all rules. This means you can delegate to ANY part of the codebase and the right rules apply automatically.
"""),
        "exercises": [
            ex(
                "15-1",
                "Create the full CLAUDE.md hierarchy: root + src/ + src/dsp/ + tests/ + scripts/. Each should have rules specific to that directory, building on the root.",
                "Organizational structure via files.",
                "Five CLAUDE.md files. Root has universal rules. Each subdirectory adds specific rules. No contradiction between levels.",
            ),
            ex(
                "15-2",
                "Delegate a task that touches src/dsp/ and verify Claude follows BOTH root and dsp-specific rules. Then delegate a task in tests/ and verify it follows root + test rules.",
                "Hierarchy enforcement test.",
                "DSP task: dsp_ prefix ✓, no malloc ✓, C99 ✓. Test task: test_ naming ✓, assert macros ✓, C99 ✓. Each follows the right combination.",
            ),
            ex(
                "15-3",
                "Add a rule to src/dsp/CLAUDE.md that CONTRADICTS a root rule (e.g., root says 'always comment functions', dsp says 'no comments in hot-path inner loops'). Delegate and see which wins. Then fix the hierarchy to be consistent.",
                "Discover and fix hierarchy conflicts.",
                "Claude may follow either. The lesson: hierarchy should be additive (more specific rules ADD constraints), not contradictory. Fix the wording.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # EXPERT — Scaling Delegation
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "16",
        "title": "Cross-Repo and Large-Scale Operations",
        "level": "Expert",
        "summary": "Delegate across multiple repositories — Claude maintains consistency where humans can't.",
        "body": md("""
## The multi-repo challenge
Your team has:
```
dsp-lib/       — core DSP algorithms
firmware-app/  — application using dsp-lib
test-harness/  — pytest + golden vectors
docs-site/     — API documentation
```
A change in `dsp-lib` needs corresponding updates in the other three.

## Cross-repo delegation script
```bash
#!/bin/bash
# scripts/cross-repo-update.sh
CHANGE_DESC=$1

for repo in dsp-lib firmware-app test-harness docs-site; do
    echo "=== Processing $repo ==="
    cd /repos/$repo
    claude -p "A change was made: $CHANGE_DESC. \
      Read CLAUDE.md for this repo's rules. \
      Update any affected files. Build and test. \
      Commit with message: 'chore: sync with $CHANGE_DESC'." \
      --allowedTools Read,Edit,Bash
    cd -
done
```

## Usage
```bash
./scripts/cross-repo-update.sh "dsp_biquad_state_t renamed to DspBiquadState"
```
Claude updates all four repos for consistency.

## At scale: batch repos
```bash
# Update copyright headers across 20 repos
for repo in /repos/*/; do
    cd "$repo"
    claude -p "Update copyright year from 2025 to 2026 in all files. \
      Do not change anything else." \
      --allowedTools Read,Edit
    cd -
done
```

## Your role: design the change, delegate the propagation.
"""),
        "exercises": [
            ex(
                "16-1",
                "Create two related repos (or two directories simulating repos): `lib/` and `app/`. The app depends on lib. Write a task brief for updating a type name in lib, and a corresponding update in app.",
                "Cross-boundary delegation planning.",
                "Two task briefs. lib brief: rename type. app brief: update imports and usage. Dependency between them documented.",
            ),
            ex(
                "16-2",
                "Write `scripts/cross-update.sh` that delegates to both repos in order. Verify each before proceeding.",
                "Cross-repo orchestration.",
                "Script delegates to lib first, verifies, then app, verifies. Both consistent after.",
            ),
            ex(
                "16-3",
                "Write a batch delegation script that applies the same change (e.g., update a license header) across multiple directories. Run it and verify consistency.",
                "Scale-out delegation.",
                "Same change applied uniformly across N directories. All consistent. Manual effort: zero per directory.",
            ),
        ],
    },
    {
        "id": "17",
        "title": "Review Workflows: PR-Based Collaboration",
        "level": "Expert",
        "summary": "Claude opens PRs. You review them. Your team reviews them. Claude addresses feedback. Normal engineering.",
        "body": md("""
## The PR workflow for delegated work
```
1. You write task brief
2. Script delegates to Claude on feature branch
3. Claude implements, commits, pushes
4. Script opens PR via `gh pr create`
5. You (or teammate) review the PR
6. Feedback → re-delegate → force-push or new commits
7. Approve → merge
```

## The delegation-to-PR script
```bash
#!/bin/bash
TASK=$1
BRANCH="feat/${TASK}"

git checkout -b "${BRANCH}" main

claude -p "Read tasks/${TASK}.md. Implement. Build. Test. Commit." \
  --allowedTools Read,Edit,Bash

git push -u origin "${BRANCH}"

gh pr create \
  --base main \
  --head "${BRANCH}" \
  --title "feat(dsp): $(head -1 tasks/${TASK}.md | sed 's/# Task: //')" \
  --body "$(cat tasks/${TASK}.md)"
```

## Addressing review feedback
```bash
# Download review comments
gh pr view $PR_NUMBER --comments > tasks/${TASK}-feedback.md

# Re-delegate with feedback
git checkout "${BRANCH}"
claude -p "Read tasks/${TASK}-feedback.md. Address all review comments. \
  Build. Test. Commit with 'fix: address review feedback'." \
  --allowedTools Read,Edit,Bash

git push
```

## To your team, this is just another PR
Claude's PR is indistinguishable from a human's. It has commits, a description, and passes CI. Review it normally.
"""),
        "exercises": [
            ex(
                "17-1",
                "Write `scripts/delegate-to-pr.sh` that: creates branch, delegates, pushes, opens draft PR. Test it end-to-end (requires GitHub remote).",
                "Full delegation-to-PR pipeline.",
                "Script creates branch, delegates, pushes, opens PR. One command from task brief to reviewable PR.",
            ),
            ex(
                "17-2",
                "Write `scripts/address-feedback.sh` that takes a PR number, downloads comments, re-delegates with feedback, and pushes the fix.",
                "Automated feedback loop.",
                "Script fetches PR comments, creates feedback file, re-delegates, pushes. Reviewer sees new commits addressing their feedback.",
            ),
            ex(
                "17-3",
                "Run the full cycle: delegate → PR → review → feedback → re-delegate → re-review → merge. Document the total time and number of human interventions.",
                "Full delegation lifecycle measurement.",
                "Total human time: spec writing (15 min) + two reviews (10 min each) = 35 min. Implementation time by Claude: ~30 min. Feature shipped with <1 hour of human attention.",
            ),
        ],
    },
    {
        "id": "18",
        "title": "Capstone: Claude Runs Your DSP Pipeline",
        "level": "Expert",
        "summary": "Design a complete DSP module pipeline. Write specs, verification, and orchestration. Claude implements everything. You review once.",
        "body": md("""
## Capstone: 3-Band Energy Meter — Delegated
This is the SAME capstone as the interactive course. But your approach is completely different.

### What YOU produce (your deliverables)
```
tasks/
  01-energy-types.md          — types and config header
  02-energy-init.md           — initialization function
  03-energy-process.md        — processing function
  04-energy-tests.md          — unit and golden tests
  05-energy-integration.md    — integration with existing modules
scripts/
  orchestrate-energy.sh       — pipeline orchestration
  verify_energy_types.sh      — phase 1 verification
  verify_energy_init.sh       — phase 2 verification
  verify_energy_process.sh    — phase 3 verification
  verify_energy_tests.sh      — phase 4 verification
  verify_energy_all.sh        — full quality gate
CLAUDE.md                     — updated handbook
```

### What CLAUDE produces (delegated deliverables)
```
src/energy_meter.h
src/energy_meter.c
tests/test_energy_meter.c
tests/gen_golden_energy.py
tests/golden/energy_ref.bin
```

### Acceptance criteria (all automated)
- Build: `make` with -Werror
- Unit tests: impulse, DC, sine sweep
- Golden comparison: max error < 1e-5 vs Python reference
- Constraints: no malloc, dsp_ prefix, const correctness
- Git: clean history on feature branch, conventional commits
- Code: every function has Doxygen comment

### The run
```bash
./scripts/orchestrate-energy.sh
# Go get coffee. Come back. Review.
```

### Your total involvement
1. Write specs (30 min)
2. Write verification scripts (20 min)
3. Run orchestration (1 min)
4. Review final result (15 min)
5. Merge (1 min)

**Total: ~67 min for a feature that takes 3-4 hours to implement manually.**
"""),
        "exercises": [
            ex(
                "18-1",
                "Write all five task briefs for the energy meter pipeline. Each brief should be implementation-ready with specific deliverables, constraints, and acceptance criteria. Do NOT involve Claude.",
                "Pure specification work. This is YOUR job.",
                "Five task briefs covering types, init, process, tests, and integration. Each is detailed enough for any developer (human or AI) to implement from.",
            ),
            ex(
                "18-2",
                "Write all verification scripts. Each should verify its phase independently. verify_energy_all.sh runs them all.",
                "Quality gate infrastructure.",
                "Five verification scripts + aggregate. Each tests its phase. Aggregate runs all. Ready for pipeline use.",
            ),
            ex(
                "18-3",
                "Write `scripts/orchestrate-energy.sh` that delegates all five tasks in order, verifying between each. Update CLAUDE.md with energy meter conventions.",
                "Pipeline orchestration.",
                "Orchestration script ready. CLAUDE.md updated. Pipeline runs tasks 1→5 with verification between each.",
            ),
            ex(
                "18-4",
                "Run the pipeline. Do NOT intervene. Go do something else while it runs. Come back and review ONLY the final result.",
                "Pure delegation. Hands off.",
                "Pipeline ran. Claude implemented five phases. All verifications passed (or some failed and you re-run after refining specs). You reviewed the final diff only.",
            ),
            ex(
                "18-5",
                "Measure: total time YOU spent (specs + verification + review). Compare to estimated manual implementation time. Write the ROI analysis in `docs/delegation-roi.md`.",
                "ROI measurement for the delegation approach.",
                "Your time: ~60-80 min. Manual implementation: ~3-4 hours. As you get better at writing specs, the ratio improves.",
            ),
            ex(
                "18-6",
                "Final review: merge to main. Push. Open a PR if using GitHub. This feature was shipped with you writing ZERO lines of implementation code.",
                "Ship it. You're the tech lead.",
                "Feature shipped. PR merged. Zero implementation lines written by you. All your effort went into specification, verification, and review.",
            ),
        ],
    },
    {
        "id": "19",
        "title": "Model Selection for Delegation & AI Worker Mastery",
        "level": "Expert",
        "summary": "Choose the right model for each delegated task. Master the full advantage of AI as your autonomous coding worker.",
        "body": md("""
## Model selection in delegation context
When you delegate headless, you choose the model upfront. The right choice saves money and time:

```bash
# Bulk documentation — use fastest, cheapest model
claude -p "Add Doxygen to all functions in src/" --model claude-haiku-3.5 --allowedTools Read,Edit

# Feature implementation — default model balances quality and cost
claude -p "Read tasks/dc-blocker.md. Implement." --allowedTools Read,Edit,Bash

# Safety-critical review — use the strongest model
claude -p "Review src/isr.c for race conditions and priority inversion" --model claude-opus-4-20250514 --allowedTools Read
```

## Model selection matrix for delegation
| Delegation Type | Model Tier | Why |
|----------------|-----------|-----|
| Bulk edits (const, Doxygen, rename) | Fastest | Volume work, low reasoning |
| Feature implementation (from task brief) | Default | Good balance of quality/cost |
| Bug fix (from failing test) | Default | Pattern matching |
| Code review (security, safety) | Strongest | Subtle reasoning needed |
| Architecture analysis | Strongest | System-level thinking |
| Test generation | Default | Standard patterns |
| Golden vector comparison | Default | Numerical, well-defined |
| CI auto-fix (warnings) | Default | Standard fixes |
| Nightly health report | Default | Analysis + reporting |

## Cost management for delegation at scale
When delegating 10+ tasks per day:
```bash
# Track costs per task
claude -p "..." --output-format json 2>&1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Tokens: {data.get(\"usage\",{}).get(\"total_tokens\",\"?\")}')
"
```

## The full advantage: AI as your autonomous coding worker

### What you've built in this course
1. **Task briefs** → clear specifications any developer (human or AI) can implement
2. **CLAUDE.md hierarchy** → organizational rules that apply automatically
3. **Verification scripts** → machine-checkable acceptance criteria
4. **Delegation scripts** → standardized task execution pipeline
5. **Orchestration** → multi-task dependency management
6. **CI integration** → event-driven autonomous work
7. **PR workflows** → team-compatible review process
8. **Cost tracking** → budget-aware automation

### Why this approach beats interactive AI use
| Interactive (old way) | Delegation (your way) |
|---|---|
| You type prompts | Scripts send prompts |
| You press y/n on each edit | --allowedTools pre-authorizes |
| One task at a time | Batch / pipeline |
| You babysit the session | You review the result |
| Your time = Claude's time | Your time << Claude's time |
| Skills plateau after basics | Skills compound with better specs |

### The compounding advantage
Every task brief you write is reusable. Every verification script catches more bugs. Every CLAUDE.md rule prevents future mistakes. Your infrastructure gets better with every delegation — this is the **compounding return** of investing in specs over code.

### Where this goes next
- **Multiple AI workers**: different Claude instances for different repos
- **Hybrid teams**: some tasks delegated to AI, some to human juniors, same review process
- **AI-generated specs**: Claude analyzes codebase and PROPOSES task briefs you approve
- **Self-improving pipeline**: CI failures auto-generate task briefs for fixes
"""),
        "exercises": [
            ex(
                "19-1",
                "Delegate the SAME task with three different models (fastest, default, strongest). Compare: implementation quality, cost (/cost or output tokens), and time to complete. Log results in `docs/model-comparison.md`.",
                "Empirical model comparison for delegation.",
                "Comparison table with quality/cost/time for each model. Clear winner for this task type. Data-driven model selection.",
            ),
            ex(
                "19-2",
                "Update `scripts/delegate.sh` to accept a `--model` flag that passes through to Claude headless. Default to standard model. Use fastest for bulk tasks, strongest for reviews.",
                "Model-aware delegation infrastructure.",
                "delegate.sh accepts --model flag. `./scripts/delegate.sh bulk-doxygen --model fast`. Infrastructure supports model selection.",
            ),
            ex(
                "19-3",
                "Create `docs/delegation-cost-tracker.md` with a table: date, task, model, tokens, cost. Fill in from your recent delegations. Analyze: which tasks are expensive? Where can you save?",
                "Cost optimization through tracking.",
                "Cost data reveals patterns. Bulk tasks with strongest model waste money. Reviews with fastest model miss bugs. Optimize the mapping.",
            ),
            ex(
                "19-4",
                "Write `docs/ai-worker-mastery.md`: your definitive playbook for AI-delegated development. Cover: when to delegate vs do manually, model selection, spec writing tips, verification patterns, review efficiency, cost management.",
                "Your delegation operations manual.",
                "Comprehensive playbook. This document captures everything you've learned. A new team member reads this and can delegate effectively from day one.",
            ),
            ex(
                "19-5",
                "Final exercise: delegate a feature you would normally implement yourself. Track: your total time (spec + review only), estimated manual implementation time. Calculate the ROI. Is delegation worth it for this task?",
                "ROI measurement — the ultimate test.",
                "Your time: ~30 min spec + review. Manual time: ~2-3 hours. ROI: 4-6x. For complex tasks the ratio is even better. For trivial tasks, manual might win. Know when to delegate.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # DAILY DRILLS
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "drills",
        "title": "Daily Drills (Delegation reps)",
        "level": "All levels",
        "summary": "5-minute exercises to build delegation muscle memory. Write specs, not code.",
        "body": md("""
## How to use drills
Pick one drill per day. The key habit: **you write specifications, Claude writes code.**

## Drill categories
- Task brief writing speed
- Acceptance criteria precision
- Verification script patterns
- Headless delegation muscle memory
- Review efficiency
"""),
        "exercises": [
            ex(
                "D-01",
                "Write a task brief for a simple function (e.g., clamp a float to a range) in under 3 minutes. Include deliverables, constraints, and acceptance criteria.",
                "Speed spec writing.",
                "Brief written in <3 min. Covers: function signature, constraints (const, C99), test (boundary values). Delegatable.",
            ),
            ex(
                "D-02",
                "Delegate the task from D-01 headless. Time it: from command to verified result.",
                "Headless delegation speed.",
                "Typically 30-90 seconds for a simple function. Brief → delegate → verify → done.",
            ),
            ex(
                "D-03",
                "Write a verification script for a module in under 5 minutes. It should check: build, test, and at least one constraint.",
                "Verification script speed.",
                "Script written quickly. Checks three things. Reusable. Under 20 lines.",
            ),
            ex(
                "D-04",
                "Review a git diff in under 2 minutes. Make a merge/reject decision. Write one-line rationale.",
                "Review speed.",
                "Diff scanned. Decision made: merge or reject with reason. Fast but informed.",
            ),
            ex(
                "D-05",
                "Write a batch task brief for a cross-file change (e.g., add a header comment to all .h files). Delegate headless. Verify with `git diff --stat`.",
                "Batch delegation drill.",
                "Brief → delegate → all files updated → diff stat confirms scope. One command, many files.",
            ),
            ex(
                "D-06",
                "Take an existing module and write a task brief for improving it (add error handling, add bounds checks). Delegate. Compare before/after.",
                "Improvement delegation.",
                "Brief specifies improvements. Claude applies them. Before/after diff shows targeted enhancements.",
            ),
            ex(
                "D-07",
                "Write a one-line addition to CLAUDE.md. Run a delegation. Check if the new rule was followed. Total time: under 2 minutes.",
                "Handbook maintenance drill.",
                "New rule added. Delegation follows it. Handbook is a living document that improves with each drill.",
            ),
            ex(
                "D-08",
                "Pipe a file into Claude headless for analysis: `cat src/X.c | claude -p 'List all potential buffer overflows' --allowedTools Read`. Review the analysis without any code changes.",
                "Read-only analysis delegation.",
                "Analysis received. No code changed. Information used for future task briefs or reviews.",
            ),
            ex(
                "D-09",
                "Write feedback for a hypothetical failed task (3 bullet points). Re-delegate with the feedback. Verify the fixes.",
                "Feedback loop speed drill.",
                "Feedback written → re-delegated → fixes applied → verified. The loop should feel natural and fast.",
            ),
            ex(
                "D-10",
                "Delegate a task, then immediately start writing the NEXT task brief while Claude is working. When Claude finishes, delegate the next one. Pipeline your work.",
                "Parallel spec writing while Claude implements.",
                "While Claude implements task A, you wrote the brief for task B. When A finishes and verifies, B is immediately ready to delegate. This is management-level throughput.",
            ),
        ],
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HTML shell — warm red/orange accent for delegation course
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Claude Code Works FOR Me — Delegation Mastery</title>
  <style>
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --surface2: #243044;
  --text: #e7ecf3;
  --muted: #9aa8bc;
  --accent: #dc2626;
  --accent2: #f87171;
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
a { color: var(--accent2); }
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
  color: #fff;
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
button.btn-primary { background: var(--accent); color: #fff; }
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
          Open this file in any browser. Progress saves locally.
          <strong>%%TOTAL%% exercises</strong> · You write specs. Claude writes code.
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
const STORAGE_KEY = 'claude-delegator-course-progress-v1';

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
</script>
</body>
</html>
"""


def main():
    course = {
        "title": "Claude Code Works FOR Me — Delegation Mastery",
        "subtitle": "You Write Specs · Claude Writes Code · Task Briefs · Headless Pipelines · Quality Gates · PR Workflows",
        "version": "2026.09",
        "modules": MODULES,
    }
    total = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(course, ensure_ascii=False)
    page = HTML_TEMPLATE.replace("%%DATA%%", data_json).replace("%%TOTAL%%", str(total))
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT}  ({total} exercises across {len(MODULES)} modules)")


if __name__ == "__main__":
    main()
