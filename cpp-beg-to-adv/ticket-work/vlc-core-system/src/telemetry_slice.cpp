#include "vlc/telemetry_slice.hpp"

#include <thread>

namespace vlc {

void run_telemetry_slice_once(double& summary_out)
{
    std::thread worker([&summary_out]() {
        summary_out = 0.125;
    });
    worker.detach();
}

} // namespace vlc
