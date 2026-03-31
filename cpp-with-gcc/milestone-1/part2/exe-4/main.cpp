
#include <iostream>
#include "Rectangle.h"
#include "Circle.h"
#include "Shape.h"

int main() {

    Shape *s0 = new Shape();
    Shape *s1 = new Circle(1);
    Shape *s2 = new Rectangle(2,3);

    s0->area();
    s1->area();
    s2->area();

    delete s0;
    delete s1;
    delete s2;
    std::cout << "Bye!" << std::endl;
};