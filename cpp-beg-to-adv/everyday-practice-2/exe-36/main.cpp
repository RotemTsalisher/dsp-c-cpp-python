#include <iostream>
#include "Base.h"
#include "Derived.h"


int main() {

    Base b;
    Derived d;

    b.tune(10.0);
    d.tune(200);

    static_cast<Base>(d).tune(10.0);
    return 0;
}