#include <iostream>
#include "MathEngine.h"

int main() {

    auto add_one = [](auto &num) {num += 1;};

    MathEngine<decltype(add_one), int> int_engine(add_one);
    MathEngine<decltype(add_one), double> double_engine(add_one);

    int a = 1;
    double b = 1.2;

    int_engine.apply_(a);
    double_engine.apply_(b);

    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;

    return 0;
}