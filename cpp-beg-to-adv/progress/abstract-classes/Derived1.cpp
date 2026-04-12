#include "Derived1.h"

Derived1::Derived1() : Base(), messege("Hello From Derived 1!") {};
void Derived1::speak() const {
    std::cout << "Derived1::speak() : " << this->messege << std::endl;
};
