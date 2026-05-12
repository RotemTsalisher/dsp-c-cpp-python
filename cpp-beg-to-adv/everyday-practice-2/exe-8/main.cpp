#include <iostream>
#include "fft_vec.h"

using WindowFn = double (*)(int, int);

double binFFTVal(int bin, int fftsize) {
    if (bin < fftsize) {
        return fft_vec[bin];
    };
    return 0;
};

double binEnergy(int bin, int fftsize, WindowFn fn) {
    return fn(bin, fftsize) * fn(bin, fftsize);
};

int main() {

    for (int k = 0; k < 20; ++k) {
        std::cout << "Bin " << k
                  << " | FFT = " << binFFTVal(k, FFTSIZE)
                  << " | Energy = " << binEnergy(k, FFTSIZE, binFFTVal)
                  << '\n';
    }

    return 0;
}
 
