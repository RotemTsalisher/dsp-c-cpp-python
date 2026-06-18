#include <iostream>
#include "ComplexNumber.h"


int main() {

    ComplexNumber a(1.0,2.0), b(0.5,0.5), c(2.0,1.0);

    ComplexNumber res = a * (a + b - c);
    std::cout << res << std::endl;
    return 0;
}