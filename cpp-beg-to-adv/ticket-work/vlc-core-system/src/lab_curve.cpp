#include "vlc/lab_curve.hpp"
#include <iostream>
namespace vlc {

double LabCurve::eval(double const x) const
{
    return eval(x, false);
}

double LabCurve::eval(double const x, bool const norm) const
{
    // Matches senior ticket VLC-SR-303 teaching snippet.
    return norm ? x * 2.0 : x;
}

} // namespace vlc
