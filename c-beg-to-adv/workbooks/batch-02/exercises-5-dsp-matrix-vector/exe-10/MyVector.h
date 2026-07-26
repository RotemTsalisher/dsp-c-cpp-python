#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>
static constexpr size_t MAX_LENGTH = 100;

class MyVector {
    private:
        double vec[MAX_LENGTH];
        size_t n;

    public:
        MyVector() = default;
        MyVector(const double *v, size_t n_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        void operator*=(double g);
        MyVector operator*(double g) const;
        double& operator[](size_t i);
        const double& operator[](size_t i) const;
        MyVector operator+(const MyVector& other);
        void operator+=(const MyVector& other);

        void axpy(double alpha, const MyVector& x);
        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
        friend MyVector operator*(double g, const MyVector& x);
};

#endif