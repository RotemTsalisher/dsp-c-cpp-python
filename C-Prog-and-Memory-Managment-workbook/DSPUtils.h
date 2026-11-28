#ifndef __DSPUTILS__H
#define __DSPUTILS__H

#include <stdio.h>
#include <stdint.h>

#define MODE_DEBUG

/* Macro Constants */
#define BIQUAD_COEFFS           3
#define BIQUAD_ORDER            (BIQUAD_COEFFS - 1)
#define AUDIO_HEADER_SIZE       (8 + 64 + 16 + 8 + 32) //in bytes
struct FirFilter {
    const float *coeffs;
    uint32_t num_of_taps;
};

struct BiQuad {
    float a_[BIQUAD_COEFFS], b_[BIQUAD_COEFFS];
    float x_[BIQUAD_COEFFS], y_[BIQUAD_COEFFS];
};

struct AudioFrameHeader {
    uint8_t sync_byte;
    uint64_t timestamp_ns;
    uint16_t sample_rate;
    uint8_t channel_count;
    uint32_t frame_index;
};

#ifdef MODE_DEBUG
struct UnoptimizedBufferMeta {
    uint8_t valid;
    double max_amplitude;
    uint16_t num_channls;
    float peak_frequency;
    uint8_t muted;
    uint64_t frame_id;
};

struct OptimizedBufferMeta {
    double max_amplitude;
    uint64_t frame_id;

    uint16_t num_channls;
    float peak_frequency;
    uint8_t valid;
    uint8_t muted;
};
#endif

typedef struct FirFilter              fir_filter_t;
typedef struct BiQuad                 biquad_filter_t;
typedef struct AudioFrameHeader       audio_frame_header_t; 
typedef struct UnoptimizedBufferMeta  unoptimized_buffer_meta_t;
typedef struct OptimizedBufferMeta    optimized_buffer_meta_t;

float normalize_sample_16_bit(int16_t raw_adc);
void fir_init(const float* const coeffs, uint32_t num_taps, fir_filter_t* fir_filter);
void biquad_init(const float* a, const float* b, biquad_filter_t* biquad);
void biquad_reset(biquad_filter_t* biquad);

#ifdef MODE_DEBUG
void print_fir_taps(fir_filter_t* fir_filter);
void print_biquad(biquad_filter_t* biquad);
void print_diff_in_size();
#endif

#endif