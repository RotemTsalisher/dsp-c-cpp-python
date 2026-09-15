#include <stdio.h>

#define MAX_NOISE_SIZE 12

static const double w[MAX_NOISE_SIZE] = {
    0.5, -0.3, 0.8, -0.2, 0.1,
    -0.7, 0.4, 0.6, -0.5, 0.2,
    0.3, -0.1
};
static double x[MAX_NOISE_SIZE] = {0.0};

void init_x();
void acf(const double *x, int n_, double *r);
void print_vector(const double *x, int l);
void vec_to_toeplitz(const double *r, int size, double **R);
void print_mat(const double **M, int r, int c);

int main() {

    double r[2 * MAX_NOISE_SIZE - 1] = {0.0};

    /* Toeplitz storage */
    double storage[MAX_NOISE_SIZE][MAX_NOISE_SIZE];
    double *R[MAX_NOISE_SIZE];

    for(int i = 0; i < MAX_NOISE_SIZE; ++i) {
        R[i] = storage[i];
    }

    /* Generate AR process */
    init_x();

    printf("x:\n");
    print_vector(x, MAX_NOISE_SIZE);

    /* Compute ACF */
    acf(x, MAX_NOISE_SIZE, r);

    printf("\nr:\n");
    print_vector(r, 2 * MAX_NOISE_SIZE - 1);

    /* Build Toeplitz from ACF */
    vec_to_toeplitz(r,
                    2 * MAX_NOISE_SIZE - 1,
                    R);

    printf("\nToeplitz matrix R:\n");
    print_mat((const double **)R,
              MAX_NOISE_SIZE,
              MAX_NOISE_SIZE);

    return 0;
}

void print_vector(const double *x, int l) {
    printf("v = <%5.3lf, ", x[0]);
    for(int i = 1; i < l - 1; ++i) {
        printf("%5.3lf, ", x[i]);
    }
    printf("%5.3lf>\n", x[l -1]);
};

void acf(const double *x, int n_, double *r) {
    
    double tmp = 0.0;
    int offset = n_ - 1;

    for(int k = 0; k < n_; ++k) {
        tmp = 0.0;
        for(int n = k; n < n_; ++n) {
            tmp += (x[n] * x[n - k]);
        };

        r[k + offset] = (1.0 / ((double)n_)) * tmp;
    };

    for(int i = 0; i < n_; ++i) {
        r[i] = r[2*(n_ - 1) - i];
    };
};

void init_x() {
    x[0] = w[0];
    for(int i = 1; i < MAX_NOISE_SIZE; ++i) {
        x[i] = 0.9*x[i - 1] + w[i];
    };
};

void vec_to_toeplitz(const double *r, int size, double **R) {

    int center = size / 2;
    int N = center + 1;

    for(int i = 0; i < N; ++i) {
        for(int j = 0; j < N; ++j) {
            R[i][j] = r[i - j + center];
        }
    }
}

void print_mat(const double **M, int r, int c) {

    for(int i = 0; i < r - 1; ++i) {
        printf("[");
        for(int j = 0; j < c - 1; ++j) {
            printf("%4.2lf ", M[i][j]);
        }
        printf("%4.2lf]\n", M[i][c-1]);
    };
    printf("[");
    for(int j = 0; j < c - 1; ++j) {
        printf("%4.2lf ",M[r-1][j]);
    };
    printf("%4.2lf]\n", M[r-1][c-1]);
};