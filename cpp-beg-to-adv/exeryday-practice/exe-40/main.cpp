#include <iostream>
#include "Codec.h"
#include "PCMCodec.h"
#include "QuantizedCodec.h"

int main() {
    // Values chosen to test rounding behavior around .5 boundaries
    double frame[] = {0.1, 0.49, 0.5, 0.51, 1.2, 1.5, 1.51};
    int numSamples = 7;

    Codec* codec = nullptr;

    // Test PCMCodec
    codec = new PCMCodec();
    codec->encondeFrame(frame, numSamples);
    delete codec;

    // Test QuantizedCodec
    codec = new QuantizedCodec();
    codec->encondeFrame(frame, numSamples);
    delete codec;

    return 0;
}