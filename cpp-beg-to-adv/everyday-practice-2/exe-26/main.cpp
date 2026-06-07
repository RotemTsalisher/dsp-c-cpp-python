#include <iostream>
#include "TapDelay.h"

int main() {
    TapDelay delay;

    std::cout << "Initial index: " << delay.readIndex() << std::endl;

    for (int i = 0; i < 5; i++) {
        delay.advanceIndex();
        std::cout << "After advance " << i + 1
                  << ": " << delay.readIndex() << std::endl;
    }

    return 0;
}