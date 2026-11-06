/*
 * REFERENCE SOLUTION — ARM Cortex-M4 and low-level programming
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* ARM Cortex-M4 and low-level programming */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
