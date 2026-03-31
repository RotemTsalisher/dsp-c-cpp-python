#include <iostream>
#include <string>

template <typename T>
struct type_multiplier {
    static constexpr int value = 1;
};

template <>
struct type_multiplier<double> {
    static constexpr int value = 2;
};

template <typename T>
constexpr int type_multiplier_v = type_multiplier<T>::value;

int main() {
    double a = 1.1;
    int b = 1;

    std::cout << "double multiplier = " << type_multiplier_v<decltype(a)> << std::endl;
    std::cout << "int multiplier = " << type_multiplier_v<decltype(b)> << std::endl;
};
