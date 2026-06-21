#include "vlc/mono_mix.hpp"

namespace vlc {

double mono_mix_down(double const left, double const right)
{
    return left + right;
}

} // namespace vlc
