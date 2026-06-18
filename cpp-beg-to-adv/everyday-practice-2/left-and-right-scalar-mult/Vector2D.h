#ifndef __VECTOR2D__H
#define __VECTOR2D__H

#include <iostream>

class Vector2D {
    private:
        double x,y;

    public:
        Vector2D(double x_ = 0.0, double y = 0.0);
        Vector2D operator*(const int t) const;
        friend Vector2D operator*(const int t, const Vector2D& v);
        friend std::ostream& operator<<(std::ostream& os, const Vector2D& v);
};

#endif