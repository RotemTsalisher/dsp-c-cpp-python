# Advanced AI Use in Modern Hi-Tech Projects

**Format:** Standalone HTML course (spa-course), 28 modules, 120 exercises.
**Level:** Expert. Not for beginners.
**Prerequisites:** You already use Cursor and/or Claude Code daily. You've written prompts, accepted diffs, reviewed AI-generated PRs. You want to stop being a *user* and start being an *operator*.
**Target audience:** Senior/staff engineers, tech leads, engineering managers embedding AI into real product work.

## What This Is
A judgment-and-routing course, not a mechanics course. The premise:

> Anyone can type a prompt. Experts choose the right **mode × model × context × tool** for the task at hand, and know when to abandon an approach.

The existing `cursor-course` and `claude-code-course` in this repo cover zero-to-hero mechanics. This course starts where those end: **when do you use Plan mode vs Ask mode vs Agent mode? When is Opus-thinking-high worth it vs Composer-fast? When do you delegate to a Cloud agent vs stay local? When do you use Claude Code headless vs interactive? How do you debug an AI-generated regression at 2 AM?**

## Structure (4 phases)

| Phase | Modules | Focus |
|-------|---------|-------|
| **0. Foundations** | 00–01 | What expert-level AI use actually means; the unified mode × model × context × tool mental model |
| **1. Cursor Advanced** | C-01 – C-10 | Mode landscape, model selection, planning discipline in Plan mode, Ask-mode interrogation, methodical Agent execution, `.cursor/rules` + `AGENTS.md`, Cloud agents, debugging with thinking models, CI integration (Bugbot/reviewers), Composer parallelism |
| **2. Claude Code Advanced** | CC-01 – CC-10 | Mode landscape (interactive/headless/SDK), model selection + thinking budgets, `CLAUDE.md` hierarchy, plan-first workflows (`ultrathink`), execution discipline with `--allowedTools` / `--max-turns`, debugging protocol, headless mastery, SDK (TS + Python), MCP servers, CI integration |
| **3. Cross-cutting** | X-01 – X-05 | Cursor vs Claude Code decision tree, hybrid daily workflows, the routing playbook (matrix), universal debugging protocol, capstone (ship a real feature end-to-end using both tools with correct routing) |
| **Drills** | drills | 10 five-minute daily reps to build routing reflexes |

## How to Open
Double-click `index.html`. Runs in any browser. Progress saves to `localStorage` under `ai-expert-tooling-course-v1`.

## How to Regenerate
```bash
python generate_course.py
```
Rewrites `index.html` from the module data. Edit `generate_course.py` to change content.

## Toolbox for Exercises
- **Cursor** (latest) with all modes available (Ask, Plan, Agent, Composer, Inline, Tab, Cloud, Bugbot)
- **Claude Code** CLI (`claude` command) — interactive + headless (`-p`) + SDK
- **Cursor SDK** — TypeScript (`@cursor/sdk`) or Python (`cursor-sdk`) for at least the SDK modules
- **A real repository** you own — the capstone requires shipping an actual PR. Ideally a project with >5k LoC, tests, and CI.
- **GitHub account** with a repo you can protect + wire Actions to
- **API access** to at least one thinking-tier model (Opus / GPT-5-thinking / Grok-thinking) — you cannot do the deep-thinking modules with fast models alone

## Design Choices
- **Judgment over syntax.** Every exercise is "given situation X, which mode/model would you choose and why?" — then verify against the reveal.
- **Anti-patterns are first-class.** Half of expert use is knowing what *not* to do (auto-accept in agent mode without tests, using Opus for a rename, letting the model plan its own plan).
- **Both tools, honestly.** No tool tribalism — Cursor and Claude Code each win specific tasks; the routing playbook (X-03) makes it explicit.
- **Real projects only.** Toy examples don't teach when to trust an agent unattended. Exercises assume you have a real codebase to try things on.
- **Indigo/cyan visual** — distinct from every other course in this repo.

## Not Covered (Deliberately)
- Mechanics of Cursor or Claude Code from scratch (see `cursor-course` and `claude-code-course`)
- General prompt engineering theory (this is about *tool operation*, not prompt-writing tricks)
- Model-provider comparisons at a marketing level (we care about *which model for which task*, not benchmarks)
- Vibe-coding a full app in one prompt (this course teaches the opposite habit)
- LangChain / autonomous agent frameworks (out of scope — those are for building AI products, not for shipping engineering work)

## How to Study This Course
1. Do phases **in order**. Foundations (00–01) sets the mental model everything else relies on.
2. Cursor phase and Claude Code phase are independent — do them in either order once foundations are done.
3. **Cross-cutting (X-01 – X-05) must be last** — it assumes you know both tools well.
4. Every module has 4–5 exercises. Don't reveal until you've written down your own answer.
5. Run the drills (10) daily for two weeks after finishing. Routing is a *reflex*, not a lookup.
6. Capstone (X-05) — ship a real, non-trivial PR using both tools correctly routed. If you can't ship it, you're not done.

## Success Criteria
You have completed this course when, for any given engineering task, you can name in under 10 seconds:
- Which tool (Cursor / Claude Code / both / neither)
- Which mode within that tool
- Which model tier + thinking budget
- What context you'll load first
- What your success signal is
- When you'll abandon and re-route

If you still default to "open Cursor, type prompt, hope for the best" — you haven't finished the course yet.
