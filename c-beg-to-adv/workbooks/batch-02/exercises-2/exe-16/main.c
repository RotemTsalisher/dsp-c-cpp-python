#include <stdio.h>
#include <stdlib.h>

#define ROWS 100
#define COLS 100

struct Matrix {
    double m[ROWS][COLS];
    int r,c;
};

void init_matrix(struct Matrix *m) {
    printf("Enter Dimentions : ");
    scanf("%d %d", &(m->r), &(m->c));

    for(int i = 0; i < m->r; ++i) {
        for(int j = 0; j < m->c; ++j) {
            printf("mat[%d][%d] : ", i, j);
            scanf(" %lf", &(m->m[i][j]));
        }
    };
};

void print_mat(const struct Matrix *m) {
    printf("===== Print %d by %d Matrix =====\n", m->r, m->c);  
    for(int i = 0; i < m->r; ++i) {
        for(int j = 0; j < m->c ; ++j) {
            printf("| %4.2lf |", m->m[i][j]);
        }
        printf("\n");
    }
}
struct Matrix mat_mult(const struct Matrix *m1, const struct Matrix* m2) {
    
    if(m1->c != m2->r) {
        printf("Dimentions Don't Match!\n");
        return (struct Matrix){0, 0, 0};
    };

    struct Matrix res = {0};
    double tmp = 0.0;
    res.r = m1->r;
    res.c = m2->c;

    for(int i = 0; i < res.r; ++i) {
        for(int j = 0; j < res.c; ++j) {
            for(int k = 0; k <m2->r; ++k) {
                res.m[i][j] += (m1->m[i][k] * m2->m[k][j]);
            }
        }
    }

    return res;
};

int main(void)
{
    struct Matrix m1, m2, res;

    printf("Matrix 1\n");
    init_matrix(&m1);

    printf("\nMatrix 2\n");
    init_matrix(&m2);

    printf("\nM1:\n");
    print_mat(&m1);

    printf("\nM2:\n");
    print_mat(&m2);

    res = mat_mult(&m1, &m2);

    printf("\nResult:\n");
    print_mat(&res);

    return 0;
}