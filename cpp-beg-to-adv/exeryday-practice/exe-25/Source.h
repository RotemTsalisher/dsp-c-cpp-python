#ifndef __SOURCE__H
#define __SOURCE__H

#include <iostream>

class Source {
    public:
        Source() = default;
        virtual double next() const;
        virtual ~Source();
};

#endif