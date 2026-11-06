# Module 07 solutions — Pointers, linked lists, stacks, and queues

> Reference only — attempt exercises first.

Code tree: `modules/07-pointers-linked-lists-stacks-and-queues/code/solution/`

## Exercise 1

class Stack:
    def __init__(self,cap): self.a=[0]*cap; self.n=0
    def push(self,x):
        if self.n>=len(self.a): raise OverflowError
        self.a[self.n]=x; self.n+=1

/* embedded_c/mod_07_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Pointers, linked lists, stacks, and queues with fixed storage only */

## Exercise 2

class Stack:
    def __init__(self,cap): self.a=[0]*cap; self.n=0
    def push(self,x):
        if self.n>=len(self.a): raise OverflowError
        self.a[self.n]=x; self.n+=1

/* embedded_c/mod_07_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Pointers, linked lists, stacks, and queues with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

class Stack:
    def __init__(self,cap): self.a=[0]*cap; self.n=0
    def push(self,x):
        if self.n>=len(self.a): raise OverflowError
        self.a[self.n]=x; self.n+=1

/* embedded_c/mod_07_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Pointers, linked lists, stacks, and queues with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

class Stack:
    def __init__(self,cap): self.a=[0]*cap; self.n=0
    def push(self,x):
        if self.n>=len(self.a): raise OverflowError
        self.a[self.n]=x; self.n+=1

/* embedded_c/mod_07_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Pointers, linked lists, stacks, and queues with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_07.py`

```
class Stack:
    def __init__(self,cap): self.a=[0]*cap; self.n=0
    def push(self,x):
        if self.n>=len(self.a): raise OverflowError
        self.a[self.n]=x; self.n+=1
```

### File `main.c`

```
/* embedded_c/mod_07_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Pointers, linked lists, stacks, and queues with fixed storage only */
```

### File `README.md`

```
# Module 07 embedded port

Build with CCS target MSP430G2553.
```

