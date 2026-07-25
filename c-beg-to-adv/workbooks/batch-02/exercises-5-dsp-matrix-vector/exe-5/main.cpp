#include <iostream>
#include "MyVector.h"

int main() {
    double x[] = {3.0, 4.0};

    MyVector v(x, 2);

    std::cout << "Original:\n" << v << '\n';

    double n = v.norm2();
    std::cout << "Norm = " << n << '\n';

    v *= 2;
    std::cout << "\nAfter *= 2:\n" << v << '\n';

    v.normalize(v.norm2());
    std::cout << "\nAfter normalization:\n" << v << '\n';

    std::cout << "Norm = " << v.norm2() << '\n';

    return 0;
}