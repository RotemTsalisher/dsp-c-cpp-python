# Module 18 solutions — Common algorithmic problem-solving patterns

> Reference only — attempt exercises first.

Code tree: `modules/18-common-algorithmic-problem-solving-patterns/code/solution/`

## Exercise 1

def window_max(a,k):
    if k<1: raise ValueError
    from collections import deque
    dq=deque(); out=[]
    for i,x in enumerate(a):
        while dq and dq[0]<=i-k: dq.popleft()
        while dq and a[dq[-1]]<=x: dq.pop()
        dq.append(i)
        if i>=k-1: out.append(a[dq[0]])
    return out

/* embedded_c/mod_18_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Common algorithmic problem-solving patterns with fixed storage only */

## Exercise 2

def window_max(a,k):
    if k<1: raise ValueError
    from collections import deque
    dq=deque(); out=[]
    for i,x in enumerate(a):
        while dq and dq[0]<=i-k: dq.popleft()
        while dq and a[dq[-1]]<=x: dq.pop()
        dq.append(i)
        if i>=k-1: out.append(a[dq[0]])
    return out

/* embedded_c/mod_18_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Common algorithmic problem-solving patterns with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def window_max(a,k):
    if k<1: raise ValueError
    from collections import deque
    dq=deque(); out=[]
    for i,x in enumerate(a):
        while dq and dq[0]<=i-k: dq.popleft()
        while dq and a[dq[-1]]<=x: dq.pop()
        dq.append(i)
        if i>=k-1: out.append(a[dq[0]])
    return out

/* embedded_c/mod_18_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Common algorithmic problem-solving patterns with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def window_max(a,k):
    if k<1: raise ValueError
    from collections import deque
    dq=deque(); out=[]
    for i,x in enumerate(a):
        while dq and dq[0]<=i-k: dq.popleft()
        while dq and a[dq[-1]]<=x: dq.pop()
        dq.append(i)
        if i>=k-1: out.append(a[dq[0]])
    return out

/* embedded_c/mod_18_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Common algorithmic problem-solving patterns with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_18.py`

```
def window_max(a,k):
    if k<1: raise ValueError
    from collections import deque
    dq=deque(); out=[]
    for i,x in enumerate(a):
        while dq and dq[0]<=i-k: dq.popleft()
        while dq and a[dq[-1]]<=x: dq.pop()
        dq.append(i)
        if i>=k-1: out.append(a[dq[0]])
    return out
```

### File `main.c`

```
/* embedded_c/mod_18_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Common algorithmic problem-solving patterns with fixed storage only */
```

### File `README.md`

```
# Module 18 embedded port

Build with CCS target MSP430G2553.
```

