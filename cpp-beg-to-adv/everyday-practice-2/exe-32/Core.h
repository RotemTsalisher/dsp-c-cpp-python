#ifndef __CORE__H
#define __CORE__H

class Core {
    protected:
        int fftOrder_;
    
    public:
        Core();
        Core(int fftOrder);
        Core(const Core& other);
};

#endif