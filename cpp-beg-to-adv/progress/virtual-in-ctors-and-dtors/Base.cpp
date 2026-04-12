#include "Base.h"

Base::Base() : val(0) {
    std::cout << "Base::Base() : " << std::endl;
    this->setup();
};

void Base::setup() {
    this->val = 100;
    std::cout << "Base::setup() : val = " << val << std::endl;
};

Base::~Base() {
    std::cout <<"Base::~Base()" << std::endl;
    this->setup();
};