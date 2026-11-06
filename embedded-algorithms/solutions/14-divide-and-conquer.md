# Module 14 solutions — Divide and conquer

> Reference only — attempt exercises first.

Code tree: `modules/14-divide-and-conquer/code/solution/`

## Exercise 1

def dc_max(a,lo,hi):
    if lo==hi: return a[lo]
    mid=(lo+hi)//2
    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))

/* embedded_c/mod_14_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Divide and conquer with fixed storage only */

## Exercise 2

def dc_max(a,lo,hi):
    if lo==hi: return a[lo]
    mid=(lo+hi)//2
    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))

/* embedded_c/mod_14_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Divide and conquer with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def dc_max(a,lo,hi):
    if lo==hi: return a[lo]
    mid=(lo+hi)//2
    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))

/* embedded_c/mod_14_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Divide and conquer with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def dc_max(a,lo,hi):
    if lo==hi: return a[lo]
    mid=(lo+hi)//2
    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))

/* embedded_c/mod_14_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Divide and conquer with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_14.py`

```
def dc_max(a,lo,hi):
    if lo==hi: return a[lo]
    mid=(lo+hi)//2
    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))
```

### File `main.c`

```
/* embedded_c/mod_14_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Divide and conquer with fixed storage only */
```

### File `README.md`

```
# Module 14 embedded port

Build with CCS target MSP430G2553.
```

