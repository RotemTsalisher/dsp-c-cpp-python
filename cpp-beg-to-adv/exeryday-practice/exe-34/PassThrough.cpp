#include "PassThrough.h"

double PassThrough::tick(double x) {
    std::cout << " PASS THROUGH ! tick!" << std::endl;
    return (x + 1.0);
};

PassThrough::~PassThrough() {
    std::cout << "PassThrough Destructor!" << std::endl;
};