#include <iostream>
#include <cmath>
#include <type_traits>
#include <concepts>


template <typename T>
requires std::is_floating_point_v<T>
constexpr T db20(T linear) {
    if (linear > 0) {
        return 20*std::log10f(linear);
    }
    return 0;
    
};

int main() {

    constexpr double x1 = 1.0;
    constexpr double x2 = 0.5;
    constexpr double x3 = 0.1;
    constexpr double x4 = 0.0;

    std::cout << "db20(" << x1 << ") = " << db20(x1) << " dB\n";
    std::cout << "db20(" << x2 << ") = " << db20(x2) << " dB\n";
    std::cout << "db20(" << x3 << ") = " << db20(x3) << " dB\n";
    std::cout << "db20(" << x4 << ") = " << db20(x4) << " dB\n";

    /* breaking down the requires clause 
    int x5 = 10;
    std::cout << db20(x5) << '\n';
    */ 
    return 0;
}