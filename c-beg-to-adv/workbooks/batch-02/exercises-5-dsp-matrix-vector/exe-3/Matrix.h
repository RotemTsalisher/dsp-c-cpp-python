#ifndef __MATRIX__H
#define __MATRIX__H

#include <iostream>

static constexpr size_t MAX_ROWS = 100, MAX_COLS = 100;

class Matrix {
    private:
        double m[MAX_ROWS][MAX_COLS];
        size_t r,c;

    public:
        Matrix() = default;
        Matrix(const double **mat, size_t r_, size_t c_);
        Matrix(const Matrix& other);
        ~Matrix() = default;

        void print_linear_storage_idX(size_t i, size_t j) const;
        friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
};

#endif