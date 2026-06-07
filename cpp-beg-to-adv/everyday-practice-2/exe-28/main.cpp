#include <iostream>
#include "IirBiquadSetup.h"

int main() {
    // Test constructor from BiquadCoeffs
    BiquadCoeffs bc = {
        1.0,    // a0
        0.5,    // b0
        -1.8,   // a1
        1.2,    // b1
        0.81,   // a2
        0.36    // b2
    };

    IirBiquadSetup biquad1(bc);

    std::cout << "biquad1:" << std::endl;
    std::cout << biquad1 << std::endl;

    // Test copy constructor
    IirBiquadSetup biquad2(biquad1);

    std::cout << "\nbiquad2 (copy of biquad1):" << std::endl;
    std::cout << biquad2 << std::endl;

    // Test setter chaining
    biquad2
        .set_a0(2.0)
        .set_b0(1.0)
        .set_a1(-1.5)
        .set_b1(0.8)
        .set_a2(0.7)
        .set_b2(0.2);

    std::cout << "\nbiquad2 after modifications:" << std::endl;
    std::cout << biquad2 << std::endl;

    // Verify original object unchanged
    std::cout << "\nbiquad1 should be unchanged:" << std::endl;
    std::cout << biquad1 << std::endl;

    return 0;
}