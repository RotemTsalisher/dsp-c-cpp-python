#ifndef __SCALEDTAP__H
#define __SCALEDTAP__H

#include <iostream>

class ScaledTap {
    private:
        int const tapIndex_;
        double const& ringSample_;
    public:
        ScaledTap();
        ScaledTap(int const tapIndex, double const& ringSample);
        ScaledTap(const ScaledTap& other);

        double value() const;
};

#endif