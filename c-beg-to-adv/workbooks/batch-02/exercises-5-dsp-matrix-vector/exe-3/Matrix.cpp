#include "Matrix.h"

Matrix::Matrix(const double **mat, size_t r_, size_t c_) : r(r_), c(c_) {
    for(size_t i = 0; i < this->r; ++i) {
        for(size_t j = 0; j < this->c; ++j) {
            this->m[i][j] = mat[i][j];
        };
    };
};

Matrix::Matrix(const Matrix& other) : r(other.r), c(other.c) {
    for(size_t i = 0; i < this->r; ++i) {
        for(size_t j = 0; j < this->c; ++j) {
            this->m[i][j] = other.m[i][j];
        };
    };
};

void Matrix::print_linear_storage_idX(size_t i, size_t j) const {
    std::cout << "Linear Storage for idx (" << i << "," << j << ") : " <<
    (i*this->c + j) << std::endl;
};

std::ostream& operator<<(std::ostream& os, const Matrix& mat) {
    for(size_t i = 0; i < mat.r; ++i) {
        for(size_t j = 0; j < mat.c; ++j) {
            os << "| " << mat.m[i][j] << " |";
        };
        os << std::endl;
    };

    return os;
};