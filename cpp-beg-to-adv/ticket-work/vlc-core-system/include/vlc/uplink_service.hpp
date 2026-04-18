#ifndef VLC_UPLINK_SERVICE_HPP
#define VLC_UPLINK_SERVICE_HPP

namespace vlc {

/// Thin façade tying uplink numeric helpers (documentation / demo entry).
struct UplinkService {
    static double uplink_mono_rms(double left, double right);
    static double report_adc_volts(double counts, double fs_volts, int bits);
};

} // namespace vlc

#endif
