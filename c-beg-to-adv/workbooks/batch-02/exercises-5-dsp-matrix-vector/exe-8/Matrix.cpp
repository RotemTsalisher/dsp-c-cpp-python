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

Matrix Matrix::operator~() const {
    Matrix _t;
    _t.m = this->n;
    _t.n = this->m;

    for(size_t i = 0; i < _t.m; ++i) {
        for(size_t j = 0; j < _t.n; ++j) {
            _t.mat[i][j] = this->mat[j][i];
        };
    };

    return _t;
};

std::ostream& operator<<(std::ostream& os, const Matrix& M) {
    for (size_t i = 0; i < M.m; ++i) {
        for (size_t j = 0; j < M.n; ++j) {
            os << M.mat[i][j] << (j + 1 < M.n ? ' ' : '\n');
        }
    }
    return os;
}