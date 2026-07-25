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

std::ostream& operator<<(std::ostream& os, const MyVector& vec) {
    os << "<";
    for(size_t i = 0; i < vec.n - 1; ++i) {
        os << vec.vec[i] << ",";
    };
    os << vec.vec[vec.n - 1] << ">";

    return os;
}

