#include <iostream>

int main() {

    auto add_num = [](auto a, auto b) {return a + b;};

    std::cout << "add_num(3,4) = " << add_num(3,4) << std::endl;
    std::cout << "add_num(-1.5, 3) = " << add_num(-1.5, 3.0) << std::endl;

    return 0;
};