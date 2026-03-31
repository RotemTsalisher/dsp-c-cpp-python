#include "Accumulator.h"
#include <iostream>

Accumulator::Accumulator() : value(0) {
    std::cout << "Empty Constructor" << std::endl;
};

Accumulator::Accumulator(double value_) : value(value_) {
    std::cout << "Parametric Constructor" << std::endl;
};

Accumulator::Accumulator(const Accumulator& acc) : value(acc.value) {
    std::cout << "Copy Constructor" << std::endl;
};

Accumulator& Accumulator::add(double x) {
    value += x;
    return *this;
};

Accumulator& Accumulator::multiply(double x) {
    value *= x;
    return *this;
};

double Accumulator::get_value() {return value;};