#include "Circle.h"

const double Circle::pi = 3.141592653589793;

Circle::Circle() : Shape(), radius(1) {};
Circle::Circle(double radius_) : Shape(), radius(radius_) {};

double Circle::get_radius() const {
    return radius;
};

double Circle::area() const {
    return pi * radius * radius;
};