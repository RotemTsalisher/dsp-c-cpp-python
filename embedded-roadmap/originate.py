"""Per-module originated content: theory, labs, exercises, code, solutions."""
from __future__ import annotations

import textwrap
from dataclasses import dataclass, field


@dataclass
class ExerciseSpec:
    prompt: str
    hint: str
    solution: str
    stretch: str = ""


@dataclass
class ModuleOrigin:
    theory: str
    lab_steps: str
    test_procedure: str
    exercises: list[ExerciseSpec] = field(default_factory=list)
    files: dict[str, str] = field(default_factory=dict)  # relative path -> content (starter/)
    solution_files: dict[str, str] = field(default_factory=dict)


def _ex4(title: str, hw: str, core: str, b: str, c: str, assign: str, sol_core: str) -> list[ExerciseSpec]:
    return [
        ExerciseSpec(core, f"Scope: {title} on {hw}.", sol_core),
        ExerciseSpec(b, "Test boundary inputs before optimizing.", sol_core + "\n\nBoundary: document edge case handling in comments."),
        ExerciseSpec(c, "Measure cycles or RAM after correctness passes.", sol_core + "\n\nOptimization: note trade-off vs baseline measurement."),
        ExerciseSpec(assign, "Include a one-page engineering report.", sol_core + "\n\nAssignment: integrate with prior module driver where applicable."),
    ]


MSP430_GPIO_STARTER = textwrap.dedent(
    r"""
    /*
     * starter/main.c — Module GPIO (MSP430G2553)
     * LaunchPad: P1.0 = red LED, P1.3 = S2 button (active low on many G2 boards)
     * TODO: configure P1.0 output, P1.3 input with pull-up, debounce in software
     */
    #include <msp430.h>

    static volatile unsigned int g_button_event;

    static void clock_init(void) {
        WDTCTL = WDTPW | WDTHOLD;
        BCSCTL3 |= LFXT1S_2; /* VLO */
    }

    int main(void) {
        clock_init();
        /* TODO: P1DIR, P1REN, P1OUT, P1IE, P1IES, P1IFG, __enable_interrupt() */
        for (;;) {
            /* TODO: toggle LED when debounced press detected */
        }
    }

    #pragma vector=PORT1_VECTOR
    __interrupt void Port1_ISR(void) {
        /* TODO: minimal ISR — set flag only */
    }
    """
).strip()

MSP430_GPIO_SOLUTION = textwrap.dedent(
    r"""
    #include <msp430.h>

    static volatile unsigned int g_button_event;
    static unsigned int debounce_guard;

    static void clock_init(void) {
        WDTCTL = WDTPW | WDTHOLD;
        BCSCTL3 |= LFXT1S_2;
    }

    static void gpio_init(void) {
        P1DIR |= BIT0;
        P1DIR &= ~BIT3;
        P1REN |= BIT3;
        P1OUT |= BIT3;
        P1IE  |= BIT3;
        P1IES |= BIT3;
        P1IFG &= ~BIT3;
    }

    int main(void) {
        clock_init();
        gpio_init();
        __enable_interrupt();
        for (;;) {
            if (g_button_event) {
                g_button_event = 0;
                P1OUT ^= BIT0;
                debounce_guard = 5000;
                while (debounce_guard--) { /* crude debounce */ }
            }
        }
    }

    #pragma vector=PORT1_VECTOR
    __interrupt void Port1_ISR(void) {
        if (P1IFG & BIT3) {
            g_button_event = 1;
            P1IFG &= ~BIT3;
        }
    }
    """
).strip()


ALGO_TASKS: list[tuple[str, str, str]] = [
    ("Array max/min/mean/count", "def array_stats(v):\n    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])", "O(n), O(1) aux"),
    ("GCD/LCM/safe mod ops", "def gcd(a,b):\n    while b: a,b=b,a%b\n    return abs(a)", "Euclid O(log n)"),
    ("Compare O(n) vs O(n^2) on growing lists", "def dup_count_naive(a):\n    c=0\n    for i in range(len(a)):\n        for j in range(i): c+= a[i]==a[j]\n    return c", "Quadratic vs linear"),
    ("Brute force vs structured search with invariants", "def is_sorted(a):\n    return all(a[i]<=a[i+1] for i in range(len(a)-1))", "O(n) check"),
    ("Static array insert/delete with shift", "def insert_at(a,n,x,i):\n    if n>=len(a): raise ValueError\n    for j in range(n,i,-1): a[j]=a[j-1]\n    a[i]=x\n    return n+1", "O(n) insert"),
    ("C-string length/compare/copy bounded", "def c_strlen(s,maxlen):\n    n=0\n    while n<maxlen and s[n]: n+=1\n    return n", "O(n)"),
    ("Stack/queue on fixed arrays", "class Stack:\n    def __init__(self,cap): self.a=[0]*cap; self.n=0\n    def push(self,x):\n        if self.n>=len(self.a): raise OverflowError\n        self.a[self.n]=x; self.n+=1", "O(1) push"),
    ("Hash table with linear probing (small)", "def h(k,m): return k%m\n# implement probe sequence in solution", "Avg O(1) lookup"),
    ("Linear and binary search", "def binary_search(a,t):\n    lo,hi=0,len(a)-1\n    while lo<=hi:\n        mid=(lo+hi)//2\n        if a[mid]==t: return mid\n        if a[mid]<t: lo=mid+1\n        else: hi=mid-1\n    return -1", "O(log n)"),
    ("Bubble/insertion sort + counters", "def insertion_sort(a):\n    for i in range(1,len(a)):\n        k=a[i]; j=i-1\n        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1\n        a[j+1]=k\n    return a", "O(n^2) worst"),
    ("Merge sort (stable) on small arrays", "def merge_sort(a):\n    if len(a)<2: return a[:]\n    m=len(a)//2\n    L=merge_sort(a[:m]); R=merge_sort(a[m:])\n    out=[]; i=j=0\n    while i<len(L) and j<len(R):\n        if L[i]<=R[j]: out.append(L[i]); i+=1\n        else: out.append(R[j]); j+=1\n    return out+L[i:]+R[j:]", "O(n log n)"),
    ("Fibonacci: recursion vs memo vs tabulation", "def fib_tab(n):\n    if n<2: return n\n    a,b=0,1\n    for _ in range(2,n+1): a,b=b,a+b\n    return b", "O(n) time O(1) space"),
    ("Bit popcount and nibble swap", "def popcount(x):\n    c=0\n    while x: x&=x-1; c+=1\n    return c", "O(bits)"),
    ("Merge sort divide-and-conquer recurrence", "def dc_max(a,lo,hi):\n    if lo==hi: return a[lo]\n    mid=(lo+hi)//2\n    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))", "T(n)=2T(n/2)+O(1)"),
    ("Activity selection greedy", "def activity_sel(start,finish):\n    idx=sorted(range(len(finish)), key=lambda i: finish[i])\n    pick=[]; last=-1\n    for i in idx:\n        if start[i]>=last: pick.append(i); last=finish[i]\n    return pick", "Greedy O(n log n)"),
    ("Coin change DP table", "def coin_change(coins,amount):\n    dp=[10**9]*(amount+1); dp[0]=0\n    for a in range(1,amount+1):\n        for c in coins:\n            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)\n    return dp[amount]", "O(amount*len(coins))"),
    ("BFS on adjacency list", "def bfs(adj,s):\n    seen={s}; q=[s]; order=[]\n    while q:\n        u=q.pop(0); order.append(u)\n        for v in adj.get(u,()):\n            if v not in seen: seen.add(v); q.append(v)\n    return order", "O(V+E)"),
    ("Sliding window max of size k", "def window_max(a,k):\n    if k<1: raise ValueError\n    from collections import deque\n    dq=deque(); out=[]\n    for i,x in enumerate(a):\n        while dq and dq[0]<=i-k: dq.popleft()\n        while dq and a[dq[-1]]<=x: dq.pop()\n        dq.append(i)\n        if i>=k-1: out.append(a[dq[0]])\n    return out", "O(n)"),
    ("Fixed-width helpers + safe add", "def sat_add16(a,b):\n    s=a+b\n    return 32767 if s>32767 else (-32768 if s<-32768 else s)", "O(1)"),
    ("Q15 multiply emulation", "def q15_mul(a,b):\n    return (a*b)>>15", "Fixed-point"),
    ("Running RMS on stream chunks", "def running_rms(chunks):\n    sq=0; n=0\n    for ch in chunks:\n        for x in ch: sq+=x*x; n+=1\n        yield (sq/n)**0.5 if n else 0.0", "O(1) per sample amortized"),
    ("Profile two sort variants; pick for n=16 on MCU", "def sort_pick(a,n):\n    return sorted(a[:n])", "Compare constants"),
    ("Property-based test: reverse twice is identity", "def rev(a):\n    a=list(a); a.reverse(); return a", "Testing discipline"),
    ("Capstone: library API surface", "def lib_version(): return '1.0.0'", "Integration"),
]


def _algo_mod(n: int, title: str) -> ModuleOrigin:
    """Algorithm course: Python POC + MSP430 C pattern per module."""
    task, py_core, complexity = ALGO_TASKS[n - 1] if 1 <= n <= len(ALGO_TASKS) else (
        f"Core algorithm for: {title}.",
        f"def solve(data):\n    raise NotImplementedError",
        "Analyze complexity after implementation.",
    )
    theory = textwrap.dedent(
        f"""
        ### Module focus
        {title}

        ### Problem statement
        {task}

        ### Complexity target
        {complexity}

        ### Pseudocode discipline
        Write pseudocode with named loops, pre/postconditions, and explicit capacity `MAX_N`
        before opening an editor.

        ### Differential testing
        Export vectors from Python (`tools/vector_export.py`) and compare UART-printed C results.
        """
    ).strip()
    lab = textwrap.dedent(
        """
        1. Implement and pytest the Python module in `python_poc/`.
        2. Write embedded C with fixed arrays (`uint16_t buf[MAX_N]`).
        3. Flash MSP430; print results over UART at 9600 baud.
        4. Fill `benchmarks/mod-NN-report.md` with map-file sizes and optional cycle count.
        """
    ).strip()
    tests = textwrap.dedent(
        f"""
        - Python: `pytest python_poc/mod_{n:02d}_*/test_mod_{n:02d}.py -q`
        - C: compare three UART lines to golden file `python_poc/mod_{n:02d}_*/vectors.json`
        """
    ).strip()
    sol_c = textwrap.dedent(
        f"""
        /* embedded_c/mod_{n:02d}_*/main.c — port validated Python behavior */
        #include <stdint.h>
        #define MAX_N 32
        /* Implement {title} with fixed storage only */
        """
    ).strip()
    ex = _ex4(
        title,
        "MSP430G2553",
        f"Python POC: {task}",
        f"Handle empty/max-size inputs for {title}.",
        f"Document {complexity} with a timing table.",
        f"Integrated report + C port for {title}.",
        py_core + "\n\n" + sol_c,
    )
    files = {
        f"starter_mod_{n:02d}.py": textwrap.dedent(
            f'"""Starter — {title}."""\n\n# TODO: {task}\n\ndef solve(*args, **kwargs):\n    raise NotImplementedError\n'
        ).strip()
        + "\n",
        f"test_mod_{n:02d}.py": textwrap.dedent(
            f"""
            import pytest
            from solution_mod_{n:02d} import *

            def test_nominal():
                assert True  # replace with real vectors for {title}
            """
        ).strip()
        + "\n",
    }
    solution_files = {
        f"solution_mod_{n:02d}.py": py_core + "\n",
        "main.c": sol_c + "\n",
        "README.md": f"# Module {n:02d} embedded port\n\nBuild with CCS target MSP430G2553.\n",
    }
    return ModuleOrigin(theory, lab, tests, ex, files, solution_files)


def get_origin(course_slug: str, mod_num: int, title: str) -> ModuleOrigin:
    idx = mod_num - 1
    if course_slug == "embedded-algorithms":
        return _algo_mod(mod_num, title)

    hw_note = {
        "msp430-embedded-c": "MSP430G2553 register access (SLAU144)",
        "msp430-embedded-dsp": "512 B RAM — prefer Q15 and small N",
        "arduino-uno-r4-minima": "Arduino core + optional FSP register peek",
        "esp32-s3-audio-dsp": "ESP-IDF v5.x, `idf.py build flash monitor`",
    }.get(course_slug, "target MCU")

    theory = textwrap.dedent(
        f"""
        ### Deep dive: {title}

        Study the official manual chapter that matches this topic on your board.
        For **{hw_note}**, map each signal to a pin before writing drivers.

        ### Key ideas
        - Configure clocks before baud rates, ADC sample time, or PWM frequency.
        - Keep interrupt service routines short; defer work to the main loop or task.
        - Document assumptions (voltage, sample rate, buffer depth) in module README.

        ### Register / API map (fill while reading docs)
        | Function | Register / API | Your notes |
        |----------|----------------|------------|
        | Enable clock to peripheral | | |
        | Configure pins | | |
        | Start operation | | |
        | Status / flags | | |
        """
    ).strip()

    lab = textwrap.dedent(
        f"""
        1. Clone module branch `module-{mod_num:02d}`.
        2. Open `code/starter/` — complete TODOs for **{title}**.
        3. Build and flash; capture serial log or scope trace.
        4. Compare against `code/solution/` only after tests fail and you have hypotheses.
        5. Write expected vs actual in `lab_checklist.md`.
        """
    ).strip()

    test = textwrap.dedent(
        f"""
        ### Test procedure — {title}
        | Case | Input / action | Expected |
        |------|----------------|----------|
        | T1 nominal | Typical operating point | Stable output, no fault flags |
        | T2 boundary | Min/max allowed value | Saturate or reject safely |
        | T3 fault | Disconnect sensor / noise | Detectable error, no lock-up |
        """
    ).strip()

    starter_main = textwrap.dedent(
        f"""
        /*
         * {course_slug} module {mod_num:02d} — {title}
         * STARTER — complete TODO sections
         */
        #include <stdint.h>

        int main(void) {{
            /* TODO: board init, peripheral setup for {title} */
            for (;;) {{
                /* TODO: application loop */
            }}
            return 0;
        }}
        """
    ).strip()

    solution_main = textwrap.dedent(
        f"""
        /*
         * REFERENCE SOLUTION — {title}
         * Adjust pin defines to your board wiring.
         */
        #include <stdint.h>

        static void board_init(void) {{ /* clock + pins */ }}
        static void module_init(void) {{ /* {title} */ }}

        int main(void) {{
            board_init();
            module_init();
            for (;;) {{ /* demo behavior */ }}
            return 0;
        }}
        """
    ).strip()

    files = {
        "code/starter/README.md": textwrap.dedent(
            f"""
            # Starter — Module {mod_num:02d}: {title}

            ## Build
            - **MSP430:** Import into CCS as `msp430-gcc` project, device MSP430G2553.
            - **Arduino R4:** Open `starter.ino` in Arduino IDE 2.x.
            - **ESP32-S3:** Copy sources into `main/` of a blank ESP-IDF project.

            ## Flash / monitor
            Document the exact command you used (e.g. `idf.py -p COMx flash monitor`).
            """
        ).strip()
        + "\n",
        "code/starter/main.c": starter_main + "\n",
    }

    if course_slug == "arduino-uno-r4-minima":
        files["code/starter/starter.ino"] = textwrap.dedent(
            f"""
            // Module {mod_num:02d}: {title}
            void setup() {{
              Serial.begin(115200);
              // TODO: {title}
            }}
            void loop() {{
              // TODO
            }}
            """
        ).strip() + "\n"

    if course_slug == "esp32-s3-audio-dsp":
        files["code/starter/CMakeLists.txt"] = "cmake_minimum_required(VERSION 3.16)\ninclude($ENV{IDF_PATH}/tools/cmake/project.cmake)\nproject(mod_lab)\n"
        files["code/starter/main/CMakeLists.txt"] = 'idf_component_register(SRCS "main.c" INCLUDE_DIRS ".")\n'
        files["code/starter/main/main.c"] = starter_main.replace("#include <stdint.h>", '#include "stdio.h"\n#include "freertos/FreeRTOS.h"\n#include "freertos/task.h"') + "\n"

    solution_files = {
        "code/solution/README.md": f"Reference wiring for {title}. Diff against starter.\n",
        "code/solution/main.c": solution_main + "\n",
    }

    if course_slug == "msp430-embedded-c" and mod_num == 3:
        files["code/starter/main.c"] = MSP430_GPIO_STARTER + "\n"
        solution_files["code/solution/main.c"] = MSP430_GPIO_SOLUTION + "\n"
        theory += textwrap.dedent(
            """

            ### LaunchPad GPIO specifics
            - `P1DIR` direction, `P1REN` pull resistors, `P1OUT` levels.
            - Active-low button: pull-up enabled, interrupt on high→low edge.
            - Debounce in main loop or timer, not long delays in ISR.
            """
        )

    sol_text = f"See `modules/{mod_num:02d}-*/code/solution/` and embedded snippets in solutions markdown."
    ex = _ex4(
        title,
        course_slug,
        f"Complete starter code for {title}.",
        f"Demonstrate boundary case for {title}.",
        f"Profile {title} (time/RAM/Flash).",
        f"Mini-project integrating {title} with documentation.",
        sol_text,
    )

    return ModuleOrigin(theory, lab, test, ex, files, solution_files)
