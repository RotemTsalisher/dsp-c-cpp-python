#ifndef AFE_TAP_SIFTER_HPP
#define AFE_TAP_SIFTER_HPP

namespace afe {

using TapPredicate = bool (*)(double);

bool over_comb_floor(double x);
bool sift_tap(double x, TapPredicate pred);

} // namespace afe

#endif
