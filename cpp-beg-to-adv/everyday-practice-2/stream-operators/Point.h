#ifndef __POINT__H
#define __POINT__H

#include <iostream>

class Point {
    private:
        double x,y;
    
    public:
        Point(double x_ = 0.0, double y_ = 0.0);
        friend std::ostream& operator<<(std::ostream& os, const Point& p);
        friend std::istream& operator>>(std::istream& is, Point& p);
};

#endif