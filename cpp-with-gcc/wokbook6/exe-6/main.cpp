#include <iostream>

int compute(int a, int b, int (*fp)(int, int)) {
    std::cout << "Inside Compute !!" << std::endl;
    return fp(a,b);
};

int multiply(int a, int b) {
    return a * b;
};

int main() {

    int (*mp)(int, int) = &multiply;

    std::cout << "2 * 6 = " << compute(2,6,mp) << std::endl;
};