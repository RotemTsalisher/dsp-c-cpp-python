#include "WatermarkedFrame.h"
#include <iostream>

int main()
{
    WatermarkedFrame w1;
    WatermarkedFrame w2(5, 10);
    WatermarkedFrame w3(w2);

    std::cout << w1 << std::endl;
    std::cout << w2 << std::endl;
    std::cout << w3 << std::endl;

    return 0;
}