#include "Shape.h"

const double PI = 3.14159;
class Circle : public Shape {
    private:
        double r;

    public:
        Circle() = default;
        Circle(double r_) : r(r_) {};
        void area();
};