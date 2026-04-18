#include <iostream>
#include <numbers>

constexpr double pi = 3.14;

double radianFreqHz(double fHz) {
    return 2 * pi * fHz;
};

int main() {
    double f0 = 1000;
    std::cout << "f0 = " << f0 << ", w0 = " << radianFreqHz(f0) << std::endl;
};