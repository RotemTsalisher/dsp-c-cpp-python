#include <iostream>
#include "GainStage.h"

int main() {

    GainStage gs;

    gs.setGainLinear(0.0);
    std::cout << "gain = " << gs.gainLinear() << std::endl;

    gs.setGainLinear(1.2);
    std::cout << "gain = " << gs.gainLinear() << std::endl;

    return 0;
};