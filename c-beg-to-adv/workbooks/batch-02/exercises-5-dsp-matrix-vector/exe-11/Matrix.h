#ifndef __MATRIX__H
#define __MATRIX__H

#include <iostream>

static constexpr size_t MAX_SIZE = 100;

class MyVector;
class Matrix {
    friend class MyVector;
    private:
        double mat[MAX_SIZE][MAX_SIZE];
        size_t m,n;
    public:
        Matrix() = default;
        Matrix(const double **m, size_t m_, size_t n_);
        Matrix(const Matrix& other);
        ~Matrix() = default;

        friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
        const double& operator()(size_t i, size_t j) const;
        double& operator()(size_t i, size_t j);
};

#endif