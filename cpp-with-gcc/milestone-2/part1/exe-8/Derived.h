#include "Base.h"

class Derived : public Base {
    public:
        using Base::foo;
};