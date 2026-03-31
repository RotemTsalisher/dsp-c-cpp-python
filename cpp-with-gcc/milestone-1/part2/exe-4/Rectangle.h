#include "Shape.h"

class Rectangle : public Shape {
    private:
        double width, height;
    public:
        Rectangle() = default;
        Rectangle(double width_, double height_) : width(width_), height(height_) {};

        void area();
};