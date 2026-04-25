#include "FilterSetup.h"

FilterSetup::FilterSetup() : order(0), ripple(1.0) {};
FilterSetup::FilterSetup(int order_, double ripple_) : order(order_), ripple(ripple_) {};

FilterSetup& FilterSetup::setOrder(int order_) {
    order = order_;
    return *this;
};

FilterSetup& FilterSetup::setRipple(double ripple_) {
    ripple = ripple_;
    return *this;
};

int FilterSetup::getOrder() const {return order;};
double FilterSetup::getRipple() const {return ripple;};


