#include "Derived.h"

class DoubleDerived: public Derived {
    public:
        void greet() override {
            std::cout << "DoubleDerived::greet(): Hello From Double Derived!" << std::endl;
        };
};
