#include <iostream>

int combDelaySamples(double delayMs, double sr) {
    return static_cast<int>((delayMs / 1000) * sr);
};

int main() {
    double sr = 48000.0;
    double delayMs = 100.0;

    std::cout << "Delay in samples: " << combDelaySamples(delayMs, sr) << std::endl;
    return 0;
};
