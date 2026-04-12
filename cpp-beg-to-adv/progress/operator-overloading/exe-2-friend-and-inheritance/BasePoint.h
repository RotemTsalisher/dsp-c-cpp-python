#ifndef __BASEPOINT__H
#define __BASEPOINT__H

class BasePoint {
    private:
        double x,y;
    public:
        BasePoint() : x(0.0), y(0.0) {};
        BasePoint(double x_, double y_) : x(x_), y(y_) {};
        BasePoint(const BasePoint& bp) : x(bp.x), y(bp.y) {};

        BasePoint& operator+=(const BasePoint& bp) {
            this->x += bp.x;
            this->y += bp.y;
            return *this;
        };
        
        BasePoint operator+(const BasePoint& bp) {
            BasePoint result = *this;
            result += bp;
            return result;
        };

};
#endif