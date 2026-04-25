#ifndef __PCMCODEC__H
#define __PCMCODEC__H

#include "Codec.h"

class PCMCodec : public Codec {
    public:
        void encondeFrame(double const* inpuit, int numSamples) override;
        ~PCMCodec() = default;
};
#endif