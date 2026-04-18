#include <iostream>

using GainFn = double (*)(double, double);

double gain(double x, double g) {

    return g * x;
};

double mapSample(double x, double g, GainFn fn) {
    return fn(x,g);
};


int main() {
    
    GainFn gain_ptr = gain;
    
    constexpr int N = 3;
    double x_[N] = {1.0, 1.5, 2.0};
    double g_[N] = {1.0, 2.0, 3.0};

    for(size_t i = 0; i< N; i++) {
        std::cout << "x[" << i << "] = " << x_[i] << " || " << "g[" << i << "] = " << g_[i] <<" || " << "g[" << i << "] * x[" << i << "] = " << mapSample(x_[i], g_[i], gain_ptr) << std::endl;
    }
    return 0;
};