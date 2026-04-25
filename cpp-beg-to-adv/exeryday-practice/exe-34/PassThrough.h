#ifndef __PASSTHROUGH__H
#define __PASSTHROUGH__H
#include <iostream>
#include "Processor.h"

class PassThrough : public Processor {
    public:
        double tick(double x) override;
        ~PassThrough();
};

#endif