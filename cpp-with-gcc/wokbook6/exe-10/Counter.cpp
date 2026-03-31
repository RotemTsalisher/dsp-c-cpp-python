#include "Counter.h"

Counter::Counter() : value(0) {
    std::cout << "Empty Constructor" << std::endl;
};

Counter::Counter(int value_) : value(value_) {
    std::cout << "Parametric Constructor" << std::endl;
};

Counter::Counter(const Counter& c) : value(c.value) {
    std::cout << "Copy Constructor" << std::endl;
};

Counter& Counter::set_value(int value_) {
    value = value_;
    return *this;
};

Counter& Counter::increment(int x) {
    value += x;
    return *this;
};

Counter& Counter::increment() {
    value ++;
    return *this;
};

int Counter::get_value(){
    return value;
};