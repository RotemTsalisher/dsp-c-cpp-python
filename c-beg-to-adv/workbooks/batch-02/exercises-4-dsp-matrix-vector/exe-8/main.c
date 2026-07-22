#include <stdio.h>
#include <stdlib.h>

#define MAX_ROWS 100
#define MAX_COLS MAX_ROWS

struct Matrix {
    double mat[MAX_ROWS][MAX_COLS];
    int r, c;
};

struct Matrix transpose_mat(const struct Matrix *m);

static void print_matrix(const struct Matrix *m) {
    for (int i = 0; i < m->r; ++i) {
        for (int j = 0; j < m->c; ++j) {
            printf("%6.1f ", m->mat[i][j]);
        }
        printf("\n");
    }
}

int main(void) {
    struct Matrix m = {
        .mat = {
            {1, 2, 3},
            {4, 5, 6}
        },
        .r = 2,
        .c = 3
    };

    printf("Original (%dx%d):\n", m.r, m.c);
    print_matrix(&m);

    struct Matrix mt = transpose_mat(&m);

    printf("\nTranspose (%dx%d):\n", mt.r, mt.c);
    print_matrix(&mt);

    return 0;
}

struct Matrix transpose_mat(const struct Matrix *m) {
    struct Matrix m_transpose;

    m_transpose.r = m->c;
    m_transpose.c = m->r;

    for (int i = 0; i < m_transpose.r; ++i) {
        for (int j = 0; j < m_transpose.c; ++j) {
            m_transpose.mat[i][j] = m->mat[j][i];
        }
    }

    return m_transpose;
}