# Module 03 solutions — Understanding algorithm complexity

> Reference only — attempt exercises first.

Code tree: `modules/03-understanding-algorithm-complexity/code/solution/`

## Exercise 1

def dup_count_naive(a):
    c=0
    for i in range(len(a)):
        for j in range(i): c+= a[i]==a[j]
    return c

/* embedded_c/mod_03_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Understanding algorithm complexity with fixed storage only */

## Exercise 2

def dup_count_naive(a):
    c=0
    for i in range(len(a)):
        for j in range(i): c+= a[i]==a[j]
    return c

/* embedded_c/mod_03_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Understanding algorithm complexity with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def dup_count_naive(a):
    c=0
    for i in range(len(a)):
        for j in range(i): c+= a[i]==a[j]
    return c

/* embedded_c/mod_03_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Understanding algorithm complexity with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def dup_count_naive(a):
    c=0
    for i in range(len(a)):
        for j in range(i): c+= a[i]==a[j]
    return c

/* embedded_c/mod_03_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Understanding algorithm complexity with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_03.py`

```
def dup_count_naive(a):
    c=0
    for i in range(len(a)):
        for j in range(i): c+= a[i]==a[j]
    return c
```

### File `main.c`

```
/* embedded_c/mod_03_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Understanding algorithm complexity with fixed storage only */
```

### File `README.md`

```
# Module 03 embedded port

Build with CCS target MSP430G2553.
```

