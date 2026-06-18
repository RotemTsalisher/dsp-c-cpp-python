#include <iostream>
#include "Vector2D.h"

int main() {

    Vector2D v0(1.0,2.0);
    Vector2D v1 = 2 * v0;
    Vector2D v2 = v1 * 2;
    
    std::cout << v0 << std::endl << v1 << std::endl << v2 << std::endl;
    return 0;
};