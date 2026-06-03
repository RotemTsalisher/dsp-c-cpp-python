#include <iostream>
#include "DcGenerator.h"

int main() {
    DcGenerator dc1;
    DcGenerator dc2(2.5);

    std::cout << "dc1: " << dc1.nextSample() << std::endl;
    std::cout << "dc2: " << dc2.nextSample() << std::endl;

    return 0;
}