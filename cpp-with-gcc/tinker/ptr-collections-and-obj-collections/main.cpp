#include <iostream>
#include "Base.h"
#include "Derived.h"
#include "DoubleDerived.h"

int main() {
    constexpr int N = 6;

    Base b0,b1;
    Derived d0,d1;
    DoubleDerived dd0,dd1;

    Base base_collection[N] = {b0,b1,d0,d1,dd0,dd1};
    Base *base_ptr_collection[N] = {&b0, &b1, &d0, &d1, &dd0, &dd1};

    for(size_t i = 0; i < N; i ++ ){
        std::cout << "Itteration (" << i + 1 << "):" << std::endl;
        base_collection[i].greet();
        base_ptr_collection[i]->greet();
        std::cout << std::endl;
    };
};