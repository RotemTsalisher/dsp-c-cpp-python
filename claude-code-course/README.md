# Claude Code Zero → Hero (Embedded DSP)

Interactive course for embedded / DSP engineers using **Claude Code** — Anthropic's **terminal-native** agentic coding tool.

## What makes this course different

Every module and exercise is designed around **Claude Code's unique advantages**:

| Claude Code Feature | Cursor Equivalent | Course Module |
|---|---|---|
| Terminal `>` prompt (CLI-first) | IDE panel | 01, 02 |
| `y`/`Y`/`n` permission gate | Auto-apply with undo | 03, 11 |
| `/compact`, `/clear`, `/cost` | No direct equivalent | 04, 09 |
| `/init` (auto-gen CLAUDE.md) | Manual `.mdc` rule creation | 04, 06 |
| `CLAUDE.md` hierarchy (root + subdir) | `.cursor/rules/*.mdc` | 06 |
| Agentic build→error→fix loop in terminal | IDE agent with terminal panel | 07 |
| Headless mode (`-p` flag) | No equivalent | 11, 14 |
| Works over SSH / Docker / tmux | Requires GUI | 12 |
| Pipe stdin/stdout (`cat \| claude`, `claude \| grep`) | No equivalent | 11, 16 |
| Session cost tracking (`/cost`) | No equivalent | 04, 09 |

## Start

1. Open **`index.html`** in Chrome, Edge, or Firefox.
2. Work through modules **00 → 19** in order; use **Daily Drills** between sessions.
3. Create a sibling folder **`dsp-sandbox`** and do every exercise in a real terminal.

## Prerequisites

- **Node.js 18+** — required to install Claude Code CLI
- **A terminal** — that's it. No IDE required. (VS Code extension is optional.)
- **gcc / cmake** — for building C/C++ exercises
- **Python 3.9+** — for golden vector generation

## Regenerate (optional)

```bash
python generate_course.py
```

Progress is stored in your browser (`localStorage`), not in files.

## Contents

- **21 modules** · **87 exercises** with **Reveal solution** / **Mark complete**
- Progression: Pre-Setup → Beginner → Intermediate → Advanced → Expert → Daily Drills
- Every exercise exploits a terminal-native Claude Code feature — not generic "AI assistant" tasks
