#include "PeakingEQ.h"

double PeakingEQ::get_a1() const {
    return this->a1;
};

PeakingEQ::PeakingEQ() : BiquadSection() {};
PeakingEQ::PeakingEQ(double a1_, double b0_) : BiquadSection(a1_, b0_) {};