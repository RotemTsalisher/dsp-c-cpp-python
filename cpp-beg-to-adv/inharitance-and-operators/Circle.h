#ifndef __CIRCLE__H
#define __CIRCLE__H

#include "Shape.h"

#define PI 3.14

class Circle : public Shape {
    private:
        double area;
    
    public:
        Circle(double diamater_ = 1.0);
        bool operator==(const Circle& other) const;
};

#endif