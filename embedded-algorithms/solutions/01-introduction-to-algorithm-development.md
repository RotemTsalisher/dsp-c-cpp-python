# Module 01 solutions — Introduction to algorithm development

> Reference only — attempt exercises first.

Code tree: `modules/01-introduction-to-algorithm-development/code/solution/`

## Exercise 1

def array_stats(v):
    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])

/* embedded_c/mod_01_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Introduction to algorithm development with fixed storage only */

## Exercise 2

def array_stats(v):
    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])

/* embedded_c/mod_01_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Introduction to algorithm development with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def array_stats(v):
    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])

/* embedded_c/mod_01_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Introduction to algorithm development with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def array_stats(v):
    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])

/* embedded_c/mod_01_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Introduction to algorithm development with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_01.py`

```
def array_stats(v):
    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])
```

### File `main.c`

```
/* embedded_c/mod_01_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Introduction to algorithm development with fixed storage only */
```

### File `README.md`

```
# Module 01 embedded port

Build with CCS target MSP430G2553.
```

