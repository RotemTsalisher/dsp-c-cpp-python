#include <iostream>
#include "Buffer.h"

int main() {
    double stereo[] = {
        1.0, 2.0,   // L,R
        3.0, 4.0,   // L,R
        5.0, 6.0,   // L,R
        7.0, 8.0    // L,R
    };

    Buffer buff(stereo, 8);

    double energy_l, energy_r;
    buff.compute_energy(energy_l, energy_r);

    std::cout << "Left energy  = " << energy_l << '\n';
    std::cout << "Right energy = " << energy_r << '\n';

    double mono_data[4] = {0};
    Buffer mono(mono_data, 4);

    buff.write_mono(mono);

    std::cout << "Mono samples:\n";
    for(size_t i = 0; i < 4; ++i) {
        std::cout << mono[i] << ' ';
    }
    std::cout << '\n';

    return 0;
}