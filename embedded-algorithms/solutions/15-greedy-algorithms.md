# Module 15 solutions — Greedy algorithms

> Reference only — attempt exercises first.

Code tree: `modules/15-greedy-algorithms/code/solution/`

## Exercise 1

def activity_sel(start,finish):
    idx=sorted(range(len(finish)), key=lambda i: finish[i])
    pick=[]; last=-1
    for i in idx:
        if start[i]>=last: pick.append(i); last=finish[i]
    return pick

/* embedded_c/mod_15_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Greedy algorithms with fixed storage only */

## Exercise 2

def activity_sel(start,finish):
    idx=sorted(range(len(finish)), key=lambda i: finish[i])
    pick=[]; last=-1
    for i in idx:
        if start[i]>=last: pick.append(i); last=finish[i]
    return pick

/* embedded_c/mod_15_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Greedy algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def activity_sel(start,finish):
    idx=sorted(range(len(finish)), key=lambda i: finish[i])
    pick=[]; last=-1
    for i in idx:
        if start[i]>=last: pick.append(i); last=finish[i]
    return pick

/* embedded_c/mod_15_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Greedy algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def activity_sel(start,finish):
    idx=sorted(range(len(finish)), key=lambda i: finish[i])
    pick=[]; last=-1
    for i in idx:
        if start[i]>=last: pick.append(i); last=finish[i]
    return pick

/* embedded_c/mod_15_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Greedy algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_15.py`

```
def activity_sel(start,finish):
    idx=sorted(range(len(finish)), key=lambda i: finish[i])
    pick=[]; last=-1
    for i in idx:
        if start[i]>=last: pick.append(i); last=finish[i]
    return pick
```

### File `main.c`

```
/* embedded_c/mod_15_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Greedy algorithms with fixed storage only */
```

### File `README.md`

```
# Module 15 embedded port

Build with CCS target MSP430G2553.
```

