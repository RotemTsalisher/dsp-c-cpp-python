#include "GainStage.h"

double GainStage::gainLinear() const {
    return this->gainLinear_;
};

void GainStage::setGainLinear(double g) {
    this->gainLinear_ = g;
};