#include "MyVector.h"

double& MyVector::operator[](size_t i) {
    return this->vec[i];
};

const double& MyVector::operator[](size_t i) const {
    return this->vec[i];
};

MyVector::MyVector(const double *v, size_t n_) : n(n_) {
    for(size_t i = 0; i < this->n; ++i) {
        (*this)[i] = v[i];
    };
};

MyVector::MyVector(const MyVector& other) : n(other.n) {
    for(size_t i = 0; i < this->n; ++i) {
        (*this)[i] = other.vec[i];
    };
};

void MyVector::operator*=(double g) {
    for(size_t i = 0; i < this->n; ++i) {
        (*this)[i] *= g;
    };
};

MyVector MyVector::operator*(double g) const {
    MyVector res = *this;

    res *= g;
    return res;
};

MyVector MyVector::operator+(const MyVector& other) {
    MyVector res = *this;

    res += other;
    return res;
};

void MyVector::operator+=(const MyVector& other) {
    
    for(size_t i = 0; i < this->n; ++i) {
        (*this)[i] += other[i];
    };
}

std::ostream& operator<<(std::ostream& os, const MyVector& vec) {
    os << "<";
    for(size_t i = 0; i < vec.n - 1; ++i) {
        os << vec[i] << ",";
    };
    os << vec[vec.n - 1] << ">";

    return os;
};

void MyVector::axpy(double alpha, const MyVector& x) {
    (*this) += (alpha * x);
};

MyVector operator*(double g, const MyVector& x) {
    MyVector res = x;

    res *= g;
    return res;
}