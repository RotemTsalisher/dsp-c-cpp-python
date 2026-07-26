#include "MyVector.h"

MyVector::MyVector(const double *v, size_t n_) : n(n_) {
    for(size_t i = 0; i < this->n; ++i) {
        this->vec[i] = v[i];
    };
};

MyVector::MyVector(const MyVector& other) : n(other.n) {
    for(size_t i = 0; i < this->n; ++i) {
        this->vec[i] = other.vec[i];
    };
};

double& MyVector::operator[](size_t i) {
    return this->vec[i];
};

double MyVector::operator[](size_t i) const {
    return this->vec[i];
};