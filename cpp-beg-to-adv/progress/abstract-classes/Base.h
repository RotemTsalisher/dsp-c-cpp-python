#ifndef __BASE__H
#define __BASE__H

#include <iostream>
#include <string>

class Base {
    public:
        virtual void speak() const = 0; // pure virtual
};
#endif