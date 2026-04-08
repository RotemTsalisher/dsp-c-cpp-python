#include "Dog.h"

Dog::Dog() : name("NoName") {
    std::cout << "Dog::Empty C'tor" << std::endl;
};

Dog::Dog(std::string name_) : name(name_) {
    std::cout << "Dog::Param C'tor" << std::endl;
};

Dog::~Dog() {
    std::cout << "Dog::Dtor!" << std::endl;
};
void Dog::sound() const {
    std::cout << "Woof! My name is " << name << std::endl;
};