#ifndef __DERIVED1__H
#define __DERIVED1__H

#include "Base.h"

class Derived1 : public Base {
    private:
        std::string messege;

    public:
        Derived1();
        void speak() const override;
};
#endif