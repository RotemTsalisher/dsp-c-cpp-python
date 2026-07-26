#ifndef __MATRIX__H
#define __MATRIX__H

#include <iostream>
#include "MyVector.h"

static constexpr size_t MAX_DIM = 100;

class Matrix {
    private:
        double mat[MAX_DIM][MAX_DIM];
        size_t m,n;

    public:
        Matrix() = default;
        Matrix(const double **m, size_t m_, size_t n_);
        Matrix(const Matrix& other);
        ~Matrix() = default;

        friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
        Matrix outer_product(const MyVector& u, const MyVector& v) const;

        double operator()(size_t i, size_t j) const;
        double& operator()(size_t i, size_t j);
        double* operator[](size_t pos);

        double operator()(int i, int j) const;
        double& operator()(int i, int j);
        double* operator[](int pos);
};

#endif