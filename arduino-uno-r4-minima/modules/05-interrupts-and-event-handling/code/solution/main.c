/*
 * REFERENCE SOLUTION — Interrupts and event handling
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* Interrupts and event handling */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
