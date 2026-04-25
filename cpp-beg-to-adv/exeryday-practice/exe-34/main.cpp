#include <iostream>
#include "Processor.h"
#include "PassThrough.h"

int main() {

    PassThrough pt;
    double res;

    res = pt.tick(1.25);
    std::cout << "res = " << res << std::endl;
    return 0;
}