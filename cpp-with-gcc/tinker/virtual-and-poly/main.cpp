#include <iostream>
#include "Animal.h"
#include "Dog.h"
#include "Cat.h"

void speak(const Animal* a) {
    a->speak();
};

int main() {

    Animal* animal_ = new Animal;
    Animal* dog_ = new Dog("Snoopy");
    Animal* cat_ = new Cat("Mr. Buckles");

    Animal* collection[3] = {animal_, dog_, cat_};
    size_t i = 0;

    for(const Animal *ele : collection) {
        std::cout << "Itteration " << (i++ + 1) << ": "; 
        ele->speak();
    };

    
    return 0;
}