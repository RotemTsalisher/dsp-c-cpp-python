#ifndef __MATRIX__H
#define __MATRIX__H

#include <iostream>

static constexpr size_t MAX_DIM_SIZE = 100;

class Matrix {
    private:
        double mat[MAX_DIM_SIZE][MAX_DIM_SIZE];
        size_t m,n;

    public:
        Matrix() = default;
        Matrix(const double **m, size_t m_, size_t n_);
        Matrix(const Matrix& other);
        ~Matrix() = default;

        Matrix operator~() const;

        friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
};

#endif