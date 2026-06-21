#include "vlc/stereo_psd.hpp"

namespace vlc {

MonoPsd::MonoPsd(double const energy)
    : e_{energy}
{
}

double MonoPsd::energy() const
{
    return e_;
}

StereoPsd::StereoPsd(double const left_energy, double const right_energy)
    : MonoPsd{left_energy}
    , r_{right_energy}
{
}

double StereoPsd::right() const
{
    return r_;
}

StereoPsd operator+(StereoPsd const& a, StereoPsd const& b)
{
    return StereoPsd{a.energy() + b.energy(), a.right() + b.right()};
}

} // namespace vlc
