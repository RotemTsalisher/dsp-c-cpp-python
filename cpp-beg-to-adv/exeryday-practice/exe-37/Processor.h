#ifndef __PROCESSOR__H
#define __PROCESSOR__H

#include <iostream>

class Processor {
    public:
        virtual double tick(double x) const;
        virtual ~Processor() = default;
};

#endif
