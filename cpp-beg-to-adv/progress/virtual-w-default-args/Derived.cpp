#include "Derived.h"

void Derived::speak(std::string m) const {
    std::cout << "Derived::speak() : " << m << std::endl;
};
