#include "vlc/tap_gate.hpp"

#include <cmath>

namespace vlc {

bool over_noise_floor(double const x)
{
    static constexpr double floor = 1e-5;
    return x > floor;
}

bool gate_tap(double const x, TapPredicate const pred)
{
    return pred(x);
}

} // namespace vlc
