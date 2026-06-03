#include <iostream>
#include "PsdAccumulator.h"

int main() {
    // 1. Default constructor (starts at 0.0)
    PsdAccumulator acc1;
    acc1.push(3.0); // 0.0 + 9.0
    std::cout << "acc1 sumSq: " << acc1.get_sumSq() << " (Expected: 9)\n";

    // 2. Parameterized constructor (starts at 10.5)
    PsdAccumulator acc2(10.5);
    acc2.push(2.0); // 10.5 + 4.0
    std::cout << "acc2 sumSq: " << acc2.get_sumSq() << " (Expected: 14.5)\n";

    // 3. Copy constructor
    PsdAccumulator acc3(acc2);
    std::cout << "acc3 sumSq: " << acc3.get_sumSq() << " (Expected: 14.5)\n";

    return 0;
}