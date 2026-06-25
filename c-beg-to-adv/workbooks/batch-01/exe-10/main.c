#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define BIT_DEPTH_ADC 12
#define ABS_THRESHOLD(val , thresh) ((val >= 0.98 * thresh) || (val <= (-(0.98 * thresh))))

double counts_to_volts(int counts, int bits, double full_scale_v);
double mono_mix(double left, double right);
int is_clipping(double sample, double full_scale_v);
static void print_afe_row(char tag, int counts, double volts, int clip);

int main(void)
{
    int const bits = 12;
    double const fs_v = 2.5;
    int const counts_l = 4095;
    int const counts_r = 4090;

    double const v_l = counts_to_volts(counts_l, bits, fs_v);
    double const v_r = counts_to_volts(counts_r, bits, fs_v);
    double const mono = mono_mix(v_l, v_r);

    printf("=== AFE mono-mix clip guard ===\n");
    print_afe_row('L', counts_l, v_l, is_clipping(v_l, fs_v));
    print_afe_row('R', counts_r, v_r, is_clipping(v_r, fs_v));
    printf("MONO mix: %7.4f V | clip=%s\n",
           mono, is_clipping(mono, fs_v) ? "YES" : "no");
    return 0;
}

double counts_to_volts(int counts, int bits, double full_scale_v) {
    double res = counts * full_scale_v / (pow(2,BIT_DEPTH_ADC) - 1.0);
    return res;
};

double mono_mix(double left, double right) {
    return 0.5 * (left + right);
};

int is_clipping(double sample, double full_scale_v) {
    return ABS_THRESHOLD(sample , full_scale_v);
};

static void print_afe_row(char tag, int counts, double volts, int clip)
{
    printf("CH %c | counts=%04d | V=%7.4f | clip=%s\n",
           tag, counts, volts, clip ? "YES" : "no");
}