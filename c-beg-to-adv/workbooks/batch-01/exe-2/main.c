#include <stdio.h>
#include <math.h>

int main() {

    int count_left = 2047, count_right = 1024, resolution_bits = 12;
    char channel_tag;
    double volts, full_scale_volts = 2.5, denom = pow(2,resolution_bits) - 1.0;

    printf("=== AFE dual-channel snapshot ===\n");

    channel_tag = 'R';
    volts = (double)count_right * full_scale_volts / (denom);
    printf("CH %c | counts=%04d | V = %7.4f\n", channel_tag, count_right, volts);

    channel_tag = 'L';
    volts = (double)count_left * full_scale_volts / (denom);
    printf("CH %c | counts=%04d | V = %7.4f\n", channel_tag, count_left, volts);
    return 0;
}