#ifndef __DERIVED__H
#define __DERIVED__H

#include "Base.h"

class Derived : public Base {
    public:
        double eval(double x, bool norm = false) const override {
                if(norm) {
                    std::cout << "x = " << x << std::endl;
                    return 1.0;
                }
                else {
                    std::cout << "FALSE !" << std::endl;
                    return -1.0;
                }
        };
};

#endif