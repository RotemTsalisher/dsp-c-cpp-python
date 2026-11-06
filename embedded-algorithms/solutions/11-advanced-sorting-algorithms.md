# Module 11 solutions — Advanced sorting algorithms

> Reference only — attempt exercises first.

Code tree: `modules/11-advanced-sorting-algorithms/code/solution/`

## Exercise 1

def merge_sort(a):
    if len(a)<2: return a[:]
    m=len(a)//2
    L=merge_sort(a[:m]); R=merge_sort(a[m:])
    out=[]; i=j=0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    return out+L[i:]+R[j:]

/* embedded_c/mod_11_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Advanced sorting algorithms with fixed storage only */

## Exercise 2

def merge_sort(a):
    if len(a)<2: return a[:]
    m=len(a)//2
    L=merge_sort(a[:m]); R=merge_sort(a[m:])
    out=[]; i=j=0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    return out+L[i:]+R[j:]

/* embedded_c/mod_11_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Advanced sorting algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def merge_sort(a):
    if len(a)<2: return a[:]
    m=len(a)//2
    L=merge_sort(a[:m]); R=merge_sort(a[m:])
    out=[]; i=j=0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    return out+L[i:]+R[j:]

/* embedded_c/mod_11_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Advanced sorting algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def merge_sort(a):
    if len(a)<2: return a[:]
    m=len(a)//2
    L=merge_sort(a[:m]); R=merge_sort(a[m:])
    out=[]; i=j=0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    return out+L[i:]+R[j:]

/* embedded_c/mod_11_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Advanced sorting algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_11.py`

```
def merge_sort(a):
    if len(a)<2: return a[:]
    m=len(a)//2
    L=merge_sort(a[:m]); R=merge_sort(a[m:])
    out=[]; i=j=0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    return out+L[i:]+R[j:]
```

### File `main.c`

```
/* embedded_c/mod_11_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Advanced sorting algorithms with fixed storage only */
```

### File `README.md`

```
# Module 11 embedded port

Build with CCS target MSP430G2553.
```

