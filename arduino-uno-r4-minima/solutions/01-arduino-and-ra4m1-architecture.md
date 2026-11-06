# Module 01 solutions — Arduino and RA4M1 architecture

> Reference only — attempt exercises first.

Code tree: `modules/01-arduino-and-ra4m1-architecture/code/solution/`

## Exercise 1

See `modules/01-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/01-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/01-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/01-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for Arduino and RA4M1 architecture. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — Arduino and RA4M1 architecture
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* Arduino and RA4M1 architecture */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

