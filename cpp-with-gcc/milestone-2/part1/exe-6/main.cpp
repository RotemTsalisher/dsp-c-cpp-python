#include "Animal.h"
#include "Dog.h"
#include "Cat.h"

int main() {

    Animal *dog = new Dog("Snoopy");
    Animal *cat = new Cat("Mr. Buckles");

    dog->speak();
    cat->speak();

};