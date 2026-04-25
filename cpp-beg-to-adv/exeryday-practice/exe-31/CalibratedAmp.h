#ifndef __CALIBRATEDAMP__H
#define __CALIBRATEDAMP__H

#include "GainStage.h"
#include "utilities.h"
#include <iostream>

class CalibratedAmp : public GainStage {
    public:
        friend void SetInternalGain(CalibratedAmp& ca, double g_);
        friend std::ostream& operator<<(std::ostream& os, const CalibratedAmp ca) {
            os<< "gain - " << ca.g << std::endl;
            return os;
        };
};

#endif