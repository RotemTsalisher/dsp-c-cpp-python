#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define OPERATOR_NAME_LEN 50
#define REF_PSD_LEN       5
#define ADC_BITS          12
#define FULL_SCALE_V      2.5

double counts_to_volts(int counts, double fsv, int bit_depth);
double mono_mix(double left, double right);
double headroom_pct(double volts, double fsv);
void draw_psd_strip(const double *psd, int size);

static char operator_name[OPERATOR_NAME_LEN];
static double ref_psd[REF_PSD_LEN];

int main() {

    const int adc_bits = ADC_BITS; 
    int left_count, right_count;
    const double full_scale_v = FULL_SCALE_V;
    double left_volts, right_volts, mono_;

    printf("Enter right counts : ");
    scanf("%d", &right_count);

    printf("Enter left counts : ");
    scanf("%d", &left_count);

    printf("==========\n");
    for(int i = 0; i < REF_PSD_LEN; ++i) {
        printf("Enter value for psd bin [%d] : ", i + 1);
        scanf("%lf", ref_psd + i);
    };

    right_volts = counts_to_volts(right_count, full_scale_v, adc_bits);
    left_volts = counts_to_volts(left_count, full_scale_v, adc_bits);

    mono_ = mono_mix(right_volts, left_volts);

    printf("Right channel: | counts = %d | volts = %5.3f |\n", right_count, right_volts);
    printf("Left channel : | counts = %d | volts = %5.3f |\n", left_count, left_volts);
    printf("Mono mix : %5.3f\n", mono_);
    draw_psd_strip(ref_psd, REF_PSD_LEN);

    return 0;
}

double counts_to_volts(int counts, double fsv, int bit_depth) {
    return (counts * fsv) / (pow(2,bit_depth) - 1.0);
};

double mono_mix(double left, double right) {
    return 0.5 * (left + right);
};

double headroom_pct(double volts, double fsv) {
    volts = (volts < 0) ? -volts : volts;
    return (1.0 - volts / fsv) * 100.0;
};

void draw_psd_strip(const double *psd, int size) {
    
    printf("========== PRINT PSD ==========\n");
    for(int i = 0; i < size; ++i){ 
        printf(" %d : %5.3lf \n", i, psd[i]);
    };
    return;
};