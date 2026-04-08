#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    protected:
        void foo() {
            std::cout << "Base class say Hello!" << std::endl;
        };
};

#endif