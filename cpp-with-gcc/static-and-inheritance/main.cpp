#include <iostream>
#include "Base.h"
#include "Derived.h"

int main() {

    Base b0;
    Derived d0;

    const Base* collection[3];

    for (const Base* ele : collection) {
        ele = new Derived;
    };
    

    std::cout << "Base counter : " << b0.get_counter() << std::endl;
    std::cout << "Derived counter : " << d0.get_counter() << std::endl;
};