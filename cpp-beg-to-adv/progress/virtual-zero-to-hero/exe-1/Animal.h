#ifndef __ANIMAL__H
#define __ANIMAL__H

#include <iostream>

class Animal {
    public:
        virtual void sound() const;

        virtual ~Animal();
};

#endif