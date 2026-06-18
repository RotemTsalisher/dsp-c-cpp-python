#include "Derived.h"

double Derived::binWeight(int k, bool normalized) const {
    std::cout << "Derived::binWeight(int k, bool normalized)" << std::endl;
    std::cout << "args: k = " << k << " , normalized = " << normalized << std::endl;
    return 2.0;
};