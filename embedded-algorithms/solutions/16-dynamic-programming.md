# Module 16 solutions — Dynamic programming

> Reference only — attempt exercises first.

Code tree: `modules/16-dynamic-programming/code/solution/`

## Exercise 1

def coin_change(coins,amount):
    dp=[10**9]*(amount+1); dp[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
    return dp[amount]

/* embedded_c/mod_16_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Dynamic programming with fixed storage only */

## Exercise 2

def coin_change(coins,amount):
    dp=[10**9]*(amount+1); dp[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
    return dp[amount]

/* embedded_c/mod_16_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Dynamic programming with fixed storage only */

Boundary: document edge case handling in comments.

## Exercise 3

def coin_change(coins,amount):
    dp=[10**9]*(amount+1); dp[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
    return dp[amount]

/* embedded_c/mod_16_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Dynamic programming with fixed storage only */

Optimization: note trade-off vs baseline measurement.

## Exercise 4

def coin_change(coins,amount):
    dp=[10**9]*(amount+1); dp[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
    return dp[amount]

/* embedded_c/mod_16_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Dynamic programming with fixed storage only */

Assignment: integrate with prior module driver where applicable.

### File `solution_mod_16.py`

```
def coin_change(coins,amount):
    dp=[10**9]*(amount+1); dp[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
    return dp[amount]
```

### File `main.c`

```
/* embedded_c/mod_16_*/main.c — port validated Python behavior */
#include <stdint.h>
#define MAX_N 32
/* Implement Dynamic programming with fixed storage only */
```

### File `README.md`

```
# Module 16 embedded port

Build with CCS target MSP430G2553.
```

