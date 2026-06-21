#include "vlc/adc_counts.hpp"

#include <cmath>

namespace vlc {

double counts_to_volts(double const counts, double const full_scale_volts, int const resolution_bits)
{
    double const denom = std::ldexp(1.0, resolution_bits) - 1.0;
    return (counts / denom) * full_scale_volts;
}

} // namespace vlc
