#ifndef __DCGENERATOR__H
#define __DCGENERATOR__H

#include "Generator.h"
#include <iostream>

class DcGenerator : public Generator {
    private:
        double offset_;
    public:
        DcGenerator() : Generator(), offset_(0.0) {};
        DcGenerator(double offset) : Generator(), offset_(offset) {};

        double nextSample() const override;
        ~DcGenerator() = default;
};


#endif