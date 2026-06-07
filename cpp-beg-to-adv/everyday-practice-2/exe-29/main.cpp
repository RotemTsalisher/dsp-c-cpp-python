#include <iostream>
#include "PeakingEQ.h"

int main()
{
    PeakingEQ eq1;

    std::cout << "eq1.get_a1() = "
              << eq1.get_a1()
              << std::endl;

    PeakingEQ eq2(1.23, 0.75);

    std::cout << "eq2.get_a1() = "
              << eq2.get_a1()
              << std::endl;

    return 0;
}