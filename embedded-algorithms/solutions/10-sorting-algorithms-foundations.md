# Module 10 solutions — Sorting algorithms: foundations

> Reference only — attempt exercises first.

Code tree: `modules/10-sorting-algorithms-foundations/code/solution/`

## Exercise 1

def insertion_sort(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
    return a

/* embedded_c/mod_10_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Sorting algorithms: foundations with fixed storage only */

## Exercise 2

def insertion_sort(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
    return a

/* embedded_c/mod_10_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Sorting algorithms: foundations with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def insertion_sort(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
    return a

/* embedded_c/mod_10_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Sorting algorithms: foundations with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def insertion_sort(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
    return a

/* embedded_c/mod_10_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Sorting algorithms: foundations with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_10.py`

```
def insertion_sort(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
    return a
```

### File `main.c`

```
/* embedded_c/mod_10_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Sorting algorithms: foundations with fixed storage only */
```

### File `README.md`

```
# Module 10 embedded port

Build with CCS target MSP430G2553.
```

