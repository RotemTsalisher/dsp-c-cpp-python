#include "MyVector.h"

double& MyVector::operator[](std::size_t index) {
    return this->v[index];
};

const double& MyVector::operator[](std::size_t index) const {
    return this->v[index];
};

MyVector& MyVector::operator=(const double *v_) {
    
    for(size_t i = 0; i < this->l; ++i) {
        (*this)[i] = v_[i];
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

MyVector& MyVector::set_val(double val, std::size_t index) {
    (*this)[index] = val;
    return *this;
}

const double MyVector::get_val(std::size_t index) const {
    if(index >= this->l) {
        return NA;
    };
    return (*this)[index];
}

std::ostream& operator<<(std::ostream& os, const MyVector& vec) {
    os << "<";
    for(std::size_t i = 0; i < vec.l - 1; ++i) {
        os << vec[i] << ", ";
    };
    os << vec[vec.l - 1] << ">" << std::endl;

    return os;
};

MyVector& MyVector::operator+=(const double x) {
    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] += x;
    };

    return *this;
}

MyVector MyVector::operator+(const double x) const {
    MyVector res = *this;
    res += x;

    return res;
}

MyVector& MyVector::operator-=(const double x) {
    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] -= x;
    };

    return *this;
};

MyVector MyVector::operator-(const double x) const {
    MyVector res = *this;

    res -= x;
    return res;
};

MyVector& MyVector::operator+=(const MyVector& other) {
    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] += other[i];
    };

    return *this;
};

MyVector MyVector::operator+(const MyVector& other) const {

    MyVector res = *this;
    res += other;

    return res;
};

MyVector& MyVector::operator*=(const double x) {
    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] *= x;
    };

    return *this;
};

MyVector MyVector::operator*(const double x) const {

    MyVector res = *this;
    res *= x;
    return res;
};

MyVector& MyVector::operator*=(const MyVector& other) {

    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] *= other[i];
    };

    return *this;
};

MyVector MyVector::operator*(const MyVector& other) const {

    MyVector res = *this;
    res *= other;

    return res;
};

MyVector& MyVector::operator/=(const MyVector& other) {

    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] /= other[i];
    };

    return *this;
};

MyVector MyVector::operator/(const MyVector& other) const {

    MyVector res = *this;
    res /= other;

    return res;
};

MyVector& MyVector::operator/=(const double x) {
    for(std::size_t i = 0; i < this->l; ++i) {
        (*this)[i] /= x;
    };

    return *this;
};

MyVector MyVector::operator/(const double x) const {

    MyVector res = *this;
    res /= x;

    return res;
};

MyVector operator+(const double x, const MyVector& other) {
    return (other + x);
};

MyVector operator-(const double x, const MyVector& other) {
    return -(other - x);
}

MyVector operator*(const double x, const MyVector& other) {
    return (other * x);
};

MyVector operator/(const double x, const MyVector& other) {
    MyVector res = other;

    for(std::size_t i = 0; i < res.l; ++i) {
        res[i] = x / res[i];
    };

    return res;
};

MyVector MyVector::operator-() const {
    
    MyVector res = *this;
    return (-1.0 * res);

};

MyVector& MyVector::operator-=(const MyVector& other) {

    return ((*this) += (-other));
};

MyVector MyVector::operator-(const MyVector& other) const {
    
    MyVector res = *this;
    res -= other;
    return res;
};

double MyVector::max() const {
    double max = (*this)[0];
    bool alpha = 0;

    for(std::size_t i = 1; i < this->l; ++i) {
        alpha = ((*this)[i] > max);
        max = (alpha)*((*this)[i]) + (1 - alpha)*max;
    };

    return max;
}

double MyVector::min() const {
    double min = (*this)[0];
    bool alpha = 0;

    for(std::size_t i = 1; i < this->l; ++i) {
        alpha = ((*this)[i] < min);
        min = (alpha)*((*this)[i]) + (1 - alpha)*min;
    };

    return min;
}

double MyVector::sum() const {
    double sum = 0.0;

    for(std::size_t i = 0; i < this->l; ++i) {
        sum += ((*this)[i]);
    };

    return sum;
};

double MyVector::mean() const {
    double sum = this->sum();
    return sum / (this->l);
};

double MyVector::norm2() const {
    MyVector tmp = (*this) * (*this);
    double norm2_ = tmp.sum();

    return norm2_;
};

double MyVector::magnitude() const {
    return std::sqrt(this->norm2());
}

double MyVector::dot_product(const MyVector& other) const {
    double res = 0.0;

    for(std::size_t i = 0; i < this->l; ++i) {
        res += ((*this)[i] * other[i]);
    };

    return res;
};

MyVector MyVector::normalized() const {
    MyVector res = *this;
    res /= res.magnitude();

    return res;
};

void MyVector::normalize() {
    (*this) /= (*this).magnitude();
};

MyVector MyVector::auto_corr() const {
    MyVector res;
    res.l = 2 * this->l - 1;

    std::size_t center = res.l / 2;

    for(std::size_t k = 0; k < this->l; ++k) {
        res[center + k] = 0.0;
        for(std::size_t n = 0; (k + n) < this->l; ++n) {
            res[center + k] += ((*this)[n] * (*this)[n + k]);
        };
    };

    return res;
};

MyVector MyVector::ones(std::size_t l_) {
    MyVector res;
    res.l = l_;

    for(std::size_t i = 0; i < res.l; ++i) {
        res[i] = 1.0;
    };

    return res;
};

MyVector MyVector::zeros(std::size_t l_) {
    MyVector res;
    res.l = l_;

    for(std::size_t i = 0; i < res.l; ++i) {
        res[i] = 0.0;
    };

    return res;
}
