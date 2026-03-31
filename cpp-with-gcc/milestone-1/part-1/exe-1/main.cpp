#include <iostream>

template <typename T>
T square(T x) {
    return x * x;
};

int main() {
    
    std::cout << "5 * 5 = " << square(5) << std::endl;
    std::cout << "1.5 * 1.5 = " << square(1.5) << std::endl;
    return 0;
};