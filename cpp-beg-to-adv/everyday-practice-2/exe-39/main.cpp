#include <iostream>
#include "Base.h"
#include "Derived.h" 

int main() {
    Base b0;
    Derived d0;

    Base* bp0 = &d0;

    std::cout << std::endl << "WITH BASE OBJECT: " << std::endl;
    b0.binWeight(5);

    std::cout << std::endl << "WITH DERIVED OBJECT:" << std::endl;
    d0.binWeight(2, false);

    std::cout << std::endl << "WITH BASE POINTER:" << std::endl;
    bp0->binWeight(10);

    return 0;

}