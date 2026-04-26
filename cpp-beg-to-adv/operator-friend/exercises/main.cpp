#include <iostream>
#include "Vec2.h"

int main() {
    Vec2 v0{1.0, 1.0}, v2{1.0, 1.0};
    std::cout << "res = " << (3 + v0 + 2) << std::endl;
    std::cout << "res = " << (2 * v0) << std::endl;
    std::cout << "res = " << (v2 * v0) << std::endl;

    if(v0 == v2) {
        std::cout << "v0 == v2!" << std::endl;
    }
    return 0;
};