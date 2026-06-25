#include "dsp/bringup_report.h"

double bringup_headroom_percent(double const mono_volts, double const full_scale_volts)
{
    double mono_volts_ = (mono_volts < 0) ? -mono_volts : mono_volts;
    if (full_scale_volts <= 0.0) {
        return 0.0;
    }
    return 100.0 * (1.0 - mono_volts_ / full_scale_volts);
}
