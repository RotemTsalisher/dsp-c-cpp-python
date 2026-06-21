#ifndef VLC_QUANTIZE_HPP
#define VLC_QUANTIZE_HPP

#include <type_traits>

namespace vlc {

/// Integer-step quantizer; arithmetic types only (C++20 requires).
template <typename T>
constexpr T quantize_sample(T value, T step)
{
    if constexpr (std::is_arithmetic_v<T>) {
        T const q = value / step;
        return static_cast<T>(static_cast<int>(q)) * step;
    } else {
        return value;
    }
}

/// Ticket / fuzz harness name (VLC-JR-201) — same as `quantize_sample`.
template <typename T>
constexpr T quantizeSample(T const value, T const step)
{
    return quantize_sample(value, step);
}

} // namespace vlc

#endif
