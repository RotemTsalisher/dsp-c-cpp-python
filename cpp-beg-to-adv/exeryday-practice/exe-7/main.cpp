#include <iostream>

double gain(double x, double g) {
    return g * x;
};


int main() {

    using GainFn = double (*)(double, double);
    GainFn gain_ptr = gain;

    double x = 1.0;
    double g = 1.2;

    std::cout << "x = " << x << ", g * x = " << gain_ptr(x,g) << std::endl;

    return 0;
};