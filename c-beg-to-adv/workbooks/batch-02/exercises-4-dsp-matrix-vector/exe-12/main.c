#include <stdio.h>
#include <stdlib.h>

#define SUCCESS    0
#define MAX_ROWS   100
#define MAX_COLS   MAX_ROWS

struct Matrix {
    double mat[MAX_ROWS][MAX_COLS];
    int m,n;
};

struct Matrix mat_mult(const struct Matrix *A, const struct Matrix *B);
inline static double dot_product(const double *u, const double *v, int length);
struct Matrix tiled_mat_mult(const struct Matrix *A, const struct Matrix *B, int tile_dim_r, int tile_dim_c);
struct Matrix copy_mat(const struct Matrix *source, int m_, int n_);
struct Matrix add_mat(const struct Matrix *A, const struct Matrix *B);

int main(void) {

    struct Matrix A = {
        .mat = {
            {1, 2, 3},
            {4, 5, 6}
        },
        .m = 2,
        .n = 3
    };

    struct Matrix B = {
        .mat = {
            {7,  8},
            {9, 10},
            {11, 12}
        },
        .m = 3,
        .n = 2
    };

    struct Matrix C1 = mat_mult(&A, &B);
    struct Matrix C2 = tiled_mat_mult(&A, &B, 2, 2);

    puts("Naive:");
    for(int i = 0; i < C1.m; ++i) {
        for(int j = 0; j < C1.n; ++j) {
            printf("%8.2lf ", C1.mat[i][j]);
        }
        putchar('\n');
    }

    puts("\nTiled:");
    for(int i = 0; i < C2.m; ++i) {
        for(int j = 0; j < C2.n; ++j) {
            printf("%8.2lf ", C2.mat[i][j]);
        }
        putchar('\n');
    }

    return SUCCESS;
}

struct Matrix copy_mat(const struct Matrix *source, int m_, int n_) {
    struct Matrix res = {.mat = {0}, .m = m_, .n = n_};

    for(int i =0; i < res.m; ++i) {
        for(int j = 0; j < res.n; ++j) {
            res.mat[i][j] = source->mat[i][j];
        }
    }

    return res;
};

struct Matrix add_mat(const struct Matrix *A, const struct Matrix *B) {

    struct Matrix res = {.mat = {0}, .m = A->m, .n = A->n};

    for(int i = 0; i < res.m; ++i) {
        for(int j = 0; j < res.n; ++j) {
            res.mat[i][j] = (A->mat[i][j] + B->mat[i][j]);
        };
    };

    return res;
};

struct Matrix tiled_mat_mult(const struct Matrix *A, const struct Matrix *B, int tile_dim_r, int tile_dim_c) {

    struct Matrix C = {.mat = {0}, .m = A->m, .n = B->n};

    for(int m_ = 0; m_ < A->m; m_ += tile_dim_r) {
        for(int n_ = 0; n_ < B->n; n_ += tile_dim_c) {
            for(int k_ = 0; k_ < A->n; k_ += tile_dim_c) {
                int row_lim = (m_ + tile_dim_r < A->m) ? m_ + tile_dim_r : A->m;
                int col_lim = (n_ + tile_dim_c < B->n) ? n_ + tile_dim_c : B->n;
                int dot_lim = (k_ + tile_dim_c < A->n) ? k_ + tile_dim_c : A->n;

                for(int i = m_ ; i < row_lim ; ++i) {
                    for(int j = n_; j < col_lim ; ++j) {
                        for(int k = k_ ; k < dot_lim ; ++k)
                        {
                            C.mat[i][j] += (A->mat[i][k] * B->mat[k][j]); 
                        }    
                    }
                }
            }
        }
    }
    return C;
}

struct Matrix mat_mult(const struct Matrix *A, const struct Matrix *B) {
    if(A->n != B->m) {
        printf("DIMENTIONS DON'T MATCH!\n");
        return (struct Matrix){0};
    };

    struct Matrix C;
    C.m = A->m;
    C.n = B->n;

    for(int i = 0; i < C.m; ++i) {
        for(int j = 0; j < C.n; ++j) {
            C.mat[i][j] = 0.0;
            for(int k = 0; k < A->n; ++k) {
                C.mat[i][j] += (A->mat[i][k] * B->mat[k][j]);
            };
        };
    };

    return C;
};

inline static double dot_product(const double *u, const double *v, int length) {
    
    double res = 0.0;
    for(int i =0 ; i < length; ++i) {
        res += (u[i] * v[i]);
    };

    return res;
}