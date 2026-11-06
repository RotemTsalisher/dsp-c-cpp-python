/*
 * starter/main.c — Module GPIO (MSP430G2553)
 * LaunchPad: P1.0 = red LED, P1.3 = S2 button (active low on many G2 boards)
 * TODO: configure P1.0 output, P1.3 input with pull-up, debounce in software
 */
#include <msp430.h>

static volatile unsigned int g_button_event;

static void clock_init(void) {
    WDTCTL = WDTPW | WDTHOLD;
    BCSCTL3 |= LFXT1S_2; /* VLO */
}

int main(void) {
    clock_init();
    /* TODO: P1DIR, P1REN, P1OUT, P1IE, P1IES, P1IFG, __enable_interrupt() */
    for (;;) {
        /* TODO: toggle LED when debounced press detected */
    }
}

#pragma vector=PORT1_VECTOR
__interrupt void Port1_ISR(void) {
    /* TODO: minimal ISR — set flag only */
}
