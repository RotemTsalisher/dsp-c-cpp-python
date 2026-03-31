#include <iostream>
#include "Calculator.h"

int add_two_integers(int a, int b) {
    return a + b;
};

int main() {

    auto multiply_two_integers = [](int a, int b) {return a * b;};

    Calculator c;

    std::cout << "2 + 3 = " << c.calculate(2,3, &add_two_integers) << std::endl;
    std::cout << "2 * 3 = " << c.calculate(2,3, multiply_two_integers) << std::endl;

    std::cout << "DONE!" << std::endl;
};