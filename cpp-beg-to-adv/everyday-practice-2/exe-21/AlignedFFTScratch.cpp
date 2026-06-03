#include "AlignedFFTScratch.h"
#include <iostream>

AlignedFFTScratch::AlignedFFTScratch() : size(256) {
    this->buf_ = new double[this->size];
    for (size_t i = 0; i < this->size; i++){
        buf_[i] = i + 1;
    };

    std::cout << "initialized " << this->size << " sized buffer with EMPTY CTOR" << std::endl;
};

AlignedFFTScratch::AlignedFFTScratch(int size_) : size(size_) { //defult
    this->buf_ = new double[this->size];
    for (size_t i = 0; i < this->size; i++){
        buf_[i] = i + 1;
    };

    std::cout << "initialized " << this->size << " sized buffer with SIZE PARAM CTOR" << std::endl;
};

AlignedFFTScratch::~AlignedFFTScratch() {
    delete[] this->buf_;
    this->size = 0;

    std::cout << "deleted buffer with destructor, size = " << this->size << std::endl;
};

std::ostream& operator<<(std::ostream& os, const AlignedFFTScratch& afs) {
    os << "printing array: " << std::endl;
    for(size_t i = 0; i < afs.size ; i++) {
        os << "buf[" << i << "] = " << afs.buf_[i] << std::endl;
    };
    return os;
};


