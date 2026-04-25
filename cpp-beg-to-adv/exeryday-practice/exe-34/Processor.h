#ifndef __PROCESSOR__H
#define __PROCESSOR__H

#include <iostream>

class Processor {
    public:
        virtual double tick(double x);
        virtual ~Processor();
};

#endif