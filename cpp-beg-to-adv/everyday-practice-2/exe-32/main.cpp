#include <iostream>
#include "Core.h"
#include "PublicCore.h"

int main() {
    PublicCore pc;

    std::cout << "pc.fftOrder = " << pc.fftOrder_ << std::endl;

    pc.fftOrder_ = 1024;

    std::cout << "pc.fftOrder = " << pc.fftOrder_ << std::endl;

    return 0;
};