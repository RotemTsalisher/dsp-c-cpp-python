#ifndef __DERIVED__H
#define __DERIVED__H
#include "Base.h"

class Derived : public Base {
    public:
        void greet() override {
            std::cout << "Derived::greet(): Hello From Derived!" << std::endl;
        };
};

#endif