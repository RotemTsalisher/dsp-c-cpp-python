#include <iostream>
#include "Point.h"

int main() {
    Point p0;
    Point p1(2,3);

    std::cout << "Points:" << std::endl;
    std::cout << p0 << " || " << p1 << std::endl;

    /*
    p0 = p0 + p1;
    p1 = p1 + 1.5;

    std::cout << "Points:" << std::endl;
    std::cout << p0 << " || " << p1 << std::endl;

    p1 = p1 + 1;

    std::cout << "Points:" << std::endl;
    std::cout << p0 << " || " << p1 << std::endl;
    */

    p0 = Point(1,1) + p1;
    std::cout << "p0 = " << p0 << std::endl;
    p0 += p1;

    std::cout << "p0 = " << p0 << std::endl;

    p1 += 1;
    p1 = p1 + 1;

    std::cout << "Points:" << std::endl;
    std::cout << p0 << " || " << p1 << std::endl;

    return 0;
};