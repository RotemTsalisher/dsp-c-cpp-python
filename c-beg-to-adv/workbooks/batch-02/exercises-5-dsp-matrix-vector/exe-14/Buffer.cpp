#include "Buffer.h"


const double& Buffer::operator[](size_t i) const {
    return this->buff[i];
};

double& Buffer::operator[](size_t i) {
    return this->buff[i];
};

Buffer::Buffer(const double *b, size_t l_) : l(l_) {
    for(size_t i = 0; i < this->l; ++i) {
        (*this)[i] = b[i];
    };

};

Buffer::Buffer(const Buffer& other) : l(other.l) {
    for(size_t i = 0; i < this->l; ++i) {
        (*this)[i] = other[i];
    };
};

void Buffer::compute_energy(double& energy_l, double& energy_r) const {
    energy_l = 0.0;
    energy_r = 0.0;

    for(size_t i = 0; i < this->l; i += 2) {
        energy_l += ((*this)[i] * (*this)[i]);
        energy_r += ((*this)[i + 1] * (*this)[i + 1]);
    };
};

void Buffer::write_mono(Buffer& mono_buffer) const { 
    
    mono_buffer.l = (int)((this->l / 2.0f) + 0.5f);
    for(size_t i = 0; i < mono_buffer.l; ++i) {
        mono_buffer[i] = 0.5 * ((*this)[2*i] + (*this)[2*i + 1]);
    };
};

std::ostream& operator<<(std::ostream& os, const Buffer& buff) {
    os << "<";
    for(size_t i = 0; i < buff.l; ++i) {
        os << buff[i] << ((i < buff.l - 1) ? ", " : "\n");
    };

    return os;
};