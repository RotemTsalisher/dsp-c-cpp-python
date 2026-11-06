#include <msp430.h>

static volatile unsigned int g_button_event;
static unsigned int debounce_guard;

static void clock_init(void) {
    WDTCTL = WDTPW | WDTHOLD;
    BCSCTL3 |= LFXT1S_2;
}

static void gpio_init(void) {
    P1DIR |= BIT0;
    P1DIR &= ~BIT3;
    P1REN |= BIT3;
    P1OUT |= BIT3;
    P1IE  |= BIT3;
    P1IES |= BIT3;
    P1IFG &= ~BIT3;
}

int main(void) {
    clock_init();
    gpio_init();
    __enable_interrupt();
    for (;;) {
        if (g_button_event) {
            g_button_event = 0;
            P1OUT ^= BIT0;
            debounce_guard = 5000;
            while (debounce_guard--) { /* crude debounce */ }
        }
    }
}

#pragma vector=PORT1_VECTOR
__interrupt void Port1_ISR(void) {
    if (P1IFG & BIT3) {
        g_button_event = 1;
        P1IFG &= ~BIT3;
    }
}
