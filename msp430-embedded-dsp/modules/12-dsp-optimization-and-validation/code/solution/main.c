/*
 * REFERENCE SOLUTION — DSP optimization and validation
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* DSP optimization and validation */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
