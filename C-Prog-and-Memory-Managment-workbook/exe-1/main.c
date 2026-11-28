#include <stdio.h>

#include "../DSPUtils.h"

int main(void)
{
    static const float coefficients[] = {
        0.25f,
        0.50f,
        0.25f
    };

    static const int16_t samples[] = {
        -32768,
        -16384,
        -8192,
        -4096,
        -1,
        0,
        1,
        4096,
        8192,
        16384,
        32767
    };

    size_t num_taps = sizeof(coefficients) / sizeof(coefficients[0]);
    fir_filter_t fir_filter;
    printf("Calling fir_init with %zu taps at address %p\n",
           num_taps,
           (const void *)coefficients);
    fir_init(coefficients, (uint32_t)num_taps, &fir_filter);
    printf("fir_init call completed.\n");

#ifdef MODE_DEBUG
    printf("Stored FIR coefficients: ");
    print_fir_taps(&fir_filter);
    printf("\n");
#endif

    for (size_t i = 0; i < sizeof(samples) / sizeof(samples[0]); ++i)
    {
        printf("Raw: %6d  Normalized: %f\n",
               samples[i],
               normalize_sample_16_bit(samples[i]));
    }

    return 0;
}