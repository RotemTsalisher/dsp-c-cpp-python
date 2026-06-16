#include "CalibratedBank.h"

CalibratedBank::CalibratedBank() : CoeffBank() {};
CalibratedBank::CalibratedBank(double g) : CoeffBank(g) {};

double CalibratedBank::get_gain() const {
    return this->g_;
};