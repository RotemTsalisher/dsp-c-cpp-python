#include "SineSource.h"

double SineSource::next() const {
    return 1.0;
};

SineSource::~SineSource() {
    std::cout << "Sine Source Destructor!" << std::endl;
};