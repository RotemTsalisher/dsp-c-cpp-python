#include <stdio.h>

#define MAX_VEC_LEN 100
#define MAX_ORDER   10
#define ABS(n)      ((n) < 0 ? (-(n)) : (n))

void prediction_error(const double *x, int length, const double a[], int p, double *e);
void acf_biased(const double* x, int N, double* r, int p);
void toeplitz_from_r(const double *r, int p, double *G);
int ld_order1(const double *r, int size, double *k, double *E);
int ld_order2(const double *r, int size, double *k, double *E, double *a_);
int check_k(const double *K, int p);
void ld_stage(double* a, double* E, const double* r, int m);
void levinson_durbin(const double *r, int p, double *a, double *E_out);
void two_by_two_inv(double **mat);

static double e_array[MAX_ORDER] = {0.0};
static int    e_idx              =  0;

int main(void)
{
    struct {
        double m[2][2];
        const char *name;
    } tests[] =
    {
        { {{4.0, 7.0}, {2.0, 6.0}}, "Classic example" },
        { {{1.0, 2.0}, {3.0, 4.0}}, "Negative determinant" },
        { {{5.0, 0.0}, {0.0, 2.0}}, "Diagonal matrix" },
        { {{1.0, 0.0}, {0.0, 1.0}}, "Identity matrix" },
        { {{2.0, -1.0}, {-1.0, 2.0}}, "Symmetric matrix" }
    };

    const int num_tests = sizeof(tests) / sizeof(tests[0]);

    for(int t = 0; t < num_tests; ++t)
    {
        double row0[2];
        double row1[2];
        double *mat[2] = { row0, row1 };

        row0[0] = tests[t].m[0][0];
        row0[1] = tests[t].m[0][1];
        row1[0] = tests[t].m[1][0];
        row1[1] = tests[t].m[1][1];

        printf("\n=================================\n");
        printf("TEST %d : %s\n", t + 1, tests[t].name);
        printf("=================================\n");

        printf("Before:\n");
        printf("[ %8.4f %8.4f ]\n", mat[0][0], mat[0][1]);
        printf("[ %8.4f %8.4f ]\n", mat[1][0], mat[1][1]);

        two_by_two_inv(mat);

        printf("\nAfter:\n");
        printf("[ %8.4f %8.4f ]\n", mat[0][0], mat[0][1]);
        printf("[ %8.4f %8.4f ]\n", mat[1][0], mat[1][1]);
    }

    return 0;
}

void toeplitz_from_r(const double *r, int p, double *G) {

    for(int i = 0; i < p; ++i) {
        for(int j = 0; j < p; ++j) {
            G[i + p*j] = r[(ABS(i - j))];
        }
    }
}

void acf_biased(const double* x, int N, double* r, int p) {
    double tmp = 0.0;

    for(int k = 0; k < p; ++k) {
        tmp = 0.0;

        for(int n = k; n < N; ++n) {
            tmp += (x[n] * x[n - k]);
        };

        r[k] = (1.0 / N) * tmp;
    };
}

void prediction_error(const double *x, int length,
                      const double a[], int p,
                      double *e)
{
    for(int n = 0; n < length; ++n) {
        double tmp = 0.0;

        printf("\n=== n = %d ===\n", n);

        for(int k = 0; k < (p + 1); ++k) {

            if(n - k < 0) {
                printf("k=%d : x[%d] unavailable -> +0.0, tmp=%lf\n",
                       k, n - k, tmp);
            }
            else {
                double term = a[k] * x[n - k];

                printf(
                    "k=%d : a[%d]=%lf * x[%d]=%lf -> term=%lf\n",
                    k,
                    k,
                    a[k],
                    n - k,
                    x[n - k],
                    term
                );

                tmp += term;

                printf("      tmp=%lf\n", tmp);
            }
        }

        e[n] = tmp;

        printf("e[%d] = %lf\n", n, e[n]);
    }
}

int ld_order1(const double *r, int size, double *k, double *E) {
    
    // size is expected to be 2 for ld order 1
    
    if( (2 != size) || (r[0] <= 0) || (ABS((*k)) >= 1)) {
        return -1;
    };

    (*k) = -(r[1] / r[0]);
    (*E) = r[0] * (1 - ((*k) * (*k)));
    return 0;
};

int ld_order2(const double *r, int size, double *k, double *E, double *a_) {

    // size is p + 1, i.e 3 for p = 2

    a_[0] = 1.0;

    if((size != 3) || (r[0] <= 0)) {
        return -1;
    }

    // p = 1:

    (*k) = -(r[1] / r[0]);
    (*E) = r[0] * (1 - ((*k) * (*k)));

    a_[1] = *k;

    (*k) = -(r[2] + a_[1]*r[1]) / (*E);
    a_[1] = a_[1] + (*k) * a_[1];
    a_[2] = (*k);

    (*E) = (*E) * (1 - ((*k) * (*k)));

    return 0;
}

int check_k(const double *K, int p) {

    for(int i = 0; i < p; ++i) {
        if( (ABS(K[i]) >= 1) ) {
            return -1;
        }
    }

    return 0;
}

void ld_stage(double* a, double* E, const double* r, int m)
{
    double delta = r[m];
    double K = 0.0;
    double a_[100] = {0.0};

    printf("\n--- ld_stage(m=%d) ---\n", m);

    printf("Initial:\n");
    printf("E = %lf\n", *E);

    for(int k = 1; k < m; ++k) {
        printf("a[%d]=%lf, r[%d]=%lf -> contribution=%lf\n",
               k,
               a[k],
               m-k,
               r[m-k],
               a[k] * r[m-k]);

        delta += a[k] * r[m-k];
    }

    printf("Delta = %lf\n", delta);

    K = -delta / (*E);

    printf("K = %lf\n", K);

    (*E) = (*E) * (1.0 - (K * K));
    e_array[e_idx++] = (*E);

    for(int k = 1; k < m; ++k) {
        a_[k] = a[k] + K * a[m - k];
    }

    for(int k = 1; k < m; ++k) {
        a[k] = a_[k];
    }

    a[m] = K;

    printf("Updated coefficients:\n");

    for(int k = 0; k <= m; ++k) {
        printf("a[%d] = %lf\n", k, a[k]);
    }

    printf("Updated E = %lf\n", *E);
}

void levinson_durbin(const double *r, int p, double *a, double *E_out) {

    (*E_out) = r[0];

    e_array[e_idx++] = (*E_out);
    for(int i = 1; i < (p + 1); ++i) {
        ld_stage(a, E_out, r, i);
    };
}

void two_by_two_inv(double **mat) {
    double ad = mat[0][0] * mat[1][1];
    double bc = mat[0][1] * mat[1][0];

    double den    = ad - bc;
    double factor = 1.0 / den;

    double tmp = mat[0][0];
    mat[0][0] = factor * mat[1][1];
    mat[1][1] = factor * tmp;

    mat[0][1] = -factor * mat[0][1];
    mat[1][0] = -factor * mat[1][0];
};