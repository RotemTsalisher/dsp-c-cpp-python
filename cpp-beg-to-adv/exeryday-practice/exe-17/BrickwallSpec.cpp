#include "BrickwallSpec.h"

BrickwallSpec::BrickwallSpec() {
    this->cutoffHz_= 20000.0;
};

BrickwallSpec::BrickwallSpec(double fc_) {
    this->cutoffHz_ = fc_;
};

double BrickwallSpec::get_fc() const {
    return this->cutoffHz_;
};