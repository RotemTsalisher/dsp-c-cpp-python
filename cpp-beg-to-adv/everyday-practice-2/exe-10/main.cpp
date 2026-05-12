#include <iostream>


constexpr size_t combLineCapacity(int maxDelaySamples, int channels) {
    return static_cast<size_t>(maxDelaySamples) * static_cast<size_t>(channels);
};

int main() {
    static_assert(combLineCapacity(2048,2) == 4096, "math is broke!");

    std::cout << "BYE BYE!" << std::endl;
    return 0;
}