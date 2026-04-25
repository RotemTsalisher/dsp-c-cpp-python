#include <iostream>
#include "CalibratedAmp.h"

int main() {
    CalibratedAmp ca;
    std::cout << ca;

    SetInternalGain(ca, 1.414);
    std::cout << ca;
    return 0;
};