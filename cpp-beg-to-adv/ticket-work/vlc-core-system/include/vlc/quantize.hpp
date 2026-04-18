#ifndef VLC_QUANTIZE_HPP
#define VLC_QUANTIZE_HPP

#include <type_traits>

namespace vlc {

/// Integer-step quantizer; arithmetic types only (C++20 requires).
template <typename T>
requires std::is_arithmetic_v<T>
constexpr T quantize_sample(T value, T step)
{
    T const q = value / step;
    return static_cast<T>(static_cast<int>(q)) * step;
}

/// Ticket / fuzz harness name (VLC-JR-201) — same as `quantize_sample`.
template <typename T>
requires std::is_arithmetic_v<T>
constexpr T quantizeSample(T const value, T const step)
{
    return quantize_sample(value, step);
}

} // namespace vlc

#endif
