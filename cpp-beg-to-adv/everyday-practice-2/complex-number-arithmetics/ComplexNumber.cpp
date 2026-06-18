#include "ComplexNumber.h"

ComplexNumber::ComplexNumber(double a_, double b_) : a(a_), b(b_) {};


ComplexNumber ComplexNumber::operator+(const ComplexNumber& other) const {
    return ComplexNumber(this->a + other.a, this->b + other.b);
};

ComplexNumber ComplexNumber::operator-(const ComplexNumber& other) const {
    return ComplexNumber(this->a - other.a, this->b - other.b);
};

ComplexNumber ComplexNumber::operator*(const ComplexNumber& other) const {
    return ComplexNumber(this->a * other.a, this->b * other.b);
};

std::ostream& operator<<(std::ostream& os, const ComplexNumber c) {
    os << "<" << c.a << "," << c.b << ">";
    return os;
};
