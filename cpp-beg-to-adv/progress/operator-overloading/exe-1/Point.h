#ifndef __POINT__H
#define __POINT__H
#include <iostream>
#include <type_traits>
#include <concepts>

template <typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

class Point {
    private:
        double x,y;
    public:
        Point() = default;
        Point(double x_, double y_) : x(x_), y(y_) {};
        Point(const Point& other) : x(other.x), y(other.y) {};

        Point operator+(const Point& p) {
            std::cout << "**operator + **" << std::endl;
            Point result = *this;
            result += p;
            return result;
        };
        Point& operator+=(const Point& p) {
            std::cout << "**operator += **" << std::endl;
            this->x += p.x;
            this->y += p.y;
            return *this;
        };

        Point operator+(Arithmetic auto t) {
            std::cout << "**operator + **" << std::endl;
            Point result = *this;
            result += t;
            return result;
        };
        Point& operator+=(Arithmetic auto t) {
            std::cout << "**operator += **" << std::endl;
            this->x += t;
            this->y += t;
            return *this;
        };

        friend std::ostream& operator<<(std::ostream& os, const Point& p);
        /*
        friend Point operator+(const int& t, const Point& p) {
            return Point(p.x + t, p.y + t);
        };
        friend Point operator+(const double& t, const Point& p) {
            return Point(p.x + t, p.y + t);
        };
        ...
        */
        friend Point operator+(const Arithmetic auto t, const Point& p) {
            return Point(t + p.x, t + p.y);
        };
};
#endif