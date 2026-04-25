  # C++ Course Workbook Generation — Reference for the Assistant

Point the assistant to this file **before** creating or extending workbooks for `cpp-beg-to-adv`. The authoritative curriculum list is `cpp-beg-to-adv/course-subjects.txt`. The extended protocol is `cpp-beg-to-adv/exercises-instructions.txt`.

---

## 1. Scope of topics (non‑negotiable)

- **Only** subjects that appear in `course-subjects.txt`, in **the same order** as in that file.
- Do **not** introduce topics “because they are normal C++” if they are absent from the list or listed as missing.
- Treat these as **out of scope** unless `course-subjects.txt` is updated (see the file’s “MISSING FOR NOW” section), for example:
  - STL containers (`vector`, `map`, etc.).
  - `std::string` / `std::string_view` when those lines are still marked missing.
- Prefer **no** `std::function` when avoiding the STL broadly; use **explicit function-pointer typedefs** (see §4).

---

## 2. Deliverables the user requested

### A. Main workbooks folder

- **Path:** `cpp-beg-to-adv/workbooks/` (sibling to other course folders).
- **Three** standalone **HTML** workbooks:
  1. **First half of the curriculum** — exercises covering roughly **the first half** of the ordered subject list (split the full list in two halves; e.g. subjects 1–21 vs 22–42 when there are 42 lines).
  2. **Second half of the curriculum** — the **remaining** subjects in order.
  3. **Interview-style** — prompts resembling technical interviews, still **only** using allowed topics, still **C++** with revealable solutions.

### B. Everyday practice folder

- **Path:** `cpp-beg-to-adv/exeryday-practice/` (spelling as requested — parallel to `workbooks`).
- **One** HTML workbook with **one straightforward exercise per subject** (every line in `course-subjects.txt` that is an active subject), simpler than the main workbooks.

---

## 3. Protocol from `exercises-instructions.txt` (adapt to halves + interview)

- **Batching (for large workbooks):** Original protocol uses batches of **5–7** subjects; **strict order**; **every subject in a batch** should appear in the exercises (directly or clearly woven in). When building “first half” / “second half” workbooks, respect the same **order** and **cumulative mix** (later exercises should reuse ideas from earlier subjects in that half).
- **Difficulty:** **5–7 exercises** per main workbook is appropriate; **progressive** difficulty (warm-up → harder); the **last one or two** should stress the **newest** subjects in that half while pulling in earlier tools.
- **EE framing:** Problems should be framed in **electronic engineering** contexts where sensible: signal processing, registers, buffers, real-time, **comb-filter** / **mono-mixing**, **PSD**-style narratives when applicable.
- **Capstone:** The protocol mentions a final “all-subject” notebook; the user’s **interview** workbook partially fills that role unless they ask for a separate capstone.

---

## 4. Technical constraints (C++ and style)

- **Standard:** **C++20** (concepts, `requires`, `constexpr`, templates, etc., as appropriate to the subject list).
- **Functions passed as values:** Prefer **named function-pointer types** (e.g. `using Fn = double (*)(double);`) instead of relying on `std::function` when staying light on STL.
- **Naming:** Professional / technical (e.g. `SignalBufferManager`, not `MyArray`).
- **Storage:** Without STL containers, use **raw arrays**, **fixed buffers**, **`new`/`delete`** (or stack objects) as appropriate to the exercise level.

---

## 5. HTML / UI rules

- Each workbook is a **single standalone `.html` file** (unless the user asks otherwise).
- If `template.html` exists in the project, prefer aligning with it; otherwise use **clean, professional** styling consistent with existing workbooks.
- **Every exercise** must have a control to **reveal a solution** (e.g. a **button** toggling a hidden block).
- **Solution content:** **Full C++** (or the requested artifact) plus a **short explanation** of why the relevant **C++20 / course** feature fits the problem.

---

## 6. File and folder checklist

| Item | Location |
|------|----------|
| Curriculum list | `cpp-beg-to-adv/course-subjects.txt` |
| Master protocol (detail) | `cpp-beg-to-adv/exercises-instructions.txt` |
| Main workbooks | `cpp-beg-to-adv/workbooks/*.html` |
| Per-subject everyday practice | `cpp-beg-to-adv/exeryday-practice/*.html` |

---

## 7. Quick pre-flight for the assistant

1. Re-read `course-subjects.txt` and note **count** and **order** of subjects.
2. Confirm **forbidden / deferred** topics from that file.
3. Decide **first half vs second half** split (half the list by subject count).
4. For each HTML file: EE context where possible, **reveal solutions**, **C++20**-aligned explanations, **no out-of-scope STL** unless the curriculum explicitly includes it.

---

*Last aligned with the user’s workbook requests and `exercises-instructions.txt` as of the session that created `workbooks/` and `exeryday-practice/`.*
