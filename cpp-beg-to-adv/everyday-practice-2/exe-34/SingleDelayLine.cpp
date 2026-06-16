#include "SingleDelayLine.h"

SingleDelayLine::SingleDelayLine() : tapCounts(0) {};
SingleDelayLine::SingleDelayLine(int n) : tapCounts(n) {std::cout << "Param Ctor Called" << std::endl;};
SingleDelayLine& SingleDelayLine::operator=(int n) {
    std::cout << "Operator = called" << std::endl;
    this->tapCounts = n;
    return *this;
};