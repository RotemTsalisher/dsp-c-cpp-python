# Module 06 solutions — ADC, DAC, and analog interfacing

> Reference only — attempt exercises first.

Code tree: `modules/06-adc-dac-and-analog-interfacing/code/solution/`

## Exercise 1

See `modules/06-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/06-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/06-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/06-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for ADC, DAC, and analog interfacing. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — ADC, DAC, and analog interfacing
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* ADC, DAC, and analog interfacing */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

