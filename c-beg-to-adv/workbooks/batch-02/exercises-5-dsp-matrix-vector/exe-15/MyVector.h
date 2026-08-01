#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>
static constexpr size_t MAX_VEC_SIZE = 100;

class MyVector {
    private:
        double vec[MAX_VEC_SIZE];
        size_t l;

    public:
        MyVector() = default;
        MyVector(const double *v, size_t l_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        double& operator[](size_t i);
        const double& operator[](size_t i) const;
        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
        void process_residual(double const *t, double const *x, int n, double *r, double *g_out, double *energy_out);
};

#endif