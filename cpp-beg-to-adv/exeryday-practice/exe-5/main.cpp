#include <iostream>

int main() {
    double floor = 10.0;

    auto mute_if_small = [floor](double x) {
        if ( (x < floor) && (x > -floor) ) {
            return 0.0;
        };
        return x;
    };

    std::cout << "mute_if_small(5.5) = " << mute_if_small(5.5) << std::endl;
    std::cout << "mute_if_small(12.25) = " << mute_if_small(12.25) << std::endl;

    return 0;
};
