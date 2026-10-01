#include "MyMatrix.h"

/* constructors */
MyMatrix::MyMatrix(const double **m, std::size_t r_, std::size_t c_) : r(r_), c(c_) {

    for(size_t i = 0; i < r; ++i) {
        mat[i] = MyVector(m[i], c_);
    };
};

MyMatrix::MyMatrix(const MyVector* row_list, std::size_t r_) : r(r_), c(row_list[0].l) {
    for(std::size_t i = 0; i < r_; ++i) {
        this->mat[i] = MyVector(row_list[i]);
    };
}

MyMatrix::MyMatrix(const MyMatrix& mat_) {
    (*this) = mat_;
};

/* element access */
double& MyMatrix::operator()(std::size_t i, std::size_t j) {
    return mat[i][j];
};

const double& MyMatrix::operator()(std::size_t i, std::size_t j) const {
    return this->mat[i][j];
};

MyMatrix& MyMatrix::set_val(double val, std::size_t i, std::size_t j) {
    (*this)(i,j) = val;
    return *this;
};

double& MyMatrix::get_val(std::size_t i, std::size_t j) {
    return ((*this)(i, j));
};

const double& MyMatrix::get_val(std::size_t i, std::size_t j) const {
    return ((*this)(i, j));
};

/* stream I / O */
std::ostream& operator<<(std::ostream& os, const MyMatrix& mat) {
    for(std::size_t i = 0; i < mat.r; ++i) {
        os << "|";
        for(std::size_t j = 0; j < mat.c; ++j) {
            os << "| " << mat(i,j) << ((j < mat.c - 1) ? " |" : " ||\n");
            };
        };

    return os;
};

/* assignment */
MyMatrix& MyMatrix::operator=(const MyMatrix& other) {
    
    this->r = other.r;
    this->c = other.c;

    for(std::size_t i = 0; i < this->r; ++i) {
        this->mat[i] = other.mat[i];
    };

    return *this;
}

MyMatrix& MyMatrix::operator=(double x) {
    for(std::size_t i = 0; i < this->r; ++i) {
        this->mat[i] = MyVector::ones(this->c) * x;
    }

    return *this;
}