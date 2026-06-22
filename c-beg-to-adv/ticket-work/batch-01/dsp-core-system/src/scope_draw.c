#include "dsp/scope_draw.h"

int scope_bar_length(double const sample, double const full_scale)
{
    if (full_scale <= 0.0) {
        return 0;
    }
    return (int)(sample / full_scale * 20.0);
}
