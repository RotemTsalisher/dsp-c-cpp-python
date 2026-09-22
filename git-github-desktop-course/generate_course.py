#!/usr/bin/env python3
"""Generate index.html — Git + GitHub via GitHub Desktop, from Zero to Hero.
GitHub Desktop is the primary tool. CLI shown only when GHD cannot do the thing."""
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
        "title": "Setup: Install GitHub Desktop, Sign In",
        "level": "Setup",
        "summary": "Install the app, create a GitHub account, sign in, verify. Zero prior knowledge assumed.",
        "body": md("""
## What you will end up with
- GitHub Desktop installed on your machine
- A free GitHub.com account
- GitHub Desktop signed in and able to see your GitHub account
- A tiny "hello world" repository that proves it all works

That is enough scaffolding for every other module in this course.

## Step 1: Install GitHub Desktop
1. Open a browser. Go to `https://desktop.github.com/`.
2. Click **Download for Windows** (or macOS, if you are on a Mac).
3. Run the installer. On Windows it is a `.exe`. On macOS it is a `.dmg`.
4. When it finishes, GitHub Desktop opens automatically.

That is the entire install. No configuration to think about yet.

## Step 2: Create a GitHub.com account (if you do not have one)
1. In a browser: `https://github.com/signup`.
2. Enter email, password, username. Free plan is fine — everything in this course works on free.
3. Verify your email (they send a code).

Note the difference:
- **GitHub Desktop** = the app on your computer (the GUI)
- **GitHub.com** = the website where your projects live
- **GitHub the company** = the people behind both

You need an account on GitHub.com even if you only ever plan to use the Desktop app.

## Step 3: Sign GitHub Desktop into your GitHub account
1. First time you open GitHub Desktop, it prompts to sign in.
2. Click **Sign in to GitHub.com**.
3. Browser opens. Approve the request.
4. Back in the app, enter your name and email (used for commit authorship).
5. Click **Finish**.

Now the app can talk to your GitHub account.

## Step 4: Verify with a smoke test
- File → New Repository
- Name: `hello-git`
- Local path: pick anywhere sensible (e.g., `Documents/repos/`)
- Check "Initialize this repository with a README"
- Click **Create Repository**

You should see:
- A new folder on disk at `Documents/repos/hello-git/`
- GitHub Desktop showing this repo as the current one
- A "History" tab with one initial commit already in it

Delete `hello-git` at the end — it was just a sanity check. We build the real first repo in Module 05.

## Step 5: Also install Git CLI (optional but recommended)
GitHub Desktop bundles its own Git internally. But you will occasionally want the command-line `git` for things GHD does not cover (Module 23).
- Windows: `https://git-scm.com/download/win` — installer, all defaults are fine.
- macOS: run `git --version` in Terminal; it prompts to install Command Line Tools.

Verify:
```bash
git --version
```
Should print something like `git version 2.43.0`. Any recent 2.x version is fine.

## Where things live on disk
When you create a repository through GitHub Desktop, it makes a normal folder with your code AND a hidden `.git/` subdirectory that stores the entire history. Everything Git knows about the project lives in `.git/`. Never delete or manually edit `.git/` — that is where all the version-control magic lives.
"""),
        "exercises": [
            ex(
                "00-1",
                "Install GitHub Desktop. Verify it opens. Note the version (Help → About).",
                "Just follow the installer defaults.",
                "You have the app installed and know its version. If updates come out, you know where to look. Nothing to commit yet.",
            ),
            ex(
                "00-2",
                "Create a free GitHub.com account (or confirm the one you already have works — go to `github.com/settings/profile`).",
                "GitHub is free for public repos AND private repos on the free tier.",
                "Account exists, email verified, you can log in. Note your username — it is part of every URL to your repositories (`github.com/YOUR-USERNAME/repo-name`).",
            ),
            ex(
                "00-3",
                "Sign GitHub Desktop into your GitHub account. Confirm it can see your account (top-right corner shows your avatar).",
                "File → Options → Accounts (Windows), or GitHub Desktop → Preferences → Accounts (macOS).",
                "GHD shows your username. If a browser prompt failed, you can also use a Personal Access Token: `github.com/settings/tokens` → generate classic token → paste into GHD sign-in.",
            ),
            ex(
                "00-4",
                "Create a throwaway repo `hello-git` locally through GHD (Initialize with README). Verify: the folder exists on disk, GHD shows one commit in History, `.git/` folder exists (may be hidden — enable 'show hidden files' in your file manager).",
                "This proves everything is wired up.",
                "You now know: (a) GHD can create local repos, (b) they live as normal folders, (c) `.git/` is where Git stores its brain. This is a smoke test — delete `hello-git` after.",
            ),
            ex(
                "00-5",
                "Install Git CLI. In a terminal / PowerShell, run `git --version`. Note the version.",
                "You will not use CLI much in this course — but it is your escape hatch for Module 23.",
                "Any 2.x version is fine. GitHub Desktop uses its OWN bundled git internally, so the CLI version does not have to match — they are independent.",
            ),
        ],
    },
    {
        "id": "01",
        "title": "What Version Control Is (And Life Without It)",
        "level": "Beginner",
        "summary": "Before Git: files named report_v2_FINAL_actualfinal_v3.docx. This module explains what version control actually solves.",
        "body": md("""
## The problem, expressed as filenames
Without version control, projects look like this:
```
proposal.docx
proposal_v2.docx
proposal_v2_edits.docx
proposal_v2_FINAL.docx
proposal_v2_FINAL_v2.docx
proposal_v2_FINAL_actualfinal.docx
proposal_v2_FINAL_actualfinal_alice_edits.docx
proposal_v2_FINAL_actualfinal_alice_edits_MERGED.docx
```
Every one of us has lived through this. It is a symptom of humans manually doing what version control does automatically.

## What version control is
A **version control system (VCS)** is software that:
- Records every change you make to a set of files
- Lets you go back to any previous state
- Lets multiple people work on the same files without stepping on each other
- Answers "what changed, when, and why?" for every line of every file

Instead of `report_v2_final.docx`, you have ONE file. The history of every version is stored automatically. You can view any old version instantly.

## The four things a VCS gives you
### 1. History
Every change to every file, forever. You can see:
- Who wrote each line
- When they wrote it
- What the file looked like a year ago
- What changed between any two moments

### 2. Undo (real undo)
Not the "Ctrl+Z that only goes back 20 steps" — real undo that reaches back to the day the project started.
- Made a mistake? Restore the file to how it was yesterday.
- Broke the whole project? Restore the entire project to any moment in the past.

### 3. Branches — parallel universes
Try an experimental change WITHOUT touching your main version. If it works: merge it in. If it flops: throw it away, and your main version was never touched.

### 4. Collaboration
Multiple people can edit the same files at the same time. The VCS figures out how to combine everyone's changes. When it can't figure it out automatically, it asks a human to resolve the conflict — but 95% of the time, it is automatic.

## Types of version control
- **Centralized** (SVN, Perforce): one big server holds the history. Every operation talks to the server.
- **Distributed** (Git, Mercurial): every user has a FULL copy of the entire history. You can commit, branch, and read history WITHOUT internet.

Git is distributed. This is a superpower — on a plane, offline, on a bad connection, you can still do 90% of your work. Only pushing/pulling needs the internet.

## What Git is not
- Not a backup system (though it is often used as one). A backup is a bit-for-bit copy stored elsewhere. Git tracks CHANGES.
- Not automatic. You decide WHEN to save a version (called a **commit**). Git does not save every keystroke.
- Not a document editor. It works with files that already exist on your disk. You use whatever editor you like.

## Why "distributed" matters
On a centralized system, if the server is down, work stops. On Git:
- Your entire history is on your laptop
- You can commit, branch, view history, diff, rebase — all offline
- When you get internet again, you sync with the shared server (GitHub) in a single operation

This is why Git wins the modern world of software development.
"""),
        "exercises": [
            ex(
                "01-1",
                "In one paragraph, describe the LAST time you dealt with a `_v2_final_actualfinal` situation (in code, documents, whatever). What was the pain? How would version control have helped?",
                "Everyone has a story here.",
                "Common pattern: 'lost track of which version was current, restored wrong file, teammate overwrote my changes.' Version control eliminates all three by having ONE file with a full recorded history.",
            ),
            ex(
                "01-2",
                "Look at any folder you use for a real project. Count the number of files whose names contain 'v2', 'final', 'copy', or a date. That count is the amount of manual version control you have been doing. Note it.",
                "This is a diagnostic, not a fix.",
                "Typical count on a working directory: 5-30. All of those disappear once the project is in Git. The mental overhead of remembering 'which one is the current one' disappears too.",
            ),
            ex(
                "01-3",
                "In your own words (1-2 sentences each), explain the four things a VCS gives you: history, undo, branches, collaboration.",
                "The names are a good starting point.",
                "History: complete change record forever. Undo: restore any past state. Branches: try changes in a parallel universe without risk. Collaboration: multiple people edit safely. If you can explain these four things, you understand WHY Git exists.",
            ),
            ex(
                "01-4",
                "Distributed vs centralized: name ONE situation where distributed (Git) wins hard.",
                "Think about connectivity, speed, or independence.",
                "Best answer: 'On a plane with no internet, I can still commit, branch, and view history — I only need internet for pushing to GitHub at the end.' Also good: 'I don't lose ability to work if the shared server is down.'",
            ),
        ],
    },
    {
        "id": "02",
        "title": "Git's Mental Model: Commits, Branches, Remotes, HEAD",
        "level": "Beginner",
        "summary": "The five concepts you need in your head to use Git confidently. Learn these once — they never change.",
        "body": md("""
## The five concepts
Once these are in your head, every Git operation makes sense. Skip this module and everything else will feel like magic — bad magic.

### 1. Working directory
Your files as they appear in the folder right now. What you edit in your text editor. The current state.

### 2. Commit
A **snapshot** of ALL your project's files at one moment in time, PLUS:
- A message describing what changed
- The author's name and email
- A timestamp
- A pointer to the previous commit ("parent")

A commit is FROZEN. Once made, it never changes. The history is a chain of these snapshots, each pointing to its parent.
```
[initial] ← [commit A] ← [commit B] ← [commit C]  ← YOU ARE HERE
```

### 3. Branch
A **movable pointer** to a specific commit. That is literally all a branch is — a label pointing at a commit.
```
                              main → [commit C]
                                      ↑
[initial] ← [commit A] ← [commit B] ← [commit C]
```
When you make a new commit on branch `main`, the `main` label moves forward:
```
                                     main → [commit D]
                                              ↑
[initial] ← [A] ← [B] ← [C] ← [commit D]
```
When you create a branch `feature`, you make a NEW label pointing at the same commit:
```
                                          main    → [C]
                                          feature → [C]
```
Now if you commit on `feature`, only `feature` moves:
```
                             main    → [C]
                                          ↓
[init] ← [A] ← [B] ← [C]  ←  [commit-on-feature]
                                          ↑
                             feature → [commit-on-feature]
```
Two parallel timelines from the same starting point. This is the whole superpower of Git.

### 4. Remote
A **copy** of the repository stored somewhere else — usually GitHub.com. Your local repo and the remote are separate. You explicitly PUSH changes up or PULL changes down.

The default remote is called `origin`. When you clone from GitHub, `origin` = the GitHub URL you cloned from.

### 5. HEAD
A pointer to "where you are right now" — usually a branch name, so it points to the tip of your current branch.
```
HEAD → main → [commit D]
```
When you "switch branches", HEAD moves to point to the other branch.

## The lifecycle of a change
```
1. Edit files in your working directory
      ↓
2. Stage the changes you want to commit (in GHD: check the boxes)
      ↓
3. Commit — creates a permanent snapshot on the current branch
      ↓
4. Push — sends your local commits up to the remote (GitHub)
      ↓
5. Other people pull your changes down to their machines
```

## The Git object model (simplified)
Behind the scenes, Git stores:
- **Blobs** — file contents (deduplicated: same content = stored once)
- **Trees** — folder listings (which files/subtrees are in each directory)
- **Commits** — snapshot metadata (tree pointer, parent, author, message)

You never need to know this. But if you Google Git internals someday and see "blobs and trees", now you know.

## What GitHub Desktop does with this model
GitHub Desktop presents this model visually:
- **Changes tab** — working directory changes waiting to be committed
- **History tab** — the chain of commits, most recent first
- **Current branch** dropdown — HEAD and available branches
- **Fetch origin / Pull / Push** — remote operations

Everything you see in GHD is one of the five concepts above, presented as UI.
"""),
        "exercises": [
            ex(
                "02-1",
                "Draw (on paper or in a text file `regression-lab/git-diagrams.txt`) the state of the branch/commit graph after: (1) initial commit A, (2) commit B on main, (3) branch off `feature`, (4) commit C on feature, (5) commit D on main. Which commits are ancestors of `feature`? Of `main`?",
                "Use the notation from the module.",
                "```\nmain    → D\n              ↓\ninit → A → B → D\n              ↓\n              C\n              ↑\nfeature → C\n```\nAncestors of feature: A, B (not D). Ancestors of main: A, B (not C). B is the common ancestor. This is what Git compares when you eventually merge feature into main.",
            ),
            ex(
                "02-2",
                "In your own words: what is the difference between a branch and a commit?",
                "One is a snapshot, one is a pointer.",
                "Commit = an immutable snapshot of files at a moment in time. Branch = a movable label pointing at some commit. Commits are the 'stuff'. Branches are labels for finding stuff. This distinction confuses beginners for months — worth internalizing early.",
            ),
            ex(
                "02-3",
                "What is HEAD? Why does it usually point to a branch name rather than directly to a commit?",
                "Think about what happens when you make a new commit.",
                "HEAD = where you currently are. It usually points to a branch name (like `main`), so when you commit, the branch moves forward automatically to the new commit. If HEAD pointed directly to a commit (called 'detached HEAD'), new commits would exist but not be reachable from any branch — easy to lose.",
            ),
            ex(
                "02-4",
                "What is a 'remote'? Why do you need to explicitly PUSH and PULL — why doesn't Git sync automatically?",
                "Remember: Git is distributed.",
                "Remote = a separate copy of the repo, usually on GitHub. Explicit push/pull is a FEATURE — you commit freely offline, then choose when to share. Auto-sync would break offline work and force you to share half-finished commits. Explicit sync is the price of distributed.",
            ),
        ],
    },
    {
        "id": "03",
        "title": "What GitHub Is (The Platform)",
        "level": "Beginner",
        "summary": "GitHub the website: repositories, pull requests, issues, orgs. It is NOT Git — it is a service built ON Git.",
        "body": md("""
## Git vs GitHub — the critical distinction
- **Git** = the version control software (created by Linus Torvalds, 2005). Works on your laptop. Free. Open source. Command-line by default.
- **GitHub** = a WEBSITE where people host their Git repositories, owned by Microsoft. Adds features like pull requests, issues, CI/CD, discussions, code review UI.

You can use Git without GitHub (host your repos on GitLab, Bitbucket, or your own server). You cannot use GitHub without Git — everything on GitHub is a Git repository.

For this course, we use Git through GitHub Desktop (the app) with GitHub.com as the remote host. But the concepts of branches / commits / merges are Git's, not GitHub's.

## What GitHub adds on top of Git
### Hosting
Your repos live in the cloud. Accessible from anywhere. Backed up by default.

### Pull Requests (PRs)
A PR is a proposal: "I did these commits on this branch — please review and merge into main." PRs enable code review, discussion, and controlled integration. This is the collaboration heartbeat of modern development.

### Issues
Bug reports, feature requests, discussions — all tracked with labels, assignees, milestones. Linked to commits and PRs.

### GitHub Actions (CI/CD)
Automated workflows that run when things happen (push, PR, schedule). Tests, deploys, releases — all automated.

### Users, Organizations, Teams
- **User** — one person's account (`github.com/username`)
- **Organization** — a shared account for a team or company (`github.com/mycompany`)
- **Teams within an org** — subgroups with different permissions per repo

### Everything else
Wiki, project boards, discussions, sponsorships, packages, container registry, code scanning, secret scanning, dependabot, static hosting via Pages, and more. Most of it optional.

## Repository visibility
- **Public** — anyone can see and clone. Contributions require permission (fork + PR).
- **Private** — only invited people can see. Free tier includes unlimited private repos.
- **Internal** (paid tier) — visible only within your organization.

## The Fork / Clone / PR loop (contributing to open source)
When you want to contribute to someone else's public repo:
1. **Fork** — click Fork on their repo page. GitHub makes YOUR OWN copy of the repo under your username.
2. **Clone** your fork to your laptop.
3. Make a branch, commit changes, push to your fork.
4. Open a **Pull Request** from your fork's branch to the original repo.
5. Original owner reviews. If they approve, they merge — your changes are now in the upstream project.

This is how thousands of contributors work on projects they do not own.

## GitHub Desktop's role
GitHub Desktop understands GitHub-the-platform. It can:
- Sign into your GitHub account (Module 00)
- Publish local repos to GitHub in one click (Module 08)
- Clone from GitHub URLs (Module 09)
- Create Pull Requests without leaving the app (Module 17)
- Show which of your local branches have unpushed commits

What GHD cannot do (you need the website):
- Manage issues (create, comment, close)
- Configure repo settings (branch protection, secrets)
- Do code review comments on PRs (view diff yes, comment no)
- Merge PRs (view yes, click Merge no — you go to the website)

For the "administrative" side of GitHub, you visit github.com in a browser. GHD is for daily coding work.
"""),
        "exercises": [
            ex(
                "03-1",
                "Explain Git vs GitHub in one sentence each. If someone asked 'why do I need both?', what would you say?",
                "Git is the software, GitHub is a hosting service.",
                "Git = the version control tool that runs on your laptop. GitHub = a website that hosts Git repositories and adds collaboration features. You need Git (or something like it) to have version control at all. You need GitHub (or GitLab, Bitbucket) to easily share/collaborate on repos over the internet.",
            ),
            ex(
                "03-2",
                "Go to `github.com/torvalds/linux`. This is the Linux kernel repo. Look at: the file browser, the commits (500,000+), the pull requests, the branches. This is what a MASSIVE production repo looks like on GitHub.",
                "Just observe. Do not try to contribute!",
                "You saw a 20-year-old, 500k+ commit, 5000+ contributor repo. Every single line has an author, a date, and a reason. That is the power of Git at scale — and GitHub is what makes it browsable.",
            ),
            ex(
                "03-3",
                "Go to `github.com/settings/repositories`. Create your first REAL repo through the website: name it `git-practice`, description 'Learning Git via GitHub Desktop', Public, add a README. Now the repo exists on GitHub. We will clone it in Module 09.",
                "Do not add anything else — keep it minimal.",
                "The repo is at `github.com/YOUR-USERNAME/git-practice`. You created it via the website (later you will do the same via GHD). Both flows are common and end up in the same place.",
            ),
            ex(
                "03-4",
                "Name three things GitHub Desktop does well, and three things where you MUST use the website (github.com).",
                "Refresh: what does GHD do vs what does the website do?",
                "GHD: daily commits, branches, PR creation, clone/publish, conflict resolution. Website: issues, repo settings (branch protection, secrets), code review comments, merging PRs, org/team management. Rule of thumb: 'coding' = GHD, 'administration' = website.",
            ),
        ],
    },
    {
        "id": "04",
        "title": "GitHub Desktop Tour",
        "level": "Beginner",
        "summary": "Every button, every panel, every menu item — a full walkthrough of the GHD interface.",
        "body": md("""
## The layout, top to bottom, left to right

### Top toolbar (always visible)
- **Current Repository** dropdown (top-left) — switch between your local repos
- **Current Branch** dropdown (top-middle-left) — switch, create, delete branches
- **Fetch origin / Pull / Push** button (top-middle-right) — sync with the remote

### Left panel (the current view)
Two tabs:
- **Changes** — files you have modified since the last commit (staging area for the next commit)
- **History** — the chain of commits, most recent at top

### Center panel (context-sensitive)
- On Changes tab: **diff view** — what changed in the selected file
- On History tab: **files in that commit + diff view**

### Bottom-left (only on Changes tab)
- **Summary** field — the commit message (required)
- **Description** field — optional longer message
- **Commit to <branch>** button — creates the commit

### Menus (top of window / macOS menu bar)
- **File** — new/clone/add repo, options
- **Edit** — undo/redo/copy/paste for text fields (limited)
- **View** — toggle sidebars, change theme
- **Repository** — open in file explorer / terminal / editor, view on GitHub, push, pull
- **Branch** — create/rename/delete branch, merge, rebase, compare
- **Help** — docs and about

## Panel-by-panel: the Changes tab
When you edit files in your working directory:
```
[Changes tab]
  ☑ src/main.py       (modified)
  ☑ README.md         (modified)
  ☐ scratch.txt       (new, not tracked)
```
- **Checkboxes** — which files (or which HUNKS within a file) will go into the next commit
- **Diff view (right)** — shows what changed in the selected file: red = removed, green = added
- **You can uncheck INDIVIDUAL LINES** — click the line number to include/exclude specific changes

This is called **staging** in Git-speak. GHD calls it "checking" — same idea.

## Panel-by-panel: the History tab
```
[History tab]
  ● Fix login bug          rotem  2 hours ago
  ● Add DC blocker         rotem  yesterday
  ● Initial commit         rotem  last week
```
Click any commit → see what it changed. Compare any two commits by shift-clicking.

## The Fetch / Pull / Push button
This one button changes label based on state:
- **Fetch origin** — no local commits waiting to push, check for remote updates
- **Pull origin** — remote has changes you don't have locally
- **Push origin** — you have local commits not yet on the remote

If both push AND pull are needed, GHD prompts to pull first, then push.

## The Repository menu (right-click on the repo in the sidebar too)
Very useful items:
- **Show in Explorer / Finder** — open the folder in your file manager
- **Open in Terminal / Command Prompt** — for the CLI escape hatch (Module 23)
- **Open in <Editor>** — jump to your default text editor (VS Code, etc.)
- **View on GitHub** — open the repo page in your browser
- **Push / Pull / Fetch** — same as the top-right button

## Keyboard shortcuts worth learning early
| Shortcut (Win/Mac) | Action |
|---|---|
| Ctrl/Cmd + 1 | Changes tab |
| Ctrl/Cmd + 2 | History tab |
| Ctrl/Cmd + T | Switch repo |
| Ctrl/Cmd + B | Switch branch |
| Ctrl/Cmd + Enter | Commit |
| Ctrl/Cmd + P | Push |
| Ctrl/Cmd + Shift + P | Pull |
| Ctrl/Cmd + , | Preferences |

The rest are in Help → Keyboard Shortcuts.

## The little status indicators
- **Blue dot next to a repo** — has unpushed commits
- **Yellow/orange dot** — has uncommitted changes
- **Number next to a branch** — how many commits ahead/behind the remote

Once you know these, you can glance at the sidebar and know the state of every repo.

## What you cannot do in GHD (yet)
- Interactive rebase (reordering / squashing arbitrary commits) — CLI only for now
- Cherry-pick INTO the current branch from another — CLI or website
- Bisect — CLI only
- Manage tags — limited (can create/push but not sign)
- Submodules — partial support

For 90% of daily work, GHD covers you. The remaining 10% is Module 23.
"""),
        "exercises": [
            ex(
                "04-1",
                "Open GHD. Identify every panel from the module (top toolbar, left tabs, center, bottom-left commit form). Point at each one — literally. This is the muscle memory that pays off for years.",
                "Just a look-and-name exercise.",
                "You know where each panel is. Every future module will say things like 'in the Changes tab, check the file' — you now know exactly where that is.",
            ),
            ex(
                "04-2",
                "In your `hello-git` test repo from Module 00, edit `README.md` (add any text). Look at the Changes tab. Look at the diff. Uncheck the file. Recheck it. Click a single line's checkbox to include/exclude just that line.",
                "Experience the granular staging.",
                "You saw: (a) the file appears in Changes, (b) the diff shows red/green, (c) you can include/exclude WHOLE files OR INDIVIDUAL LINES. Line-level control lets you make focused commits even from messy work.",
            ),
            ex(
                "04-3",
                "Commit your change with the summary 'test edit'. Look at the History tab — your commit appears at the top. Click it. See the diff. This is your first end-to-end cycle in GHD.",
                "Summary is required; Description is optional.",
                "Commit exists. History shows: you → 2 seconds ago → 'test edit'. Click it and you see exactly what you changed. This tiny loop is the atomic unit of everything else in the course.",
            ),
            ex(
                "04-4",
                "Learn the four essential shortcuts: Ctrl/Cmd+1 (Changes), Ctrl/Cmd+2 (History), Ctrl/Cmd+Enter (Commit), Ctrl/Cmd+P (Push). Try each in your test repo.",
                "Muscle memory beats mouse hunting.",
                "You commit with Cmd+Enter instead of clicking the button. Small time savings compound massively over years of daily use. Learn these four first, add more as you go.",
            ),
            ex(
                "04-5",
                "Open Repository menu → Open in Terminal. A terminal opens in the repo folder. Run `git status`. This is your escape hatch — you can always drop to CLI without leaving GHD.",
                "GHD makes CLI access one click away.",
                "You see `git status` output — GHD and CLI show the SAME repository. They are two views into the same underlying `.git/` folder. Use whichever is easier for the task.",
            ),
        ],
    },
    # ────────────────────── PHASE 2: FIRST REPO ──────────────────────
    {
        "id": "05",
        "title": "Create Your First Real Repository",
        "level": "Beginner",
        "summary": "Two paths: create locally then publish, or create on GitHub then clone. Both end up in the same place.",
        "body": md("""
## The two paths (and when to use each)

### Path A: Create locally first, publish later
Use when you already have code on your machine or you want to start coding immediately without deciding on the GitHub name yet.
1. GHD → File → New Repository
2. Name, local path, optional README/gitignore/license
3. Create Repository (this makes a local repo)
4. Later: click **Publish repository** → choose owner (you or an org) → visibility → confirm
5. Now the repo also exists on GitHub

### Path B: Create on GitHub first, clone
Use when you know from the start this is a shared project, or when you want GitHub's README/gitignore/license templates.
1. github.com → New repository → fill in name, description, visibility
2. Optionally add README, `.gitignore`, license
3. Click Create Repository
4. In GHD: File → Clone Repository → pick from list (your GitHub repos appear automatically since you signed in)
5. Choose local path → Clone

Both paths end with a working local repo connected to a GitHub remote. Path A is more common for personal exploration; Path B is more common for team projects.

## Naming your repo
- Lowercase, hyphens, no spaces: `my-audio-tool` not `My Audio Tool`
- Descriptive: `fir-filter-lib` not `stuff`
- Prefix / suffix conventions: `dsp-` for related projects, `-lib` for libraries, `-app` for apps
- Cannot easily rename later (URL changes break links) — pick well the first time

## Files GHD offers to create
### README.md
The project's front page. Renders as HTML on GitHub. Write it in Markdown.
Every serious repo has one. Contents: what the project is, how to install, how to run, license.

### .gitignore
A list of files/folders Git should NEVER track. Common items: `build/`, `node_modules/`, `.env`, `*.o`, `*.exe`.
GHD lets you pick a template (Python, Node, C++, etc.) based on your language.
See Module 26 for a deep dive.

### License
The legal terms under which others can use your code.
- **MIT** — permissive, most common for open source
- **Apache-2.0** — permissive with patent grant
- **GPL** — copyleft, derivative works must be open source too
- No license = "all rights reserved" = nobody can legally use it. Add a license unless intentional.

## The first commit
Whether you use Path A or Path B, the initial commit is usually just "Initial commit" and contains README/gitignore/license.

Do NOT skip having an initial commit before you start real work. Some Git operations behave weirdly on a completely empty repo. The initial commit is the anchor for everything after.

## Folder layout starting simple
For a first repo, a sensible layout:
```
my-project/
  README.md
  .gitignore
  LICENSE
  src/
    main.py         # or main.c, or whatever
  tests/
    test_main.py
```
Do not over-engineer the folder structure early. Grow it as needed.

## Publishing a local repo (Path A finish)
After creating locally, GHD shows a big **Publish repository** button in the top bar.
- Owner: you or an org
- Visibility: Public / Private
- Repo name (can differ from local folder name)
- Description (optional)

Click Publish. Behind the scenes:
1. GHD creates the repo on github.com
2. Sets your local repo's remote (`origin`) to point at it
3. Pushes all your local commits up

Now `github.com/YOUR-USERNAME/repo-name` exists and matches your local.
"""),
        "exercises": [
            ex(
                "05-1",
                "Delete the `hello-git` from Module 00 (Repository → Remove... in GHD). Now File → New Repository. Name: `git-lab`, description 'personal Git learning lab', local path anywhere sensible, check README, pick .gitignore template = Python. Create. Verify: folder exists, GHD shows the repo, History shows 1 commit.",
                "This is your real starting repo for the whole course.",
                "Local repo exists with README and Python .gitignore. Initial commit in History. This repo will accompany you through every module — do not delete it.",
            ),
            ex(
                "05-2",
                "In `git-lab`, click the big **Publish repository** button. Owner = your username, keep the same name (`git-lab`), keep it PUBLIC for learning, click Publish. Verify: browser to `github.com/YOUR-USERNAME/git-lab` — the repo exists with your README.",
                "Publishing = creating the remote and pushing your commits.",
                "GitHub URL loads and shows your README, .gitignore, license (if you added one). You just did the local-first workflow end to end.",
            ),
            ex(
                "05-3",
                "Now do Path B for practice. On github.com: New repository → name `git-lab-remote-first`, add README, add MIT license, Public, Create. Then in GHD: File → Clone Repository → find it in the list → Clone.",
                "Same result via the opposite direction.",
                "You have `git-lab-remote-first` locally, cloned from GitHub. Notice: this repo already has its remote set up (unlike Path A where publishing set it). Both flows are valid, both very common.",
            ),
            ex(
                "05-4",
                "Compare the two `.gitignore` files (Python template from GHD vs from GitHub's template). Are they different? What is inside?",
                "GHD and GitHub use slightly different template sources.",
                "Both include common Python patterns (`__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, etc.) but may differ in specifics. Not important now — just know: `.gitignore` prevents these from ever being committed. Module 26 goes deep.",
            ),
            ex(
                "05-5",
                "Delete `git-lab-remote-first` from GitHub (Settings → Danger Zone → Delete repository) AND remove from GHD (Repository → Remove). Cleanup practice. Keep `git-lab` — that is your working lab.",
                "Deletion on GitHub is permanent — practice on throwaways only.",
                "Both remote and local copies gone. Clean state. Notice GitHub requires you to type the full repo name to confirm deletion — that safety exists for a reason.",
            ),
        ],
    },
    {
        "id": "06",
        "title": "The Change / Stage / Commit Cycle",
        "level": "Beginner",
        "summary": "Every day of using Git is variants on this three-step loop. Learn it once, use it a million times.",
        "body": md("""
## The atomic loop
```
1. CHANGE  — edit files in your text editor
2. STAGE   — pick which changes to include in the next commit (checkboxes in GHD)
3. COMMIT  — permanently record those changes with a message
```
Then repeat. Forever. That is 90% of using Git.

## The staging area (what "stage" actually means)
Between "changes on disk" and "committed to history", there is an in-between zone called the **staging area** (or **index** in Git-speak).
```
Working directory  →  Staging area  →  Committed history
   (edited files)      (check boxes)      (permanent record)
```
Why the middle step? Because you often want to commit SOME changes but not others. Example:
- You fixed a bug in `filter.c`
- You also added a debug `printf` in `main.c` for testing
- You want to commit ONLY the bug fix, not the debug print

Staging lets you pick per file — or in GHD, even per LINE.

## GHD's staging UI
```
[Changes tab]
  ☑ filter.c    (2 lines changed)
  ☐ main.c      (1 line changed)   ← unchecked, will NOT be committed
```
Clicking the checkbox toggles the whole file. Clicking a specific line's checkbox (in the diff view) toggles just that line.

## Writing the commit
Bottom-left of GHD:
```
Summary (required):  Fix off-by-one in filter loop
Description (opt):   The FIR filter was reading one sample past the end
                     of the input buffer when the last coefficient was zero.

[Commit to main ↵]
```
- **Summary** — 50-72 chars, imperative mood ("Fix", not "Fixed"). This is what shows in History.
- **Description** — optional. Use for WHY the change was made, or for longer context.

Click **Commit to main** (or Cmd/Ctrl+Enter). Done. History gets a new entry.

## What a commit contains
When you commit, Git records:
- The full state of every STAGED change
- Your name and email (set at signup — File → Options → Git)
- The current timestamp
- Your commit message
- A pointer to the previous commit (parent)
- A unique SHA-1 hash identifying THIS commit (like `a3f7c2b`)

The commit is IMMUTABLE — once made, its content cannot be changed (only added-to or reverted).

## The three-file demo
1. Create `notes.md` with any content
2. Edit `README.md` (change one word)
3. Delete `LICENSE` (or leave alone — your choice)

Now GHD's Changes tab shows:
- notes.md (new file)
- README.md (modified)
- LICENSE (deleted, if you did)

Check all → commit with message "Working with three file changes". Push (Cmd/Ctrl+P).

Look at History: one commit, three file changes captured together.

## Commit granularity — how much per commit?
The community convention:
- **One logical change per commit** — a bug fix, one refactor, one small feature
- **Not** one commit per file (too small)
- **Not** one commit per day of work (too big)

A good rule: if you cannot write a summary in ~50 characters, the commit is probably doing too many things. Split it.

## The undo before commit
Before you commit, you can always:
- **Discard changes** on a file — right-click → Discard changes → confirm. This RESETS the file to the last committed state. GONE. Not recoverable.
- **Uncheck** a file — keeps the changes on disk, just excludes from THIS commit
- Edit some more, or use a different summary

After commit, undoing is different (Module 20).

## What NOT to commit
- Generated files (`.exe`, `.o`, `build/`) → use `.gitignore`
- Secrets (API keys, passwords) → NEVER commit, even briefly (Module 26)
- Huge binaries (>50 MB) → use Git LFS (Module 26)
- Temp / editor / OS files (`.DS_Store`, `Thumbs.db`, `*.swp`) → use `.gitignore`

If you accidentally commit a secret, changing the source is not enough — you must scrub it from history AND rotate the credential. See Module 26.
"""),
        "exercises": [
            ex(
                "06-1",
                "In `git-lab`, create three files: `notes.md`, `todo.md`, `scratch.txt` (any content). In GHD's Changes tab: check `notes.md` and `todo.md`, uncheck `scratch.txt`. Commit with message 'Add notes and todo'. Observe: History shows the commit with only 2 files.",
                "Selective staging is the whole point.",
                "You committed 2 files but kept `scratch.txt` uncommitted (it still shows in Changes, ready for a future commit). This is a normal, useful pattern.",
            ),
            ex(
                "06-2",
                "Edit `notes.md`: add 5 lines. In the diff view, uncheck lines 2 and 4 (click their line numbers). Commit with message 'Add note lines 1, 3, 5'. Now edit again, commit the remaining lines separately.",
                "Line-level staging in GHD is a killer feature.",
                "You made 2 commits from what could have been 1 messy commit. Each has a clear purpose. This is how you keep history clean even when you code messily.",
            ),
            ex(
                "06-3",
                "Write a good commit summary and description for this scenario: 'You changed the way the audio filter handles zero-length input, previously it crashed, now it returns an empty buffer'.",
                "Summary imperative, ~50-72 chars. Description explains why.",
                "Summary: `Handle zero-length input in audio filter`\nDescription:\n```\nPreviously the filter crashed with a division-by-zero when given\nan empty input buffer. Now it returns an empty output immediately.\n\nCloses issue #42.\n```",
            ),
            ex(
                "06-4",
                "Right-click a modified file in Changes → Discard changes → confirm. The file reverts to the last committed state. Practice this until you understand: DISCARD IS PERMANENT (before commit). There is no undo for discard.",
                "This is one of the two ways to lose work in Git. Know it.",
                "Discard writes over your working copy with the last committed version. Unstaged changes = gone forever. Rule: if you might want it later, commit first, revert later. Committed things can be recovered; discarded uncommitted things cannot.",
            ),
            ex(
                "06-5",
                "Push your commits (Ctrl/Cmd+P). Refresh github.com/YOUR/git-lab in the browser. Your commits appear there. Click a commit → see the diff on GitHub. Web view and GHD view show the same thing.",
                "Local commits are private until pushed.",
                "GitHub now shows what your local repo shows. Push is the moment your commits become visible to everyone. Before push, nothing you commit is public.",
            ),
        ],
    },
    {
        "id": "07",
        "title": "Writing Commits That Do Not Embarrass You Later",
        "level": "Beginner",
        "summary": "Commits are the historical record of your project. Six months later, YOU are the reader. Write for that future self.",
        "body": md("""
## The commit as time-travel note
Every commit you make becomes part of the permanent history. Six months from now, a future you (or a colleague) will read your commit messages while debugging something. Bad messages waste hours. Good messages save hours.

## The seven rules (widely adopted convention)
Based on Chris Beams' well-known style guide:
1. Separate summary from body with a blank line
2. Limit the summary to 50 characters (72 is a hard max)
3. Capitalize the summary
4. Do not end the summary with a period
5. Use imperative mood in the summary ("Fix bug" not "Fixed bug" not "Fixes bug")
6. Wrap the body at 72 characters
7. Use the body to explain WHAT and WHY, not HOW

## Imperative mood — why it matters
Imperative: "Fix the login bug"
Past: "Fixed the login bug"
Present: "Fixes the login bug"

Imperative wins because it matches how Git itself talks: "This commit will `Fix the login bug` if applied." Git's own auto-generated messages ("Merge branch...", "Revert...") are imperative. Following the same style makes history feel consistent.

## Good vs bad commit summaries
```
BAD                            GOOD
------------------------       -----------------------------
"stuff"                        "Fix off-by-one in FIR loop"
"updates"                      "Add DC blocker to audio path"
"WIP"                          "Handle zero-length input safely"
"fixed the thing"              "Reject negative sample rates"
"asdf"                         "Rename biquad coefficients for clarity"
```
The good ones tell you WHAT the commit does at a glance. History becomes browsable.

## When to use the description (body)
Use the body for:
- **Why** the change was made (context that is not in the code)
- **What** was changed at a high level, if summary is not enough
- **Trade-offs** considered
- **Links** to issues, PRs, docs
- **Breaking changes** (in bold or with a `BREAKING:` prefix)

Example:
```
Rewrite biquad in transposed direct-form II

Previous implementation used direct-form I, which requires
5 delay elements. Transposed direct-form II uses only 2,
saves memory on the STM32 (~1KB across all instances).

Bit-exact output verified against golden vectors — see
tests/goldens/biquad_dtf2.bin.

Refs: issue #123, discussion in PR #456.
```

## Conventional Commits (a popular schema)
Some teams enforce a structured summary format:
```
type(scope): description

feat(audio): add DC blocker
fix(ui): correct button alignment on macOS
docs(readme): add installation instructions
refactor(filter): extract common biquad math
test(dsp): add regression test for issue #42
chore(deps): bump numpy to 1.26
```
Types: feat / fix / docs / style / refactor / test / chore. Optional `!` for breaking: `feat(api)!: rename process() to run()`.

Adopting conventional commits enables auto-generated changelogs, semver bumps, and structured review. Not mandatory, but if your team uses it, follow it. If starting fresh, consider it.

## Commit size — the Goldilocks principle
- **Too small**: one commit per typo, one per rename. History becomes 200 commits of noise.
- **Too big**: "day's work" or "final refactor" — impossible to review, impossible to revert cleanly.
- **Just right**: one logical change per commit. Compiles. Passes tests. Has a clear message.

Rule of thumb: if you can describe it in ONE sentence and it does not change unrelated things, commit size is fine.

## Editing commit messages you made
- **Just made a bad commit, not pushed yet**: Right-click on the last commit in History → Amend commit → fix the message → save. This REPLACES the commit (creates a new one with new SHA).
- **Pushed already**: technically possible with force-push but risky if others use the repo. Best practice: leave it and do better next time.

Amend is only for local, unpushed commits. Never amend or rebase commits that others have already pulled.

## Anti-patterns to avoid
- Committing broken code that "you will fix in the next commit"
- Committing generated files (`.exe`, `dist/`)
- Committing commented-out code just in case
- "WIP" commits pushed to shared branches (WIP is fine locally, squash before merging)
- Sensitive data in commit messages (customer emails, API keys)
"""),
        "exercises": [
            ex(
                "07-1",
                "Write commit summaries for these fake scenarios. Follow the 7 rules:\n(a) You added a Python function that reads a WAV file\n(b) You fixed a crash when the user clicked Cancel during export\n(c) You renamed the `foo_util.py` module to `signal_utils.py`\n(d) You removed dead code from `parser.c`\n(e) You updated the numpy dependency from 1.24 to 1.26",
                "Imperative mood, capitalize, no period, under 72 chars.",
                "(a) `Add read_wav utility for loading WAV files`\n(b) `Prevent crash when Cancel pressed mid-export`\n(c) `Rename foo_util to signal_utils`\n(d) `Remove dead code from parser`\n(e) `Bump numpy from 1.24 to 1.26`\nAll pass the seven rules.",
            ),
            ex(
                "07-2",
                "In `git-lab`, make an intentional bad commit (`stuff` as summary). Then use right-click → Amend commit to fix the summary to something good. Verify History shows the new (better) message, not the old one.",
                "Amend replaces the last commit — new SHA, new message.",
                "Amended commit shows the improved message. The SHA changed (visible in commit details). Note: this only works cleanly on the LAST commit and BEFORE pushing.",
            ),
            ex(
                "07-3",
                "Write a full commit (summary + body) for the scenario: 'You refactored the audio pipeline to use dependency injection, keeping the same public API but making it 40% easier to test.'",
                "Body explains WHY, mentions trade-offs, links to context.",
                "```\nRefactor audio pipeline to use dependency injection\n\nThe processing stages (input, filter, output) now receive their\ndependencies via constructor arguments instead of importing them\ndirectly. Public API is unchanged - callers of Pipeline.process()\nsee no difference.\n\nMotivation: tests can now inject fakes for the audio driver and\nfile I/O layers, reducing test setup by ~40% and eliminating the\nneed for tmp files in the unit suite.\n\nSee design note in docs/adr/003-di-audio.md.\n```",
            ),
            ex(
                "07-4",
                "Discuss (in `notes.md` inside `git-lab`): what problems do bad commit messages create six months later? Give 3 concrete examples.",
                "Think about debugging, blame, rollback.",
                "(1) When bisecting a regression, you land on a commit called 'stuff' - no idea if this is where the bug is. (2) When code review looks at a PR titled 'updates', reviewer must read every line to understand intent. (3) When rolling back a bug, hard to identify which commits are safe to revert vs which are dependencies. Bad messages compound over time.",
            ),
        ],
    },
    {
        "id": "08",
        "title": "Publishing and Pushing",
        "level": "Beginner",
        "summary": "Push sends your local commits to the remote. Publish is the first push for a new repo. Same idea, different words.",
        "body": md("""
## Publish vs Push
- **Publish** = first-time upload of a local repo to GitHub. Creates the remote repo AND pushes all commits. One-time per repo.
- **Push** = ongoing sync of new local commits to the existing remote. Every time you commit and want to share.

GHD uses different button labels for these but does the same underlying thing (`git push`).

## The Push button lifecycle
Look at the top-right button in GHD:
| State | Button says | What it does |
|-------|-------------|--------------|
| Nothing to sync | "Fetch origin" | Checks remote for updates |
| Remote has new commits | "Pull origin (N)" | Downloads their commits |
| You have new local commits | "Push origin (N)" | Uploads your commits |
| Both | Prompts pull first | Then push |

The number (N) is how many commits are ahead / behind.

## What "push" actually does
1. Git compares your local branch to the remote branch (e.g., local `main` vs `origin/main`)
2. Finds commits you have that the remote doesn't
3. Sends those commits (as compressed packages) up to GitHub
4. Updates the remote branch pointer to your latest commit

Push is FAST — only the new commit data is transferred, not the entire repo.

## What can go wrong with push
### Push rejected (someone else pushed first)
Scenario:
- You: local `main` at commit `C`
- Remote `main` at commit `D` (someone else pushed while you were coding)
- Your commit `E` is based on `C`, not `D`

Git refuses to push — pushing would erase their commit `D`. GHD prompts you to **Pull first** (see Module 10).

### Push rejected (permission denied)
You don't have write access to this repo (common on other people's repos). Solutions:
- **Fork** the repo (Module 18) — then push to your fork
- Ask the owner for collaborator access

### Push includes a huge file
GitHub rejects pushes with files > 100 MB. Solutions:
- Remove the file from the commit (see Module 20 for how to un-commit)
- Add to `.gitignore` for future
- Use **Git LFS** for legitimately large files (Module 26)

## Pushing branches other than main
When you create a new branch (Module 13) and commit on it, that branch is LOCAL only until you push it. GHD's Push button will offer to publish the branch on first push.

## What appears on GitHub after push
After push:
- The commit(s) are visible in the GitHub Commits tab
- Any files added/modified appear in the file browser
- If Actions (CI) is configured, it may run automatically
- If branch protection or required reviews exist, some pushes are blocked

## Force push — the dangerous cousin
Sometimes you want to REPLACE the remote history with a rewritten local history (after amending or rebasing). This is called **force push**. GHD does NOT expose force-push in normal UI — it is a safety measure.

If you must force-push:
- Repository → Open in Terminal → `git push --force-with-lease origin branchname`
- **Only do this on YOUR OWN branches, never on shared branches like `main`**
- `--force-with-lease` is safer than `--force` — it aborts if someone else pushed in the meantime

Force-push is why "never rewrite public history" is a Git rule (Module 22).

## Fetch vs Pull vs Push (quick reminder)
- **Fetch** — download remote changes but don't apply them to your working files. Safe, informational.
- **Pull** — fetch AND merge remote changes into your current branch.
- **Push** — upload YOUR commits to the remote.

Full breakdown in Module 10.

## Two-factor authentication (2FA)
GitHub requires 2FA for accounts (since 2023). GHD handles this via OAuth (browser sign-in) so you rarely think about it. If you use CLI, you need a **Personal Access Token** (PAT) instead of a password:
- github.com/settings/tokens → Generate new token (classic)
- Give it `repo` scope
- Use as your password when git prompts

Save the PAT securely (Windows Credential Manager, macOS Keychain, or a password manager) — you cannot view it again after creation.
"""),
        "exercises": [
            ex(
                "08-1",
                "In `git-lab`, make 3 small commits (edit README, add a file, delete a file). Each commit separately. Then look at the top-right button — should say `Push origin (3)`. Click it. Refresh github.com — all 3 commits appear.",
                "Push handles any number of pending commits in one go.",
                "Three commits arrive on GitHub in one push. This is the standard workflow — commit locally many times, push in a batch when ready.",
            ),
            ex(
                "08-2",
                "Try to push when there is nothing to push (button says 'Fetch origin'). Click it anyway. Nothing changes locally — GHD just checked if the remote had updates. Fetch is safe and informational.",
                "Fetch = 'ask the server what's new', without applying anything.",
                "Fetch confirms your local view of the remote is up to date. No commits move. Good habit: fetch before starting work to see if teammates pushed anything.",
            ),
            ex(
                "08-3",
                "Simulate 'push rejected' scenario: on github.com in the browser, edit README.md directly (Edit pencil → change a word → Commit changes directly to main). Now in GHD, without fetching, try to make a local commit and push. GHD will detect the divergence and prompt to pull first.",
                "This is the most common push conflict — someone (or your web edit) got there first.",
                "GHD detects the remote has changed and prompts 'Pull first'. This is Git protecting you from overwriting the web edit. After pulling (Module 10), you can push cleanly.",
            ),
            ex(
                "08-4",
                "Discuss: your teammate is trying to push to a shared repo and it fails with 'permission denied'. What are the two likely causes and how do you fix each?",
                "Access vs authentication.",
                "(1) They are not a collaborator on the repo → owner adds them via Settings → Collaborators. (2) Their credentials are stale (old PAT, expired OAuth) → sign out of GHD, sign back in; or regenerate PAT. Most 'permission denied' errors are one of these two.",
            ),
            ex(
                "08-5",
                "Read the module's warning on force-push carefully. In your own words: why is force-push dangerous, and when is it acceptable?",
                "Force overwrites remote history — the risk is other people's work.",
                "Dangerous: force-push replaces the remote's history with yours. If a teammate had pulled the OLD history and made commits on it, those commits are orphaned. Acceptable: on branches YOU alone use (feature branches nobody else touches). Never on shared branches (main, develop) unless everyone coordinates.",
            ),
        ],
    },
    # ────────────────────── PHASE 3: EXISTING REPOS ──────────────────────
    {
        "id": "09",
        "title": "Cloning a Repository",
        "level": "Beginner",
        "summary": "Bringing an existing GitHub repo down to your machine. The starting point for contributing to any project.",
        "body": md("""
## What clone does
Cloning downloads a complete copy of a repository from GitHub to your local machine:
- Every file in the current state
- The ENTIRE history (every commit ever)
- All branches
- All tags
- A pointer to the remote (`origin`) set up automatically

After cloning, you have a fully functional local repo. You can work offline immediately.

## Three ways to clone in GHD
### Way 1: From your GitHub account
File → Clone Repository → "GitHub.com" tab.
Lists all repos you have access to (yours, orgs you belong to, ones you've forked).
Pick one → choose local path → Clone.
Simplest for repos you own or collaborate on.

### Way 2: From a URL
File → Clone Repository → "URL" tab.
Paste a URL like `https://github.com/owner/repo` or `git@github.com:owner/repo.git`.
Works for any repo you have access to (or any public repo).
Useful when someone sends you a link.

### Way 3: From the GitHub website
On a repo's page → click green **Code** button → "Open with GitHub Desktop" → confirms in GHD.
Handy when browsing GitHub in a browser.

## HTTPS vs SSH URLs
When you copy a clone URL from GitHub, there are two flavors:
- **HTTPS**: `https://github.com/owner/repo.git` — uses your OAuth login (via GHD) or PAT (via CLI)
- **SSH**: `git@github.com:owner/repo.git` — uses SSH keys stored on your machine

For GitHub Desktop, HTTPS is the default and works out of the box. SSH requires generating a key and adding it to your GitHub account (Settings → SSH keys). Only bother with SSH if you use CLI heavily or prefer key-based auth.

## Where to clone (local path)
Pick a stable "repos" folder — something like:
- Windows: `C:\\Users\\YourName\\repos\\`
- macOS/Linux: `~/repos/` or `~/dev/`

DO NOT clone into:
- OneDrive / Dropbox / iCloud sync folders → sync tools fight with Git internals
- Program Files or other system-protected folders
- Inside another Git repo (creates confusion)

If you must use a cloud-sync folder, EXCLUDE it from sync at that path.

## Shallow clones (large repos)
Very large repos (Linux kernel, Chromium) have gigabytes of history. GHD does not offer shallow clone in UI, but you can do it via CLI:
```bash
git clone --depth 1 https://github.com/torvalds/linux.git
```
Depth 1 = only the latest commit, no history. Saves gigabytes. Downside: cannot see history or use bisect.

For most repos you clone, don't bother with shallow — the full history is usually a few megabytes.

## Cloning a private repo
If you have access (are a collaborator or in the owning org), it works identically to a public repo through GHD's list. GHD's OAuth login handles the auth.

If someone shares a URL to a private repo you don't have access to, cloning will fail with 'not found' (GitHub doesn't distinguish 'private' from 'doesn't exist' to prevent probing).

## After cloning: what's set up automatically
- Local repo folder created with all files
- `.git/` directory containing full history
- Remote `origin` points to the GitHub URL
- Local branch `main` (or `master`) tracks `origin/main`
- All remote branches visible in the branch dropdown

You are ready to work immediately.

## Cloning a specific branch
By default clone gives you the default branch (usually `main`). To start on a different branch:
```bash
git clone -b feature-x https://github.com/owner/repo.git
```
In GHD: clone normally, then use the branch dropdown to switch (Module 13).

## What clone does NOT do
- It does not upload anything (that's push, Module 08)
- It does not link to your GitHub identity in a special way — clone is a one-time snapshot pull; further syncing is push/pull
- It does not fork — cloning is downloading; forking is making your own remote copy (Module 18)
"""),
        "exercises": [
            ex(
                "09-1",
                "In GHD: File → Clone Repository → GitHub.com tab. Clone your own `git-lab` repo again to a NEW local path (e.g., `~/repos/git-lab-clone/`). Now you have two local copies of the same remote repo. Notice both work independently.",
                "This proves clone is just a download.",
                "Two folders, both fully functional, both pointing at the same origin. Commits in one require push+pull to appear in the other. This is exactly what happens when a colleague clones your repo.",
            ),
            ex(
                "09-2",
                "Clone a public repo you did not create. Suggestion: `https://github.com/torvalds/uemacs` (Linus' small text editor, ~1 MB) or `https://github.com/git/git-scm.com`. Explore the History tab — many years of commits.",
                "Any small public repo works.",
                "You have a full local copy of a real project you don't own. You can browse history, view branches, even make local commits (but you cannot push without permission — you would need to fork for that, Module 18).",
            ),
            ex(
                "09-3",
                "Delete the second `git-lab-clone` folder (Repository → Remove from GHD). Notice: the ORIGINAL `git-lab` is untouched, and github.com is untouched. Local removal is safe.",
                "'Remove from GHD' only removes from GHD's list AND (optionally) the local disk folder. It never touches the remote.",
                "The second clone is gone. First clone still works. github.com repo still works. This is why 'clone' is safe experimentation — you can always clone again.",
            ),
            ex(
                "09-4",
                "In your `git-lab` folder, open the hidden `.git/config` file in a text editor. Find the `[remote \"origin\"]` section. That is where the URL to GitHub is stored. This is the connection.",
                "Do not edit unless you know what you're doing.",
                "You see `url = https://github.com/YOUR-USERNAME/git-lab.git` (or similar). This one line is what makes your local repo know where 'origin' is. If you change or delete this, GHD loses the ability to push/pull to GitHub.",
            ),
        ],
    },
    {
        "id": "10",
        "title": "Fetch vs Pull vs Sync",
        "level": "Beginner",
        "summary": "The three remote-download operations. Fetch is safe. Pull is fetch+merge. Sync (in GHD) is fetch+pull+push.",
        "body": md("""
## The three operations
### Fetch
Downloads new commits from the remote WITHOUT changing your working files or current branch.
- Safe: nothing on your disk changes
- Informational: you can see what's on the remote
- After fetch: `origin/main` is up to date, but your local `main` is not
- Use when: you want to see what's new without integrating

### Pull
Fetch + immediately merge the remote changes into your current branch.
- Downloads AND applies
- Your working files may change
- Can create merge commits or produce conflicts (Module 15)
- Use when: you want to catch up your local branch to the remote

### Push
Uploads YOUR commits to the remote. Opposite direction of fetch/pull. (Module 08)

## GHD's "Sync" behavior
GHD combines these into a smart button:
- If ahead only (unpushed local commits): button = **Push**
- If behind only (unpulled remote commits): button = **Pull**
- If both ahead and behind: button = **Pull** (must pull first, then push)
- If in sync: button = **Fetch origin** (just check for updates)

The button label tells you the state at a glance.

## Fetch first — the golden habit
Best practice at the start of each work session:
1. Click **Fetch origin**
2. See if anyone pushed anything
3. If yes: pull, review what changed, maybe restart your work plan
4. If no: proceed with your day

Skipping fetch means you might work for hours on the wrong version, then face a big painful merge at push time.

## The three states after fetch
### 1. Everything is even
Your local `main` matches `origin/main`. Nothing to do.

### 2. You are ahead
You have local commits that aren't on the remote. Next step: push.

### 3. You are behind
Remote has commits you don't have. Next step: pull.

### 4. Diverged (both ahead AND behind)
You have local commits AND the remote has different commits. Requires merge or rebase.
GHD prompts: **Pull with merge** (default) or **Pull with rebase** (if configured in Options).

## Pull with merge vs pull with rebase
Two ways to integrate remote changes:

### Merge (default in GHD)
Creates a **merge commit** that combines both histories:
```
Before:                    After pull:
    A - B - C (local)          A - B - C - M (local)
      \\                          \\        /
       D - E (origin/main)        D - E---
```
- Preserves full history of what happened
- Creates a merge commit
- Simple, safe, always works

### Rebase (opt-in via Options)
Replays your local commits ON TOP of the remote:
```
Before:                    After rebase-pull:
    A - B - C (local)          A - D - E - B' - C' (local)
      \\
       D - E (origin/main)
```
- Linear, cleaner history
- Rewrites your local commits (new SHAs)
- Do NOT rebase-pull if your local commits were already pushed and pulled by others

To choose the default: GHD → Preferences → Advanced → "Pull with rebase". Personal preference; rebase gives cleaner history but has sharper edges.

## Force pull (throw away local, take remote)
Sometimes you want to obliterate local changes and just match the remote:
1. Discard all local changes (Changes tab → right-click → Discard all changes)
2. Then Pull

Or via CLI:
```bash
git fetch
git reset --hard origin/main
```
Warning: this DELETES uncommitted work. Commit or stash first if unsure.

## When pull is slow
Pull downloads new commit data over the internet. For small changes, milliseconds. For a repo that hasn't been pulled in months with hundreds of new commits, could be a minute. This is normal.

If pull is slow on EVERY pull for a small change — likely the remote has huge binary files. See Module 26 (Git LFS).

## What to do when pull creates a conflict
When the remote changed the same lines you changed, pull produces a merge conflict. Full resolution workflow: Module 15.

Quick preview: GHD stops the merge, shows conflicted files, and gives you tools to resolve. It is not scary once you have done it once or twice.

## Practical daily flow
```
Morning:
  1. Fetch origin (see the button label change)
  2. If behind: Pull. Review what changed.
  3. Start coding

During work:
  1. Commit often (small, focused)
  2. Push periodically (once per commit or every few commits — either works)

Before pushing after a long work session:
  1. Fetch again — maybe someone pushed while you were coding
  2. If diverged: pull (with merge or rebase, per your preference)
  3. Then push
```
"""),
        "exercises": [
            ex(
                "10-1",
                "In `git-lab`, edit a file on github.com directly (web pencil icon → change → commit to main). Come back to GHD. Click **Fetch origin**. GHD button changes to **Pull origin (1)**. Look at History — you can see the new commit is 'from origin' but not yet merged into local.",
                "Fetch shows remote state without applying it.",
                "You see the remote is ahead by 1 commit. Your local files are unchanged. This gives you a moment to decide: pull now, or keep working first.",
            ),
            ex(
                "10-2",
                "Now click **Pull origin (1)**. Your local `main` catches up. The file on disk now matches what you edited on GitHub. History shows the new commit as part of your local history.",
                "Pull = fetch + merge (into current branch).",
                "Local caught up. Working files updated. No conflict because you only changed on the remote side. This is the standard pull-when-behind flow.",
            ),
            ex(
                "10-3",
                "Create the diverged scenario: edit README.md on github.com (change 'A'). Then edit the SAME line in GHD locally (change to 'B') and commit locally. Now try Fetch → notice both ahead AND behind. Click Pull. GHD merges — may produce a conflict.",
                "This is the diverged case — the most common Git 'situation' you will face.",
                "GHD shows a merge conflict on README.md. Two versions to reconcile. Module 15 teaches how — for now, just observe: this is what 'diverged branches' looks like. It happens constantly on multi-person projects.",
            ),
            ex(
                "10-4",
                "Toggle merge vs rebase preference: GHD → Preferences → Advanced → 'Pull with rebase'. Now repeat exercise 10-3 with rebase. Compare the resulting history: merge = extra merge commit, rebase = linear.",
                "Same result (both branches integrated) but different history shape.",
                "With rebase, no merge commit. Your local commits appear AFTER the remote ones in history. Linear. With merge, you see the two lines of history join at a merge commit. Both are correct — pick what your team prefers.",
            ),
            ex(
                "10-5",
                "Write a checklist you will actually follow: 'When I start work in the morning, I do...' Include Fetch, decide-based-on-state, then start. Save in `git-lab/morning-routine.md`.",
                "Habits beat memory. Write it, follow it.",
                "Sample:\n```\n1. Open GHD, switch to today's repo\n2. Click Fetch origin\n3. If Pull button appears: click Pull, look at History for new commits\n4. Read commit messages of new commits — did anyone touch what I'm about to work on?\n5. If yes: rethink plan. If no: proceed.\n6. Only THEN start coding\n```",
            ),
        ],
    },
    {
        "id": "11",
        "title": "Reading the History (Log, Diff, Blame)",
        "level": "Beginner",
        "summary": "History is where Git's value materializes. Learn to browse it, diff any two points, and find who wrote each line.",
        "body": md("""
## The History tab
GHD → Ctrl/Cmd+2. You see:
```
● Fix biquad denormals                     rotem  2h ago    a3f7c2b
● Add DC blocker to audio path             rotem  yesterday  b8d4e1a
● Rename FIR coefficients for clarity      alice  3d ago     c2f9d5e
● Initial commit                           rotem  2w ago     d5a8f3b
```
Each row = one commit. Left dot connects to parents (branch/merge visualization). Author, time, and short SHA on the right.

Click a commit → the center panel shows:
- File list (which files this commit changed)
- Diff for the currently selected file (red=removed, green=added)
- Full commit message at the top

## Filtering history
GHD's search box (top of History tab) filters by:
- Commit message text (search "denormal" → finds commits mentioning denormals)
- Author name (search "alice" → alice's commits)
- File path (limited — use CLI for advanced file-scoped history)

Advanced filtering:
```bash
git log --grep="denormal"          # commits with 'denormal' in message
git log --author="alice"           # alice's commits
git log -- path/to/file            # commits touching a file
git log --since="2 weeks ago"      # time-scoped
```
Repository → Open in Terminal to run these.

## Diffing two commits (compare)
- Click one commit
- Shift+click another commit
- GHD shows the diff BETWEEN those two commits

This is powerful for: "what changed between last release and now?"

## The 'blame' view — who wrote each line
Blame answers: for each line in a file, WHICH commit last touched it (and by whom, when)?

GHD does not have a built-in blame UI. Two ways to access it:
### Way 1: View on GitHub
- Repository → View on GitHub
- Navigate to the file
- Click "Blame" button
Each line shows the commit and author.

### Way 2: CLI
```bash
git blame path/to/file
```
Output: each line prefixed with SHA, author, date.

For serious blame work (finding when a specific line was written and why), the GitHub web view is usually the most readable.

## Following a line's history (line log)
On GitHub: open file → Blame → click the "..." next to a line's commit → "View file at this commit". Walk backwards through the file's history line by line.

Extremely useful for debugging: "why is this weird line here?" — trace it back to the commit that added it, read that commit's message and PR.

## The commit SHA (fingerprint)
Every commit has a unique 40-character SHA-1 hash: `a3f7c2b8d4e1a9c2f5b8d4e1a9c2f5b8d4e1a9c2`. GHD shows the short version (`a3f7c2b`) — first 7 chars, usually enough to be unique in a repo.

Refer to commits by their SHA in:
- Commit messages: "Reverts a3f7c2b"
- Issue discussions: "The bug started in a3f7c2b"
- PR reviews: "Look at what a3f7c2b changed"

Copy a SHA from GHD: right-click commit → Copy SHA.

## Viewing history for a specific file
- Right-click a file in Explorer/Finder (with GHD installed correctly, context menu integration)
- Or: click a file → GHD shows commits that touched it (in some views)
- Or CLI: `git log -- path/to/file`

## Understanding merge commits in history
A merge commit has TWO parents (two dots joining):
```
●───┐
    │
● ● ┘
```
When you click a merge commit, its "changes" are the resolution — how the two histories were reconciled.

## History visualization tools beyond GHD
For complex history (many branches, lots of merges), external tools are clearer:
- **git log --oneline --graph --all** (CLI, no install)
- **gitk** (bundled with Git)
- **GitKraken**, **SourceTree**, **Sublime Merge** (dedicated GUIs)

GHD's history view is fine for most work. For a Linux-kernel-scale repo with 500 branches, use a dedicated tool.

## Practical archaeology
Real scenarios you will use history for:
- **A bug appeared. When?** Bisect (Module in regression-testing-course; also possible via CLI on any repo).
- **Why is this weird line here?** Blame → read that commit's message → read the PR it was part of.
- **What did the release 3 months ago look like?** Checkout the tag or old commit (Module 25).
- **Who owns this module?** Blame → aggregate authors → talk to them.

Good history + good commit messages (Module 07) = productive archaeology. Bad messages = you learn nothing.
"""),
        "exercises": [
            ex(
                "11-1",
                "In `git-lab`, browse the History tab. Click each commit in order. Read the diff for each. Note: even short commits are readable if the messages and diffs are clear.",
                "Just navigate. Do not modify.",
                "You experienced walking through history the way a future maintainer will. This is the payoff of good commit hygiene from Module 07.",
            ),
            ex(
                "11-2",
                "Click your OLDEST commit. Shift+click your NEWEST. GHD shows the cumulative diff — the entire evolution of the repo. Useful for 'what has changed since we branched?'",
                "Compare-mode via shift-click.",
                "You see the total delta between the two points. On real projects, this is how you review 'what's new in this release?' or 'what has this branch done since main?'",
            ),
            ex(
                "11-3",
                "Right-click any commit → Copy SHA. Paste it somewhere (a note file). Now you can refer to this exact snapshot from anywhere — commit messages, PR discussions, chat.",
                "SHAs are the universal Git address.",
                "You have a 40-char (or short 7-char) identifier for this exact state of the repo. Anyone with access can `git show a3f7c2b` to see exactly what you're talking about. Permanent, unambiguous reference.",
            ),
            ex(
                "11-4",
                "Repository → View on GitHub → navigate to README.md → click Blame. Look at each line: who wrote it, when, and in what commit. Click a commit SHA → see the whole commit.",
                "GitHub's blame is the best view.",
                "Every line traceable to a person and a change. On a real project with 3 years of history, this is how you find the person who introduced a subtle behavior — talk to them, read the commit context, understand.",
            ),
            ex(
                "11-5",
                "Open in Terminal → run `git log --oneline --graph --all`. Compare to GHD's History view. Both show the same thing — different presentation. Use whichever suits the task.",
                "CLI and GUI are two views of the same data.",
                "The CLI graph is dense; GHD is spacious with per-commit diff view. For branch-topology understanding, the CLI graph is often clearer. For 'what did this commit change?', GHD is easier.",
            ),
        ],
    },
    # ────────────────────── PHASE 4: BRANCHING ──────────────────────
    {
        "id": "12",
        "title": "Why Branches (The Concept)",
        "level": "Intermediate",
        "summary": "The single most important feature in Git. Once you get branches, everything else clicks.",
        "body": md("""
## The problem branches solve
You are working on your main version. You want to try an experimental refactor. Options WITHOUT branches:
- Just edit main directly — if it breaks, you've broken main
- Copy the whole folder to `project_experimental/` — messy, hard to sync fixes
- Comment out the current code, write the new — instantly a mess

WITH branches:
- Create a branch called `experimental`
- Work freely on it
- If it works: merge back into main
- If it flops: delete the branch, main was never touched

Branches are the mechanism for parallel, safe, experimental work.

## The mental model (again, because it matters)
A branch is a **movable pointer to a commit**. Nothing more.

Starting state:
```
main → C
        ↑
A ← B ← C
```

Create branch `feature` (still at C):
```
main    → C
feature → C
        ↑
A ← B ← C
```

Switch to `feature` (HEAD moves):
```
main    → C
feature → C  ← HEAD
        ↑
A ← B ← C
```

Commit on `feature`:
```
main    → C
feature → D  ← HEAD
        ↑   ↑
A ← B ← C ← D
```

`main` still at C. `feature` moved to D. Two timelines from the same starting point.

## Why this is fundamentally cheap
In some VCSes (SVN, Perforce), branching means copying the entire codebase — slow, expensive. Git branches are just LABELS pointing at commits. Creating one is instant. Deleting one is instant. Switching between them is fast.

This changes how you work. You can:
- Branch for a 5-minute experiment
- Have 20 branches open at once
- Try 3 different approaches to the same problem, in parallel
- Not think twice about creating a branch

If you find yourself hesitating to create a branch, you're still thinking in old-VCS terms.

## What branches let you do (concretely)
### 1. Feature development in isolation
Every feature goes on its own branch. Main stays clean. When feature is done, merge back.

### 2. Bug fixes without disturbing feature work
Currently working on `big-feature`. Urgent bug in production. Create `hotfix-XYZ` from main, fix, merge, deploy. Return to `big-feature`.

### 3. Multiple people, same codebase
Alice on `alice-feature`, Bob on `bob-feature`. Neither disturbs main until their branch merges. They can also review each other's branches by switching.

### 4. Trying different approaches
Not sure if approach A or approach B is better? Do BOTH on separate branches. Compare. Keep the winner.

### 5. Preserving snapshots
Want to preserve "this is what we had at v1.0 release"? Tag it or branch it. `release-1.0` branch stays frozen; main moves on.

## The default branch: main
Historically, Git's default branch was called `master`. In 2020, GitHub (and most tools) transitioned to `main` as the default. Any new repo uses `main` unless you configure otherwise.

You may still see `master` in older repos or corporate environments — it works identically. Just a name.

## Long-lived vs short-lived branches
### Long-lived
- `main` — the always-shippable trunk
- `develop` — integration branch (in some workflows)
- `release-2.x` — kept alive to maintain older versions

### Short-lived
- `feature/add-dc-blocker` — created when work starts, deleted after merge
- `fix/issue-123` — same
- `experiment/try-lock-free-queue` — often deleted without merging

Rule of thumb: any branch that has been alive for more than a few weeks without merging is a problem. Old branches accumulate divergence, become painful to merge, get abandoned. Merge or delete.

## The tension: how many branches at once?
Too few: everyone edits main, conflicts constantly.
Too many: hard to keep track of what's where, stale branches proliferate.

Sensible: one active feature branch per person, plus long-lived main. If you spawn 5 branches while chasing a bug, delete the losers before moving on.

## What GHD shows about branches
The **Current Branch** dropdown lists:
- All local branches
- All remote branches (`origin/*`)
- Recently used branches at the top
- New branch button
- Compare branches button

Every operation (commit, push, pull) applies to the currently checked-out branch. Look at the dropdown before you commit to confirm you are on the right branch.
"""),
        "exercises": [
            ex(
                "12-1",
                "In your own words (1 paragraph): why is 'branch' the single most important feature of Git? What does it let you do that would otherwise be impossible?",
                "Think about experimentation and safety.",
                "Branches let you try changes IN PARALLEL to your main version without risk. You can experiment freely — commit progress, iterate, keep or throw away — and main is untouched until you deliberately merge. This is the mechanism that makes Git safe to use aggressively.",
            ),
            ex(
                "12-2",
                "Draw the state of the graph after: (a) initial commit A on main, (b) commit B on main, (c) create branch `feature`, (d) commit C on feature, (e) commit D on main, (f) commit E on feature. Which commits does `main` reach? Which does `feature` reach?",
                "Follow the pointer-moves-forward rule.",
                "```\nmain    → D\n            ↓\nA → B → D\n    ↓\n    C → E\n        ↑\nfeature → E\n```\nmain reaches: A, B, D. feature reaches: A, B, C, E. Common ancestor: B. This is what merge/rebase eventually reconciles.",
            ),
            ex(
                "12-3",
                "In `git-lab`, look at the Current Branch dropdown. Currently only `main`. Note the button 'New Branch' at the bottom of the list — we'll use it in Module 13.",
                "Just observe the UI.",
                "You see the dropdown structure: local branches, remote branches (currently just `origin/main`), option to create new. Every branch operation starts here.",
            ),
            ex(
                "12-4",
                "Discuss (in `git-lab/branch-strategy.md`): for a solo project with just you, how many branches at once feels right? For a 5-person team? For a 50-person company? Justify with what you know so far.",
                "There is no universal answer — this is about calibrating intuition.",
                "Solo: 1 active feature branch + main is enough. Occasionally 2-3 if you're exploring. 5-person: one per person minimum, plus release branches. 50-person: dozens active, strict naming conventions (`fix/`, `feat/`, `feature/username/`) so people can find their work. Volume scales with team size.",
            ),
        ],
    },
    {
        "id": "13",
        "title": "Creating, Switching, Deleting Branches in GHD",
        "level": "Intermediate",
        "summary": "The mechanical skills. Fast, safe branch management is table stakes.",
        "body": md("""
## Creating a branch
GHD → Current Branch dropdown → **New Branch**.
- **Name**: descriptive, no spaces, use hyphens (`add-dc-blocker`)
- **Based on**: usually `main` (or whatever branch you branched off from)
- **Create Branch** button

The new branch is created AND checked out (you are now on it). No commit yet — the branch points at the same commit as its base.

## Branch naming conventions
Common team conventions:
- `feature/add-dc-blocker` or `feat/add-dc-blocker`
- `fix/issue-123-crash-on-null` or `bugfix/...`
- `hotfix/rollback-broken-deploy`
- `experiment/try-new-algo`
- `docs/update-readme`
- `refactor/extract-audio-pipeline`

Some teams prefix with username: `alice/add-dc-blocker`. Others don't. Pick a convention, stick with it.

Rules:
- No spaces (use `-` or `_`)
- Case matters on Linux servers — stick to lowercase
- Slashes are just cosmetic (they create folders in the branch listing, useful for organization)

## Switching branches
- Current Branch dropdown → click any branch name
- GHD updates your working files to match that branch's state instantly
- Any uncommitted changes are carried with you (usually) or blocked (if they conflict with the target branch)

If you have uncommitted changes that would conflict:
- GHD warns you
- Options: commit changes here first, or stash them (Module 21), or discard them
- Safest: commit or stash before switching

## Deleting a branch
GHD → Current Branch dropdown → right-click branch → Delete...
- Local delete: removes local branch pointer only
- Also delete on remote: removes it from GitHub too (if it exists there)
- GHD warns if the branch has unmerged commits — deleting it means losing those commits

Cannot delete the branch you're currently on. Switch to `main` first.

## Renaming a branch
- Branch menu → Rename Branch
- Enter new name
- If the branch is on the remote too, GHD asks whether to also rename the remote branch

Renaming a shared branch that others are using is disruptive — coordinate with team.

## Comparing branches
- Branch menu → Compare to Branch
- Pick a branch to compare against
- See commits that are on one but not the other

Useful for: "what does my feature branch contain that main doesn't?" before opening a PR.

## The `origin/` prefix
When you fetch from the remote, GHD sees:
- `main` (local)
- `origin/main` (remote's copy of main)

These are separate references. Your local `main` moves when YOU commit. `origin/main` moves when you fetch (to reflect what's on the remote).

The branch dropdown shows both. Clicking `origin/main` switches to a detached view of it — usually not what you want. Prefer switching to a LOCAL branch.

## Tracking branches
When you clone, local `main` is set to "track" `origin/main`. This means:
- GHD knows push/pull go to `origin/main` by default
- Ahead/behind counts appear in the UI
- The Push/Pull button labels reflect the state

If you create a new local branch, on first push GHD asks whether to also create it on the remote (and set it to track). Usually yes.

## The "checkout" vocabulary
In Git-speak, switching to a branch is called **checking out** the branch. GHD hides this word (just says "switch"), but you'll see it everywhere in Git docs and error messages.
- "Check out branch X" = "switch to branch X"
- "Detached HEAD after checkout" = "you switched to a commit that isn't at the tip of any branch"

## Common branch scenarios and how to handle them
### "I started coding on main by accident"
- Uncommitted work only: create a new branch NOW — GHD carries your changes to the new branch. Commit there.
- Already committed to main locally, not pushed: create a branch from your current position, then reset main back to origin/main (Module 20).
- Already pushed to main: harder — see revert workflow (Module 20). Do not force-push shared main.

### "I want to bring a fix from another branch to my current one"
- Cherry-pick (limited in GHD): Branch menu → Cherry-pick (if available in your GHD version)
- Or via CLI: `git cherry-pick <sha>` — copies one commit onto your current branch
- Merge or rebase (Module 14) — brings ALL commits from the other branch

### "I want to save current work but switch branches"
- Stash it (Module 21) — GHD calls this "bring changes to a new branch" or use stash CLI
"""),
        "exercises": [
            ex(
                "13-1",
                "In `git-lab`, create a branch `feature/add-notes-file` off main. Verify: Current Branch dropdown shows it. History looks the same as main (branch is at the same commit).",
                "New Branch → name → Create.",
                "Branch created and checked out. History unchanged (branch points at the same commit as main). You are now free to commit here without touching main.",
            ),
            ex(
                "13-2",
                "On `feature/add-notes-file`, create a new file `notes/day-01.md` (create the `notes/` folder), add content, commit. Push (Publish branch — GHD offers this on first push). Verify on github.com: the branch appears in the branches list, main is unchanged.",
                "Standard branch → commit → push flow.",
                "New file exists on the feature branch. main branch on GitHub is UNCHANGED. Two parallel realities, both persisted.",
            ),
            ex(
                "13-3",
                "Switch back to `main` via the dropdown. Look at your working folder — `notes/day-01.md` is GONE. That's expected! It only exists on the feature branch. Switch back to `feature/add-notes-file` — the file returns.",
                "Switching branches literally rewrites your working files.",
                "Files appear and disappear as you switch. Nothing is lost — they're stored in the branch. This is why 'branch' is such a powerful mental model: you truly enter and leave parallel worlds.",
            ),
            ex(
                "13-4",
                "Create THREE more branches off main with different purposes: `experiment/pointless`, `docs/update-readme`, `fix/nothing-yet`. All from main, no commits on them yet. Notice: the branch dropdown now has clutter — this is why naming conventions matter.",
                "Sample branches for the delete exercise next.",
                "Four feature branches exist. The dropdown starts to be busy. Real projects have this problem constantly. Rule: create branches when needed, DELETE when done.",
            ),
            ex(
                "13-5",
                "Delete two of the empty branches: right-click in dropdown → Delete → confirm. Confirm delete on remote if pushed. Verify: dropdown is cleaner, github.com no longer shows them.",
                "Keep the branches directory tidy.",
                "Two branches gone locally and remotely. The remaining branches are ones with actual purpose. This is the hygiene: delete branches immediately after they've served their purpose (merged, or abandoned).",
            ),
        ],
    },
    {
        "id": "14",
        "title": "Merging: Bringing Branch Work Back to Main",
        "level": "Intermediate",
        "summary": "The other half of the branch superpower: getting your isolated work integrated back.",
        "body": md("""
## The merge concept
You have a feature branch with commits. Feature is done. You want those commits to be part of `main`. That is merging.

Two histories → one history.

## The two flavors of merge
### Fast-forward
If main has NOT moved since you branched, the merge is trivial — just advance main's pointer to your feature branch's tip:
```
Before:
    main    → B
    feature → D
              ↑
    A ← B ← C ← D
    ↑
    main (also here)

After fast-forward merge:
    main    → D
    feature → D
              ↑
    A ← B ← C ← D
```
No new commit needed. Main's label just moves forward to catch up. History looks completely linear as if you always committed on main.

### True merge (3-way merge)
If main moved while you were working on feature (someone else pushed to main), merging must create a MERGE COMMIT that has TWO parents (one from each history):
```
Before:
    main    → E
    feature → D
                    E (main's advance)
                    ↑
    A ← B ← C ← D
                    ↓
                    D (feature)

After merge:
    main    → M (merge commit)
    feature → D (unchanged)

    A ← B ← C ← D ←┐
              ↓    │
              E ← M
                  ↑
                  main
```
The merge commit M has TWO parents: D (from feature) and E (from main). It records "these two histories joined here."

## Doing a merge in GHD
1. Switch to the branch you want to merge INTO (usually `main`)
2. Branch menu → **Merge into current branch...**
3. Pick the branch you want to merge FROM (e.g., `feature/add-dc-blocker`)
4. GHD shows what will happen (how many commits, any conflicts detected)
5. Click **Create a merge commit** (or **Fast-forward** if available)
6. If clean: merge is complete, main updated
7. If conflicts: GHD guides you through resolution (Module 15)

## Pull Request merges (recommended)
For team projects, merging directly is uncommon. The standard flow:
1. Push your feature branch
2. Open a Pull Request on GitHub (Module 17)
3. Reviewers approve
4. Click "Merge" on the PR page
5. Optionally delete the feature branch

This gives you code review + discussion + merge commit + audit trail — all on the website. Preferred over direct local merges for shared projects.

## Merge vs rebase (preview)
Merge PRESERVES history:
```
main ─── A ─── B ─── M
                    /
feature ──── C ─── D
```
Rebase REWRITES history to be linear:
```
main ─── A ─── B ─── C' ─── D'
```
- Merge: honest history, easier to understand, but many merge commits over time
- Rebase: clean linear history, but rewrites commits (new SHAs)

Team convention decides which is default. GHD's Branch menu has both options. See Module 22 for the rebase warnings.

## After merging: what to do with the feature branch
Once merged, the branch has done its job. Options:
- **Delete it** — clean up. GHD offers this at merge time or later.
- **Keep it around** — useful if the branch is a release marker or you might revisit.

Convention: delete short-lived feature branches after merge. Keep long-lived release branches.

## Aborting a merge in progress
Started a merge, hit conflicts you don't want to resolve right now?
- GHD's merge conflict dialog has an **Abort Merge** button — returns to the pre-merge state
- Or CLI: `git merge --abort`

Nothing is lost. You can try again later.

## Fast-forward vs no-fast-forward (a stylistic choice)
When a fast-forward is possible, some teams prefer to FORCE a merge commit anyway — "even trivial merges get a commit so we can see the branch topology in history."

GHD → Branch menu → merge dialog has options for this. Some teams configure it globally (`git config merge.ff false`). This is a taste question — either is fine.

## Merge commit messages
Auto-generated: "Merge branch 'feature/xyz' into main". Usually fine. You can customize when merging via GHD or CLI. For PR merges via GitHub, the merge commit message is customizable in the UI.
"""),
        "exercises": [
            ex(
                "14-1",
                "In `git-lab`, on `feature/add-notes-file` (from Module 13), verify you have at least one commit. Switch to `main`. Branch menu → Merge into current branch → pick `feature/add-notes-file` → Merge. Verify: main now has the feature's commits and files.",
                "Standard merge into main workflow.",
                "main now contains `notes/day-01.md`. History shows either a fast-forward (linear) or a merge commit (join point) depending on whether main had moved. Either result is 'merge done.'",
            ),
            ex(
                "14-2",
                "Push main. Verify github.com/YOUR/git-lab shows the merged file on the main branch page.",
                "Merged work isn't shared until pushed.",
                "The merge appears on GitHub. This is the typical last step of a local merge. In PR-based workflows (Module 17), GitHub itself does the merge and no push is needed after.",
            ),
            ex(
                "14-3",
                "Create the diverged scenario: on main, edit README.md (add a line), commit, push. On `feature/add-notes-file` (via switch), edit README.md DIFFERENTLY at the same lines, commit. Now try to merge feature into main. GHD detects conflict.",
                "Sets up Module 15's conflict resolution.",
                "GHD stops with 'conflicts detected'. This is exactly what happens when two branches independently modify the same lines. Do not resolve yet — save this state for Module 15 (or abort the merge and revisit later).",
            ),
            ex(
                "14-4",
                "Delete the merged `feature/add-notes-file` branch. Right-click → Delete → confirm. Delete on remote too. Verify GitHub no longer lists it.",
                "Clean-up after successful merge.",
                "Branch gone from local and remote. History is preserved (the commits are now part of main's history). The BRANCH POINTER is gone but the commits themselves are safe.",
            ),
            ex(
                "14-5",
                "Discuss: for a solo project, do you need PR-based merges, or is direct local merge fine? For a team of 5?",
                "Direct is faster; PR is more disciplined.",
                "Solo: direct merges into main are fine — you're your own reviewer. PR flow adds ceremony without value. Team: PR is nearly mandatory. It gives code review, discussion, CI status checks, and an audit trail of every change. Even 2-person teams benefit.",
            ),
        ],
    },
    {
        "id": "15",
        "title": "Conflict Resolution in GitHub Desktop",
        "level": "Intermediate",
        "summary": "When two branches modify the same lines, Git can't merge automatically. Here's exactly what to do.",
        "body": md("""
## What a conflict actually is
Git can auto-merge:
- Changes to different files
- Changes to different regions of the same file
- Changes that don't overlap

Git CANNOT auto-merge:
- Both branches modified the SAME lines (both changed, differently)
- One branch deleted a file, the other modified it
- Both created a file with the same name but different content

In those cases, Git says "I can't decide — a human must." That is a merge conflict.

## What conflicts look like in files
When Git hits a conflict, it writes BOTH versions into the file, separated by markers:
```
<<<<<<< HEAD
This is what main had.
=======
This is what feature had.
>>>>>>> feature/add-notes
```
- Everything between `<<<<<<<` and `=======` = the version from your CURRENT branch (main)
- Everything between `=======` and `>>>>>>>` = the version from the branch being merged (feature)

Your job: edit the file to be what it SHOULD be after the merge, and remove the markers.

## What GHD shows during a conflict
GHD stops the merge and displays:
```
[Conflict UI]
  ⚠ 3 conflicts in 1 file
  ├─ README.md   [Resolve using external editor] [Use main] [Use feature/x]
```
Three options per file:
1. **Resolve using external editor** — opens the file in your default editor (VS Code, etc.), you edit manually
2. **Use main** — accept the main branch version wholesale, discard feature's changes
3. **Use feature/X** — accept feature's version wholesale, discard main's changes

## The three resolution strategies
### Strategy 1: Manual edit (most common)
1. Click "Resolve using external editor" → file opens in your editor
2. VS Code (and most modern editors) show the conflict with nice UI: "Accept Current Change", "Accept Incoming Change", "Accept Both", "Compare Changes"
3. Edit the file to be what you want (may involve keeping some of each)
4. REMOVE all `<<<<<<<`, `=======`, `>>>>>>>` markers
5. Save the file
6. Return to GHD — conflict marker changes to "resolved"

### Strategy 2: Use ours (main)
Accept your side entirely, throw away the other side's changes.
- Reason: you know your version is correct; the other side's change was wrong
- Risk: you may lose intentional changes

### Strategy 3: Use theirs (feature)
Accept the other side entirely.
- Reason: their version is the correct one; your local was outdated or wrong
- Risk: you may throw away your own work

Most real conflicts require Strategy 1 (manual) — usually you want SOME of each side.

## Completing the merge after resolution
1. Resolve all conflicted files
2. GHD's UI updates to "All conflicts resolved"
3. Click **Continue merge** (or the merge completes automatically)
4. GHD creates the merge commit
5. History now shows the merge

## VS Code's conflict UI (if that's your editor)
VS Code detects Git conflict markers and adds inline buttons above each conflict block:
- **Accept Current Change**
- **Accept Incoming Change**
- **Accept Both**
- **Compare Changes** (opens a side-by-side diff)

Very fast for simple conflicts. For complex ones, still edit manually.

## Preventing conflicts
Conflicts happen when parallel work touches the same code. Reduce them by:
- **Small, frequent commits** — less opportunity for overlap
- **Communication** — "I'm refactoring the audio pipeline this week" so others avoid it
- **Feature flags** — hide in-progress features so branches can merge often
- **Rebase often** — pull main's changes into your feature branch regularly so conflicts stay small
- **Modular code** — code in separate files/modules rarely conflicts

Even with all this, conflicts will happen. Skill: resolve them calmly and correctly.

## When to abort
If a conflict is complex and you're not sure what the resolution should be:
- GHD merge UI has an **Abort merge** button
- Aborts cleanly — returns to pre-merge state
- Talk to the branch's author about how to reconcile
- Retry the merge later with a plan

Do not GUESS at conflict resolution. A wrong resolution silently drops changes.

## Special conflicts
### Modified/deleted
One side modified a file, the other deleted it. GHD asks: keep modified version or accept deletion?
Manual: if the file is truly obsolete, accept deletion. If the modification is important, keep it.

### Renamed/renamed
Both sides renamed the same file to different names. Git detects this. Resolution: pick a name (or a new one), keep the content.

### Binary files
Cannot auto-merge — one side wins entirely. GHD asks which. For truly binary files (images, PDFs), this is the only option.

## After the merge: verify
Once merged, RUN THE TESTS. Just because the merge completed and compiled doesn't mean the LOGIC is correct. Conflicts can be resolved syntactically-correctly but semantically-wrongly.

If you have a good regression test suite (see the Regression Testing course), this catches broken merges immediately.
"""),
        "exercises": [
            ex(
                "15-1",
                "Set up a real conflict: In `git-lab`, on main, edit README.md — change line 1 to 'MAIN VERSION'. Commit. Create branch `feature/conflict-test`. Switch to it. Edit README.md — change line 1 to 'FEATURE VERSION'. Commit. Switch back to main. Try to merge `feature/conflict-test` → GHD says conflict.",
                "Deliberately conflicting edits.",
                "GHD conflict UI appears. This is the state you must resolve. Do not skip this — the mechanical practice matters.",
            ),
            ex(
                "15-2",
                "Click 'Resolve using external editor'. See the conflict markers in your editor. Edit to keep BOTH lines: `MAIN VERSION and FEATURE VERSION combined`. Remove all `<<<<<<<`, `=======`, `>>>>>>>` markers. Save.",
                "Manual resolution — the common case.",
                "File is clean, markers gone, both intents captured. Back in GHD, conflict marks as resolved. Click Continue Merge. Merge commit created. Look at history: you can see the merge.",
            ),
            ex(
                "15-3",
                "Repeat with a different pair of files: this time use the 'Use main' button on one file and 'Use feature/X' on another. Observe: you skip manual editing entirely — one side wins wholesale.",
                "Sometimes wholesale-accept is right. Not usually.",
                "Two files, each resolved by picking one side. Faster than manual editing. Use when the other side's change is definitely wrong or obsolete — not as a shortcut for real conflicts.",
            ),
            ex(
                "15-4",
                "Practice abort: create another conflict scenario (any way you like). Start merge → see conflicts → click 'Abort merge'. Verify: back to clean state, no half-merge dangling.",
                "Abort is your escape hatch.",
                "State returns to pre-merge. Files are as they were before you started. Safe. Now you can regroup, plan the resolution, and try again later.",
            ),
            ex(
                "15-5",
                "Discuss: after resolving a merge conflict, WHY should you run tests before committing the merge?",
                "Conflict resolution can be syntactically OK but semantically wrong.",
                "Two changes may resolve to code that compiles but produces the wrong behavior. Example: main changed default value from 0.5 to 0.7; feature changed same variable name and initial calc. Resolving by keeping feature's line loses main's intentional value change. Only tests catch this. Merge = pause point for verification, not a done-signal.",
            ),
        ],
    },
    {
        "id": "16",
        "title": "Merge vs Rebase (When Each Is Right)",
        "level": "Intermediate",
        "summary": "Two ways to integrate branches. Merge preserves history, rebase rewrites it. Choose per situation.",
        "body": md("""
## The two integration strategies visualized

### Merge (default)
```
Before:
    main    ─── A ─── B ─── E
                       \\
    feature             C ─── D

After merge:
    main    ─── A ─── B ─── E ─── M
                       \\        /
    feature             C ─── D
```
- Creates a new commit `M` with TWO parents
- Preserves the fact that feature was a branch
- History shows the "shape" of parallel work

### Rebase (opt-in)
```
Before:
    main    ─── A ─── B ─── E
                       \\
    feature             C ─── D

After rebase feature onto main:
    main    ─── A ─── B ─── E
                             \\
    feature                   C' ─── D'
```
- Rewrites C and D as C' and D' (new commits, new SHAs)
- Pretends feature was always based on E
- Linear history, no branch topology visible

## When to prefer merge
- On shared branches that others have pulled
- When you WANT to see the branch topology in history
- When the branch has many commits — merge captures "here's where feature joined"
- Default in most enterprise / regulated environments (audit trail)

## When to prefer rebase
- On YOUR OWN branch, before opening a PR — cleans up your history to be tidy
- When the team prefers linear history for `git log` readability
- When the feature had lots of tiny "fix typo" / "WIP" commits you want to squash before merging

## The golden rule
> Never rebase commits that are already public and used by others.

Rebase rewrites commit SHAs. If someone else has pulled the OLD SHAs and made their own commits on top, your rebased branch will be inconsistent with theirs. When they pull, they get a mess.

Safe: rebase YOUR OWN feature branch before pushing (or before others pull it).
Unsafe: rebase `main` or `develop` or anything shared. Merge those.

## GHD's rebase UI
Branch menu → **Rebase current branch...** → pick base branch.
GHD walks through:
- Preview: how many commits will be rebased
- If conflicts occur: resolve per commit (same UI as merge conflicts, done once per commit)
- Once done: your branch has new SHAs, based on the chosen base

Push after rebase requires force-push (because remote has old SHAs). GHD prompts you. Use `--force-with-lease` via CLI for safety, or accept GHD's prompt if you're sure.

## Rebase-onto-main workflow (recommended for feature branches)
```
1. Work on feature/xyz, commit locally as usual
2. Meanwhile main advances (other people push)
3. Before opening PR: switch to feature/xyz, rebase onto main
   - Feature commits are replayed on top of latest main
   - Any conflicts resolved
4. Force-push feature/xyz (safe: nobody else uses this branch)
5. Open PR — the diff is clean, the base is current
```
Result: PR reviews are easier because the diff is exactly what you'd add to main.

## Squash merge (a third option)
GitHub's PR page offers three merge strategies:
- **Merge commit** — standard merge, creates M commit (default)
- **Squash and merge** — combines ALL feature commits into ONE commit on main
- **Rebase and merge** — rebases feature onto main, no merge commit

Squash is popular for teams that want clean main history but don't rebase during development. Feature branch may have 15 messy commits; squash flattens them to 1 clean commit on main.

Choose based on team preference. GitHub repo settings can restrict which options are allowed.

## The history reading test
After the smoke settles, look at `git log --oneline --graph --all` (or GHD's history):
- Lots of merge commits and criss-crossing lines = merge-heavy team
- Linear log with occasional feature branches = rebase-heavy or squash-heavy team

Neither is wrong. Consistency matters more than the choice.

## Interactive rebase (advanced)
Beyond simple "rebase onto X" is **interactive rebase** (`git rebase -i`) — lets you reorder, squash, edit, or drop individual commits before publishing.

Example workflow: you made 5 commits on feature; the middle 3 are all "fix typo". Interactive rebase lets you squash them into 1 commit before opening the PR.

GHD does NOT have interactive rebase in the UI (as of writing). Use CLI:
```bash
git rebase -i main    # opens editor with commit list
```
See Module 23 for the CLI escape hatch, or use GitHub's UI (which offers squash on PR merge).

## The single most useful mental model
- Merge = **honest** history: "this branch existed, these commits happened, then joined"
- Rebase = **tidy** history: "here's a clean linear story"

Some teams (and some individuals) value honesty; others value tidiness. Both are defensible. Adapt to your team.
"""),
        "exercises": [
            ex(
                "16-1",
                "In `git-lab`: create branch `feature/rebase-demo`. Make 2 commits on it. Meanwhile switch to main, make 2 different commits. Now switch back to `feature/rebase-demo`. Branch menu → Rebase current branch → base = main. Observe: your commits are 'replayed' on top of main.",
                "Direct experience with rebase.",
                "Feature's commits have new SHAs. They now appear AFTER main's commits in the linear history. If you draw the graph, it's a single line — no branching visible.",
            ),
            ex(
                "16-2",
                "Compare: create ANOTHER branch `feature/merge-demo`, 2 commits, plus 2 different commits on main. Switch to main → Merge into current branch → feature/merge-demo. History now has a merge commit M with two parent lines.",
                "Same starting scenario, different integration.",
                "Merge produced a commit M with two parents. History graph shows the branch/join topology. This is visually different from the rebase result — same code state, different history story.",
            ),
            ex(
                "16-3",
                "Discuss (in `git-lab/merge-vs-rebase-notes.md`): given you now understand both, what would you default to? What convinces you to change to the other?",
                "Personal calibration.",
                "Common answer: 'merge by default, rebase MY OWN feature branches before opening PRs to clean up history.' This is the middle path — honest shared history, tidy personal branches. Different teams choose differently, all reasonable.",
            ),
            ex(
                "16-4",
                "Read the module's warning: 'Never rebase commits that are already public and used by others.' In your own words, explain why. What breaks if you do?",
                "Think about SHAs and other people's local repos.",
                "Rebase rewrites SHAs. If Alice already pulled your old commits and started working on top of them, her local commits reference the OLD SHAs. When you force-push new SHAs, her commits are 'orphaned' — pointing at commits that no longer exist on origin. Her next pull is a mess. Rule: rebase your private history, merge public history.",
            ),
            ex(
                "16-5",
                "On github.com, open Settings → General → Pull Requests. Look at the three merge options. Enable all three, then disable them one by one — see how each corresponds to a strategy from the module.",
                "GitHub repo settings control what PR mergers can do.",
                "You see the three options: Merge commit, Squash and merge, Rebase and merge. Restrict them per team convention. Common: enable 'Squash' + 'Merge commit', disable 'Rebase' (to force explicit merge commits).",
            ),
        ],
    },
    # ────────────────────── PHASE 5: COLLABORATION ──────────────────────
    {
        "id": "17",
        "title": "Pull Requests from GHD",
        "level": "Intermediate",
        "summary": "The primary collaboration mechanism on GitHub. PR = 'propose to merge this branch into that branch, discuss first'.",
        "body": md("""
## What a Pull Request is
A **Pull Request (PR)** is a proposal on GitHub:
- "I made these commits on branch X"
- "Please review them"
- "If approved, merge into branch Y (usually main)"

It is where:
- Code review happens
- CI runs
- Team discussion is captured
- Changes get approved and integrated

PRs are the collaboration heartbeat of every modern software team.

## The PR lifecycle
```
1. Create a feature branch, make commits, push
2. Open a Pull Request (from feature branch → main)
3. CI runs automatically (Module 28)
4. Reviewers read the diff, leave comments
5. Author responds to comments, pushes fixes (branch updates in PR)
6. Reviewers approve
7. Someone (author or maintainer) clicks Merge
8. Feature branch is deleted (usually)
9. Main has the changes
```

## Opening a PR from GHD
1. Push your feature branch (Module 13)
2. GHD offers a **Create Pull Request** button (top area)
3. Click → browser opens to GitHub's new PR page pre-filled
4. Fill in:
   - **Title**: what the PR does (similar to a commit summary but scope-wider)
   - **Description**: context, what changed, screenshots, links to issues
5. Choose reviewers (if applicable)
6. Click **Create pull request**

That's it. PR now exists on GitHub for review.

## Writing a good PR description
A minimal template:
```
## What
One-paragraph summary of what this PR changes.

## Why
Why is this change needed? Link to issue: Closes #123.

## How
High-level approach. Any trade-offs? Alternatives considered?

## Testing
How you verified this works. Manual steps, added tests, before/after screenshots.

## Notes for reviewers
Anything specific to look at. Known limitations. Follow-ups planned.
```
Not every PR needs every section — but for anything non-trivial, cover them.

## PR titles
Same rules as commit summaries (Module 07):
- Imperative mood: "Add DC blocker" not "Added DC blocker"
- ~50-72 chars
- Capitalized

If your team uses Conventional Commits (feat:, fix:, etc.), same in PR titles.

## Linking issues
In the PR description, use closing keywords:
```
Closes #123
Fixes #456
Resolves #789
```
When the PR merges, GitHub AUTO-CLOSES the linked issues. Very handy.

Also useful: `Refs #123` (mentions but doesn't close), `See #456` (informational).

## Draft PRs
Not ready for review, but want CI to run or want teammates to see WIP?
- On the New PR page, click the dropdown next to "Create pull request" → **Create draft pull request**
- Draft PRs cannot be merged
- Reviewers know it's WIP
- CI still runs

Convert draft → ready when you're done: button on the PR page.

## Pushing more commits to an existing PR
- Just push more commits to the same feature branch (from GHD)
- The PR auto-updates — new commits appear in the PR
- Any old review comments on unchanged lines remain; comments on changed lines become "outdated"
- Reviewers see the changes and can re-approve

This is the normal cycle: push initial version → review comments → address them → push again → re-review → merge.

## Requesting reviewers
On the PR page (right sidebar) → Reviewers. Type a username. GitHub notifies them.
- **CODEOWNERS file** (Module 27) can auto-assign based on which files changed
- Multiple reviewers can be requested; approval requirements set in branch protection (Module 27)

## Handling review comments
Reviewers leave comments inline on specific lines. Author sees them:
- On the Files Changed tab of the PR
- Via email/notification
- In GHD (limited — comments don't appear in GHD, use the web)

Address by:
- Making changes locally, committing, pushing → new commits appear in PR
- Replying to comments in the web UI ("Fixed in abc1234")
- Marking conversations as resolved when addressed

## Merging a PR
Once approved and CI green:
- Click **Merge pull request** on the PR page
- Choose merge strategy (Merge commit / Squash / Rebase — Module 16)
- Optional: edit the merge commit message
- Click **Confirm merge**
- Optional: click **Delete branch** to clean up

Merge happens on GitHub (not locally). Your local main is NOT auto-updated — you must fetch/pull to see the merged commits locally.

## After merge cleanup
- Delete the feature branch (offered right after merge)
- Locally: switch to main, pull, delete local feature branch
- Update any linked issues (usually auto-closed by "Closes #X")
"""),
        "exercises": [
            ex(
                "17-1",
                "In `git-lab`: create branch `feat/pr-practice`. Make 2 commits (any changes). Push. Verify GHD offers 'Create Pull Request' → click. Browser opens to New PR page.",
                "The GHD → browser handoff for PR creation.",
                "You are at GitHub's New PR page. All the fields are pre-filled based on the branch's commits. This is the standard entry to PR creation.",
            ),
            ex(
                "17-2",
                "Fill in a proper PR: Title 'Add PR practice branch' (imperative, concise). Description using the template from the module (What / Why / How / Testing / Notes). Create. Verify: PR page exists, shows your commits.",
                "Practice the description template.",
                "Your PR is a good example of PR hygiene. Reviewers can understand what you changed and why without reading the code first. This is what makes reviews FAST — good context up-front.",
            ),
            ex(
                "17-3",
                "Since you're solo, self-review: click 'Add your review' → leave a comment on a specific line ('nit: rename this variable'). Then in GHD, make the requested change, commit, push. Refresh the PR — comment persists, new commit appears.",
                "Full comment → fix → re-push loop.",
                "You experienced the reviewer/author cycle from both sides. On real teams, the review can go 3-10 rounds before merge. Each round is: comment → fix → push → resolve. GHD is where you make fixes; GitHub is where discussion happens.",
            ),
            ex(
                "17-4",
                "Merge the PR: click Merge pull request → Confirm merge → Delete branch. In GHD, switch to main and pull. Verify: the PR's commits are now in main, feature branch gone.",
                "Standard end-of-PR cleanup.",
                "Merge complete on GitHub. Local main updated after pull. Feature branch deleted on remote (and locally, if you delete it). This is the full round-trip: local branch → PR → review → merge → clean up.",
            ),
            ex(
                "17-5",
                "Open ONE MORE PR — this time as a DRAFT (dropdown next to Create). Verify: PR page shows 'Draft', Merge button is disabled. Convert to Ready for Review. Then close it (Close pull request without merging — for practice, no need to actually merge).",
                "Draft vs ready-for-review states.",
                "Draft is a signal: 'work in progress, feedback welcome but not ready'. Very useful for gathering early feedback. Close without merge = 'never mind, not going in.' Both states are non-destructive — no code lost.",
            ),
        ],
    },
    {
        "id": "18",
        "title": "Reviewing Pull Requests",
        "level": "Intermediate",
        "summary": "Being a good reviewer is a skill. Reviews should catch bugs, improve design, and not personally attack authors.",
        "body": md("""
## The reviewer's job
When someone asks you to review their PR, you check:
1. **Correctness** — does the code do what it claims? Any obvious bugs?
2. **Design** — is the approach reasonable? Are there simpler ways?
3. **Readability** — will future maintainers understand this?
4. **Tests** — are behaviors adequately guarded (see Regression Testing course)?
5. **Consistency** — matches team conventions (naming, style, structure)?
6. **Security** — any obvious vulnerabilities (SQL injection, path traversal, secrets)?

You are NOT checking:
- Personal style disagreements ("I would have named it differently")
- Nitpicks on things machine-formatters can handle (auto-linters)
- Rearranging things that work fine

## The GitHub review UI
On any PR → **Files changed** tab.
- See the full diff, file by file
- Click line numbers to add inline comments (green `+` appears)
- Comments are queued as a REVIEW, not sent immediately
- When done, click **Review changes** (top-right)
- Choose: **Comment** (feedback only), **Approve**, or **Request changes**
- Optionally add a summary comment
- Submit review

This queuing is important: authors get ONE notification with all your comments, not spam of 20 individual ones.

## Types of comments (a common convention)
Prefix your comments with type indicators to signal severity:
- **nit:** — nitpick, not blocking (e.g., "nit: extra whitespace")
- **suggestion:** — you propose a change, but not required (e.g., "suggestion: use a dict here")
- **question:** — you don't understand something (e.g., "question: why negate here?")
- **issue:** — this must be fixed before merge (e.g., "issue: this leaks memory on error path")
- **blocking:** — do not merge until resolved

This clarity helps authors prioritize: fix all `issue:` immediately, consider `suggestion:`, address `nit:` if time.

## The three review outcomes
### Approve
"Looks good, safe to merge." Doesn't mean perfect — means acceptable for the codebase.
### Request changes
"Fix these before merge." Blocks the merge until you re-review (with GitHub branch protection).
### Comment
Neutral — providing feedback without a strong stance. Doesn't block merge.

Do NOT approve without reading. Do NOT request-changes for nits (comment instead).

## What good comments look like
Bad:
> "This is wrong."

Good:
> "issue: the loop exits before processing the last element when input has odd length. Add `n >= last` check. Reproduce: `filter([1,2,3])` returns `[?,?]` instead of `[?,?,?]`."

Bad:
> "Ugly code."

Good:
> "suggestion: this 40-line function could be split into `parse()` and `process()`. Would make testing easier. Not blocking, but consider before merge."

Give ACTIONABLE feedback with context. Vague criticism is worse than silence.

## Suggested changes (GitHub's built-in feature)
For small edits (a single line or few), you can suggest the exact new text:
```
```suggestion
new content here
```
```
The author can click "Commit suggestion" to apply your edit directly. Fastest for typos, one-liner fixes.

## Reviewing large PRs
When a PR is 500+ lines of diff:
- Ask if it can be broken up (usually yes — most large PRs are actually 3-4 unrelated changes)
- If not: review it in TWO passes. Pass 1: overall structure. Pass 2: line-by-line.
- Read tests first — they show intended behavior
- Do not skip files because they're "just tests" — tests are code too

## Reviewing as an author (self-review)
Before requesting reviewers, review your OWN PR:
- Read through Files Changed
- Look for debug prints, TODO comments you forgot, commented-out code
- Confirm the description matches what you actually did
- Push fixes for anything you find

This catches half the review comments before others waste time.

## When you disagree
As author: reviewers occasionally push for changes you don't agree with. Options:
- Discuss in comments: "I chose X because Y — thoughts?"
- Compromise
- Escalate to a tech lead if truly stuck

As reviewer: if the author pushes back with a good reason, update your position. "OK, that makes sense — approving."

Reviews are collaborative, not combative. Both sides want the same thing: code that works and is maintainable.

## The tempo
- **Small PR (<200 lines)**: review within a few hours
- **Medium PR (200-500 lines)**: within a day
- **Large PR (500+)**: within 2-3 days, or ask for a split

Slow reviews block teammates and cause context-loss ("what was this again?").

## Blocking vs non-blocking approvals
Some teams require 2 approvals; others 1; solo devs need none. Configured in branch protection (Module 27).

If you approve WITH suggestions, be clear: "Approving; feel free to merge without addressing the nits."

If you request changes, the author must re-request review after fixing.
"""),
        "exercises": [
            ex(
                "18-1",
                "Create a PR in `git-lab` (any small change). Then review it as if it were someone else's — Files changed → add at least 3 inline comments prefixed with `nit:`, `suggestion:`, `question:`. Submit as Comment (not Approve/Request changes).",
                "Practice giving actionable, prefixed comments.",
                "You practiced the review UI. Real reviews are the same mechanic on other people's code. The prefixes signal urgency — authors know which comments are optional vs blocking.",
            ),
            ex(
                "18-2",
                "On the same PR, add a **suggested change**: use the `\\`\\`\\`suggestion` block syntax to propose new text for one line. Verify the author (you) can click 'Commit suggestion' to apply.",
                "GitHub's built-in code suggestion feature.",
                "Suggestion accepted with one click. Faster than 'change X to Y' comments. Great for typos, small fixes.",
            ),
            ex(
                "18-3",
                "Read a public open source PR (any project on GitHub). Look at the review comments. How do the reviewers phrase things? What tone? What level of detail?",
                "Learn by observation.",
                "You see real professional review patterns: specific, actionable, respectful, prefixed. Sometimes brief ('nit: typo'), sometimes deep ('this approach won't scale because...'). Absorbing these patterns is how you become a good reviewer.",
            ),
            ex(
                "18-4",
                "Discuss (in `git-lab/review-checklist.md`): write YOUR personal checklist for reviewing a PR. 8-10 items you check every time.",
                "Habits > memory. Write it down.",
                "Sample checklist:\n1. Read PR description first — do I understand intent?\n2. Read tests — do they cover the claim?\n3. Read implementation — does it do what the PR says?\n4. Check for obvious bugs (nil deref, off-by-one, error paths)\n5. Naming — clear?\n6. Structure — sensible?\n7. Any commented-out code, debug prints, TODOs?\n8. Any secrets or hard-coded credentials?\n9. Docs updated if needed?\n10. Submit review with prefixed comments.",
            ),
        ],
    },
    {
        "id": "19",
        "title": "Forks and Contributing to Other People's Repos",
        "level": "Intermediate",
        "summary": "The fork/clone/PR loop — how open source contributions work at scale.",
        "body": md("""
## The problem forks solve
You want to contribute to someone else's public repo (say, an open source project). You can't push directly — you don't have write access. Solution: **fork it**.

A fork is YOUR OWN COPY of the repo, on GitHub, under your username. You can push freely there. Then propose your changes back to the original via a PR.

## The workflow
```
1. Find the repo on GitHub (e.g., github.com/torvalds/uemacs)
2. Click Fork (top-right of the repo page)
3. GitHub creates github.com/YOU/uemacs — a copy under your account
4. Clone YOUR fork to your machine (Module 09)
5. Add the original repo as a "remote" called `upstream`
6. Create a branch, commit, push to YOUR fork
7. Open a PR from YOUR fork → the ORIGINAL repo
8. Original maintainer reviews, requests changes, or merges
```

## Adding upstream in GHD
GHD does this partially:
- When you fork on GitHub and clone in GHD, GHD sees the fork
- To add "upstream" (the original), use the CLI:
```bash
cd path/to/your/fork
git remote add upstream https://github.com/torvalds/uemacs.git
git fetch upstream
```
Now your local repo knows about both:
- `origin` = your fork
- `upstream` = the original

## Keeping your fork in sync
Over time, the original repo (upstream) moves forward. Your fork gets stale. Sync periodically:
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```
Or in GHD:
- Sync via CLI as above, OR
- On the GitHub website: your fork's page has a **Sync fork** button that pulls upstream into your main

Sync your fork before starting new work — otherwise your PR is based on an old version.

## Opening a PR from your fork
1. Push your feature branch to your fork
2. On GitHub, navigate to the ORIGINAL repo
3. GitHub often detects your recent push and offers "Compare & pull request"
4. Or manually: Pull Requests → New → "compare across forks" → base = original/main, compare = yourfork/feature-branch
5. Fill in title/description
6. Create pull request

The PR shows up on the ORIGINAL repo's PR list. The maintainer can review and merge.

## Fork-specific etiquette
### Read CONTRIBUTING.md first
Many repos have a `CONTRIBUTING.md` at the root explaining:
- Coding style
- Commit message conventions
- Branch naming
- PR template requirements
- Testing requirements

Read it BEFORE opening a PR. Following the conventions massively increases merge chances.

### Small PRs win
A 50-line focused PR: merged in a week.
A 5000-line "big improvement" PR: probably never merged.

Split large contributions into smaller, focused PRs. Each does ONE thing.

### Discuss first for big changes
Before spending 40 hours on a feature nobody asked for, open an ISSUE proposing it. Maintainer's response tells you whether to proceed. Saves both sides time.

### Respond to review promptly
If a maintainer reviews within a week and you take a month to respond, they may lose interest. Contributions that go stale get closed.

## The upstream sync habit
Every time before starting a new feature branch:
```bash
git fetch upstream
git checkout main
git merge upstream/main   # or: git rebase upstream/main
git push origin main
git checkout -b feature/new-thing   # branch off latest
```
This keeps your fork current so your PR diffs are clean.

## Contributing without forking
For repos where you ARE a collaborator (given write access):
- No fork needed
- Just create a branch directly on the origin repo
- Open PR to main

Forks are specifically for when you don't have write access. Inside your own org, direct branches are more common.

## Deleting your fork
When you're done contributing:
- Fork's GitHub page → Settings → Danger Zone → Delete this repository
- Your local clone is unaffected (you can also delete)

Or keep it around forever — GitHub has no fork limit on free accounts.

## Fork network on GitHub
On any repo, click "Insights" → "Forks" to see all forks. Popular repos have thousands. This is how open source thrives: every fork is a potential contributor.

## When forks diverge (become their own project)
Sometimes a fork becomes the "real" version:
- **XFree86 → X.Org** (2004)
- **MySQL → MariaDB** (2009)
- **OpenOffice → LibreOffice** (2010)

These started as forks, then became the primary project after the original stagnated. Forks are also insurance against bad governance.

## Summary
- Fork = your own remote copy of a repo you don't own
- Contribute via: fork → clone → branch → commit → push (to fork) → PR (to original)
- Sync with upstream regularly
- Read CONTRIBUTING.md before submitting
- Keep PRs small and focused
"""),
        "exercises": [
            ex(
                "19-1",
                "Find a small, active open source repo on GitHub (not too popular — you're less likely to submit a real PR). Suggestion: search for repos with `first-good-issue` label. Fork it. Clone your fork.",
                "Real practice on a real repo.",
                "You have a fork under your username and a local clone of it. You can now commit freely without asking permission — because you're pushing to YOUR fork, not the original.",
            ),
            ex(
                "19-2",
                "Add upstream remote via CLI: `git remote add upstream <original-url>`. Verify with `git remote -v` — you see both origin (your fork) and upstream (the original). Fetch upstream: `git fetch upstream`.",
                "Two remotes, one repo.",
                "You see both remotes listed. Now you can fetch changes from the original AND push to your own fork. This is the fork contributor's setup.",
            ),
            ex(
                "19-3",
                "Look for a `CONTRIBUTING.md` in the original repo. Read it. What does it require? (Style, tests, commit format, PR template.)",
                "Understanding the maintainer's expectations.",
                "Common items: 'run linter before committing', 'use conventional commits', 'add tests for new features', 'sign the CLA'. Meeting these is the difference between a merged PR and a closed one.",
            ),
            ex(
                "19-4",
                "Discuss (in `git-lab/open-source-notes.md`): what's the difference between a fork on GitHub and a clone on your laptop? Why do you need BOTH when contributing?",
                "Fork = remote copy. Clone = local copy.",
                "Fork lives on GitHub — you can push to it because it's under your account. Clone lives on your laptop — where you actually edit code. You need the fork so you can push somewhere; you need the clone so you can edit locally. Then PR proposes the fork's branch into the original.",
            ),
            ex(
                "19-5",
                "Delete your fork (optional). On GitHub, go to fork's Settings → Delete. Verify: fork gone, but the ORIGINAL repo is completely untouched.",
                "Cleanup practice.",
                "Fork deleted. Original repo unaware you ever existed. Your local clone still works but has no remote to push to (origin URL now invalid). This is the natural end of a done contribution.",
            ),
        ],
    },
    {
        "id": "20",
        "title": "Issues, Labels, Milestones",
        "level": "Intermediate",
        "summary": "GitHub's project management: bug tracking, feature planning, discussion — all cross-linked with your code.",
        "body": md("""
## What issues are for
An **issue** on GitHub is a discussion thread attached to your repo. Uses:
- Bug reports ("crash when clicking X")
- Feature requests ("add support for Y")
- Questions ("how do I use Z?")
- Internal tasks ("refactor the parser")
- Design discussions ("should we support format Q?")

Issues are structured, searchable, and linkable to commits and PRs.

## Creating an issue
- Repo page on GitHub → Issues tab → New issue
- Title: short summary
- Body: detailed description, steps to reproduce, expected vs actual, screenshots
- Labels, assignees, milestone (optional)
- Submit new issue

Issue gets a number (`#1`, `#2`, ...). Reference it anywhere with `#N`.

## Issue templates
For repos that get many issues, set up templates: `.github/ISSUE_TEMPLATE/` folder with `bug-report.md`, `feature-request.md`, etc. When someone clicks New Issue, they pick a template — pre-fills the structure so all bug reports have "Steps to reproduce", "Expected", "Actual", etc.

Templates make issues easier to triage.

## Labels
Labels categorize issues:
- `bug`, `enhancement`, `question`, `documentation`
- `good-first-issue` (invites new contributors)
- `help-wanted`
- Priority: `p0`, `p1`, `p2`
- Component: `audio`, `ui`, `build`

Create labels: Issues → Labels → New label. Assign colors for visual scanning.

## Milestones
Group issues into a target: "v2.0 release", "Q1 features", "Beta". An issue can belong to one milestone. GitHub shows progress bars.

Create: Issues → Milestones → New milestone. Assign issues to it via the sidebar.

## Assignees
Who's working on this? Assign a person (or multiple). Shows in filters, notifications. On self-managed teams, people self-assign; on managed teams, a lead assigns.

## Linking issues to PRs and commits
In commit messages or PR descriptions:
```
Closes #42       # auto-closes issue when merged
Fixes #42        # same as Closes
Resolves #42     # same
Refs #42         # mentions but doesn't close
See #42          # informational
```
GitHub cross-links: issue #42 gets a bidirectional link to the PR/commit.

## Comments and mentions
On any issue, anyone can comment. Mention users with `@username`. Reference other issues/PRs with `#N`. Reference commits with SHA.

Rich formatting: Markdown, code blocks, embedded images (paste screenshots).

## Closing and reopening
- Close: "Close issue" button (or auto-close via linked PR)
- Reopen: "Reopen issue" (if the problem returns)

Closed issues stay in the repo forever, searchable. This is your bug history.

## Filters and searches
Issues page has a search bar with filters:
```
is:issue is:open label:bug            # open bugs
is:issue is:closed assignee:@me       # your closed issues
is:issue milestone:v2.0               # everything in v2.0
is:pr author:alice is:open            # alice's open PRs
```
Learning the syntax makes issue triage fast.

## The relationship: issue → PR → commit
Common flow:
1. Bug reported as issue #42
2. Someone creates branch, commits fix (message: "Fix crash on export — refs #42")
3. Push, open PR: title mentions the issue, description says "Closes #42"
4. Reviewer approves, merge
5. GitHub auto-closes issue #42
6. Later, the issue serves as the historical record of what was wrong and how it was fixed

This traceability from user problem → code fix is the whole reason issues + PRs exist.

## Project boards (Kanban-style)
Beyond issues, GitHub has **Projects** — Kanban boards that group issues into columns (To do / In progress / Done). Two flavors:
- **Repo-scoped** project (older, being deprecated)
- **User/org-scoped** projects (newer, more powerful) — issues from multiple repos in one board

For personal or small team use, simple issue labels + milestones are often enough. Projects add value at 20+ concurrent items.

## When NOT to use GitHub issues
- Sensitive info: don't put customer PII, credentials, or private data in public issues
- Trivial personal TODOs: use a note file, not an issue that clutters the tracker
- Support conversations: use a dedicated support tool (Zendesk, Discord) not issue threads
- Confidential planning: use a private repo's issues, or a dedicated PM tool

## Discussions (newer feature)
GitHub Discussions is a separate feature (like a forum). Better than issues for:
- Q&A ("how do I use X?")
- Show-and-tell
- Announcements
- Free-form community chat

Enable via repo Settings → Features → Discussions. Reduces noise in the issue tracker.
"""),
        "exercises": [
            ex(
                "20-1",
                "In `git-lab`, on GitHub: Issues tab → New issue. Title: 'Add a hello-world script'. Body: describe what you want. Add label `enhancement`. Submit. Note the issue number (probably #1).",
                "First issue creation.",
                "Issue #1 exists on your repo. Public (since git-lab is public) or private. This is now a tracked item on your project.",
            ),
            ex(
                "20-2",
                "Create a branch in GHD: `feat/hello-script` (references issue #1). Commit a `hello.py`. In the commit message, include 'Refs #1'. Push, open PR, in PR description say 'Closes #1'. Merge the PR. Verify: issue #1 is auto-closed.",
                "The full issue → PR → merge cycle.",
                "Issue #1 shows 'Closed' status. Linked to the PR that closed it. Anyone reading the issue can click through to the actual code change. This is the historical trail that makes projects maintainable years later.",
            ),
            ex(
                "20-3",
                "Create 3 more issues with different labels: one 'bug', one 'question', one 'good-first-issue'. Play with the filter bar: `label:bug`, `label:question`, `is:open`. Get comfortable filtering.",
                "Practice the search-filter language.",
                "You navigate issues by intent quickly. On a project with 200 issues, this filtering is essential — otherwise you drown.",
            ),
            ex(
                "20-4",
                "Create a milestone `v0.1` (Issues → Milestones → New milestone). Assign 2 of your issues to it. Look at the milestone page — shows progress bar (0% complete). This is how release planning works.",
                "Grouping for planning.",
                "You have a lightweight roadmap: 'v0.1 will contain these 2 issues.' As issues close, the milestone bar fills up. Simple, effective planning for small projects.",
            ),
            ex(
                "20-5",
                "Discuss (in `git-lab/issue-hygiene.md`): what's YOUR policy for creating an issue vs just fixing something? What TYPES of things deserve an issue?",
                "Not every change needs an issue.",
                "Common answer: 'Bugs I can't fix immediately deserve an issue. Features anyone else might work on deserve an issue. Design decisions deserve an issue for discussion. Trivial typos I just fix — no issue.' The threshold is 'does this need discussion, tracking, or coordination?' If yes → issue. If no → just do it.",
            ),
        ],
    },
    # ────────────────────── PHASE 6: UNDO / SAFETY ──────────────────────
    {
        "id": "21",
        "title": "Undoing Things: Discard, Revert, Reset, Amend",
        "level": "Advanced",
        "summary": "The four undo operations. Different scopes, different danger levels. Know which to reach for.",
        "body": md("""
## The four undo operations
| Operation | Scope | Recoverable? | Safe on shared? |
|-----------|-------|--------------|-----------------|
| **Discard** | Uncommitted changes | ❌ No (gone forever) | Yes |
| **Amend** | Last commit only | Yes if not pushed | ⚠ Only if not pushed |
| **Revert** | Any past commit | Yes (creates new commit) | ✅ Yes |
| **Reset** | Recent commits | Sometimes | ❌ No if pushed |

Pick based on: what did you do, and has it been pushed?

## Discard (uncommitted changes)
You edited a file, changes are showing in Changes tab, you want to abandon them.
- GHD: right-click file → **Discard changes** → confirm
- Multi-file: right-click any → **Discard all changes**
- CLI: `git checkout -- file.py` or `git restore file.py`

Result: file reverts to last committed state. Uncommitted work GONE. No undo.

Use when: "I was just experimenting, forget it."

## Amend (fix the last commit)
You committed but the message is bad, or you forgot a file, or you want to add one more small change.
- GHD: right-click the LAST commit in History → **Amend commit**
- OR: with new uncommitted changes present, tick "Amend previous commit" before committing (some GHD versions)
- CLI: `git commit --amend`

Result: replaces the last commit with a new one (new SHA). Old commit gone.

Use when: "Just made a commit locally, want to fix the message or add one more small thing, haven't pushed yet."

**Danger**: if you already pushed, amending creates a mismatch. You'd need force-push, which is bad on shared branches. Rule: only amend if you HAVEN'T PUSHED YET.

## Revert (undo a specific commit)
You want to undo a specific past commit — but keep the history record of it happening.
- GHD: right-click the commit → **Revert commit**
- CLI: `git revert <sha>`

Result: creates a NEW commit that inverts the changes of the target commit. Old commit stays in history.

Example:
```
Before:
    A ← B ← C ← D    (D introduced a bug)

After revert D:
    A ← B ← C ← D ← D'    (D' undoes D)
```

Use when: "Committed something bad that's already pushed and shared. Need to undo it safely."

Revert is SAFE on shared branches. It doesn't rewrite history — it adds a new commit.

## Reset (rewind to an earlier commit)
You want to move your branch back to an earlier commit, throwing away everything after.
- GHD: Branch menu → Reset (limited options in UI)
- CLI: `git reset --hard <sha>` (destructive) or `git reset --soft <sha>` (keeps changes staged)

Three flavors:
- **soft**: reset branch pointer, keep changes staged
- **mixed** (default): reset branch pointer, keep changes unstaged
- **hard**: reset branch pointer, discard all changes

Result of `--hard`: branch and files match the target commit. Everything after is gone.

Example:
```
Before:
    A ← B ← C ← D    (main here at D)

After git reset --hard B:
    A ← B         (main here at B; C and D gone)
```

**Extreme danger** on shared branches: if you reset back and force-push, you erase commits others have. Never reset shared branches without team coordination.

Use when: "Made bad LOCAL commits, want to erase them and start over. No one else has these yet."

## The recovery mechanism: reflog
Git remembers every state your local branch was in for ~90 days (default). Even if you reset and think work is lost:
```bash
git reflog                    # list of all recent HEAD positions
git checkout <old-sha>        # restore to any point
git branch recovered <sha>    # save as a new branch
```
Reflog is your safety net for "I destroyed my work". If it happened in the last 30 days on your local machine, you can probably get it back.

GHD does not expose reflog in UI — use CLI when needed.

## Decision tree: which undo to use?
```
Did you commit yet?
├── No → Discard (uncommitted only) or just don't stage
└── Yes:
    ├── Did you push yet?
    │   ├── No:
    │   │   ├── Fix the LAST commit only → Amend
    │   │   └── Rewind multiple commits → Reset
    │   └── Yes:
    │       ├── Undo one specific commit → Revert
    │       └── Undo many commits → Multiple Reverts, or coordinate a reset+force-push
```

## Removing a file from a commit
Common: "I accidentally committed a secret file, need to un-commit."
- If not pushed: amend the last commit, unchecking the file in staging. File returns to unstaged.
- If pushed: revert (creates a new commit removing the file). WARNING: the file is still visible in history for anyone with access. If it's a secret, rotate the credential AND scrub history (advanced — see BFG or git filter-repo tools).

## The nuclear option: fresh clone
When your local repo is in a truly messed-up state and you don't know how to fix it:
1. Push any local commits you want to keep (to a backup branch)
2. Delete your local folder
3. Fresh clone
4. Cherry-pick or re-do work

This is not shameful — it's a legitimate recovery strategy when confusion outweighs work-to-recover.
"""),
        "exercises": [
            ex(
                "21-1",
                "In `git-lab`: edit a file, don't commit. Right-click → Discard changes → confirm. The file returns to last committed state. Uncommitted work: GONE.",
                "Feel the finality of discard.",
                "Discard is one-way. Undo does not work. This is why 'commit early, commit often' matters — committed things are recoverable, uncommitted things are not.",
            ),
            ex(
                "21-2",
                "Make a commit with a bad message ('asdf'). Do NOT push. Right-click the commit → Amend commit → change message to something good. Verify: History shows the new message, SHA changed. If you had pushed, force-push would be needed (bad idea).",
                "Amend for pre-push fixes.",
                "Message is now good. Old commit gone (SHA changed). This is the ideal usage: fix a mistake before it leaves your machine.",
            ),
            ex(
                "21-3",
                "Make a commit. Push it. Now regret it. Right-click → Revert commit. A new commit appears that undoes the previous. Push. Verify on GitHub: both commits visible, the change is effectively undone.",
                "Revert = the SAFE undo for pushed work.",
                "Both commits in history. Effect is zero (revert cancels the previous). Anyone reading history sees the story: 'we did X, then reverted X.' Safe, honest, no rewriting.",
            ),
            ex(
                "21-4",
                "CLI practice: Repository → Open in Terminal → `git reflog`. See the list of recent HEAD positions. If you screw up in future, this list is how you find any 'lost' commit.",
                "Reflog is your safety net.",
                "You see a numbered list of HEAD moves. If you ever reset/force-push and lose work, `git reflog` finds the pre-reset SHA and `git checkout <sha>` restores it. Life-saver.",
            ),
            ex(
                "21-5",
                "Discuss (in `git-lab/undo-decision.md`): given the scenarios, which undo would you use?\n(a) You just typed a bunch, want to abandon\n(b) You committed a typo in the message, not pushed\n(c) You committed and pushed a broken feature to main\n(d) You committed 5 things locally and want to redo them from scratch",
                "Practice matching operation to scenario.",
                "(a) Discard. (b) Amend. (c) Revert (the safe undo for pushed work). (d) Reset --hard to the commit before your 5, then start over — only OK if not pushed.",
            ),
        ],
    },
    {
        "id": "22",
        "title": "Stashing and Rewriting Warnings",
        "level": "Advanced",
        "summary": "Stashing = 'set aside my in-progress changes'. Rewriting history = 'do not do this on shared branches'.",
        "body": md("""
## Stashing: pause without committing
Scenario: you're mid-work on a feature. Urgent bug needs a fix. You want to:
1. Set aside your current changes (not commit them — they're not done)
2. Switch to a hotfix branch
3. Fix the bug, commit, push
4. Come back to your original branch
5. Restore your set-aside changes

That is stashing.

## GHD's version of stashing
GHD does NOT have a straightforward "Stash" button. Instead:
### Option A: "Bring changes to..."
When you switch branches with uncommitted changes, GHD asks:
- **Leave changes on this branch** — try to switch anyway (may block)
- **Bring changes to <new branch>** — carry your uncommitted work along

Not exactly a stash, but works for the common case of "I switched branches by accident with changes."

### Option B: The workaround — WIP commit
1. Make a temporary "WIP" commit with your in-progress changes
2. Switch branches, do the hotfix
3. Switch back
4. Amend or reset --soft to un-commit and continue

Not ideal but works. Adds a temporary commit to history that you clean up later.

### Option C: The CLI (real stash)
```bash
git stash                    # save changes to stash stack
git stash list               # see all stashes
git stash pop                # restore most recent stash and remove from stack
git stash apply              # restore without removing from stack
git stash drop               # remove a stash without applying
```
Full featured. Use this when you actually need stashing.

## Stash gotchas
- Stashes do NOT include NEW files (untracked). Use `git stash -u` to include them.
- Stashes are LOCAL. Not pushed. If your laptop dies, stashes die.
- Stashes are named by number by default (`stash@{0}`, `stash@{1}`) — use `git stash push -m "descriptive message"` to name them.
- Don't accumulate 20 stashes. They rot. Pop or drop them.

## Alternative to stash: "stash-as-a-branch" workflow
Modern preference in many teams:
- Instead of `git stash`, make a proper branch (`experiment/wip-notes`), commit your WIP there
- Switch away freely
- Come back to the branch when ready
- Branches are visible in GHD, remembered, easy to see

This uses branches as the "safe place to leave work" — which is what stashes originally were before Git had cheap branches.

## History rewriting: the danger zone
Some Git operations REWRITE history — they change or replace commits that already exist:
- **Amend** — replaces last commit
- **Reset** — moves branch pointer backward, orphaning commits
- **Rebase** — replays commits with new SHAs
- **Interactive rebase** — reorder / squash / drop commits

Rewriting is FINE for commits that ONLY EXIST LOCALLY (never pushed).

Rewriting is DANGEROUS for commits that have been PUSHED and PULLED BY OTHERS.

## Why rewriting shared history is bad
Say your local commits are C, D (based on B). You push. Alice pulls — her local has C, D too.
You rebase, replacing C, D with C', D'. Force-push.
Now: origin has C', D'. Alice's local still has C, D.
When Alice pulls, Git sees divergence. Merge is messy. Alice's local commits based on old C, D are orphaned.
Multiply by 5 teammates = disaster.

The rule (from Module 16):
> Never rewrite public history.

## What "public" means
- Pushed to a shared branch (main, develop, release-*) that others pull
- Pushed to a shared feature branch (multi-person feature) that others pull

What's PRIVATE (safe to rewrite):
- Local commits never pushed
- Your own feature branch that only you use, even if pushed

## Squashing before opening a PR (the good rewrite)
Very common good use of rewriting:
1. On your feature branch, you made 15 commits (some fixups, WIPs, typos)
2. Before opening PR: interactively rebase to squash them into 2-3 clean commits
3. Force-push (safe: only you use this branch)
4. Now PR has clean history

This is normal and encouraged. It's YOUR OWN private branch — squash away.

## The safety net: `--force-with-lease`
When you MUST force-push, use `--force-with-lease` instead of `--force`:
```bash
git push --force-with-lease origin feature-branch
```
This aborts the push if someone else pushed to the branch since your last fetch. Prevents you from silently overwriting a teammate's push.

GHD's force-push (Repository menu → Force push or via CLI) may or may not use `--force-with-lease` depending on version. When in doubt, drop to CLI.

## Recovering from a bad rewrite
If you rewrote history and lost work:
- `git reflog` (Module 21) shows every HEAD position. Find your old SHA.
- `git checkout <old-sha>` — visit the lost commit
- `git branch recovered <sha>` — save it as a branch
- Merge or cherry-pick into current work

Reflog is the ultimate safety net. Even after amend/reset/rebase, your old commits linger for 90 days.

## Practical stashing patterns
### "I need to switch branches for 5 minutes"
- CLI: `git stash; git checkout other-branch; ... ; git checkout original; git stash pop`
- Or: WIP commit → switch → switch back → amend

### "I want to try an experimental fix without losing current work"
- Create a branch: `git checkout -b experiment/try-fix`
- Commit freely
- If it works: merge back or cherry-pick
- If it doesn't: switch away, delete the branch

Branches are better than stashes for anything longer than 10 minutes.

### "I want to save all in-progress work at end of day"
- Commit as WIP: `git commit -am "WIP: end of day <date>"`
- Push to your private branch
- Next morning: pull, reset --soft HEAD~1 to un-commit, continue

Personal-branch-as-stash is a robust pattern. Also gives you cross-machine access (stash is local; branch is on GitHub).
"""),
        "exercises": [
            ex(
                "22-1",
                "In `git-lab`: make some uncommitted changes. Try to switch branches — GHD asks 'Bring changes to <target> or leave here?'. Choose 'Bring changes'. Your changes migrate to the target branch. This is GHD's lightweight stash.",
                "The auto-migration on branch switch.",
                "Changes moved with you. Useful for 'oh, I meant to commit these on a feature branch, not main.' Not a real stash — just a helper.",
            ),
            ex(
                "22-2",
                "CLI stash: Repository → Open in Terminal → make changes → `git stash` → verify with `git status` (clean) → `git stash list` (one stash) → `git stash pop` (changes return, stash removed).",
                "The full stash lifecycle in CLI.",
                "You experienced: hide changes → do other things → restore. This is the classic pattern. GHD doesn't expose it directly but CLI does.",
            ),
            ex(
                "22-3",
                "Read the module's warning on rewriting public history CAREFULLY. Summarize in 2 sentences why it's dangerous and when it's OK.",
                "This is the single most important 'do not do' in Git.",
                "Rewriting history changes commit SHAs. If others have pulled the old SHAs, force-pushing new ones creates divergence they can't easily reconcile. Rewrite freely on your own local/private branches; never on shared branches.",
            ),
            ex(
                "22-4",
                "Practice `git reflog` in your `git-lab`. Run `git reflog` in a terminal. You see a numbered list of every HEAD position for the last N days. This is your safety net — memorize this command.",
                "Reflog is the ultimate recovery tool.",
                "You saw the reflog output. In future, if you ever think 'I destroyed my work with a bad reset/rebase', run reflog and find the pre-disaster SHA. `git checkout <sha>` visits it; `git branch recovery <sha>` saves it.",
            ),
            ex(
                "22-5",
                "Discuss: your teammate force-pushed to main. You just pulled. Your local main is now different from origin/main. What do you do?",
                "This is a real scenario that happens to teams that break the rules.",
                "(1) Talk to teammate immediately — force-push to main is a serious problem, coordinate before doing more damage. (2) Determine what to keep: your local commits (that referenced OLD main) may be based on now-orphaned commits. (3) `git reflog` to find your work; cherry-pick onto new main. (4) Team retrospective: how did this happen? Add branch protection to prevent recurrence (Module 27).",
            ),
        ],
    },
    {
        "id": "23",
        "title": "When to Drop to CLI",
        "level": "Advanced",
        "summary": "GHD covers ~90% of daily work. Here's the 10% where you need the terminal — and how to do it.",
        "body": md("""
## What GHD does well
- Everyday commit/push/pull/branch/merge
- PR creation
- Conflict resolution (via external editor)
- History browsing
- Cloning and publishing

Use GHD for these. It's faster and less error-prone than CLI.

## What GHD does poorly or not at all
- **Interactive rebase** (`git rebase -i`) — reordering, squashing, editing arbitrary commits
- **Cherry-pick from arbitrary commits** — copying one commit's changes onto current branch
- **Reset with fine control** — `--soft`, `--mixed`, `--hard` distinctions
- **Reflog inspection and recovery** — finding lost commits
- **Stash (full featured)** — named stashes, apply-vs-pop, untracked
- **Bisect** — automated regression finding
- **Submodules** — subrepo management
- **Custom hooks** — pre-commit, post-commit scripts
- **Sparse checkout, worktrees, filter-branch** — advanced repo shaping
- **Remote management** — multiple remotes (upstream/origin/private-fork), URL edits
- **`.gitattributes` and complex .gitignore behaviors**
- **Global config** — user name/email defaults, aliases, editors

For these, drop to CLI.

## Opening the CLI from GHD
Every repo:
- Repository menu → **Open in Terminal / Command Prompt / PowerShell**

Terminal opens in the repo folder, ready for `git` commands. GHD and CLI both see the same `.git/` — they don't conflict.

## The 20 CLI commands you actually need
```bash
# Status and inspection (safe, informational)
git status                        # what's changed, what's staged
git log --oneline --graph --all   # branch topology
git diff                          # unstaged changes
git diff --staged                 # staged changes
git blame path/to/file            # who wrote each line
git show <sha>                    # full details of a commit
git reflog                        # every HEAD position (recovery)

# Branching
git branch                        # list branches
git branch -d name                # delete branch
git checkout -b feature/x         # create and switch to branch
git switch main                   # switch to branch (newer than checkout)

# Committing
git add file                      # stage a file
git add -p                        # stage HUNKS interactively (excellent!)
git commit --amend                # fix last commit
git commit --amend --no-edit      # amend without changing message

# Rebasing
git rebase main                   # rebase current branch onto main
git rebase -i HEAD~5              # interactive: reorder/squash last 5

# Cherry-picking
git cherry-pick <sha>             # copy one commit onto current branch

# Undoing
git reset --soft HEAD~1           # un-commit last, keep staged
git reset --mixed HEAD~1          # un-commit last, unstage
git reset --hard HEAD~1           # OBLITERATE last commit

# Stashing
git stash                         # save uncommitted, clean working dir
git stash pop                     # restore latest stash
git stash list                    # see all stashes

# Remote
git remote -v                     # list remotes
git remote add name url           # add a remote
git fetch --all                   # fetch from all remotes
git push -u origin branch         # push and set upstream tracking
git push --force-with-lease       # safer force-push
```

## `git add -p` — the killer feature
Interactive per-hunk staging on the CLI:
```bash
git add -p file.py
```
For each change:
- **y** = stage this hunk
- **n** = skip this hunk
- **s** = split into smaller hunks
- **e** = edit the hunk manually (advanced)
- **q** = quit

This is like GHD's line-level checkboxes, but more granular. Once you learn it, you'll use it constantly.

## Interactive rebase — squashing commits before PR
Scenario: 8 commits on your feature branch, want to squash into 2 clean commits before PR.
```bash
git rebase -i HEAD~8
```
Editor opens with:
```
pick a3f7c2b Add filter
pick b8d4e1a Fix typo
pick c2f9d5e More typo fixes
pick d5a8f3b WIP
pick e1b7d6a Actually implement filter
pick f4c9e2b Fix filter bug
pick g7d8a5c Rename var
pick h3e2b1a Update docs
```
Change `pick` to `squash` (or `s`) to squash into the previous commit:
```
pick a3f7c2b Add filter
s b8d4e1a Fix typo
s c2f9d5e More typo fixes
s d5a8f3b WIP
s e1b7d6a Actually implement filter
s f4c9e2b Fix filter bug
pick g7d8a5c Rename var
s h3e2b1a Update docs
```
Save, close. Git squashes them. Second editor opens for you to write the combined commit message. Save. Done.

Now your 8 messy commits are 2 clean ones. Force-push (safe: your own branch).

Other actions: `reword` (change message), `edit` (pause to modify code), `drop` (delete commit entirely), `fixup` (like squash but discards the squashed commit's message).

## Bisect for regression hunting
See the Regression Testing course. Summary:
```bash
git bisect start HEAD v1.2.0
git bisect run pytest test_that_shows_bug.py
# Git finds the first bad commit automatically
git bisect reset    # done
```

## Aliases: save typing
Common shortcuts in `~/.gitconfig`:
```ini
[alias]
    st = status
    co = checkout
    sw = switch
    br = branch
    ci = commit
    lg = log --oneline --graph --all --decorate
    unstage = reset HEAD --
    last = log -1 HEAD
```
Add via CLI:
```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
```
Now `git lg` shows the pretty log.

## When you're stuck: search for the exact error
Git error messages are legendary in their specificity. Copy-paste the error to search — someone on StackOverflow has seen it. Common ones:
- "Your local changes to the following files would be overwritten" → commit or stash first
- "Please, commit your changes or stash them before you switch branches" → same
- "fatal: refusing to merge unrelated histories" → `git pull --allow-unrelated-histories`
- "Everything up-to-date" (when trying to push) → nothing to push, or check branch name

## Learning path
- Weeks 1-2: pure GHD, no CLI
- Weeks 3-4: CLI for `git status`, `git log`, `git diff` (inspection only)
- Month 2: CLI for occasional rebase, cherry-pick, stash
- Month 3+: CLI as needed, GHD for routine

Do NOT try to learn CLI first — it's opaque without the mental model that GHD makes visible. GHD first, CLI as escape hatch.
"""),
        "exercises": [
            ex(
                "23-1",
                "Open terminal in `git-lab`. Run every command in the '20 commands' list above (the safe/informational ones — status, log, branch, diff, show, reflog). Read the output. Get comfortable seeing raw Git output.",
                "Reading CLI output = essential skill.",
                "You saw the raw Git worldview. Every GHD feature is a visual layer over these commands. Understanding the raw output makes GHD's abstractions less mysterious.",
            ),
            ex(
                "23-2",
                "Practice `git add -p` on a file with multiple changes: edit README.md in 3 different places, then `git add -p README.md`. Say y/n/s to different hunks. Commit the staged ones. Verify: only the y-hunks are in the commit.",
                "This is the CLI equivalent of GHD's line-level checkboxes.",
                "You made a focused commit from a messy file. `git add -p` is a superpower — it makes any working directory commit-able cleanly. Use daily.",
            ),
            ex(
                "23-3",
                "Interactive rebase practice: make 5 tiny commits on a branch (`fix typo`, `fix typo again`, `WIP`, `real change`, `revert WIP`). Then `git rebase -i HEAD~5`. Squash the fixups. Save. Verify: history now has 1-2 clean commits.",
                "This is why you rebase — turn messy dev commits into clean history.",
                "5 commits collapsed into 1-2 meaningful ones. This is how you keep your feature branch's history clean without being neurotic during development. Squash before opening PR = universal good habit.",
            ),
            ex(
                "23-4",
                "Cherry-pick: create a commit on branch A. Switch to branch B. `git cherry-pick <sha-of-commit-on-A>`. That single commit is now on B too. Verify with history.",
                "Cherry-pick = copy one commit across branches.",
                "You copied one commit from branch A to branch B. Useful for backporting a fix from main to a release branch, or grabbing one useful commit from a colleague's WIP branch.",
            ),
            ex(
                "23-5",
                "Set up aliases: run `git config --global alias.lg \"log --oneline --graph --all --decorate\"` and `git config --global alias.st status`. Now `git lg` and `git st` work as shortcuts. Small time saver, big quality-of-life.",
                "Aliases = your daily accelerators.",
                "Muscle memory for `git st` beats `git status` after a week. Add more aliases as patterns emerge. This is how CLI users get productive fast.",
            ),
        ],
    },
    # ────────────────────── PHASE 7: REAL-WORLD WORKFLOWS ──────────────────────
    {
        "id": "24",
        "title": "Feature Branch Workflow (GitHub Flow)",
        "level": "Advanced",
        "summary": "The simplest team workflow: main is always deployable, every change goes through a PR on a feature branch.",
        "body": md("""
## GitHub Flow — the simple workflow
1. `main` is always deployable (never broken)
2. Create a branch off main for any change (`feat/x`, `fix/y`)
3. Commit on the branch, push
4. Open a PR when ready
5. Review, discuss
6. Merge (deploy if CI passes)
7. Delete branch

That's it. Six steps, done.

## Why this is the default for most teams
- **Simple**: one long-lived branch (main), everything else short-lived
- **Fast**: no need for release branches, staging branches, integration branches
- **Safe**: main is always shippable, CI enforces quality
- **PR-centric**: all changes discussed, reviewed, tracked

Suits: web apps deployed continuously, libraries with frequent releases, most SaaS.

## Contrast: Git Flow (heavier)
A more structured alternative for products with formal releases:
- `main` = production
- `develop` = integration
- `feature/*` off develop
- `release/*` off develop, merged to main and develop when done
- `hotfix/*` off main for emergency fixes

More branches, more merging, more ceremony. Better fit for:
- Long release cycles (monthly, quarterly)
- Formal QA gates
- Multiple production versions maintained simultaneously

For most modern software, GitHub Flow is simpler and sufficient.

## Deployment strategies with GitHub Flow
### Continuous deployment
Every merge to main auto-deploys to production. CI/CD pipeline runs tests, if green → deploy.
- Requires excellent tests and monitoring
- Feature flags decouple deploy from release
- Fast feedback: minutes from merge to prod

### Deploy on-demand
Merge to main = ready to ship. Deploy manually (button, `deploy.sh`) when someone decides.
- Simpler infra
- Batches of features per deploy
- Some human coordination

### Release cadence
Cut a release tag periodically (weekly, monthly). Deploy the tag.
- More traditional
- Time to plan and communicate releases

Pick based on your product's risk profile.

## Branch naming conventions
Common patterns:
```
feature/short-description    or  feat/description
fix/issue-number-description  or  bug/description
hotfix/urgent-issue
docs/what-changed
refactor/what
chore/dependency-updates
```
The prefix filters visibility: `git branch --list "feature/*"` shows only features.

## Pull request tempo
- **Open early, iterate**: draft PRs let you get early feedback before you're done
- **Small PRs**: <200 lines is ideal; >500 is a review nightmare
- **Fast reviews**: within a day for anything non-huge
- **Merge quickly after approval**: PRs that sit approved for a week get stale

Rule of thumb: from branch creation to merge, aim for <1 week for typical PRs.

## Handling long-running work
If a feature is genuinely huge (weeks/months of work):
### Option A: Break into small PRs
Ship one small piece at a time, behind a feature flag if needed. Each PR merges to main quickly.

### Option B: Long-lived feature branch
`feature/big-thing` lives for weeks. Regularly rebase or merge main into it to stay current. When ready, one big PR to main.
- Danger: massive PR, hard to review
- Prefer Option A when possible

### Option C: Fork/subproject
The work is so different it's really its own subproject. Consider a separate repo or subdirectory.

## Feature flags (decoupling deploy from release)
Merge code to main and deploy it, but hide the feature behind a flag:
```python
if feature_flags.enabled("new_biquad"):
    use_new_biquad()
else:
    use_old_biquad()
```
- Ship in-progress work safely
- Turn on for internal users first
- A/B test with subset of users
- Instant rollback (turn flag off) without redeploy

Enables trunk-based development: everyone works on main-ish, features toggle on when ready.

## The team disciplines that make GitHub Flow work
1. **Green main**: broken main = stop-the-world event, fix immediately
2. **CI on every PR**: no merging red PRs
3. **Fast review turnaround**: <1 day for typical
4. **Small PRs**: split if >500 lines
5. **Delete merged branches**: keep the branch list clean
6. **Descriptive commits and PRs**: (Modules 07, 17)
7. **Branch protection**: enforce the rules mechanically (Module 27)

Without these disciplines, GitHub Flow degrades into "everyone pushes to main and it's constantly broken." The discipline is what makes the workflow work.

## What NOT to do
- **Don't commit to main directly** (except tiny doc typos, and even those preferably via PR)
- **Don't merge without review** (unless you're solo — then self-review still)
- **Don't leave branches around indefinitely** — they become archeological curiosities
- **Don't push broken code just because it's "on a branch"** — every push runs CI, waste of compute
- **Don't have 5 concurrent branches by yourself** — you'll lose track. Finish one before starting the next.

## The morning routine (from Module 10, extended)
1. Fetch origin
2. Pull main to be current
3. Check for new PRs to review
4. Continue your current feature branch (or start a new one)
5. Push periodically
6. When done: open PR
7. Address review comments same-day if possible
8. After merge: delete branch

This routine, repeated daily, IS the workflow. Not fancy. Very effective.
"""),
        "exercises": [
            ex(
                "24-1",
                "Practice a full GitHub Flow cycle in `git-lab`: (1) branch `feat/practice-flow`, (2) 2 commits, (3) push, (4) open PR, (5) merge (self-approve OK), (6) delete branch. Time it. Under 5 minutes for a trivial change.",
                "Muscle memory for the standard flow.",
                "You did the standard cycle end to end. In real work, add: reviewer waiting, CI running, back-and-forth on comments. Skeleton is the same. Do this 100 times and it becomes automatic.",
            ),
            ex(
                "24-2",
                "Discuss (in `git-lab/workflow-notes.md`): for `git-lab` (your personal learning repo), what would 'green main' mean? What would you enforce as a matter of habit?",
                "Apply the discipline concept to your personal work.",
                "Green main for personal repo: 'code runs without errors, tests pass if any, README is not lying.' Enforce via: don't commit broken WIP to main (use branches), run tests before merging PRs, keep a script that verifies everything works. Even solo, these habits pay.",
            ),
            ex(
                "24-3",
                "Set up branch naming conventions for `git-lab`. In `CONTRIBUTING.md`, write:\n- `feat/*` for features\n- `fix/*` for bug fixes\n- `docs/*` for documentation\n- `refactor/*` for restructuring\n- `chore/*` for maintenance\n\nCommit it. Now future branches follow the pattern.",
                "Conventions codified = followed.",
                "CONTRIBUTING.md exists. Future you (and any collaborator) knows the naming rule. Consistency compounds — after 20 branches, the pattern is obvious and searchable.",
            ),
            ex(
                "24-4",
                "Read about feature flags in 3 minutes (any online source). Discuss: could feature flags help YOUR personal work? What kind of feature would benefit?",
                "Feature flags are advanced but often useful.",
                "For personal projects: usually overkill unless you're experimenting with two approaches simultaneously and want to A/B them. For team products: essential for shipping big features safely. Understanding the concept is table stakes even if you never implement one.",
            ),
        ],
    },
    {
        "id": "25",
        "title": "Tags, Releases, Semantic Versioning",
        "level": "Advanced",
        "summary": "How to mark specific commits as 'this is version X'. Users install those. You maintain them.",
        "body": md("""
## Tags vs branches
- **Branch** = movable pointer, moves forward with new commits
- **Tag** = FROZEN pointer at a specific commit, never moves

You tag when you want to say "THIS commit is v1.0.0". A month later, main has moved forward, but the tag still points at that same commit. Users can install v1.0.0 forever.

## Two flavors of tags
### Lightweight tag
Just a name attached to a commit. Simple.
```bash
git tag v1.0.0                    # tag current commit
git tag v1.0.0 <sha>              # tag a specific commit
git push origin v1.0.0            # push tag to remote
git push --tags                   # push all local tags
```

### Annotated tag (recommended)
Includes a message, tagger name, timestamp. Full commit-like metadata.
```bash
git tag -a v1.0.0 -m "First stable release"
```
Preferred for real releases. Lightweight tags are for scratch marking.

## Creating a tag in GHD
- Right-click a commit in History → **Create Tag**
- Enter tag name (e.g., `v1.0.0`)
- Push tag (Repository menu → Push → will include tags, or use CLI `git push --tags`)

## Semantic Versioning (semver)
The convention for version numbers: `MAJOR.MINOR.PATCH`
- **MAJOR** — incompatible API changes (breaking)
- **MINOR** — new features, backward compatible
- **PATCH** — bug fixes, backward compatible

Examples:
- `1.0.0` → `1.0.1` — bug fix
- `1.0.1` → `1.1.0` — new feature (backward compat)
- `1.1.0` → `2.0.0` — breaking change

Pre-release suffixes: `1.0.0-alpha`, `1.0.0-beta.2`, `1.0.0-rc.1`.
Build metadata: `1.0.0+build.123`.

Rule for API stability: after 1.0.0, MAJOR bumps are the ONLY place you may break users. Before 1.0.0 (`0.x.y`), anything goes — you're pre-stable.

## GitHub Releases
GitHub adds a UI on top of tags — **Releases**. A Release is:
- A tag
- Plus a title and description (release notes)
- Plus optional binary artifacts (compiled binaries, installers)
- Plus asset downloads and download counts

Create: Repo → Releases → Draft a new release → pick or create tag → title → notes → attach artifacts → Publish.

Users see Releases on your repo page. Easy to find "the current stable version" without digging through tags.

## Release notes
For each release, write:
```markdown
## v1.2.0 (2026-09-22)

### Added
- New `dc_block()` function
- Support for stereo input

### Changed
- Faster FIR implementation (2x on ARM Cortex-M)

### Fixed
- Crash on empty input (#42)
- Off-by-one in filter loop (#43)

### Breaking
- (none)

**Full changelog**: [v1.1.0...v1.2.0](link)
```
Even for personal projects, release notes are your future memory of what changed.

## Auto-generated release notes
GitHub Releases has a **Generate release notes** button. It reads PRs merged since the last release and drafts notes. Excellent starting point — edit before publishing.

## Tagging a release: the workflow
```bash
# Merge everything you want in the release
# Verify tests pass on main
git checkout main
git pull
git tag -a v1.2.0 -m "v1.2.0 - DC blocker and stereo support"
git push --tags
# On GitHub: Releases → tag v1.2.0 → add notes → publish
```

Or on GitHub website:
- Releases → Draft a new release
- Choose tag (creates if not exists)
- Target = main (or a specific commit)
- Title, notes, artifacts
- Publish

## Pre-releases
Mark a release as pre-release (checkbox in UI). Signals to users: "not fully stable, don't use in production yet." Common for alphas, betas, release candidates.

## Downloading a specific version
Users can:
- Clone the repo and `git checkout v1.0.0`
- Download source zip from the Releases page
- Download an artifact (binary) from Releases

The tag freezes a specific commit — users get exactly what you shipped.

## Deleting or moving a tag
Tags are meant to be immutable. If you MUST change one:
```bash
git tag -d v1.0.0                     # delete local
git push origin :refs/tags/v1.0.0     # delete remote
git tag -a v1.0.0 <new-sha>           # recreate
git push --tags
```
DANGEROUS: users may have installed v1.0.0 already. Changing it invalidates their install. Prefer: bump to v1.0.1 with the fix.

Cardinal rule: DO NOT MOVE a tag that's been published. Users trust that v1.0.0 always means the same thing.

## Version numbering in code
Somewhere in your code, expose the version:
```python
# python
__version__ = "1.2.0"
```
```c
// C
#define VERSION "1.2.0"
```
Match your git tag. Tools like `setuptools-scm` (Python) can auto-derive version from git tags — no manual sync needed.

## The changelog file
Some projects maintain `CHANGELOG.md` in the repo — human-curated list of changes across all versions. Update as you go, or generate from PR/commit history.

Popular format: [Keep a Changelog](https://keepachangelog.com/).

## Backporting fixes to old versions
Scenario: v2.0 is current, but a user on v1.5 hits a bug. You want to fix v1.5 without forcing them to upgrade.
- Branch off v1.5 tag: `git checkout -b v1.5.x v1.5.0`
- Cherry-pick or manually apply the fix
- Commit, tag v1.5.1
- Publish new release for v1.5.x line

Maintaining multiple version lines is complex. Only do it for products with real user-versioning needs (libraries, embedded firmware, LTS releases).

## The version.txt file
For firmware or embedded work where the running device needs to know its version at runtime:
- Include a `version.txt` or `version.h` file
- Update on tag/release
- Bake into the binary

Some CI pipelines auto-update this from the git tag on release build.
"""),
        "exercises": [
            ex(
                "25-1",
                "In `git-lab`: right-click your most recent commit → Create Tag → `v0.1.0`. Push tags. On github.com: verify tag appears under Releases → Tags.",
                "First tag creation.",
                "Tag v0.1.0 exists locally and on GitHub. Users can now `git checkout v0.1.0` to get exactly this state, forever.",
            ),
            ex(
                "25-2",
                "On github.com → Releases → Draft a new release → pick tag `v0.1.0` → title 'First release' → write release notes describing what's in it → Publish. Verify: Releases page shows your v0.1.0 with source zip auto-attached.",
                "Turning a tag into a proper Release.",
                "You have a discoverable Release with notes and downloadable source. Every serious project on GitHub does this for every version.",
            ),
            ex(
                "25-3",
                "Make more commits after the tag. Then check out the tag: switch branches → `v0.1.0` (from the Tags section of the branch dropdown). Working files revert to the tagged state. Switch back to main — latest state returns.",
                "Tags freeze a moment; you can time-travel.",
                "You visited the v0.1.0 code state. Notice the branch dropdown says '(detached HEAD)' when you're on a tag — you can look but shouldn't commit here. To make new commits from v0.1.0, create a branch first.",
            ),
            ex(
                "25-4",
                "Discuss (in `git-lab/versioning-notes.md`): apply semver to these scenarios:\n(a) You added a new optional function\n(b) You changed the signature of an existing function\n(c) You fixed a typo in a comment\n(d) You improved performance without changing behavior",
                "Practice semver classification.",
                "(a) MINOR (new feature, backward compat).\n(b) MAJOR (breaking change to existing API).\n(c) PATCH (or skip — some teams don't bump for comment-only changes).\n(d) PATCH (bug/quality fix, no behavior change).",
            ),
            ex(
                "25-5",
                "Create a second tag `v0.2.0` on the latest commit, publish a Release for it. On the Releases page, verify BOTH v0.1.0 and v0.2.0 exist, with v0.2.0 marked 'Latest'.",
                "Multiple versions coexist.",
                "Two releases visible. Users can pick which version to install. The 'Latest' badge highlights your recommended version. This is how you evolve a project while preserving old versions.",
            ),
        ],
    },
    {
        "id": "26",
        "title": ".gitignore, .gitattributes, and Git LFS",
        "level": "Advanced",
        "summary": "Repo hygiene: what to never commit, how to handle binary files and line endings, and large-file storage.",
        "body": md("""
## .gitignore — what NOT to track
A text file at the repo root listing patterns for files/folders Git should IGNORE:
```
# Compiled output
build/
dist/
*.o
*.exe
*.pyc
__pycache__/

# Dependencies
node_modules/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.key
config.local.json

# Logs and temp
*.log
tmp/
```

## How .gitignore works
- Git IGNORES matching files: they don't show in Changes tab, aren't committed
- Patterns are per-directory (subdirectory `.gitignore` can override)
- `/` at start = relative to repo root
- `/` at end = folder only
- `*` = wildcard
- `!pattern` = un-ignore (re-include)
- `#` = comment

Examples:
```
build/          # ignore build folder anywhere
/build/         # ignore only top-level build folder
*.log           # ignore all .log files
!important.log  # but keep this one
```

## Templates
GitHub maintains templates for common languages:
- `github.com/github/gitignore` — pick from Python, C++, Node, etc.
- GHD's New Repository dialog offers to include one based on your language choice

Copy-paste as starting point, then customize.

## Files already tracked, then added to .gitignore
If you accidentally committed a file, adding it to `.gitignore` DOES NOT remove it from history. It only prevents FUTURE commits from tracking new instances.

To untrack a file that's already in the repo:
```bash
git rm --cached path/to/file
# then commit
```
`--cached` removes from Git tracking but keeps the file on disk. Then `.gitignore` prevents re-adding.

If the file was a SECRET, this is not enough — see 'Removing secrets' below.

## .gitattributes — file-specific rules
Sibling to `.gitignore`. Controls per-file behavior:
```
# Enforce LF line endings for shell scripts
*.sh text eol=lf

# Enforce CRLF for Windows batch files
*.bat text eol=crlf

# Treat these as binary (no diff, no merge)
*.png binary
*.pdf binary

# Custom diff for markdown
*.md diff=markdown

# Export-ignore: exclude from `git archive` (zip downloads)
docs/ export-ignore
```

Most important use: line-ending normalization for cross-platform teams.

## Line endings: CRLF vs LF
- Windows uses CRLF (`\\r\\n`)
- Unix/macOS uses LF (`\\n`)

When a Windows dev and Mac dev collaborate, files can flip endings on every commit — creates false diffs, ugly PRs.

Fix with `.gitattributes`:
```
* text=auto eol=lf
```
This normalizes everything to LF in the repo, converts on checkout per platform. Cleaner history.

Global config (per user):
```bash
git config --global core.autocrlf true    # Windows: convert to LF on commit, CRLF on checkout
git config --global core.autocrlf input   # Mac/Linux: convert to LF on commit, no change on checkout
```

## Large files: the 100 MB limit and Git LFS
GitHub rejects pushes with files > 100 MB. Even below that, big binaries in Git make clones slow and bloat repo size forever (history keeps all versions).

**Git LFS (Large File Storage)** replaces large files with tiny pointers in the repo; actual content stored separately.

Install LFS:
```bash
# One-time per machine
git lfs install

# Per repo: track file types
git lfs track "*.wav"
git lfs track "*.mp4"
git lfs track "goldens/*.bin"

# This adds patterns to .gitattributes automatically
git add .gitattributes
git commit -m "Track binary types with LFS"

# Now commit big files as normal
git add big-audio.wav
git commit -m "Add audio sample"
git push
```

Behind the scenes: `big-audio.wav` in the repo is a 100-byte pointer file. Actual bytes stored on LFS server. On clone, LFS downloads real content.

Free tier: GitHub gives 1 GB LFS storage and 1 GB bandwidth per month. Paid tiers for more.

## When to use LFS
- Audio/video files >10 MB
- Generated golden vectors (large numerical files)
- Design assets (PSD, Sketch)
- ML models, datasets
- Compiled binaries you version (unusual but sometimes needed)

## When NOT to use LFS
- Small binaries (<1 MB) — just commit normally
- Files that change EVERY commit (LFS still keeps versions, but bandwidth adds up)
- Truly huge datasets (>100 GB) — use a proper data store (S3, DVC), not Git

## Removing secrets from history
If you accidentally committed a secret (API key, password) and pushed:
1. Rotate the secret IMMEDIATELY (assume it's compromised)
2. Change source to remove the secret AND add to `.gitignore`
3. Optionally: scrub from history with `git filter-repo` or BFG Repo-Cleaner
4. Force-push (dangerous — coordinate with team)
5. All collaborators must re-clone

The rotate step is critical: even if you scrub history, someone may have already scraped the secret between commit and now. Assume compromised.

Better: never commit secrets. Use `.env` files (in .gitignore) and environment variables.

## The globally-ignored patterns
Some things you always want to ignore, EVERY repo. Set a global gitignore:
```bash
git config --global core.excludesfile ~/.gitignore_global
```
Then in `~/.gitignore_global`:
```
.DS_Store
Thumbs.db
.vscode/
.idea/
*.swp
```
Now these are ignored in every repo you touch, no need to add to each repo's `.gitignore`.

## Testing your .gitignore
- `git status` — files in `.gitignore` don't appear as untracked
- `git check-ignore -v path/to/file` — shows which .gitignore rule matches (or nothing if not ignored)
- GHD's Changes tab omits ignored files entirely

If you expected a file to be ignored but it's not, check: is it already tracked? (Then .gitignore is too late — use `git rm --cached`.)
"""),
        "exercises": [
            ex(
                "26-1",
                "Open `git-lab/.gitignore` (should exist from Module 05 Python template). Add three custom entries: `notes/private/`, `*.local.json`, `scratch/`. Save. Now create files matching these patterns — verify GHD doesn't show them in Changes.",
                "Custom .gitignore patterns.",
                "Files matching your patterns don't appear in Changes tab. Git literally cannot see them (from a version-control perspective). Useful for local-only experiments, private notes, editor configs.",
            ),
            ex(
                "26-2",
                "Simulate the 'already committed' problem: create `debug.log`, commit it, push. Realize you shouldn't have. Add `*.log` to `.gitignore` — notice `debug.log` still shows tracked. Fix: `git rm --cached debug.log`, commit. Now it's untracked.",
                "The two-step remove for already-committed files.",
                "The file is no longer tracked. `.gitignore` prevents re-adding. But: the file EXISTS in history forever (past commits still contain it). For non-sensitive files, that's fine. For secrets, additional scrubbing needed.",
            ),
            ex(
                "26-3",
                "Create `.gitattributes` with:\n```\n* text=auto eol=lf\n*.bin binary\n*.md diff=markdown\n```\nCommit. Verify: future commits normalize line endings.",
                "Cross-platform hygiene.",
                "New files added under this repo will have LF line endings. Binary files (`.bin`) skip diff/merge attempts. This prevents the CRLF/LF flipping that plagues cross-platform teams.",
            ),
            ex(
                "26-4",
                "Install Git LFS (if not already): `git lfs install` (one-time per machine). Then track WAVs in your repo: `git lfs track \"*.wav\"`. Verify: `.gitattributes` updated with `*.wav filter=lfs...`. Commit the .gitattributes.",
                "LFS setup.",
                "You configured LFS. Future .wav files added will be stored via LFS (pointer in repo, content on LFS server). Small metadata overhead, huge benefit for binary content.",
            ),
            ex(
                "26-5",
                "Discuss (in `git-lab/repo-hygiene.md`): for a hypothetical DSP audio project, what would be in `.gitignore`? What in `.gitattributes`? What via LFS?",
                "Apply the concepts to a real scenario.",
                "**.gitignore**: `build/`, `*.o`, `*.exe`, `.vscode/`, `venv/`, `.env`, `logs/`. **.gitattributes**: `* text=auto eol=lf`, `*.wav binary`, `*.bin binary`. **LFS**: `*.wav`, `*.mp3`, `goldens/*.bin` (if bulky), any file over ~10 MB. This hygiene keeps the repo small, clean, and cross-platform friendly.",
            ),
        ],
    },
    # ────────────────────── PHASE 8: GITHUB PLATFORM ──────────────────────
    {
        "id": "27",
        "title": "Branch Protection, Required Reviews, CODEOWNERS",
        "level": "Advanced",
        "summary": "Enforce workflow rules mechanically. Nobody can bypass them by mistake or shortcut.",
        "body": md("""
## Why enforce mechanically
Human discipline fails. Even well-intentioned teams:
- Someone pushes broken code to main "just this once"
- A merge happens without review because "it's urgent"
- CI fails but the merge button still works

Branch protection turns rules from voluntary to enforced. Adds friction to bad actions.

## Setting branch protection
Repo → Settings → Branches → Add rule
- **Branch name pattern**: `main` (or `main`, `release/*`, etc.)
- Then choose protections:

### Require pull request before merging
No direct pushes to `main`. Every change comes through a PR.
- Also: **Require approvals** — set to 1, 2, etc.
- **Dismiss stale approvals when new commits pushed** (recommended)
- **Require review from Code Owners** (see CODEOWNERS below)

### Require status checks to pass before merging
CI checks (from GitHub Actions, external CI) must be green before merge.
- Pick which checks are required
- **Require branches to be up to date** (must be current with base branch before merge)

### Require conversation resolution before merging
All PR review comments must be marked "resolved" before merge. Prevents "oh I forgot to fix that" merges.

### Require signed commits
Commits must be cryptographically signed (GPG or SSH). High-security environments.

### Require linear history
No merge commits — must rebase or squash. Enforces clean history.

### Include administrators
By default, repo admins can bypass rules. Check this to prevent even admins from bypassing.

### Restrict who can push
Only certain users/teams can push to the protected branch. Great for shared branches.

### Allow force pushes / Allow deletions
Uncheck both for `main` — you don't want anyone force-pushing or deleting it.

## The recommended baseline for `main`
1. Require pull request before merging
2. Require 1 approval (or 2 for critical repos)
3. Require CI status checks
4. Require branches up to date
5. Require conversation resolution
6. Include administrators (yes — no bypasses)
7. Disallow force pushes and deletions

This baseline stops 99% of accidents.

## CODEOWNERS: who reviews what
`.github/CODEOWNERS` (or `CODEOWNERS` at repo root) maps file paths to required reviewers:
```
# Global fallback
*                    @rotem @alice

# Frontend
/frontend/           @alice @bob
/frontend/mobile/    @bob

# DSP code
/src/dsp/            @rotem
/src/dsp/biquad.c    @rotem @carol

# CI configs
/.github/            @tech-lead
```
When someone opens a PR:
- GitHub auto-assigns reviewers based on which files changed
- If "Require review from Code Owners" is on, PR is blocked until CODEOWNER approves

Great for large repos where different modules have different domain owners.

## Rulesets (newer, more powerful)
GitHub's newer feature: **Rulesets** (Repo → Settings → Rules → Rulesets).
- Everything branch protection does, plus more
- Multiple rulesets can apply to the same branch (composable)
- Can bypass with specific users (auditable)

Rulesets are gradually replacing classic branch protection. Both work; for new setups, prefer Rulesets.

## Required status checks and CI
For "Require status checks" to work, you need CI configured (Module 28). The status checks are:
- GitHub Actions workflow results
- External CI (Travis, CircleCI, custom)
- Any bot that posts a check status

Once a check name shows up in a PR's checks section, you can require it. Then merges without that check green are blocked.

## Environments and required reviewers for deploys
Beyond branch protection, GitHub Environments (Settings → Environments) let you:
- Define named environments: `staging`, `production`
- Require reviewers to approve DEPLOYMENTS to those environments
- Restrict which branches can deploy

Example: your CI deploys on merge to main. But `production` environment requires manual approval — 1 SRE person clicks Approve before deploy proceeds.

Blocks accidental deploys. Very common pattern for production-facing services.

## Repository role and permissions
GitHub permissions (repo Settings → Collaborators or Org → Teams):
- **Read** — clone and pull only
- **Triage** — read + manage issues/PRs (label, close)
- **Write** — read + push branches + merge PRs
- **Maintain** — write + some settings
- **Admin** — everything

For team projects: give devs **Write**, tech leads **Maintain**, org owners **Admin**. Never grant more than needed.

## Two-factor authentication for the org
Org owners can require ALL members to have 2FA enabled. Non-compliant members lose access.

Enforce in: Org Settings → Authentication security.

## Secret scanning and dependabot
GitHub auto-scans repos for:
- **Committed secrets** — flags AWS keys, API tokens, etc. in commits/PRs
- **Vulnerable dependencies** — Dependabot alerts and auto-PRs to update

Both are free and should be enabled. Free find-real-problems automation.

Enable: Repo → Settings → Security & analysis → Enable all recommended.

## Audit log (org / enterprise)
Every setting change, permission grant, push, etc. is logged. Org owners can view via:
- Org Settings → Audit log

For compliance, this is essential. For personal use, informational.

## Practical minimum for a small team
1. Branch protection on main: require PR, require 1 review, require CI green
2. Delete branches after merge (auto-delete in repo settings)
3. Enable Dependabot alerts
4. Enable secret scanning
5. 2FA on all accounts

This baseline gives a well-run team ~90% of the safety of a highly-regulated setup.
"""),
        "exercises": [
            ex(
                "27-1",
                "In your `git-lab` (public), on GitHub: Settings → Branches → Add rule → Branch name = `main` → check: Require pull request before merging, Require 1 approval, Do not allow bypassing. Save. Now try to push directly to main from GHD — GitHub rejects it.",
                "Feel the friction of enforced rules.",
                "Push rejected with 'required status check' or 'must be reviewed' message. Now you're FORCED into the PR workflow. Even solo, this discipline is good practice.",
            ),
            ex(
                "27-2",
                "Create a `.github/CODEOWNERS` file. Content:\n```\n* @YOUR-USERNAME\n/docs/ @YOUR-USERNAME\n```\nCommit via PR (since main is protected!). Verify: future PRs auto-assign you as reviewer.",
                "First CODEOWNERS setup.",
                "You are the automatic reviewer for everything (and specifically for docs). On a real team, different owners for different directories give clean review routing.",
            ),
            ex(
                "27-3",
                "In Settings → General → Pull Requests: uncheck 'Allow merge commits', keep 'Allow squash merging' only. Now future PR merges will be squash-only. This is one way to enforce clean linear history.",
                "PR merge strategy enforcement.",
                "Squash-only merges keep main's history clean — one commit per PR. Different teams prefer different strategies. Enforce whichever you pick.",
            ),
            ex(
                "27-4",
                "Enable secret scanning and Dependabot alerts: Settings → Security & analysis → Enable everything free. Now GitHub scans your code for exposed secrets and vulnerable dependencies automatically.",
                "Free automated security help.",
                "Two more layers of automated safety. Every push gets scanned. Alerts appear in Security tab. For a solo project, mostly informational. For a team, catches things humans miss.",
            ),
            ex(
                "27-5",
                "Discuss (in `git-lab/protection-strategy.md`): for a 5-person team's production repo, what protection would you set? For a solo learning repo? Justify.",
                "Match protection level to context.",
                "5-person team production: full baseline (PR + 2 approvals + CI + CODEOWNERS + no bypasses + squash-only). Solo learning: PR + 1 approval (self) + CI. Even solo, PRs give you the pause/reflection habit. Overkill = friction that hurts productivity; too little = accidents happen. Match to real risk.",
            ),
        ],
    },
    {
        "id": "28",
        "title": "GitHub Actions: Your First CI",
        "level": "Advanced",
        "summary": "Automate anything that runs when a Git event happens. Tests on every PR, deploys on every merge, scheduled jobs.",
        "body": md("""
## What GitHub Actions is
A CI/CD (Continuous Integration / Continuous Deployment) service built into GitHub. Free for public repos, generous free tier for private (2000 min/month on the free plan).

Runs YOUR code (called a **workflow**) in response to events (**triggers**):
- Push to a branch
- PR opened / synchronized
- Schedule (cron)
- Manual dispatch
- Release published
- And 30+ more

## The workflow file
Workflows live in `.github/workflows/*.yml`. YAML files describing what to run.

Minimal example — `.github/workflows/tests.yml`:
```yaml
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
      - run: pip install pytest
      - run: pytest
```

Commit this to your repo. On next push or PR, GitHub runs the workflow in a fresh Ubuntu VM, executes the steps, and reports pass/fail as a check.

## The anatomy of a workflow
```yaml
name: Human-readable workflow name
on: [triggers]                    # what runs it
jobs:
  job-name:                       # one or more jobs
    runs-on: os-image             # what OS to run on
    steps:
      - name: Step name           # optional
        uses: action@version      # use a pre-built action
      - name: Another step
        run: shell command        # or run a command
```

## Common triggers
```yaml
on: push                          # any push
on: pull_request                  # any PR event
on: [push, pull_request]          # both

on:
  push:
    branches: [main]              # only pushes to main
  pull_request:
    branches: [main]              # only PRs targeting main
  schedule:
    - cron: '0 3 * * *'           # daily at 3 UTC
  workflow_dispatch:              # manual trigger button
```

## Actions marketplace
The `uses:` line references a pre-built action. Thousands available:
- `actions/checkout@v4` — clone your repo into the VM
- `actions/setup-python@v5` — install Python
- `actions/setup-node@v4` — install Node
- `actions/cache@v4` — cache dependencies between runs
- `actions/upload-artifact@v4` — save files as downloadable artifacts

Browse: [github.com/marketplace?type=actions](https://github.com/marketplace?type=actions).

## Matrix builds — test on multiple platforms
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install pytest
      - run: pytest
```
This runs 9 jobs (3 OS × 3 Python). All parallel. If any fails, the workflow fails.

## Secrets
Never commit secrets in workflow files. Use GitHub Secrets:
- Repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `MY_API_KEY`, Value: (secret)

Access in workflow:
```yaml
env:
  API_KEY: ${{ secrets.MY_API_KEY }}
steps:
  - run: ./deploy.sh
    env:
      API_KEY: ${{ secrets.MY_API_KEY }}
```

## Caching for speed
Downloading dependencies on every run is slow. Cache them:
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: ${{ runner.os }}-pip-
```
First run: cache miss, saves cache at end. Subsequent runs: cache hit, restores in seconds.

## Deploy on merge to main
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: ./scripts/deploy.sh
```
Combined with branch protection (Module 27), merge → CI green → auto-deploy. Continuous deployment.

## Required checks (from Module 27)
Once a workflow has run at least once, its name appears in "Require status checks" in branch protection. Add it → future PRs are blocked from merging until the workflow is green.

## Debugging failed workflows
- Actions tab → click the workflow → see the log
- Each step shows its output
- Click failed steps to expand and read errors
- Common causes: missing dependency, wrong path, syntax error in YAML, permissions

Tips:
- Add `echo` statements liberally when debugging
- Use `actions/upload-artifact` to save intermediate files for inspection
- SSH into a failed run: use `mxschmitt/action-tmate@v3` action (opens SSH session, useful for hard bugs)

## Workflow examples for common languages
### Python
```yaml
- uses: actions/setup-python@v5
- run: pip install -e .[dev]
- run: pytest
```

### Node.js
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
- run: npm ci
- run: npm test
```

### C/C++
```yaml
- run: sudo apt-get install -y gcc make
- run: make
- run: make test
```

### CMake
```yaml
- run: cmake -B build -DCMAKE_BUILD_TYPE=Release
- run: cmake --build build
- run: ctest --test-dir build --output-on-failure
```

## Cost and limits
Free tier (2026):
- Public repos: unlimited minutes
- Private repos (personal free): 2000 min/month
- Storage for artifacts: 500 MB
- Concurrency: limited

Pay-as-you-go for more. For a personal project or small team, free is enough.

## Alternatives to consider
- **CircleCI, Travis, Jenkins** — pre-Actions era, still used
- **GitLab CI** — GitLab's built-in (if you're on GitLab)
- **Buildkite** — self-hosted runners
- **Local CI**: `act` runs GitHub Actions locally for testing

For 90% of GitHub users, Actions is the default and works well.

## Beyond CI: automations
Actions runs ANY code on ANY event. Beyond testing:
- Auto-label PRs based on files changed
- Post to Slack on release
- Deploy documentation on merge
- Run scheduled cleanup jobs
- Trigger external services

The pattern is: "when X happens, do Y." Countless uses.
"""),
        "exercises": [
            ex(
                "28-1",
                "In `git-lab`, create `.github/workflows/hello.yml`:\n```yaml\nname: Hello\non: [push]\njobs:\n  say-hi:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo 'Hello, Actions!'\n```\nCommit via PR (main is protected). Merge. Go to Actions tab — verify the workflow ran and printed the message.",
                "First CI workflow.",
                "You have a green check on your commit. The Actions tab shows the run log. This is the base pattern — every advanced workflow is variations on this template.",
            ),
            ex(
                "28-2",
                "Expand the workflow: add pytest. Create `test_dummy.py` at repo root: `def test_pass(): assert True`. Update the workflow to install pytest and run it. Push. Verify the workflow installs Python, pytest, runs, passes.",
                "The minimum-viable Python CI.",
                "```yaml\nname: Tests\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.11'\n      - run: pip install pytest\n      - run: pytest\n```\nGreen check appears on PRs. This one file gives you automated testing on every change.",
            ),
            ex(
                "28-3",
                "Break the test intentionally (`assert False`). Push. Verify: CI turns RED. The PR is blocked (if branch protection requires CI). Fix. Push. CI turns GREEN. PR unblocked.",
                "Feel the CI feedback loop.",
                "Red check, blocked merge. Fix, green check, unblocked. This is the entire value of CI — you see quality problems in seconds, not weeks. Every dev on every project should have at least this.",
            ),
            ex(
                "28-4",
                "Add matrix build: test on 3 Python versions. Verify Actions tab shows 3 parallel jobs.",
                "Multi-version testing.",
                "```yaml\nstrategy:\n  matrix:\n    python: ['3.10', '3.11', '3.12']\n```\nThree jobs run in parallel. If one fails, workflow fails. This catches version-specific bugs before your users hit them.",
            ),
            ex(
                "28-5",
                "Add caching for pip. Compare a fresh run vs a cached run — the cached run is much faster.",
                "Cache = speed win.",
                "```yaml\n- uses: actions/cache@v4\n  with:\n    path: ~/.cache/pip\n    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}\n```\nFirst run: cache miss, saved. Second run: cache hit, deps install in seconds. Saves minutes per run on real projects.",
            ),
        ],
    },
    {
        "id": "29",
        "title": "Secrets, Environments, Deploy Keys",
        "level": "Advanced",
        "summary": "How to store credentials without ever committing them. Deploy safely from CI.",
        "body": md("""
## The rule: never commit secrets
- No API keys in code
- No passwords in configs
- No tokens in commit messages
- No `.env` files with real values

Committed secrets are compromised forever — even if you delete the commit, someone may have already scraped it. Assume any secret in a commit (even deleted) is compromised → rotate immediately.

## Where secrets belong
- Local dev: `.env` file in `.gitignore` (never committed), or environment variables in your shell
- CI: GitHub Secrets (Repo → Settings → Secrets and variables → Actions)
- Prod: your deploy platform's secret manager (AWS Secrets Manager, K8s secrets, Doppler, 1Password Connect)

## Adding a repo secret
Repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `MY_API_KEY` (uppercase, underscores convention)
- Value: paste the secret
- Add secret

Once saved, you can NEVER view the value again. Only overwrite or delete.

## Using secrets in workflows
```yaml
steps:
  - run: ./deploy.sh
    env:
      API_KEY: ${{ secrets.MY_API_KEY }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```
The `secrets.` prefix accesses stored secrets. Values are injected as environment variables at runtime, never printed to logs (GitHub auto-masks known secret values in logs).

## Environment vs repository secrets
- **Repository secrets** — available to any workflow in the repo
- **Environment secrets** — only available to workflows targeting a specific "environment"

Environments (Settings → Environments) let you:
- Group secrets by environment: `staging` vs `production`
- Require reviewers before deploys to that environment
- Restrict which branches can deploy

Example:
```yaml
jobs:
  deploy:
    environment: production
    steps:
      - run: ./deploy.sh
        env:
          KEY: ${{ secrets.PROD_KEY }}
```
`production` environment might require 2 approvals from designated reviewers before running. Prevents accidental production deploys.

## Deploy keys (SSH-based)
For deploying to a specific server via SSH:
- Generate an SSH key pair on the server
- Add public key to server's `~/.ssh/authorized_keys`
- Add private key to GitHub as a **Deploy Key** (Repo → Settings → Deploy keys) OR as a secret

In workflow:
```yaml
- name: Setup SSH
  uses: webfactory/ssh-agent@v0.9.0
  with:
    ssh-private-key: ${{ secrets.DEPLOY_SSH_KEY }}
- run: ssh user@server 'cd /app && git pull && systemctl restart'
```

## OIDC (OpenID Connect) — no long-lived secrets
Modern approach: instead of storing long-lived cloud credentials as secrets, use OIDC to exchange a short-lived GitHub token for a cloud provider token per-job.

Supported by AWS, Azure, GCP:
```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-deploy
      aws-region: us-east-1
  - run: aws s3 sync build/ s3://my-bucket/
```
No long-lived AWS key in secrets. GitHub authenticates as itself; AWS verifies and grants a temporary token. Much safer.

For serious cloud work, use OIDC.

## Personal Access Tokens (PATs)
For CLI Git access to private repos (or via workflow to modify other repos):
- github.com/settings/tokens → Generate new (classic)
- Name it, set expiration, pick scopes (`repo` for full repo access)
- Save the token immediately (only shown once)

Use in CLI:
```bash
# git prompts for password → paste PAT
git push
```
Or store in credential helper (Windows Credential Manager, macOS Keychain, Linux libsecret).

PATs are user-scoped and have the user's permissions. Alternative: **fine-grained PATs** (newer, per-repo scoped).

## GitHub App vs PAT vs OIDC
When your workflow needs to interact with GitHub (create issues, comment on PRs, push to other repos):

- **`GITHUB_TOKEN`** (built-in) — auto-provided per workflow run. Limited to the current repo. Free.
- **PAT** (user token) — user's permissions. Convenient for personal projects. Do not use for team workflows (belongs to one person).
- **GitHub App** — proper way for team/org bots. Own identity, permissions per install. More setup, but correct.

Rule: for anything beyond the current repo, use a GitHub App. For within the current repo, `GITHUB_TOKEN` is enough.

## Secret rotation
Best practice: rotate secrets on a schedule (quarterly, annually) even if not compromised:
1. Generate a new secret (new API key, new SSH key)
2. Update in GitHub Secrets
3. Deploy (trigger a run — verify workflow still works)
4. Revoke the old secret at the source

For accidentally exposed secrets: rotate immediately, not scheduled. Assume compromised.

## Auditing secret access
GitHub logs when secrets are accessed by workflows. Admins can review via Audit Log (org-level). Regular audits catch:
- Unexpected accesses
- Secrets that are no longer needed (delete them)
- Compromised runs

## The .env.example pattern
For local dev, provide a template (committed) and a real file (gitignored):

`.env.example` (committed):
```
API_KEY=your_api_key_here
DB_PASSWORD=your_password_here
```

`.env` (gitignored):
```
API_KEY=actual-secret-value
DB_PASSWORD=actual-password
```

New developers copy `.env.example` → `.env`, fill in real values from a secure share (password manager, 1Password vault). Real values never enter git.

## Emergency: leaked secret
If a secret WAS committed and pushed:
1. **Rotate immediately** — assume it's already been scraped
2. Remove from source code, add to `.gitignore`
3. Optionally: scrub from history (BFG, git filter-repo)
4. Force-push scrubbed history (coordinate with team)
5. All collaborators re-clone

The rotate step is critical. History-scrubbing alone doesn't help — the secret was public for some window.

## The full picture
```
Developer → local .env (gitignored)
     ↓
Commit code (no secrets)
     ↓
Push to GitHub
     ↓
Workflow runs on push
     ↓
Workflow reads GitHub Secrets
     ↓
Deploys with secrets as env vars
     ↓
Production reads secrets from platform's secret manager
```
Secrets flow from secure stores to runtime, never through git. That's the whole point.
"""),
        "exercises": [
            ex(
                "29-1",
                "In `git-lab`: Settings → Secrets and variables → Actions → New repository secret → name `TEST_SECRET`, value `hello`. Update your `hello.yml` workflow to print the length (not the value!) of the secret. Push. Verify: log shows the length, secret value is not exposed.",
                "First secret usage.",
                "```yaml\n- run: echo \"secret length is ${#TEST_SECRET}\"\n  env:\n    TEST_SECRET: ${{ secrets.TEST_SECRET }}\n```\nLog shows '5'. Never print the value directly — CI logs are visible to anyone with repo access.",
            ),
            ex(
                "29-2",
                "Create an Environment: Settings → Environments → New environment → `production`. Add a required reviewer (yourself). Add an env-specific secret `PROD_KEY`. In your workflow, add `environment: production` to a job. Push — workflow pauses at the deploy job, awaits your approval.",
                "Deploy gate practice.",
                "You approve → deploy proceeds. This is exactly how production deploys work in serious teams: an SRE clicks Approve before production changes. Prevents 3am accidents.",
            ),
            ex(
                "29-3",
                "Create a `.env.example` file with placeholder values. Add `.env` to `.gitignore`. Commit. Verify: `.env.example` in repo, `.env` invisible to Git even if you create it.",
                "The .env.example pattern.",
                "New collaborators know what env vars to set (from .env.example) but real values stay local. Standard pattern for any project with local config.",
            ),
            ex(
                "29-4",
                "Discuss (in `git-lab/secrets-strategy.md`): what would you use for these scenarios?\n(a) API key for a personal script that runs on your laptop\n(b) Deploy key for pushing your site to a server from CI\n(c) AWS credential for deploying to production",
                "Match tool to scenario.",
                "(a) Local `.env` file, in .gitignore. (b) GitHub Deploy Key or SSH secret in Actions Secrets. (c) OIDC federation — no long-lived AWS keys anywhere; GitHub authenticates directly to AWS per-workflow. Modernizing from PATs to OIDC is a common migration.",
            ),
            ex(
                "29-5",
                "Read: what would you do if you accidentally committed a real API key? Write the 5-step recovery procedure in `git-lab/incident-response.md`.",
                "Preparedness matters — this WILL happen to you eventually.",
                "1. Rotate the API key at the source IMMEDIATELY (revoke the leaked key, generate a new one). 2. Update all systems using it (GitHub Secrets, prod config). 3. Remove from source, add pattern to .gitignore. 4. Optionally scrub from history with BFG/filter-repo (force-push). 5. Retrospective: how did this happen? Add pre-commit hook (e.g., `gitleaks`) to prevent recurrence.",
            ),
        ],
    },
    # ────────────────────── PHASE 9: CAPSTONE ──────────────────────
    {
        "id": "30",
        "title": "Capstone: Ship a Real Project End-to-End",
        "level": "Expert",
        "summary": "Apply every module. Build, review, ship a project through the complete workflow with real discipline.",
        "body": md("""
## The capstone challenge
Take a project — real or invented — and ship version 1.0 using every technique from the course. This is where mastery consolidates.

Suggested project: a small CLI tool (any language). Options if stuck:
- A file organizer (moves files by extension)
- A note-taking CLI (add/list/search notes)
- A DSP utility (e.g., simple WAV analyzer)
- Anything you'd genuinely find useful

## The deliverables
### 1. A repo on GitHub
- Public or private (your choice)
- README.md with description, install, usage
- LICENSE
- .gitignore appropriate to the language
- .gitattributes with sensible line-ending rules
- CONTRIBUTING.md with branch naming conventions

### 2. Branching discipline
- All changes via feature branches
- No direct pushes to main
- Descriptive branch names (`feat/*`, `fix/*`, etc.)
- Deleted after merge

### 3. PRs for every change
- At least 5 PRs during development
- Good titles and descriptions (from Module 07 and 17)
- Linked to issues where relevant
- Self-review before requesting approval

### 4. Issues tracked
- At least 3 issues created (feature/bug/question)
- Labels applied
- At least one milestone (`v1.0.0`)
- Issues closed via PRs (`Closes #N`)

### 5. CI passing
- GitHub Actions workflow that runs tests on every push and PR
- Set as required status check
- Matrix build if applicable

### 6. Branch protection on main
- Require PR
- Require 1 approval (self-approve OK for solo)
- Require CI green
- No force pushes, no deletions

### 7. Semantic versioning + release
- Tag `v1.0.0`
- Publish as a GitHub Release
- Release notes describing what's in v1.0.0

### 8. Historical hygiene
- Every commit has a good message
- No secrets in history
- No huge binaries (unless via LFS)
- Linear or cleanly-merged history

### 9. Real workflow used
- Fetch daily
- Small commits, frequent
- PRs opened for feedback, iterated, merged
- Branches deleted after merge

## The acceptance criteria (self-scored)
Score each 1-3 (basic / good / excellent):
- [ ] Repo has README, LICENSE, .gitignore, CONTRIBUTING.md
- [ ] Branch protection enforced on main
- [ ] All changes via PRs (verify: no direct pushes in main's history)
- [ ] At least 5 merged PRs
- [ ] At least 3 issues, at least 1 milestone
- [ ] CI workflow runs on every push, passes
- [ ] CI required for merge (branch protection)
- [ ] All commit messages follow the 7 rules (Module 07)
- [ ] v1.0.0 tag + Release published with notes
- [ ] Zero secrets in history (`git log -p | grep -i "api_key\\|password"` returns nothing sensitive)

Target: ≥ 24/30 total. Below 20/30 → tighten the weak areas before declaring done.

## The mindset shift
You started thinking "Git is a black box, GHD is buttons." You leave thinking "Git is a small set of primitives, and I know them; GHD is the UI I use daily, CLI is the tool for when I need control; GitHub is where my work lives and where I collaborate; everything integrates."

That is the shift.

## Where to go next
- **Contribute to open source**: pick a project, find a `good-first-issue`, follow the fork-clone-PR flow (Module 19)
- **Set up CI in real projects**: apply Module 28 to your day-job repos
- **Learn interactive rebase**: it's the CLI skill that pays off most (Module 23)
- **Explore GitHub Apps**: build your own bots that respond to events
- **Study another workflow**: Git Flow if your team uses it, trunk-based development if that fits better

## The final reflection
Write in `git-lab/capstone-reflection.md`:
- What was hardest?
- What clicked mid-course?
- What will you do differently on your next project?
- What single Git superpower do you feel you've gained?

Save this. Read it in 6 months. Compare to who you are then.
"""),
        "exercises": [
            ex(
                "30-1",
                "Create the capstone repo. Name it whatever suits your project. Add README, LICENSE, .gitignore, .gitattributes, CONTRIBUTING.md. This is your foundation.",
                "The setup pass from Modules 05, 26, 27.",
                "Repo exists with hygiene files in place. Publish to GitHub. This is the moment the project stops being 'scratch' and becomes 'real'.",
            ),
            ex(
                "30-2",
                "Enable branch protection on main: require PR + 1 review + CI. From now on, EVERYTHING goes through a PR. This is the discipline that makes the workflow work.",
                "Enforce the rules mechanically.",
                "Direct pushes to main are now impossible. Even by you. Every change is a PR. This may feel like overhead — it isn't. It's the discipline that catches half of would-be problems.",
            ),
            ex(
                "30-3",
                "Set up CI: GitHub Actions workflow that runs tests (or a build) on every push and PR. Mark as required in branch protection. Verify: a broken PR is blocked from merging.",
                "Module 28's automation in place.",
                "CI green = mergeable. CI red = blocked. This automation is what turns 'we should test' into 'we always test'. Every push validated.",
            ),
            ex(
                "30-4",
                "Ship at least 5 meaningful PRs. Each: branch off main, commit, push, open PR with good description, self-review, merge, delete branch. Track: how long does the full cycle take once you're in flow?",
                "Muscle memory for the workflow.",
                "Typical cycle: 5-30 minutes for a small change. After 5 iterations, the pattern is automatic. You STOP thinking about mechanics and START thinking about the work.",
            ),
            ex(
                "30-5",
                "Create at least 3 issues. Assign labels. Create a `v1.0.0` milestone. Close issues via PRs using `Closes #N` in PR descriptions.",
                "Traceability from user problem → code fix.",
                "Issues closed automatically when PRs merge. The historical trail from 'this was a bug' to 'here's the fix commit' is preserved forever. Future you (or a future maintainer) can walk the history.",
            ),
            ex(
                "30-6",
                "Tag v1.0.0. Publish a GitHub Release with release notes summarizing what's in v1.0.0. Verify: the Releases page shows it as Latest.",
                "The ceremonial shipping of version 1.",
                "Your project has a real release. Users could install it. You have marked a milestone in the history. Every future change is 'post-v1.0.0'. The discipline of releasing forces you to think 'is this ready?' — which is valuable.",
            ),
            ex(
                "30-7",
                "Self-score against the acceptance criteria (10 items, 3 points each). Address any item below 2/3 with follow-up commits. Aim for 24/30 or better.",
                "Honest self-assessment.",
                "You have a comprehensive score. Weak areas identified. Address them or knowingly accept the trade-off. This is how professional engineering works: assess against criteria, close gaps.",
            ),
            ex(
                "30-8",
                "Write `capstone-reflection.md`. Answer the questions from the module. This is your knowledge-consolidation moment.",
                "Explicit reflection cements learning.",
                "You have a written record of your Git journey. Read it periodically. Compare to your future self's evolution. Learning is a process; this document is a snapshot of a big step forward.",
            ),
        ],
    },
    # ────────────────────── DRILLS ──────────────────────
    {
        "id": "drills",
        "title": "Daily Drills",
        "level": "All levels",
        "summary": "Quick reps to build Git + GHD fluency. One per day, five minutes each.",
        "body": md("""
## How to use drills
One drill per day, in addition to modules. Each takes ~5 minutes. Repetition builds muscle memory.
"""),
        "exercises": [
            ex("D-01", "In GHD, use Ctrl/Cmd+1 (Changes), Ctrl/Cmd+2 (History), Ctrl/Cmd+Enter (commit), Ctrl/Cmd+P (push). Use them for every operation today, no mouse.", "Shortcuts pay off cumulatively.", "You're faster tomorrow than yesterday. Small wins compound."),
            ex("D-02", "Make one commit with a summary + description body. Follow the 7 rules from Module 07.", "Descriptive commits become habitual.", "Your history readability improves permanently."),
            ex("D-03", "Create a branch, make a commit, delete the branch (locally and remote). No merge — practice the create/delete cycle.", "Branches are cheap.", "You stop hesitating to create branches. That mental unblock is worth days per year."),
            ex("D-04", "Open Terminal from GHD → run `git log --oneline --graph --all`. Read the topology.", "CLI is your friend.", "You gradually build CLI fluency without abandoning GHD."),
            ex("D-05", "Do a `git add -p` on any file with multiple changes. Say y/n/s per hunk. Commit only the y hunks.", "Granular staging = clean commits.", "Your commits become focused even when your working directory isn't."),
            ex("D-06", "Rebase your current feature branch onto latest main. Handle any conflicts calmly (Module 15).", "Rebase practice keeps history clean.", "You stop fearing rebase. Feature branches stay up to date."),
            ex("D-07", "Open one of your recent PRs. Review it as if it were someone else's. Add 3 inline comments (nit / suggestion / question).", "Reviewing your own work catches issues.", "Half of code review comments come from a good self-review beforehand."),
            ex("D-08", "Fetch origin. Look at what's new. If behind, pull. If ahead, push. Get into rhythm.", "Morning sync habit.", "You start your day with full context of what changed on the team overnight."),
            ex("D-09", "Right-click any file → View history for the file. Read the last 5 changes. What has the file been used for?", "History reading is archaeology.", "You develop intuition for tracking down 'why is this code here?' — a superpower for maintenance."),
            ex("D-10", "Deliberately mess something up (bad commit, wrong branch). Use undo (Module 21) to recover. Practice under low stakes.", "Undo confidence.", "Real Git crises are terrifying without undo practice. Do it now in a safe repo — the real crisis will be manageable."),
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
  <title>Git + GitHub via GitHub Desktop — Zero to Hero</title>
  <style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #21262d;
  --text: #e6edf3;
  --muted: #8b949e;
  --accent: #6f42c1;
  --accent2: #a371f7;
  --warn: #d29922;
  --ok: #3fb950;
  --border: #30363d;
  --ex: #1c2029;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); line-height: 1.55; }
a { color: var(--accent2); }
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
nav.sidebar button.module-link.active { background: var(--accent); color: #fff; font-weight: 600; }
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
  background: #010409; border: 1px solid var(--border); border-radius: 8px;
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
button.btn-primary { background: var(--accent); color: #fff; }
button.btn-ghost { background: var(--surface2); color: var(--text); }
button.btn-ok { background: #196c2e; color: #ecfdf5; }
.exercise.done { border-left-color: var(--ok); opacity: 0.92; }
.solution {
  display: none; margin-top: 0.85rem; padding: 0.85rem; background: #010409;
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
          Open this file in any browser. Progress saves to <code>localStorage</code>.
          <strong>%%TOTAL%% exercises</strong> · concepts + hands-on in GitHub Desktop · CLI shown only when GHD can't do the thing.
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
const STORAGE_KEY = 'git-github-desktop-course-v1';

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
        "title": "Git + GitHub via GitHub Desktop — Zero to Hero",
        "subtitle": "Concepts · GHD workflows · PRs · CI · Branch protection · Capstone",
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
