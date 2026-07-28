#include "Matrix.h"

const double& Matrix::operator()(size_t i, size_t j) const {
    return this->mat[i][j];
};

double& Matrix::operator()(size_t i, size_t j) {
    return this->mat[i][j];
};

Matrix::Matrix(const double **m, size_t m_, size_t n_) : n(n_), m(m_) {
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

Matrix Matrix::operator*(const Matrix& other) const {
    Matrix res;
    double acc = 0.0;
    res.m = this->m;
    res.n = other.n;

    for(size_t i = 0; i < res.m; ++i) {
        for(size_t j = 0; j < res.n; ++j) {
            acc = 0.0;
            for(size_t k = 0; k < this->n; ++k) {
                acc += (((*this)(i,k)) * (other(k,j)));
            };

            res(i, j) = acc;
        };
    };

    return res;
};

Matrix Matrix::multiply_tile(const Matrix& other, size_t tile) {
    Matrix res;

    res.m = this->m;
    res.n = other.n;

    for(size_t ii = 0; ii < res.m; ii += tile) { 
        for(size_t jj = 0; jj < res.n; jj += tile) {
            size_t i_end = (ii + tile > res.m ? res.m : ii + tile);
            size_t j_end = (jj + tile > res.n ? res.n : jj + tile);

            for(size_t i = ii; i < i_end; ++i) {
                for(size_t j = jj; j < j_end; ++j) {
                    res(i,j) = 0.0;

                    for(size_t k = 0; k < tile; ++k) {
                        res(i,j) += ((*this)(i,jj + k) * other(ii + k,j));
                    };
                };
            };
        };
    };

    return res;
}

std::ostream& operator<<(std::ostream& os, const Matrix& matrix)
{
    for(size_t i = 0; i < matrix.m; ++i) {
        for(size_t j = 0; j < matrix.n; ++j) {
            os << matrix(i,j) << ' ';
        }
        os << '\n';
    }

    return os;
};

