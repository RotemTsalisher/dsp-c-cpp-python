#ifndef __HEAPBINS__H
#define __HEAPBINS__H

#include <iostream>

class HeapBins {
    private:
        double *bins_;
        size_t n;
    public:
        HeapBins();
        HeapBins(size_t n);

        HeapBins& set_bin(double val, size_t idx);
        void print_bins() const;


        ~HeapBins();
};

#endif