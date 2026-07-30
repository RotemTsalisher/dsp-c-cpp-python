#ifndef __MATRIX__H
#define __MATRIX__H

#include <iostream>
static constexpr size_t MAX_ROWS = 100, MAX_COLS = 100;

class MyVector;
class Matrix {
    friend class MyVector;
    private:
        double mat[MAX_ROWS][MAX_COLS];
        size_t m,n;
    
    public:
        Matrix() = default;
        Matrix(const double **mat, size_t m_, size_t n_);
        Matrix(const Matrix& other);
        ~Matrix() = default;

        const double& operator()(size_t i, size_t j) const;
        double& operator()(size_t i, size_t j);
        MyVector& operator*(const MyVector& vec) const;
        friend std::ostream& operator<<(std::ostream& os, const Matrix mat);

};

#endif