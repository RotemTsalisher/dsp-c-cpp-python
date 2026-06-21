#include "afe/stereo_comb.hpp"

namespace afe {

StereoComb operator+(StereoComb const& a, StereoComb const& b)
{
    return StereoComb{a.left() + b.left(), a.left() + b.left()};
}

} // namespace afe
