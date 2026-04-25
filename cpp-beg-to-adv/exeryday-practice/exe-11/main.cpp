#include <iostream>
#include <type_traits>

template <typename T>
struct is_ieee754 {
    static constexpr bool v = std::is_same_v<T, double> || std::is_same_v<T, float>; 
};

template <typename T>
inline constexpr bool is_ieee754_v = is_ieee754<T>::v;

int main() {
    std::cout << "is_ieee754_v<int> = " << is_ieee754_v<int> << std::endl;
    std::cout << "is_ieee754_v<char> = " << is_ieee754_v<char> << std::endl;
    std::cout << "is_ieee754_v<float> = " << is_ieee754_v<float> << std::endl;
    std::cout << "is_ieee754_v<double> = " << is_ieee754_v<double> << std::endl;

    return 0;
};
