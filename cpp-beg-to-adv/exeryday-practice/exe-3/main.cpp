#include <iostream>

template <typename T>
T clamp_abs(T value, T limit) {
    if(value > limit) {
        return limit;
    }
    else if(value < limit) {
        return limit;
    }
    return value;
};

int main() {
    int limit = 10;

    int value = 3;
    std::cout << "value = " << value << ", limit = " << limit << "|| returned value = " << clamp_abs(value, limit) << std::endl;

    value = 12;
    std::cout << "value = " << value << ", limit = " << limit << "|| returned value = " << clamp_abs(value, limit) << std::endl;

    double limit_ = 2.3;

    double value_ = 1.2;
    std::cout << "value = " << value_ << ", limit = " << limit_ << "|| returned value = " << clamp_abs(value_, limit_) << std::endl;

    value_ = 2.5;
    std::cout << "value = " << value_ << ", limit = " << limit_ << "|| returned value = " << clamp_abs(value_, limit_) << std::endl;
    
    return 0;
};
