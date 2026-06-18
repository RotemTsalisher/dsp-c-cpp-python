#include <iostream>
#include "Vector2D.h"

Vector2D::Vector2D(double x_, double y_) : x(x_), y(y_) {
    std::cout << "Creating a new Vector2D object" << std::endl;
};
Vector2D Vector2D::operator+(const Vector2D other) {
    std::cout << "Operator +" << std::endl;
    return Vector2D(this->x + other.x, this->y + other.y);
};