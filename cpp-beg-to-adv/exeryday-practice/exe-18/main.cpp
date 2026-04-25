#include <iostream>
#include "DelayLine.h"

int main() {

    DelayLine dl0; // tap count = 0
    DelayLine dl1(12);

    std::cout << "dl0 has a delay of " << dl0.get_tap_counts() << " taps!" << std::endl;
    std::cout << "dl1 has a delay of " << dl1.get_tap_counts() << " taps!" << std::endl;

    dl0.set_tap_counts(4);
    std::cout << "dl0 has a delay of " << dl0.get_tap_counts() << " taps!" << std::endl;

    return 0;
};
