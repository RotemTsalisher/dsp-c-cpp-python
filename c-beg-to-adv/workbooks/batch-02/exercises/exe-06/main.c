#include <stdio.h>
#include <stdlib.h>

#define MICRO_SCALER 1000000.0
int main() {

    short raw = -8192;
    double vref = 3.3;
    int full_scale = 32767;

    double volts = (double)raw * (vref / (double)full_scale);
    long uv = volts * MICRO_SCALER;

    printf("volts = %5.3lf || uv = %ld || \n", volts, uv);
    return 0;
}