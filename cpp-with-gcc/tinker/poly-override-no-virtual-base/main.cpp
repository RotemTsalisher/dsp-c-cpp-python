#include <iostream>
#include "Base.h"
#include "Derived.h"

int main() {

    Base b;
    Derived d;

    Base *base_ptr_to_base_obj = &b;
    Base *base_ptr_to_derived_obj = &d;

    base_ptr_to_base_obj->greet();
    base_ptr_to_derived_obj->greet();

    /* an upstream overload that does not exist in the base class */
    //base_ptr_to_derived_obj->greet("Hello From Parameter greet()!");

    base_ptr_to_base_obj->greet(1, "Hello From Param Greet()!");
    base_ptr_to_derived_obj->greet(2, "Hello From Param Greet()!");
    return 0;
};