#ifndef __DERIVEDPOINT__H
#define __DERIVEDPOINT__H

#include "BasePoint.h"
#include <string>

class DerivedPoint : public BasePoint {
    private:
        std::string class_;
    
    public:
    DerivedPoint() : BasePoint(), class_("NULL") {};
    DerivedPoint(double x_, double y_, std::string c_) : BasePoint(x_,y_), class_(c_) {};

        DerivedPoint& operator+=(const DerivedPoint& dp) override {
            this->x += dp.x;
            this->y += dp.y;
            return *this;
        };

        BasePoint operator+(const BasePoint& bp) override {
            BasePoint result = *this;
            result += bp;
            return result;
        };

        BasePoint& operator+=(const Arithmetic auto t) override {
            this->x += t;
            this->y += t;

            return *this;
        };

        BasePoint operator+(const Arithmetic auto t) override {
            BasePoint result = *this;
            result += t;
            return result;
        };
}

#endif