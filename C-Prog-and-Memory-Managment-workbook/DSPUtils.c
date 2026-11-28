#include "DSPUtils.h"


/* Macro Functions (UnExposed) */
#define TWO_TO_THE_POWER(p)     (0x01 << (p))
#define ADC_NORMALIZE(p)        TWO_TO_THE_POWER((p) - 1)
#define SCALE_AFE_VALUE(channel_ptr, gain_factor, clip_limits) \
    do { \
        (*(channel_ptr)) *= (gain_factor); \
        if((*(channel_ptr)) > (clip_limits)) \
            (*(channel_ptr)) = (clip_limits); \
    } while(0);


float normalize_sample_16_bit(int16_t raw_adc) {

    float res = (float)raw_adc / ADC_NORMALIZE(16);
    return res;
};

void fir_init(const float* const coeffs, uint32_t num_taps, fir_filter_t* fir_filter) {
    fir_filter->coeffs = coeffs;
    fir_filter->num_of_taps = num_taps;
};

void biquad_init(const float* a, const float* b, biquad_filter_t* biquad) {
    
    biquad->a_[0] = 1;

    for(int i = 0; i < BIQUAD_COEFFS; ++i) {
        biquad->a_[i] = a[i];
        biquad->b_[i] = b[i];
        biquad->x_[i] = 0.0f;
        biquad->y_[i] = 0.0f;
    };
};

void biquad_reset(biquad_filter_t* biquad) {
    for(int i = 0; i < BIQUAD_COEFFS; ++i) {
        biquad->x_[i] = 0.0f;
        biquad->y_[i] = 0.0f;
    };
};

#ifdef MODE_DEBUG
void print_fir_taps(fir_filter_t* fir_filter) {
    for(int i = 0; i < fir_filter->num_of_taps; ++i) {
        printf("coeffs[%d] = %5.3f || ", i, fir_filter->coeffs[i]);
    };
};

void print_biquad(biquad_filter_t* biquad) {
    for(int i = 0; i < BIQUAD_COEFFS; ++i) {
        printf("biquad->a[%d] = %4.2f\n", i, biquad->a_[i]);
        printf("biquad->b[%d] = %4.2f\n", i, biquad->b_[i]);
        printf("biquad->x[%d] = %4.2f\n", i, biquad->x_[i]);
        printf("biquad->y[%d] = %4.2f\n", i, biquad->y_[i]);
    }
};
#endif