#ifndef __CODEC__H
#define __CODEC__H

#include <iostream>

class Codec {
    public:
        virtual void encondeFrame(double const* inpuit, int numSamples) = 0;
        virtual ~Codec() = default;

    protected:
        Codec() = default;
    
};

#endif