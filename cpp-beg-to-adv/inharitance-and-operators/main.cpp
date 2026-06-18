#include <iostream>
#include "Shape.h"
#include "Circle.h"


int main() {
    Circle circle1, circle2(2.0);

    std::cout << "circle1 == circle2 : " << (circle1 == circle2) << std::endl;

    return 0;
};