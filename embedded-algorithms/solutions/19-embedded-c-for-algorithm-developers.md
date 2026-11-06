# Module 19 solutions — Embedded C for algorithm developers

> Reference only — attempt exercises first.

Code tree: `modules/19-embedded-c-for-algorithm-developers/code/solution/`

## Exercise 1

def sat_add16(a,b):
    s=a+b
    return 32767 if s>32767 else (-32768 if s<-32768 else s)

/* embedded_c/mod_19_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Embedded C for algorithm developers with fixed storage only */

## Exercise 2

def sat_add16(a,b):
    s=a+b
    return 32767 if s>32767 else (-32768 if s<-32768 else s)

/* embedded_c/mod_19_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Embedded C for algorithm developers with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def sat_add16(a,b):
    s=a+b
    return 32767 if s>32767 else (-32768 if s<-32768 else s)

/* embedded_c/mod_19_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Embedded C for algorithm developers with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def sat_add16(a,b):
    s=a+b
    return 32767 if s>32767 else (-32768 if s<-32768 else s)

/* embedded_c/mod_19_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Embedded C for algorithm developers with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_19.py`

```
def sat_add16(a,b):
    s=a+b
    return 32767 if s>32767 else (-32768 if s<-32768 else s)
```

### File `main.c`

```
/* embedded_c/mod_19_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Embedded C for algorithm developers with fixed storage only */
```

### File `README.md`

```
# Module 19 embedded port

Build with CCS target MSP430G2553.
```

