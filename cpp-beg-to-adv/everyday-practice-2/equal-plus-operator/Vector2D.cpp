#include "Vector2D.h"

Vector2D::Vector2D(double x_, double y_) : x(x_), y(y_) {};
Vector2D& Vector2D::operator+=(const Vector2D& other) {
    std::cout << "OPERATOR +=" << std::endl;
    this->x += other.x;
    this->y += other.y;

    return *this;
};

Vector2D Vector2D::operator+(const Vector2D& other) const {
    std::cout << "OPERATOR +" << std::endl;
    Vector2D res(this->x, this->y);
    return res += other;
};

std::ostream& operator<<(std::ostream& os, const Vector2D& v) {
    os << "<" << v.x << "," << v.y << ">";
    return os;
};