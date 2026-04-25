#include "Processor.h"

double Processor::tick(double x) {
    std::cout << "processor tick!" << std::endl;
    return (x + 2.0);
};
Processor::~Processor() {
    std::cout << "Processor Destructor!" << std::endl;
};