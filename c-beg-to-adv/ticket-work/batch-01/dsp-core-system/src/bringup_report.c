#include "dsp/bringup_report.h"

double bringup_headroom_percent(double const mono_volts, double const full_scale_volts)
{
    if (full_scale_volts <= 0.0) {
        return 0.0;
    }
    return 100.0 * mono_volts / full_scale_volts;
}
