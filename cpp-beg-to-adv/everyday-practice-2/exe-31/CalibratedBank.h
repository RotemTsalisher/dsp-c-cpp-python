#ifndef __CALIBRATEDBANK__H
#define __CALIBRATEDBANK__H

#include "CoeffBank.h"
#include "helper_funcs.h"

class CalibratedBank : public CoeffBank {
    public:
        CalibratedBank();
        CalibratedBank(double g);
        double get_gain() const;

        friend void zero_gain(CalibratedBank& cb);
};

#endif