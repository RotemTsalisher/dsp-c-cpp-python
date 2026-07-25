#ifndef __MATRIX__H
#define __MATRIX__H

#include <iostream>
#include "MyVector.h"

static constexpr size_t MAX_ROWS = 100, MAX_COLS= 100;

class Matrix {
    private:
        double mat[MAX_ROWS][MAX_COLS];
        size_t m,n;

    public:
        Matrix() = default;
        Matrix(const double **m, size_t m_, size_t n_);
        Matrix(const Matrix& other);
        ~Matrix() = default;

        MyVector operator*(const MyVector& v) const;
};

#endif