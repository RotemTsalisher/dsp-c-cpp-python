#include <iostream>
#include "MyVector.h"

int main() {
    double x[] = {1, 2, 3};
    double y[] = {4, 5, 6};

    MyVector v1(x, 3);
    MyVector v2(y, 3);

    std::cout << "v1:\n" << v1 << '\n';
    std::cout << "v2:\n" << v2 << '\n';

    std::cout << "v1 · v2 = " << v1.dot(v2) << '\n';

    return 0;
}