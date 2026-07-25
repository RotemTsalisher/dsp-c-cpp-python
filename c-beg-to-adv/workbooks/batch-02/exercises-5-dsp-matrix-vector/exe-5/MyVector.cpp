#include "MyVector.h"

MyVector::MyVector(const double *v, size_t l_) : l(l_) {
    for(size_t i = 0; i < this->l; ++i) {
        this->vec[i] = v[i];
    };
};

MyVector::MyVector(const MyVector& other) : l(other.l) {
    for(size_t i = 0; i < this->l; ++i) {
        this->vec[i] = other.vec[i];
    };
};

double MyVector::norm2() const {
    double res = 0.0;
    for(size_t i = 0; i < this->l; ++i) {
        res += (this->vec[i] * this->vec[i]);
    };

    return std::sqrt(res);
};

void MyVector::operator*(double g) {
    for(size_t i = 0; i < this->l; ++i) {
        this->vec[i] *= g;
    };
};

void MyVector::operator*=(double g) {
    this->operator*(g);
};

void MyVector::normalize(double norm) {
    if(!(norm)) {
        return;
    };

    (*this) *= (1.0 / norm);
};

std::ostream& operator<<(std::ostream& os, const MyVector& vec) {
    os << "<";
    for(size_t i = 0; i < vec.l - 1; ++i) {
        os << vec.vec[i] << ",";
    };
    os << vec.vec[vec.l - 1] << ">" << std::endl;

    os << "Length : " << vec.l << std::endl;
    return os;
}