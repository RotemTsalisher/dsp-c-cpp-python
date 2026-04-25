#include <iostream>
#include "Oscillator.h"

int main() {

    Oscillator os;
    os.frequencyHz = 1000.0;

    std::cout << "fHz = " << os.frequencyHz << std::endl;
    return 0;
};