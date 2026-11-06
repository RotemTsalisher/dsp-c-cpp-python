# Module 17 solutions — Graph representations and algorithms

> Reference only — attempt exercises first.

Code tree: `modules/17-graph-representations-and-algorithms/code/solution/`

## Exercise 1

def bfs(adj,s):
    seen={s}; q=[s]; order=[]
    while q:
        u=q.pop(0); order.append(u)
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); q.append(v)
    return order

/* embedded_c/mod_17_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Graph representations and algorithms with fixed storage only */

## Exercise 2

def bfs(adj,s):
    seen={s}; q=[s]; order=[]
    while q:
        u=q.pop(0); order.append(u)
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); q.append(v)
    return order

/* embedded_c/mod_17_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Graph representations and algorithms with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def bfs(adj,s):
    seen={s}; q=[s]; order=[]
    while q:
        u=q.pop(0); order.append(u)
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); q.append(v)
    return order

/* embedded_c/mod_17_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Graph representations and algorithms with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def bfs(adj,s):
    seen={s}; q=[s]; order=[]
    while q:
        u=q.pop(0); order.append(u)
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); q.append(v)
    return order

/* embedded_c/mod_17_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Graph representations and algorithms with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_17.py`

```
def bfs(adj,s):
    seen={s}; q=[s]; order=[]
    while q:
        u=q.pop(0); order.append(u)
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); q.append(v)
    return order
```

### File `main.c`

```
/* embedded_c/mod_17_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Graph representations and algorithms with fixed storage only */
```

### File `README.md`

```
# Module 17 embedded port

Build with CCS target MSP430G2553.
```

