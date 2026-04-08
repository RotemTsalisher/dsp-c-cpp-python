#ifndef __BASE__H
#define __BASE__H

#include <iostream>

class Base {
    public:
        virtual void greet() {
            std::cout << "Base::greet(): Hello From Base!" << std::endl;
        };
};

#endif