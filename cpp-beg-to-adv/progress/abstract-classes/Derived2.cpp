#include "Derived2.h"

Derived2::Derived2() : Base(), messege("Hello From Derived 2!") {};
void Derived2::speak() const {
    std::cout << "Derived2::speak() : " << this->messege << std::endl;
};