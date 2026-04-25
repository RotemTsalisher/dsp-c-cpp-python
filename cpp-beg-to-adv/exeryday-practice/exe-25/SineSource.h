#ifndef __SINESOURCE__H
#define __SINESOURCE__H

#include "Source.h"

class SineSource : public Source {
    public:
        double next() const override final;
        ~SineSource();
};

#endif