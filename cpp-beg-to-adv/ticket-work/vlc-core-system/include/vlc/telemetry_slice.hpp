#ifndef VLC_TELEMETRY_SLICE_HPP
#define VLC_TELEMETRY_SLICE_HPP

namespace vlc {

/// Integrates one slow PSD slice on a worker thread; joins before return.
void run_telemetry_slice_once(double& summary_out);

/// Ticket-shaped façade (VLC-JR-202) — delegates to `run_telemetry_slice_once`.
struct TelemetrySlice {
    static void runOnce(double& summary_out)
    {
        run_telemetry_slice_once(summary_out);
    }
};

} // namespace vlc

#endif
