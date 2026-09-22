# Git + GitHub via GitHub Desktop — Zero to Hero

**Format:** Standalone HTML course (spa-course), 32 modules, 160 exercises.
**Primary tool:** GitHub Desktop (GHD). CLI shown only when GHD cannot do the thing (Module 23).
**Prerequisites:** None. Assumes zero prior Git/GitHub/version-control knowledge.

## What This Is
The full path from "I've never used version control" to "I confidently use branches, PRs, CI, branch protection, and drop to CLI only when needed."

Primary target is GitHub Desktop as the daily driver. Git command-line is treated as an escape hatch for the 10% of tasks GHD cannot do (interactive rebase, reflog recovery, `git add -p`, bisect, submodules, etc.).

GitLab is not covered — GitHub Desktop only works with GitHub. If you need GitLab, most concepts transfer but the tool would be a different GUI (GitLab's own, GitKraken, SourceTree, or CLI).

## Modules (9 phases)
| Phase | Modules | Focus |
|-------|---------|-------|
| **1. Foundations** | 00–04 | Install, sign in, what VCS is, Git's mental model, GitHub the platform, GHD tour |
| **2. First repo** | 05–08 | Create locally & publish / clone from GitHub, change→stage→commit cycle, writing commits, publish/push |
| **3. Existing repos** | 09–11 | Clone, fetch vs pull vs sync, reading history (log/diff/blame) |
| **4. Branching** | 12–16 | Why branches, create/switch/delete in GHD, merge, conflict resolution, merge vs rebase |
| **5. Collaboration** | 17–20 | PRs from GHD, reviewing PRs, forks & upstream, issues/labels/milestones |
| **6. Undoing & safety** | 21–23 | Discard/revert/reset/amend, stashing & rewrite warnings, when to drop to CLI |
| **7. Real workflows** | 24–26 | Feature branch (GitHub Flow), tags/releases/semver, .gitignore/.gitattributes/LFS |
| **8. GitHub platform** | 27–29 | Branch protection & CODEOWNERS, GitHub Actions (first CI), secrets/environments/deploy keys |
| **9. Capstone** | 30 | Ship a real project end-to-end with 10-item acceptance criteria |
| **Drills** | drills | 10 five-minute daily reps |

## How to Open
Double-click `index.html`. Runs in any browser. Progress saves to `localStorage` under `git-github-desktop-course-v1`.

## How to Regenerate
```bash
python generate_course.py
```
Rewrites `index.html` from the module data. Edit `generate_course.py` to change content.

## Toolbox for Exercises
- **GitHub Desktop** (`desktop.github.com`) — primary tool
- **GitHub.com account** (free tier works for everything)
- **Git CLI** — for the CLI escape-hatch modules (23) and drills
- **A text editor** (VS Code, Sublime, whatever) — for editing files and resolving conflicts

The course sets up a working repo called `git-lab` (in Module 05) and uses it throughout — every exercise writes into `git-lab/` or creates additional practice repos alongside it.

## Design Choices
- GHD-first: every mechanical exercise uses GHD's UI. CLI shown only in Module 23 and drills.
- Concept-heavy: modules 01–04, 06, 12, 16, 21–23 are theory before mechanics.
- Real workflow: capstone in Module 30 ships a real project through PRs + CI + branch protection + a v1.0.0 release.
- Visual: uses GitHub's own dark theme colors (purple accent) — distinct from other courses in this repo.
- Language-independent: works for any programming language (or none — for docs, prose, config repos).

## Not Covered (Deliberately)
- GitLab (different platform, use CLI or GitLab's own GUI)
- Bitbucket
- Advanced Git internals (packfiles, delta compression, object DB)
- Submodules (Module 23 mentions them; separate deep-dive would be its own course)
- Git worktrees (Module 23 mentions; not core zero-to-hero)
- Enterprise SSO / SAML setups
