#ifndef __FIRSTAGE__H
#define __FIRSTAGE__H
#include "Stage.h"

class FirStage final : public Stage {
    public:
        double process(double x);
};

//class AnotherStage : public FirStage {} // not possible for final derive

#endif