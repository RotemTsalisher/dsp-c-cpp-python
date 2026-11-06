# Module 02 solutions — Mathematical foundations for algorithms

> Reference only — attempt exercises first.

Code tree: `modules/02-mathematical-foundations-for-algorithms/code/solution/`

## Exercise 1

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

/* embedded_c/mod_02_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Mathematical foundations for algorithms with fixed storage only */

## Exercise 2

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

/* embedded_c/mod_02_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Mathematical foundations for algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

/* embedded_c/mod_02_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Mathematical foundations for algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

/* embedded_c/mod_02_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Mathematical foundations for algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_02.py`

```
def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)
```

### File `main.c`

```
/* embedded_c/mod_02_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Mathematical foundations for algorithms with fixed storage only */
```

### File `README.md`

```
# Module 02 embedded port

Build with CCS target MSP430G2553.
```

