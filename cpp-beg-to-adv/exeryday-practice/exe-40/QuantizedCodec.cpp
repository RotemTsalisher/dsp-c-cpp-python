#include "QuantizedCodec.h"

void QuantizedCodec::encondeFrame(double const* input, int numSamples) {
    std::cout << "[";
    for(int i = 0; i<numSamples - 1; i++){
        std::cout << int(input[i] + 0.5) << ", ";
    };
    std::cout << int(input[numSamples - 1] + 0.5);
    std::cout << "]" << std::endl;
};