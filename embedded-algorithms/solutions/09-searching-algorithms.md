# Module 09 solutions — Searching algorithms

> Reference only — attempt exercises first.

Code tree: `modules/09-searching-algorithms/code/solution/`

## Exercise 1

def binary_search(a,t):
    lo,hi=0,len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]==t: return mid
        if a[mid]<t: lo=mid+1
        else: hi=mid-1
    return -1

/* embedded_c/mod_09_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Searching algorithms with fixed storage only */

## Exercise 2

def binary_search(a,t):
    lo,hi=0,len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]==t: return mid
        if a[mid]<t: lo=mid+1
        else: hi=mid-1
    return -1

/* embedded_c/mod_09_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Searching algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def binary_search(a,t):
    lo,hi=0,len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]==t: return mid
        if a[mid]<t: lo=mid+1
        else: hi=mid-1
    return -1

/* embedded_c/mod_09_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Searching algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def binary_search(a,t):
    lo,hi=0,len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]==t: return mid
        if a[mid]<t: lo=mid+1
        else: hi=mid-1
    return -1

/* embedded_c/mod_09_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Searching algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_09.py`

```
def binary_search(a,t):
    lo,hi=0,len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]==t: return mid
        if a[mid]<t: lo=mid+1
        else: hi=mid-1
    return -1
```

### File `main.c`

```
/* embedded_c/mod_09_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Searching algorithms with fixed storage only */
```

### File `README.md`

```
# Module 09 embedded port

Build with CCS target MSP430G2553.
```

