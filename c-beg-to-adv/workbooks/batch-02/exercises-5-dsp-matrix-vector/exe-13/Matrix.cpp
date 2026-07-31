#include "Matrix.h"
#include "MyVector.h"
double& Matrix::operator()(size_t i, size_t j) {
    return this->mat[i][j];
};

const double& Matrix::operator()(size_t i, size_t j) const {
    return this->mat[i][j];
};


Matrix::Matrix(const double **mat, size_t m_, size_t n_) : m(m_), n(n_) {
    for(size_t i = 0; i < this->m; ++i) {
        for(size_t j = 0; j < this->n; ++j) {
            (*this)(i,j) = mat[i][j];
        };
    };
};

Matrix::Matrix(const Matrix& other) : n(other.n), m(other.m) {
    for(size_t i = 0; i < this->m; ++i) {
        for(size_t j = 0; j < this->n; ++j) {
            (*this)(i, j) = other(i,j);
        };
    };
};

std::ostream& operator<<(std::ostream& os, const Matrix& mat) {
    for(size_t i = 0; i < mat.m; ++i) {
        for(size_t j = 0; j < mat.n; ++j) {
            os << mat(i, j) << (j + 1 < mat.n ? " | " : "\n");
        };
    };

    return os;
};

MyVector Matrix::operator*(const MyVector& vec) const {
    
    MyVector y;

    y.l = this->m;

    for(size_t i = 0; i < y.l; ++i) {
        y[i] = 0.0;

        for(size_t k = 0; k < this->n; ++k) {
            y[i] += ((*this)(i , k) * vec[k]);
        };
    };

    return y;
}