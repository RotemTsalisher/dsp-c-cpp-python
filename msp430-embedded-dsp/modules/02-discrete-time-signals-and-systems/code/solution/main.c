/*
 * REFERENCE SOLUTION — Discrete-time signals and systems
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* Discrete-time signals and systems */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
