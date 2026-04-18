#include "vlc/notch_source.hpp"

namespace vlc {

double NotchSource::next()
{
    phase_ += 0.01;
    if (phase_ > 1.0) {
        phase_ -= 1.0;
    }
    return 0.1 * phase_;
}

} // namespace vlc
