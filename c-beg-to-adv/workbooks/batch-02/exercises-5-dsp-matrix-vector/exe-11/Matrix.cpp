#include "Matrix.h"

const double& Matrix::operator()(size_t i, size_t j) const {
    return this->mat[i][j];
};

double& Matrix::operator()(size_t i, size_t j) {
    return this->mat[i][j];
};

Matrix::Matrix(const double **m, size_t m_, size_t n_) : m(m_), n(n_) {
    for(size_t i = 0; i < this->m; ++i) {
        for(size_t j = 0; j < this->n; ++j) {
            (*this)(i,j) = m[i][j];
        };
    };
};

Matrix::Matrix(const Matrix& other) : m(other.m), n(other.n) {
    for(size_t i = 0; i < this->m; ++i) {
        for(size_t j = 0; j < this->n; ++j) {
            (*this)(i,j) = other(i,j);
        };
    };
};

std::ostream& operator<<(std::ostream& os, const Matrix& mat) {
    for(size_t i = 0; i < mat.m; ++i){
        for(size_t j = 0; j < mat.n; ++j) {
            os << mat(i,j) << (j + 1 < mat.n ? " | " : "\n");
        };
    };

    return os;
};