#include <stdio.h>
#include <stdlib.h>

#define MAX_ROWS 100
#define MAX_COLS MAX_ROWS

struct Matrix {
    double m[MAX_ROWS][MAX_COLS];
    int r,c;
};

struct Vector {
    double v[MAX_COLS];
    int m;
};

void gemv_rowmajor(const struct Matrix *A, const struct Vector *x, struct Vector *y);

int main() {
    struct Matrix A = {
        .m = {
            { 1,  2,  3,  4},
            { 5,  6,  7,  8},
            { 9, 10, 11, 12},
            {13, 14, 15, 16},
            {17, 18, 19, 20},
            {21, 22, 23, 24},
            {25, 26, 27, 28},
            {29, 30, 31, 32}
        },
        .r = 8,
        .c = 4
    };

    struct Vector x = {
        .v = {1, 2, 3, 4},
        .m = 4
    };

    struct Vector y;

    gemv_rowmajor(&A, &x, &y);

    for (int i = 0; i < y.m; ++i) {
        printf("%.1lf ", y.v[i]);
    }
    printf("\n");

    return 0;
}

void gemv_rowmajor(const struct Matrix *A, const struct Vector *x, struct Vector *y) {

    if(A->c != x->m) {
        return ;
    }

    y->m = A->r;

    for(int i = 0; i < y->m; ++i) {
        y->v[i] = 0.0;
        for(int j = 0; j <A->c; ++j) {
            y->v[i] += (A->m[i][j] * x->v[j]);
        }
    }
}

