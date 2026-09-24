#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>

class MyMatrix;

static constexpr size_t MAX_VEC_SIZE = 4096;

class MyVector {

    friend class MyMatrix;
    private:
        double v[MAX_VEC_SIZE];
        std::size_t l;
    
    public:
        MyVector() = default;
        MyVector(const double *v_, std::size_t l_);
        MyVector(const MyVector& other);

        MyVector& set_val(std::size_t index, double val);
        const double get_val(std::size_t index) const;

        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
};

#endif