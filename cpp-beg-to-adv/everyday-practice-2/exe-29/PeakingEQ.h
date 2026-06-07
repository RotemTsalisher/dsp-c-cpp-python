#ifndef __PEAKINGEQ__H
#define __PEAKINGEQ__H

#include "BiquadSection.h"

class PeakingEQ : public BiquadSection {
    public:
        PeakingEQ();
        PeakingEQ(double a1_, double b0_);
        double get_a1() const;
};

#endif