#ifndef SHAPE_H_
#define SHAPE_H_

#include <iostream>
class Shape {

    public:
        virtual void area();
        Shape() = default;
        virtual ~Shape() = default;
};

#endif

