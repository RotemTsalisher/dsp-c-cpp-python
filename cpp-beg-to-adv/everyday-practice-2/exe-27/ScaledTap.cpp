#include "ScaledTap.h"

ScaledTap::ScaledTap() : tapIndex_(0), ringSample_(0.0) {};
ScaledTap::ScaledTap(int const tapIndex, double const& ringSample) : tapIndex_(tapIndex), ringSample_(ringSample) {};
ScaledTap::ScaledTap(const ScaledTap& other) : tapIndex_(other.tapIndex_), ringSample_(other.ringSample_) {};

double ScaledTap::value() const {
    return this->ringSample_;
};