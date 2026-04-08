#include "..\exe-5\Shape.h"

class Circle : public Shape {
    private:
        static const double pi;
        double radius;
    public: 
        Circle();
        Circle(double radius_);

        double get_radius() const;
        double area() const override;
};