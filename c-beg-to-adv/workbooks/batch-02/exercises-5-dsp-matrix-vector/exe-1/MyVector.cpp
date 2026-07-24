#include "MyVector.h"
#include <iostream>

MyVector::MyVector(const double *v_, size_t n_) : n(n_) {
    for(size_t i = 0; i < this->n; ++i) {
        this->v[i] = v_[i];
    };
};

MyVector::MyVector(const MyVector& other) : n(other.n) {

    for(size_t i = 0; i < this->n; ++i) {
        this->v[i] = other.v[i];
    };
};

MyVector& MyVector::set_val(size_t idx, double val) {
    this->v[idx] = val;
    return *this;
};

double MyVector::get_val(size_t idx) const {
    return this->v[idx];
};

void MyVector::print_vec() const {
    for(size_t i = 0; i < this->n; ++i) {
        std::cout << "index = <" << i << ">, value = <" << this->v[i] << ">" << std::endl;
    };

    std::cout << "Length = " << this->n << std::endl;
};