#ifndef __SHAPE__H
#define __SHAPE__H

#include <iostream>

class Shape {
    protected:
        double diamater;
    
    public:
        Shape(double diamater_ = 1.0);
        bool operator==(const Shape& other) const;
};

#endif