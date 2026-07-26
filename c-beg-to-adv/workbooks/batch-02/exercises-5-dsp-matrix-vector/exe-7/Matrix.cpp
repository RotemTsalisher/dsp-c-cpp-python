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

Matrix Matrix::operator*(const Matrix& other) const {
    
    Matrix res;
    if(this->n !=other.m) {
        std::cout << "DIMENTIONS MISS MATCH!" << std::endl;
        return res;
    };

    res.m = this->m;
    res.n = other.n;

    for(size_t i = 0; i < res.m; ++i) {
        for(size_t j = 0; j < res.n; ++j) {
            res.mat[i][j] = 0.0;
            for(size_t k = 0; k < this->n; ++k) {
                res.mat[i][j] += (this->mat[i][k] * other.mat[k][j]);
            }
        }
    }

    return res;
};

std::ostream& operator<<(std::ostream& os , const Matrix& mat) {
    for(size_t i = 0; i < mat.m; ++i) {
        for(size_t j = 0; j < mat.n; ++j) {
            std::cout << "| " << mat.mat[i][j] << "|";
        };
        std::cout <<std::endl;
    };

    return os;
};