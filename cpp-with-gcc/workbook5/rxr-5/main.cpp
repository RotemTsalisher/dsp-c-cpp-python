#include <iostream>
#include "Accumulator.h"

int main() {

    Accumulator acc0;
    Accumulator acc1(15);
    Accumulator acc2(acc0);

    std::cout << "acc0.value = " << acc0.get_value() << std::endl;
    std::cout << "acc1.value = " << acc1.get_value() << std::endl;
    std::cout << "acc2.value = " << acc2.get_value() << std::endl;

    acc2.add(acc1.get_value()).multiply(0.5);
    std::cout << "acc2.value = " << acc2.get_value() << std::endl;
    return 0;
}