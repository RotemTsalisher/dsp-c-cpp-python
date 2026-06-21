#include "afe/tap_sifter.hpp"

namespace afe {

bool over_comb_floor(double const x)
{
    static constexpr double floor = 1e-5;
    return x > floor;
}

bool sift_tap(double const x, TapPredicate const pred)
{
    (void)x;
    (void)pred;
    return true;
}

} // namespace afe
