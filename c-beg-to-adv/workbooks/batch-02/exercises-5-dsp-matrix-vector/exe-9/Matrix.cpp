#include "Matrix.h"

Matrix::Matrix(const double **m, size_t m_, size_t n_) : m(m_), n(n_) {
    for(size_t i = 0; i < this->m; ++i) {
        for(size_t j = 0; j < this->n; ++j) {
            this->mat[i][j] = m[i][j];
        };
    };
};

Matrix::Matrix(const Matrix& other) : m(other.m), n(other.n) {
    for(size_t i = 0; i < this->m; ++i) {
        for(size_t j = 0; j < this->n; ++j) {
            this->mat[i][j] = other.mat[i][j];
        };
    };
};

std::ostream& operator<<(std::ostream& os, const Matrix& mat) {
    for(size_t i = 0; i < mat.m; ++i) {
        for(size_t j = 0; j < mat.n; ++j) {
            os << mat.mat[i][j] << ((j + 1 < mat.n) ? " | " : "\n"); 
        };
    };

    return os;
};

Matrix Matrix::outer_product(const MyVector& u, const MyVector& v) const {
    Matrix res;

    res.m = u.n;
    res.n = v.n;

    for(size_t i = 0; i < res.m; ++i) {
        for(size_t j = 0; j < res.n; ++j) {
            res.mat[i][j] = u[i] * v[j];
        };
    };

    return res;
};

double Matrix::operator()(size_t i, size_t j) const {
    return this->mat[i][j];
};

double& Matrix::operator()(size_t i, size_t j) {
    return this->mat[i][j];
};

double* Matrix::operator[](size_t pos) {
    return this->mat[pos];
};

double Matrix::operator()(int i, int j) const {
    return this->mat[i][j];
};

double& Matrix::operator()(int i, int j) {
    return this->mat[i][j];
};

double* Matrix::operator[](int pos) {
    return this->mat[pos];
};