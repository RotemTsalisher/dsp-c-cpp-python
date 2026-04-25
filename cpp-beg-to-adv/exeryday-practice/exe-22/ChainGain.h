#ifndef __CHAINGAIN__H
#define __CHAINGAIN__H

#include <iostream>

class ChainGain {
    private:
        double g_;
    public:
        ChainGain();
        ChainGain(double g);

        double get_gain() const;

        ChainGain& mul(double m);
        ChainGain& reset();
        ChainGain& print_gain();
};


#endif