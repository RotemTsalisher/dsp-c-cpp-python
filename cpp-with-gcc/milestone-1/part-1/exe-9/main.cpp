#include <iostream>

constexpr int factorial_(int n) {
    int res = 1;
    for(size_t i = n; i > 1; res*=i, i--);
    return res;
};

int main() {
    static_assert(factorial_(5) == 120, "Math is Broke!");
    static_assert(factorial_(4) == 24, "Math is Broke!");

    std::cout << "DONE!" << std::endl;
};