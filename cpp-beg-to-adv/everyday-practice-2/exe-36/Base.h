#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    public:
        virtual void tune(double hz);
        virtual ~Base() = default;
};

#endif 