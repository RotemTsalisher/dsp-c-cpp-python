#include <iostream>

int multiply(int a, int b) {
    return a * b;
};

int main() {

    int (*fp)(int, int) = &multiply;

    std::cout << "multiply(2,6) = " << fp(2,6) << std::endl;
    return 0;
};