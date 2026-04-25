#ifndef __FIRKERNEL__H
#define __FIRKERMEL__H

#include "Processor.h"

class FirKernel final : public Processor {
    public:
        double tick(double x) const override;
        ~FirKernel() = default;
};
#endif