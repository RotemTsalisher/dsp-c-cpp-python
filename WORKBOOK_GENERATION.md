# Course Workbook Generation — Reference for the Assistant

Point the assistant to this file **before** creating or extending workbooks for `c-beg-to-adv` or `cpp-beg-to-adv`. The authoritative curriculum list is the matching `course-subjects.txt` inside each course folder.

---

## 1. Scope of topics (non‑negotiable)

- **Only** subjects that appear in `course-subjects.txt`, in **the same order** as in that file.
- Do **not** introduce topics “because they are normal C/C++” if they are absent from the list or listed as missing.
- For **C** (`c-beg-to-adv`): ANSI **C11**; headers such as `<stdio.h>`, `<math.h>`, `<string.h>`, `<stdlib.h>` as allowed by the subject list.
- For **C++** (`cpp-beg-to-adv`): **C++20** unless the user specifies otherwise; respect any “MISSING FOR NOW” lines in that course’s subject file (e.g. defer STL containers until listed).

---

## 2. Deliverables

### A. Main workbooks folder

- **Path:** `<course>/workbooks/` with optional batch subfolders (`batch-01/`, `batch-02/`, …) when the user requests a new batch without overwriting prior work.
- **Three** standalone **HTML** workbooks per batch:
  1. **First half of the curriculum** — subjects from the **first half** of the ordered list (split by subject count; e.g. 29 subjects → 1–14 and 15–29).
  2. **Second half of the curriculum** — the **remaining** subjects in order.
  3. **Interview-style** — fewer integrated prompts resembling technical screens; still **only** allowed topics; revealable solutions.

### B. Exercise count and difficulty (main half workbooks)

**Rejected pattern (do not use for new batches):** a single workbook with only **5–7** total exercises spanning many subjects.

**Required pattern:**

| Rule | Detail |
|------|--------|
| **Per subject** | Exactly **2** exercises for **every** active subject in that half. |
| **Order** | Subjects appear in **`course-subjects.txt` order**; within each subject, **medium** then **hard**. |
| **Difficulty** | **Medium** — focused practice on that subject; challenging but not a capstone. **Hard** — same subject, noticeably harder; may reuse earlier subjects but must still center on the current subject. |
| **No warm-up tier** | Do not label “easy”; only **medium** and **hard** within each subject block. |
| **Milestones** | Milestone subjects (e.g. “milestone (1) project”, “milestone (2) game”) also get **medium + hard** — two distinct projects/games at different scope. |

**Example:** first half with 14 subjects → **28** exercises (14 × 2). Second half with 15 subjects → **30** exercises (15 × 2).

### C. Everyday practice folder (C++ course)

- **Path:** `cpp-beg-to-adv/exeryday-practice/` (spelling as in repo).
- **One** HTML workbook with **one straightforward exercise per subject** — simpler than main workbooks.

---

## 3. Instructions and solutions (user requirements)

- **`exercises-instructions.txt`:** Optional legacy detail for some C++ flows. When the user says to **ignore** it, generate **only** from this file + `course-subjects.txt`.
- **Exercise text:** **Clear, precise, descriptive** requirements (context + bullet/numbered deliverables).
- **No solution hints in the exercise body:** Do **not** include “Topics: …”, threshold spoilers, algorithm nudges, or partial code answers in the visible instruction. The student should not see how to solve it until they click **Reveal solution**.
- **Solutions:** Full **C** or **C++** (as appropriate) behind a **button** (toggle hidden block), plus a **short “why”** explaining the relevant course feature.

---

## 4. Framing and cumulative mix

- **EE / DSP context** where sensible: AFE, uplink frames, comb/mono-mix, PSD bins, registers, buffers, HIL capture.
- **Cumulative mix:** Hard exercises may combine earlier tools; later subjects in a half may assume skills from earlier subjects in that same half.
- **Distinct batches:** New batch folders should use **new scenarios** — not duplicates of prior batches.

---

## 5. HTML / UI rules

- Each workbook is a **single standalone `.html` file** unless the user asks otherwise.
- Align with existing workbook styling (exercise cards, difficulty badges, reveal buttons).
- Badge colors: **medium** (e.g. amber/gold), **hard** (e.g. orange/dark). Subject section headers group the pair.
- **Every exercise** must have **Reveal solution**.

---

## 6. Technical constraints

### C (`c-beg-to-adv`)

- ANSI **C11**; no C++.
- Fixed buffers and static arrays unless the subject introduces pointers/files.
- Prefer professional names (`UplinkFrame`, `classify_sample`) over toy names.

### C++ (`cpp-beg-to-adv`)

- **C++20** where the curriculum allows.
- Prefer **named function-pointer types** over `std::function` when avoiding STL.
- Without STL containers: raw arrays, fixed buffers, `new`/`delete` as appropriate.

---

## 7. File checklist

| Item | C course | C++ course |
|------|----------|------------|
| Curriculum | `c-beg-to-adv/course-subjects.txt` | `cpp-beg-to-adv/course-subjects.txt` |
| Main workbooks | `c-beg-to-adv/workbooks/batch-NN/*.html` | `cpp-beg-to-adv/workbooks/*.html` |
| Everyday practice | — | `cpp-beg-to-adv/exeryday-practice/*.html` |

---

## 8. Pre-flight checklist

1. Re-read `course-subjects.txt` — **count** and **order** of subjects.
2. Split **first half / second half** (ceil or floor half; document split in workbook scope box).
3. Plan **2 × subject_count** exercises per half workbook; interview workbook separately.
4. Confirm **no forbidden topics** and **no hints** in exercise bodies.
5. New batch → new folder; **do not modify** prior batches unless asked.

---

*Updated after batch-02 feedback: two exercises per subject (medium + hard), no in-exercise hints, `exercises-instructions.txt` optional.*
