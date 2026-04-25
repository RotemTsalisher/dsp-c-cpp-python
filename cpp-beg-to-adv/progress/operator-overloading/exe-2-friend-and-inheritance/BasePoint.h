#ifndef __BASEPOINT__H
#define __BASEPOINT__H

#include <concepts>
#include <type_traits>

template <typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

class BasePoint {
    protected:
        double x,y;
    public:
        BasePoint() : x(0.0), y(0.0) {};
        BasePoint(double x_, double y_) : x(x_), y(y_) {};
        BasePoint(const BasePoint& bp) : x(bp.x), y(bp.y) {};

        virtual BasePoint& operator+=(const BasePoint& bp) {
            this->x += bp.x;
            this->y += bp.y;
            return *this;
        };

        virtual BasePoint operator+(const BasePoint& bp) {
            BasePoint result = *this;
            result += bp;
            return result;
        };

        virtual BasePoint& operator+=(const Arithmetic auto t) {
            this->x += t;
            this->y += t;

            return *this;
        };

        virtual BasePoint operator+(const Arithmetic auto t) {
            BasePoint result = *this;
            result += t;
            return result;
        };

};
#endif