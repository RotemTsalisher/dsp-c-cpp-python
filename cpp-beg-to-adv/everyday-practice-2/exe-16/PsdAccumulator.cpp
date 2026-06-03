#include "PsdAccumulator.h"

void PsdAccumulator::push(double x) {
    sumSq_ += (x * x);
};

double PsdAccumulator::get_sumSq() const {
    return this->sumSq_;
};