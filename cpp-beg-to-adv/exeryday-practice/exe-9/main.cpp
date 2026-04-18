#include <iostream>

template <typename... Ts>
constexpr double sum_(Ts... v) {
    return (v + ...);
};

int main() {

    std::cout << "sum(1,2,3,4) = " << sum_(1,2,3,4) << std::endl;
    std::cout << "sum(1.1, 2.2, 3.3, 4.4, 5.5) = " << sum_(1.1,2.2,3.3,4.4,5.5) << std::endl;
    return 0;
};

