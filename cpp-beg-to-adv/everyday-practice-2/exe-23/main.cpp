#include <iostream>

struct BinPower {
    int k;
    double psd;
};

double toneToNoise(struct BinPower peak, struct BinPower floorBin) {
    return (floorBin.psd > 0) ? (peak.psd / floorBin.psd) : 0;
}

int main() {
    BinPower peak{42, 100.0};
    BinPower floorBin{17, 5.0};

    double tnr = toneToNoise(peak, floorBin);

    std::cout << "Peak bin:  k = " << peak.k
              << ", PSD = " << peak.psd << '\n';

    std::cout << "Floor bin: k = " << floorBin.k
              << ", PSD = " << floorBin.psd << '\n';

    std::cout << "Tone-to-noise ratio = " << tnr << '\n';

    // Test divide-by-zero protection
    BinPower zeroFloor{18, 0.0};

    std::cout << "Tone-to-noise ratio with zero floor PSD = "
              << toneToNoise(peak, zeroFloor) << '\n';

    return 0;
}