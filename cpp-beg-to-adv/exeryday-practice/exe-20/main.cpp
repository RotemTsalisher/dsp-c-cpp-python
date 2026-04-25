#include <iostream>
#include "..\exe-16\GainStage.h"

void adjust_gain(GainStage *gs, double g) {
    gs->setGainLinear(g);
};

int main() {
    GainStage *gs = new GainStage();

    adjust_gain(gs, 0.0);
    std::cout << "gs.gain = " << gs->gainLinear() << std::endl;

    adjust_gain(gs, 6.0);
    std::cout << "gs.gain = " << gs->gainLinear() << std::endl;
    
    delete gs;
    return 0;
};


