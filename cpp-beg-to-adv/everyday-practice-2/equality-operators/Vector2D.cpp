#include "Vector2D.h"

Vector2D::Vector2D(double x_, double y_) : x(x_), y(y_) {};

bool Vector2D::operator==(const Vector2D& other) const {
    return (this->x == other.x && this->y == other.y);
};

bool Vector2D::operator!=(const Vector2D& other) const {
    return !(*this == other);
};