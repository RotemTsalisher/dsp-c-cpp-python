#include <stdio.h>
#include <stdlib.h>

#define SUCCESS      0
#define ROWS         2
#define COLS         3
#define MAX_DIM_SIZE 100

struct Matrix {
    double m[MAX_DIM_SIZE][MAX_DIM_SIZE];
    int r,c;
};

// static inline double dot_product(const double *v1, const double *v2, int n);
void mat_mult(const struct Matrix *m1, const struct Matrix *m2, struct Matrix *res) {
    /* check dimentions fit */
    if(m1->c != m2->r) {
        /* dimentions don't fit */
        return ;
    }

    /* define result's dimentions */
    res->r = m1->r;
    res->c = m2->c;

    /* compute elements of result */
    for(int i = 0; i < res->r; ++i) {
        for(int j = 0; j < res->c; ++j) {

            /* init this slot of result matrix */
            res->m[i][j] = 0.0;

            for(int k = 0; k < m1->c; ++k) {
                res->m[i][j] += (m1->m[i][k] * m2->m[k][j]);
            }
        }
    }
}

int main(void)
{
    struct Matrix m1 = {
        .m = {
            { 1.0, 2.0, 3.0 },
            { 4.0, 5.0, 6.0 }
        },
        .r = 2,
        .c = 3
    };

    struct Matrix m2 = {
        .m = {
            { 7.0,  8.0 },
            { 9.0, 10.0 },
            {11.0, 12.0 }
        },
        .r = 3,
        .c = 2
    };

    struct Matrix res = {0};

    mat_mult(&m1, &m2, &res);

    printf("Result (%d x %d):\n", res.r, res.c);

    for (int i = 0; i < res.r; ++i) {
        for (int j = 0; j < res.c; ++j) {
            printf("%8.2lf", res.m[i][j]);
        }
        printf("\n");
    }

    return SUCCESS;
}
/*
__attribute__((always_inline))
static inline double dot_product(const double *v1, const double *v2, int n) { 

    double sum = 0.0;
    for(int i = 0; i < n; sum += (v1[i] * v2[i]), i++);
};*/

