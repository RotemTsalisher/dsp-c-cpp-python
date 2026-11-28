#include "DSPUtils.h"

#define TWO_TO_THE_POWER(p)     (0x01 << (p))
#define ADC_NORMALIZE(p)        TWO_TO_THE_POWER((p) - 1)

struct FirFilter {
    
    const float *coeffs;
    uint32_t num_of_taps;
};

typedef struct FirFilter fir_filter_t;

static fir_filter_t fir_filter;

float normalize_sample_16_bit(int16_t raw_adc) {

    float res = (float)raw_adc / ADC_NORMALIZE(16);
    return res;
};

void fir_init(const float* const coeffs, uint32_t num_taps) {
    fir_filter.coeffs = coeffs;
    fir_filter.num_of_taps = num_taps;
};

#ifdef MODE_DEBUG
void print_fir_taps() {
    for(int i = 0; i < fir_filter.num_of_taps; ++i) {
        printf("coeffs[%d] = %5.3f || ", i, fir_filter.coeffs[i]);
    };
}
#endif