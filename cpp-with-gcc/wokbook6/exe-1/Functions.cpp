#include "Functions.h"

int square(int a) {
    std::cout << "Squaring and integer" << std::endl;
    return a * a;
};

double square(double a) {
    std::cout << "Squaring a double" << std::endl;
    return a * a;
};