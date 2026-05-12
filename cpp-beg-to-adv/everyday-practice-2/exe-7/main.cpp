#include <iostream>

using WindowFn = double (*)(int binIndex, int fftSize);
double rectangularWindow(int k, int n) {
    if (k >= 0 && k < n) {
        return 1;
    };
    return 0;
};

int main() {

    WindowFn fp = rectangularWindow;

    std::cout << "fp(200, 256) = " << fp(200, 256) << std::endl <<
    "fp(1025, 1024) = " << fp(1025, 1024) << std::endl;
    return 0;
};