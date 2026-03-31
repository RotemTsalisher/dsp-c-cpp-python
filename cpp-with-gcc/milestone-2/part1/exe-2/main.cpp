#include <iostream>
#include <type_traits>
#include <concepts>
#include <string>

template <typename T>
concept Numeric = std::is_arithmetic_v<T>;

void print_arithmetic_types(Numeric auto x) {
    std::cout << "x = " << x << std::endl;
};

int main() {
    print_arithmetic_types(4);
    print_arithmetic_types(3.14);
    //print_arithmetic_types("Hello!"); Not Arithmetic Type!
    return 0;
};