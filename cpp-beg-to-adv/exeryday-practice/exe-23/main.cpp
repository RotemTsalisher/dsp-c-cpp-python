#include <iostream>
#include "structs.h"

int main() {
    ComplexSample cs0, cs1;

    ComplexSampleInit(&cs0);
    ComplexSampleInit(&cs1, std::sqrt(2) / 2, std::sqrt(2) / 2);

    std::cout << "cs0 magnitude = " << cs0.mag(&cs0) << std::endl;
    std::cout << "cs1 magnitude = " << cs1.mag(&cs1) << std::endl;

    return 0;
};