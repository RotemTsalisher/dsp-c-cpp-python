#include <iostream>
#include "Vector2D.h"

int main() {
    Vector2D a(1.6, 2.5), b(1.3, 2.5);

    std::cout << "a == b : " << (a == b) << std::endl;
    std::cout << "a != b : " << (a != b) << std::endl;
    
    return 0;
};