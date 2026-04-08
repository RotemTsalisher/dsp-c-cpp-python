#include "Circle.h"
#include <iostream>

int main() {
    Circle c0;
    Circle c1(2.5);

    std::cout << "c0 area : " << c0.area() << std::endl;
    std::cout << "c1 area : " << c1.area() << std::endl;
};