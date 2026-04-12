#include <iostream>
#include "Base.h"
#include "Derived1.h"
#include "Derived2.h"

int main() {
    Base* b_ptr_to_derived_1 = new Derived1();
    Base* b_ptr_to_derived_2 = new Derived2();

    b_ptr_to_derived_1->speak();
    b_ptr_to_derived_2->speak();
    return 0;
};