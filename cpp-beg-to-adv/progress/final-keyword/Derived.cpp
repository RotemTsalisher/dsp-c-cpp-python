#include "Derived.h"

void Derived::speak() const {
    std::cout << "Derived::speak() : Hello From Derived!" << std::endl;
};

void Derived::dance() const {
    std::cout << "Derived::dance() : Twist and Shout! Twist and Shout!" << std::endl;
};
