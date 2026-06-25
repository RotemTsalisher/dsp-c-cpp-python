#include "dsp/scope_draw.h"

int scope_bar_length(double const sample, double const full_scale)
{
    double sample_ = (sample < 0) ? -sample : sample;
    if (full_scale <= 0.0) {
        return 0;
    }
    return (int)(sample_ / full_scale * 20.0);
}
