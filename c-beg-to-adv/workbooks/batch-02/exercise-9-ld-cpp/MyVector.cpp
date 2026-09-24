#include "MyVector.h"


MyVector& MyVector::operator=(const double *v_) {
    
    for(size_t i = 0; i < this->l; ++i) {
        this->v[i] = v_[i];
    };

    return *this;
};

MyVector& MyVector::operator=(const MyVector& other) {
    this->l = other.l;
    (*this) = other.v;

    return *this;
}

MyVector::MyVector(const double *v_, std::size_t l_) : l(l_) {
    (*this) = v_;
};

MyVector::MyVector(const MyVector& other) : l(other.l) {
    (*this) = other.v;
};
