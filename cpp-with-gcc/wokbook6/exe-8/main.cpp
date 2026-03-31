#include <iostream>
#include <type_traits>

template <typename T>
requires std::is_integral_v<T>
void increment(T &a) {
    a++;
};

int main() {
    int a = 3;
    std::cout << "a = " << a << std::endl;
    increment(a);
    std::cout << "a = " << a << std::endl;
};