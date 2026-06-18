#include <iostream>
#include "Vector2D.h"


int main() {
    Vector2D a(1.0,2.0);
    Vector2D b(0.5,0.5);

    Vector2D c;
    c += (a + b);

    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "c = " << c << std::endl;
    return 0;
}