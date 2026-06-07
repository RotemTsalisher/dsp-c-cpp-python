#ifndef __IIRBIQUADSETUP__H
#define __IIRBIQUADSETUP__H

#include <iostream>

struct BiquadCoeffs {
    double a0, b0, a1, b1, a2, b2;
};

class IirBiquadSetup {
    private:
        double a0, b0, a1, b1, a2, b2;
    public:
        IirBiquadSetup();
        IirBiquadSetup(const struct BiquadCoeffs& bc);
        IirBiquadSetup(const IirBiquadSetup& other);

        IirBiquadSetup& set_a0(double a0_);
        IirBiquadSetup& set_b0(double b0_);
        IirBiquadSetup& set_a1(double a1_);
        IirBiquadSetup& set_b1(double b1_);
        IirBiquadSetup& set_a2(double a2_);
        IirBiquadSetup& set_b2(double b2_);

        friend std::ostream& operator<<(std::ostream& os, const IirBiquadSetup& ibs);
};

#endif