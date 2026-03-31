#include <iostream>

template <typename... Args>
auto sum_all(Args... args) {
    return (args + ...);
};

int main() {
    std::cout << "sum_all(1,2,3,4,5) = " << sum_all<int>(1,2,3,4,5) << std::endl;
    std::cout << "sum_all(1,2,3.4,4.5,5.9) = " << sum_all<double>(1,2,3.4,4.5,5.9) << std::endl;
    return 0;
};