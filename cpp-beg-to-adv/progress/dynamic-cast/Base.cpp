#include "Base.h"

void Base::speak(std::string m) const {
    std::cout << "Base::speak() : " << m << std::endl;
};

void Base::dance() const {
    std::cout << "Base::dance() : Twist and Shout ! , Twist and Shout !" << std::endl;
};