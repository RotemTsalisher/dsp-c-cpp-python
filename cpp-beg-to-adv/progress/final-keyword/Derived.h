#ifndef __DERIVED__H
#define __DERIVED__H

#include "Base.h"

class Derived : public Base {
    public:
        void speak() const override;
        void dance() const override final;
};

#endif