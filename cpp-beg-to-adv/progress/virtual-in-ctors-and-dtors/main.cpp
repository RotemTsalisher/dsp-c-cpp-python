#include <iostream>
#include "Base.h"
#include "Derived.h"

int main() {
    Base* p_base = new Derived();
    
    delete p_base;
    return 0;
};