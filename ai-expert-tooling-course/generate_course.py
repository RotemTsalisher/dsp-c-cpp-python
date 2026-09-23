#!/usr/bin/env python3
"""Generate index.html — Advanced AI Use in Modern Hi-Tech Projects.
Part 1: Cursor. Part 2: Claude Code. Cross-cutting: mode/model routing, debugging protocol, capstone.
Audience: engineers who already USE Cursor and Claude Code but want to be experts."""
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
    # ─────────────────────────── PHASE 0 ───────────────────────────
    {
        "id": "00",
        "title": "What Expert-Level AI Use Actually Means",
        "level": "Setup",
        "summary": "The distinction between using AI tools and using them well. This course teaches judgment, not buttons.",
        "body": md("""
## The novice → expert gradient
- **Novice**: knows the buttons exist. Uses Chat and Agent interchangeably. Uses the same model for everything.
- **Intermediate**: knows Plan is different from Agent. Sometimes switches models. Occasionally writes rules.
- **Expert**: chooses mode, model, and tool DELIBERATELY per task. Has an explicit protocol for planning, execution, and debugging. Uses both Cursor and Claude Code as complementary — not as competing options.

This course is for engineers already sitting at "intermediate" who want to make the jump.

## What experts actually do differently
1. **They plan before they act.** Explicit plan artifacts, not "let me just start."
2. **They route by task.** A refactor gets one setup; a bug hunt gets another; a green-field feature gets a third.
3. **They budget thinking.** Extended reasoning for hard problems, cheap fast models for boilerplate — never one-size-fits-all.
4. **They treat rules as engineering artifacts.** `AGENTS.md` / `CLAUDE.md` / `.cursor/rules/` are code, versioned, reviewed, refined.
5. **They debug systematically.** Reproducer → hypothesis → verification loop, guided by AI but driven by them.
6. **They use both tools.** Cursor for IDE-native flow, Claude Code for terminal / headless / delegation. Not one or the other.

## Prerequisites (assumed knowledge)
- You have both Cursor and Claude Code installed and signed in
- You've written at least a few features with each
- You know what a PR, CI check, and merge conflict are
- You understand basic Git operations

If any of these are unfamiliar, complete `cursor-course/`, `claude-code-course/`, and `git-github-desktop-course/` first — then return.

## What this course is NOT
- Not "how to install Cursor" — see the beginner course
- Not "how to use `/plan`" mechanically — you already know that
- Not marketing pitches for either tool — both have real strengths and real weaknesses
- Not "AI will replace you" — this is about YOU using AI to be 10x

## The mental model this course builds
Every AI task in a hi-tech project has three axes:
```
     MODE  (plan / ask / agent / debug / edit / composer)
      ×
    MODEL  (thinking depth / speed / cost)
      ×
     TASK  (novel / routine / debug / refactor / research / integrate)
      ×
     TOOL  (Cursor / Claude Code / hybrid)
```
Expert = you can route any real-world task to the right combination in seconds, and can defend the choice.

## How to work through this course
- Don't skip Phase 0 (Module 01) — the mental model IS the course
- Phase 1 (Cursor) and Phase 2 (Claude Code) can be done in parallel or sequentially
- Phase 3 (cross-cutting) is where the two tools synthesize — do this LAST
- Do the capstone. It is where the routing becomes automatic.

## The single most important habit
**Before opening any AI tool, articulate: "This is a X task, I need Y depth of thinking, so I will use MODE M with MODEL N in TOOL T."**

At first, this feels slow. Within a week, it takes 2 seconds. Within a month, it's automatic. This one habit is 60% of what separates expert users from everyone else.
"""),
        "exercises": [
            ex(
                "00-1",
                "Score yourself honestly on the novice/intermediate/expert gradient for both Cursor and Claude Code. Write your scores and reasoning in `ai-expert-lab/self-assessment.md`. Revisit at the end of the course.",
                "Two dimensions per tool: mode/model discipline (do you switch deliberately?) and workflow discipline (planning/debugging protocol).",
                "Typical intermediate signals: 'I use Agent for most things, sometimes Plan.' 'I stick with one model.' 'I've written a rules file but rarely update it.' Expert signals: 'I have a routing protocol.' 'I switch models per phase.' 'My rules file is versioned and reviewed.' Honest baseline = accurate progress measurement.",
            ),
            ex(
                "00-2",
                "For each of these tasks, write which axis-combination you'd currently use (mode/model/tool). No looking things up yet — capture your gut choice:\n(a) Add a new REST endpoint to an existing Flask app\n(b) Debug a subtle race condition in a threading layer\n(c) Refactor a 400-line file into 5 smaller files without changing behavior\n(d) Write a design document for a new feature\n(e) Generate 20 golden test vectors from a MATLAB reference\n(f) Review a teammate's 800-line PR",
                "Just record instincts. We revisit in Module X-03 with the expert playbook.",
                "There are no wrong answers here — the point is a baseline to compare against. Expert answers vary: (a) Cursor Agent, mid model; (b) Plan mode / Ask mode with deep thinking; (c) Cursor Composer or Claude Code headless with a spec; (d) Ask mode, deep-thinking model; (e) Claude Code headless with a script; (f) Cursor Ask on the diff, or a Bugbot subagent.",
            ),
            ex(
                "00-3",
                "Create `ai-expert-lab/` as your working directory. Subfolders: `plans/`, `prompts/`, `rules/`, `verification/`, `capstone/`. This is where every exercise's artifacts land.",
                "Just directory scaffolding.",
                "Lab exists with structure. Every plan, prompt, rule, and verification script you write in this course goes into one of these folders. At the end, it's a reusable template for your future projects.",
            ),
        ],
    },
    {
        "id": "01",
        "title": "The Unified Mental Model: Mode × Model × Task × Tool",
        "level": "Setup",
        "summary": "One framework to route any AI task. This module is the spine of the course.",
        "body": md("""
## The four axes

### Axis 1: MODE
What the AI is allowed to do and how it responds.
- **Ask / Chat** — read-only reasoning. No file changes. Best for questions, analysis, design discussion.
- **Plan** — reasoning + proposed steps, no execution. Produces a plan artifact.
- **Agent / Auto** — execution with tool calls. Reads files, edits code, runs commands, iterates.
- **Debug** — execution scoped to reproducing/analyzing a bug (Cursor's debug workflows; CC's iterative test-fix).
- **Composer / Multi-file** — Cursor-specific: targeted edits across a chosen file set.
- **Inline / Tab / Edit** — precision edits at a specific location.

### Axis 2: MODEL
Depth of reasoning, speed, cost. All tools now offer tiers:
- **Fast / cheap** — Composer 2.5 fast, Haiku, Grok fast, GPT-5.6 fast. For boilerplate, small mechanical edits, syntax-only questions.
- **Balanced / mid** — Sonnet, GPT-5 medium, Opus medium. For most feature work, refactors, moderate debugging.
- **Deep-thinking / max** — Opus with thinking, GPT-5.6 with thinking-high, extended-thinking modes. For architectural decisions, hard debugging, novel design.

Cost scales roughly 10x from fast to deep-thinking. Speed scales 3-10x in the opposite direction. You are paying for reasoning depth.

### Axis 3: TASK
Not all tasks want the same setup. Common categories:
- **Novel feature** — no template exists in the codebase. Requires design.
- **Routine feature** — pattern exists (add endpoint, add form, add test). Mechanical.
- **Refactor** — behavior preserved, structure changed. Needs safety net.
- **Debug** — a specific broken thing. Needs reproducer, then hypothesis, then fix.
- **Research** — understanding an unfamiliar codebase, API, or algorithm.
- **Integration** — wiring two known things together. Mostly mechanical.
- **Review** — reading someone else's diff, PR, or design.

### Axis 4: TOOL
- **Cursor** — IDE-native. Best when you're actively coding, visual navigation, tab completion in flow, multi-file diffs you want to see.
- **Claude Code** — terminal-native. Best for headless / delegated / scripted / long-running / CI / SSH work.
- **Both** — many workflows use both (plan in one, execute in the other, review in the third).

## The routing algorithm (memorize this)
Given a task, ask in this order:
1. **What's the task type?** (novel / routine / refactor / debug / research / integration / review)
2. **Where's my body?** In an IDE session or a terminal? → biases tool choice
3. **How novel is this?** Novel → deep model. Routine → fast model.
4. **Do I have a plan yet?** No → Plan/Ask first. Yes → Agent/execution.
5. **What's the blast radius?** Small edit → Inline/Tab. Multiple files → Agent/Composer. Whole feature → Plan-then-Agent.
6. **Is there a known reproducer?** Debug: yes → Agent with test loop. No → Ask/Plan to design one.

Five seconds of routing before you start saves 30 minutes of AI wandering.

## The three failure modes of non-expert AI use
### Failure 1: One-mode habit
"I use Agent for everything." Result: agent produces sprawling edits for research questions; produces flimsy plans for novel work; wastes tokens.

### Failure 2: One-model habit
"I always use the best model." Result: 10x cost for tasks a fast model handles equally well; slow iteration.

### Failure 3: No planning discipline
"Just go." Result: agent goes down wrong path for 5 minutes; you interrupt; agent starts over; you burn context.

Every module in this course is a countermeasure to these three failures.

## The router card (print this)
```
TASK          → default MODE       → default MODEL     → default TOOL
─────────────────────────────────────────────────────────────────────
Novel feature → Plan → Agent      → Deep → Balanced   → Cursor
Routine feat. → Agent             → Fast/Balanced     → Cursor
Refactor      → Plan → Composer   → Balanced          → Cursor
Debug (repro) → Agent (test loop) → Balanced          → Either
Debug (no r.) → Ask → Plan        → Deep              → Cursor
Research      → Ask               → Balanced/Deep     → Either
Integration   → Agent             → Fast/Balanced     → Cursor
Review        → Ask on diff       → Balanced          → Cursor
Delegated     → Headless          → Balanced          → Claude Code
Bulk / batch  → Headless / SDK    → Fast/Balanced     → Claude Code
Long-running  → Cloud agent       → Balanced/Deep     → Cursor or CC
```
This is your starting default. Every module deepens one row.

## Why this framework beats "just try things"
- **Speed**: routing takes 5 seconds; wandering takes 5 minutes.
- **Cost**: right-sized model saves 10x-50x on token spend.
- **Quality**: the right mode makes the right output shape (plan artifact vs code diff vs analysis).
- **Habits**: your team can review and improve YOUR routing over time — it's explicit.
"""),
        "exercises": [
            ex(
                "01-1",
                "Copy the router card into `ai-expert-lab/router.md`. This is your reference card. Update it as you learn — expect the defaults to shift with your team's conventions.",
                "The card is the artifact. Personalize it.",
                "You have a physical reference. First week: consult it before every task. Week two: consult occasionally. Month one: internalized. Your version will diverge from the default as your work profile does.",
            ),
            ex(
                "01-2",
                "For your last 5 real AI-assisted tasks (personal or work), retrofit the axes: what task type was it, what mode did you use, what model, what tool? Would you route it differently now?",
                "This is calibration by hindsight.",
                "Common realization: 'I used Agent + big model for a routine task that would have been faster with a fast model in Inline mode.' Or: 'I skipped Plan on a novel feature and wasted 30 minutes.' Both are learning signals — write them down.",
            ),
            ex(
                "01-3",
                "Explain the routing algorithm to someone else (a colleague, or write a tutorial in `ai-expert-lab/router-explainer.md`). If you can teach it, you understand it.",
                "Teaching is the acid test.",
                "Your explanation is clear if it fits on one page. If it doesn't, you're still uncertain about the framework — reread the module and try again. Explicit routing is the foundation of everything downstream.",
            ),
            ex(
                "01-4",
                "For each of the three failure modes (one-mode habit, one-model habit, no planning), think of a specific instance from YOUR work in the last month. What did it cost you in time or tokens?",
                "Real numbers make the cost visceral.",
                "Common: 'I used Agent for a research question that Ask would have answered — cost 15 minutes and unnecessary file edits.' Or: 'I used Opus for boilerplate CRUD — cost me 3x what Sonnet would have.' Concrete costs = motivation to change.",
            ),
        ],
    },
    # ─────────────────────────── PHASE 1: CURSOR ───────────────────────────
    {
        "id": "C-01",
        "title": "Cursor's Mode Landscape (Ask / Plan / Agent / Composer / Tab / Inline)",
        "level": "Cursor Advanced",
        "summary": "Every mode Cursor offers, when each wins, and the common misuses that experts avoid.",
        "body": md("""
## The full mode inventory
Modern Cursor exposes (roughly, depending on version):
- **Ask / Chat** — question, get an answer, no file changes
- **Agent** — autonomous execution with tools; writes files, runs commands
- **Plan** — produces a step-by-step plan without execution
- **Composer** — multi-file surgical edits within a curated scope
- **Inline edit** (Cmd/Ctrl+K) — targeted edit at cursor position
- **Tab completion** — inline single-line suggestions
- **Cloud / Background agents** — long-running work off your machine

Names and shortcuts drift version-to-version. The CONCEPTS above are stable.

## When each wins (the expert map)
| Situation | Use | Not |
|-----------|-----|-----|
| "What does this function do?" | Ask | Agent |
| "Which files use this API?" | Ask | Agent (unless refactor follows) |
| "Add a rate limiter to this endpoint" | Agent | Ask |
| "Refactor the audio pipeline into 4 modules" | Plan → Composer/Agent | Direct Agent |
| "Fix this obvious typo" | Inline edit | Agent |
| "Rewrite this function to be async" | Inline edit → Composer if it spreads | Agent |
| "Generate the 20 endpoints from this spec" | Agent with a spec pinned | Ask |
| "Design the API for a new feature" | Ask + Plan | Agent |
| "Why is this test flaky?" | Ask (with logs pinned) → Plan → Agent | Direct Agent |
| "Rename a symbol across 40 files" | Composer (or LSP + Composer for verify) | Agent |
| "Batch: add copyright header to 200 files" | Cloud agent OR headless script | Chat |
| "Update all imports after a package rename" | Composer with focused scope | Agent (too broad) |

## Common expert-caught misuses
### Misuse 1: Agent for questions
Asking "how does X work?" with Agent selected — the agent starts editing while you just wanted to know. Waste and risk.

### Misuse 2: Ask for execution
"Now do it" in Ask mode — response is text describing what to do, but nothing happens. Round-trip friction.

### Misuse 3: Composer with a huge scope
Selecting 30 files and asking Composer to refactor — output is diffuse, hard to review, easy to break unrelated things. Scope Composer to 3-8 files max.

### Misuse 4: Agent when Plan would save you
Novel feature, no template, no plan — Agent goes down one path and you didn't authorize it. Plan first, THEN execute the plan.

### Misuse 5: Tab-driven design
Accepting tab completions on the shape of a new abstraction — Tab is optimizing local text, not designing. Design should happen in Ask/Plan.

## Mode-switching within one task
Expert flow for a real feature (e.g., "add server-side pagination"):
```
1. Ask: "How does pagination work today in this codebase?" (survey existing patterns)
2. Plan: "Draft a plan to add cursor-based pagination to /users endpoint"
3. Read and refine the plan (2-3 iterations)
4. Agent: execute the approved plan
5. Ask (on the diff): "Are there any edge cases we missed?" (review)
6. Inline edits: fix the 2-3 things review found
7. Agent: run the tests
8. Manual: open PR (or ask Agent to draft the PR description)
```
Notice: FIVE mode changes in one task. Each transition is deliberate.

## Session hygiene per mode
- **Ask** — context is your best friend. Pin relevant files. Reference symbols explicitly.
- **Plan** — output should be a written plan you can save. If you can't, the mode isn't paying off.
- **Agent** — bound scope EXPLICITLY. "Only touch files in `src/api/`". "Don't add dependencies." Otherwise Agent invents.
- **Composer** — curate the file list yourself. Don't let it auto-add.
- **Inline** — the smaller the selection, the better the edit. Whole-file edits belong in Composer.

## What experts don't do
- Don't leave Agent running unsupervised for > 5 minutes without checkpoints
- Don't use one mode for an entire session
- Don't accept edits without reading the diff (Cursor makes this easy — no excuse)
- Don't ignore the mode label in the UI — glance at it before every message

## Recovery: "Agent went sideways"
Signs: files being edited you didn't want, dependencies being added, tests being disabled.
Recovery:
1. Stop the agent (interrupt button)
2. Discard the changes (Git checkout or Cursor's revert)
3. Switch to Plan mode
4. Ask the model to write out what it was TRYING to do
5. Fix the plan, then re-run in Agent

Never let a bad Agent session propagate — it's a small cost to reset, a huge cost to unwind.
"""),
        "exercises": [
            ex(
                "C-01-1",
                "For today's next 3 real coding tasks, EXPLICITLY name the mode before starting. Say (aloud or in a note): 'This is task T, I will use mode M because R.' Do this for a day. Notice how the deliberation changes results.",
                "The habit is the whole point.",
                "You catch yourself defaulting to Agent for research questions, or opening Chat when you meant Plan. That awareness IS the growth. Within a week, the choice becomes preconscious.",
            ),
            ex(
                "C-01-2",
                "Take a real recent task where you used Agent and it went sideways. Retrospectively: what should the sequence have been? Write it out in `ai-expert-lab/mode-audit.md` as a small case study.",
                "One good case study beats abstract advice.",
                "Typical audit: 'Started with Agent → wandered → interrupted → discarded → started with Plan → clean execution.' Reading these back a month later teaches you your OWN patterns.",
            ),
            ex(
                "C-01-3",
                "Pick a moderately complex feature (real or invented). Execute it deliberately through 5 mode transitions (Ask → Plan → Agent → Ask on diff → Inline fixes). Time the whole thing.",
                "Feel the rhythm of multi-mode work.",
                "Total time similar to your usual single-mode approach, but the OUTPUT is cleaner (plan artifact + focused agent run + fewer regressions). The overhead of switching is real but small; the quality gain is large.",
            ),
            ex(
                "C-01-4",
                "Write in `ai-expert-lab/cursor-anti-patterns.md`: your top 3 mode-misuses you tend to commit, and the concrete cue that should trigger you to switch. Example: 'When I type \"how does...\" — that's an Ask cue, not Agent.'",
                "Cues that live in your body beat abstract rules.",
                "The cue-response pairing is a habit-formation technique. Write specific ones. Reread the file weekly for a month. The cues become automatic.",
            ),
        ],
    },
    {
        "id": "C-02",
        "title": "Model Selection in Cursor",
        "level": "Cursor Advanced",
        "summary": "Not all models are equal at all tasks. Pick per phase, not per session.",
        "body": md("""
## The model tiers (conceptual, not brand-specific)
### Fast tier
- Cursor: `composer-2.5-fast`, `grok-4.7-fast`, `gpt-5.6-fast`
- Character: <1s latency, cheap, good at boilerplate, syntax, template code
- Weakness: shallow reasoning, breaks on novel or ambiguous problems

### Balanced tier
- Cursor: `claude-sonnet-4.x`, `gpt-5-medium`, `cursor-grok-4.6-medium`
- Character: 2-5s latency, moderate cost, handles most real coding
- Weakness: not great at architectural decisions or hard debugging

### Deep-thinking tier
- Cursor: `claude-opus-4.7-high-thinking`, `claude-opus-5-thinking-xhigh`, `gpt-5.6-thinking-high`
- Character: 10-30s+ latency, expensive, excellent reasoning
- Weakness: overkill for routine tasks; slow feedback loop

The tiers are FUNCTIONAL not marketing. A "fast" model from any vendor is roughly comparable to another vendor's fast tier for daily coding work.

## The per-phase model discipline
Expert flow uses DIFFERENT models within a single task:
```
Planning phase:    Deep-thinking model  (few messages, high stakes)
Execution phase:   Balanced model       (many messages, moderate stakes)
Boilerplate:       Fast model           (many small edits, low stakes)
Review / debug:    Balanced or Deep     (few but critical messages)
```
Switching mid-task via the model dropdown is free and takes 2 seconds. Do it.

## The economics
Rough cost ratio (as of 2026, order of magnitude):
- Fast: 1x
- Balanced: 3-5x
- Deep-thinking: 10-30x

An 8-hour session using deep-thinking for everything can cost 20-40x more than the same session with expert routing. Same output quality — usually better with routing, because deep models overthink easy problems.

## When "just use the best" fails
- **Boilerplate**: deep model wanders, adds features you didn't ask for, "improves" your patterns
- **Fast iteration**: 20s latency × 30 iterations = 10 minutes of thumb-twiddling
- **Simple debugging**: deep model spawns hypotheses for scenarios that aren't the bug
- **Cost sensitivity**: if you're on a metered plan, cost per session matters

## When "just use the cheapest" fails
- **Novel design**: fast models produce plausible-looking wrong architecture
- **Hard debugging**: fast models can't hold enough context to reason about state machines, race conditions, memory
- **Anything with subtle correctness**: numerics, concurrency, security — pay for depth

## The Auto option
Cursor's `Auto` model picker chooses per message. Good defaults for most work, but:
- Not optimal for CRITICAL decisions (upgrade to Deep manually)
- Can surprise you with model changes mid-task
- Fine for the majority of work; explicit picks for the rest

Expert usage: Auto by default, explicit deep-model pins for planning and hard debugging.

## Thinking budgets
Deep-thinking models expose a thinking budget:
- `high` — long thinking, best reasoning, slow
- `medium` — moderate thinking, balanced
- `low` — brief thinking, faster but weaker

For genuinely hard problems, `high` is worth the wait. For a plan draft you'll iterate on, `medium` is often enough — you're going to refine anyway.

## Cost telemetry
- Cursor shows per-session token usage (Settings → Usage or the status bar)
- Watch it for a week. Learn what your typical session costs.
- If cost spikes 5x, ask: was the task 5x harder, or did you accidentally leave deep-thinking on?

## The team dimension
- Teams should agree on defaults (which model, when to escalate)
- Add to `AGENTS.md` or `.cursor/rules/`: "Use `claude-sonnet-4.x` unless the task requires deep reasoning."
- Track team-level cost, share learnings

## The single most useful model habit
**When switching to Plan or Debug modes, PROACTIVELY check the model dropdown and set it to a deep-thinking tier.**

Planning and debugging are the two phases where model quality has the biggest ROI. Never leave them on Fast by accident.
"""),
        "exercises": [
            ex(
                "C-02-1",
                "Look at your Cursor Usage tab (Settings → Usage or wherever your version exposes it). Note your model usage over the last week. What percentage was Fast / Balanced / Deep? Does it match the phase-by-task discipline?",
                "Data > intuition.",
                "Common realization: 'I'm 90% on one balanced model regardless of phase.' Expert distribution varies (60% balanced, 20% fast, 20% deep is not unusual). Yours will differ by role — but if it's flat across tasks, you're not routing.",
            ),
            ex(
                "C-02-2",
                "Run the same non-trivial task (e.g., 'refactor this 200-line file into 3 files with tests') three times: once with Fast, once with Balanced, once with Deep. Compare: quality of output, time to first useful diff, how many iterations to acceptable.",
                "Direct A/B/C evidence for your work.",
                "Typical: Fast produces syntactically OK but sloppy factoring; Balanced produces good factoring with 1-2 iteration; Deep produces excellent factoring in 1 shot but takes 3-4x the wall-clock. Your judgment now has concrete data behind it.",
            ),
            ex(
                "C-02-3",
                "Write in `ai-expert-lab/model-defaults.md`: for each phase (planning / execution / boilerplate / debugging / review), which model do YOU default to? Which is your escalation model when the default fails?",
                "Your personal routing card.",
                "Sample: 'Planning: Opus high-thinking. Execution: Sonnet. Boilerplate: Composer fast. Debugging: Opus medium, escalate to high. Review: Sonnet on diff.' Personal defaults you can defend > following someone else's blindly.",
            ),
            ex(
                "C-02-4",
                "For your next planning session, pin the deep-thinking model EXPLICITLY. Notice: how does the plan quality differ from your usual planning?",
                "Feel the ROI of paying for depth where it matters.",
                "Typical difference: deep-thinking plans anticipate more edge cases, suggest alternatives you didn't think of, and identify hidden risks. Costs a few dollars more per plan. Pays back in reduced execution debt.",
            ),
        ],
    },
    {
        "id": "C-03",
        "title": "Planning Discipline with Plan Mode",
        "level": "Cursor Advanced",
        "summary": "How to write plan prompts that produce actionable, executable plans — not vague summaries.",
        "body": md("""
## Why explicit planning
"Just start" works for tasks you've done 20 times. Everything else deserves 5-10 minutes of planning that saves 30-60 minutes of execution debt.

Novel work without planning:
- Agent picks a path (may not be the right one)
- You interrupt at 5 minutes with "wait, actually..."
- Agent restarts with partial context, loses coherence
- Iteration count doubles, quality drops

Planning first:
- You articulate WHAT and WHY before HOW
- Model catches things you didn't consider
- Plan becomes the spec that agent executes cleanly
- Fewer mid-flight corrections

## Anatomy of a good plan prompt
```
[Context]
We have a Flask app at repo root. Currently /users returns all users
in one JSON response. Some tenants have >100k users. Response times
are 5-15s and memory usage spikes.

[Goal]
Add cursor-based pagination to /users. Default page size 50, max 500.
Backward compatible: existing clients without cursor params get the
first page (with new pagination metadata).

[Constraints]
- No new dependencies (we use SQLAlchemy + Flask, keep it there)
- Response schema addition only, no removal
- Must include a migration for a new opaque cursor column if needed
- Deprecate the old behavior only via a header, not by breaking

[What to plan]
1. Identify all files that need changes
2. Design the cursor encoding (opaque, stable, no PII)
3. List the tests needed (unit + integration)
4. Note any risks or open questions
5. Estimate effort

[What NOT to do in this pass]
- Do not write any code yet
- Do not modify any files
- Do not run any commands
```

## What a good plan output looks like
Structured, actionable, and NOT code:
```
## Files to touch (7)
1. src/api/users.py            (endpoint changes)
2. src/models/user.py          (add cursor index)
3. src/pagination.py           (NEW: cursor encoder/decoder)
4. tests/api/test_users.py     (extended)
5. tests/pagination_test.py    (NEW)
6. migrations/20260923_...     (NEW)
7. docs/api-changelog.md       (append)

## Cursor design
- Opaque base64 of (last_id, timestamp) — 24 bytes
- Stable across app restarts (no random seed)
- Not tied to any specific user (no PII)

## Test plan
- Unit: cursor encode/decode roundtrip, edge cases (empty, one item, exact page)
- Integration: pagination through 3 pages, forward-only, invalid cursor rejected
- Regression: existing /users?limit= behavior unchanged

## Risks
- Cursor tied to primary key ordering — if we ever migrate to UUIDs, cursor breaks
- Not clear if downstream clients handle 'next_cursor: null' correctly — check
- Migration on large tables (>1M rows) may lock for minutes

## Open questions
- Should we support backward pagination? (Assume no for v1)
- What happens if the "cursor" row is deleted between requests? (Skip forward gracefully)

## Estimated effort
- Design + review: 30 min
- Implementation: 2-3 hours
- Tests: 1-2 hours
- Docs + deploy: 30 min
```
This is what you approve, refine, and then hand to Agent.

## The three-pass plan
Real expert flow:
1. **First pass**: quick plan with balanced model, ~2 min. Read it. Note what's wrong or missing.
2. **Second pass**: refine with concrete corrections. "Add step for backward compat testing. Cursor should not include timestamps — makes it non-idempotent."
3. **Third pass** (optional): with deep-thinking model on the refined plan, ask: "What could go wrong? What are we missing?"

By pass 3, the plan is battle-tested. Execution is boring — the way it should be.

## When Plan mode isn't Plan mode
Some Cursor versions have `Plan` as a distinct mode; others use Ask with an explicit "plan this" instruction. Both work. The DISCIPLINE matters more than the mode label:
- Explicit request for a plan artifact
- No file changes
- Structured output (files, steps, risks)
- Iterated to convergence

If your version doesn't have a Plan mode, use Ask mode with this system-level prompt as part of your rules:
```
When asked to plan, produce a structured plan with:
- Files to touch (with reason)
- Steps in order
- Tests to add
- Risks and open questions
- Estimated effort
Do NOT modify any files. Do NOT execute anything.
```

## Common planning failures
### Failure: Plan is too vague
"Add pagination to /users." Result: agent has to make 20 decisions the plan didn't cover. Fix: constraints and specifics in the prompt.

### Failure: Plan is too detailed
Down to variable names. Result: brittle, hard to iterate. Fix: plan the SHAPE, let execution pick the details.

### Failure: Plan is one-shot
No iteration. Result: first plan is usually wrong in some way. Fix: three-pass discipline.

### Failure: Plan doesn't survive execution
Agent deviates, plan becomes irrelevant. Fix: pin the plan as context, remind agent "follow the plan; deviations must be flagged."

## The plan-to-execution handoff
When you switch from Plan to Agent:
1. Save the plan as a markdown file in the repo (e.g., `docs/plans/pagination.md`) or paste it into a chat message pinned to the session
2. Switch to Agent
3. First Agent message: "Execute the plan at `docs/plans/pagination.md`. Follow it step by step. If you need to deviate, stop and ask."
4. Agent executes with a clear scope
5. If plan needed adjustment, update the plan file (not just the code)

Plans that live only in chat history evaporate. Plans as artifacts persist and can be reviewed.
"""),
        "exercises": [
            ex(
                "C-03-1",
                "Pick a real upcoming feature. Write a plan prompt using the anatomy from the module. Run it in Plan (or Ask) mode with a deep-thinking model. Save the output as `ai-expert-lab/plans/<feature>.md`.",
                "One real plan is worth 10 abstract discussions.",
                "You have a concrete plan artifact. Notice: writing the PROMPT well takes 5-10 minutes. That is time you didn't waste later on execution correction. Real experts iterate on prompts before iterating on outputs.",
            ),
            ex(
                "C-03-2",
                "Run the three-pass planning discipline: pass 1 draft, pass 2 refine, pass 3 stress-test with deep-thinking. Compare pass 1 to pass 3. What was missed initially?",
                "See the value of iteration.",
                "Typical: pass 1 misses edge cases (backward compat, migration cost, error handling). Pass 3 has these. Deep-thinking on pass 3 sometimes surfaces architectural concerns you'd only hit in code review — expensive to fix late.",
            ),
            ex(
                "C-03-3",
                "Take a plan you wrote and hand it to Agent with: 'Execute this plan. If you need to deviate, stop and ask.' Observe: does Agent respect the constraints? Does it deviate? When it deviates, how does it flag?",
                "Test the plan-to-execution handoff.",
                "Well-planned Agent runs deviate rarely and always ask first. Poorly-planned runs deviate silently. Your plan quality directly correlates with agent obedience. If Agent keeps deviating, the plan is under-specified.",
            ),
            ex(
                "C-03-4",
                "Write in `ai-expert-lab/plan-template.md`: your team's or personal template for planning prompts. Reuse it. Refine it as you learn what your specific work needs.",
                "Templates compound.",
                "After 10 uses, your template is battle-tested. New team members can adopt it directly. Plans have consistent shape, so reviews are faster. This is how discipline becomes culture.",
            ),
        ],
    },
    {
        "id": "C-04",
        "title": "Ask Mode as a Scoped Reasoning Tool",
        "level": "Cursor Advanced",
        "summary": "Ask is not 'lite Agent'. It's the mode for questions, analysis, and design — the read-only counterpart to execution.",
        "body": md("""
## What Ask is really for
- Understanding existing code ("what does this function do?")
- Analyzing behavior ("why might this be slow?")
- Comparing options ("A vs B vs C — trade-offs?")
- Reading and summarizing (docs, logs, PRs, diffs)
- Designing (before Plan mode formalizes it)
- Reviewing (someone else's PR, your own diff)

What Ask is NOT for:
- Executing changes (use Agent)
- Producing structured plans you'll execute (use Plan)
- Iterating on code (use Inline / Composer)

## Ask's superpower: no side effects
- No files change
- No commands run
- You can experiment with framing without cost
- You can pin arbitrary context (docs, logs, code) and reason over it

This makes Ask the safest mode for exploration. When in doubt, START in Ask.

## Ask + context = expert leverage
The value of Ask scales with context quality:
- Ask with no context: generic answer, may not fit your codebase
- Ask with 1 file pinned: reasonable answer
- Ask with 5 relevant files + a paragraph of situation: excellent, specific answer

Cursor's context tools (pinning files, referencing symbols with `@`, adding docs) are Ask's amplifiers. Use them.

## Ask on a diff (review workflow)
```
[Context: pin the diff or paste PR description]
Review this diff for:
- Correctness bugs
- Missing edge cases
- Test coverage gaps
- Any behavior regressions vs the previous version
- Security concerns

Be specific. Reference file:line for each finding.
```
Fast, systematic, catches things a human reviewer misses.

## Ask on logs (debugging workflow, phase 1)
```
[Context: paste the failing log or error]
Given this log, what are the top 3 hypotheses for the root cause?
For each, tell me:
- What evidence in the log supports it
- What additional evidence would confirm or refute it
- What is the cheapest way to test it
```
Ask produces hypotheses. You verify. Then move to Plan/Agent to fix.

## Ask on unfamiliar code (research workflow)
```
[Context: pin the module you're new to]
Summarize this module in three levels:
1. One sentence — what does it do?
2. One paragraph — what are its main concerns and boundaries?
3. One page — walk through the key data flow

Then list: (a) most surprising design choice, (b) most fragile code path, (c) most likely place to add my new feature X.
```
30 minutes of Ask beats 3 hours of manual code archaeology.

## Ask vs Plan (the subtle distinction)
- **Ask** — asks a question, expects an answer. Output shape: free-form text.
- **Plan** — asks for a plan, expects a plan artifact. Output shape: structured steps.

Ask is for questions. Plan is for "what am I going to do." Use both — often Ask first (understand), then Plan (decide), then Agent (execute).

## Ask discipline
- **Ask FOCUSED questions**. "Why is this slow?" > "Analyze this file." (Focus produces useful answers.)
- **Pin context deliberately.** Vague context = vague answer.
- **Iterate.** First answer is a starting point. Refine with follow-up questions.
- **Save the good outputs.** If Ask produced a great analysis, paste it into a doc — future you or your team benefits.

## When to escalate from Ask to Plan/Agent
- Ask produced a design → Plan formalizes it
- Ask produced hypotheses → Agent tests them
- Ask produced review findings → Inline/Agent fixes them

Never let Ask output evaporate. Every good Ask response has a next step.

## Common Ask misuses
### Misuse: Using Ask for execution
"Now do it." Response: text. Nothing happens. Round-trip friction.
Fix: notice the mode label. Switch to Agent BEFORE typing "do it."

### Misuse: Ask with no context
"How should I structure a Flask API?" — generic answer, useless.
Fix: pin your existing Flask code, then ask "Given how we structure things, how should I add X?"

### Misuse: One-shot Ask
Getting one answer and moving on.
Fix: 3-5 turn conversations. First answer is a hypothesis; iterate.

### Misuse: Ask where Google would have been faster
"What's the Python syntax for X?" — Google. Save AI cycles for judgment.
"""),
        "exercises": [
            ex(
                "C-04-1",
                "For your next code review, use Ask mode with the diff pinned and the review prompt from the module. Compare findings to what you'd catch manually.",
                "AI-assisted review, systematic.",
                "Typical: AI catches 3-5 things you'd miss (edge cases, missing null checks, subtle API misuse). Human catches 1-2 things AI misses (project-specific conventions, intent mismatches). Both together > either alone.",
            ),
            ex(
                "C-04-2",
                "For an unfamiliar module in a real codebase (yours or open source), run the three-level summary prompt from the module. Save output to `ai-expert-lab/research/<module>.md`.",
                "Research workflow in action.",
                "You now have a research artifact you can share with teammates or refer back to. 30 minutes of guided reading via Ask compresses many hours of manual archaeology.",
            ),
            ex(
                "C-04-3",
                "Practice the Ask → Plan → Agent chain on a real feature. Notice the transitions: at what point did Ask outputs stop being useful and Plan needed to take over?",
                "Feel the boundaries between modes.",
                "Transition is usually when 'what' and 'why' are settled and you need to decide 'how in what order.' At that moment, save the Ask conversation as context, switch to Plan, hand off the understanding.",
            ),
            ex(
                "C-04-4",
                "Write in `ai-expert-lab/ask-prompts.md`: 3-5 reusable Ask prompts for your common tasks (code review, debugging, research, design comparison). Iterate on these — they're the templates you'll reuse for years.",
                "Prompt templates compound value.",
                "Templates capture your best framings. After 10 uses, they're refined. Share with team; adopt team's. This is how prompt engineering becomes an engineering discipline, not folklore.",
            ),
        ],
    },
    {
        "id": "C-05",
        "title": "Agent Mode — Controlled Methodical Execution",
        "level": "Cursor Advanced",
        "summary": "Agent is powerful and dangerous. Experts bound scope, checkpoint often, and recover fast.",
        "body": md("""
## The Agent value prop
Agent takes a specification and executes: reads code, writes code, runs tests, iterates. When it works, it's magic. When it drifts, it's expensive.

The expert's job: make it work consistently.

## The five pillars of controlled Agent use
1. **Explicit scope** — what files, what boundaries
2. **Explicit context** — what the agent knows about the codebase and task
3. **Checkpoints** — commit or note progress at meaningful stages
4. **Interrupts** — stop when Agent drifts; don't hope it self-corrects
5. **Recovery** — reset cleanly if a run goes bad

## Explicit scope in the prompt
Bad: "Fix the pagination bug."
Better: "In `src/api/users.py` only, fix the off-by-one at line 42 that returns page N+1 items instead of N. Do not touch other files. Do not add dependencies. Do not change the schema."

Explicit scope is a contract. Agent tries to respect it; when it can't, it tells you (well-tuned agents will).

## Explicit context
Agent's implicit context is the currently-open files and any files in the recent chat. Explicit context is:
- Pinned files (`@` mentions)
- Referenced symbols
- Documentation pointers
- The plan (if one exists)

Rule: if a piece of information is NECESSARY to do the task correctly, PIN it explicitly. Don't rely on Agent to auto-discover.

## Checkpointing
Long agent runs without checkpoints are dangerous. Every 5-10 minutes or every meaningful step, do one of:
- Commit locally (`git commit -m "checkpoint: WIP"`)
- Have Agent write a status note to a file
- Manually save the current state elsewhere

If Agent later drifts, you can `git reset` back to the last checkpoint without losing all progress.

## Interrupts — the underused feature
When you notice Agent going down a wrong path:
1. **INTERRUPT immediately** (the stop button, or Esc)
2. Don't hope it self-corrects — it usually won't
3. Read what it was trying to do
4. Adjust the prompt or plan
5. Restart with clearer scope

The cost of interrupting is small. The cost of letting a wrong path run for another 10 minutes is huge.

Common signs to interrupt:
- Agent is editing files you didn't authorize
- Agent is adding dependencies you didn't approve
- Agent is disabling tests to "make them pass"
- Agent is invoking things in an infinite loop
- Agent output doesn't reference the pinned context

## Recovery protocol
When Agent goes badly sideways:
```
1. Interrupt
2. git status — what's dirty?
3. git diff — is any of it worth keeping?
4. git stash (if partially useful) OR git checkout . (if all garbage)
5. Switch to Plan/Ask mode
6. Diagnose: what did Agent misunderstand?
7. Refine the prompt or plan
8. New Agent session with cleaner scope
```
Never continue a bad Agent session by adding more instructions. Reset and restart.

## Auto-approve boundaries
Cursor lets you set auto-approve for certain tool calls (read files, run tests, etc.). Expert settings:
- Auto-approve READS (any file access)
- Auto-approve tests (running the test suite)
- MANUAL approve for: writes, deletes, running arbitrary shell, network calls
- MANUAL approve for: adding dependencies, modifying CI config

Adjust per project. High-trust internal repos: more auto. External or high-stakes: manual for anything with side effects.

## Todo lists and progress
Cursor's Agent supports internal todos. Well-tuned agents on complex tasks will:
- Break the task into steps
- Show current step
- Update as done/failed
- Allow you to see progress at a glance

Encourage this in your prompt: "Break this into steps. Show progress. Only start step N+1 when N is verified."

## The multi-turn Agent conversation
Agent runs aren't one-shot. Real workflow:
- Turn 1: Agent executes, produces initial diff
- You review the diff
- Turn 2: "Looks good but tests are missing for edge case X — add them"
- Agent adds tests
- Turn 3: "Test T is redundant with existing test U — merge them"
- Agent merges
- Turn 4: "Done. Draft the PR description."

Each turn is small, focused, verifiable. Long autonomous runs feel efficient but produce diffs you can't verify.

## When Agent shines
- Well-specified refactors within a bounded scope
- Test authoring from a spec
- Migration tasks (rename symbol, upgrade API usage)
- Multi-file edits following a pattern
- Boilerplate expansion from a template

## When Agent struggles
- Novel design (better in Plan first)
- Debugging without a reproducer (Ask first, then Agent with the reproducer)
- Anything requiring outside-the-repo knowledge (paste it in)
- Anything where "correctness" is subjective or subtle (numerics, concurrency, security-critical)
"""),
        "exercises": [
            ex(
                "C-05-1",
                "Take your next 3 Agent tasks. For each, WRITE the scope explicitly in the prompt before starting: files, boundaries, non-goals. Compare drift rate to your usual approach.",
                "Explicit scope = fewer surprises.",
                "Explicit-scope runs deviate less. When they do, they flag it (well-tuned agents ask permission to expand scope). Drift-free runs are shorter, cleaner, faster to review.",
            ),
            ex(
                "C-05-2",
                "Practice interrupts. Deliberately let an Agent run go 2-3 minutes past when you'd normally interrupt. Notice the mess. Then rerun with clean interrupt discipline. Compare outcomes.",
                "Feel the cost of NOT interrupting.",
                "Delayed-interrupt runs typically require full reset. Timely-interrupt runs recover with a 30-second prompt refinement. This is a habit-formation exercise — the pain teaches faster than the theory.",
            ),
            ex(
                "C-05-3",
                "For a real complex task, use checkpointing: after each meaningful sub-step, commit locally with a descriptive message. If it goes wrong, `git reset --hard <checkpoint>`. Feel the safety.",
                "Checkpoints turn irrecoverable messes into 5-minute setbacks.",
                "Once you experience recovery via checkpoint, you'll never do long Agent runs without them. The cost is negligible; the safety is huge.",
            ),
            ex(
                "C-05-4",
                "Write in `ai-expert-lab/agent-scope-template.md`: your standard Agent prompt template with scope/context/non-goals slots. Reuse for every non-trivial Agent invocation.",
                "Reusable scaffolds > ad-hoc prompts.",
                "Sample template:\n```\n[Scope] Files: X, Y. Do not touch anything else.\n[Context] The plan is at plans/foo.md. The tests to keep green: test_a, test_b.\n[Non-goals] No new dependencies. No schema changes. No touching CI config.\n[Task] <specific instruction>\n```\nFill the slots each time. Consistency compounds.",
            ),
        ],
    },
    {
        "id": "C-06",
        "title": "Rules, AGENTS.md, and Repo Memory as Engineering",
        "level": "Cursor Advanced",
        "summary": "Rules that actually work are engineering artifacts: versioned, reviewed, refined. Most rules files are neglected — yours won't be.",
        "body": md("""
## The rules hierarchy in Cursor
- **User rules** (global) — your personal preferences (style, tone)
- **`.cursor/rules/*.mdc`** (project) — versioned in the repo, applies to all users
- **`AGENTS.md`** (project) — human-readable spec for AI agents, versioned
- **Inline conventions** — per-file comments, docstrings AI reads for context

Precedence: project rules > user rules > model defaults.

## What belongs in rules (and what doesn't)
### Belongs
- Coding conventions specific to the project ("use snake_case for filenames")
- Framework-specific do's and don'ts ("no async in this thread-only codebase")
- Testing conventions ("every new function needs a pytest test")
- Non-obvious constraints ("do not use library X, we have our own wrapper")
- Preferred file/module organization
- Team-specific commit message and PR conventions

### Doesn't belong
- General programming advice ("write clean code")
- Restatements of things AI already knows well
- Bloat that dilutes the important signal
- Personal preferences that vary among team members (put in user rules instead)

## The rules quality test
For each rule, ask: "If this rule wasn't here, would AI make a mistake?" If yes, keep it. If no, delete it. Signal beats volume.

## AGENTS.md — the human-first spec
`AGENTS.md` is markdown, in the repo root, versioned. It describes the project TO an agent (or a new engineer). Structure:
```
# Project X

## What this is
One paragraph.

## Key concepts
- Term A: definition
- Term B: definition

## Repository layout
src/... — description
tests/... — description
scripts/... — description

## Coding conventions
- Style
- Testing
- Commit messages

## Non-obvious constraints
- Don't do X because Y
- Prefer A over B for reason C

## How to run
`make dev` — starts dev server
`make test` — runs tests
`make lint` — runs linter

## When adding a feature
1. Update this file if you add a new concept
2. Write tests first
3. Follow the plan-then-execute discipline
```

AGENTS.md serves TWO audiences: humans new to the repo, and AI agents. Both benefit from the same clarity.

## `.cursor/rules/*.mdc` — the enforcement layer
Rules files support metadata:
```mdc
---
description: Testing conventions for the API layer
globs:
  - "src/api/**"
  - "tests/api/**"
alwaysApply: true
---

# API testing rules

- Every new endpoint MUST have a pytest test
- Use `client` fixture, not raw requests
- Assert response status AND body shape
- Test 200, 4xx, and one 5xx case at minimum
```
The globs mean this rule loads when Agent touches those paths. Scoped rules > global rules — less noise, more signal.

## Rules refinement as a discipline
Rules aren't write-once. Every time Agent makes the same mistake twice:
1. Add a rule to prevent it
2. Test that the rule works (re-run the task, verify the mistake is avoided)
3. Commit the rule with a message: "Prevent [mistake]"

Over 3-6 months, your rules become highly tuned to your project. This IS your team's institutional knowledge for agents.

## Team-shared vs personal
- `.cursor/rules/` and `AGENTS.md` — versioned, team-shared. Change via PR.
- User rules (Settings) — personal. Style preferences ("I like verbose docstrings").
- Do NOT put personal preferences in team-shared rules. Frustration guaranteed.

## The rules audit
Once a quarter, audit rules:
- Which rules did Agent violate anyway? (Reword, or split into more specific rules.)
- Which rules haven't been triggered in 3 months? (Consider deleting — not relevant.)
- Which rules contradict each other? (Reconcile.)
- Which repeated mistakes have NO rule yet? (Add rules.)

Rules rot. Audit prevents it.

## Rules examples from real projects
### Good rule (specific, actionable)
```
When adding a new REST endpoint:
1. Add the route in `src/api/routes.py`
2. Add a handler in `src/api/handlers/<name>.py`
3. Add a pytest test in `tests/api/test_<name>.py`
4. Update `docs/api-changelog.md` with a bullet under Unreleased
```

### Bad rule (vague, unenforceable)
```
Write clean, maintainable code.
```

### Good rule (constraint)
```
DO NOT install new npm packages. If you need a new dependency, stop and
ask before adding. We have strict security review for new packages.
```

### Bad rule (uncontextualized)
```
Follow best practices.
```

## The meta-rule: keep rules TIGHT
- Aim for 20-100 lines of rules for a typical project. Not 500.
- Each rule earns its keep by preventing real mistakes.
- Prune ruthlessly. Bloated rules files get ignored by the model AND by humans.
"""),
        "exercises": [
            ex(
                "C-06-1",
                "Audit your current `.cursor/rules/` or `AGENTS.md` (or check a project's if you have one). For each rule, apply the quality test: 'Would AI make a mistake without this?' Delete rules that fail. Note what percentage survived.",
                "Signal beats volume.",
                "Typical: 30-60% of rules in a mature file survive rigorous audit. The rest are aspirational, generic, or stale. Pruning improves BOTH model behavior and human onboarding.",
            ),
            ex(
                "C-06-2",
                "For a repo you own (or your `ai-expert-lab/`), write a proper `AGENTS.md` using the template. 20-50 lines. Test it: start a new Cursor session in the repo, ask the model to describe the project. Does it match your intent?",
                "AGENTS.md test = model's summary matches your intent.",
                "Mismatch = rewrite. Match = AGENTS.md is doing its job. This is the fastest feedback loop for rules quality.",
            ),
            ex(
                "C-06-3",
                "Set up scoped rules: create `.cursor/rules/testing.mdc` with globs for your test directory only. Verify the rule loads when Agent touches test files but not when it touches source files.",
                "Scoped rules = less noise.",
                "You'll notice: model behavior changes based on which files it's editing. Testing rules apply only during testing work. This is how large repos with diverse patterns stay coherent — scoped rules per module.",
            ),
            ex(
                "C-06-4",
                "For your team (or personal work), draft a rules refinement policy in `ai-expert-lab/rules-policy.md`. Who can add rules? How are they reviewed? How often are they audited? Even solo, having a policy prevents rules rot.",
                "Governance for the rules file.",
                "Sample: 'Anyone can propose a rule via PR. Rules require 1 approval. Every rule cites the mistake it prevents. Quarterly audit removes stale rules. Rules over 100 lines total require a case for necessity.' Discipline scales.",
            ),
        ],
    },
    {
        "id": "C-07",
        "title": "Cloud Agents & Parallel Work",
        "level": "Cursor Advanced",
        "summary": "Delegating long-running or independent work to background agents. Worktree strategy. When parallelism actually helps.",
        "body": md("""
## What cloud / background agents are
Long-running Cursor agents that:
- Execute off your local machine (in Cursor's cloud infrastructure)
- Persist across your work sessions
- Can be triggered from anywhere (desktop, mobile, CLI)
- Report results asynchronously
- Handle tasks that would tie up your local session

Sometimes called Bugbot, Cloud Agents, or Background Agents depending on version.

## When cloud agents shine
- **Long refactors** — "rename symbol X across 500 files, ensure tests pass"
- **Bulk operations** — "add copyright header to all `.py` files in `src/`"
- **CI-style tasks** — "run the full slow test suite and summarize failures"
- **Reviews** — "review PR #234 and post detailed comments"
- **Investigations** — "trace why test X is flaky, produce a report"
- **Chore batches** — "update all deps to latest minor versions"

If it would take >20 minutes of your local attention, consider delegating.

## Parallelism is not just cloud
Local parallelism via git worktrees:
```bash
git worktree add ../myrepo-feature-a feature-a-branch
git worktree add ../myrepo-feature-b feature-b-branch
```
Now you have TWO working directories from ONE repo, on different branches. Open both in Cursor. Work on both in parallel — one Cursor window per worktree.

Use case: while agent A is working on feature X in one worktree, you're actively coding feature Y in another. No branch switching, no state confusion.

## When parallelism helps vs hurts
### Helps
- Independent tasks (unrelated features, orthogonal refactors)
- One long-running task blocking otherwise idle time (delegate, do other work)
- Investigation runs that can go in background while you code
- Batch operations that fan out cleanly

### Hurts
- Tightly-coupled work (parallel agents step on each other)
- Complex tasks that need frequent oversight
- When context-switching cost > parallel gain
- Bug hunts (deep single-thread focus usually wins)

## The parallelism ratio
An expert typically has:
- 1 primary Cursor session (their active work)
- 0-2 parallel local worktree sessions (independent features)
- 0-3 cloud/background agents (delegated tasks)

Beyond this, cognitive overhead kills productivity. You spend more time managing agents than coding.

## Delegating well
Cloud agents need CLEARER specs than interactive ones — you're not there to correct mid-flight.

Good delegation prompt:
```
[Task]
Rename all instances of the class `LegacyProcessor` to `Processor` across the codebase.
Update: class definitions, imports, docstrings, comments, tests, docs.

[Constraints]
- Only in the `src/` and `tests/` directories
- Do not touch `docs/legacy/` (those refer to the old name intentionally)
- Ensure `pytest` passes after the rename
- If tests fail, report the failure — do not disable tests

[Deliverable]
- One PR with the rename
- PR description lists any test failures or edge cases encountered

[Verification]
Before submitting, run: pytest, mypy, ruff. All must pass.
```

Bad delegation prompt:
```
Clean up the LegacyProcessor stuff.
```
Interactive agent can ask for clarification. Cloud agent cannot — it just guesses.

## Verification scripts (for delegated work)
When delegating anything with a definite pass/fail, provide a verification command:
```
[Verification]
Run: `make verify-rename`
This script:
- Greps for any remaining "LegacyProcessor" (should be 0)
- Runs pytest with the "rename" markers
- Verifies mypy on the changed files
Success = script exits 0. Failure = agent must fix or report why.
```
Verification scripts turn "did it work?" from subjective to binary.

## Monitoring async agents
Cursor exposes cloud agent status:
- Web dashboard
- Desktop notifications
- Mobile app (yes — check status from your phone)

Discipline: check on cloud agents at your natural break points (post-lunch, before EOD). Don't obsess.

## Cost management for parallelism
More agents = more tokens = more cost. Expert habits:
- Delegate BOUNDED tasks (defined completion)
- Set token/time budgets when the tool supports them
- Cancel drifting agents fast
- Track cost weekly; adjust delegation cadence

## The delegation checklist
Before delegating a task, verify:
- [ ] Task has a clear completion criterion (not "improve X")
- [ ] Constraints are explicit (files, boundaries, non-goals)
- [ ] Verification command exists (or manual verification plan)
- [ ] Estimated time / token cost is worth delegating (not <5 min tasks)
- [ ] Failure mode is understood (what if agent can't complete? what if it produces junk?)

If any is missing, delegating will produce mess. Do it locally, interactively, instead.

## Mobile / remote workflows
Cursor's mobile app (and browser access to some features) enables:
- Kicking off tasks during commute
- Reviewing agent results on the way home
- Approving/merging cloud agent PRs from anywhere
- Monitoring long jobs while away from desk

For tasks with 30-minute cycles, this dramatically expands your working day. Use judiciously — being ALWAYS available is not the goal.
"""),
        "exercises": [
            ex(
                "C-07-1",
                "Set up two local git worktrees on a repo you use. Open both in Cursor. Do a small task in each — feel the parallel flow. Record: when did it help, when did it hurt?",
                "Direct experience with parallel worktrees.",
                "Typical: 'Helped when tasks were unrelated. Hurt when I forgot which worktree I was in and made changes in the wrong one.' Naming worktrees clearly (e.g., `-feature-a`, `-hotfix`) reduces confusion.",
            ),
            ex(
                "C-07-2",
                "Delegate one real task to a cloud/background agent using the delegation prompt template. Provide a verification script. Compare the deliverable to what interactive Agent would produce.",
                "Real delegation, real learning.",
                "Cloud agents produce more explicit output (they can't ask you) — often longer PRs with more edge-case handling. When the delegation prompt is good, quality matches or exceeds interactive. When bad, they wander further than interactive would.",
            ),
            ex(
                "C-07-3",
                "Write your delegation checklist in `ai-expert-lab/delegation-checklist.md`. Reuse for every cloud-agent task. Refine as you learn.",
                "Checklists prevent forgetting.",
                "First uses feel bureaucratic. After 5-10 delegations, going through the checklist takes 30 seconds and catches missing verification, ambiguous scope, or tasks that should have stayed local.",
            ),
            ex(
                "C-07-4",
                "Track your agent usage for a week: how many local, how many worktree-parallel, how many cloud. Cost per category. Are you at the right parallelism ratio for your workload?",
                "Data > gut.",
                "Common: overuse cloud agents on small tasks (wasted setup overhead), underuse on tasks that would benefit. Recalibrate weekly. The right ratio is per-person and per-project — no universal answer.",
            ),
        ],
    },
    {
        "id": "C-08",
        "title": "Advanced Debugging with Cursor",
        "level": "Cursor Advanced",
        "summary": "Cursor's debugging superpowers: agent-assisted RCA, log analysis, breakpoint-driven exploration. The systematic protocol.",
        "body": md("""
## The debugging superpowers
Modern Cursor offers:
- **Debug mode / iterative test loop** — Agent runs tests, reads failures, hypothesizes, tries fixes, re-runs
- **Log analysis** — pin logs, ask "why is this happening?"
- **Reproducer generation** — "write a minimal test that reproduces this bug"
- **Bisect assist** — walk through git history to find the introducing commit
- **RCA assist** — synthesize hypothesis from error + code + history
- **Breakpoint-aware Ask** — reason about state at a specific execution point

Not all versions expose all of these. The concepts apply regardless.

## The expert debugging protocol
```
1. REPRODUCE — get a reliable failing case
2. ISOLATE   — smallest input that fails
3. HYPOTHESIZE — what could cause this?
4. VERIFY   — cheap test of each hypothesis
5. FIX      — implement the correct fix
6. GUARD    — regression test to lock the fix
7. LEARN    — what did we learn about the codebase?
```
This protocol works with or without AI. AI accelerates every step.

## Step 1: Reproduce with AI
When you have symptoms but no reproducer:
```
[Context: paste the bug report, error, stack trace, or user complaint]
Ask mode with deep-thinking model:
"Based on this evidence, propose 3 different scenarios that could produce
this symptom. For each: describe the trigger, what code path would be
hit, and how to construct a minimal reproducer."
```
AI generates hypotheses; you test the most likely.

## Step 2: Isolate
```
Agent mode:
"Reduce the reproducer to the minimum: shortest input, fewest files,
smallest state. Preserve the failure. Show me the minimal test."
```
Result: a small pytest or script that fails deterministically. Now you can iterate fast.

## Step 3: Hypothesize (deep-thinking model)
```
Ask mode with deep-thinking, minimal reproducer pinned + relevant source:
"Given this reproducer and this code, list the top 5 hypotheses for
root cause. For each, tell me:
- The specific line(s) where the bug likely lives
- What evidence supports this hypothesis
- What single experiment would confirm or refute it"
```
Deep model earns its cost here — hypothesis quality matters.

## Step 4: Verify (fast iteration)
For each hypothesis:
- Add a print / logger.debug at the suspected spot
- Rerun the reproducer
- Confirm or refute

Agent mode helps: "Add a print at line 42 that shows the value of X. Rerun the reproducer. Report the output."

## Step 5: Fix
Now you know what's wrong. Fix is often small — one line or a few. Use Inline edit or Composer for scope.

Do NOT let Agent go wild here. Small fix = small change. Read the diff.

## Step 6: Guard (regression test)
```
Agent mode:
"Add a regression test that fails against the pre-fix code and passes
against the fixed code. Name it descriptively. Add to <appropriate file>.
Follow our testing conventions."
```
See the Regression Testing course for the guarding discipline. Every debug session should produce at least one regression test.

## Step 7: Learn (write it down)
After a hard debug session:
- Update `AGENTS.md` if the bug revealed a non-obvious constraint
- Update `.cursor/rules/` if AI could have prevented it
- Add a comment near the fix explaining WHY it exists
- Consider a post-mortem note in `docs/postmortems/` for high-impact bugs

## Log analysis workflows
### Massive log, need to find the pattern
Pin the log (or a representative sample). Ask:
```
"In this log, identify: (a) any errors or warnings, (b) any anomalies
in timing / order, (c) any state that seems inconsistent. Prioritize
by likely relevance to <the symptom>."
```

### Stack trace decoding
Pin the trace + relevant source. Ask:
```
"Walk through this stack trace. For each frame, explain what the code
was trying to do. Identify the deepest frame that might be at fault
and why."
```

### Comparing runs
Pin two logs (working run, broken run). Ask:
```
"Compare these two logs. What is the earliest divergence? Focus on
that point — what changed between the two runs?"
```

## The breakpoint workflow
When you have a debugger attached and paused at a breakpoint:
1. Note the file:line and relevant state
2. Ask (with relevant code pinned):
```
"Execution is paused at file.py:42. At this point, variable X = <value>,
Y = <value>, Z = <value>. State of the pipeline is <describe>.
Given the surrounding code, what should happen next? What might be
wrong with the current state?"
```
AI reasoning + your debugger visibility = powerful diagnostic combo.

## Bisect with Cursor
When you have "was working, now broken" and want to find the introducing commit:
- Manual bisect: `git bisect start` — walk the commits, test each
- Agent-assisted: "Between commits A and Z, find the first commit where <this test> fails. Use `git bisect run`."

For fully automated bisect, see the Regression Testing course. Cursor can DRIVE the bisect if you give it the reproducer command.

## Common debugging antipatterns AI can enable
### Antipattern: throwing prints everywhere
Agent adds 20 print statements. Fixes bug. Never removes them. Log pollution.
Fix: explicit cleanup step. "Remove all debug prints added in this session."

### Antipattern: "just make the test pass"
Agent modifies the test to accommodate the bug. Test now green, bug still there.
Fix: rule / manual review. "Never modify a test to make it pass unless the test was wrong."

### Antipattern: fix without regression test
Bug is fixed but no guard. Reintroduced 3 weeks later.
Fix: mandatory regression test step (Step 6 above).

### Antipattern: fix without understanding
Agent guesses and lands a fix. You don't understand it. Next similar bug: no leverage.
Fix: require RCA before fix. "Explain the root cause before proposing the fix."

## The debug budget
Set a time budget before starting: "I'll spend 45 minutes on this."
At budget exhaustion:
- If close: extend by 30 minutes
- If far: STOP. Write up what you know. Ask a colleague or switch tasks.
- Coming back fresh often produces the insight

AI accelerates debugging but doesn't guarantee success. Budgets prevent rabbit-holing.
"""),
        "exercises": [
            ex(
                "C-08-1",
                "For your next real bug, follow the 7-step protocol EXPLICITLY. Note the time each step took. Compare total to your usual debugging time.",
                "The protocol IS the training.",
                "Typical: first few uses feel slower (extra ceremony). After 5-10 bugs, faster than ad-hoc debugging because you don't wander. Regression test at the end means you don't debug the SAME bug again.",
            ),
            ex(
                "C-08-2",
                "Practice log analysis: take a real log (from any past project or public source). Ask the model to identify anomalies. Compare AI's findings to what you catch manually.",
                "Log-analysis-with-AI is a genuine superpower.",
                "AI catches patterns humans miss (subtle timing shifts, unusual state transitions). Humans catch context AI misses (project-specific meaning). Together = better than either alone.",
            ),
            ex(
                "C-08-3",
                "Set up an agent-driven bisect on a repo. Provide a reproducer script that exits 0/1 correctly. Kick off `git bisect run`. Verify it finds the introducing commit.",
                "Automated regression hunting.",
                "This is the highest-leverage debugging tool you can master. Once you have a reliable reproducer + bisect, finding regressions in months-old code takes minutes instead of hours.",
            ),
            ex(
                "C-08-4",
                "Write in `ai-expert-lab/debug-protocol.md`: your personal 7-step protocol adapted to your projects. Include the specific prompts you use at each step. Reuse it.",
                "Personalized protocol > generic advice.",
                "After 10 uses, your protocol is battle-tested. Share with team. Adopt teammates'. Consistent debugging = predictable outcomes.",
            ),
        ],
    },
    {
        "id": "C-09",
        "title": "Cursor + CI: From Agent Output to Green Checks",
        "level": "Cursor Advanced",
        "summary": "Making CI a first-class output of your Agent work. Verification loops, PR-ready diffs, Bugbot-style reviews.",
        "body": md("""
## The principle
The output of an Agent session should not be "code that seems right." It should be "code with green CI, ready to merge."

Experts close the loop between local Agent work and CI verification. If CI fails, Agent's job isn't done.

## The verification loop
```
1. Agent produces the change
2. Agent runs the local test suite (or a subset relevant to the change)
3. If red → Agent diagnoses and fixes → back to 1
4. If green → push branch, open PR
5. CI runs → if red, Agent addresses → push fixes → CI reruns
6. Only when CI green + reviewed → merge
```
Every step here is enforceable via prompts and rules.

## Making Agent run tests before finishing
Rule (in `.cursor/rules/`):
```
When completing any code change, always:
1. Run the relevant tests
2. Report the result
3. If any test fails, either fix it or explain why the failure is expected
4. Only claim completion when tests pass
```
This becomes automatic once rules are in place.

## PR-ready diffs
A "PR-ready" diff:
- Has no debug code
- Includes any needed tests
- Includes any needed docs
- Updates changelog
- Passes local tests + linters
- Has a clean commit history

Agent can produce all of these if you ask:
```
Complete the change. Then:
- Run: pytest, mypy, ruff
- Remove any debug prints or commented-out experiments
- Ensure the diff includes tests for new behavior
- Update CHANGELOG.md under [Unreleased]
- Rebase into a single clean commit with a descriptive message
Only report done when all of the above are complete.
```

## PR description generation
Once code is ready, have Agent draft the PR description:
```
Draft a PR description for these changes. Include:
- What (one paragraph)
- Why (context, linked issue)
- How (approach at high level)
- Testing (what I verified)
- Risks (anything reviewers should double-check)
- Screenshots or output if relevant
```
Cursor may have a "Generate PR" button that does this — check your version.

## Bugbot-style automated review
Cursor's Bugbot (or equivalent) is a subagent that reviews your local changes as if it were a reviewer. Usage:
- Trigger Bugbot on unstaged / staged / branch changes
- Bugbot posts inline comments (or a summary)
- You address findings, rerun, iterate

Expert use: run Bugbot BEFORE opening the PR to a human reviewer. Free "pre-review" catches embarrassments.

## CI failure workflow
When CI fails on your PR:
1. Read the failing check (Cursor can help — pin the CI log to Ask)
2. Ask: "Given this CI failure log, what's the likely cause? How to reproduce locally?"
3. Reproduce locally
4. Fix
5. Push. CI reruns.

Don't push blind fixes hoping CI passes. Reproduce, fix, verify locally FIRST.

## The ci-investigator pattern
For persistent or opaque CI failures, delegate to a specialized investigator (either Cursor subagent or a Claude Code headless task):
```
[Task] Investigate CI check "test-integration" failing on PR #234.
[Deliverable] Root cause + proposed fix in a short report.
```
This runs while you continue other work; report lands when done.

## Test-driven fix loops
When fixing a bug that has a reproducer:
```
Agent, follow this loop until green:
1. Run the reproducer test
2. If fail: propose a fix, apply it
3. Rerun the reproducer
4. If pass: verify no other tests regressed
5. Report completion with the diff
```
Agent iterates autonomously; you review the final state, not each iteration.

## Cursor + GitHub Actions
For repos with GH Actions:
- Cursor can read your `.github/workflows/*.yml` and understand the CI pipeline
- Ask: "Which of my current changes would cause the `lint` job to fail?"
- Agent can preemptively fix lint before push

For projects with painful CI (slow, flaky), local pre-flight discipline saves hours per week.

## Preventing "green tests, wrong code"
CI green ≠ code correct. Tests only catch what they test. Expert habits:
- Always eyeball the diff even when tests pass
- Ask (in Ask mode on the diff): "What could this diff break that tests wouldn't catch?"
- For risky changes, request extra reviewers or run in staging first

AI + CI is a strong safety net. Not a magic guarantee.

## The clean-branch discipline
Before opening a PR:
- Rebase onto latest main (or merge, per team preference)
- Verify no merge conflicts
- Verify tests still pass on the rebased branch
- Squash WIP / typo commits (Interactive rebase — see Git course Module 23)
- Push clean

Agent can handle most of this: "Rebase onto main. Squash WIP commits. Verify tests pass. Report status."

## The PR-to-merge workflow with AI
```
1. Agent writes code + tests, ensures local green
2. Agent generates PR description + creates PR
3. Bugbot (or equivalent) reviews the PR
4. You address Bugbot findings (or approve and merge)
5. Human reviewer reviews (if required)
6. CI runs on the PR — green
7. Merge (or agent merges if you have auto-merge configured)
```
Every step is AI-accelerated. Human oversight at the critical decision points.
"""),
        "exercises": [
            ex(
                "C-09-1",
                "Add a rule to your project (or `ai-expert-lab/`) that requires Agent to run tests before claiming completion. Test it: give Agent a task, see if it follows the rule.",
                "Rule → observed behavior.",
                "Well-tuned rule = Agent reports test status unprompted. If Agent still claims 'done' with tests untested, refine the rule (be more specific).",
            ),
            ex(
                "C-09-2",
                "For a real change, drive the full verification loop: Agent codes → runs tests → fixes any failures → generates PR description → opens PR. Compare to your usual workflow.",
                "End-to-end AI-assisted change.",
                "Time from 'start task' to 'PR opened' typically drops 30-50% vs manual. Quality is similar or better because verification isn't skipped. This IS what expert-level AI use produces.",
            ),
            ex(
                "C-09-3",
                "Run Bugbot (or Cursor's local review) on a real change before opening a PR. Note what it finds. Was any of it embarrassing? Fix and rerun until Bugbot has nothing to say.",
                "Pre-review saves face and time.",
                "Typical Bugbot findings: missing edge cases, unclear error messages, missing tests for a new branch, minor style violations. Addressing these before human review shortens review cycles.",
            ),
            ex(
                "C-09-4",
                "When CI next fails on a PR, use the CI-failure workflow: reproduce locally with AI help, fix, push. Time the whole cycle. Compare to your usual approach.",
                "The systematic CI-failure protocol.",
                "Systematic: 10-30 minutes. Ad-hoc (push blind fixes and pray): often 1-2 hours. The reproduce-locally step is what separates them.",
            ),
        ],
    },
    {
        "id": "C-10",
        "title": "Composer & Multi-File Surgical Edits",
        "level": "Cursor Advanced",
        "summary": "Composer is the precision tool for coordinated edits across 3-10 files. Scope matters more than model.",
        "body": md("""
## What Composer is for
Coordinated edits across a KNOWN set of files, where the changes are RELATED:
- Rename a symbol used in 8 files
- Update a shared API's callers after signature change
- Add a new field to a struct + its serializers + its tests
- Refactor a pattern used in 6 similar places
- Migrate away from a deprecated import across a module

What Composer is NOT for:
- One-file changes (use Inline)
- Broad "clean up the codebase" (use Agent with a plan)
- Exploratory changes where scope is unknown

## The scoping discipline
Composer works best with 3-10 files in scope. More = drift risk.

Curate the file list DELIBERATELY:
- Not "all files that MIGHT be related"
- Actually related files, confirmed
- If more than 10, split into two Composer runs

## The pattern-then-verify workflow
```
1. Identify the pattern to change (in your head or in Ask mode)
2. Find all instances (grep, LSP references, or Ask)
3. Select the files (max 10)
4. Composer: describe the pattern change with an example
5. Composer produces coordinated edits
6. Review the diff (Cursor makes this easy — side-by-side)
7. Apply. Run tests.
```

## Good Composer prompts
Specific, referenced to an example:
```
In the pinned files, wherever you see:
    logger.info("something happened", extra={"data": data})

Change to:
    logger.info("something happened", extra=make_log_context(data))

Where `make_log_context` is defined in `src/logging.py`.

Only touch call sites — do not modify the definition.
```

## Bad Composer prompts
Vague:
```
Clean up the logging in these files.
```
Result: Composer reinterprets scope, adds unrelated changes.

## Model choice for Composer
- Fast Composer models are optimized for exactly this: pattern-based multi-file edits
- Deep-thinking models are usually overkill for Composer's use case
- Balanced is fine for anything ambiguous

Rule: match model to complexity. Simple pattern renames → fast. Nuanced refactor → balanced.

## The multi-hunk review discipline
Composer produces a diff with hunks in multiple files. Review ALL of them:
- Look for the intended change in every expected place
- Look for unintended changes (Composer sometimes "helpfully" fixes adjacent code)
- Look for missed places (Composer sometimes skips edge cases)

If any hunk is wrong, REJECT the whole diff and refine the prompt. Do NOT hand-fix a broken multi-file diff — it desynchronizes files.

## Composer for large-scale rename
For symbol rename across many files:
- LSP rename (Cursor's built-in refactor) is usually more reliable
- Composer is better when the change is semantic (not just textual)

Example where Composer wins over LSP rename:
```
Rename `LegacyProcessor` → `Processor`, AND:
- Update docstrings mentioning "legacy processor" (natural language)
- Update comments
- Update log messages that say "using legacy processor"
- Update test names like `test_legacy_processor_edge_case`
```
LSP handles just the symbol. Composer handles the semantic sprawl.

## Composer + tests
After a Composer refactor, ALWAYS run tests:
```
After Composer:
1. Run: pytest
2. If any test fails: Ask (with the failure pinned) what the Composer missed
3. Refine the Composer prompt and re-run
```
Don't accept a Composer diff without test verification for anything non-trivial.

## Composer anti-patterns
### Anti-pattern: over-broad scope
50 files selected. Composer's output is diffuse, hard to review. Split into 5 Composer runs of 10 files each.

### Anti-pattern: no example
Vague pattern description. Composer guesses. Always show an example of the change (before/after).

### Anti-pattern: hand-editing Composer output
Composer produced a mostly-correct diff. You want to fix 2 lines manually. RISK: rest of the diff assumes those lines have a certain shape. Better: refine prompt, rerun.

### Anti-pattern: chained Composer runs without git commits
Composer 1 → Composer 2 → Composer 3, all on same worktree. If anything's wrong at run 3, you can't easily bisect. Commit between runs.

## The pre-Composer checklist
- [ ] I know the exact pattern to change
- [ ] I have an example (before + after)
- [ ] I've selected the specific files (3-10 max)
- [ ] I have a test I can run after to verify
- [ ] Non-goals are explicit (what NOT to touch)

If checklist incomplete, don't Composer yet. Use Ask to complete the missing pieces first.
"""),
        "exercises": [
            ex(
                "C-10-1",
                "Identify a real refactor across 5-10 files (in your code or a sample repo). Follow the pattern-then-verify workflow. Use Composer with a good prompt (example, scope, non-goals). Review carefully.",
                "One good Composer run > 30 ad-hoc edits.",
                "You have a coordinated multi-file change reviewed as a single diff. Tests pass. This is Composer's sweet spot.",
            ),
            ex(
                "C-10-2",
                "Deliberately give Composer a BAD prompt (vague scope, no example). Observe the mess. Then refine and re-run with a good prompt. Compare outputs.",
                "The prompt quality feedback loop.",
                "Bad prompt: diffuse changes, missed spots, adjacent unrelated edits. Good prompt: focused, complete, clean. This exercise is faster to feel than to describe.",
            ),
            ex(
                "C-10-3",
                "Compare LSP rename vs Composer rename for a symbol used in 20+ files. When does LSP win? When does Composer win?",
                "Right tool for the job.",
                "LSP: precise, deterministic, fast for symbols. Composer: catches semantic sprawl (docs, comments, log messages, test names). Use both for large renames — LSP first, then Composer for the semantic tail.",
            ),
            ex(
                "C-10-4",
                "Write in `ai-expert-lab/composer-checklist.md`: your pre-Composer checklist. Use it before every Composer run for a week. Note what changed.",
                "Discipline through checklist.",
                "Typical: initially 'this is too much ceremony,' after a week: 'I catch scope issues before wasting a Composer run.' The 30 seconds of checklist saves 5-10 minutes of misdirected work.",
            ),
        ],
    },
    # ─────────────────────────── PHASE 2: CLAUDE CODE ───────────────────────────
    {
        "id": "CC-01",
        "title": "Claude Code Mode Landscape",
        "level": "Claude Code Advanced",
        "summary": "Interactive vs headless vs SDK. Each mode fits a different workflow.",
        "body": md("""
## The three fundamental CC modes
### Interactive (default)
- You type in a terminal, Claude Code responds
- Tool calls happen with your approval (y/Y/n permission model)
- Iterative dialogue
- Best for: active coding sessions, exploration, complex tasks needing oversight

### Headless (`-p` / `--print` / prompt-only)
- Single prompt, single response, no interaction
- Runs to completion or fails
- Scripted / automated / CI-driven
- Best for: batch operations, CI jobs, delegated tasks, cron-scheduled work

### SDK (programmatic)
- Python or TypeScript SDK
- Full control over prompt, tools, streaming, error handling
- Integrates CC into your applications
- Best for: bots, integrations, custom workflows, pipelines

## The mode decision
Ask:
- "Am I actively at the keyboard, iterating?" → Interactive
- "Do I want to fire and forget, script it?" → Headless
- "Am I building software that uses Claude?" → SDK

Most experts use ALL three. Interactive for exploration and design; Headless for delegated / CI tasks; SDK for tools they build.

## Interactive mode nuances
- Slash commands (`/plan`, `/model`, `/clear`, `/compact`, `/init`) change session state
- Permission model: `y` this call, `Y` this call type, `n` deny
- `Ctrl+C` stops current tool call; `Ctrl+D` exits
- Auto-context: recent files, project structure, git state

Expert habit: `/clear` between unrelated tasks. Context bleeding is expensive.

## Headless mode nuances
```bash
claude-code -p "Fix the failing test in tests/test_pagination.py" \\
  --allowedTools "read,write,bash" \\
  --output-format json
```
Key flags:
- `-p PROMPT` — the prompt
- `--allowedTools` — explicit tool allowlist (security)
- `--output-format` — text (default) or json (for parsing in scripts)
- `--max-turns` — cap on tool call iterations
- `--session-id` — resumable across runs

Headless requires MORE prompt discipline — no interactive correction possible.

## SDK nuances (brief)
```typescript
import { Agent } from '@cursor/sdk'; // or Claude SDK equivalent

const agent = await Agent.create({
  model: 'claude-opus-4-7-thinking-high',
  systemPrompt: '...',
  tools: ['read', 'write', 'bash'],
});

const result = await agent.prompt('Fix the failing test', {
  streaming: true,
  onEvent: (evt) => console.log(evt),
});
```
Real SDK usage: bots, dashboards, custom review pipelines, agentic apps.

## When each mode wins
| Situation | Mode | Why |
|-----------|------|-----|
| Debug a subtle bug | Interactive | Need oversight and iteration |
| Add copyright headers to 200 files | Headless | Bounded, scriptable |
| Nightly code review of open PRs | SDK (or headless in cron) | Automated, structured output |
| Explore an unfamiliar codebase | Interactive | Ask, follow up |
| Generate 50 goldens from a spec | Headless with a loop | Bulk, deterministic |
| PR triage bot in Slack | SDK | Custom integration |
| Refactor with human oversight | Interactive | Review each change |
| Reformat entire repo | Headless | Fire and forget |

## The auto-approve calibration
Interactive:
- Default: prompt for each tool call
- `Y` (uppercase) approves all future calls of that type in session
- Aggressive experts use `Y` on read tools, cautious on write/bash

Headless:
- All tools in `--allowedTools` are pre-approved
- If a tool isn't in the list, execution fails
- SECURITY: never `--allowedTools '*'` in headless. Explicit list.

## The permission model in practice
Interactive session:
```
> Read src/api/users.py?
[Y/n] Y  (approves all future reads)

> Write to src/api/users.py?
[Y/n] y  (approves just this write)

> Bash: pytest tests/
[Y/n] y  (approves just this bash call)
```
Reading: freely allow. Writing: consider each. Bashing: definitely consider.

## Session management
- `/clear` — wipe conversation, keep session
- `/compact` — summarize context to save tokens
- `/init` — set up CLAUDE.md if missing
- `/model` — switch model mid-session
- `/cost` — see current session cost
- `/help` — everything else

Expert habit: `/compact` when session gets long. Long contexts degrade quality AND cost more per turn.

## The multi-terminal workflow
Some experts run 2-3 CC sessions in different terminals:
- Terminal 1: interactive coding session
- Terminal 2: headless CI investigator running in background
- Terminal 3: SDK-driven bot dashboard

`tmux` or your terminal multiplexer helps. Screen real estate matters.

## When to switch mode mid-workflow
Common pattern: interactive exploration → headless execution.
1. Interactive: figure out the spec, draft the plan
2. Save the spec to a file (`docs/plans/foo.md`)
3. Headless: `claude-code -p "Execute plans/foo.md" --allowedTools "..."`
4. Result: agent runs to completion while you do other work

This hybrid pattern is where CC shines vs pure interactive tools.
"""),
        "exercises": [
            ex(
                "CC-01-1",
                "Set up all three modes on your machine: interactive (run CC), headless (`claude-code -p 'echo hello' --allowedTools 'bash'`), SDK (install and run a minimal script). Verify each works.",
                "Mechanical setup — but do all three.",
                "Verify: interactive session opens; headless returns exit 0 with output; SDK script runs without error. Now you have all three modes available.",
            ),
            ex(
                "CC-01-2",
                "For each of these tasks, pick a mode and justify:\n(a) Fix a specific bug in one file\n(b) Rename a symbol across 50 files\n(c) Nightly review of yesterday's merged PRs\n(d) Explore a new dependency's API\n(e) Build a Slack bot that answers questions about your repo",
                "Practice mode routing.",
                "(a) Interactive — need oversight for a fix. (b) Headless with a script — bounded, batchable. (c) Headless in cron OR SDK — scheduled, structured output. (d) Interactive — questions and follow-ups. (e) SDK — custom integration.",
            ),
            ex(
                "CC-01-3",
                "Run a real task in headless mode with explicit `--allowedTools` list. Notice: what tools does the task need? What did you have to think about that you'd normally not?",
                "Headless forces explicit thinking.",
                "Common: you realize you were relying on implicit approvals interactively. Explicit lists force clarity. If the task needs `bash` and `write`, list them. If it doesn't need `network`, don't allow it — security.",
            ),
            ex(
                "CC-01-4",
                "Practice `/clear` and `/compact` discipline: in an interactive session, note when context is getting long. `/compact` when appropriate. Notice how quality (and cost) shifts.",
                "Context management is expert-level CC.",
                "Long contexts degrade — model quality drops, cost rises, hallucinations increase. Periodic /compact keeps sessions healthy. Rule: if a session has gone through 3+ distinct sub-tasks, /clear or /compact.",
            ),
        ],
    },
    {
        "id": "CC-02",
        "title": "Model Selection in Claude Code",
        "level": "Claude Code Advanced",
        "summary": "Opus vs Sonnet vs Haiku, thinking budgets, `/model` per session. The Claude-specific routing.",
        "body": md("""
## The Claude model tiers
Claude Code's model landscape (as of 2026, subject to Anthropic's cadence):
- **Haiku** — fastest, cheapest, weakest reasoning
- **Sonnet** — balanced default (versions 3.5, 4.x)
- **Opus** — deepest reasoning, most expensive (4.x, 5.x)
- Each may have **thinking** variants — extended reasoning budgets

## When to reach for each
### Haiku
- Simple file operations
- Quick reformatting
- Trivial questions
- High-volume batch operations where cost dominates
- Rarely the right choice for design or debugging

### Sonnet
- Everyday coding
- Feature implementation from a clear spec
- Test authoring
- Straightforward refactors
- Most CC sessions default here — good balance

### Opus
- Architectural decisions
- Hard debugging
- Novel design
- Complex refactors touching multiple concerns
- Anything where quality > speed

### Opus with extended thinking
- Genuinely hard problems: race conditions, subtle correctness, numerical stability
- Planning novel systems
- Ambiguous requirements needing careful reasoning
- Post-mortems and RCAs

## Cost calibration (order of magnitude)
- Haiku: 1x
- Sonnet: 5-10x
- Opus: 25-50x
- Opus + extended thinking: 50-100x+

An 8-hour Opus-thinking session can cost $50-200 depending on token volume. Sonnet for the same session: $5-20. Route accordingly.

## `/model` in interactive sessions
```
> /model
Current: claude-sonnet-4.x
Available: haiku, sonnet, opus, opus-thinking-high, ...

> /model opus-thinking-high
Switched to opus-thinking-high.
```
Switch takes effect immediately. Cost meter jumps. Reasoning depth jumps.

Expert pattern:
- Start sessions in Sonnet (default)
- Switch to Opus-thinking for planning or hard sub-problems
- Switch back to Sonnet for execution
- Consider Haiku for grep-like tasks

## Model choice for headless
Specify per invocation:
```bash
claude-code -p "..." --model claude-opus-4-7-thinking-high --allowedTools "..."
```
For scripts running many headless calls, default to Sonnet or Haiku unless a specific call needs deep reasoning.

## Thinking budgets (Anthropic-specific)
Extended thinking modes let the model reason internally before responding. Budgets:
- `low` — brief thinking
- `medium` — moderate
- `high` — extensive

For hard problems, `high` is dramatically better than `medium`. For everyday work, `medium` or off is enough. Turning `high` on for boilerplate is expensive with no quality gain.

## The escalation ladder
Sensible progression when stuck:
1. Start with Sonnet
2. If Sonnet flounders after 1-2 tries: switch to Opus
3. If Opus flounders: switch to Opus with thinking-high
4. If Opus-thinking floundes: rethink the framing (maybe it's not solvable this way)

Skipping to Opus-thinking for everything is wasteful. Escalating on evidence is disciplined.

## The de-escalation habit
After a hard sub-problem is resolved with Opus-thinking, switch BACK to Sonnet for the remaining routine work. Don't leave the expensive model on out of laziness — that's most of the excess cost in AI-heavy workflows.

## Cost visibility
```
> /cost
Session cost: $2.34 (Sonnet: $1.10, Opus: $0.85, Opus-thinking: $0.39)
Turns: 42. Tokens: 128k in, 15k out.
```
Check `/cost` periodically. Learn your session cost distributions. When surprised, investigate — usually leftover Opus-thinking or a runaway context.

## Cross-tool model routing
- Cursor and Claude Code have overlapping model catalogs
- Sometimes Cursor has better access to a model (or vice versa)
- Route by tool + model, not just model

For expensive deep-thinking work: which tool has better UX for your workflow? Interactive design in Cursor Ask with Opus-thinking is often smoother than CC's terminal-based equivalent for the same model.

## The single most useful CC model habit
**When entering planning, debugging, or design phases, EXPLICITLY switch to Opus (with thinking, when the problem warrants it). When exiting those phases, EXPLICITLY switch back to Sonnet.**

The explicit switches are the discipline. The model dropdown / `/model` is your instrument panel — don't fly on autopilot when precision matters.
"""),
        "exercises": [
            ex(
                "CC-02-1",
                "Run the same 30-minute task in Sonnet vs Opus vs Opus-thinking-high (in CC). Compare: quality, time, cost. When did the extra depth pay off?",
                "Direct evidence for your work profile.",
                "Typical: Sonnet gets 80% right in 30 min. Opus gets 90% right in 30-45 min. Opus-thinking gets 95% right in 45-60 min. For a design phase, the extra 5-15% might be worth it. For routine execution, usually not.",
            ),
            ex(
                "CC-02-2",
                "Practice `/model` switching mid-session. Start in Sonnet, hit a hard sub-problem, switch to Opus-thinking, resolve, switch back. Repeat until natural.",
                "Muscle memory for model routing.",
                "Initially feels like ceremony. After 5-10 sessions, the switches feel like changing gears in a manual car — deliberate, seamless. Cost savings compound.",
            ),
            ex(
                "CC-02-3",
                "Check `/cost` at the end of your next 5 CC sessions. Note the total, distribution by model. Are you accidentally leaving expensive models on?",
                "Cost visibility = cost discipline.",
                "Common realization: 20-40% of cost from 'leftover Opus-thinking' after the hard problem was solved. De-escalation habit reclaims that spend.",
            ),
            ex(
                "CC-02-4",
                "Write in `ai-expert-lab/cc-model-defaults.md`: your default model per phase (exploration, planning, execution, debugging, review). Include escalation triggers ('switch to Opus when...').",
                "Personal defaults, defensible choices.",
                "Sample: 'Exploration: Sonnet. Planning: Opus-thinking-medium (upgrade to high on novel systems). Execution: Sonnet. Debugging: Sonnet for known bugs, Opus for mysteries. Review: Sonnet.' Your defaults will differ. What matters: they're explicit.",
            ),
        ],
    },
    {
        "id": "CC-03",
        "title": "CLAUDE.md as an Engineering Artifact",
        "level": "Claude Code Advanced",
        "summary": "CLAUDE.md is not a scratchpad. It's versioned, reviewed, layered documentation for AI agents.",
        "body": md("""
## What CLAUDE.md is
A markdown file (usually at repo root, but there's a hierarchy) that Claude Code auto-loads for every session. It's how your project SPEAKS to the model.

Think of it as: "if I hired a competent engineer today, what would I want them to know before touching this codebase?"

## The CLAUDE.md hierarchy
Claude Code respects multiple CLAUDE.md files:
- `~/.claude/CLAUDE.md` — global, personal (your preferences everywhere)
- `<repo>/CLAUDE.md` — project-level (versioned, team-shared)
- `<repo>/<dir>/CLAUDE.md` — directory-level (rules specific to that area)

Later (more specific) files augment earlier ones. Directory-level rules only apply when working in that directory.

## What belongs in project CLAUDE.md
### Essential
- Project purpose (one paragraph)
- Repository layout with key directories described
- Build/test/run commands (exact shell invocations)
- Coding conventions (style, testing, commit messages)
- Non-obvious constraints (things a smart engineer would still get wrong)
- Where to look for X (e.g., "auth code is in `src/auth/`, don't touch `src/legacy_auth/`")

### Often useful
- Framework-specific quirks
- Deprecated patterns to avoid
- Preferred libraries when multiple exist
- Testing philosophy (what level of coverage, what to prioritize)
- PR / commit conventions

### Never
- Restatements of things models know (Python syntax, git basics)
- General programming platitudes
- Personal preferences that vary among teammates
- Outdated information

## Directory-level CLAUDE.md examples
`src/api/CLAUDE.md`:
```
# API layer conventions

- Every endpoint has a corresponding pytest test
- Use `client` fixture in tests, not raw requests
- Errors return JSON: `{"error": "code", "message": "human message"}`
- Auth is enforced via `@requires_auth` decorator
- Log at INFO for request/response, ERROR for exceptions
- Rate limits configured in `settings.py`, not per-endpoint

## Common tasks
- Adding an endpoint: see `docs/patterns/new-endpoint.md`
- Deprecating an endpoint: add `@deprecated(version, alt="...")` and warn in docs
```
This file loads ONLY when working under `src/api/`. Focused rules, high signal.

## The CLAUDE.md quality test
Same as rules test: for each line, ask "would the model make a mistake without this?" If yes, keep. If no, cut.

Aim: 30-150 lines for project root CLAUDE.md. Longer = probably bloated.

## Refinement as a discipline
Every time Claude Code makes the same mistake twice, ADD it to CLAUDE.md:
```
## Non-obvious constraints
- Do NOT add new npm dependencies. We have security review; ask first.
- Do NOT use `datetime.now()` — use `time_service.now()` for testability.
- Do NOT commit inside src/generated/ — regenerated by CI.
```
Over 3-6 months, CLAUDE.md becomes a highly-tuned artifact.

## The `/init` command
CC's `/init` command scans the repo and drafts an initial CLAUDE.md:
- Detects languages, frameworks, build tools
- Suggests structure
- Populates commands section from what it finds

Use `/init` as a starting point on new projects. THEN refine manually — the auto-draft is generic.

## Auto-updated CLAUDE.md via hooks
CC hooks (`~/.claude/hooks/`) can run scripts on session events. Pattern:
- Hook: after successful task, ask model "did we learn anything worth adding to CLAUDE.md?"
- If yes, propose an update as a PR

This makes CLAUDE.md a living document. Advanced setup; worth it for teams.

## Team review of CLAUDE.md
- Treat CLAUDE.md as code — PR reviews, comments, iterative refinement
- Deprecate rules that no longer apply
- New team members read it as onboarding

## CLAUDE.md vs AGENTS.md vs .cursor/rules/
- **AGENTS.md** — generic across AI tools (Claude Code, Cursor, others). Cross-tool standard.
- **CLAUDE.md** — Claude Code specifically.
- **.cursor/rules/** — Cursor specifically.

If you use both tools, consider:
- AGENTS.md as the primary source
- CLAUDE.md and .cursor/rules/ as thin pointers to AGENTS.md + tool-specific tweaks

OR maintain all three separately if the tools have divergent needs. There's no universal right answer — pick one convention and stick with it.

## Common CLAUDE.md failure modes
### Failure: too long
500 lines. Model ignores half. Team ignores all.
Fix: aggressive pruning. Anything not preventing a real mistake goes.

### Failure: too abstract
"Write clean code." Meaningless.
Fix: specific rules with example.

### Failure: stale
References old libraries, deprecated patterns, defunct services.
Fix: quarterly review, update or delete.

### Failure: personal
Contains preferences only one dev cares about. Frustrates others.
Fix: personal preferences go in `~/.claude/CLAUDE.md`, not the project's.

## The 3 questions for every CLAUDE.md entry
1. Would a competent new engineer make this mistake without knowing this?
2. Is this SPECIFIC to this project (not general programming)?
3. Is it CURRENT (still relevant right now)?

Three yes: keep. Any no: cut.
"""),
        "exercises": [
            ex(
                "CC-03-1",
                "Run `/init` on a repo without an existing CLAUDE.md. Read the draft. What's useful? What's generic? Refine it into a real CLAUDE.md.",
                "The auto-draft is a starting point, not the answer.",
                "Typical: `/init` gets the structure right and 40-60% of the content right. Refinement adds the non-obvious constraints and project-specific rules that generic detection misses.",
            ),
            ex(
                "CC-03-2",
                "Audit an existing CLAUDE.md (or your `AGENTS.md`). Apply the 3-question test to every entry. Cut what fails.",
                "Signal > volume.",
                "Typical: 30-60% survives rigorous audit. Result: cleaner file, model behavior improves (more signal, less noise). Sometimes teammates notice the change.",
            ),
            ex(
                "CC-03-3",
                "Add a directory-scoped CLAUDE.md for a specific area of your codebase (e.g., `src/tests/CLAUDE.md` with testing conventions). Verify: CC picks it up when working in that directory.",
                "Scoped rules > global rules.",
                "Model behavior when editing tests aligns with the scoped rules. Adding tests follows the pattern. This is how large repos with diverse conventions stay coherent.",
            ),
            ex(
                "CC-03-4",
                "Draft an ADR (architecture decision record) style entry for CLAUDE.md documenting a non-obvious constraint from your project. Include: what, why, alternatives considered, when to revisit.",
                "CLAUDE.md as durable docs.",
                "Sample: '**Constraint**: All timestamps use UTC internally. **Why**: our infrastructure spans 3 timezones. **Alternatives**: local + tz, split fields — rejected due to bug history. **Revisit**: if we consolidate to one region.' This kind of entry pays off for years.",
            ),
        ],
    },
    {
        "id": "CC-04",
        "title": "Plan-First Workflows with Extended Thinking",
        "level": "Claude Code Advanced",
        "summary": "How to use `/plan`, thinking modes, and structured planning to make execution boring.",
        "body": md("""
## The `/plan` mode
Some CC versions expose `/plan` as a mode where the model produces a plan without executing. If yours does, use it. If not, achieve the same via prompt:
```
Do NOT execute anything. Produce a plan for:
[task description]

Plan should include:
- Files to touch (with reason)
- Order of operations
- Tests to add
- Risks and open questions
- Estimated effort

Wait for my approval before executing.
```

## Extended thinking for planning
Planning is where extended thinking earns its cost. Turn it on explicitly:
```
> /model claude-opus-4-7-thinking-high
Switched.

> [Plan prompt as above]
```
Deep thinking on a plan produces more thorough analysis than deep thinking on execution. Return on token spend is highest here.

## The `ultrathink` / `think hard` / `think` cues
Anthropic exposes thinking budget cues in the prompt itself:
- Regular request — model does default thinking
- "think hard about this" — extended thinking
- "think really hard" / "ultrathink" — extensive thinking

Version details vary; treat these as suggestions to the model to spend more reasoning budget. Combine with model choice (Opus) for maximum depth.

## The plan artifact
Whether from `/plan` mode or manual prompt, save the plan as a FILE:
```
docs/plans/2026-09-add-pagination.md
```
- Versioned in git
- Referenced by name in execution prompts
- Reviewable in PRs
- Updated as the plan changes

Plans as files > plans in chat history.

## The plan-then-execute pattern
Full flow:
```
1. Interactive session (Opus-thinking): draft plan
2. Iterate on the plan for 2-3 turns
3. Save the plan: docs/plans/foo.md
4. /clear the session (or exit)
5. New session (Sonnet, or same session with /model switch):
   "Execute the plan at docs/plans/foo.md. Follow it step by step.
    If deviation needed, stop and ask."
6. Agent executes with clear scope
7. If plan needs update mid-execution, update the FILE, not just the chat
```
This pattern separates thinking from doing. Both benefit.

## Plans as team artifacts
When plans are files:
- Team can review before execution
- Future you can see WHY changes were made
- New team members can understand HOW things got the way they are
- CI can validate plan format (linting for structure)

## Multi-phase plans
Complex work has phases. Structure the plan:
```
# Add cursor-based pagination

## Phase 1: Design (2h)
- Cursor encoding
- API contract
- Migration plan
Deliverable: docs/design/pagination.md

## Phase 2: Implementation (4h)
- Migration
- Encoder/decoder
- Endpoint changes
Deliverable: PR with code + tests

## Phase 3: Rollout (2h)
- Deploy to staging
- Deprecation notice to clients
- Monitor for 24h
Deliverable: production deploy + docs updated
```
Each phase gets its own execution session, ideally its own PR.

## When to skip planning
- Trivial changes (fix a typo, one-line change)
- Highly repeated patterns you've done 10+ times
- Emergency hotfixes (plan RETROACTIVELY in the postmortem)

Everything else: plan. Even 10 minutes of planning pays back on non-trivial work.

## Plan refinement loop
```
1. Draft plan (Opus-thinking)
2. Read it. What's missing? What's wrong?
3. "In this plan, [specific concern] isn't addressed. How should we handle it?"
4. Model updates the plan
5. Repeat until the plan feels complete
6. Deep-thinking pass: "What could go wrong with this plan? What are the risks?"
7. Address risks
8. Approve for execution
```
3-5 turns of refinement is typical. First-shot plans are almost never good enough.

## Turning plans into scripts
For repeatable work (deploys, migrations), the plan → executable script pipeline:
1. Draft plan for the operation
2. Refine
3. "Convert this plan into a bash script (or Python script) that executes each step. Include error handling and rollback for each step."
4. Review the script
5. Test in staging
6. Use for real

Plans become reusable automation.

## Plan review checklist
Before approving a plan for execution:
- [ ] All files to touch are listed (spot-check: is anything missing?)
- [ ] Order of operations makes sense (dependencies first)
- [ ] Tests are called out (what to add, what to verify)
- [ ] Risks are named (not just optimistic)
- [ ] Non-goals are explicit (what NOT to do)
- [ ] Effort estimate is realistic (a rough hour count)
- [ ] Rollback plan exists (or "no rollback needed" is justified)

If any is missing, refine further before executing.
"""),
        "exercises": [
            ex(
                "CC-04-1",
                "For a real task, use `/plan` (or equivalent prompt) with Opus-thinking. Save the plan as a file. Iterate 3-4 turns. Compare final plan quality to first draft.",
                "See the value of iteration.",
                "Typical: first draft is 60-70% complete. Third pass with risks + open questions is 90%+ complete. The extra 20-30% is what would have surfaced as expensive mid-execution corrections.",
            ),
            ex(
                "CC-04-2",
                "Execute a plan-from-file in a fresh session: `Execute the plan at docs/plans/foo.md. Report progress.` Notice: how well does the model follow it? What deviations happen?",
                "Test the plan-to-execution handoff.",
                "Good plans → tight execution. Model references the file, follows steps, flags deviations. Bad plans → wandering. If model deviates constantly, the plan is under-specified — revise before continuing.",
            ),
            ex(
                "CC-04-3",
                "Practice the model-switching pattern: Opus-thinking for planning, Sonnet for execution. Track cost distribution across a real task.",
                "Cost-aware routing.",
                "Typical distribution: 60-80% Opus-thinking cost in the planning phase (short, high-value), 20-40% Sonnet cost in the execution phase (long, moderate value). Total often less than doing everything in Sonnet — because good planning cuts execution turns.",
            ),
            ex(
                "CC-04-4",
                "Convert a plan into an executable script. Take a real repeatable task, plan it, then have the model produce a bash or Python script implementing the plan. Save and reuse.",
                "Plans become automation.",
                "You now have a script for a task that used to require decisions. Repeated executions are consistent. This is how ad-hoc AI-assisted work becomes team infrastructure.",
            ),
        ],
    },
    {
        "id": "CC-05",
        "title": "Execution Discipline: Tool Allowlists, Hooks, Auto-Approve",
        "level": "Claude Code Advanced",
        "summary": "Making Claude Code do exactly what you want, nothing you don't. Security and predictability at scale.",
        "body": md("""
## The permission model recap
Interactive: prompt per tool call, `Y` to approve future calls of type.
Headless: `--allowedTools` list, everything else fails.

Expert defaults skew toward EXPLICIT allowlists even interactively — reduces "oh I didn't mean to do that" mistakes.

## Tool categories
- **Read** — file reads, directory listings, git status, log reading (LOW RISK — allow broadly)
- **Write** — file edits, file creation (MEDIUM RISK — allow with awareness)
- **Bash** — shell command execution (HIGH RISK — allow specific patterns or approve each)
- **Network** — HTTP calls, package installs (HIGH RISK — allow deliberately)
- **Delete** — file removal (HIGH RISK — approve each unless sandboxed)

Different tools deserve different scrutiny.

## Recommended allowlists per context
### Personal, trusted repo, interactive
- Auto-approve: read
- Prompt: write, bash
- Never: unnecessary network

### Shared repo, interactive
- Auto-approve: read
- Prompt: everything else

### Headless, personal machine
```
--allowedTools "read,write,bash,pytest"
```
Explicit. No surprises.

### Headless, CI
```
--allowedTools "read,write,bash:pytest,bash:make"
```
Restrict bash to specific commands where possible. No network unless required.

### Untrusted repo, evaluation only
```
--allowedTools "read"
```
Read-only. Cannot modify anything.

## Hooks
CC hooks run scripts at session events (as of writing, an evolving feature — check current docs):
- Pre-session: environment setup
- Pre-tool-call: intercept and possibly veto
- Post-tool-call: audit / cleanup
- Post-session: summary / logging

Example hook use cases:
- Log every bash command to a security audit file
- Reject bash commands matching dangerous patterns (`rm -rf /`, `curl | bash`, etc.)
- After session, ask "did we learn anything worth documenting?"
- Auto-run linter after every write

## The bash-command discipline
Most risk comes from bash. Expert habits:
- Read the exact command before approving
- Prefer specific commands (`pytest tests/api/`) over broad ones (`pytest`)
- Refuse chained commands with `&&` if the second command wasn't discussed
- Never approve `curl | bash` or equivalent
- Never approve `sudo` in an AI session

## Runaway prevention
CC can loop if a task is misspecified. Guardrails:
- `--max-turns N` in headless: hard cap on iterations
- `--max-tokens N`: cap on generation length
- Session `/cost` check: if it's spiking, investigate
- Interrupt discipline: don't hesitate to `Ctrl+C`

## Session resumption
CC supports `--session-id` (or resume prompts) for continuing sessions:
- Useful for long tasks split across days
- Preserves conversation context
- BE CAREFUL: resumed sessions carry the same context risks (stale, drifted)

Rule: resume for meaningful continuation. `/clear` for a fresh task.

## Environment variables and secrets
CC reads env vars from your shell. Best practices:
- Never `export API_KEY=xxx` in the shell where CC runs — it's readable
- Use secret managers (1Password CLI, `pass`, `gopass`) that inject per-command
- For headless in CI: use CI's secret system, not env vars in the workflow file

## The audit trail
For sensitive work, keep an audit trail:
```bash
claude-code -p "..." --output-format json | tee audit-$(date +%s).json
```
JSON output includes every tool call, response, cost. Reviewable after the fact. Essential for regulated environments.

## Auto-approve creep
Over time, users tend to `Y` more and more. Prevent creep:
- Weekly: review your default approvals. Any you shouldn't have?
- Reset auto-approvals in each new session
- Distinguish "trust the tool" from "trust this specific approval"

## The blast radius question
Before approving any tool call, ask: "What's the worst that happens if this call does something unintended?"
- Read a file: nothing bad.
- Write a source file: recoverable via git.
- Delete a file: recoverable via git IF committed; otherwise gone.
- Run `pytest`: fine.
- Run `pip install X`: possibly recoverable, but changes environment.
- Run `curl ... | bash`: unbounded blast radius. NEVER approve.

Match approval to blast radius.

## Post-session cleanup
After every non-trivial session:
- Check `git status` — any files you didn't expect?
- Check running processes — CC leave anything?
- Check `~/.claude/sessions/` — old sessions to prune?
- Check installed packages — any new ones from bash calls?

5 minutes of hygiene prevents accumulation of AI-session residue.

## The team-wide discipline
For teams:
- Standardize `--allowedTools` per environment
- Share hooks (versioned in a team repo)
- Audit CI CC invocations
- Post-incident review: was CC involved? Any tool call that shouldn't have been allowed?

CC in production requires the same discipline as any other automation.
"""),
        "exercises": [
            ex(
                "CC-05-1",
                "For your next headless CC run, use the most restrictive `--allowedTools` list that still lets the task complete. Notice: what tools does it actually need vs what you'd have allowed by default?",
                "Explicit allowlists reveal implicit assumptions.",
                "Common realization: 'I would have allowed network but the task didn't need it.' Least-privilege applied to AI is the same principle as least-privilege in security.",
            ),
            ex(
                "CC-05-2",
                "Write a hook (or design one on paper if hooks aren't set up yet) that logs every bash command CC runs. Review a session's log. Any surprises?",
                "Visibility into what CC actually does.",
                "Typical: most commands are expected (pytest, git status, ls). Occasionally a surprise (git diff piped somewhere unexpected). Logs make surprises catchable.",
            ),
            ex(
                "CC-05-3",
                "Practice the blast-radius question: for your next 10 tool call approvals, PAUSE and answer 'what's the worst that happens if this call misbehaves?' before approving.",
                "The habit is the training.",
                "Initially adds 2-3 seconds per approval. Within a day, becomes preconscious. Occasionally the answer is 'unbounded' — that's when you deny and ask CC to reframe.",
            ),
            ex(
                "CC-05-4",
                "Write in `ai-expert-lab/allowlist-defaults.md`: your standard allowlists for interactive personal, interactive shared, headless local, headless CI. Reuse.",
                "Documented defaults > ad-hoc choices.",
                "Documented allowlists become team standards. New CI job? Reference the defaults. New CC user on the team? Onboard with the defaults. Consistency reduces error surface.",
            ),
        ],
    },
    {
        "id": "CC-06",
        "title": "Advanced Debugging with Claude Code",
        "level": "Claude Code Advanced",
        "summary": "CC's debugging superpowers: iterative test-fix loops, bisect scripting, reproducer generation, log analysis.",
        "body": md("""
## The debugging protocol (same as Cursor's, tool-adapted)
```
REPRODUCE → ISOLATE → HYPOTHESIZE → VERIFY → FIX → GUARD → LEARN
```
CC has specific strengths at each step because of terminal-native workflows.

## Test-fix loop (CC's sweet spot)
```bash
claude-code -p "The test tests/test_foo.py::test_bar is failing.
Read the test, read the code under test, propose a fix, apply it,
rerun the test. If still failing, iterate up to 5 times. Report the final state." \\
--allowedTools "read,write,bash:pytest"
```
CC iterates: read → hypothesize → try → rerun. Each turn a small change. Ideal for bugs with a clear failing test.

Interactive equivalent:
```
> The test tests/test_foo.py::test_bar is failing. Fix it.
[CC reads, proposes, applies, runs pytest]
[Test still fails]
[CC iterates automatically until pass or gives up]
```

## Bisect scripting
For "was working, now broken":
```bash
# The reproducer must exit 0 on good, non-zero on bad
git bisect start HEAD v1.2.3
git bisect run pytest tests/test_regression.py::test_specific_case
```
CC can:
- Write the reproducer script from a bug description
- Run the bisect (in a headless session with bash allowed)
- Report the introducing commit

## Reproducer generation
Given a symptom without a test:
```
Interactive:
> Bug report: users on iOS 15 see blank screens on the settings page.
> Write a pytest that reproduces this bug against our current code.
```
CC:
- Reads relevant code
- Understands the reported symptom
- Constructs a minimal test case
- Verifies the test fails against current code

Sometimes the test is enough — the reproducer itself reveals the bug.

## Log analysis via CC
```bash
cat production-error.log | claude-code -p "Analyze this log.
Identify the earliest anomaly. Hypothesize causes. Suggest what
to check next." --allowedTools "read"
```
Or interactively: paste the log, ask.

CC (with a good model) is very good at:
- Spotting patterns in noisy logs
- Correlating timestamps across services
- Identifying the "first bad thing" that led to cascading failures
- Suggesting what additional info would clarify

## Debugging distributed systems
For issues spanning multiple services:
1. Collect logs from all services around the failure window
2. Paste (or file-attach) all of them
3. Ask CC to build a timeline
4. Ask which service acted first anomalously
5. Deep-dive into that service

CC can hold multi-service context better than a human trying to correlate manually.

## Debugging with hypotheses (deep-thinking model)
For truly hard bugs (races, memory, subtle state):
```
> /model claude-opus-4-7-thinking-high
> [Pin the reproducer, code, relevant logs]
> "Think really carefully. Propose 5 hypotheses for the root cause.
> For each, describe: (a) the specific mechanism, (b) evidence
> supporting it, (c) the cheapest experiment to confirm/refute,
> (d) likelihood (1-10)."
```
Opus with extended thinking is worth every token here. Debugging is where max reasoning ROI is highest.

## The "explain to me why this is broken" pattern
Sometimes just describing the symptom to CC produces insight:
```
> The service returns 200 OK but the response body is empty for
> exactly 1 out of every 30 requests, on average. No errors in logs.
> No pattern in which request. What could cause this?
```
CC generates hypotheses. Some you've considered; some you haven't. The unexpected ones are the value.

## Interactive step-through
For code you don't understand:
```
> Explain what happens when a request hits /api/users, step by step,
> from the middleware to the response. Note where state changes,
> where I/O happens, where errors could arise.
```
Better than reading code cold. CC narrates the flow; you learn structure.

## Regression tests as debugging output
Every debug session should produce at least one regression test. Prompt:
```
> After fixing, write a regression test that:
> - Fails against the pre-fix code
> - Passes against the fixed code
> - Has a name describing what it protects
> - Includes a docstring linking to this bug's ticket/PR
```
This ensures the bug is guarded, not just fixed. See the Regression Testing course.

## Post-mortem generation
For high-impact bugs, CC can help draft the postmortem:
```
> Draft a postmortem for the bug we just fixed. Include:
> - Timeline (when detected, when reproduced, when fixed)
> - Root cause (technical explanation)
> - Impact (what was affected, for how long)
> - What went well
> - What could have been better
> - Action items (regression test, monitoring, prevention)
```
Post-mortems are painful to write from scratch. AI-drafted, human-edited is 5x faster.

## The bug that hunts YOU
Sometimes a bug involves systems you don't have direct access to. CC can help you frame:
- "Given this symptom, what would you ask the SRE team to check?"
- "What logs from service X would help me diagnose this?"
- "What monitoring signals would have caught this earlier?"

Debugging is a conversation with your infrastructure. CC helps you ask better questions.
"""),
        "exercises": [
            ex(
                "CC-06-1",
                "Run a test-fix loop headlessly on a real bug: `claude-code -p \"Fix the failing test X\" --allowedTools \"...\"`. Time it. Compare to your manual debugging.",
                "The headless test-fix loop is CC's biggest debugging strength.",
                "For clear-failing-test bugs: often faster than manual. For subtle bugs: still needs oversight. Learn which category your bugs fall in.",
            ),
            ex(
                "CC-06-2",
                "Use CC to generate a reproducer for a real bug (from a report, error, or symptom). Verify the reproducer actually fails against the current code.",
                "Reproducer generation is a genuine superpower.",
                "First-try reproducers work about 60% of the time. When they don't, iterate (\"the test doesn't fail — the actual failure looks like X, adjust\"). Two turns usually gets there.",
            ),
            ex(
                "CC-06-3",
                "Practice bisect-with-CC: for a repo, break a commit deliberately, then use CC + `git bisect run` to find the introducing commit automatically.",
                "Automated regression hunting.",
                "You have a reproducible fast bisect workflow. Next time production has a mystery regression from days ago, you find the commit in minutes instead of hours.",
            ),
            ex(
                "CC-06-4",
                "For your next hard bug, use Opus-thinking-high for the hypothesis phase. Compare hypothesis quality to Sonnet's for the same bug.",
                "Where deep thinking earns cost.",
                "Deep model often generates hypotheses you didn't consider. Even one novel hypothesis can save hours. This is where thinking budgets pay off — hard debugging is the ROI peak.",
            ),
        ],
    },
    {
        "id": "CC-07",
        "title": "Headless Mode Mastery",
        "level": "Claude Code Advanced",
        "summary": "Prompt engineering for headless. Verification scripts. Cron jobs. CI integration. The delegation superpower.",
        "body": md("""
## Why headless is different
Interactive lets you correct mid-flight. Headless doesn't. This changes everything:
- Prompts must be SELF-CONTAINED (no assumed context)
- Success criteria must be EXPLICIT
- Recovery paths must be BUILT IN
- Output must be VERIFIABLE

Good headless prompt engineering is a distinct skill from interactive.

## Anatomy of a great headless prompt
```
[Role / Context]
You are working in a Flask + SQLAlchemy repository. Convention: pytest for tests,
mypy for type checking, ruff for linting. See CLAUDE.md for details.

[Task]
Add cursor-based pagination to the /api/users endpoint.
- Default page size: 50, max: 500
- Backward compatible: no cursor param = first page
- Cursor is opaque base64 of last_id

[Constraints]
- Do not add new dependencies
- Do not modify unrelated endpoints
- Do not touch tests unrelated to /api/users

[Deliverable]
- Modified src/api/users.py with new pagination logic
- New src/pagination.py with cursor encode/decode
- New tests in tests/api/test_users_pagination.py (min 5 test cases)
- Updated docs/api-changelog.md under [Unreleased]

[Verification]
Run these commands. All must succeed:
- pytest tests/api/test_users_pagination.py -v
- pytest tests/api/  (ensure no regressions)
- mypy src/api/users.py src/pagination.py
- ruff check src/

If any fails, DO NOT claim completion. Report the failure with details.

[On failure]
If you cannot complete the task, stop and produce a detailed report:
- What was attempted
- What failed
- What info would help
Do NOT partially commit broken code.
```

## The verification-first mindset
Never trust "I completed the task." Trust verified output.
- Verification commands specified UP FRONT
- Success = commands pass
- Failure = report, don't guess
- Include verification as PART OF the task, not an afterthought

## Common headless invocations
### One-off tasks
```bash
claude-code -p "..." --allowedTools "read,write,bash:pytest"
```

### With session persistence
```bash
claude-code -p "..." --session-id "pagination-work-2026-09"
```
Resume later with the same session-id if you need to continue.

### JSON output for scripting
```bash
result=$(claude-code -p "..." --output-format json --allowedTools "...")
echo "$result" | jq '.status'
```
Parse structured output. Use in shell pipelines.

### Batch operations
```bash
for file in src/*.py; do
  claude-code -p "Add docstrings to all public functions in $file. \
    Do not change any function bodies. Run mypy after." \
    --allowedTools "read,write,bash:mypy"
done
```
Parallelize with `xargs -P` for speed.

## Verification scripts (external)
For complex verification, write a script:
```bash
#!/bin/bash
# verify-pagination.sh
set -e

pytest tests/api/test_users_pagination.py -v || exit 1
pytest tests/api/ -q || exit 1
mypy src/api/users.py src/pagination.py || exit 1
ruff check src/ || exit 1

# Custom checks
grep -q "cursor" src/api/users.py || exit 1
grep -q "def encode_cursor" src/pagination.py || exit 1

echo "All verifications passed"
```
Then in the CC prompt:
```
Verification: run ./verify-pagination.sh. Must exit 0.
```
Cleaner, reusable, testable independently.

## Cron / scheduled headless
For recurring tasks:
```
# /etc/cron.d/nightly-audit
0 2 * * * cd /repos/myproject && claude-code -p "$(cat prompts/nightly-audit.md)" \
  --allowedTools "read,bash:git" \
  --output-format json \
  > /var/log/cc-audit-$(date +\%s).json 2>&1
```
Runs at 2 AM. Output is machine-parseable.

Use cases:
- Nightly dependency audit
- Weekly stale PR triage
- Daily test flakiness detection
- Continuous code health metrics

## CI integration
In GitHub Actions (or equivalent):
```yaml
- name: Auto-generate release notes
  run: |
    claude-code -p "Read CHANGELOG.md's [Unreleased] section. Format
    it as GitHub release notes. Output to release-notes.md." \
    --allowedTools "read,write" \
    --output-format json > cc-output.json
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```
CC becomes a step in your CI, generating notes / drafting PRs / auditing.

## Delegation patterns
### Delegate a task
```bash
claude-code -p "$(cat tasks/refactor-legacy.md)" \
  --allowedTools "read,write,bash:pytest" \
  --max-turns 30 \
  > refactor-log.txt
```
Fire, come back later, read log.

### Delegate + PR
```bash
claude-code -p "Implement the task in tasks/foo.md. When complete,
  create a git branch, commit, and open a PR to main using gh cli. \
  PR title: <derived from task>. PR body: what/why/testing sections." \
  --allowedTools "read,write,bash:pytest,bash:git,bash:gh"
```
Task in, PR out. Human reviews the PR.

## When headless fails silently
Symptom: exits 0, but the actual work isn't complete.
Cause: prompt didn't require explicit verification.
Fix: bake verification into the prompt (as above). No verification = no completion.

## When headless drifts
Symptom: takes 20+ turns, scope explodes.
Causes:
- Task under-specified
- No `--max-turns` cap
- No verification to stop early on success
Fix: tighter task spec, `--max-turns 15`, explicit verification.

## The headless task file convention
Store recurring / template tasks as files:
```
tasks/
  add-endpoint.md
  refactor-legacy.md
  release-notes.md
  weekly-audit.md
```
Each file: role, task, constraints, deliverable, verification, on-failure.
Invoke with `-p "$(cat tasks/foo.md)"`.

Tasks-as-code. Versioned. Reviewable. Improvable.

## The cost of headless
Headless with `--max-turns 30` on Opus can be expensive. Budget:
- Set token/cost caps if the tool supports
- Model down to Sonnet unless deep reasoning needed
- Prefer many small headless tasks over one giant one (easier to review, cheaper to retry)
"""),
        "exercises": [
            ex(
                "CC-07-1",
                "Write a real headless task file (`ai-expert-lab/tasks/example.md`) with all 6 sections. Run it. Verify the output matches the deliverable spec.",
                "One good headless prompt = template for many.",
                "First try often has under-specified verification. Iterate: add explicit `pytest`, `grep`, or shell checks. Once solid, this task file becomes a template for similar tasks.",
            ),
            ex(
                "CC-07-2",
                "Write a verification script (`ai-expert-lab/verification/verify-example.sh`) that CC's task can invoke. Test that it correctly exits 0/1 for pass/fail.",
                "External verification scripts > inline commands.",
                "Reusable, testable, versionable. Same script can verify local runs, CI runs, and headless CC runs. Consistency in verification = consistency in confidence.",
            ),
            ex(
                "CC-07-3",
                "Delegate a real task headlessly with `--max-turns 15`. Read the log after. Did CC stay in scope? Did verification pass? What would you change in the prompt?",
                "Real delegation reveals prompt gaps.",
                "First delegations often hit `--max-turns` because the prompt was ambiguous. Refined prompts complete in 5-10 turns cleanly. Iteration on prompts pays off.",
            ),
            ex(
                "CC-07-4",
                "Set up a simple CI job (or cron) that runs a headless CC task. Suggestion: nightly stale-PR reporter or weekly dependency audit. Verify it runs and produces output.",
                "CC in your infrastructure.",
                "You've promoted CC from a tool to infrastructure. Scheduled AI tasks become part of your team's operations. This is the shift from 'AI assistant' to 'AI worker'.",
            ),
        ],
    },
    {
        "id": "CC-08",
        "title": "The SDK — Programmatic Claude in Pipelines",
        "level": "Claude Code Advanced",
        "summary": "When headless isn't enough. Building integrations, bots, dashboards, and custom workflows with the CC/Claude SDK.",
        "body": md("""
## When you need the SDK (vs headless)
Headless is a CLI. SDK is a library. Reach for SDK when:
- You're building software that USES Claude (bots, dashboards, integrations)
- You need STREAMING responses (real-time UIs)
- You need FINE-GRAINED error handling
- You need to integrate with non-shell environments (web servers, workers)
- You need to compose Claude with other services

## The SDK landscape (2026)
- **`@cursor/sdk`** (TypeScript) — Cursor's SDK for programmatic agent use
- **`cursor-sdk`** / **`cursor_sdk`** (Python) — Python equivalent
- **Anthropic SDK** — direct Claude API access (lower-level)

Cursor SDK is a good abstraction: it handles model routing, tool calling, streaming. Anthropic SDK is closer to the metal.

For most integrations, the Cursor SDK (or its Anthropic-flavored equivalent) is the right level.

## Minimal Python SDK example
```python
from cursor_sdk import Agent

agent = Agent.create(
    model="claude-opus-4-7-thinking-high",
    system_prompt="You are a code review assistant. Focus on correctness and clarity.",
    tools=["read", "write"],
)

result = agent.prompt(
    "Review the diff in /tmp/pr-diff.txt and suggest 3 improvements.",
    streaming=False,
)

print(result.messages[-1].content)
```

## Minimal TypeScript SDK example
```typescript
import { Agent } from '@cursor/sdk';

const agent = await Agent.create({
  model: 'claude-opus-4-7-thinking-high',
  systemPrompt: 'You are a code review assistant.',
  tools: ['read', 'write'],
});

for await (const event of agent.stream('Review the diff...')) {
  if (event.type === 'text') process.stdout.write(event.text);
  if (event.type === 'tool_call') console.log('[tool]', event.name, event.args);
}
```

## Streaming vs batch
- **Streaming**: get tokens as they arrive. Best for UIs, chatbots, interactive tools.
- **Batch**: wait for full completion. Best for scripts, background jobs.

Choose based on user experience:
- User is watching output? Stream.
- Script producing a file? Batch.

## Real use cases
### 1. PR review bot
- Webhook: PR opened
- SDK: agent reviews diff, checks style, suggests improvements
- Post: comments back on PR via GitHub API

### 2. Slack Q&A bot
- Slack event: message in a channel
- SDK: agent with tools to search your docs / codebase
- Reply: answer in-thread

### 3. Dashboard for cost/usage tracking
- Web app that queries CC/Anthropic APIs for team usage
- SDK: analyzes trends, generates weekly report

### 4. Continuous documentation
- Cron: SDK agent reads recent commits, updates CHANGELOG
- Approves via PR

### 5. Test authoring pipeline
- CI: for each new function without tests, SDK generates a test
- Opens PR with the test

## Error handling
```python
from cursor_sdk import Agent, CursorAgentError

try:
    result = agent.prompt("...", max_turns=10)
except CursorAgentError as e:
    if e.code == "rate_limit":
        # back off and retry
        ...
    elif e.code == "context_exceeded":
        # compact context and retry
        ...
    else:
        # unknown error, log and alert
        ...
```
Handle rate limits, context overflow, tool errors, model errors distinctly.

## Cost management in SDK
- Track tokens per request (SDK exposes usage stats)
- Set per-request budgets (`max_tokens`)
- Route model by request type (cheap for classification, expensive for reasoning)
- Aggregate: dashboard shows daily/weekly/monthly spend

At scale, SDK cost visibility is essential. Uncontrolled SDK use in a busy service can burn $1000s per day.

## Concurrency
SDK supports parallel agents:
```python
import asyncio

async def review_pr(pr_id):
    agent = Agent.create(...)
    return await agent.prompt_async(f"Review PR {pr_id}")

async def review_all():
    return await asyncio.gather(*[review_pr(pr) for pr in pending_prs])
```
Fan out across PRs, files, or subtasks. Fan in results.

## Session management
```python
# Persistent session across API calls
session_id = "user-123-code-review"

result1 = agent.prompt("Start review", session_id=session_id)
# ... later ...
result2 = agent.prompt("Continue review", session_id=session_id)
```
Sessions preserve context between calls. Great for chat-like UIs.

## Rate limiting and backoff
Every agentic service must handle:
- Rate limits (429s from the model provider)
- Transient errors (network, 5xx)
- Deadlines (per-request timeouts)

Use exponential backoff with jitter. Never retry indefinitely. Alert on repeated failures.

## Testing SDK code
Mock the agent for unit tests:
```python
from cursor_sdk.testing import MockAgent

def test_review_bot():
    agent = MockAgent(responses=["Great PR!", "LGTM"])
    result = my_review_bot(agent, pr_id=42)
    assert "Great PR" in result
```
Never call real agents in unit tests — flaky and expensive.

## Deployment considerations
- Store API keys in secret managers (never env vars in yaml)
- Monitor: latency, cost, error rate per endpoint
- Cache responses for identical prompts (dedup)
- Fallback: what happens if the API is down? Degrade gracefully.

## The SDK vs REST API question
Direct REST calls to Anthropic:
- Maximum control
- Minimum abstraction
- Handle streaming, tool calls yourself

SDK:
- Batteries-included
- Handles common patterns (streaming, tools, retries)
- Faster to build with

For prototyping or standard use: SDK.
For truly custom needs: REST.

## When NOT to use the SDK
- If interactive CLI or headless CC suffices, don't overbuild
- Building a script? Use headless with `--output-format json`
- One-off task? Interactive.
- Recurring but not integrated? Cron + headless.
- Actually integrated into a product? SDK.
"""),
        "exercises": [
            ex(
                "CC-08-1",
                "Install the SDK (Python or TS, your preference). Write a minimal script that: creates an agent, sends one prompt, prints the response. Verify it works.",
                "Mechanical setup. Get past the friction.",
                "You have a working SDK invocation. This is the foundation for every SDK use case. If setup was painful, note where — future you (or a teammate) will hit the same friction.",
            ),
            ex(
                "CC-08-2",
                "Build a minimal 'PR reviewer' script: reads a diff from a file, uses SDK to generate 3 review comments, prints them. Not integrated with GitHub yet — just the review logic.",
                "The core of a real integration.",
                "Working script. The GitHub webhook / posting step would be another layer. Understanding the CORE agent interaction is the value.",
            ),
            ex(
                "CC-08-3",
                "Add error handling: rate limits, context overflow, timeouts. Simulate each (block network, oversized prompt, artificial delay). Verify graceful degradation.",
                "Production-ready SDK code handles failure paths.",
                "You now have a script that would survive real production. Most SDK tutorials skip this — real integrations require it.",
            ),
            ex(
                "CC-08-4",
                "Estimate: if your PR reviewer script ran on every PR in a busy repo (say, 100 PRs/day), what would the monthly cost be? Include tokens per review + model choice + overhead.",
                "Cost math matters at scale.",
                "Sample estimate: 100 PRs × 30d × 5k tokens avg × Sonnet cost ≈ $50-100/month. Opus × 10 = $500-1000/month. Choose model with production volumes in mind, not just quality.",
            ),
        ],
    },
    {
        "id": "CC-09",
        "title": "MCP Servers — Extending Claude Code",
        "level": "Claude Code Advanced",
        "summary": "MCP is how you give Claude access to YOUR systems, tools, and data. Beyond files and bash.",
        "body": md("""
## What MCP is
**Model Context Protocol** — a standard for exposing tools and resources to AI agents. Claude Code (and Cursor) speak MCP.

Instead of "here's a file, here's bash," MCP lets you expose:
- Custom APIs (your internal services)
- Databases (query, not just SQL bash)
- Domain-specific tools (Datadog, Sentry, Linear, Slack, etc.)
- Structured resources (docs, schemas, dashboards)

An MCP server is a small program that speaks the protocol. Claude Code connects to it and gets new tools automatically.

## Why MCP matters
Without MCP, extending AI capabilities means:
- Writing shell scripts
- Configuring CLI tools
- Hoping the model figures out how to use them

With MCP:
- Tools show up as first-class capabilities
- Model knows their schemas
- Structured input/output
- Reliable, discoverable

MCP is the API layer between the AI world and your infrastructure.

## Common MCP servers (as of 2026)
- **filesystem** — controlled file access
- **git** — richer git operations
- **github** — GitHub API (issues, PRs, actions)
- **slack** — post messages, read channels
- **datadog** — query metrics and logs
- **sentry** — read errors and traces
- **linear** / **jira** — read/update tickets
- **postgres** / **mysql** — query databases
- **memory** — persistent memory across sessions
- **puppeteer** / **browser** — web automation

Ecosystem grows constantly. Check the MCP registry / Anthropic docs / Cursor's MCP marketplace.

## Setting up an MCP server
CC config (usually `~/.claude/mcp.json` or similar):
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    }
  }
}
```
Restart CC. Tools appear.

Cursor has similar config (per-workspace or global). Check Cursor's MCP settings UI.

## When to add an MCP server
Ask: "Am I frequently pasting X into prompts?" — then X should probably be an MCP tool.
- Repeatedly pasting error IDs from Sentry → add Sentry MCP
- Manually querying Postgres for the same tables → add Postgres MCP
- Copying Linear ticket details → add Linear MCP

## Building a custom MCP server
For your organization's internal systems:
```typescript
// minimal MCP server
import { Server } from '@modelcontextprotocol/sdk/server';

const server = new Server({ name: 'my-internal-api' });

server.tool('search_incidents', {
  description: 'Search incident tickets by keyword',
  parameters: { query: 'string', limit: 'number' },
  handler: async ({ query, limit }) => {
    return await internalApi.searchIncidents(query, limit);
  },
});

server.start();
```
Package as a small binary or npm/pip package. Deploy internally. Tell teammates to add it to their MCP config.

## Security considerations
MCP servers can be POWERFUL. They can:
- Query production databases
- Modify tickets
- Post to Slack
- Deploy code

For each MCP tool, ask:
- Read-only or read-write?
- Production data or dev/staging?
- Who has access to invoke this via AI?
- Is there an audit trail?

Same discipline as any API you'd expose to a bot. Because that's what you're doing.

## Least-privilege MCP setup
- Read-only Postgres by default; separate read-write MCP for cases needing it
- Sentry MCP scoped to specific projects, not all-projects
- GitHub MCP with a PAT limited to specific repos
- Never expose admin-level tools broadly

## MCP + rules
Your CLAUDE.md / AGENTS.md should mention available MCP tools:
```
## Available tools (via MCP)
- github: fetch PRs, issues, workflow status
- sentry: search errors, get stack traces
- postgres (readonly): query app_prod.* tables

When answering questions about production behavior, prefer querying
these directly over guessing.
```
Model uses tools better when it knows they exist.

## MCP debugging
When an MCP tool doesn't work:
- Check server logs (usually stderr)
- Verify env vars/credentials
- Test the server standalone (not through CC)
- Update to latest version

MCP is an evolving protocol; occasional version mismatches. Keep tools updated.

## The MCP ROI question
For each candidate MCP server:
- Setup cost: 30 min - 2 hours
- Per-use benefit: seconds to minutes saved per invocation
- Break-even: 10-50 uses

If a tool would be used 10+ times, MCP is usually worth it. Once for setup, forever for use.

## MCP anti-patterns
### Anti-pattern: exposing everything
"Let's add every MCP server we can find." Result: model overloaded, security risk.
Fix: add MCPs deliberately. Prune unused ones.

### Anti-pattern: write access to production
MCP tool that can modify prod data + interactive agent = accidents waiting.
Fix: strict least-privilege. Prefer read-only for prod.

### Anti-pattern: no audit
MCP tools invoked frequently, no logs of who / what / when.
Fix: MCP server logs every invocation. Weekly review.

### Anti-pattern: stale credentials
PAT expires; MCP silently fails; model works around by hallucinating.
Fix: monitor MCP health; alert on failures; rotate credentials on schedule.

## The team-level MCP standard
For teams:
- Centralize MCP configs (versioned in a shared repo)
- Standard set of servers everyone has
- Onboarding: install standard MCPs
- Deprecation: retire unused ones
- Custom MCPs for internal systems, versioned in the team's tooling repo

MCP becomes infrastructure. Not per-person hackery.
"""),
        "exercises": [
            ex(
                "CC-09-1",
                "Install one MCP server (suggested: GitHub or filesystem). Verify Claude Code recognizes the new tools. Use them in a session.",
                "First MCP is the friction. After that: easy.",
                "You see new tools in the CC session (e.g., `github_get_pr`, `github_list_issues`). Try one. Note: the model uses them naturally without you having to explain.",
            ),
            ex(
                "CC-09-2",
                "For your workflow, identify 3 tasks where you frequently paste data into prompts (Sentry errors, Slack messages, DB query results). Which of these has an existing MCP? Which would justify a custom MCP?",
                "MCP ROI audit.",
                "Common wins: Sentry, Datadog, GitHub, Slack. Custom MCPs earn keep for internal tools used 20+ times/week. Don't build custom for one-off tasks.",
            ),
            ex(
                "CC-09-3",
                "Design (on paper, in `ai-expert-lab/mcp-design.md`) a custom MCP server for one of your internal systems. Include: tool names, parameters, security scope, audit strategy. Don't build yet — just design.",
                "Design before code.",
                "Good MCP design > good MCP code. Spec what tools you'd expose, why, what the model would gain. If the design isn't compelling, don't build. If it is, building is straightforward.",
            ),
            ex(
                "CC-09-4",
                "Write MCP hygiene guidance in `ai-expert-lab/mcp-policy.md`: what MCPs are approved, which are read-only vs read-write, who audits them, credential rotation cadence. Even for solo use, having a policy prevents sprawl.",
                "Governance for MCP.",
                "Sample policy: 'Approved: github, sentry, slack. Read-only in prod, read-write in staging. Credentials rotate quarterly. Weekly log review.' Discipline prevents 'why does the AI have prod DB write access?' incidents.",
            ),
        ],
    },
    {
        "id": "CC-10",
        "title": "Claude Code + CI: Automated Reviews, Tests, Release Notes",
        "level": "Claude Code Advanced",
        "summary": "CC as a CI participant: reviewing PRs, generating tests, drafting release notes, auditing for regressions.",
        "body": md("""
## The premise
CI is where automation lives. Adding CC to CI = adding intelligence to your pipelines. Not for everything, but for tasks where structured AI output beats scripting.

## High-ROI CC-in-CI patterns

### Pattern 1: PR reviewer bot
```yaml
- name: AI review
  run: |
    diff=$(gh pr diff ${{ github.event.pull_request.number }})
    echo "$diff" | claude-code -p "$(cat .github/prompts/review.md)" \
      --allowedTools "read" \
      --output-format json > review.json
    # Parse and post as PR comment
    node scripts/post-review.js review.json
```
Prompt in `.github/prompts/review.md`:
```
Review this diff for:
- Correctness bugs
- Missing edge cases
- Missing tests
- Style violations we care about (see AGENTS.md)

For each finding, output JSON:
{ "file": "...", "line": N, "severity": "issue|nit|question", "text": "..." }
```
Every PR gets an AI first-pass review. Complements human reviewers.

### Pattern 2: Test authoring
```yaml
- name: Ensure new functions have tests
  run: |
    new_funcs=$(git diff origin/main..HEAD --name-only | grep '\.py$' | \
      xargs -I{} python scripts/find_new_funcs.py {})
    if [ -n "$new_funcs" ]; then
      claude-code -p "For each new public function in the following, \
        write a pytest test. Files: $new_funcs. Save tests alongside." \
        --allowedTools "read,write,bash:pytest"
    fi
```
New functions without tests get tests added automatically. Human reviews the auto-added tests.

### Pattern 3: Release note drafting
```yaml
- name: Draft release notes
  if: github.event_name == 'release'
  run: |
    commits=$(git log v${{ steps.prev.outputs.tag }}..HEAD --oneline)
    echo "$commits" | claude-code -p "Draft release notes in Keep-a-Changelog format \
      from these commits. Group by Added/Changed/Fixed/Deprecated." \
      --output-format text > release-notes.md
    gh release edit ${{ github.event.release.tag_name }} \
      --notes-file release-notes.md
```

### Pattern 4: Regression triage
```yaml
- name: Analyze test failures
  if: failure()
  run: |
    log=$(cat test-output.log)
    echo "$log" | claude-code -p "Analyze this test failure. \
      Identify the most likely root cause. Suggest 3 places to investigate." \
      --output-format text
    # Optionally post as PR comment
```
Failed CI runs get instant AI analysis. Sometimes CC identifies the fix before you look.

### Pattern 5: Documentation sync
```yaml
- name: Update API docs from code
  run: |
    changed=$(git diff --name-only | grep 'api/')
    if [ -n "$changed" ]; then
      claude-code -p "The API code changed in these files: $changed. \
        Read the changes and update docs/api-reference.md accordingly. \
        Match the existing doc style." \
        --allowedTools "read,write"
    fi
```
Docs never drift from code. Human reviews the auto-updates.

## The CI cost consideration
CC in CI runs per push. Costs add up:
- 100 PRs/day × 5k tokens per review × Sonnet = ~$5-10/day = $150-300/month
- Same on Opus = 5x more

Budget:
- Prefer Sonnet or Haiku for high-volume tasks
- Opus only when reasoning depth is critical
- Cache when possible (identical diffs get same reviews — cache by diff hash)
- Rate-limit per user/repo if it explodes

## Safety in CI
- CI runs with the CI's credentials. Scope PATs tightly.
- Never let CI CC modify main directly (require PRs)
- Log all CC invocations to a monitored channel
- On unusual behavior (5x normal tokens, weird outputs), alert

## The prompt library
For each CC-in-CI task, prompts live in the repo:
```
.github/prompts/
  review.md
  test-generation.md
  release-notes.md
  regression-triage.md
```
Versioned. Reviewable. Improveable. Discoverable.

## The human-in-loop principle
Even automated CC output should have human review points:
- AI review → posted as suggestion, human decides
- Auto-generated test → PR opened, human merges
- Release notes → drafted, human publishes
- Doc updates → PR opened, human merges

Never auto-merge AI output to main. Automate the DRAFTING, not the DECISION.

## The CI-CC feedback loop
When AI output is wrong (bad review, wrong test, hallucinated docs):
1. Log the failure
2. Update the prompt
3. Deploy the updated prompt
4. Monitor: are failures decreasing?

Prompts in CI are software. They regress. They improve. Treat them as such.

## Cursor Bugbot vs custom CI CC
- **Cursor Bugbot** — turnkey PR review. Zero setup. Good enough for many teams.
- **Custom CI CC** — full control, custom prompts, integrates with your stack. More setup.

Start with Bugbot. Graduate to custom when you need customization Bugbot doesn't offer.

## The AI-CI report card
Monthly, review:
- Cost per task type
- Accept rate (how often do humans keep AI suggestions?)
- False positive rate (how often is AI wrong?)
- Cycle time reduction (are PRs merged faster?)

Adjust: turn off low-value AI tasks. Double down on high-value ones.

## What NOT to automate in CI
- Anything requiring human judgment where the cost of being wrong is high
- Deployment decisions
- Security responses
- User-facing content that hasn't been reviewed
- Anything the team hasn't agreed should be automated

"Just because you can" is not "you should."
"""),
        "exercises": [
            ex(
                "CC-10-1",
                "Set up Bugbot (or the equivalent Cursor / CC review bot) on your repo. Compare its findings on 3 PRs to human reviewer findings.",
                "Establish the baseline before customizing.",
                "Bugbot typically catches 60-80% of what a careful human reviewer would. Misses project-specific conventions unless configured. Good complement to human review; not a full replacement.",
            ),
            ex(
                "CC-10-2",
                "Design a custom CC-in-CI task for your team. Write the prompt in `.github/prompts/<task>.md`. Draft the workflow YAML. Don't deploy yet — just design.",
                "Design > implementation.",
                "Good CI CC design specifies: trigger, allowlist, output format, human-review point, cost estimate. Bad design ('run CC on every push') sprawls into cost and noise.",
            ),
            ex(
                "CC-10-3",
                "For an existing CI job that has a manual step (e.g., someone drafts release notes, someone triages failures), estimate: would AI automation save time? At what quality trade-off?",
                "ROI evaluation for AI automation.",
                "Rule of thumb: if the manual task takes >15 min and happens weekly+, AI drafting saves real time. If quality bar is very high (customer-facing content), AI + human review still beats human alone. If quality bar is life-critical (deploys, security), manual only.",
            ),
            ex(
                "CC-10-4",
                "Write in `ai-expert-lab/ci-ai-policy.md`: your team's (or personal) policy for AI in CI. What's allowed to run? What must have human review? Budget caps?",
                "Governance for CI AI.",
                "Sample: 'AI reviews on all PRs (Sonnet). AI drafts release notes and docs (Sonnet, human approves). No auto-merge. Cost budget: $200/mo for CI AI tasks combined. Prompts versioned in .github/prompts/. Monthly cost + accept-rate review.' Discipline scales.",
            ),
        ],
    },
    # ─────────────────────────── PHASE 3: CROSS-CUTTING ───────────────────────────
    {
        "id": "X-01",
        "title": "Cursor vs Claude Code — The Decision Tree",
        "level": "Cross-cutting",
        "summary": "Both are excellent. Neither is universally better. When to reach for each, per task.",
        "body": md("""
## The false dichotomy
"Which is better, Cursor or Claude Code?" is the wrong question. The right question is: "For THIS task, in THIS context, which one wins?"

Expert use = both, chosen deliberately.

## Cursor's strengths
- **IDE-native** — you're already coding in Cursor; AI is one keystroke away
- **Visual diff review** — side-by-side, easy to accept/reject
- **Tab completion in flow** — micro-suggestions without breaking rhythm
- **Multi-model at fingertips** — dropdown to switch
- **Composer** — precision multi-file edits with visual scope control
- **Cloud agents / Bugbot** — polished PR-integrated automation
- **Visual navigation** — file tree, jump to symbol, etc.

## Claude Code's strengths
- **Terminal-native** — where much dev work already lives (SSH, remote servers, tmux)
- **Headless mode** — scriptable, CI-friendly, cron-able
- **SDK** — programmatic integration into products/tools
- **CLAUDE.md hierarchy** — clean project + directory scoping
- **Extended thinking** — deep reasoning cues (`ultrathink`, budgets)
- **`--allowedTools` explicit** — security-conscious defaults
- **Session persistence** — resume across days
- **Fewer clicks** — pure keyboard flow for terminal natives

## Where each shines (task by task)
| Task | Cursor | Claude Code | Notes |
|------|--------|-------------|-------|
| Active feature dev in an IDE | ✓✓ | ✓ | IDE context wins |
| Terminal-heavy work (SSH, servers) | | ✓✓ | GHD not available |
| PR review (structured) | ✓✓ (Bugbot) | ✓ (headless in CI) | Both work |
| Delegated batch work | ✓ (cloud agents) | ✓✓ (headless) | CC's specialty |
| SDK integration | ✓ | ✓✓ | CC has stronger SDK story |
| Quick file edits | ✓✓ (Tab, Inline) | ✓ | IDE wins |
| Long refactor with review | ✓✓ (Composer) | ✓ | Visual diff crucial |
| Debugging (interactive) | ✓✓ | ✓✓ | Both good, personal preference |
| Debugging (headless test-fix) | ✓ | ✓✓ | CC's test loop is strong |
| Deep architectural design | ✓✓ | ✓✓ | Model matters more than tool |
| Log analysis (pipe from CLI) | ✓ | ✓✓ | CC integrates with pipes naturally |
| Automation / cron | ✓ | ✓✓ | CC headless designed for this |
| Team-standardized workflows | ✓ | ✓ | Whichever you standardize on |

## The context-of-use axis
Where's your body?
- **In the IDE actively coding** → Cursor is closer
- **In a terminal running commands** → CC is closer
- **On a remote server via SSH** → CC (Cursor doesn't run there easily)
- **In a browser reviewing a PR** → GitHub UI + Bugbot / Cursor's PR features
- **On mobile** → both have some mobile presence; check specific versions

Optimize for the FEWEST context switches.

## The task shape axis
- **Interactive iteration** — either works; personal preference
- **One-shot execution** — CC headless is purpose-built
- **Long-running background** — CC (persistent shell) or Cursor cloud agents
- **Integrated into product** — CC SDK is more mature at time of writing

## The model access axis
Both tools access most major models. Where they differ:
- Cursor's `Composer` fast model — not exposed in CC
- CC's extended thinking cues (`ultrathink`, etc.) — Cursor equivalent varies by version
- Grok / GPT models via Cursor — sometimes better UX than direct APIs

Usually: models are equivalent across tools. The tool difference is UX and integration.

## The team axis
Teams often standardize:
- "We use Cursor for interactive, CC for CI." (common split)
- "We use CC everywhere for consistency." (terminal-heavy teams)
- "We use Cursor everywhere; CC only for headless." (IDE-heavy teams)

Standardization reduces cognitive load. But allow individuals to use the other for tasks it clearly wins.

## When to use BOTH in one task
A common expert pattern:
1. **Cursor** — plan interactively with Ask + Plan modes
2. **Cursor** — begin implementation in Agent mode
3. **CC** — for a headless batch sub-task (e.g., "add tests to these 20 files")
4. **Cursor** — review the sub-task's output in the IDE, integrate
5. **CC** in CI — automated review of the resulting PR

Not overkill — each tool at its strength.

## The switching cost
Real switching costs:
- Context lost when moving tools (unless artifacts are file-based)
- Cognitive tax of different UIs
- Occasional divergence in rules (`.cursor/rules/` vs `CLAUDE.md`)

Minimize by:
- Always save plans as files, not just chat
- Standardize on AGENTS.md as cross-tool spec
- Use `git commit` as the checkpoint between tool sessions

## The one-tool discipline (contrarian view)
Some engineers deliberately use ONE tool for months to master it, then adopt the other. Rationale: two half-mastered tools < one fully-mastered tool.

Reasonable path:
- Months 1-3: master Cursor
- Months 4-6: master Claude Code
- Month 7+: expert with both, route per task

Better than trying to learn both simultaneously and mastering neither.

## The routing card revisited
```
CONTEXT           RECOMMENDATION
─────────────────────────────────────────────────────────────
Coding in IDE  →  Cursor (Ask/Plan/Agent/Composer/Inline/Tab)
Terminal / SSH →  Claude Code (interactive or headless)
CI / cron      →  Claude Code (headless)
Bot / product  →  Claude Code (SDK) or Cursor SDK
PR review      →  Cursor Bugbot OR Claude Code in CI
Batch scripts  →  Claude Code (headless with a shell loop)
Deep design    →  Either — model + prompt matter more
```
This is your default routing. Deviate with justification.
"""),
        "exercises": [
            ex(
                "X-01-1",
                "For your typical work week, list 10 recurring AI-assisted task types. For each, note: current tool, ideal tool per this module. Where does your practice diverge from the ideal?",
                "Audit for potential re-routing.",
                "Common realization: 'I use Cursor for cron-like batch tasks because I never learned CC headless. Switching would save 30% of my automation time.' Concrete adjustments follow.",
            ),
            ex(
                "X-01-2",
                "Deliberately do a task that's mid-workflow tool-switching: Cursor for plan, CC headless for batch sub-task, Cursor for integration. Time it. What was the overhead of switching?",
                "Feel the cost and value of switching.",
                "Switching overhead is ~2-5 min per switch. Value depends on task fit. If switching saves 20+ min, worth it. If it saves 5 min, break-even or worse.",
            ),
            ex(
                "X-01-3",
                "Try the 'one-tool for a week' discipline. Pick the tool you use LESS. Use only it (except emergencies) for a week. Note: what did you struggle with? What surprised you?",
                "Immersion accelerates learning.",
                "Typical: first 2 days painful, muscle memory rebels. Day 3-5: patterns emerge. Day 6-7: comfort. This is how experts get both tools to expert level — not simultaneously.",
            ),
            ex(
                "X-01-4",
                "Write in `ai-expert-lab/tool-routing.md`: your personal defaults for tool per task type. Include the exceptions (when you'd break your own default). Reuse.",
                "Explicit routing = defensible choices.",
                "Sample: 'Default IDE work: Cursor. Default headless: CC. Exception: if I'm in tmux+ssh (which is often), CC even for interactive. Exception: SDK work always CC.' Personal, reasoned, iterable.",
            ),
        ],
    },
    {
        "id": "X-02",
        "title": "Hybrid Daily Workflows",
        "level": "Cross-cutting",
        "summary": "A real day in the life of an expert who uses both Cursor and Claude Code. Handoffs, transitions, cognitive load.",
        "body": md("""
## A representative expert day
This is illustrative — YOUR day will differ. The RHYTHMS are what matter.

### 9:00 — Morning triage
- Terminal: `gh pr list --author=@me --state=open` (see my open PRs)
- CC headless (running from cron overnight): read summary of yesterday's build failures
- Cursor: open the top-priority PR for the day, `git fetch`, checkout branch

### 9:30 — First deep work session
- Cursor IDE: Ask mode with Opus-thinking. Design question for a new feature.
- Iterate on the design 4-5 turns.
- Save design decisions to `docs/design/feature-x.md` (a file).
- Switch to Plan mode. Draft implementation plan referencing the design doc.
- Save plan to `docs/plans/feature-x.md`.

### 10:30 — Execute the plan
- Cursor Agent mode with Sonnet. "Execute the plan at docs/plans/feature-x.md."
- Watch progress. Interrupt at first checkpoint to review approach.
- Continue. Small commits as Agent hits checkpoints.
- When Agent finishes: manual review of the diff.

### 12:00 — Lunch + delegate batch task
- Before leaving: kick off CC headless in a tmux session:
  ```bash
  claude-code -p "$(cat tasks/add-docstrings.md)" \\
    --allowedTools "read,write,bash:mypy" \\
    --max-turns 40 > docstring-run.log &
  ```
- Come back after lunch to check.

### 13:00 — Return, check delegated work
- `tail -100 docstring-run.log` — did it complete? Any issues?
- If clean: `git diff | head -100` — spot check. Open PR.
- If not clean: read the failure log, decide: retry with refined prompt, or manually finish.

### 14:00 — Debug session
- Bug reported by QA: pagination inconsistent under load.
- Cursor Ask (Opus-thinking): pin the bug report + relevant code. "Propose 5 hypotheses."
- Cursor Agent: "Write a reproducer test for hypothesis 3."
- Test fails. Confirms hypothesis 3.
- Cursor Inline: fix the specific line.
- Cursor Agent: "Run the reproducer. If passes, run the full pagination test suite."
- Green.
- Cursor Agent: "Add a regression test with a descriptive name. Commit."

### 15:30 — Code review
- PR from teammate open in browser.
- Cursor: open the PR branch locally.
- Cursor Ask (Sonnet): "Review the diff for correctness bugs, missing edge cases, tests."
- Cross-reference AI findings with my own read.
- Post review comments on GitHub (some directly from AI's structured output).

### 16:30 — Documentation
- CC interactive (Sonnet): "Update docs/api-reference.md to reflect the pagination changes from feature-x. Match existing style."
- Review the doc diff.
- Commit.

### 17:00 — End of day cleanup
- Check `/cost` for CC usage today
- Check Cursor cloud agent status (any results waiting?)
- Kick off overnight CC job: "Run the full slow test suite. Report any regressions."
- Commit any final WIP to a branch. Push.
- `git status` clean. Done.

## The rhythms embedded above
- **Plan → Save → Execute**: plans are files, not chat
- **Right tool per phase**: Cursor for interactive coding, CC for batch/scheduled
- **Right model per phase**: Opus-thinking for design/debug, Sonnet for execution
- **Delegation over blocking**: kick off batches during natural breaks
- **Explicit verification**: never trust "done" without tests green

## The tool-switching etiquette
Between tools:
- **File-based handoff**: always. Chat context evaporates; files persist.
- **Commit-based checkpoint**: `git commit` before switching. If the other tool wanders, revert is easy.
- **Explicit reference**: when using tool B, reference the plan/artifact from tool A by file path.

## Common daily patterns
### Pattern: Design in Cursor, batch in CC
- Cursor for interactive design (visual)
- CC headless for the resulting batch of mechanical work
- Cursor to review the batch's output

### Pattern: Plan once, execute headless
- Cursor Ask/Plan interactively
- CC headless executes the plan without further interaction
- You do other work while it runs
- Come back, review

### Pattern: Interactive debug, headless verify
- Cursor for hypothesis + fix (interactive)
- CC headless to run full test suite as final verification
- Report back

### Pattern: Fast CC for pipe work, Cursor for design
```bash
cat huge-log.txt | claude-code -p "extract errors, group by root cause" > errors.md
```
Then open `errors.md` in Cursor for design work.

## What NOT to do daily
- **Don't context-switch tools every 5 minutes.** Batch tool use.
- **Don't leave both tools running with the same task.** They fight.
- **Don't skip the commit between tools.** Ambiguous state = pain.
- **Don't ignore the delegated background jobs.** Check periodically.
- **Don't run cursor/cc calls in a loop without cost check.** $500 nights happen.

## The cognitive load management
Two tools + multiple models = a lot to track. Reduce load:
- One primary IDE window at a time (not 5)
- Named tmux windows (`design`, `debug`, `batch`) for CC sessions
- Written todo list for what's delegated
- End-of-day review to close loops

If cognitive load is high, you're probably parallelizing too much. Cut back to 2-3 concurrent AI tasks max.

## The team rhythm
On teams, coordinate:
- Who's running the nightly CC batches?
- What CI CC tasks are running per PR?
- Cost dashboard visible to the team
- Weekly review: what worked, what didn't

Team-level AI hygiene prevents individual chaos from scaling.
"""),
        "exercises": [
            ex(
                "X-02-1",
                "For one real work day, JOURNAL every AI interaction in `ai-expert-lab/journal-day-1.md`. Time, tool, mode, model, task, outcome. At end of day, review: what was efficient, what was wasted?",
                "Audit by observation.",
                "Typical: 50-100 AI interactions in a working day. Distribution reveals patterns. Common findings: too much time in one mode, tool mismatches, unnecessary model tier changes. Data > memory.",
            ),
            ex(
                "X-02-2",
                "Practice a full-day workflow with intentional Cursor+CC hybrid: design in Cursor, delegate batch in CC, review in Cursor, verify in CC-CI. Note handoffs and their overhead.",
                "Real hybrid day.",
                "Handoff overhead is small when using files. Handoff overhead is large when relying on chat context. File-based artifacts are the key ergonomic decision.",
            ),
            ex(
                "X-02-3",
                "Design your ideal daily routine in `ai-expert-lab/daily-routine.md`: when do you plan, when do you execute, when do you delegate, when do you review. Even a rough sketch helps.",
                "Explicit routine > ad-hoc.",
                "Routines beat willpower. Even a rough sketch ('mornings: deep work + Cursor; afternoons: review + CC batches') anchors your day. Adjust weekly as you learn what fits your rhythm.",
            ),
            ex(
                "X-02-4",
                "Try a 'no context switch' hour: pick ONE task, ONE tool, ONE model. Stay in it. Notice how flow feels vs your usual bouncing.",
                "Depth beats breadth in an hour block.",
                "Typical realization: uninterrupted single-tool work is MUCH more productive than the illusion of parallelism from switching. Block deep-work hours; use tool-switching for lower-value periods.",
            ),
        ],
    },
    {
        "id": "X-03",
        "title": "The Expert Mode/Model/Tool Routing Playbook",
        "level": "Cross-cutting",
        "summary": "15+ real scenarios with recommended routing. Reference this often.",
        "body": md("""
## How to use this playbook
For each scenario: recommended tool, mode, model, and why. These are STARTING POINTS. Your context may shift the answer.

## Scenario 1: Add a new REST endpoint (routine)
- Tool: **Cursor** (IDE-native)
- Mode: **Agent** (execution)
- Model: **Sonnet / balanced**
- Why: pattern exists in the codebase; agent expands it; visual review of the diff.
- Anti-choice: Opus-thinking (overkill), Ask-only (why not execute?).

## Scenario 2: Add a new REST endpoint (novel — no pattern exists)
- Tool: **Cursor**
- Mode: **Ask → Plan → Agent**
- Model: **Opus-thinking (planning), Sonnet (execution)**
- Why: novel design; needs planning first.

## Scenario 3: Refactor a 400-line file into 5 files (structure only, no behavior change)
- Tool: **Cursor**
- Mode: **Ask (design the split) → Composer (execute)**
- Model: **Sonnet (design), Balanced Composer (execution)**
- Why: multi-file coordinated edit; Composer's sweet spot.

## Scenario 4: Debug a subtle race condition
- Tool: **Either** (personal preference)
- Mode: **Ask (hypothesize) → Agent (test loop)**
- Model: **Opus-thinking-high (hypothesis), Sonnet (verify)**
- Why: hypothesis quality dominates; deep model earns cost here.

## Scenario 5: Fix an obvious typo
- Tool: **Cursor**
- Mode: **Inline edit** (Cmd/Ctrl+K)
- Model: **Fast**
- Why: tiny scope; overhead of any bigger workflow is wasted.

## Scenario 6: Rename a symbol across 40 files
- Tool: **Cursor** (LSP rename + Composer for semantic sprawl)
- Mode: **Composer** for semantic follow-up (docs, comments)
- Model: **Fast Composer**
- Why: mechanical; fast model handles patterns cheaply.

## Scenario 7: Generate 20 endpoints from an OpenAPI spec
- Tool: **Claude Code (headless)** or Cursor Agent with the spec pinned
- Mode: **Headless with a script** (CC) or **Agent** (Cursor)
- Model: **Sonnet**
- Why: bounded, repeatable, scriptable. CC headless slightly favored for bulk.

## Scenario 8: Design a new microservice's API
- Tool: **Cursor** (or CC — either works)
- Mode: **Ask (design) → Plan (formalize)**
- Model: **Opus-thinking-high**
- Why: pure design, no execution yet; deep reasoning is where ROI is highest.

## Scenario 9: Review a teammate's 800-line PR
- Tool: **Cursor** (with the branch checked out) OR **Cursor Bugbot** (automated)
- Mode: **Ask on diff** (interactive) OR Bugbot (automated)
- Model: **Sonnet**
- Why: structured analysis; Sonnet is enough; Opus overkill.

## Scenario 10: Write test cases for a new function
- Tool: **Cursor** (interactive) or **Claude Code** (headless if generating for many functions)
- Mode: **Agent** (Cursor) or headless (CC)
- Model: **Sonnet**
- Why: pattern-based; not novel; balanced model suffices.

## Scenario 11: Generate release notes from git log
- Tool: **Claude Code** (headless in CI)
- Mode: **Headless** with `-p`
- Model: **Sonnet**
- Why: structured, scriptable, one-shot.

## Scenario 12: Research a new library / framework you're evaluating
- Tool: **Either**
- Mode: **Ask** (with docs pinned)
- Model: **Sonnet or Opus** (depends on depth)
- Why: pure information-gathering; no code changes; Ask is the mode.

## Scenario 13: Investigate a mystery CI failure
- Tool: **Claude Code** (log analysis in terminal) or **Cursor** (if you want IDE context)
- Mode: **Ask** with logs pinned, then **Agent** if it becomes a test-fix loop
- Model: **Opus-thinking (hypothesis), Sonnet (execute fix)**
- Why: hard debugging; deep model on the hypothesis pays off.

## Scenario 14: Draft a design document
- Tool: **Cursor** (write the doc alongside code) or **CC** (terminal preference)
- Mode: **Ask → write to a file**
- Model: **Opus-thinking**
- Why: high-value written artifact; deep reasoning improves quality.

## Scenario 15: Bulk update: bump copyright year in all files
- Tool: **Claude Code (headless)** or shell script + AI review
- Mode: **Headless with a bash-heavy allowlist**
- Model: **Haiku**
- Why: fully mechanical; cheapest model.

## Scenario 16: Post-mortem for a production incident
- Tool: **Cursor** or **CC** — either
- Mode: **Ask** (with logs, timeline, code pinned)
- Model: **Opus-thinking-high**
- Why: high-stakes analysis; deep reasoning; one-shot draft, then edit.

## Scenario 17: Add error handling to a function
- Tool: **Cursor**
- Mode: **Inline edit** (single function) or **Agent** (multiple functions)
- Model: **Sonnet**
- Why: mechanical but context-dependent; balanced model.

## Scenario 18: Explain unfamiliar code to yourself
- Tool: **Either**
- Mode: **Ask** with the code pinned
- Model: **Sonnet**
- Why: comprehension task; no execution needed.

## Scenario 19: Migrate deprecated API usages across the codebase
- Tool: **Claude Code (headless)** for bulk, **Cursor Composer** for precise
- Mode: **Composer** (Cursor) or **Headless with allowlist** (CC)
- Model: **Sonnet**
- Why: pattern-based, bounded, verifiable via test suite.

## Scenario 20: Weekly stale-PR triage
- Tool: **Claude Code (headless in cron)**
- Mode: **Headless with GitHub MCP**
- Model: **Sonnet**
- Why: recurring, structured, automatable.

## The playbook doctrine
- These are DEFAULTS. Override with reason.
- YOUR playbook will diverge from this one based on your work.
- Print YOUR playbook. Reference it. Refine it.

## How playbooks evolve
Once a month:
- Review your recent tasks
- Which routings worked? Which didn't?
- Update playbook entries
- Add scenarios that recur enough to deserve a slot

Your playbook after 6 months looks nothing like the starter. That IS the point.
"""),
        "exercises": [
            ex(
                "X-03-1",
                "Copy this playbook into `ai-expert-lab/routing-playbook.md`. Personalize: cross out defaults you disagree with, add your own scenarios. This is now YOUR reference.",
                "Personalize before using.",
                "Your playbook diverges from the starter based on YOUR work. That divergence IS the expertise emerging. Reread and refine monthly.",
            ),
            ex(
                "X-03-2",
                "For your NEXT 10 real tasks, consult the playbook before starting. Note when the playbook was right, when your instinct differed, and why.",
                "Feedback loop for the playbook.",
                "Typical: playbook right 70-80% of the time. Divergences reveal either playbook improvements or task-specific context the playbook doesn't capture. Both feed refinement.",
            ),
            ex(
                "X-03-3",
                "Add 5 scenarios to your playbook that are specific to YOUR domain (DSP, embedded, audio, whatever). What tools/modes/models fit YOUR common tasks?",
                "Domain-specific routing.",
                "Sample DSP scenarios: 'Golden vector generation → CC headless + Python spec.' 'MATLAB → C port → Cursor Composer with side-by-side.' Your domain has specifics; capture them.",
            ),
            ex(
                "X-03-4",
                "Compare playbooks with a colleague (if possible) or public expert content. Where do you agree? Where do you disagree? Reconciling teaches you why your defaults are what they are.",
                "External input calibrates internal defaults.",
                "You articulate WHY you chose a specific routing. Sometimes the exercise reveals the choice was arbitrary — worth revisiting. Sometimes it confirms the choice was reasoned.",
            ),
        ],
    },
    {
        "id": "X-04",
        "title": "The Expert Debugging Protocol (Both Tools)",
        "level": "Cross-cutting",
        "summary": "The unified 7-step debugging protocol, using Cursor and CC as complementary weapons.",
        "body": md("""
## The protocol (recap)
```
1. REPRODUCE — reliably failing case
2. ISOLATE   — minimal input that fails
3. HYPOTHESIZE — what could cause this?
4. VERIFY   — cheap tests of each hypothesis
5. FIX      — implement correct fix
6. GUARD    — regression test
7. LEARN    — capture the insight
```
Each step has tool + mode + model recommendations.

## Step 1: REPRODUCE
### Goal
A test or command that fails reliably. Without this, everything downstream is guessing.

### Tools
- **Cursor Ask** (with the bug report / logs pinned): "Based on this evidence, propose 3 reproducer scenarios."
- **Claude Code** (if the reproducer needs the terminal): "Write a script that triggers this behavior."
- Model: **Sonnet** usually; **Opus** if the symptom is very vague.

### Deliverable
A reproducer command / script / test that FAILS every time on current code.

### Failure signals
- "It happens intermittently" — you don't have a reproducer yet. Keep looking.
- "It happened once and I can't get it back" — collect more context, don't guess.

## Step 2: ISOLATE
### Goal
The SMALLEST reproducer. Removes noise, speeds iteration.

### Tools
- **Claude Code Agent** (headless with test-fix loop): "Reduce this reproducer to the minimum that still fails."
- **Cursor Agent**: same, interactive.
- Model: **Sonnet**.

### Deliverable
A minimal failing test / script (often 5-20 lines).

### Anti-pattern
Debugging a 500-line reproducer for hours. Isolate first. Every minute of isolation saves 10 minutes of debugging.

## Step 3: HYPOTHESIZE
### Goal
5+ plausible root causes, ranked. Best done with a deep-thinking model.

### Tools
- **Cursor Ask** or **CC Ask**: pin minimal reproducer + relevant source + relevant logs.
- Model: **Opus-thinking-high** — this is where deep reasoning pays off most.

### Prompt (template)
```
Given:
- Reproducer: <pin file>
- Relevant code: <pin files>
- Relevant logs: <pin logs>
- Symptom: <description>

Think really carefully. Propose 5 hypotheses for the root cause.
For each:
1. Specific mechanism (which line, which state, which race)
2. Evidence supporting it (from the artifacts above)
3. Evidence AGAINST it (would there be no bug if this were true?)
4. Cheapest experiment to confirm or refute
5. Likelihood (1-10)

Rank by likelihood. Note any that seem 8+.
```

### Deliverable
Ranked hypothesis list, each with a specific verification experiment.

## Step 4: VERIFY
### Goal
Test each hypothesis cheaply. Confirm or refute.

### Tools
- **Cursor Agent** (interactive) or **CC** (headless): "Run the experiment for hypothesis 1: add a log at line X, rerun, report the output."
- Model: **Sonnet** (execution).

### Discipline
- Test ONE hypothesis at a time (don't add 5 logs and lose track)
- Move on quickly when refuted (don't force a favorite hypothesis to be right)
- Update hypothesis rankings as evidence comes in

### Deliverable
Confirmed root cause. One hypothesis validated by evidence.

## Step 5: FIX
### Goal
The correct fix, no more, no less.

### Tools
- **Cursor Inline** (small fix) or **Composer** (fix touches multiple files).
- Model: **Sonnet**.

### Discipline
- Small diff (a bug fix diff should usually be < 20 lines)
- No unrelated changes (no "while I'm here, let me refactor")
- Preserve behavior for cases the bug DIDN'T affect

### Deliverable
A minimal diff that fixes the specific bug.

## Step 6: GUARD
### Goal
A regression test that fails against pre-fix code, passes against fixed code.

### Tools
- **Cursor Agent** or **CC**: "Add a regression test that fails against the buggy code and passes now."
- Model: **Sonnet**.

### Naming
Descriptive, references the bug:
```python
def test_regression_pagination_returns_correct_count_at_page_boundary():
    \"\"\"Guards fix for #234: cursor decoding was off-by-one at page boundary.\"\"\"
    ...
```

### Deliverable
A committed regression test. See the Regression Testing course for the full discipline.

## Step 7: LEARN
### Goal
Capture the insight so this class of bug doesn't return.

### Tools
- **Either** tool — you write markdown.
- Model: none needed (or Sonnet for drafting).

### Outputs
- Update `AGENTS.md` / `CLAUDE.md` if the bug revealed a non-obvious constraint
- Add a rule to `.cursor/rules/` if AI should have prevented it
- Add a comment near the fix explaining WHY
- For high-impact bugs: post-mortem in `docs/postmortems/`

### The one-line lesson
Every debug session ends with: "Next time we see X, we should Y." That's the learning.

## The tool split (illustrated)
```
Step 1 REPRODUCE  →  Cursor Ask / CC             (Sonnet)
Step 2 ISOLATE    →  CC headless / Cursor Agent  (Sonnet)
Step 3 HYPOTHESIZE →  Cursor Ask / CC Ask         (Opus-thinking-high)  ★
Step 4 VERIFY     →  Cursor Agent / CC           (Sonnet)
Step 5 FIX        →  Cursor Inline / Composer    (Sonnet)
Step 6 GUARD      →  Cursor Agent / CC           (Sonnet)
Step 7 LEARN      →  Either (write markdown)     (Sonnet or none)
```
★ = where deep-thinking model earns its cost.

## The tempo
- Simple bugs (typo, off-by-one with a clear reproducer): 15-30 min
- Medium bugs (misunderstanding of a library, minor state issue): 1-2 hours
- Hard bugs (races, subtle numerical, distributed): half a day to a day
- Genuine mysteries (why is this even possible?): unbounded — set a budget

## The debug budget
Before starting: "I'll spend N minutes."
At exhaustion:
- If close: extend by half
- If far: STOP. Write up what you know. Sleep on it or hand off.
- Coming back fresh (or a colleague) often produces the insight.

The unbounded debug session is a productivity killer. Bounded sessions with hand-offs beat solo grinding.

## Anti-patterns to catch yourself
- Skipping REPRODUCE ("I'll just try a fix")
- Skipping HYPOTHESIZE ("I know what's wrong")
- Skipping GUARD ("I'll add the test later")
- Not LEARNING ("It's fixed, moving on")

Every skip has a specific cost. GUARD skips create returned bugs. HYPOTHESIZE skips waste hours. REPRODUCE skips make you chase ghosts.
"""),
        "exercises": [
            ex(
                "X-04-1",
                "For your next 3 real bugs (of any complexity), follow the 7-step protocol EXPLICITLY. Note tool + model per step. Compare total time to your usual approach.",
                "The protocol IS the training.",
                "Typical: first 1-2 uses feel slower. By bug 3, faster than ad-hoc and higher-quality (regression tests, learnings captured). Compounding value.",
            ),
            ex(
                "X-04-2",
                "For your next hard bug, invest in HYPOTHESIZE: pin all relevant context, use Opus-thinking-high, generate 5+ hypotheses. Compare quality to your usual first-instinct.",
                "See where deep thinking earns cost.",
                "Deep model often includes 1-2 hypotheses you'd never consider. Even if wrong, they widen your search space. The right one is often not the obvious one.",
            ),
            ex(
                "X-04-3",
                "Adopt the debug budget: before starting a bug, set a time. When it hits, stop and reassess. Track: how often does the budget prevent you from wasting hours?",
                "Bounded debugging.",
                "Common: 30% of the time, hitting the budget without solving leads to a fresh-eyes solution within an hour. Unbounded grinding hits diminishing returns fast.",
            ),
            ex(
                "X-04-4",
                "Write in `ai-expert-lab/debug-protocol.md`: your personal 7-step protocol adapted to your tools and stack. Include the specific prompts, models, and tools for each step.",
                "Personalized > generic.",
                "After 10 uses, your protocol is battle-tested. Sharing with team creates common language. Different bugs still follow the same discipline, just with different specifics per step.",
            ),
        ],
    },
    {
        "id": "X-05",
        "title": "Capstone: Run a Complex Feature Through the Full Pipeline",
        "level": "Expert",
        "summary": "Apply every module. Ship a complex feature using both tools, all modes, right models, and the debug protocol.",
        "body": md("""
## The capstone challenge
Take a genuinely complex feature. Ship it end-to-end using both Cursor and Claude Code as complementary tools, with explicit mode/model routing at each step.

Suggested feature (pick one or invent):
- Add real-time notifications to an existing app (backend + frontend)
- Migrate a subsystem from synchronous to async (with backward compat)
- Add an AI-assisted feature to a product (using SDK)
- Refactor a legacy module into modern architecture (with safety net)
- Build a small internal tool that scratches a real itch

## The required disciplines
### 1. Written plan (Phase 1)
- Use Ask + Plan modes with deep-thinking model
- Save as `capstone/plan.md`
- Iterate 3 passes (draft → refine → stress-test)
- Include: files, order, risks, tests, non-goals, effort estimate

### 2. Cross-tool execution (Phase 2)
- Use Cursor for interactive design and IDE-native coding
- Use Claude Code for AT LEAST ONE headless batch task
- Handoffs are file-based (plans, specs, verification scripts)
- Explicit mode + model per step (logged in a journal)

### 3. Debugging encountered (Phase 3)
- At least ONE bug must be caught via tests (not shipped broken)
- Debug protocol applied (all 7 steps)
- Regression test added for the caught bug

### 4. Rules + docs updated (Phase 4)
- Any non-obvious constraints discovered → updated `AGENTS.md` / `CLAUDE.md` / `.cursor/rules/`
- Feature documented in project docs
- CHANGELOG entry

### 5. CI + PR (Phase 5)
- Feature branch, PR opened
- CI green (tests, lint, type check)
- PR description mentions plan + verification
- Merged (self-approve OK if solo)

### 6. Journal (Phase 6)
- `capstone/journal.md` — timestamps, tool+mode+model per major step, decisions, deviations
- End with a written retrospective

## The acceptance criteria (10 items, self-scored 1-3)
- [ ] Plan file exists, iterated 3 passes, references risks and non-goals
- [ ] Both Cursor AND Claude Code used (headless CC at least once)
- [ ] Mode + model chosen deliberately per step (journal proves it)
- [ ] At least one bug caught in testing (not after merge)
- [ ] Debug protocol applied when bugs found (7 steps in journal)
- [ ] Regression test added for the caught bug(s)
- [ ] AGENTS.md / CLAUDE.md / rules updated with lessons learned
- [ ] CI green on the PR
- [ ] Journal documents tool/model choices with reasoning
- [ ] Retrospective identifies what worked, what didn't, what changes for next time

Target: ≥ 24/30. Below 20 → address weak areas before declaring done.

## The mindset shift
You started thinking: "I use Cursor. Sometimes I use Claude Code."
You leave thinking: "I have a routing protocol. I use the right tool + mode + model per phase. My plans are files. My debugs follow a discipline. My AI use is engineering, not folklore."

That IS expertise.

## The reflection questions
In `capstone/retrospective.md`, answer:
1. **Tool routing**: did the tool-per-phase actually help, or was it ceremony? Where did it clearly win?
2. **Model routing**: when did deep-thinking pay off? When was it wasted?
3. **Planning**: how did the plan artifact hold up during execution? What deviations happened?
4. **Debugging**: how much time did the protocol save vs your usual approach?
5. **What surprised you**: the biggest "huh, I didn't expect that" moment.
6. **What you'd change**: for the next complex feature, what will you do differently?

## Where to go next (post-capstone)
- **Master the SDK**: build one real integration (bot, dashboard, workflow tool)
- **Author team standards**: your team's routing playbook, prompt library, CLAUDE.md conventions
- **Automate more**: replace weekly manual chores with headless CC in cron
- **Teach**: run a workshop for teammates. Their questions refine your understanding.
- **Study a related domain**: agentic AI systems, MCP server authoring, prompt optimization

## The single most important habit you leave with
**Before opening any AI tool: articulate the task type, choose the mode, choose the model, choose the tool. Every time. Until it's automatic.**

Everything else in this course was elaboration on that one habit.
"""),
        "exercises": [
            ex(
                "X-05-1",
                "Choose your capstone feature. Draft a scope statement in `capstone/scope.md`: what will be shipped, what won't, what success looks like. This is the anchor for everything.",
                "Scope defines success.",
                "Well-scoped capstone finishes in 1-2 weeks of part-time work. Over-scoped capstones drag or get abandoned. Under-scoped: doesn't stress the disciplines enough. Aim for genuinely complex but bounded.",
            ),
            ex(
                "X-05-2",
                "Phase 1: Plan. Draft, iterate 3 passes, save as `capstone/plan.md`. Include everything the discipline requires. Time this phase — expect 30-90 min.",
                "Front-load the thinking.",
                "Well-iterated plan often surfaces risks or reshapes scope. Common: after pass 3, you realize a subtask can be deleted or a completely different approach is cleaner. Time invested here is time NOT wasted in execution.",
            ),
            ex(
                "X-05-3",
                "Phase 2: Execute across tools. Journal every major step. Ensure at least one headless CC batch task. Aim for 5-8 tool/mode transitions across the feature.",
                "Cross-tool discipline in real work.",
                "Feel where tool switches genuinely help vs where they're ceremony. This calibrates future work — you'll know when to switch and when to stay put.",
            ),
            ex(
                "X-05-4",
                "Phase 3: When bugs arise (they will), apply the 7-step debug protocol EXPLICITLY. Journal each step. Add regression tests.",
                "Debugging discipline under real pressure.",
                "Real bugs teach faster than staged exercises. Following the protocol under pressure builds real habits. Regression tests protect the fix forever.",
            ),
            ex(
                "X-05-5",
                "Phase 4-5: Update rules/docs/AGENTS.md with lessons. Open PR. Verify CI green. Merge.",
                "Ship it.",
                "Feature in main. Rules updated. Docs updated. Tests protect it. PR history shows the work. This is what shipping looks like at expert level.",
            ),
            ex(
                "X-05-6",
                "Phase 6: Retrospective. `capstone/retrospective.md`. Score against the 10 acceptance criteria. Write the reflection questions honestly.",
                "Reflection cements learning.",
                "Score honestly. Weak areas identified. Retrospective document is now a personal reference — reread in 6 months to see how far you've moved.",
            ),
            ex(
                "X-05-7",
                "Compare your capstone journal to your self-assessment from Module 00. Where have you moved on the novice → expert gradient?",
                "Bookend measurement.",
                "Concrete evidence of movement. If little movement: the course didn't stick — pick 2-3 modules to redo more deliberately. If big movement: you've earned the expert label.",
            ),
        ],
    },
    # ────────────────────── DRILLS ──────────────────────
    {
        "id": "drills",
        "title": "Daily Drills",
        "level": "All levels",
        "summary": "Quick reps to build routing/planning/debugging fluency. One per day, 5-10 minutes.",
        "body": md("""
## How to use drills
One per day, in addition to modules or after the course. Each takes 5-10 minutes. Repetition builds fluency.
"""),
        "exercises": [
            ex("D-01", "Before your next AI task today, ARTICULATE (aloud or in a note): task type + mode + model + tool. Do this for every task today.", "The habit is the whole game.", "One day of articulation shifts your defaults. A week makes it automatic."),
            ex("D-02", "Write a plan for something you'd normally 'just do.' Save it as a file. Reference it during execution.", "Plans-as-files habit.", "Even small tasks benefit from 60 seconds of planning. Compounds massively over time."),
            ex("D-03", "In your next CC session, `/model` switch mid-task to a different tier when the sub-task warrants. Consciously.", "Model switching muscle memory.", "Feels awkward first few times. Becomes natural like changing gears in a car."),
            ex("D-04", "Use Cursor Ask mode (not Agent) for a research question. Save the useful answer to a doc.", "Not everything needs execution.", "You'll notice tasks you were mis-routing to Agent when Ask was the answer."),
            ex("D-05", "Delegate ONE task to CC headless. Write the prompt with all 6 sections. Come back to results.", "Headless delegation rep.", "Weekly delegation habit reduces context-switching costs and expands throughput."),
            ex("D-06", "Run Bugbot (or Cursor's local review) on a change before committing. Address findings before human review.", "Pre-review saves face.", "Human reviewer sees a cleaner diff. Your review cycles shorten. Compounds."),
            ex("D-07", "Debug a bug using the 7-step protocol EXPLICITLY. Journal each step. Note which step took longest.", "Protocol under real pressure.", "Time distribution reveals bottlenecks. Usually: HYPOTHESIZE if you skimp on deep model, or VERIFY if you try too many things at once."),
            ex("D-08", "Update AGENTS.md / CLAUDE.md with ONE lesson learned this week.", "Rules refinement habit.", "Small weekly updates > big quarterly rewrites. Rules stay current, useful, tight."),
            ex("D-09", "Check `/cost` in CC or Cursor's Usage panel. Note trends. Any surprises?", "Cost visibility.", "Data-informed budget decisions. Nobody's a good spender without visibility."),
            ex("D-10", "Try a mode or tool you use LESS. For one task. Feel the difference.", "Skill breadth.", "Comfort with all tools means real routing, not lock-in. Weekly variety keeps skills fresh."),
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
  <title>Advanced AI Use in Modern Hi-Tech Projects</title>
  <style>
:root {
  --bg: #0b1020;
  --surface: #131b30;
  --surface2: #1c2540;
  --text: #e7ecf5;
  --muted: #98a5c0;
  --accent: #4f46e5;
  --accent2: #06b6d4;
  --warn: #f59e0b;
  --ok: #10b981;
  --border: #2a3454;
  --ex: #172038;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); line-height: 1.55; }
a { color: var(--accent2); }
.layout { display: grid; grid-template-columns: 320px 1fr; min-height: 100vh; }
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
nav.sidebar button.module-link.active {
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  color: #fff; font-weight: 600;
}
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
main { padding: 1.5rem 2rem 4rem; max-width: 960px; }
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
  background: #05081a; border: 1px solid var(--border); border-radius: 8px;
  padding: 0.85rem 1rem; overflow-x: auto; font-size: 0.82rem;
}
.lesson code { background: var(--surface2); padding: 0.1rem 0.35rem; border-radius: 4px; font-size: 0.88em; }
.exercise {
  background: var(--ex); border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
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
button.btn-primary { background: var(--accent); color: #fff; }
button.btn-ghost { background: var(--surface2); color: var(--text); }
button.btn-ok { background: #065f46; color: #ecfdf5; }
.exercise.done { border-left-color: var(--ok); opacity: 0.92; }
.solution {
  display: none; margin-top: 0.85rem; padding: 0.85rem; background: #05081a;
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
          Open in any browser. Progress saves locally. <strong>%%TOTAL%% exercises</strong>
          across Cursor advanced, Claude Code advanced, cross-cutting routing/debug/capstone, and daily drills.
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
const STORAGE_KEY = 'ai-expert-tooling-course-v1';

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
        "title": "Advanced AI Use in Modern Hi-Tech Projects",
        "subtitle": "Part 1: Cursor · Part 2: Claude Code · Cross-cutting: routing, debug protocol, capstone",
        "version": "2026.09",
        "modules": MODULES,
    }
    total = sum(len(m.get("exercises", [])) for m in MODULES)
    data_json = json.dumps(course, ensure_ascii=False)
    page = HTML_TEMPLATE.replace("%%DATA%%", data_json).replace("%%TOTAL%%", str(total))
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT} - {len(MODULES)} modules, {total} exercises")


if __name__ == "__main__":
    main()
