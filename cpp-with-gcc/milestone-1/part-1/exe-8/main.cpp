#include <iostream>

template <typename... Args>
auto sum_all(Args... args) {
    return (args + ...);
};

int main() {

    std::cout << "1 + 2 + 3 + 4 + 5 = " << sum_all(1,2,3,4,5) << std::endl;
    std::cout << "1.2 + 2.5 + (-3.2) = " << sum_all(1.2, 2.5, -3.2) << std::endl;
};
