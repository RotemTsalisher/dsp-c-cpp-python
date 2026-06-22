#include "dsp/apply_gain_fn.h"

double apply_gain_fn(double const sample, GainFn const fn)
{
    (void)fn;
    return sample;
}
