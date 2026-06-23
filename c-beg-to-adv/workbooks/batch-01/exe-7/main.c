#include <stdio.h>
#include <math.h>

int main() {

    const int SAMPLE_RATE_HZ = 48000;
    const double COMB_DELAY_MS = 100.0;
    const int ADC_BITS = 12;
    const double FULL_SCALE_V = 2.5;

    int delay_in_samples = (COMB_DELAY_MS / 1000.0) * SAMPLE_RATE_HZ;
    int left_channel = 1023, right_channel = 2012;

    double v_right, v_left, denom = pow(2, ADC_BITS) - 1.0;
    v_right = right_channel * FULL_SCALE_V / denom;
    v_left = left_channel * FULL_SCALE_V / denom;

    double headroom_precentage_right = (1 - (v_right / FULL_SCALE_V)) * 100.0;
    double headroom_precentage_left = (1 - (v_left / FULL_SCALE_V)) * 100.0;


    printf("v_right = %5.3f || headroom = %5.3f%%\n", v_right, headroom_precentage_right);
    printf("v_left = %5.3f || headroom = %5.3f%%\n", v_left, headroom_precentage_left);
    return 0;
}