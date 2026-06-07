#include "IirBiquadSetup.h"

IirBiquadSetup::IirBiquadSetup() : 
    a0(1.0), a1(0.0), a2(0.0), b0(0.0), b1(0.0), b2(0.0) {};

IirBiquadSetup::IirBiquadSetup(const struct BiquadCoeffs& bc) : 
    a0(bc.a0), a1(bc.a1), a2(bc.a2), b0(bc.b0), b1(bc.b1), b2(bc.b2) {};

IirBiquadSetup::IirBiquadSetup(const IirBiquadSetup& other) :
    a0(other.a0), a1(other.a1), a2(other.a2), b0(other.b0), b1(other.b1), b2(other.b2) {};

IirBiquadSetup& IirBiquadSetup::set_a0(double a0_) {
    a0 = a0_;
    return *this;
};

IirBiquadSetup& IirBiquadSetup::set_a1(double a1_) {
    a1 = a1_;
    return *this;
};

IirBiquadSetup& IirBiquadSetup::set_a2(double a2_) {
    a2 = a2_;
    return *this;
};

IirBiquadSetup& IirBiquadSetup::set_b0(double b0_) {
    b0 = b0_;
    return *this;
};

IirBiquadSetup& IirBiquadSetup::set_b1(double b1_) {
    b1 = b1_;
    return *this;
};

IirBiquadSetup& IirBiquadSetup::set_b2(double b2_) {
    b2 = b2_;
    return *this;
};

std::ostream& operator<<(std::ostream& os, const IirBiquadSetup& ibs) {
    os << "Biquds: (a0, a1, a2) = (" << ibs.a0 << ", " << ibs.a1 << ", " 
    << ibs.a2 << ") || (b0, b1, b2) = (" << 
    ibs.b0 << ", " << ibs.b1 << ", " << ibs.b2 << ")" << std::endl;

    return os;
};