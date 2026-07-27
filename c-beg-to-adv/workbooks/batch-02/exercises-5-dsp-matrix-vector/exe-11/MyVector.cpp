#include "MyVector.h"

double& MyVector::operator[](size_t i) {
    return this->vec[i];
};

const double& MyVector::operator[](size_t i) const {
    return this->vec[i];
};

MyVector::MyVector(const double *v, size_t l_) : l(l_) {
    for(size_t i = 0; i < this->l; ++i) {
        (*this)[i] = v[i];
    };
};

MyVector::MyVector(const MyVector& other) : l(other.l) {
    for(size_t i = 0; i < this->l; ++i) {
        (*this)[i] = other[i];
    };   
};

std::ostream& operator<<(std::ostream& os, const MyVector& vec) {
    os << "<";
    for(size_t i = 0; i < vec.l - 1; ++i) {
        os << vec[i] << ",";
    }

    os << vec[vec.l - 1] << ">";
    return os;
};

MyVector MyVector::matvec(const Matrix& mat, const MyVector& vec) {
    MyVector res;
    res.l = mat.m;

    double acc = 0.0;

    for(size_t i = 0; i < res.l; ++i) {
        acc = 0.0;
        for(size_t k = 0; k < mat.n; ++k) {
            acc += (mat(i,k) * vec[k]);
        };

        res[i] = acc;
    };

    return res;
};
