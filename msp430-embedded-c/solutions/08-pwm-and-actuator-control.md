# Module 08 solutions — PWM and actuator control

> Reference only — attempt exercises first.

Code tree: `modules/08-pwm-and-actuator-control/code/solution/`

## Exercise 1

See `modules/08-*/code/solution/` and embedded snippets in solutions markdown.

## Exercise 2

See `modules/08-*/code/solution/` and embedded snippets in solutions markdown.

Boundary: document edge case handling in comments.

## Exercise 3

See `modules/08-*/code/solution/` and embedded snippets in solutions markdown.

Optimization: note trade-off vs baseline measurement.

## Exercise 4

See `modules/08-*/code/solution/` and embedded snippets in solutions markdown.

Assignment: integrate with prior module driver where applicable.

### File `code/solution/README.md`

```
Reference wiring for PWM and actuator control. Diff against starter.
```

### File `code/solution/main.c`

```
/*
 * REFERENCE SOLUTION — PWM and actuator control
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* PWM and actuator control */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
```

