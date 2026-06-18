#ifndef __INTERLEAVEDDESC__H
#define __INTERLEAVEDDESC__H

#include "BufferDesc.h"

class InterleavedDesc : public BufferDesc {
    public:
        int channels() const;
};

#endif