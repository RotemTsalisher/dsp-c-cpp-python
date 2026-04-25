#include <iostream>


class Vec2 {
public:
    double x, y;

    Vec2(double x = 0.0, double y = 0.0) : x(x), y(y) {}
    Vec2(const Vec2& other) {std::cout << "COPY CTOR!" << std::endl; *this = other;};
    void print() const {
        std::cout << "(" << x << ", " << y << ")\n";
    }

    Vec2 operator+(const Vec2& other) const {
        std::cout << "MEMBER OPERATOR+" << std::endl;
        return Vec2(this->x + other.x, this->y + other.y);
    };

    Vec2& operator+=(const Vec2& other) {
        this->x += other.x;
        this->y += other.y;
        return *this;
    };
    
    Vec2 operator-() const {
        return Vec2(-this->x, -this->y);
    };

    Vec2& operator+=(int t) {
        this->x += t;
        this->y += t;
        return *this;
    };

    Vec2 operator+(int t) {
        std::cout << "OPERATOR + with int" << std::endl;
        Vec2 res = *this;
        res += t;
        return res;
    };

    Vec2 operator*(const int s) const {
        Vec2 res = *this;
        res *= s;
        return res;
    };

    Vec2& operator*=(const int s) {
        this->x *= s;
        this->y *= s;
        return *this;
    };

    friend Vec2 operator*(const int s, const Vec2& v) {
        Vec2 res = v;
        res *= s;
        return res;
    };

    bool operator==(const Vec2& other) {
        return (this->x == other.x && this->y == other.y);
    };

    Vec2& operator=(const Vec2& other) {
        std::cout << "OPERATOR =" << std::endl;
        if (this != &other){
            this->x = other.x;
            this->y = other.y;
        };
        return *this;
    };
};

/* NON MEMBER OPERATORS */
Vec2 operator+(const Vec2& other, double s) {
    std::cout << "NON MEMBER OPERATOR+ >> LEFT OPERAND" << std::endl;
    return Vec2(other.x + s, other.y + s);  
};

Vec2 operator+(double s, const Vec2& other) {
    std::cout << "NON MEMBER OPERATOR+ >> RIGHT OPERAND" << std::endl;
    return Vec2(s + other.x, s + other.y);
};