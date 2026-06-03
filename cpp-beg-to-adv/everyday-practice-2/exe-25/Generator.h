#ifndef __GENERATOR__H
#define __GENERATOR__H

#include <iostream>

class Generator {
    public:
        virtual double nextSample() const;
        virtual ~Generator() = default;
};

#endif