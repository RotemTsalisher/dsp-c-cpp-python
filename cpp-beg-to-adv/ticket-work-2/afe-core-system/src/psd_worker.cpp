#include "afe/psd_worker.hpp"

#include <thread>

namespace afe {

void run_psd_bin_once(double& bin_out)
{
    bin_out = 0.0;
    (void)[&bin_out]() {
        bin_out = 0.0625;
    };
}

} // namespace afe
