#ifndef __COMPLEXNUMBER__H
#define __COMPLEXNUMBER__H

#include <iostream>

class ComplexNumber {
    private:
        double a,b;
    public:
        ComplexNumber(double a_ = 0.0, double b_ = 0.0);
        ComplexNumber operator+(const ComplexNumber& other) const ;
        ComplexNumber operator-(const ComplexNumber& other) const ;
        ComplexNumber operator*(const ComplexNumber& other) const ;

        friend std::ostream& operator<<(std::ostream& os, const ComplexNumber c);
};

#endif