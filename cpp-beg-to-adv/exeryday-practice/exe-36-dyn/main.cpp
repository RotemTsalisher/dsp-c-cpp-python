#include <iostream>
#include "Base.h"
#include "Derived.h"
#include "NotDerived.h"

int main() {
    Base *p_obj = new Derived;


    p_obj->hello_();
    dynamic_cast<Derived *>(p_obj)->hello_();
    p_obj->Base::hello_();

    auto *test = dynamic_cast<NotDerived *>(p_obj);
    if(test) {
        test->hello_();
    }
    else {
        std::cout << " THIS IS NOT DERIVED!!" << std::endl;
    }
    return 0;

};