#include <stdio.h>
#include <stdlib.h>

#define FS 48000
#define LOG_INFO "Delay in ms: %5.3f | Delay in samples (double) : %5.3f | Delay in samples (int) : %d |\n"

int main() {

    double delay_in_ms = 2.5012;

    double delay_in_samples_double = delay_in_ms * FS;
    int delay_in_samples_int = delay_in_samples_double;

    printf(LOG_INFO, delay_in_ms, delay_in_samples_double, delay_in_samples_int);
    return 0;
}