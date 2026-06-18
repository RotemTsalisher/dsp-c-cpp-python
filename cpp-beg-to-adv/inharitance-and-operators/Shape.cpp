#include "Shape.h"

Shape::Shape(double diamater_) : diamater(diamater_) {};

bool Shape::operator==(const Shape& other) const {
    std::cout << "Shape::operatpr==" << std::endl;
    return (this->diamater == other.diamater);
};