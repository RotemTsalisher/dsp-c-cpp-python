#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>

static constexpr size_t MAX_VECTOR_LENGTH = 100;

class MyVector {
    private:
        double vec[MAX_VECTOR_LENGTH];
        size_t l;
    public:
        MyVector() = default;
        MyVector(const double *v, size_t l_);
        MyVector(const MyVector& other);
        ~MyVector() = default;

        double dot(const MyVector& other) const;
        size_t get_length() const;
        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
};

#endif