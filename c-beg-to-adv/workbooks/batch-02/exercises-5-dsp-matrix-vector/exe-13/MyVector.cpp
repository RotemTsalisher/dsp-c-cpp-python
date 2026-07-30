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
    for(size_t i = 0; i < vec.l; ++i) {
        os << vec[i] << (i < vec.l - 1 ? ", " : ">");
    };

    return os;
};