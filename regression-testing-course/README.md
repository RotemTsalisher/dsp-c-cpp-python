# Regression Testing — Theory & Practice

**Format:** Standalone HTML course (spa-course), 26 modules, 104 exercises.
**Languages used:** Python (pytest — most exercises), C (minimal harness), C++ (doctest), MATLAB (unit tests + golden generation). Language chosen per exercise for fastest concept delivery.
**Prerequisites:** None. Starts from absolute scratch.

## What This Is
A concept-heavy course on regression testing — what it is, why it exists, what the standard use cases look like, and how to set up regression tests in practice. Exercises serve the learning of the concept, not busywork.

## Modules (6 phases)
| Phase | Modules | Focus |
|-------|---------|-------|
| **1. Foundations** | 00–04 | What / why / vocabulary / lifecycle |
| **2. Concepts** | 05–09 | AAA structure, goldens, tolerances, isolation, quality criteria |
| **3. Practical Setup** | 10–14 | pytest, C harness, DSP goldens, MATLAB, C++/doctest |
| **4. Real Use Cases** | 15–19 | Bug-fix / refactor / numerical / performance / API |
| **5. Automation** | 20–23 | CI/CD, bisect, flakies, suite maintenance |
| **6. Capstone** | 24 | Build a complete regression suite for a real module |
| **Drills** | drills | Daily 5-minute reps |

## How to Open
Double-click `index.html`. It runs in any browser. Progress is saved to `localStorage` under the key `regression-testing-course-v1`.

## How to Regenerate
```bash
python generate_course.py
```
Rewrites `index.html` from the module data. Edit `generate_course.py` to change content.

## Toolbox for Exercises
Minimum useful setup:
```bash
python -m pip install --user pytest numpy
gcc --version   # for C exercises
```
Optional: MATLAB (Module 13), a C++ compiler with doctest.h (Module 14).

## Working Directory
Exercises write into a lab directory:
```
regression-lab/
  python/     # pytest exercises
  c/          # C harness exercises
  cpp/        # doctest exercises
  matlab/     # MATLAB test exercises
  goldens/    # generated golden files + generators
  capstone/   # final project
```
Create it once (Exercise 00-2) and reuse throughout.

## Design Notes
- Concept-heavy: every module has substantial theory before exercises.
- Language pragmatism: the same idea might be shown in Python OR C depending on which makes the concept clearer.
- Self-scored capstone: 10 acceptance criteria, 30-point scale.
- Daily drills are separate from module exercises — for maintenance after the course.
