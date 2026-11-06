# Module 09 solutions — UART communication

> Reference only — attempt exercises first.

Code tree: `modules/09-uart-communication/code/solution/`

## Exercise 1

See `modules/09-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/09-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/09-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/09-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for UART communication. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — UART communication
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* UART communication */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

