#include <iostream>
#include <algorithm> // Optional, but standard if you want std::clamp later

namespace dsp::comb {
    double normalizedCombFeedback(double gRaw, double maxMag) {
        if (gRaw > maxMag) {
            gRaw = maxMag;
        }
        else if (gRaw < -maxMag) {
            gRaw = -maxMag;
        }
        return gRaw;
    }
}

int main() {
    // Test case 1: Inside bounds
    std::cout << "Test 1 (Within bounds): " 
              << dsp::comb::normalizedCombFeedback(2.5, 5.0) << " (Expected: 2.5)\n";

    // Test case 2: Exceeds positive bound
    std::cout << "Test 2 (Exceeds max):   " 
              << dsp::comb::normalizedCombFeedback(7.2, 5.0) << " (Expected: 5)\n";

    // Test case 3: Exceeds negative bound
    std::cout << "Test 3 (Exceeds min):   " 
              << dsp::comb::normalizedCombFeedback(-9.0, 5.0) << " (Expected: -5)\n";

    return 0;
}