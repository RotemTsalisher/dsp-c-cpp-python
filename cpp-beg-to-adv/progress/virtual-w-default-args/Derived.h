#ifndef __DERIVED__H
#define __DERIVED__H

#include "Base.h"

class Derived : public Base {
    public:
        void speak(std::string m = "Hello From Derived Class !") const override;
};
#endif