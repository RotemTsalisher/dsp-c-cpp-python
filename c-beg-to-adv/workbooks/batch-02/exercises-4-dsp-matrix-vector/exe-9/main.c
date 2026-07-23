#include <stdio.h>
#include <stdlib.h>

#define MAX_ROWS 100
#define MAX_COLS MAX_ROWS

struct Matrix {
    double mat[MAX_ROWS][MAX_COLS];
    int m,n;
};

void outer_product(const double *u, int m, const double *v, int n, struct Matrix *M) {
    M->m = m;
    M->n = n;

    for(int i = 0; i < M->m; ++i) {
        for(int j = 0; j < M->n; ++j) {
            M->mat[i][j] = u[i] * v[j];
        }
    }
};

int main(void)
{
    double u[] = {1.0, 2.0, 3.0};
    double v[] = {4.0, 5.0};

    struct Matrix M = {0};

    outer_product(u, 3, v, 2, &M);

    printf("M (%d x %d):\n", M.m, M.n);

    for (int i = 0; i < M.m; ++i) {
        for (int j = 0; j < M.n; ++j) {
            printf("%6.1f ", M.mat[i][j]);
        }
        printf("\n");
    }

    return 0;
}