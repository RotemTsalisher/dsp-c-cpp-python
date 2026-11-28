#ifndef __DSPUTILS__H
#define __DSPUTILS__H

#include <stdio.h>
#include <stdint.h>

#define MODE_DEBUG

float normalize_sample_16_bit(int16_t raw_adc);
void fir_init(const float* const coeffs, uint32_t num_taps);

#ifdef MODE_DEBUG
void print_fir_taps();
#endif

#endif