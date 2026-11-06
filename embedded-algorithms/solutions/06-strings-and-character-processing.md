# Module 06 solutions — Strings and character processing

> Reference only — attempt exercises first.

Code tree: `modules/06-strings-and-character-processing/code/solution/`

## Exercise 1

def c_strlen(s,maxlen):
    n=0
    while n<maxlen and s[n]: n+=1
    return n

/* embedded_c/mod_06_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Strings and character processing with fixed storage only */

## Exercise 2

def c_strlen(s,maxlen):
    n=0
    while n<maxlen and s[n]: n+=1
    return n

/* embedded_c/mod_06_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Strings and character processing with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def c_strlen(s,maxlen):
    n=0
    while n<maxlen and s[n]: n+=1
    return n

/* embedded_c/mod_06_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Strings and character processing with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def c_strlen(s,maxlen):
    n=0
    while n<maxlen and s[n]: n+=1
    return n

/* embedded_c/mod_06_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Strings and character processing with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_06.py`

```
def c_strlen(s,maxlen):
    n=0
    while n<maxlen and s[n]: n+=1
    return n
```

### File `main.c`

```
/* embedded_c/mod_06_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Strings and character processing with fixed storage only */
```

### File `README.md`

```
# Module 06 embedded port

Build with CCS target MSP430G2553.
```

