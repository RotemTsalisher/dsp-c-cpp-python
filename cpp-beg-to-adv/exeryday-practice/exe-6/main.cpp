#include <iostream>
#include <type_traits>
#include <concepts>

template <typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

template <Arithmetic T>
double average_two(T a, T b) {
    return 0.5 * (static_cast<float>(a) + b);
};

int main() {

    double a = 1.0;
    double b = 2.0;

    int a_ = 1;
    int b_ = 2;

    std::cout << "0.5(1.0 + 2.0) = " << average_two(a,b) << std::endl;
    std::cout << "0.5( 1  + 2  ) = " << average_two(a_,b_) << std::endl;

    return 0;

};
