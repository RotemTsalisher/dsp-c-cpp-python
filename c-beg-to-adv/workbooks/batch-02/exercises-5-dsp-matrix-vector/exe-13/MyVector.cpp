#include "MyVector.h"
#include "Matrix.h"
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

MyVector MyVector::fir_direct(const MyVector& h) const {
    MyVector y;

    y.l = this->l;

    for(size_t i = 0; i < y.l; ++i) {
        y[i] = 0.0;
        for(size_t k = 0; k < h.l; ++k) {
            y[i] += (h[k] * (*this)[(i - k + this->l) % this->l]);
        };
    };

    return y;
};

MyVector MyVector::fir_via_matvec(const MyVector& h) const {

    // vector to circulant:

    MyVector padded_h;
    padded_h.l = this->l;

    for(size_t i = 0; i < padded_h.l; ++i) {
        if(i < h.l) {
            padded_h[i] = h[i];
        }
        else {
            padded_h[i] = 0.0;
        };
    };

    Matrix circulant;

    circulant.m = padded_h.l;
    circulant.n = padded_h.l;

    for(size_t i = 0; i < circulant.m; ++i) {
        for(size_t j = 0; j < circulant.n; ++j) {
            circulant(i,j) = padded_h[(i - j + padded_h.l) % padded_h.l];
        };
    };

    MyVector y;

    y = (circulant * (*this));
/*    y.l = this->l;

    for(size_t i = 0; i < y.l; ++i) {
        y[i] = 0.0;

        for(size_t k = 0; k < circulant.n; ++k) {
            y[i] += (circulant(i , k) * (*this)[k]);
        };
    };
*/
    return y;
};
