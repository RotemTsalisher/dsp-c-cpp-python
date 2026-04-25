#include <iostream>
#include "Processor.h"
#include "FirKernel.h"

int main(){
    Processor processor;
    FirKernel fir_kernel;

    double x = 1.25;

    std::cout << "Processor::tick(1.25) = " << processor.tick(x) << std::endl;
    std::cout << "FirKernel::tick(1.25) = " << fir_kernel.tick(x) << std::endl;
    return 0;

};