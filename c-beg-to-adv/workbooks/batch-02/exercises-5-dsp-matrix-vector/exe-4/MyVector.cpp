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

double MyVector::dot(const MyVector& other) const{
    
    double res = 0.0;

    for(size_t i = 0; i < this->l; ++i) {
        res += (this->vec[i] * other.vec[i]);
    };

    return res;
};

size_t MyVector::get_length() const {
    return this->l;
};

std::ostream& operator<<(std::ostream& os, const MyVector& v) {
    
    os << "<";
    for(size_t i = 0; i < v.l - 1; ++i) {
        os << v.vec[i] << ",";
    };
    os << v.vec[v.l - 1] << ">" << std::endl;
    os << "Length : " << v.l << std::endl;

    return os;
};