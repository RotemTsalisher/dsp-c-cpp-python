# Module 05 solutions — FreeRTOS and multitasking

> Reference only — attempt exercises first.

Code tree: `modules/05-freertos-and-multitasking/code/solution/`

## Exercise 1

See `modules/05-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/05-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/05-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/05-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for FreeRTOS and multitasking. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — FreeRTOS and multitasking
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* FreeRTOS and multitasking */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

