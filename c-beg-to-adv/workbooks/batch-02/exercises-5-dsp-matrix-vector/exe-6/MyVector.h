#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>

class Matrix;

static constexpr size_t MAX_LENGTH = 100;

class MyVector {
    friend class Matrix;
    private:
        double vec[MAX_LENGTH];
        size_t n;
    
    public:
        MyVector() = default;
        MyVector(const double *v, size_t n_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        friend std::ostream& operator<<(std::ostream& os, const MyVector& v);
};

#endif