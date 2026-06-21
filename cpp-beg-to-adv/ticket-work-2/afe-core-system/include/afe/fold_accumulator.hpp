#ifndef AFE_FOLD_ACCUMULATOR_HPP
#define AFE_FOLD_ACCUMULATOR_HPP

namespace afe {

template <typename... Ts>
constexpr double fold_negated_from_zero(Ts... values)
{
    return (... - static_cast<double>(values));
}

} // namespace afe

#endif
