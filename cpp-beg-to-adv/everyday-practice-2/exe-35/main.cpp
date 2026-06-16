#include "Stage.h"
#include "Attenuator.h"
#include <iostream>

int main() {

    Attenuator at;
    double x = 2.0;

    std::cout << "x = " << x << std::endl << "x * .25 = " << at.process(x) << std::endl;
    return 0;
}