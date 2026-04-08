#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    public:
        virtual void speak() const;
        virtual void dance() const;
};
#endif