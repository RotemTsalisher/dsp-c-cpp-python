#include "PCMCodec.h"

void PCMCodec::encondeFrame(double const* input, int numSamples) {
    std::cout << "[";
    for(int i = 0; i <numSamples - 1; i++) {
        std::cout << input[i] << ", ";
    };
    std::cout << input[numSamples - 1] << "]" << std::endl;
};