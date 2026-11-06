# Module 13 solutions — Final embedded DSP project

> Reference only — attempt exercises first.

Code tree: `modules/13-final-embedded-dsp-project/code/solution/`

## Exercise 1

See `modules/13-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/13-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/13-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/13-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for Final embedded DSP project. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — Final embedded DSP project
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* Final embedded DSP project */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

