#include "Derived.h"

void Derived::setup() {
    this->val = 200;
    std::cout << "Dervied::setup() : val = " << val << std::endl;
};

Derived::Derived() : val(0) {
    std::cout << "Derived::Derived() : " << std::endl;
    this->setup();
};

Derived::~Derived() {
    std::cout << "Derived::~Derived" << std::endl;
    this->setup();
};