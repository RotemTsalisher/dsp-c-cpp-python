#ifndef VLC_AFE_REGISTERS_HPP
#define VLC_AFE_REGISTERS_HPP

#include <cstdint>
#include <type_traits>

namespace vlc::dsp::afe {

template <typename T>
inline constexpr bool is_word32_v = std::is_same_v<T, std::uint32_t>;

template <typename T>
constexpr std::uint32_t masked_or(std::uint32_t base, std::uint32_t mask, T field)
{
    return base | (static_cast<std::uint32_t>(field) & mask);
}

} // namespace vlc::dsp::afe

/// HAL doc / ticket spelling (VLC-JR-204): `dsp::afe::maskedOr` forwards into `vlc::dsp::afe`.
namespace dsp::afe {

template <typename T>
constexpr std::uint32_t maskedOr(std::uint32_t const base, std::uint32_t const mask, T const field)
{
    return vlc::dsp::afe::masked_or(base, mask, field);
}

} // namespace dsp::afe

#endif
