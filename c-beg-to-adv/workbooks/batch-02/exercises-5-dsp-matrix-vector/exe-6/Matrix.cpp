#include "Matrix.h"
#include "MyVector.h"

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
MyVector Matrix::operator*(const MyVector& v) const {
    MyVector res;
    if(this->n != v.n) {
        std::cout << "SIZE MISMATCH!" << std::endl;
        return res;
    };

    res.n = this->m;
    for(size_t i = 0; i < res.n; ++i) {
        res.vec[i] = 0.0;
        for(size_t k = 0; k < this->n; ++k) {
            res.vec[i] += (this->mat[i][k] * v.vec[k]);
        };
    };

    return res;
};