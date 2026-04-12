#ifndef __DERIVED2__H
#define __DERIVED2__H

#include "Base.h"

class Derived2 : public Base {
    private:
        std::string messege;

    public:
        Derived2();
        void speak() const override;
};

#endif