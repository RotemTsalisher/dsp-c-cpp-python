#ifndef __BIQUADSECTION__H
#define __BIQUADSECTION__H

class BiquadSection {
    protected:
        double a1, b0;
    public:
        BiquadSection();
        BiquadSection(double a1_, double b0_);
};

#endif