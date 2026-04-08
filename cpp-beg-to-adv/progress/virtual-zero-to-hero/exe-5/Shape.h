#ifndef __SHAPE__H
#define __SHAPE__H

class Shape {
    public:
        Shape() = default;
        virtual double area() const = 0;
};

#endif