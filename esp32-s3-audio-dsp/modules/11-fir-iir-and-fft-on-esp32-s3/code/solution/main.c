/*
 * REFERENCE SOLUTION — FIR, IIR, and FFT on ESP32-S3
 * Adjust pin defines to your board wiring.
 */
#include <stdint.h>

static void board_init(void) { /* clock + pins */ }
static void module_init(void) { /* FIR, IIR, and FFT on ESP32-S3 */ }

int main(void) {
    board_init();
    module_init();
    for (;;) { /* demo behavior */ }
    return 0;
}
