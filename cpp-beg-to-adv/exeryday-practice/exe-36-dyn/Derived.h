#ifndef __DERIVED__H
#define __DERIVED__H

#include "Base.h"
class Derived : public Base {
    public:
        void hello_() const override;
};

#endif