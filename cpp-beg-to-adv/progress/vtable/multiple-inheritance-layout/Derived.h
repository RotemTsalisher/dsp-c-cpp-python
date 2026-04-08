#ifndef __DERIVED__H
#define __DERIVED__H

#include "Base1.h"
#include "Base2.h"

#include <iostream>

class Derived : public Base1, public Base2 {

    public:
        void speak() const override;
        void dance() const override;
};

#endif