#include "Derived.h"

int Derived::counter = 0;

Derived::Derived() : Base() {
    std::cout << "Derived Empty Constructor!" << std::endl;
    Derived::counter++;
};

int Derived::get_counter() const {
    return counter;
};