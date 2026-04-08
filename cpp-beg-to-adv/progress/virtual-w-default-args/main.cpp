#include <iostream>
#include "Base.h"
#include "Derived.h"

int main() {
    Base b0;
    Derived d0;

    Base *poly = new Derived;

    std::cout << std::endl << "Base No Polymorphism:" << std::endl;
    b0.speak();
    std::cout << std::endl << "Derived No Polymorphism:" << std::endl;
    d0.speak();
    std::cout << std::endl << "Derived By Base Polymorphism:" << std::endl;
    poly->speak();
    return 0;
};