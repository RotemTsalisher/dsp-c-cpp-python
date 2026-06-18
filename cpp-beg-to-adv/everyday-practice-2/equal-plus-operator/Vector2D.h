#ifndef __VECTOR2D__H
#define __VECTOR2D__H

#include <iostream>

class Vector2D {
    private:
        double x,y;

    public:
        Vector2D(double x_ = 0.0, double y_ = 0.0);
        Vector2D& operator+=(const Vector2D& other);
        Vector2D operator+(const Vector2D& other) const;

        friend std::ostream& operator<<(std::ostream& os, const Vector2D& v);
};

#endif