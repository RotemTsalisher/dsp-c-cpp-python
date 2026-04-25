#include <iostream>
#include "FilterSetup.h"

int main() {
    FilterSetup fs0;
    FilterSetup fs1(2, 1.5);

    std::cout << "fs0 is a " << fs0.getOrder() << " order filter with ripple = " << fs0.getRipple() << std::endl;
    std::cout << "fs1 is a " << fs1.getOrder() << " order filter with ripple = " << fs1.getRipple() << std::endl;

    fs0.setOrder(4).setRipple(1.25);
    std::cout << "fs0 is a " << fs0.getOrder() << " order filter with ripple = " << fs0.getRipple() << std::endl;

    return 0;
};