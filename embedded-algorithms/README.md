# Algorithm Development for Embedded Systems (C/C++)

        **Hardware:** MSP-EXP430G2 LaunchPad (MSP430G2553); host PC for Python/C++ exercises
        **Prerequisites:** Second-year EE coding level; no prior formal algorithms or Big-O course.
        **Toolchain:** Python 3 for POC; MSP430 C (CCS/gcc); host C++20 for STL modules.

        ## Open the course
        - **Browser:** double-click `index.html` (progress saves in localStorage).
        - **Git-friendly:** read `modules/` lessons, work in `exercises/`, check `solutions/` only after attempting.

        ## Constraints
        512 B RAM, 16 KB Flash, no FPU. Every major exercise follows: problem → design → Python POC → complexity analysis → embedded C → differential validation → measurement → engineering report.

        ## Module map
        | # | Module | Folder |
        |---|--------|--------|
        | 01 | Introduction to algorithm development | `modules/01-introduction-to-algorithm-development/` |
| 02 | Mathematical foundations for algorithms | `modules/02-mathematical-foundations-for-algorithms/` |
| 03 | Understanding algorithm complexity | `modules/03-understanding-algorithm-complexity/` |
| 04 | Problem-solving methods and correctness | `modules/04-problem-solving-methods-and-correctness/` |
| 05 | Arrays and memory representation | `modules/05-arrays-and-memory-representation/` |
| 06 | Strings and character processing | `modules/06-strings-and-character-processing/` |
| 07 | Pointers, linked lists, stacks, and queues | `modules/07-pointers-linked-lists-stacks-and-queues/` |
| 08 | Hash tables, heaps, and priority queues | `modules/08-hash-tables-heaps-and-priority-queues/` |
| 09 | Searching algorithms | `modules/09-searching-algorithms/` |
| 10 | Sorting algorithms: foundations | `modules/10-sorting-algorithms-foundations/` |
| 11 | Advanced sorting algorithms | `modules/11-advanced-sorting-algorithms/` |
| 12 | Recursion and backtracking | `modules/12-recursion-and-backtracking/` |
| 13 | Bit manipulation and bitwise algorithms | `modules/13-bit-manipulation-and-bitwise-algorithms/` |
| 14 | Divide and conquer | `modules/14-divide-and-conquer/` |
| 15 | Greedy algorithms | `modules/15-greedy-algorithms/` |
| 16 | Dynamic programming | `modules/16-dynamic-programming/` |
| 17 | Graph representations and algorithms | `modules/17-graph-representations-and-algorithms/` |
| 18 | Common algorithmic problem-solving patterns | `modules/18-common-algorithmic-problem-solving-patterns/` |
| 19 | Embedded C for algorithm developers | `modules/19-embedded-c-for-algorithm-developers/` |
| 20 | Fixed-point arithmetic and numerical algorithms | `modules/20-fixed-point-arithmetic-and-numerical-algorithms/` |
| 21 | Real-time and streaming algorithms | `modules/21-real-time-and-streaming-algorithms/` |
| 22 | Optimization for embedded targets | `modules/22-optimization-for-embedded-targets/` |
| 23 | Testing, verification, and engineering quality | `modules/23-testing-verification-and-engineering-quality/` |
| 24 | Final engineering project: embedded algorithm library | `modules/24-final-engineering-project-embedded-algorithm-library/` |

        ## Final project options
        - Reusable MSP430 algorithm library with benchmark and test reports

        ## Regenerate browser bundle
        ```powershell
        cd embedded-roadmap
        python generate_courses.py
        ```

        ## References
        See `references/README.md` for datasheets and official manuals.
