#include <iostream>
#include "Counter.h"

int main() {
    Counter c0;
    Counter c1(100);
    Counter c2(c0);

    c0.set_value(25).increment();
    std::cout << "c0 = " << c0.get_value() << std::endl;
    
    c1.increment(150);
    std::cout << "c1 = " << c1.get_value() << std::endl;

    c2.increment(1000).set_value(20);
    std::cout << "c2 = " << c2.get_value() << std::endl;
};