#include <iostream>
#include "Temperature.h"


int main() {
    Temperature t0;
    Temperature t1(20.0);

    int x = 3;

    t0 = t0 + x;
    std::cout << t0 << std::endl;

    t0 = x + t0;
    std::cout << t0 << std::endl;

    t1 = t0 - (x - 1);
    std::cout << t1 << std::endl;

    std::cout << "t0:" << std::endl;
    std::cout << t0 << std::endl;
    
    t1 = (x + 100) - t0;
    std::cout << t1 << std::endl;

    return 0;
};