# Module 21 solutions — Real-time and streaming algorithms

> Reference only — attempt exercises first.

Code tree: `modules/21-real-time-and-streaming-algorithms/code/solution/`

## Exercise 1

def running_rms(chunks):
    sq=0; n=0
    for ch in chunks:
        for x in ch: sq+=x*x; n+=1
        yield (sq/n)**0.5 if n else 0.0

/* embedded_c/mod_21_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Real-time and streaming algorithms with fixed storage only */

## Exercise 2

def running_rms(chunks):
    sq=0; n=0
    for ch in chunks:
        for x in ch: sq+=x*x; n+=1
        yield (sq/n)**0.5 if n else 0.0

/* embedded_c/mod_21_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Real-time and streaming algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def running_rms(chunks):
    sq=0; n=0
    for ch in chunks:
        for x in ch: sq+=x*x; n+=1
        yield (sq/n)**0.5 if n else 0.0

/* embedded_c/mod_21_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Real-time and streaming algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def running_rms(chunks):
    sq=0; n=0
    for ch in chunks:
        for x in ch: sq+=x*x; n+=1
        yield (sq/n)**0.5 if n else 0.0

/* embedded_c/mod_21_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Real-time and streaming algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_21.py`

```
def running_rms(chunks):
    sq=0; n=0
    for ch in chunks:
        for x in ch: sq+=x*x; n+=1
        yield (sq/n)**0.5 if n else 0.0
```

### File `main.c`

```
/* embedded_c/mod_21_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Real-time and streaming algorithms with fixed storage only */
```

### File `README.md`

```
# Module 21 embedded port

Build with CCS target MSP430G2553.
```

