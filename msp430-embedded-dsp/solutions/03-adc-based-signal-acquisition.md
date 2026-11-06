# Module 03 solutions — ADC-based signal acquisition

> Reference only — attempt exercises first.

Code tree: `modules/03-adc-based-signal-acquisition/code/solution/`

## Exercise 1

See `modules/03-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/03-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/03-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/03-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for ADC-based signal acquisition. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — ADC-based signal acquisition
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* ADC-based signal acquisition */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

