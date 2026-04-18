#ifndef VLC_TAP_GATE_HPP
#define VLC_TAP_GATE_HPP

namespace vlc {

using TapPredicate = bool (*)(double);
/// Ticket typedef (VLC-JR-205).
using TapPred = TapPredicate;

bool over_noise_floor(double x);

bool gate_tap(double x, TapPredicate pred);

inline bool overNoiseFloor(double const x)
{
    return over_noise_floor(x);
}

inline bool gateTap(double const x, TapPred const pred)
{
    return gate_tap(x, pred);
}

} // namespace vlc

#endif
