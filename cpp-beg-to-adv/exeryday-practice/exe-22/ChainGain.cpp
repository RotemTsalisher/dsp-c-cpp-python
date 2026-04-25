#include "ChainGain.h"

ChainGain::ChainGain() : g_(1.0) {};
ChainGain::ChainGain(double g) : g_(g) {};

ChainGain& ChainGain::mul(double m) {
    g_ *= m;
    return *this;
};

ChainGain& ChainGain::reset() {
    g_ = 1.0;
    return *this;
};

ChainGain& ChainGain::print_gain() {
    std::cout << "gain = " << this->g_ << std::endl;
    return *this;
};

double ChainGain::get_gain() const {
    return this->g_;
};