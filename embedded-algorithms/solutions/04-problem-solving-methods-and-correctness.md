# Module 04 solutions — Problem-solving methods and correctness

> Reference only — attempt exercises first.

Code tree: `modules/04-problem-solving-methods-and-correctness/code/solution/`

## Exercise 1

def is_sorted(a):
    return all(a[i]<=a[i+1] for i in range(len(a)-1))

/* embedded_c/mod_04_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Problem-solving methods and correctness with fixed storage only */

## Exercise 2

def is_sorted(a):
    return all(a[i]<=a[i+1] for i in range(len(a)-1))

/* embedded_c/mod_04_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Problem-solving methods and correctness with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def is_sorted(a):
    return all(a[i]<=a[i+1] for i in range(len(a)-1))

/* embedded_c/mod_04_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Problem-solving methods and correctness with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def is_sorted(a):
    return all(a[i]<=a[i+1] for i in range(len(a)-1))

/* embedded_c/mod_04_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Problem-solving methods and correctness with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_04.py`

```
def is_sorted(a):
    return all(a[i]<=a[i+1] for i in range(len(a)-1))
```

### File `main.c`

```
/* embedded_c/mod_04_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Problem-solving methods and correctness with fixed storage only */
```

### File `README.md`

```
# Module 04 embedded port

Build with CCS target MSP430G2553.
```

