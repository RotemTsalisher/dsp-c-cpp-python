#ifndef __GRANDDERIVED__H
#define __GRANDDERIVED__H
#include "Derived.h"

class GrandDerived : public Derived {
    public:
        void speak() const override;
        // void dance() const; | Can't override a "final" virtual function !
};

#endif