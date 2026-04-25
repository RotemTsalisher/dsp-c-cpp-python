#include <iostream>
#include "ScaledRef.h"

int main() {
    ScaledRef sr0;
    ScaledRef sr1(1.0, 2.0);

    std::cout << "sr0 = " << sr0.get_scale() << ", " << sr0.get_ref() << std::endl;
    std::cout << "sr1 = " << sr1.get_scale() << ", " << sr1.get_ref() << std::endl;
    return 0;
    
}