# Module 13 solutions — Bit manipulation and bitwise algorithms

> Reference only — attempt exercises first.

Code tree: `modules/13-bit-manipulation-and-bitwise-algorithms/code/solution/`

## Exercise 1

def popcount(x):
    c=0
    while x: x&=x-1; c+=1
    return c

/* embedded_c/mod_13_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Bit manipulation and bitwise algorithms with fixed storage only */

## Exercise 2

def popcount(x):
    c=0
    while x: x&=x-1; c+=1
    return c

/* embedded_c/mod_13_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Bit manipulation and bitwise algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def popcount(x):
    c=0
    while x: x&=x-1; c+=1
    return c

/* embedded_c/mod_13_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Bit manipulation and bitwise algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def popcount(x):
    c=0
    while x: x&=x-1; c+=1
    return c

/* embedded_c/mod_13_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Bit manipulation and bitwise algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_13.py`

```
def popcount(x):
    c=0
    while x: x&=x-1; c+=1
    return c
```

### File `main.c`

```
/* embedded_c/mod_13_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Bit manipulation and bitwise algorithms with fixed storage only */
```

### File `README.md`

```
# Module 13 embedded port

Build with CCS target MSP430G2553.
```

