#ifndef __VEC2__H
#define __VEC2__H

#include <iostream>


class Vec2 {
    private:
        double x, y;
    
    public:
        Vec2() = default;
        Vec2(double x_, double y_) : x(x_), y(y_) {};
        Vec2& operator+=(const int s) {
            this->x += s;
            this->y += s;
            return *this;
        };

        Vec2 operator+(int s) {
            Vec2 res = *this;
            res += s;
            return res;
        };

        friend Vec2 operator+(const int& x, const Vec2& other) {
            Vec2 res = other;
            return res + x;
        };

        friend std::ostream& operator<<(std::ostream& os, const Vec2& v) {
            os << "(" << v.x << ", " << v.y << ")";
            return os;
        };

        friend bool operator==(const Vec2& v1, const Vec2& v2) {
            return ((v1.x == v2.x) && (v1.y == v2.y));
        };

        Vec2& operator-=(int s) {
            this->x -= s;
            this->y -= s;
            return *this;
        };

        Vec2 operator-(const int& s) {
            Vec2 res = *this;
            res -= s;
            return res;
        };

        friend Vec2 operator-(const int& s, Vec2& v) {
            return (v - s);
        };

        Vec2& operator*=(const int& s) {
            this->x *= s;
            this->y *= s;
            return *this;
        };

        Vec2 operator*(const int& s) {
            Vec2 res = *this;
            res *= s;
            return res;
        };

        friend Vec2 operator*(const int& s, Vec2& v) {
            return (v * s);
        };

        friend double operator*(const Vec2& v1, const Vec2& v2) {
            return (v1.x * v2.x + v1.y * v2.y);
        };

        
};

#endif