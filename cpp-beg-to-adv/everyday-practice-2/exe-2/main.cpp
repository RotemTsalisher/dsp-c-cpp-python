#include <iostream>

double quadraticEnergy(double x) {
    return x * x;
};

double quadraticEnergy(double left, double right) {
    return 0.5*(left * left + right * right);
};

int main() {

    double x = 1.25;
    double r = 0.7, l = 0.7;

    std::cout << "quadraticEnergy(x) = " << quadraticEnergy(x) << std::endl;
    std::cout << "quadraticEnergy(l, r) = " << quadraticEnergy(l, r) << std::endl;

    return 0;
};