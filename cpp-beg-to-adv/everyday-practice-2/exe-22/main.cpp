#include <iostream>
#include "CombMixer.h"

int main() {
    // Test default constructor
    CombMixer mixer1;

    std::cout << "mixer1:\n";
    std::cout << "  dry = " << mixer1.get_dry() << '\n';
    std::cout << "  wet = " << mixer1.get_wet() << '\n';

    // Test parameterized constructor
    CombMixer mixer2(0.6, 0.4);

    std::cout << "\nmixer2:\n";
    std::cout << "  dry = " << mixer2.get_dry() << '\n';
    std::cout << "  wet = " << mixer2.get_wet() << '\n';

    // Test method chaining
    mixer2.set_dry(0.2)
          .set_wet(0.8);

    std::cout << "\nmixer2 after setters:\n";
    std::cout << "  dry = " << mixer2.get_dry() << '\n';
    std::cout << "  wet = " << mixer2.get_wet() << '\n';

    return 0;
}