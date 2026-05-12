#include <iostream>

template <typename... Args>
double args_product(Args... args) {
    return (1 * ... * args);
}

int main() {

    std::cout << args_product(2, 3, 4) << '\n';          // 24
    std::cout << args_product(1.5, 2.0, 3.0) << '\n';    // 9
    std::cout << args_product(5) << '\n';                // 5
    std::cout << args_product() << '\n';                 // 1

    return 0;
}