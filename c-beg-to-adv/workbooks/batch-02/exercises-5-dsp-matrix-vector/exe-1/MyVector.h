#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>

constexpr size_t MAX_VECTOR_SIZE = 100;

class MyVector {
    
    private:
        double v[MAX_VECTOR_SIZE];
        size_t n;
    public:
        MyVector() = default;
        MyVector(const double* v_, size_t n_);
        MyVector(const MyVector &other);
        ~MyVector() = default;

        MyVector& set_val(size_t idx, double val);
        double get_val(size_t idx) const;
        void print_vec() const;
};

#endif