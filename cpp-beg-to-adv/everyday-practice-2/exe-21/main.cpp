#include <iostream>
#include "AlignedFFTScratch.h"

int main()
{
    AlignedFFTScratch scratch1;
    std::cout << scratch1 << std::endl;

    AlignedFFTScratch scratch2(1024);
    std::cout << scratch2 << std::endl;

    return 0;
}