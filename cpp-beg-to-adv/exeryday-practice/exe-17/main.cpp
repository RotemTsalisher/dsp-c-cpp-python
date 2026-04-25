#include <iostream>
#include "BrickwallSpec.h"

int main() {
    BrickwallSpec bw0;
    BrickwallSpec bw1(15000.0);

    std::cout << "bw0.fc = " << bw0.get_fc() << std::endl;
    std::cout << "bw1.fc = " << bw1.get_fc() << std::endl;

    return 0;
};
