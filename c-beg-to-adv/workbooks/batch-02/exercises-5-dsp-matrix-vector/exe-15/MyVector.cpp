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
        os << vec[i] << (i + 1 < vec.l ? ", " : ">");
    };

    return os;
};

void MyVector::process_residual(double const *t, double const *x, int n, double *r, double *g_out, double *energy_out) {
    double tt = 0.0, tx = 0.0;
    *energy_out = 0.0;

    for(size_t i = 0; i < n; ++i) {
        tt += (t[i] * t[i]);
        tx += (t[i] * x[i]);
    };

    *g_out = (tt == 0.0) ? 0.0 : (tx / tt);

    for(size_t i = 0; i < n; ++i) {
        r[i] = x[i] - (*g_out) * t[i];
        *energy_out += (r[i] * r[i]);
    };
};