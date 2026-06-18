#include "Circle.h"

Circle::Circle(double diamater_) : Shape(diamater_) {
    this->area = this->diamater * this->diamater * PI;
};

bool Circle::operator==(const Circle& other) const {
    std::cout << "Circle::operator==" << std::endl;
    return (other.Shape::operator==(other) && (this->area == other.area));
};