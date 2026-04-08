#include <iostream>
#include "..\exe-1\Animal.h"
#include "Dog.h"
#include "Cat.h"

int main() {

    constexpr size_t N = 5;

    Animal a0;
    Dog d0, d1("Fluffy");
    Cat c0, c1("Mr. Bunkles");

    const Animal* collection[N] = {&a0, &d0, &d1, &c0, &c1};

    for(const Animal* ele : collection) {
        ele->sound();
    };
    
    std::cout << "BYE!" << std::endl;
};