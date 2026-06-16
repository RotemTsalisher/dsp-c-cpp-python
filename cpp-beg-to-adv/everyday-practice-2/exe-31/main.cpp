#include <iostream>
#include "CalibratedBank.h"
#include "helper_funcs.h"

int main() {
    CalibratedBank cb(5.0);

    std::cout << "Initial gain: " << cb.get_gain() << std::endl;

    zero_gain(cb);

    std::cout << "After zero_gain: " << cb.get_gain() << std::endl;

    return 0;
}