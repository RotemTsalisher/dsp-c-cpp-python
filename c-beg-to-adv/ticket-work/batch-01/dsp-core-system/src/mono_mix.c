#include "dsp/mono_mix.h"

double mono_mix_down(double const left, double const right)
{
    return 0.5 * (left + right);
}
