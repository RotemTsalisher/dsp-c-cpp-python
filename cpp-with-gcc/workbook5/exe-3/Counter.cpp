#include "Counter.h"

Counter::Counter() : value(0) {
    std::cout << "Empty Constructor" << std::endl;
};

Counter::Counter(int value_) : value(value_) {
    std::cout << "Parametric Constructor" << std::endl;
};

Counter::Counter(const Counter& counter_) : value(counter_.value) {
    std::cout << "Copy Constructor" << std::endl;
};

void Counter::increment() {
    value++;
};

void Counter::increment(int x) {
    value += x;
};

int Counter::get_value() {
    return value;
};

Counter::~Counter(){
    std::cout << "Destructing Counter with value = " << value << std::endl;
};