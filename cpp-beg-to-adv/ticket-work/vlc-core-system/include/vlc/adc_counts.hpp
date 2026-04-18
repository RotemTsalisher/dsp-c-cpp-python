#ifndef VLC_ADC_COUNTS_HPP
#define VLC_ADC_COUNTS_HPP

namespace vlc {

/// Unipolar ADC counts → volts (full-scale maps to last code).
double counts_to_volts(double counts, double full_scale_volts, int resolution_bits);

/// Ticket name (VLC-ENTRY-102) — same as `counts_to_volts`.
inline double countsToVolts(double const counts, double const full_scale_volts, int const resolution_bits)
{
    return counts_to_volts(counts, full_scale_volts, resolution_bits);
}

} // namespace vlc

#endif
