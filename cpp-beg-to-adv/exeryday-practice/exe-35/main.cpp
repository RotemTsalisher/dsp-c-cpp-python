#include <iostream>
#include "Base.h"
#include "Derived.h"

int main() {
    Derived d0;
    
    d0.work(97.2); // character !!
    d0.work('a');
    d0.Base::work(97);

    return 0;
};