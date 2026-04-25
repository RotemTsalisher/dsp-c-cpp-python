#include <iostream>

constexpr int fftBint(int order) {
    return (1 << order);
};

int main() {
    
    static_assert(fftBint(5) == 32, "Math is broke!");
    //static_assert(fftBint(3) == 7, "Math is broke!");
    return 0;
};
