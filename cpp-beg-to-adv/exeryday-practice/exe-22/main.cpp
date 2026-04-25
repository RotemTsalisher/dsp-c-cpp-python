#include <iostream>
#include "ChainGain.h"

int main() {

    ChainGain g;

    g.mul(1.5).mul(1.5).print_gain().mul(0.5).print_gain();

    g.reset().print_gain().mul(0.75).print_gain();
    return 0;
}