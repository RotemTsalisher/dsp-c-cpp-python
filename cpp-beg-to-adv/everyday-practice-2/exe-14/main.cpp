#include <iostream>
#include <concepts>
#include <type_traits>

static double sum = 0;

template <typename T>
concept Floating = std::is_floating_point_v<T>;

void accumulatePsd(Floating auto pwr, double& sum) {
    sum += pwr;
};

int main() {
    double totalSum = 0.0;

    // Test Case 1: passing a double
    double initialPower = 10.5;
    accumulatePsd(initialPower, totalSum);
    std::cout << "After adding double (10.5): " << totalSum << " (Expected: 10.5)\n";

    // Test Case 2: passing a float
    float nextPower = 4.5f;
    accumulatePsd(nextPower, totalSum);
    std::cout << "After adding float  (4.5):  " << totalSum << " (Expected: 15.0)\n";

    // Note: Trying to pass an integer like accumulatePsd(5, totalSum) 
    // will fail to compile because int does not satisfy the 'Floating' concept.

    return 0;
}