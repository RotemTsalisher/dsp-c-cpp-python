# Module 07 solutions — UART, SPI, and I2C

> Reference only — attempt exercises first.

Code tree: `modules/07-uart-spi-and-i2c/code/solution/`

## Exercise 1

See `modules/07-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/07-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/07-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/07-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for UART, SPI, and I2C. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — UART, SPI, and I2C
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* UART, SPI, and I2C */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

