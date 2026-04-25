#include "HeapBins.h"

HeapBins::HeapBins() : bins_(new double[5]), n(5) {
    for(size_t i = 0; i < 5 ; i++) {
        bins_[i] = 0;
    };
};

HeapBins::HeapBins(size_t n_) : bins_(new double[n]), n(n_) {
    for(size_t i = 0; i < n; i++) {
        bins_[i] = 0;
    };
};

HeapBins& HeapBins::set_bin(double val, size_t idx) {

    if(idx > n - 1) {
        return *this;
    };
    this->bins_[idx] = val;
    return *this;
};

void HeapBins::print_bins() const {
    for(size_t i = 0; i < this->n; i++) {
        std::cout << "bins[" << i << "] = " << bins_[i] << ", ";
    };
    std::cout << std::endl;
};

HeapBins::~HeapBins() {
    delete[] this->bins_;
};