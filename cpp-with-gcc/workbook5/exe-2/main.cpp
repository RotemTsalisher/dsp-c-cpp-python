#include <iostream>
#include "Rectangle.h"

int main() {

    Rectangle rect0;
    Rectangle rect1(1.5, 2.5);
    
    std::cout << rect0 << std::endl;
    rect0.set_height(1.0).set_width(2.0);

    std::cout << rect0 << std::endl;
    std::cout << rect1 << std::endl;
    return 0;
}