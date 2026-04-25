#ifndef __BASE__H
#define __BASE__H

#include <type_traits>
#include <concepts>

template <typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

class Base {
    protected:
        double x,y;
    public:
        Base() : x(0), y(0) {};
        Base(double x_, double y_) : x(x_), y(y_) {};
        Base(const Base& other) : x(other.x), y(other.y) {};

        friend Base operator+(const int t, Base& p) {
            Base result;
            result.x = p.x + t;
            result.y = p.y + t;
            return result;
        };
};
#endif