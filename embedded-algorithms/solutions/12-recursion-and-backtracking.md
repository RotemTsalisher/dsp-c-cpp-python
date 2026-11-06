# Module 12 solutions — Recursion and backtracking

> Reference only — attempt exercises first.

Code tree: `modules/12-recursion-and-backtracking/code/solution/`

## Exercise 1

def fib_tab(n):
    if n<2: return n
    a,b=0,1
    for _ in range(2,n+1): a,b=b,a+b
    return b

/* embedded_c/mod_12_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Recursion and backtracking with fixed storage only */

## Exercise 2

def fib_tab(n):
    if n<2: return n
    a,b=0,1
    for _ in range(2,n+1): a,b=b,a+b
    return b

/* embedded_c/mod_12_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Recursion and backtracking with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def fib_tab(n):
    if n<2: return n
    a,b=0,1
    for _ in range(2,n+1): a,b=b,a+b
    return b

/* embedded_c/mod_12_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Recursion and backtracking with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def fib_tab(n):
    if n<2: return n
    a,b=0,1
    for _ in range(2,n+1): a,b=b,a+b
    return b

/* embedded_c/mod_12_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Recursion and backtracking with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_12.py`

```
def fib_tab(n):
    if n<2: return n
    a,b=0,1
    for _ in range(2,n+1): a,b=b,a+b
    return b
```

### File `main.c`

```
/* embedded_c/mod_12_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Recursion and backtracking with fixed storage only */
```

### File `README.md`

```
# Module 12 embedded port

Build with CCS target MSP430G2553.
```

