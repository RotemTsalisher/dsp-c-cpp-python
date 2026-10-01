#ifndef __MATRIX__H
#define __MATRIX__H

#include "MyVector.h"

static constexpr std::size_t MAX_ROWS = 10000;
static constexpr std::size_t MAX_COLS = 10000;

class MyMatrix {
    private:
        std::size_t r,c;
        MyVector mat[MAX_ROWS];
    public:

        MyMatrix() : r(0), c(0) {};
        MyMatrix(const double **m, std::size_t r_, std::size_t c_);
        MyMatrix(const MyVector* row_list, std::size_t r_);
        MyMatrix(const MyMatrix& mat_);
        
        double& operator()(std::size_t i, std::size_t j);
        const double& operator()(std::size_t i, std::size_t j) const;

        MyMatrix& set_val(double val, std::size_t i, std::size_t j);
        double& get_val(std::size_t i, std::size_t j);
        const double& get_val(std::size_t i, std::size_t j) const;

        friend std::ostream& operator<<(std::ostream& os, const MyMatrix& mat);

        /* matrix & copy assignment */
        MyMatrix& operator=(const MyMatrix& other);

        /* scalar assignment */
        MyMatrix& operator=(const double x);

        /* row access */
        MyVector& operator[](std::size_t row_);
        const MyVector& operator[](std::size_t row_) const;

        /* unary minus */
        MyMatrix operator-() const;

        /* matrix scalar arithmetics */

        /* matrix + scalar */
        MyMatrix& operator+=(const double x);
        MyMatrix operator+(const double x) const;

        /* matrix - scalar */
        MyMatrix& operator-=(const double x);
        MyMatrix operator-(const double x) const;

        /* matrix * scalar */
        MyMatrix& operator*=(const double x);
        MyMatrix operator*(const double x) const;

        /* matrix / scalar */
        MyMatrix& operator/=(const double x);
        MyMatrix operator/(const double x) const;

        /* scalar matrix arithmetics */
        friend MyMatrix operator+=(const double x, const MyMatrix& A);
        friend MyMatrix operator-=(const double x, const MyMatrix& A);
        friend MyMatrix operator*=(const double x, const MyMatrix& A);
        friend MyMatrix operator/=(const double x, const MyMatrix& A);

        friend MyMatrix operator+(const double x, const MyMatrix& A);
        friend MyMatrix operator-(const double x, const MyMatrix& A);
        friend MyMatrix operator*(const double x, const MyMatrix& A);
        friend MyMatrix operator/(const double x, const MyMatrix& A);

        /* matrix - matrix arithmetics (element wise) */
        MyMatrix operator+(const MyMatrix& B) const;
        MyMatrix operator-(const MyMatrix& B) const;
        MyMatrix operator*(const MyMatrix& B) const;
        MyMatrix operator/(const MyMatrix& B) const;

        /* compound matrix arithmetics (element wise) */
        MyMatrix& operator+=(const MyMatrix& B);
        MyMatrix& operator-=(const MyMatrix& B);
        MyMatrix& operator*=(const MyMatrix& B);
        MyMatrix& operator/=(const MyMatrix& B);

        /* linear algebra */
        MyVector operator*(const MyVector& v) const;
        friend MyVector operator*(const MyVector& v, const MyMatrix& M);
        
        MyMatrix& inplace_mat_mult(const MyMatrix& M);
        MyMatrix mat_mult(const MyMatrix& M) const;

        /* comparisons */
        bool operator==(const MyMatrix& M) const;
        bool operator!=(const MyMatrix& M) const;

        /* matrix transformations */
        void transpose();
        MyMatrix transposed() const;

        /* matrix properties */
        double det() const;
        void inverse();
        MyMatrix inverted() const;
        double trace() const;
        bool is_square() const;

        /* row operations */
        MyVector get_row(std::size_t index) const;
        MyMatrix& set_row(const MyVector& v, std::size_t index);
        MyMatrix& swap_rows(std::size_t i, std::size_t j);

        /* column operations */
        MyVector get_column(std::size_t index) const;
        MyMatrix& set_column(const MyVector& v, std::size_t index);
        MyMatrix& swap_columns(std::size_t i, std::size_t j);

        /* statistics */
        double max()  const;
        double min()  const;
        double sum()  const;
        double mean() const;
        double norm1() const;
        double norm2() const;
        double frobenius() const;

        /* stream I / O */
        /* output is already declared */
        friend std::istream& operator>>(std::istream& is, MyMatrix& M);

        /* factory */
        static MyMatrix identity(std::size_t size);
        static MyMatrix diagonal(const MyVector& v);
        static MyMatrix zeros(std::size_t r, std::size_t c);
        static MyMatrix ones(std::size_t r, std::size_t c);
        
        /* DSP Oriented */
        static MyMatrix outer_product(const MyVector& u, const MyVector& v);
        static MyMatrix toeplitz(const MyVector& v);
        static MyMatrix circulant(const MyVector& v);
        static MyMatrix covariance(const MyVector& u, const MyVector& v);
        static MyMatrix correlation(const MyVector& u, const MyVector& v);

};

#endif