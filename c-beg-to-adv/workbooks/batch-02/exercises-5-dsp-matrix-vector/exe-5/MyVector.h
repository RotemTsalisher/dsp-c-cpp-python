#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>
#include <cmath>
static constexpr size_t MAX_LENGTH = 100;

class MyVector {
    private:
        double vec[MAX_LENGTH];
        size_t l;

    public:
        MyVector() = default;
        MyVector(const double *v, size_t l_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        double norm2() const;
        void normalize(double norm);
        void operator*(double g);
        void operator*=(double g);
        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
};

#endif