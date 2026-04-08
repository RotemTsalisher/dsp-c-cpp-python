#include "Animal.h"

void Animal::sound() const {
    std::cout << "Animal::sound()" << std::endl;
    std::cout << "Animal Makes A Sound!" << std::endl;
}

Animal::~Animal() {
    std::cout << "Animal::Dtor" << std::endl;
};