#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>
static constexpr size_t MAX_DIM_SIZE = 100;

class Matrix;
class MyVector {
    friend class Matrix;
    private:
        double vec[MAX_DIM_SIZE];
        size_t l;

    public:
        MyVector() = default;
        MyVector(const double *v, size_t l_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        const double& operator[](size_t i) const;
        double& operator[](size_t i);
        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
        MyVector fir_via_matvec(const MyVector& h) const;
        MyVector fir_direct(const MyVector& h) const;
};


#endif