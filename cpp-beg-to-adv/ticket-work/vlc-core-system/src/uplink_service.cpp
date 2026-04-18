#include "vlc/uplink_service.hpp"

#include "vlc/adc_counts.hpp"
#include "vlc/mono_mix.hpp"

namespace vlc {

double UplinkService::uplink_mono_rms(double const left, double const right)
{
    return mono_mix_down(left, right);
}

double UplinkService::report_adc_volts(double const counts, double const fs_volts, int const bits)
{
    return counts_to_volts(counts, fs_volts, bits);
}

} // namespace vlc
