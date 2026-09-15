#!/usr/bin/env python3
"""Generate index.html — Claude Code course for embedded DSP engineers.
Focused on what makes Claude Code UNIQUE: CLI-first, terminal-native,
headless-capable, permission-gated, CLAUDE.md memory, SSH/Docker/tmux."""
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
# MODULES — designed around Claude Code's UNIQUE advantages
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MODULES = [
    # ══════════════════════════════════════════════════════════════════════
    # PRE-SETUP
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "00",
        "title": "Pre-Setup: Installing Claude Code",
        "level": "Pre-Setup",
        "summary": "Install the CLI, authenticate, and optionally add the VS Code extension — everything from the terminal.",
        "body": md("""
## What is Claude Code?
Claude Code is Anthropic's **terminal-native agentic coding tool**. Unlike IDE-embedded AI assistants, Claude Code lives in your **shell**. It reads files, proposes diffs, runs commands, and drives multi-step workflows — all from a terminal prompt. No IDE required.

## Why terminal-first matters for embedded engineers
- You already live in terminals: build servers, SSH to targets, Docker containers, CI runners.
- Claude Code works **everywhere a shell exists** — headless Linux boxes, remote VMs, WSL, tmux sessions, Docker.
- No GUI dependency means it runs in CI pipelines, cron jobs, and automation scripts via headless mode.
- The permission model (`y`/`n` per action) maps perfectly to embedded safety culture: **review before execute**.

## Step 1: Install Node.js 18+ (if missing)
Claude Code requires Node.js. Check:
```bash
node --version
```
If missing, install from [nodejs.org](https://nodejs.org) or via your package manager:
```bash
# macOS
brew install node
# Ubuntu/Debian
sudo apt install nodejs npm
# Windows — download installer from nodejs.org
```

## Step 2: Install Claude Code CLI
```bash
npm install -g @anthropic-ai/claude-code
```
Verify:
```bash
claude --version
```
You should see a version number (e.g., `1.x.x`). If `command not found`, ensure npm's global bin is in your PATH.

Alternative (no global install):
```bash
npx @anthropic-ai/claude-code
```

## Step 3: Authenticate
```bash
claude
```
First launch opens a browser window for Anthropic account authentication (API key or SSO). Follow the prompts. The token is stored locally — you won't need to re-auth unless it expires.

## Step 4 (optional): VS Code extension
The extension is a **companion**, not a requirement. It gives you a sidebar view of Claude Code inside VS Code.
1. Open **VS Code** → Extensions (`Ctrl+Shift+X`).
2. Search **"Claude Code"** by Anthropic → Install.
3. A new icon appears in the Activity Bar (left sidebar). Click it → the panel connects to the CLI.

### Troubleshooting the extension
- If it can't find the CLI: verify `claude --version` works in VS Code's **integrated terminal**.
- If you use `nvm`: ensure VS Code inherits the right Node version (check `.nvmrc` or set in terminal profile).
- On Windows: restart VS Code after the npm global install so PATH refreshes.

## Why Claude Code is your ultimate coding worker
Claude Code isn't just an assistant — it's a **terminal-native coding worker** that:
- **Runs anywhere**: SSH, Docker, tmux, CI, cron — no GUI dependency
- **Follows rules**: CLAUDE.md is your persistent rulebook across all sessions
- **Self-corrects**: reads build errors, proposes fixes, rebuilds — without you copy-pasting
- **Works autonomously**: headless mode (-p) enables scripts, CI, and automation
- **Permission-gated**: you control every action with y/Y/n — embedded-safe by design
- **Cost-transparent**: /cost shows real-time token usage — no surprise bills

## Model selection from day one
Claude Code supports multiple models. Key insight: **use the right model for each task**.
- **Fastest**: bulk edits, boilerplate, documentation
- **Default**: implementation, bug fixes, test writing
- **Strongest**: architecture review, concurrency analysis, safety-critical code
Use `/model` to switch. You'll master this in Module 20.

## Step 5: Create your workspace
```bash
mkdir dsp-sandbox && cd dsp-sandbox
mkdir src tests scripts docs
echo "# DSP Sandbox — ARM Cortex-M4F target" > README.md
git init
claude
```
You are now inside Claude Code, in your project. Type your first prompt.
"""),
        "exercises": [
            ex(
                "00-1",
                "Install Claude Code CLI. Run `claude --version` in your terminal and note the version.",
                "If npm is missing, install Node.js 18+ first.",
                "Output shows a version like `1.x.x`. If 'command not found', add npm global bin to PATH:\n- Linux/macOS: `export PATH=\"$HOME/.npm-global/bin:$PATH\"`\n- Windows: restart terminal after npm install.",
            ),
            ex(
                "00-2",
                "Run `claude` in an empty folder. Complete authentication in the browser. Once you see the `>` prompt, type `What model are you?` then type `/quit` to exit.",
                "First run opens a browser for auth. After that, you land at a `>` prompt.",
                "Claude responds with its model name. `/quit` exits cleanly. The session token is now cached locally.",
            ),
            ex(
                "00-3",
                "Install the VS Code extension (Claude Code by Anthropic). Open a folder, click the sidebar icon, and verify the prompt input appears.",
                "The extension is optional but useful for seeing diffs visually.",
                "Sidebar shows an input box connected to the same Claude Code backend. You can type prompts here too.",
            ),
            ex(
                "00-4",
                "Create the `dsp-sandbox` project structure from the terminal (not Claude — do it yourself with `mkdir`). Then `cd dsp-sandbox && claude` to start your first session inside a real project.",
                "`mkdir -p src tests scripts docs && echo '# DSP Sandbox' > README.md && git init`",
                "You're now inside Claude Code in a project with src/, tests/, scripts/, docs/. Claude can see the entire directory tree.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # BEGINNER — Terminal Foundations
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "01",
        "title": "Your First Conversation in the Terminal",
        "level": "Beginner",
        "summary": "Talk to Claude Code at the > prompt — ask questions, see tool calls, understand the terminal-native UX.",
        "body": md("""
## The `>` prompt
When you run `claude` in a project, you see:
```
>
```
This is your prompt. Type natural language. Press Enter to send.

## What happens when you ask something
Claude Code doesn't just answer from memory — it **uses tools**. Watch the terminal output:
```
> What files are in this project?

⏺ Tool: list_directory
  Path: .

  README.md
  src/
  tests/
  scripts/
  docs/

There are 4 directories and 1 file in the project root...
```
Notice: Claude ran a **tool** (`list_directory`). It explored your actual filesystem. This is fundamentally different from a chatbot — it **acts**, then **reports**.

## Tool types you will see
- **Read** — reads a file's contents (automatic, no approval needed)
- **Write** — proposes a file edit or creation (needs your `y`/`n`)
- **Execute** — wants to run a shell command (needs your `y`/`n`)
- **Search** — greps or globs your codebase (automatic)

## Multi-line input
For long prompts, you can use `\\` at line end or just keep typing — Claude Code handles multi-line.

## The terminal is the UI
There are no buttons, no sidebars, no panels. Everything is text. Diffs are shown as colored text (`+` green, `-` red). This is the power: it works **anywhere** — SSH, tmux, Docker, CI.
"""),
        "exercises": [
            ex(
                "01-1",
                "Launch `claude` in `dsp-sandbox`. Ask: `What is the directory structure of this project?` — watch the tool calls in the terminal output. Note which tool Claude used to answer.",
                "Look for the tool label (e.g., `list_directory`, `glob`).",
                "Claude uses a listing or glob tool, shows the actual tree, then summarizes. It did NOT guess — it checked the filesystem.",
            ),
            ex(
                "01-2",
                "Ask: `Explain fixed-point Q15 multiply in one paragraph with a 3-line C example. Do not create any files.` Verify that no tools beyond thinking were used — no file writes.",
                "This tests read-only conversation. No tool approvals should appear.",
                "Claude answers with `(int16_t)(((int32_t)a * b) >> 15)` pattern. No Write or Execute tool calls. Pure conversation.",
            ),
            ex(
                "01-3",
                "Ask: `Search this project for any .c files.` Observe the search/grep tool Claude uses. Then ask: `How many lines total across all files?` — watch Claude chain tools.",
                "Claude should use grep/glob then possibly read + count.",
                "First: glob for *.c (finds none or few). Second: reads files and counts. Tool chaining visible in terminal.",
            ),
            ex(
                "01-4",
                "Type a question, then before Claude finishes responding press `Esc` (or `Ctrl+C`). Observe how Claude Code handles interruption. Then continue with a follow-up.",
                "Interruption is useful when Claude goes off track.",
                "Claude stops mid-response. You can give a new prompt or refine. The partial response is still in context.",
            ),
        ],
    },
    {
        "id": "02",
        "title": "The Diff-Accept Workflow: File Edits in Terminal",
        "level": "Beginner",
        "summary": "Claude proposes file changes as terminal diffs — you review and y/n each one. This is your primary safety gate.",
        "body": md("""
## How file edits work in the terminal
When Claude wants to create or modify a file, you see a **diff** in the terminal:
```
⏺ Write: src/biquad.h
  + #pragma once
  + #include <stdint.h>
  +
  + typedef struct {
  +     float z1, z2;
  + } BiquadState;
  +
  + void biquad_process(const float *in, float *out,
  +                     uint32_t n, const float *coeffs,
  +                     BiquadState *st);

Apply? (y/n)
```

Green `+` lines are additions. Red `-` lines are deletions. For edits to existing files, you see the full context diff.

## The y/n decision
- `y` — apply this edit to disk immediately
- `n` — reject; Claude acknowledges and you can ask for a different approach

This is **not** like an IDE auto-apply. You see every change before it hits disk. For embedded engineers used to code reviews, this is natural.

## Reject → Refine → Accept
The most powerful pattern:
1. Claude proposes a diff
2. You see something wrong → press `n`
3. You say: "Use `const` on the input pointer and add a length check."
4. Claude proposes a new diff incorporating your feedback
5. You press `y`

## Multiple file edits
When Claude modifies several files, each gets its own diff prompt. You can accept some and reject others.

## What makes this different from IDE agents
- You see the **raw diff** — no UI abstraction hiding changes
- Works identically over SSH, in tmux, in Docker — the review experience is the same everywhere
- You build the muscle memory of reading diffs in terminal, which transfers directly to `git diff` and code review
"""),
        "exercises": [
            ex(
                "02-1",
                "Ask Claude to create `src/biquad.h` with a `BiquadState` struct and `biquad_process` prototype. When the diff appears, read every line, then press `y` to accept.",
                "Focus on reading the terminal diff carefully before accepting.",
                "File created on disk. You practiced reading a terminal diff — green `+` lines for new file content.",
            ),
            ex(
                "02-2",
                "Ask Claude to add a `biquad_init` function prototype to the header. When the diff appears, press `n` to reject. Then say: 'Make it take a pointer to BiquadState and return void.' Accept the revised diff.",
                "Practice the reject → refine → accept cycle.",
                "First diff rejected. Second diff matches your specification. File updated only after `y`.",
            ),
            ex(
                "02-3",
                "Ask Claude to create both `src/biquad.c` (implementation) and update `src/biquad.h` (add Doxygen comments). You will see two separate diffs. Accept the `.c` file but reject the header change.",
                "Selective acceptance across multiple file diffs.",
                "The .c file is created. The header stays unchanged because you rejected that diff. Claude acknowledges the partial acceptance.",
            ),
            ex(
                "02-4",
                "Ask Claude to create `tests/test_biquad.c` with a main() that tests impulse response. Before accepting, check: does it `#include` the right header? Is the tolerance reasonable for float32? Then accept or reject based on your review.",
                "This is a real code review — in the terminal.",
                "You reviewed the diff for correct includes, sensible test logic, and appropriate tolerance (e.g., 1e-6). Accepted after verification.",
            ),
        ],
    },
    {
        "id": "03",
        "title": "Shell Commands & The Permission Gate",
        "level": "Beginner",
        "summary": "Claude proposes shell commands — you control execution with y/Y/n. Learn the trust escalation model.",
        "body": md("""
## How shell commands work
When Claude needs to build or test, you see:
```
⏺ Execute: gcc -std=c99 -Wall -o build/test_biquad src/biquad.c tests/test_biquad.c -lm

Allow? (y/n/Y)
```

## The three responses
- **`y`** (lowercase) — allow this one command, this one time
- **`Y`** (uppercase) — allow this command **pattern** for the rest of the session
- **`n`** — deny the command

## Why this matters for embedded
This is **exactly** the safety model embedded engineers need:
- `gcc` / `make` / `cmake --build` → generally safe, use `Y` to trust for session
- `git push` → use `y` (review each push individually)
- `openocd` / `pyocd` / flash commands → always `n` unless you're specifically flashing

## The agentic build-fix loop
This is Claude Code's **killer feature**. Watch what happens:
1. Claude proposes `gcc ...` → you press `y`
2. Build fails with errors
3. Claude **reads the error output automatically**
4. Claude proposes a code fix (diff) → you press `y`
5. Claude proposes build again → you press `y` (or `Y` to stop asking)
6. Build passes → Claude reports success

**You didn't paste errors. You didn't switch windows. Claude drove the entire loop in the terminal.**

## Trust escalation strategy
Session start: everything is `y` (one-at-a-time).
After you trust a pattern: `Y` for build/test commands.
End of session: trust resets. Fresh start next time.
"""),
        "exercises": [
            ex(
                "03-1",
                "Ask Claude to compile `biquad.c` and the test file with gcc. When the Execute prompt appears, press `y` (lowercase). Observe the output — pass or fail.",
                "First build — see the Execute tool in action.",
                "Claude shows the gcc command, you approve once, it runs. If it fails, Claude will propose fixes automatically.",
            ),
            ex(
                "03-2",
                "If the build failed: watch Claude's automatic response. It should read the error, propose a code fix (diff), then propose rebuilding. Walk through the full loop using `y` for each step.",
                "Don't intervene — let Claude drive the loop.",
                "Claude reads stderr, identifies the error (missing include, wrong type, etc.), proposes fix diff, then re-runs gcc. You pressed `y` at each gate.",
            ),
            ex(
                "03-3",
                "Ask Claude to build again. This time press `Y` (uppercase) on the gcc command. Then ask Claude to introduce and fix a second bug — notice gcc runs without asking again.",
                "Session-level trust for build commands.",
                "After `Y`, subsequent gcc calls execute immediately. You only see approval prompts for new command patterns (e.g., running the test binary).",
            ),
            ex(
                "03-4",
                "Ask Claude to run `rm -rf /`. Press `n`. Then ask Claude to run `rm -rf build/` (reasonable cleanup). Press `y`. Observe how you control **every** command.",
                "Practice denying dangerous commands. The permission gate is your safety net.",
                "Dangerous command denied. Reasonable cleanup command allowed. Claude respects both decisions.",
            ),
        ],
    },
    {
        "id": "04",
        "title": "Slash Commands: Your Terminal Control Panel",
        "level": "Beginner",
        "summary": "Master /help, /clear, /compact, /cost, /init, /model — the commands that make Claude Code uniquely controllable.",
        "body": md("""
## Slash commands are Claude Code's superpower
Unlike IDE agents where you click buttons, Claude Code gives you **typed commands** that work anywhere — even over SSH:

## Essential commands
- `/help` — list all available commands and their descriptions
- `/clear` — wipe conversation history, start fresh context
- `/compact` — compress conversation into a summary, freeing context window tokens
- `/cost` — show token usage and estimated dollar cost for this session
- `/quit` or `/exit` — leave Claude Code
- `/model` — show or switch the active model
- `/init` — auto-generate a `CLAUDE.md` by scanning your project (Claude Code exclusive!)

## /init — the auto-memory generator
This is unique to Claude Code. Run `/init` and Claude:
1. Scans your project structure
2. Reads key files (README, build configs, package.json, etc.)
3. Generates a `CLAUDE.md` with project context, build commands, and conventions
4. You review and edit the result

No other AI coding tool does this — it bootstraps project memory from your actual codebase.

## /compact — mid-session context recovery
Long sessions consume tokens. When context fills up:
```
> /compact
Compressing conversation... (summarized 12,847 tokens into 1,203)
```
Claude retains key decisions and file states but frees space for more work.

## /cost — budget awareness
```
> /cost
Session: 24,531 input tokens, 8,120 output tokens
Estimated cost: $0.12
```
No other AI coding tool gives you real-time session cost tracking in the terminal.
"""),
        "exercises": [
            ex(
                "04-1",
                "Run `/help` inside Claude Code. List (in your notes) every slash command available and write a one-line description of each.",
                "This is your reference card.",
                "You should find: /help, /clear, /compact, /cost, /quit (or /exit), /model, /init, and possibly others depending on version.",
            ),
            ex(
                "04-2",
                "Run `/init` in your `dsp-sandbox` project. Let Claude scan the project and generate a `CLAUDE.md`. Review what it produced — how accurate is it?",
                "This bootstraps project memory automatically.",
                "Claude generates CLAUDE.md with project structure, detected languages, build system hints. Quality depends on what's in the project. You can edit it afterwards.",
            ),
            ex(
                "04-3",
                "Have a 5-message conversation about DSP filter design. Run `/cost` to see token usage. Then run `/compact` and run `/cost` again. Note the token reduction.",
                "Track the before/after token counts.",
                "Before compact: higher token count. After: significantly reduced. Claude retains key decisions in the compressed summary.",
            ),
            ex(
                "04-4",
                "After `/compact`, ask Claude a follow-up about the filter discussion. Verify it remembers the key points (filter type, sample rate, constraints). Then `/clear` and ask the same question — it should NOT remember.",
                "/compact preserves context; /clear destroys it.",
                "Post-compact: Claude remembers. Post-clear: Claude has no memory of the conversation. This demonstrates the difference between compression and reset.",
            ),
        ],
    },
    {
        "id": "05",
        "title": "Prompt Precision from the Terminal",
        "level": "Beginner",
        "summary": "Write prompts that work in a terminal agent: explicit file paths, constraints first, scope limits.",
        "body": md("""
## Terminal prompts are different from chat prompts
In an IDE, you can point at code, select text, or use @ mentions. In the terminal, your prompt is **all Claude gets** (plus CLAUDE.md and what it reads itself).

## Rule 1: Name files explicitly
```
BAD:  Fix the bug in the filter code.
GOOD: In src/biquad.c, the process function has an off-by-one:
      it reads N+1 samples instead of N. Fix the loop bound.
```

## Rule 2: Constraints before task
```
Constraints:
- C99 only, no C++ features
- No dynamic allocation
- Block size always power of 2
- All pointers: const where read-only

Task: Implement overlap-add convolution in src/ola.c
```

## Rule 3: Negative scope
```
Do NOT:
- Modify any file in third_party/
- Change the Makefile
- Add new dependencies

ONLY edit: src/fir.c and src/fir.h
```

## Rule 4: Verification command
```
After implementing, build with: make test
Report pass/fail.
```
This tells Claude to close the loop — implement, build, test, report.

## Rule 5: Multi-step with checkpoints
```
Step 1: Create the header with types and prototypes. Build.
Step 2: Implement init(). Build.
Step 3: Implement process(). Build and test.
```
Each step is a checkpoint. Claude builds after each, catching errors early.
"""),
        "exercises": [
            ex(
                "05-1",
                "Write a prompt with explicit file paths: tell Claude to create `src/gain.h` and `src/gain.c` implementing a float32 gain function. Include constraints (C99, no malloc, const input pointer) and a verification command (build with gcc).",
                "Apply Rules 1, 2, and 4 from the lesson.",
                "Claude creates both files respecting constraints, builds, and reports. Your prompt named exact files, stated constraints, and gave a build command.",
            ),
            ex(
                "05-2",
                "Write a prompt with negative scope: ask Claude to add a test for the gain function but explicitly forbid it from touching `src/gain.c` or `src/gain.h`. Watch if Claude obeys.",
                "Apply Rule 3. Claude should only create test files.",
                "Claude creates `tests/test_gain.c` only. No diffs proposed for forbidden files.",
            ),
            ex(
                "05-3",
                "Write a multi-step prompt: implement a peak detector in 3 steps (header → init → process), building after each step. Watch Claude execute checkpoints.",
                "Apply Rule 5. Three build-verify cycles.",
                "Claude executes three steps sequentially. Each step builds green before proceeding to the next.",
            ),
            ex(
                "05-4",
                "Write the worst possible prompt: 'Write DSP code.' Send it. Observe Claude's response — it will ask for clarification. Then write a precise version of the same request and compare the results.",
                "Contrast vague vs precise prompting.",
                "Vague prompt: Claude asks what kind of DSP, what language, what constraints. Precise prompt: Claude delivers exactly what you specified.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # INTERMEDIATE — Project Memory & Workflows
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "06",
        "title": "CLAUDE.md: Persistent Project Memory",
        "level": "Intermediate",
        "summary": "The file Claude reads on every session start — your project's rules, commands, and conventions encoded permanently.",
        "body": md("""
## CLAUDE.md is Claude Code's unique memory system
Unlike IDE agents that use per-rule files with frontmatter (like Cursor's `.mdc` files), Claude Code reads a single **`CLAUDE.md`** at your repo root. It's plain markdown. Claude reads it **automatically** on every session start.

## What goes in CLAUDE.md
```markdown
# DSP Audio Library

## Build
- Host build: `make` or `cmake -B build && cmake --build build`
- Tests: `make test` or `ctest --test-dir build`
- Toolchain: gcc, C99, `-Wall -Wextra -Werror`

## Conventions
- All DSP functions prefixed `dsp_`
- Use `stdint.h` types only (no bare `int` for sizes)
- No dynamic allocation in `src/dsp/`
- Q15 format: `dsp_q15_mul()`, `dsp_sat_q15()`
- Input pointers always `const`

## Test policy
- Golden vectors in `tests/golden/` as float32 binary
- Max error tolerance: 1e-6 for float; 1 LSB for Q15
- Every new function needs an impulse response test

## Forbidden
- Never modify `third_party/`
- No `malloc`/`free` in ISR-reachable paths
- Do not `git push --force`
- Do not commit `.bin` flash artifacts

## Git
- Conventional commits: type(scope): description
- Feature branches: `feat/module-name`
- Never commit directly to main
```

## Subdirectory CLAUDE.md files
Place additional `CLAUDE.md` in subdirectories for path-specific overrides:
- `tests/CLAUDE.md` — test conventions and golden vector paths
- `src/dsp/CLAUDE.md` — DSP-specific rules (e.g., no float in fixed-point module)
- `scripts/CLAUDE.md` — scripting conventions

When Claude works in a subdirectory, it reads **both** the root and local CLAUDE.md.

## /init vs manual
`/init` bootstraps a starting point. But the real value is **your manual additions**: the domain-specific rules Claude can't infer from scanning files.
"""),
        "exercises": [
            ex(
                "06-1",
                "Write `CLAUDE.md` at repo root with four sections: Build, Conventions, Test Policy, and Forbidden. Include your actual gcc/make command, `dsp_` prefix rule, and at least three forbidden patterns.",
                "Write it yourself (or use /init as a starting point and edit).",
                "CLAUDE.md with four sections. Build has exact commands. Conventions mention dsp_ prefix and stdint.h. Forbidden lists third_party/, malloc in ISR paths, and force-push.",
            ),
            ex(
                "06-2",
                "Exit Claude (`/quit`), re-launch (`claude`), and ask: `What naming convention do we use for DSP functions?` — Claude should answer from CLAUDE.md WITHOUT you telling it.",
                "Session-start auto-read test.",
                "Claude answers 'dsp_ prefix' from CLAUDE.md. It read the file on startup. You can verify by asking 'Did you read CLAUDE.md?'",
            ),
            ex(
                "06-3",
                "Create `tests/CLAUDE.md` with test-specific rules: 'All tests use assert macros from test_utils.h. Compare against golden files in tests/golden/. Test function names start with test_.' Then start a new session and ask Claude to write a test — observe if it follows BOTH CLAUDE.md files.",
                "Subdirectory CLAUDE.md stacking test.",
                "Claude follows root conventions (dsp_ prefix, C99) AND tests-specific rules (assert macros, golden comparison, test_ naming).",
            ),
            ex(
                "06-4",
                "Ask Claude to add a function using `malloc` inside `src/dsp/`. If Claude complies (violating CLAUDE.md), reject the diff and say 'Check CLAUDE.md forbidden section.' If Claude refuses citing the rule, congratulate it.",
                "Test rule enforcement.",
                "Claude should reference the 'no malloc in ISR-reachable paths' rule. If it doesn't, your CLAUDE.md wording needs to be clearer — iterate on it.",
            ),
        ],
    },
    {
        "id": "07",
        "title": "The Agentic Loop: Multi-Step Autonomy",
        "level": "Intermediate",
        "summary": "Give Claude a goal and watch it plan → code → build → read errors → fix → rebuild — all in the terminal.",
        "body": md("""
## What makes Claude Code's agentic loop special
In an IDE agent, you see edits applied inline and run commands in an embedded terminal panel. In Claude Code, the entire loop happens **in one terminal stream**:

```
> Implement a DC blocker in src/dc_block.c with tests. Build and run.

⏺ Read: src/dc_block.h (checking existing header)
⏺ Write: src/dc_block.c (34 lines)
  + #include "dc_block.h"
  + void dc_block_init(...) { ... }
  + void dc_block_process(...) { ... }
Apply? y

⏺ Write: tests/test_dc_block.c (28 lines)
  + #include "../src/dc_block.h"
  + int main() { ... assert ... }
Apply? y

⏺ Execute: gcc -std=c99 -Wall -o build/test_dc src/dc_block.c tests/test_dc_block.c -lm
Allow? y

  error: 'dc_block_state' undeclared

⏺ Read: src/dc_block.h (re-reading to find the issue)
⏺ Write: src/dc_block.c (fix: use correct struct name)
  - dc_block_state st;
  + DcBlockState st;
Apply? y

⏺ Execute: gcc ...
Allow? y   (or already Y-trusted)

  Build successful.

⏺ Execute: ./build/test_dc
Allow? y

  PASS: impulse response test
  All tests passed.
```

## Key observations
1. **Claude reads errors itself** — you didn't paste them.
2. **Claude proposes fixes** — you just approve.
3. **Claude rebuilds** — closing the loop.
4. **Everything is visible** — every tool call, every diff, every command output.

## When to intervene
- If Claude is going in circles (3+ failed attempts at the same error)
- If the approach is fundamentally wrong (wrong algorithm, wrong file)
- If you want to change direction

Just type your correction at the `>` prompt. Claude adjusts.

## Controlling scope
Always specify which files Claude may touch:
"Only edit `src/dc_block.c` and `tests/test_dc_block.c`. Do not modify headers or build files."
"""),
        "exercises": [
            ex(
                "07-1",
                "Give Claude a single prompt: 'Implement a simple gain function in src/gain.c with tests in tests/test_gain.c. Build and run until green. Use gcc with -std=c99 -Wall -lm.' Then sit back and only press y/n — count how many tool calls Claude makes to complete the task.",
                "Let Claude drive. Count the tool calls.",
                "Typical: 2 Writes (source + test), 1–3 Executes (build, possibly fix, run). Total ~4–8 tool calls for a simple function.",
            ),
            ex(
                "07-2",
                "Give Claude a task that will **fail** on first attempt: 'Implement a circular buffer in src/ringbuf.c with push/pop/peek. Test it with 1000 random operations.' Watch the full error-fix-rebuild cycle without intervening.",
                "More complex task — expect at least one build error or test failure.",
                "Claude iterates: implement → build error → fix → build → test fail → fix logic → rebuild → test pass. Multiple cycles visible in terminal.",
            ),
            ex(
                "07-3",
                "Give Claude a task with explicit scope restriction: 'Add error checking to all functions in src/. Do NOT create new files. Do NOT modify tests/.' Count how many files Claude proposes edits for and verify none are outside scope.",
                "Scope enforcement in agentic loop.",
                "Claude edits only src/*.c and src/*.h files. No test files touched. No new files created. Scope obeyed.",
            ),
            ex(
                "07-4",
                "Give Claude a task, let it start working, then interrupt mid-loop (Esc or Ctrl+C) and redirect: 'Actually, use fixed-point Q15 instead of float.' Watch Claude adapt to the mid-stream change.",
                "Mid-task redirection — unique to conversational agents.",
                "Claude acknowledges the change, reads what it already did, and switches approach. May propose diffs that undo float code and replace with Q15.",
            ),
        ],
    },
    {
        "id": "08",
        "title": "Git Workflows from the Agent",
        "level": "Intermediate",
        "summary": "Claude drives git: status, diff, commit, branch — each command goes through your permission gate.",
        "body": md("""
## Git in Claude Code
Every git command is a shell execution — same y/Y/n flow as any command:
```
⏺ Execute: git status
Allow? y

  On branch main
  Untracked files: src/gain.c src/gain.h tests/test_gain.c

⏺ Execute: git add src/gain.c src/gain.h
Allow? y

⏺ Execute: git commit -m "feat(dsp): add gain function with tests"
Allow? y
```

## Why this is better than IDE git buttons for learning
- You see the **exact** commands. No abstraction.
- You learn git commands by watching Claude use them.
- The same flow works over SSH on a build server.

## Git discipline via CLAUDE.md
Put in your CLAUDE.md:
```
## Git
- Never use git add -A (always name files explicitly)
- Conventional commits: type(scope): description
- Never force-push any branch
- Feature branches: feat/feature-name
```
Claude follows these rules because it reads CLAUDE.md on startup.

## Focused commits
"Commit only src/gain.c and src/gain.h with message 'feat(dsp): add float32 gain function'. Do NOT commit test files — those go in a separate commit."

Claude stages exactly the named files.

## Diff review before commit
"Show me `git diff --cached` before committing."
Claude runs the diff, you review in terminal, then approve the commit.
"""),
        "exercises": [
            ex(
                "08-1",
                "Ask Claude to run `git status` and explain what's tracked vs untracked. Press `y` for the command. Then ask it to run `git diff` if there are modifications. Review the output.",
                "Read-only git exploration through the agent.",
                "Claude runs git status, parses output, explains. Runs git diff if applicable. All via Execute tool calls you approved.",
            ),
            ex(
                "08-2",
                "Ask Claude to make two separate commits: one for source files (`src/`) and one for test files (`tests/`). Give it explicit commit messages for each. Verify it stages files correctly.",
                "Two-commit discipline via explicit prompting.",
                "Commit 1: `git add src/gain.c src/gain.h && git commit -m 'feat(dsp): add gain function'`. Commit 2: `git add tests/test_gain.c && git commit -m 'test(dsp): add gain function tests'`."),
            ex(
                "08-3",
                "Ask Claude to show `git log --oneline -5` and explain the recent history. Then ask it to create a branch `feat/dc-block` and switch to it.",
                "Git navigation + branching via agent.",
                "Claude shows log, explains, then runs `git checkout -b feat/dc-block`. All through Execute tool with your approval.",
            ),
            ex(
                "08-4",
                "Add a 'Git' section to CLAUDE.md with your rules (no force-push, conventional commits, named file staging). Start a new session and ask Claude to commit everything — does it follow the rules?",
                "CLAUDE.md git rule enforcement.",
                "Claude should stage files individually (not `git add -A`) and use conventional commit format, following CLAUDE.md.",
            ),
        ],
    },
    {
        "id": "09",
        "title": "Context Window Mastery",
        "level": "Intermediate",
        "summary": "Understand tokens, manage context with /compact and /clear, and structure sessions for maximum efficiency.",
        "body": md("""
## The context window is your session's memory
Everything in a Claude Code session lives in a **context window** — a fixed-size buffer of tokens:
- Your prompts
- Claude's responses
- File contents Claude read
- Shell command outputs
- CLAUDE.md contents

When the window fills up, Claude warns you and may lose earlier context.

## /cost — your context dashboard
```
> /cost
Session: 18,421 input tokens · 6,302 output tokens
Estimated cost: $0.09
```
Run `/cost` regularly — especially during long implementation tasks. Watch input tokens grow as Claude reads files and receives build output.

## /compact — compress without losing knowledge
```
> /compact
Summarizing conversation... Compressed 24,831 tokens into 2,104.
```
What `/compact` preserves:
- Key decisions (which algorithm, which approach)
- File names and what was changed
- Build status (passing/failing)
- Your stated constraints

What it may lose:
- Exact error messages from earlier builds
- Detailed discussion about rejected approaches
- Intermediate diffs

## /clear — nuclear reset
Everything gone. Fresh session. Use when:
- Switching to a completely different task
- Context is polluted with irrelevant discussion
- You want Claude to re-read CLAUDE.md fresh

## Session discipline for embedded work
1. **One task per session** when possible
2. **Build commands generate lots of output** — use /compact after a long build cycle
3. **Large file reads eat tokens** — ask Claude to read specific functions, not entire 1000-line files
4. **Check /cost before starting a new sub-task** — compact if > 50% consumed
"""),
        "exercises": [
            ex(
                "09-1",
                "Run `/cost` at the start of a session (note the baseline). Ask Claude to read a source file and explain it. Run `/cost` again. Note how many tokens the read + explanation consumed.",
                "Token awareness exercise.",
                "Before: near zero. After: several thousand tokens. Reading a file + explanation typically costs 500–3000 tokens depending on file size.",
            ),
            ex(
                "09-2",
                "Build up a long conversation (at least 8 messages about filter design and implementation). Run `/cost`, then `/compact`, then `/cost` again. Calculate the compression ratio.",
                "Measure compact's effectiveness.",
                "Typical compression: 5–10x reduction. A 20,000 token conversation might compress to 2,000–4,000.",
            ),
            ex(
                "09-3",
                "After `/compact`, ask Claude: 'What build command do we use?' and 'What naming convention did we agree on?' — verify it retained these from the compressed summary.",
                "Post-compact retention test.",
                "Claude remembers build commands and naming conventions from the compressed summary. These are 'key decisions' that /compact preserves.",
            ),
            ex(
                "09-4",
                "After `/clear`, ask the same two questions. Claude should NOT remember the conversation — but it SHOULD remember things from CLAUDE.md (if you wrote them there).",
                "/clear destroys conversation; CLAUDE.md persists across sessions.",
                "Conversation knowledge gone. CLAUDE.md knowledge retained. This shows why important rules belong in CLAUDE.md, not just in chat.",
            ),
        ],
    },
    {
        "id": "10",
        "title": "Debugging: Feed Errors, Get Hypotheses",
        "level": "Intermediate",
        "summary": "Claude reads compiler errors, runtime crashes, and test failures from the terminal — proposes fixes in the same loop.",
        "body": md("""
## Error-driven debugging in the terminal
Claude Code's debugging flow is unique because **it reads error output directly from the terminal** — no copy-paste, no screenshots, no IDE diagnostics panel.

```
> Build and run tests/test_fir.c

⏺ Execute: gcc -std=c99 -Wall -o build/test_fir src/fir.c tests/test_fir.c -lm
  error: implicit declaration of function 'dsp_fir_process'

⏺ Read: src/fir.h (checking if prototype exists)
⏺ Read: tests/test_fir.c (checking include)

The test file is missing #include "fir.h". The header exists but
isn't included in the test.

⏺ Write: tests/test_fir.c
  + #include "../src/fir.h"
Apply? y

⏺ Execute: gcc ...
  Build successful.

⏺ Execute: ./build/test_fir
  FAIL: test_impulse — expected 0.250000, got 0.000000

The output is all zeros. Let me check the process function...
⏺ Read: src/fir.c

The issue is in the convolution loop: the coefficient index is
never incremented (using `coeffs[0]` instead of `coeffs[k]`).

⏺ Write: src/fir.c (fix coefficient indexing)
Apply? y

⏺ Execute: gcc ... && ./build/test_fir
  PASS: test_impulse
  All tests passed.
```

## The complete loop happened in ONE terminal session
Claude: saw error → read files → hypothesized → proposed fix → rebuilt → tested.
You: pressed `y` four times.

## Feeding external diagnostics
For errors Claude didn't generate itself, paste them directly:
```
> Here is a GDB backtrace from our target:
> #0 0x08002a4c in dsp_fir_process (in=0x0, ...) at fir.c:42
> #1 0x08001b20 in main () at main.c:18
> What are the likely causes?
```
Claude analyzes without needing to run GDB itself.

## Limitations
Claude can't attach a debugger or interact with hardware. But it's an excellent **hypothesis generator** given error output, traces, or logs.
"""),
        "exercises": [
            ex(
                "10-1",
                "Intentionally introduce a bug: change a loop bound from `< n` to `<= n` in a process function. Ask Claude to 'build and run all tests, diagnose any failures.' Do NOT tell it where the bug is.",
                "Let Claude find the bug from test output alone.",
                "Claude builds, runs test, sees wrong output or crash, reads code, identifies off-by-one, proposes fix. Full diagnostic loop in terminal.",
            ),
            ex(
                "10-2",
                "Paste this fake GDB backtrace into Claude Code:\n`#0 0x0800dead in dsp_biquad_process (in=0x0, out=0x20001000, n=256) at biquad.c:28`\n`#1 0x08001234 in audio_callback () at main.c:45`\nAsk for ranked hypotheses and one defensive code change.",
                "External diagnostic analysis — no file execution needed.",
                "Claude ranks: 1) NULL input pointer, 2) uninitialized state, 3) invalid n. Proposes NULL check at function entry.",
            ),
            ex(
                "10-3",
                "Ask Claude to add `#ifdef DEBUG` trace macros to a DSP function that print intermediate values. Then build in debug mode (`-DDEBUG`) and run. Verify trace output appears.",
                "Conditional debugging via the agent.",
                "Trace macro like `#ifdef DEBUG` `#define TRACE(fmt,...) printf(fmt,##__VA_ARGS__)` `#else` `#define TRACE(...)` `#endif`. Debug build shows values; release build silent.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # ADVANCED — Power Features
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "11",
        "title": "Headless Mode: Claude Without a Human",
        "level": "Advanced",
        "summary": "Run Claude Code non-interactively with -p flag — the killer feature for scripts, CI, and automation.",
        "body": md("""
## What is headless mode?
Claude Code can run **without** an interactive terminal:
```bash
claude -p "List all functions in src/ and count their parameters"
```
Claude executes, prints the result to **stdout**, and exits. No `>` prompt, no interactive session.

## This is Claude Code's unique advantage over IDE agents
Cursor's agent requires the IDE to be open. Claude Code headless runs:
- In **CI pipelines** (GitHub Actions, GitLab CI, Jenkins)
- In **cron jobs** (nightly golden regen, weekly lint sweeps)
- In **shell scripts** (automated workflows)
- In **Docker containers** with no display
- Over **SSH** on remote build servers

## Key flags
```bash
# Basic headless prompt
claude -p "Fix all compiler warnings in src/"

# Restrict tools (safety!)
claude -p "Analyze code quality" --allowedTools "Read"

# JSON output for scripting
claude -p "List all TODOs" --output-format json

# Pipe input
cat error.log | claude -p "Diagnose these errors"

# Combine with shell tools
claude -p "List all functions in src/" | grep "dsp_"
```

## --allowedTools is critical
In headless mode there's no human to press `y`/`n`. You MUST restrict tools:
- `Read` — read files only (safest)
- `Read,Edit` — read and write files (no shell commands)
- `Read,Edit,Bash` — full power (use in trusted CI only)

## Exit codes
Claude Code returns meaningful exit codes for scripting:
- 0 = success
- Non-zero = error or failure

You can use this in shell scripts: `claude -p "..." && echo "Success" || echo "Failed"`

## Piping INTO Claude
```bash
# Feed a build log
make 2>&1 | claude -p "Diagnose these build errors and suggest fixes"

# Feed a git diff
git diff | claude -p "Review this diff for off-by-one errors"

# Feed test output
./run_tests 2>&1 | claude -p "Summarize failures and suggest fixes"
```
"""),
        "exercises": [
            ex(
                "11-1",
                "Run Claude headless: `claude -p 'List all .c and .h files in this project' --allowedTools Read` from your terminal (not inside an interactive session). Observe stdout output.",
                "First headless invocation — Read-only, safe.",
                "Claude scans the project, prints file list to stdout, and exits. No interactive session. Pure script-friendly output.",
            ),
            ex(
                "11-2",
                "Run: `claude -p 'Count the total lines of C code in src/' --allowedTools Read` and pipe the output to a file: `... > code_stats.txt`. Open the file and verify the content.",
                "Headless output piped to file — scriptable Claude.",
                "code_stats.txt contains Claude's analysis. This could be run nightly by a cron job.",
            ),
            ex(
                "11-3",
                "Pipe a git diff into Claude headless: `git diff HEAD~1 | claude -p 'Review this diff for potential buffer overflows' --allowedTools Read`. Read the review output.",
                "Piping external data into headless Claude.",
                "Claude receives the diff via stdin, analyzes it, and prints findings to stdout. This is a lightweight automated code review.",
            ),
            ex(
                "11-4",
                "Write a shell script `scripts/auto_review.sh` that: 1) runs `git diff HEAD~1`, 2) pipes it to Claude headless with review instructions, 3) saves output to `review_report.txt`. Make it executable and run it.",
                "Building an automation script around headless Claude.",
                "Script chains git diff → Claude headless → file output. Can be added to CI or run on commit hooks.",
            ),
        ],
    },
    {
        "id": "12",
        "title": "SSH, Docker, tmux: Claude Everywhere",
        "level": "Advanced",
        "summary": "Claude Code runs anywhere a terminal exists — remote servers, containers, multiplexed sessions. No GUI needed.",
        "body": md("""
## Why this matters
IDE agents are tied to a graphical environment. Claude Code is tied to **nothing but a terminal**.

## SSH: remote development
```bash
ssh build-server
cd /home/user/firmware-project
claude
```
You're now running Claude Code on a remote build server. Same UX as local. Same diff-review workflow. Same /compact, /cost, /clear.

Use case: your cross-compiler and target hardware are on a dedicated build machine. You SSH in and use Claude Code to develop, build, and test — without installing any IDE.

## Docker: containerized development
```dockerfile
FROM node:18
RUN npm install -g @anthropic-ai/claude-code
WORKDIR /app
COPY . .
```
```bash
docker run -it -v $(pwd):/app my-dsp-image claude
```
Claude Code inside a container with your toolchain pre-installed.

## tmux: multiplexed sessions
```bash
tmux new-session -s dev
# Pane 1: Claude Code
claude
# Pane 2: (Ctrl+B %) manual builds and testing
make && ./build/test_all
```
Side-by-side: Claude in one pane, your manual work in another. Both in the same terminal.

## The embedded engineer's dream setup
```
tmux pane 1: Claude Code (AI agent)
tmux pane 2: minicom/picocom (UART console)
tmux pane 3: openocd (debug server)
tmux pane 4: build terminal (make/cmake)
```
Claude edits code in pane 1; you build and flash from pane 4; see target output in pane 2. All over SSH. No IDE.
"""),
        "exercises": [
            ex(
                "12-1",
                "Open a tmux session with two panes (horizontal split: `Ctrl+B %`). In pane 1, run `claude`. In pane 2, keep a shell ready for manual commands. Use Claude in pane 1 to create a file, then verify it exists in pane 2 with `ls`.",
                "tmux + Claude Code side-by-side. (If on Windows without tmux, use two terminal tabs.)",
                "Pane 1: Claude creates file. Pane 2: `ls` confirms file exists. Demonstrates real-time collaboration between Claude and your manual work.",
            ),
            ex(
                "12-2",
                "If you have access to a remote machine (or WSL): SSH in, install Claude Code there (`npm install -g @anthropic-ai/claude-code`), and run `claude` in a remote project. Verify the UX is identical to local.",
                "Remote Claude Code — same experience everywhere. Skip if no remote access.",
                "Identical UX over SSH. Diffs look the same. /compact, /cost, /clear all work. No GUI dependency.",
            ),
            ex(
                "12-3",
                "Run Claude Code headless inside a command substitution: `FUNC_COUNT=$(claude -p 'Count functions in src/' --allowedTools Read)` then `echo $FUNC_COUNT`. Claude's output is now a shell variable.",
                "Claude as a shell pipeline component.",
                "The function count is stored in a shell variable. Claude Code's stdout output integrates with standard shell tooling.",
            ),
        ],
    },
    {
        "id": "13",
        "title": "Test-Driven Development with the Agent",
        "level": "Advanced",
        "summary": "Write failing tests, then let Claude implement until green — TDD at agent speed with terminal visibility.",
        "body": md("""
## TDD in Claude Code
The terminal-native workflow makes TDD iterations **visible and fast**:

1. You: "Here is a failing test. Implement the function to make it pass."
2. Claude: writes implementation → builds → runs test → reads failure → fixes → rebuilds → passes
3. You: pressed `y` at each gate, watching the entire loop scroll by

## Why TDD + Claude Code is powerful
- **Tests encode contracts**: "output within 1e-5 of reference" is unambiguous
- **Claude closes the loop itself**: implement → build → test → fix → rebuild
- **You see every step**: no hidden magic, every diff visible
- **Golden vectors are ground truth**: Claude targets them, not abstractions

## The test-first prompt pattern
```
I have tests/test_fir.c with the following test:
- Unit impulse input {1,0,0,...} with coefficients {0.25, 0.5, 0.25}
- Expected output: {0.25, 0.5, 0.25, 0, 0, ...}
- Tolerance: 1e-6

The test fails because dsp_fir_process() doesn't exist yet.
Implement it in src/fir.c. Build and run until green.
```

## Python golden → C test pipeline
```
Step 1: Create tests/gen_fir_golden.py that generates a 256-point
        golden output for our FIR filter using scipy.signal.lfilter.
        Save as tests/golden/fir_out.bin (float32 binary).

Step 2: Create tests/test_fir_golden.c that loads the golden file,
        runs our C implementation, and compares with max error < 1e-6.

Step 3: Build and run until green.
```
"""),
        "exercises": [
            ex(
                "13-1",
                "Write a test `tests/test_fir_impulse.c` YOURSELF (manually, not via Claude) that tests a 3-tap FIR with known impulse response. The test should FAIL because the function doesn't exist. Then ask Claude: 'Implement dsp_fir_process to make this test pass. Build and run.'",
                "You write the test. Claude writes the implementation. TDD roles.",
                "Claude implements FIR, builds (may fail first), fixes, builds again, runs test, passes. You watch the full loop.",
            ),
            ex(
                "13-2",
                "Ask Claude to add a SECOND test (step response: all-ones input) to the same test file. Run it WITHOUT changing the implementation. It should pass if the FIR is correct.",
                "Adding tests without changing code — verification of correctness.",
                "New test passes immediately if FIR is correct. If not, Claude proposes implementation fix. Tests are additive.",
            ),
            ex(
                "13-3",
                "Ask Claude to create a Python script `tests/gen_golden.py` that generates a float32 golden vector for a 256-point sine through the FIR, then create a C test that loads and compares.",
                "Full cross-language golden vector pipeline.",
                "Python generates binary. C test reads file, processes through FIR, compares. Claude drives both sides.",
            ),
            ex(
                "13-4",
                "Give Claude a deliberately wrong test (expected value is incorrect). See if Claude implements code to pass the wrong test, or if it questions the expected value.",
                "Meta-exercise: does Claude blindly target tests or reason about correctness?",
                "Claude may either: implement to match (wrong) expectation, or note the expected value seems incorrect. Either outcome teaches about AI agent limitations.",
            ),
        ],
    },
    {
        "id": "14",
        "title": "CI/CD Integration with Headless Claude",
        "level": "Advanced",
        "summary": "Put Claude Code in GitHub Actions, scripts, and cron jobs — automated code fixes, reviews, and generation.",
        "body": md("""
## Claude in CI: the unique proposition
No other AI coding tool gives you a **non-interactive agent you can run in CI**. Claude Code headless mode enables:

## Use case 1: Auto-fix warnings on push
```yaml
# .github/workflows/fix-warnings.yml
name: Auto-fix warnings
on: push
jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '18' }
      - run: npm install -g @anthropic-ai/claude-code
      - run: |
          claude -p "Fix all compiler warnings in src/. Build with 'make'." \\
            --allowedTools "Read,Edit,Bash"
      - run: |
          if [ -n "$(git diff)" ]; then
            git add -A && git commit -m "fix: auto-resolve warnings"
            git push
          fi
```

## Use case 2: Nightly golden vector regeneration
```bash
#!/bin/bash
# scripts/nightly_golden.sh — run via cron
cd /path/to/project
claude -p "Regenerate all golden vectors in tests/golden/ using Python scripts. Run tests. If all pass, commit with message 'chore: regen goldens'." \\
  --allowedTools "Read,Edit,Bash"
```

## Use case 3: PR review comment
```bash
# On PR, run review
DIFF=$(gh pr diff $PR_NUMBER)
echo "$DIFF" | claude -p "Review this diff for buffer overflows, off-by-one errors, and missing const qualifiers." --allowedTools "Read"
```

## Safety rules for CI
- **Always restrict --allowedTools** to minimum needed
- **Read-only** for review/analysis tasks
- **Read,Edit** for code generation (no shell commands)
- **Read,Edit,Bash** only for trusted build/test pipelines
- **Never allow Bash in untrusted contexts** (PRs from forks!)
- Treat Claude's CI commits like any automated commit: review before merge
"""),
        "exercises": [
            ex(
                "14-1",
                "Write a shell script `scripts/lint_check.sh` that runs Claude headless with --allowedTools Read to analyze code quality in `src/`. The script should capture output and exit with Claude's exit code.",
                "Read-only CI analysis script.",
                "Script: `claude -p 'Analyze src/ for code quality issues: missing const, magic numbers, missing error checks' --allowedTools Read`. Output captured, exit code propagated.",
            ),
            ex(
                "14-2",
                "Write a script `scripts/auto_fix_warnings.sh` that: 1) builds with `make`, 2) if warnings exist, runs Claude headless with Read,Edit,Bash to fix them, 3) rebuilds to verify, 4) shows git diff of changes.",
                "Auto-fix pipeline for local use or CI.",
                "Script chains: build → detect warnings → Claude fix → rebuild → diff. Could be a pre-commit hook.",
            ),
            ex(
                "14-3",
                "Draft `.github/workflows/claude-review.yml` that on pull_request runs Claude headless to review the PR diff (piped via `gh pr diff`) with Read-only tools. Output goes to a step summary.",
                "CI code review via Claude headless.",
                "YAML workflow: checkout, install Claude, `gh pr diff | claude -p 'Review...' --allowedTools Read`, capture output to `$GITHUB_STEP_SUMMARY`.",
            ),
            ex(
                "14-4",
                "Draft a nightly cron workflow that runs Claude headless to regenerate golden vectors, runs tests, and opens a PR if there are changes. Use `gh pr create` at the end.",
                "Full automated pipeline: generate → test → PR.",
                "Cron schedule, Claude regen with Edit+Bash, test, `git diff --exit-code || gh pr create`. Complete automation loop.",
            ),
        ],
    },
    {
        "id": "15",
        "title": "MCP: Extending Claude Code with External Tools",
        "level": "Advanced",
        "summary": "Connect GitHub, databases, and custom APIs via Model Context Protocol — Claude calls external tools with your approval.",
        "body": md("""
## What MCP adds to Claude Code
Model Context Protocol lets Claude call **external tools** beyond the built-in file/shell:
- GitHub API: issues, PRs, checks, reviews
- Databases: read-only queries
- Custom services: benchmark servers, artifact stores
- Documentation servers

## How MCP differs in Claude Code vs IDE agents
In Claude Code, MCP tool calls go through the **same permission gate** as everything else:
```
⏺ MCP Tool: github.list_issues
  repo: my-org/dsp-firmware
  labels: ["bug", "dsp"]
Allow? y
```
You see the tool name, parameters, and approve. Same y/Y/n model.

## Configuring MCP servers
Configuration depends on version — check `claude --help` or docs. Typically:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "..." }
    }
  }
}
```

## Embedded-safe MCP strategy
**Read-only tools only** for production systems:
- ✅ Read issues, PRs, CI status
- ✅ Fetch benchmark CSVs from artifact server
- ✅ Query test result database
- ❌ Flash firmware via MCP
- ❌ Write to production databases
- ❌ Trigger OTA updates
"""),
        "exercises": [
            ex(
                "15-1",
                "Ask Claude: 'What MCP tools do you currently have access to?' Document the answer. If none: that's normal for a fresh install.",
                "MCP inventory check.",
                "Claude lists available MCP tools or reports none. This is your baseline.",
            ),
            ex(
                "15-2",
                "Even without MCP, Claude can use `gh` CLI as a fallback. Ask Claude to run `gh issue list` (if you have a GitHub remote) or `gh --version` to verify gh is available.",
                "CLI-based GitHub access as MCP alternative.",
                "If gh is installed: issue list or version shown. If not: Claude reports missing tool and suggests install.",
            ),
            ex(
                "15-3",
                "Write a spec document `docs/mcp-spec.md` describing a hypothetical read-only MCP tool `get_dsp_benchmark` that returns CSV data for a given test run. Include: tool name, parameters, return format, auth method.",
                "Design exercise for custom MCP tooling.",
                "Spec doc with: tool name, input (run_id: string), output (CSV text), auth (Bearer token from env), rate limit (10 req/min).",
            ),
        ],
    },
    {
        "id": "16",
        "title": "Advanced Prompting Patterns",
        "level": "Advanced",
        "summary": "Constraint-first, plan-execute-verify, negative scope, incremental delivery — patterns that exploit terminal agent strengths.",
        "body": md("""
## Pattern 1: Constraint → Task → Verify
```
Constraints:
- C99, no C++ features
- No dynamic allocation
- ARM Cortex-M4F, single-precision FPU
- Block size always power of 2
- All functions prefixed dsp_

Task: Implement 4-stage biquad cascade in src/biquad_cascade.c

Verify: Build with make and run tests/test_cascade.c
```
Constraints FIRST prevents wrong assumptions. Verify LAST closes the loop.

## Pattern 2: Plan → Execute → Verify (three separate prompts)
```
Prompt 1: "Plan adding a peak detector module. List files, functions,
           tests. Do NOT write any code yet."
(Review plan)
Prompt 2: "Execute the plan. Build after each file."
Prompt 3: "Run all tests and give me a pass/fail summary."
```

## Pattern 3: Scope restriction
```
You may ONLY edit: src/fir.c, src/fir.h, tests/test_fir.c
Do NOT touch: Makefile, CLAUDE.md, any other source file
Do NOT run: any git command
```
This is critical in the terminal — Claude will obey file restrictions.

## Pattern 4: Pipe-augmented prompts (headless only)
```bash
# Feed build errors for diagnosis
make 2>&1 | claude -p "Diagnose and fix these build errors"

# Feed test output for analysis
./run_tests 2>&1 | claude -p "Which tests failed and why?"

# Feed code for review
cat src/fir.c | claude -p "Review this for MISRA-C violations"
```
These work because Claude Code is a terminal tool — it speaks stdin/stdout.

## Pattern 5: Iterative refinement
```
Step 1: "Create header with types and prototypes only."
Step 2: "Implement init function. Build."
Step 3: "Implement process (naive loop). Build and test."
Step 4: "Optimize process with 4x loop unrolling. Build and test.
         Compare cycle count (or host timing) vs step 3."
```
Each step has a build checkpoint. Claude can't skip ahead.
"""),
        "exercises": [
            ex(
                "16-1",
                "Use Pattern 1 (Constraint → Task → Verify): list 5 constraints, give a task (e.g., implement RMS energy calculator), and include a verify step. Send as one prompt.",
                "All three parts in one prompt.",
                "Claude respects all constraints, implements, builds, tests. No violations.",
            ),
            ex(
                "16-2",
                "Use Pattern 2 (Plan → Execute → Verify): send three separate prompts for adding a noise gate module. Review the plan before allowing execution.",
                "Three-turn structured workflow.",
                "Prompt 1: plan with file list. Prompt 2: implementation. Prompt 3: test summary. Each step separate.",
            ),
            ex(
                "16-3",
                "Use Pattern 4 (pipe-augmented): run `cat src/biquad.c | claude -p 'Review this code for potential integer overflow in Q15 operations' --allowedTools Read` in headless mode. Compare the review quality to an interactive review.",
                "Pipe code into headless Claude for review.",
                "Headless review output is focused and concise — designed for scripting. Compare to interactive: similar quality but no back-and-forth.",
            ),
            ex(
                "16-4",
                "Use Pattern 5 (iterative refinement): implement a feature in 4 explicit steps, with build checkpoints. If step 3 fails, Claude must fix before step 4.",
                "Stepwise implementation with gates.",
                "Four steps executed in order. Each builds green. If a step breaks, Claude fixes before proceeding.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # EXPERT
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "17",
        "title": "Multi-file Refactors & Codebase Search",
        "level": "Expert",
        "summary": "Large renames, module extractions, and architecture changes — Claude searches before it edits.",
        "body": md("""
## Claude Code's search tools
Claude uses grep and glob to find symbols across your codebase:
```
> Rename dsp_biquad_state to DspBiquadState in all files

⏺ Search: grep "dsp_biquad_state" --include="*.{c,h}"
  src/biquad.h:5:  typedef struct dsp_biquad_state {
  src/biquad.c:12: void init(dsp_biquad_state *st) {
  src/biquad.c:28: void process(dsp_biquad_state *st, ...) {
  tests/test_biquad.c:8: dsp_biquad_state state;

Found 4 files. Proposing renames...
```

## Safe large refactors in the terminal
The terminal diff view is actually **ideal** for large refactors because:
- You see **every** change as a separate diff
- You can accept some files and reject others
- The sequential review mirrors `git add -p` discipline

## Refactor recipe
1. "Search for all uses of `BLOCK_SIZE` in the project." (search only)
2. "Plan replacing 256 with `DSP_BLOCK_SIZE` from `src/config.h`." (plan only)
3. "Execute: define in config.h, replace everywhere." (edits)
4. "Build and run all tests." (verify)

## Module extraction
"Split `src/dsp.c` (400 lines) into `src/fir.c`, `src/iir.c`, `src/dc_block.c`. Create matching headers. Update Makefile. Build."

Claude: searches for function boundaries → creates new files → moves code → updates includes → updates build → builds → tests.
"""),
        "exercises": [
            ex(
                "17-1",
                "Ask Claude to search for ALL uses of a specific symbol across the project (e.g., a function name or type). Tell it: 'Search only, do not edit.' Count the occurrences.",
                "Search-only exercise. Observe grep/glob tools.",
                "Claude uses search tools, reports file:line for every occurrence. No edits proposed.",
            ),
            ex(
                "17-2",
                "Ask Claude to rename a type across all files (e.g., `BiquadState` → `dsp_biquad_state_t`). Review each file's diff individually. Accept all, then build and test.",
                "Multi-file rename via terminal diffs.",
                "Each file gets its own diff. You review and accept each. Build and tests pass after all renames.",
            ),
            ex(
                "17-3",
                "Ask Claude to extract a utility function that's duplicated in two test files into a shared `tests/test_utils.h`. Update both test files.",
                "Deduplication refactor.",
                "New shared header created. Both test files updated to use it. Duplicated code removed. Build green.",
            ),
        ],
    },
    {
        "id": "18",
        "title": "Claude Code SDK & Programmatic Agents",
        "level": "Expert",
        "summary": "Run Claude programmatically from TypeScript/Python — nightly DSP regression, auto-triage, batch processing.",
        "body": md("""
## The SDK: Claude Code as a library
Beyond the CLI, Claude Code can be invoked **programmatically**:

### TypeScript
```typescript
import { claude } from '@anthropic-ai/claude-code';

const result = await claude({
  prompt: "Fix compiler warnings in src/",
  allowedTools: ["Edit", "Read", "Bash"],
  cwd: "/path/to/dsp-project"
});
console.log(result.stdout);
```

### Python
```python
import subprocess, json

result = subprocess.run(
    ["claude", "-p", "List all DSP functions", "--allowedTools", "Read",
     "--output-format", "json"],
    capture_output=True, text=True, cwd="/path/to/project"
)
data = json.loads(result.stdout)
```

## Use cases for DSP teams
- **Nightly regression**: on golden vector diff → spawn Claude → update code → open PR
- **Auto-triage CI failures**: on red build → spawn Claude → analyze → comment on PR
- **Batch analysis**: iterate over 10 repos with the same review prompt
- **Internal tooling**: web UI that triggers Claude for specific DSP tasks

## Safety
- SDK agents inherit CLAUDE.md rules
- Always restrict allowedTools
- Never expose flash/JTAG tools to SDK-driven agents
- Treat SDK output like CI output: review before deploy

## vs Cursor SDK
Cursor's SDK runs agents inside the IDE context. Claude Code SDK runs **anywhere** — servers, CI, Docker, cron. No IDE needed. This is the fundamental difference.
"""),
        "exercises": [
            ex(
                "18-1",
                "Write a Python script `scripts/sdk_analyze.py` that invokes Claude Code headless via `subprocess.run` to analyze code quality in `src/`. Parse the output and print a summary.",
                "Programmatic Claude invocation.",
                "Script runs `claude -p '...' --allowedTools Read`, captures stdout, prints analysis. This is the simplest SDK pattern.",
            ),
            ex(
                "18-2",
                "Extend the script to accept a file path argument and review that specific file for DSP-related issues. Run it on two different files and compare outputs.",
                "Parameterized programmatic analysis.",
                "Script accepts argv[1] as filepath, pipes to Claude headless, outputs review. Different files get different reviews.",
            ),
            ex(
                "18-3",
                "Map which steps in your DSP development workflow could use SDK automation vs must stay interactive. Write the mapping in `docs/automation-map.md`.",
                "Design exercise: human vs machine boundary.",
                "Human: hardware bring-up, analog measurement, EMC compliance. Automate: host tests, lint, golden regen, doc sync, warning fix, code review.",
            ),
        ],
    },
    {
        "id": "19",
        "title": "Capstone: End-to-End Feature Shipment",
        "level": "Expert",
        "summary": "Ship a complete DSP module using every Claude Code skill: CLAUDE.md → TDD → agentic loops → git → headless CI.",
        "body": md("""
## Capstone: 3-Band Energy Meter
Implement a **3-band energy meter** (low / mid / high) for float32 audio:

### Deliverables
- `src/energy_meter.h` and `src/energy_meter.c`
- Configurable band edges via init function
- Host tests vs Python golden reference
- Build system updated (Makefile or CMake)
- CLAUDE.md updated with module conventions
- Clean git history on feature branch
- A headless script that runs the full test suite
- PR-ready description

### Acceptance criteria
- Bands: 20–300 Hz, 300–3000 Hz, 3000–20000 Hz
- Energy = RMS over block
- Max error vs Python reference: 1e-5
- All tests pass with `-Werror`

### Required techniques (use ALL of these)
1. **CLAUDE.md** — update with energy meter conventions
2. **Constraint-first prompting** — C99, no malloc, const correctness
3. **TDD** — write test first, then implement
4. **Agentic loop** — let Claude drive build-fix-test
5. **/compact** — manage context during long implementation
6. **Git via agent** — feature branch, focused commits
7. **Headless mode** — write a script that runs the full test suite non-interactively
8. **/cost** — track total session cost for the capstone
"""),
        "exercises": [
            ex(
                "19-1",
                "Plan only: ask Claude to plan the full energy meter implementation. List files, functions, tests, and git strategy. Do NOT code yet. Review the plan.",
                "Plan before execute.",
                "Plan includes: 2 source files, 1-2 test files, golden gen script, 3 commits (types, impl, tests), band edge validation notes.",
            ),
            ex(
                "19-2",
                "Create feature branch `feat/energy-meter`. Update CLAUDE.md with energy meter conventions. Implement slice 1: types, init, and stub process. Build green. Commit.",
                "First slice: compiles but doesn't compute yet.",
                "Branch created. CLAUDE.md updated. Header + stub source created. Builds clean. Committed with conventional message.",
            ),
            ex(
                "19-3",
                "TDD: write a test with known expected values. Then ask Claude: 'Implement the full process function to make tests pass. Build and run until green.' Let Claude drive the agentic loop. Use /compact if context gets large.",
                "Claude drives the full build-fix-test loop.",
                "Claude implements, builds, tests, fixes (possibly multiple iterations), passes. /compact used if needed. All visible in terminal.",
            ),
            ex(
                "19-4",
                "Create Python golden generator + C golden comparison test. Commit separately. Run /cost to check total session spending.",
                "Cross-language validation + cost awareness.",
                "Python generates golden binary. C test loads and compares. Separate clean commit. /cost shows total session cost.",
            ),
            ex(
                "19-5",
                "Write `scripts/test_energy_meter.sh` that runs Claude headless to build and test the energy meter. Run it and verify it passes non-interactively.",
                "Headless test automation for the capstone.",
                "Script: `claude -p 'Build and run all energy meter tests. Report pass/fail.' --allowedTools Read,Bash`. Runs and reports success.",
            ),
            ex(
                "19-6",
                "Ask Claude to review the entire feature branch diff for buffer overflows, missing bounds checks, and DSP accuracy issues. Fix any findings. Prepare a PR description with Summary, Test Plan, and Performance Notes.",
                "Self-review + PR prep.",
                "Review findings addressed. PR description ready. Clean git history on feature branch. Capstone complete.",
            ),
        ],
    },
    {
        "id": "20",
        "title": "Model Selection & AI Worker Advantages",
        "level": "Advanced",
        "summary": "Choose the right model via /model for each task. Understand why Claude Code as your coding worker is a force multiplier.",
        "body": md("""
## /model — choose the right brain for the job
Claude Code lets you switch models mid-session:
```
> /model
Current: claude-sonnet-4-20250514
Available:
  1. claude-sonnet-4-20250514 (default)
  2. claude-opus-4-20250514 (strongest)
  3. claude-haiku-3.5 (fastest)
Select: _
```

## Model selection by task type for embedded DSP
| Task | Recommended Tier | Why |
|------|-----------------|-----|
| Explain a register map | Default | Factual, well-documented topic |
| Debug DMA + ISR race condition | Strongest | Deep concurrent reasoning needed |
| Generate boilerplate C structs | Fastest | Repetitive pattern, low reasoning |
| Review code for buffer overflows | Strongest | Subtle security analysis |
| Write CMakeLists.txt | Default | Standard build system pattern |
| Fix compiler warnings | Default | Pattern matching, well-understood |
| Plan architecture refactor | Strongest | System-level reasoning |
| Add Doxygen comments | Fastest | Bulk repetitive task |
| Headless CI review | Default | Good balance for automation |
| Analyze priority inversion | Strongest | RTOS concurrency subtlety |

## Headless model selection
```bash
# Use strongest model for safety-critical review
claude -p "Review src/isr.c for concurrency issues" --model claude-opus-4-20250514 --allowedTools Read

# Use fastest for bulk tasks
claude -p "Add header guards to all .h files" --model claude-haiku-3.5 --allowedTools Read,Edit
```

## Why Claude Code as your coding worker is a force multiplier
### What AI workers give you (that humans can't match)
- **Terminal-native = everywhere**: works on SSH servers, Docker, CI — no GUI needed
- **Zero context-switch cost**: reads register map → writes code → fixes build → runs tests seamlessly
- **Infinite patience**: add const to 200 pointers, rename across 30 files — no fatigue
- **Instant domain recall**: every C quirk, every CMSIS function, every gcc flag
- **Headless autonomy**: works while you sleep (CI, cron, scripts)
- **Reproducible**: CLAUDE.md rules produce consistent behavior across sessions and team members

### What YOU contribute (that AI can't)
- **Domain judgment**: is this filter right for THIS application?
- **Hardware truth**: does this register sequence match the silicon?
- **System thinking**: power budget, latency, EMC implications
- **Safety assessment**: is this safe to deploy to production devices?

### The optimal split
You do the thinking and reviewing. Claude does the implementing and testing. CLAUDE.md keeps Claude on track. Tests verify the output. This is a **managed workflow**, not pair programming.
"""),
        "exercises": [
            ex(
                "20-1",
                "Run `/model` to see available models. Switch to the strongest model. Ask it to review a DSP function for subtle bugs. Then switch to default model and ask the same. Compare depth.",
                "Direct model comparison.",
                "Strongest: catches subtle issues (intermediate overflow, edge cases). Default: finds obvious issues. Cost difference visible via /cost.",
            ),
            ex(
                "20-2",
                "Run a headless command with explicit model flag: `claude -p 'Add Doxygen to all functions in src/' --model <fastest> --allowedTools Read,Edit`. Compare speed to doing it with the default model.",
                "Model selection for automation speed.",
                "Fastest model handles bulk documentation quickly. Default model is slower but may produce slightly better comments. For bulk tasks, fastest wins.",
            ),
            ex(
                "20-3",
                "Create a model selection guide in your CLAUDE.md: add a section 'Model Recommendations' mapping task types to models. This becomes your team's reference.",
                "Encode model selection in project memory.",
                "CLAUDE.md now has task→model mapping. Any team member using Claude Code in this project knows which model to use when.",
            ),
            ex(
                "20-4",
                "Write `docs/ai-worker-playbook.md`: for each task type in your DSP workflow, document (1) interactive vs headless, (2) which model, (3) what context to provide, (4) how to verify.",
                "Your operational manual for AI-assisted development.",
                "Playbook covers 10+ scenarios. This is your definitive guide to using Claude Code effectively in your project.",
            ),
            ex(
                "20-5",
                "Track session costs across one week using `/cost`. Log in `docs/cost-log.md`: date, task, model used, tokens, cost. Analyze: where did you overspend? Where could you use a cheaper model?",
                "Cost optimization through data.",
                "Week of cost data shows patterns: review tasks are expensive (use strongest), bulk tasks are cheap (use fastest). Optimize your model selection based on real data.",
            ),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    # DAILY DRILLS
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "drills",
        "title": "Daily Drills (Quick reps)",
        "level": "All levels",
        "summary": "5-minute exercises to build terminal-agent muscle memory. One per day.",
        "body": md("""
## How to use drills
Pick one drill per day. Repeat until the workflow is automatic. Every drill is designed for Claude Code's **terminal-native** UX.

## Drill categories
- Permission gate practice (y/Y/n)
- Slash command muscle memory
- Prompt precision
- Headless mode scripting
- Context management
- CLAUDE.md maintenance
"""),
        "exercises": [
            ex(
                "D-01",
                "Launch Claude, ask it to create a 10-element Hann window array in C. Accept the diff. Exit with `/quit`. Total time target: under 60 seconds.",
                "Speed drill: launch → prompt → accept → exit.",
                "Fast cycle. File created. Clean exit. Muscle memory for the basic loop.",
            ),
            ex(
                "D-02",
                "Ask Claude to explain a function in your code WITHOUT editing anything. Verify zero Write/Execute tool calls in the output.",
                "Read-only conversation discipline.",
                "Explanation provided. Only Read tools used. No diffs, no commands.",
            ),
            ex(
                "D-03",
                "Ask Claude to run a build command. Press `Y` (uppercase). Then ask for another build. Verify it runs without asking again.",
                "Trust escalation practice.",
                "Second build runs immediately. Session trust working.",
            ),
            ex(
                "D-04",
                "Run `/cost`. Note tokens. Ask a question. Run `/cost` again. Calculate the cost of one interaction.",
                "Cost awareness micro-drill.",
                "Typically 500–2000 tokens per Q&A round. Builds awareness.",
            ),
            ex(
                "D-05",
                "Run `/compact`. Then ask Claude what you were working on. Verify it retained the key context.",
                "Compact retention check.",
                "Key decisions and file names retained. Detail may be lost. CLAUDE.md info always preserved.",
            ),
            ex(
                "D-06",
                "Add one new rule to CLAUDE.md. `/quit`. Re-launch. Ask Claude about the rule. Verify it knows.",
                "CLAUDE.md update → session restart → verification.",
                "Rule persisted across sessions. Claude quotes it on startup.",
            ),
            ex(
                "D-07",
                "Run Claude headless: `claude -p 'Find all TODO comments in this project' --allowedTools Read`. Time how long it takes.",
                "Headless speed drill.",
                "Output to stdout. Typically 5–15 seconds for small projects. No interactive session overhead.",
            ),
            ex(
                "D-08",
                "Pipe a file into Claude headless: `cat src/biquad.c | claude -p 'How many functions are in this file?' --allowedTools Read`. Verify the count.",
                "Pipe input drill.",
                "Claude counts functions from stdin. Correct count verified manually.",
            ),
            ex(
                "D-09",
                "Ask Claude to compose a git commit message for your last change. Review it for conventional commit format. Reject if bad, accept if good.",
                "Commit message review via agent.",
                "Message like `feat(dsp): add peak detector`. Concise, scoped, descriptive.",
            ),
            ex(
                "D-10",
                "Ask Claude to run a dangerous-sounding command (e.g., `rm -rf src/`). Press `n`. Then ask it to run `ls src/` instead. Press `y`. Practice the deny → redirect flow.",
                "Permission gate reflex drill.",
                "Dangerous: denied. Safe alternative: allowed. The gate protects you.",
            ),
        ],
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HTML shell — same architecture as cursor-course, amber accent theme
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Claude Code Zero to Hero — Embedded DSP Engineers</title>
  <style>
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --surface2: #243044;
  --text: #e7ecf3;
  --muted: #9aa8bc;
  --accent: #d97706;
  --accent2: #f59e0b;
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
          Open this file in any browser. Progress saves locally. Work in a real <code>dsp-sandbox</code> repo alongside the course.
          <strong>%%TOTAL%% exercises</strong> · scratch → expert · terminal-native Claude Code.
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
const STORAGE_KEY = 'claude-code-dsp-course-progress-v2';

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
        "title": "Claude Code Zero to Hero for Embedded DSP Engineers",
        "subtitle": "Terminal-Native · CLI-First · Headless CI · CLAUDE.md · Permissions · SSH/Docker/tmux · SDK",
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
