#include <iostream>
#include "ScaledTap.h"

int main() {
    double sample = 0.75;

    ScaledTap tap1(10, sample);

    std::cout << "tap1.value() = "
              << tap1.value() << std::endl;

    // Test copy constructor
    ScaledTap tap2(tap1);

    std::cout << "tap2.value() = "
              << tap2.value() << std::endl;

    // Change the referenced sample
    sample = 1.25;

    std::cout << "\nAfter changing sample:\n";
    std::cout << "tap1.value() = "
              << tap1.value() << std::endl;

    std::cout << "tap2.value() = "
              << tap2.value() << std::endl;

    return 0;
}