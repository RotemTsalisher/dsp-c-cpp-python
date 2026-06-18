#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    public:
        virtual double binWeight(int k, bool normalized = true) const;
        virtual ~Base() = default;
};

#endif