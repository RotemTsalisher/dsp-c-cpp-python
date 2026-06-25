#include "dsp/adc_counts.h"

#include <math.h>

double counts_to_volts(int const counts, double const full_scale_volts, int const bits)
{
    double const denom = pow(2.0, (double)bits) - 1.0;
    return ((double)counts / denom) * full_scale_volts;
}
