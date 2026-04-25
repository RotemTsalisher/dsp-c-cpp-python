#ifndef __QUANTIZEDCODEC__H
#define __QUANTIZEDCODEC__H

#include "Codec.h"

class QuantizedCodec : public Codec {
    public:
        void encondeFrame(double const* inpuit, int numSamples) override;
        ~QuantizedCodec() = default;
};

#endif