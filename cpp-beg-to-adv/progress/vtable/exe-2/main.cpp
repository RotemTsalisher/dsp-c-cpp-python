#include <iostream>
#include "..\exe-1\Base.h"
#include "Derived.h"


int main() {
    Base b0;
    Derived d0;

    b0.talk();
    b0.twist_and_shout();

    d0.talk();
    d0.twist_and_shout();

    void*** vptr = (void***)&d0;
    void** vtable = *(vptr);

    using Func = void(*)();
    Func f0 = (Func)(vtable[0]);
    Func f1 = (Func)(vtable[1]);


    std::cout << "f0: ";
    f0();
    std::cout << "f1: ";
    f1();
    return 0;

};