#include <iostream>
#include "Base.h"
#include "Derived.h"

int main() {

    Base *poly = new Derived();

    std::cout << std::endl << "** Calls Without Dynamic Casting: " << std::endl;
    poly->speak();
    poly->dance();

    std::cout << std::endl << "** Calls With Dynamic Casting: " << std::endl;
    dynamic_cast<Derived*>(poly)->speak();
    dynamic_cast<Derived*>(poly)->dance();

    return 0;
}