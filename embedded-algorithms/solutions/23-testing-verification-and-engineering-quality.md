# Module 23 solutions — Testing, verification, and engineering quality

> Reference only — attempt exercises first.

Code tree: `modules/23-testing-verification-and-engineering-quality/code/solution/`

## Exercise 1

def rev(a):
    a=list(a); a.reverse(); return a

/* embedded_c/mod_23_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Testing, verification, and engineering quality with fixed storage only */

## Exercise 2

def rev(a):
    a=list(a); a.reverse(); return a

/* embedded_c/mod_23_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Testing, verification, and engineering quality with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def rev(a):
    a=list(a); a.reverse(); return a

/* embedded_c/mod_23_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Testing, verification, and engineering quality with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def rev(a):
    a=list(a); a.reverse(); return a

/* embedded_c/mod_23_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Testing, verification, and engineering quality with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_23.py`

```
def rev(a):
    a=list(a); a.reverse(); return a
```

### File `main.c`

```
/* embedded_c/mod_23_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Testing, verification, and engineering quality with fixed storage only */
```

### File `README.md`

```
# Module 23 embedded port

Build with CCS target MSP430G2553.
```

