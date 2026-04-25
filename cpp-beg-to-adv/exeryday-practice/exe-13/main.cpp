#include <iostream>
#include <cmath>

namespace dsp::math {
    double db10(double db_linear) {
        return 10 * std::log10(db_linear);
    };
};

int main() {
    double linear_ = 100;

    std::cout << "dsp::math::db10(100) = " << dsp::math::db10(linear_) << std::endl;
    return 0;
};