#ifndef __ALIGNEDFFTSCRATCH__H
#define __ALIGNEDFFTSCRATCH__H

#include <iostream>

class AlignedFFTScratch {
    private:
        double* buf_;
        int size;
    
    public:

        AlignedFFTScratch();
        AlignedFFTScratch(int size_);
        ~AlignedFFTScratch();

        AlignedFFTScratch(const AlignedFFTScratch& other) = delete;
        AlignedFFTScratch& operator=(const AlignedFFTScratch& other) = delete;

        friend std::ostream& operator<<(std::ostream& os, const AlignedFFTScratch& afs);
};

#endif