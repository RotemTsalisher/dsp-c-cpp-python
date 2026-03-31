#include <iostream>

template <typename T>
T max_value(T a, T b) {
    return (a > b) ? a : b;
};

int main() {

    int a = 3, b = 4;
    double c = 3.2, d = 4.2;

    std::cout << "max(" << a << "," << b << ") = " << max_value(a,b) << std::endl;
    std::cout << "max(" << c << "," << d << ") = " << max_value(c,d) << std::endl;
    return 0;
};