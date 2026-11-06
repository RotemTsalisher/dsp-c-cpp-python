# Module 05 solutions — Arrays and memory representation

> Reference only — attempt exercises first.

Code tree: `modules/05-arrays-and-memory-representation/code/solution/`

## Exercise 1

def insert_at(a,n,x,i):
    if n>=len(a): raise ValueError
    for j in range(n,i,-1): a[j]=a[j-1]
    a[i]=x
    return n+1

/* embedded_c/mod_05_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Arrays and memory representation with fixed storage only */

## Exercise 2

def insert_at(a,n,x,i):
    if n>=len(a): raise ValueError
    for j in range(n,i,-1): a[j]=a[j-1]
    a[i]=x
    return n+1

/* embedded_c/mod_05_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Arrays and memory representation with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def insert_at(a,n,x,i):
    if n>=len(a): raise ValueError
    for j in range(n,i,-1): a[j]=a[j-1]
    a[i]=x
    return n+1

/* embedded_c/mod_05_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Arrays and memory representation with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def insert_at(a,n,x,i):
    if n>=len(a): raise ValueError
    for j in range(n,i,-1): a[j]=a[j-1]
    a[i]=x
    return n+1

/* embedded_c/mod_05_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Arrays and memory representation with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_05.py`

```
def insert_at(a,n,x,i):
    if n>=len(a): raise ValueError
    for j in range(n,i,-1): a[j]=a[j-1]
    a[i]=x
    return n+1
```

### File `main.c`

```
/* embedded_c/mod_05_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Arrays and memory representation with fixed storage only */
```

### File `README.md`

```
# Module 05 embedded port

Build with CCS target MSP430G2553.
```

