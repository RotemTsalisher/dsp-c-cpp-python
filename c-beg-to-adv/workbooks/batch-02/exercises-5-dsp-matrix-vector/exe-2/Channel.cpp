#include "Channel.h"

Channel::Channel(const double *v, size_t l_) : l(l_) {
    for(int i = 0; i < this->l; ++i) {
        this->vec[i] = v[i];
    };
};

Channel::Channel(const Channel &other) : l(other.l) {
    for(int i = 0; i < this->l; ++i) {
        this->vec[i] = other.vec[i];
    };
};

void Channel::operator*(double g) {
    for(int i = 0; i < this->l; ++i) {
        this->vec[i] *= g;
    };
};

void Channel::operator+(const Channel &other) {
    for(int i = 0; i < this->l; ++i) {
        this->vec[i] += other.vec[i];
    };
};

std::ostream& operator<<(std::ostream& os, const Channel& ch) {
    os << "<";
    for(int i =0; i < ch.l - 1; ++i) {
        os << ch.vec[i] << ",";
    };
    os <<ch.vec[ch.l - 1] << ">" << std::endl;
    os <<"Length : " << ch.l << std::endl;

    return os;
};