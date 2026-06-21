#ifndef AFE_REGISTER_MASK_HPP
#define AFE_REGISTER_MASK_HPP

#include <cstdint>
#include <type_traits>

namespace afe {

template <typename T>
requires std::is_integral_v<T>
std::uint32_t masked_or(std::uint32_t base, std::uint32_t mask, T field)
{
    return (base & ~mask) | (static_cast<std::uint32_t>(field) & mask);
}

} // namespace afe

#endif
