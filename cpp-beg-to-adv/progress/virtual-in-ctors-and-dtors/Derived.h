#ifndef __DERIVED__H
#define __DERIVED__H
#include "Base.h"
#include <iostream>

class Derived : public Base {
    private:
        int val;
    public:
        Derived();
        void setup() override;
        ~Derived();
        //void cleanup() override;

};
#endif