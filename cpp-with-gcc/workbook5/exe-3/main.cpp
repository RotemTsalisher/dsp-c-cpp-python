#include <iostream>
#include "Counter.h"

int main() {

    Counter* c0;
    c0 = new Counter;
    Counter* c1;
    c1 = new Counter{15};
    Counter* c2;
    c2 = new Counter{*c0};

    std::cout << "c0.value = " << c0->get_value() << std::endl;
    std::cout << "c1.value = " << c1->get_value() << std::endl;
    std::cout << "c2.value = " << c2->get_value() << std::endl;


    c0->increment();
    c1->increment(15);
    c2->increment(20);

    std::cout << "c0.value = " << c0->get_value() << std::endl;
    std::cout << "c1.value = " << c1->get_value() << std::endl;
    std::cout << "c2.value = " << c2->get_value() << std::endl;

    delete c2;
    delete c1;
    delete c0;

    return 0;
}