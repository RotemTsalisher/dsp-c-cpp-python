#include "Base.h"

int Base::counter = 0;

Base::Base() {
    std::cout << "Base Empty Constructor!" << std::endl;
    Base::counter++;
};

int Base::get_counter() const {
    return counter;
};