#include <stdio.h>
#include <stdlib.h>

#define ROWS 3
#define COLS 4

static inline double dot_product(const double *v1, const double *v2, int n);
inline void print_vec(const double *v, int n);
void print_mat(const double **mat, int rows, int cols);
void matvec(const double **mat, const double *v, double *y, int rows, int cols);

int main(void)
{
    static double row0[COLS] = { 1.0, 2.0, 3.0, 4.0 };
    static double row1[COLS] = { 5.0, 6.0, 7.0, 8.0 };
    static double row2[COLS] = { 9.0, 10.0, 11.0, 12.0 };

    static double *mat[ROWS] = {
        row0,
        row1,
        row2
    };

    static double v[COLS] = {
        1.0, 1.0, 1.0, 1.0
    };

    double y[ROWS] = {0};

    print_mat((const double **)mat, ROWS, COLS);

    printf("\nv = ");
    print_vec(v, COLS);

    matvec((const double **)mat, v, y, ROWS, COLS);

    printf("\ny = ");
    print_vec(y, ROWS);

    return 0;
}

__attribute__((always_inline))
static inline double dot_product(const double *v1, const double *v2, int n) {
    
    double sum = 0.0;
    for (int i = 0; i < n; ++i) {
        sum += (v1[i] * v2[i]);
    };

    return sum;
};

void matvec(const double **mat, const double *v, double *y, int rows, int cols) {

    for(int i = 0; i <rows; ++i) {
        y[i] = dot_product(mat[i], v, cols);
    };
}

inline void print_vec(const double *v, int n) {
    for(int i = 0; i < n; ++i) {
        printf("| %4.2lf |", v[i]);
    };
    printf("\n");
};

void print_mat(const double **mat, int rows, int cols) {

    for(int i = 0; i < rows; ++i) {
        print_vec(mat[i], cols);
    };
};