#include "Vector2D.h"

Vector2D::Vector2D(double x_, double y_) : x(x_), y(y_) {
    std::cout << "Creating New Vector2D Object" << std::endl;
};

Vector2D Vector2D::operator*(const int t) const {
    return Vector2D(this->x * t, this->y * t);
};

Vector2D operator*(const int t, const Vector2D& v) {
    return v * t;
};

std::ostream& operator<<(std::ostream& os, const Vector2D& v) {
    os << "vector : (" << v.x << "," << v.y << ")";
    return os;
};