#ifndef __DSPUTILS__H
#define __DSPUTILS__H

#include <stdio.h>
#include <stdint.h>

#define MODE_DEBUG

/* Macro Constants */
#define BIQUAD_COEFFS           3
#define BIQUAD_ORDER            (BIQUAD_COEFFS - 1)

struct FirFilter {
    const float *coeffs;
    uint32_t num_of_taps;
};

struct BiQuad {
    float a_[BIQUAD_COEFFS], b_[BIQUAD_COEFFS];
    float x_[BIQUAD_COEFFS], y_[BIQUAD_COEFFS];
};

typedef struct FirFilter fir_filter_t;
typedef struct BiQuad    biquad_filter_t;

float normalize_sample_16_bit(int16_t raw_adc);
void fir_init(const float* const coeffs, uint32_t num_taps, fir_filter_t* fir_filter);
void biquad_init(const float* a, const float* b, biquad_filter_t* biquad);
void biquad_reset(biquad_filter_t* biquad);

#ifdef MODE_DEBUG
void print_fir_taps(fir_filter_t* fir_filter);
void print_biquad(biquad_filter_t* biquad);
#endif

#endif