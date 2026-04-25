#include <iostream>
#include "Plugin.h"
#include "Engine.h"

int main() {
    Plugin p0;
    Plugin p1(16000);
    Plugin p2(48000);

    std::cout << "p0.sr = " << p0.get_sample_rate() << std::endl;
    std::cout << "p1.sr = " << p1.get_sample_rate() << std::endl;
    std::cout << "p2.sr = " << p2.get_sample_rate() << std::endl;

    return 0;
};