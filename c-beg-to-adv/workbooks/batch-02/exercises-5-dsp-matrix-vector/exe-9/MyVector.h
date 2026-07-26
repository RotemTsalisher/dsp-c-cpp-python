#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>
static constexpr size_t MAX_LEN = 100;

class MyVector {

    friend class Matrix;
    private:
        double vec[MAX_LEN];
        size_t n;

    public:
        MyVector() = default;
        MyVector(const double *v, size_t n_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        double& operator[](size_t i);
        double operator[](size_t i) const;
};

#endif