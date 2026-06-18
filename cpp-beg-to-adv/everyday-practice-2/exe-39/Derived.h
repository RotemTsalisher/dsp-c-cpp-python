#ifndef __DERIVED__H
#define __DERIVED__H

#include "Base.h"

class Derived : public Base {
    public:
        double binWeight(int k, bool normalized) const;
};

#endif