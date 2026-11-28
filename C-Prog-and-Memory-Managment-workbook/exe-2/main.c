#include <stdint.h>
#include <stdio.h>

#include "../DSPUtils.h"
#include "../DSPUtils.h"

int main(void)
{
    const float coefficients[] = {
        0.25f,
        0.50f,
        0.25f
    };

    const float biquad_a[] = { 1.0f, -0.250f, 0.125f };
    const float biquad_b[] = { 0.500f, 0.250f, 0.125f };

    const int16_t samples[] = {
        -32768, -16384, -8192, -4096, -1, 0,
        1, 4096, 8192, 16384, 32767
    };

    puts("=== DSPUtils header: repeated inclusion test ===");
    puts("DSPUtils.h compiled successfully when included twice.");

    puts("\n=== Exercise 1.2: FIR initialization ===");
    const uint32_t num_taps =
        (uint32_t)(sizeof(coefficients) / sizeof(coefficients[0]));

    fir_filter_t fir_filter;
    fir_init(coefficients, num_taps, &fir_filter);

#ifdef MODE_DEBUG
    print_fir_taps(&fir_filter);
    puts("");
#endif

    puts("\n=== Exercise 2.2 equivalent: Biquad state/reset ===");
    biquad_filter_t biquad;
    biquad_init(biquad_a, biquad_b, &biquad);

    puts("Initial state:");
#ifdef MODE_DEBUG
    print_biquad(&biquad);
#endif

    biquad.x_[0] = 1.0f;
    biquad.x_[1] = 0.5f;
    biquad.y_[0] = 0.75f;
    biquad.y_[1] = -0.25f;

    puts("State after assigning test delay values:");
#ifdef MODE_DEBUG
    print_biquad(&biquad);
#endif

    biquad_reset(&biquad);

    puts("State after biquad_reset():");
#ifdef MODE_DEBUG
    print_biquad(&biquad);
#endif

    int reset_ok = 1;
    for (int i = 0; i < BIQUAD_COEFFS; ++i)
    {
        if (biquad.x_[i] != 0.0f || biquad.y_[i] != 0.0f)
        {
            reset_ok = 0;
        }

        if (biquad.a_[i] != biquad_a[i] ||
            biquad.b_[i] != biquad_b[i])
        {
            reset_ok = 0;
        }
    }

    printf("Biquad reset result: %s\n",
           reset_ok ? "PASS (delay states zero, coefficients unchanged)"
                    : "FAIL");

    puts("\n=== Exercise 1.1: 16-bit normalization ===");
    for (size_t i = 0;
         i < sizeof(samples) / sizeof(samples[0]);
         ++i)
    {
        printf("Raw: %6d  Normalized: % .6f\n",
               samples[i],
               normalize_sample_16_bit(samples[i]));
    }

    return 0;
}