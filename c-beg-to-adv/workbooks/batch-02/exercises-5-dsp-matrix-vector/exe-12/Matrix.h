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

        friend std::ostream& operator<<(std::ostream& os, const Matrix& matrix);
        const double& operator()(size_t i, size_t j) const;
        double& operator()(size_t i, size_t j);

        Matrix operator*(const Matrix& other) const;
        Matrix multiply_tile(const Matrix& other, size_t tile);
};

#endif