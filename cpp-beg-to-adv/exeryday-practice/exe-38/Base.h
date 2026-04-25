#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    public:
        virtual double eval(double x, bool norm = true) const {
            if(norm) {
                std::cout << "x = " << x << std::endl;
                return 1.0;
            }
            else {
                std::cout << "FALSE !" << std::endl;
                return -1.0;
            }
        }
};

#endif