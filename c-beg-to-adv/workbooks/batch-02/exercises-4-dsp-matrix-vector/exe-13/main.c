#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROWS 100
#define MAX_COLS MAX_ROWS

struct Matrix {
    int m,n;
    double mat[MAX_ROWS][MAX_COLS];
};

struct Vector {
    int n;
    double vec[MAX_COLS];
};

void fir_direct(const struct Vector *h, const struct Vector *x, struct Vector *y);
void vec_to_toplitz(const struct Vector *v, struct Matrix *toplitz_v, int N);
struct Vector matvec(const struct Matrix *A, const struct Vector *v);
void fir_via_matvec(const struct Vector *h, const struct Vector *x, struct Vector *y);

int main(void) {

    struct Vector h = {
        .n = 4,
        .vec = {1, 2, 3, 4}
    };

    struct Vector x = {
        .n = 4,
        .vec = {5, 6, 7, 8}
    };

    struct Vector y_direct = {0};
    struct Vector y_matvec = {0};

    fir_direct(&h, &x, &y_direct);
    fir_via_matvec(&h, &x, &y_matvec);

    printf("h = ");
    for(int i = 0; i < h.n; ++i)
        printf("%6.1lf ", h.vec[i]);

    printf("\n");

    printf("x = ");
    for(int i = 0; i < x.n; ++i)
        printf("%6.1lf ", x.vec[i]);

    printf("\n\n");

    printf("y_direct = ");
    for(int i = 0; i < y_direct.n; ++i)
        printf("%6.1lf ", y_direct.vec[i]);

    printf("\n");

    printf("y_matvec = ");
    for(int i = 0; i < y_matvec.n; ++i)
        printf("%6.1lf ", y_matvec.vec[i]);

    printf("\n\n");

    int match = 1;
    for(int i = 0; i < y_direct.n; ++i) {
        match &= (y_direct.vec[i] == y_matvec.vec[i]);
    }

    printf("MATCH = %s\n", match ? "YES" : "NO");

    return 0;
}

void fir_direct(const struct Vector *h, const struct Vector *x, struct Vector *y) {
    y->n = x->n;

    for(int i = 0; i < y->n; ++i) {
        y->vec[i] = 0.0;
        for(int k = 0; k < h->n; ++k) {
            y->vec[i] += (x->vec[k] * h->vec[(i - k + h->n) % h->n]);
        }
    }
}

void fir_via_matvec(const struct Vector *h, const struct Vector *x, struct Vector *y) {

    struct Matrix toplitz_h;
    vec_to_toplitz(h, &toplitz_h, x->n);
    *y = matvec(&toplitz_h, x);
}

void vec_to_toplitz(const struct Vector *v, struct Matrix *toplitz_v, int N) {
    
    if(N == 0) {
        toplitz_v->m = v->n;
        toplitz_v->n = v->n;
    }
    else {
        toplitz_v->m = N;
        toplitz_v->n = N;
    }

    memset(toplitz_v->mat, 0, sizeof(toplitz_v->mat));

    for(int i = 0; i < toplitz_v->m; ++i) {
        for(int j = 0; j < toplitz_v->n; ++j) {
            toplitz_v->mat[i][j] = v->vec[(i - j + v->n) % v->n]; 
        }
    }
}

struct Vector matvec(const struct Matrix *A, const struct Vector *v) {
    
    if(A->n != v->n) {
        printf("DIMENTIONS DON'T MATCH!\n");
        return (struct Vector){0};
    }

    struct Vector res = {.n = A->m, .vec = {0}};
    for(int i = 0; i < res.n; ++i) {
        for(int k = 0; k < A->n; ++k) {
            res.vec[i] += (A->mat[i][k] * v->vec[k]);
        }
    }

    return res;
}