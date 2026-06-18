#ifndef __VECTOR2D__H
#define __VECTOR2D__H

class Vector2D {
    private:
        double x,y;
    public:
        Vector2D(double x_ = 0.0, double y_ = 0.0);
        Vector2D operator+(const Vector2D other);
};

#endif