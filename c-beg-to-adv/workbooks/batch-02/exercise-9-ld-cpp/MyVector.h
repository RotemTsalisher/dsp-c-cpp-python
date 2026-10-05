#ifndef __MYVECTOR__H
#define __MYVECTOR__H

#include <iostream>
#include <cmath>

class MyMatrix;

static constexpr size_t MAX_VEC_SIZE = 4096;
static constexpr double NA           = -1000000.0;

class MyVector {

    friend class MyMatrix;

    private:
        double v[MAX_VEC_SIZE];
        std::size_t l;
    
    public:
        MyVector() : l(0) {};
        MyVector(const double *v_, std::size_t l_);
        MyVector(const MyVector& other);

        MyVector& set_val(double val, std::size_t index);
        const double get_val(std::size_t index) const;
        //double& get_val(std::size_t index);

        friend std::ostream& operator<<(std::ostream& os, const MyVector& vec);
        double& operator[](std::size_t index);
        const double& operator[](std::size_t index) const;

        /* vector math */
        /* vector on lhs */
        MyVector& operator=(const double *v_);
        MyVector& operator=(const MyVector& other);

        MyVector& operator+=(const double x);
        MyVector operator+(const double x) const;

        MyVector operator-(const double x) const;
        MyVector& operator-=(const double x);

        MyVector& operator+=(const MyVector& other);
        MyVector operator+(const MyVector& other) const;

        MyVector& operator-=(const MyVector& other);
        MyVector operator-(const MyVector& other) const;

        MyVector& operator*=(const double x);
        MyVector operator*(const double x) const;

        MyVector& operator*=(const MyVector& other); /* element wise */
        MyVector operator*(const MyVector& other) const; /* element wise */

        MyVector operator/(const MyVector& other) const;
        MyVector& operator/=(const MyVector& other);

        MyVector operator/(const double x) const;
        MyVector& operator/=(const double x);

        MyVector operator-() const;

        /* vector on rhs */
        friend MyVector operator+(const double x, const MyVector& other);
        friend MyVector operator-(const double x, const MyVector& other);
        friend MyVector operator*(const double x, const MyVector& other);
        friend MyVector operator/(const double x, const MyVector& other);


        double norm2() const;
        double magnitude() const;
        double sum() const;
        double mean() const;
        double dot_product(const MyVector& other) const;

        double max() const;
        double min() const;

        MyVector normalized() const; /* return a new vector */
        void normalize(); /* in place */

        MyVector cross_corr(const MyVector& other) const;
        MyVector auto_corr() const;
        static MyVector ones(std::size_t l_);
        static MyVector zeros(std::size_t l_);
};

#endif