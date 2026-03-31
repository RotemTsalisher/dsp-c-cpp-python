#include "Rectangle.h"

Rectangle::Rectangle() : width(0), height(0) {
    std::cout << "Empty Constructor" << std::endl;
};

Rectangle::Rectangle(float width_, float height_) : width(width_), height(height_) {
    std::cout << "Parametric Constructor" << std::endl;
};

Rectangle& Rectangle::set_width(float width_) {
    width = width_;
    return *this;
};

Rectangle& Rectangle::set_height(float height_) {
    height = height_;
    return *this;
};

float Rectangle::area() const {
    return height * width;
};

