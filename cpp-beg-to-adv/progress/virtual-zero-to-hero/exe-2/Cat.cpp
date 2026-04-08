#include "Cat.h"

Cat::Cat() : name("NoName") {
    std::cout << "Cat::Empty C'tor" << std::endl;
};

Cat::Cat(std::string name_) : name(name_) {
    std::cout << "Cat::Params C'tor" << std::endl;
};

Cat::~Cat() {
    std::cout << "Cat::Dtor!" << std::endl;
};

void Cat::sound() const {
    std::cout << "Meow! My name is " << name << std::endl;
};