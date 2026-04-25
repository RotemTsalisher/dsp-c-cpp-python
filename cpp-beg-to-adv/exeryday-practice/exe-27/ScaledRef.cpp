#include "ScaledRef.h"

ScaledRef::ScaledRef() : scale_(0.0), ref_(0.0) {};
ScaledRef::ScaledRef(double scale, double ref) : scale_(scale), ref_(ref) {};

double ScaledRef::get_scale() const {
    return scale_;
};

double ScaledRef::get_ref() const {
    return ref_;
};