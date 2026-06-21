#include "afe/response_curve.hpp"

namespace afe {

double ResponseCurve::eval(double const x) const
{
    return eval(x, true);
}

double ResponseCurve::eval(double const x, bool const normalized) const
{
    return normalized ? x * 2.0 : x;
}

} // namespace afe
