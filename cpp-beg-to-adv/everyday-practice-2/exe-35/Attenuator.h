#ifndef __ATTENUATOR__H
#define __ATTENUATOR__H

#include "Stage.h"

class Attenuator : public Stage {
    public:
        double process(double x) override;
};

#endif