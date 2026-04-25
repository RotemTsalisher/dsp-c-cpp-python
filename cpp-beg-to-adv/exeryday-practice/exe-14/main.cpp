#include <iostream>
#include <concepts>
#include <type_traits>

template <typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

void sink_(Arithmetic auto x) {
    decltype(x) y = x;
    std::cout << "y = " << y << std::endl;
};

int main() {

    double x0 = 1.2;
    int x1 = 2;

    sink_(x0);
    sink_(x1);

    return 0;
}
