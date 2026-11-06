# Module 22 solutions — Optimization for embedded targets

> Reference only — attempt exercises first.

Code tree: `modules/22-optimization-for-embedded-targets/code/solution/`

## Exercise 1

def sort_pick(a,n):
    return sorted(a[:n])

/* embedded_c/mod_22_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Optimization for embedded targets with fixed storage only */

## Exercise 2

def sort_pick(a,n):
    return sorted(a[:n])

/* embedded_c/mod_22_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Optimization for embedded targets with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def sort_pick(a,n):
    return sorted(a[:n])

/* embedded_c/mod_22_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Optimization for embedded targets with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def sort_pick(a,n):
    return sorted(a[:n])

/* embedded_c/mod_22_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Optimization for embedded targets with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_22.py`

```
def sort_pick(a,n):
    return sorted(a[:n])
```

### File `main.c`

```
/* embedded_c/mod_22_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Optimization for embedded targets with fixed storage only */
```

### File `README.md`

```
# Module 22 embedded port

Build with CCS target MSP430G2553.
```

