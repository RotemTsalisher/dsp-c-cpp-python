#include "Derived.h"

void Derived::speak(std::string m) const {
    std::cout << "Derived::speak() : " << m << std::endl;
};

void Derived::dance() const {
    std::cout << "Derived::dance() : Twist and Shout ! , Twist and Shout !" << std::endl;
};