#include "Source.h"

double Source::next() const {
    return 0;
};

Source::~Source() {
    std::cout << "Source Destructor!" << std::endl;
};