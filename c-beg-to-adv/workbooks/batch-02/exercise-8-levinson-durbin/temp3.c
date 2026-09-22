#include <stdio.h>

#define MAX_NOISE_SIZE 12
#define MAX_ORDER      64 
#define ABS(x)         (((x) > 0) ? (x) : (-(x)))

static const double w[MAX_NOISE_SIZE] = {
    0.5, -0.3, 0.8, -0.2, 0.1,
    -0.7, 0.4, 0.6, -0.5, 0.2,
    0.3, -0.1
};
static double x[MAX_NOISE_SIZE] =     {0.0};
static double k_arr[MAX_NOISE_SIZE] = {0.0};
static int    flop_counter          =  0;

void init_x();
void acf(const double *x, int n_, double *r);
void print_vector(const double *x, int l);
void vec_to_toeplitz(const double *r, int size, double **R);
void print_mat(const double **M, int r, int c);
double ld_stage(double *a, double *E, const double* r, int m);
void levinson_durbin(const double *r, int p, double *a);
int k_stable(int m);

void print_result(const char *test_name,
                  const double *a,
                  double E,
                  int order)
{
    printf("========================================\n");
    printf("%s\n", test_name);
    printf("========================================\n");

    printf("Order: %d\n\n", order);

    for(int i = 0; i <= order; ++i)
    {
        printf("a[%d] = % .12f\n", i, a[i]);
    }

    printf("\nE    = % .12f\n\n", E);
}

int main(void)
{
    init_x();

    printf("x[n\\]:\n");
    print_vector(x, MAX_NOISE_SIZE);

    double r[(2 * MAX_NOISE_SIZE) - 1] = {0.0};

    acf(x, MAX_NOISE_SIZE, r);

    printf("\nACF:\n");
    print_vector(r, (2 * MAX_NOISE_SIZE) - 1);

    double a[5] = {0.0};

    /* =========================================================
       CASE 1: Valid ACF generated from x[n]
       ========================================================= */

    printf("\n\n");
    printf("========================================\n");
    printf("CASE 1: VALID ACF\n");
    printf("========================================\n");

    /* p = 4, pass pointer to lag-0 element */
    levinson_durbin(&r[MAX_NOISE_SIZE - 1], 4, a);

    printf("\nLPC coefficients:\n");

    for(int i = 0; i <= 4; ++i) {
        printf("a[%d] = %.12lf\n", i, a[i]);
    }

    printf("\nReflection coefficient stability check:\n");

    int unstable_count = k_stable(4);

    if(unstable_count == 0) {
        printf("All reflection coefficients are stable (|k| <= 1)\n");
    } else {
        printf("%d unstable reflection coefficient(s) detected "
               "(|k| > 1)\n",
               unstable_count);
    }

    /* =========================================================
       CASE 2: Deliberately invalid ACF
       ========================================================= */

    printf("\n\n");
    printf("========================================\n");
    printf("CASE 2: FORCED INVALID ACF\n");
    printf("========================================\n");

    int center = MAX_NOISE_SIZE - 1;

    /*
     * Force:
     *
     *     r[1] = 1.1 * r[0]
     *
     * Therefore, at Levinson-Durbin stage 1:
     *
     *     K = -r[1] / r[0] = -1.1
     *
     * and:
     *
     *     |K| = 1.1 > 1
     */

    r[center + 1] = 1.1 * r[center];

    /* Preserve ACF symmetry */
    r[center - 1] = r[center + 1];

    printf("\nForced invalid ACF:\n");
    print_vector(r, (2 * MAX_NOISE_SIZE) - 1);

    double a_bad[2] = {0.0};

    /*
     * Only order 1 is required to demonstrate the invalid
     * reflection coefficient. Continuing after E becomes
     * negative is unnecessary for this test.
     */
    levinson_durbin(&r[center], 1, a_bad);

    printf("\nLPC coefficients:\n");

    for(int i = 0; i <= 1; ++i) {
        printf("a[%d] = %.12lf\n", i, a_bad[i]);
    }

    printf("\nReflection coefficient stability check:\n");

    unstable_count = k_stable(1);

    if(unstable_count == 0) {
        printf("All reflection coefficients are stable (|k| <= 1)\n");
    } else {
        printf("%d unstable reflection coefficient(s) detected "
               "(|k| > 1)\n",
               unstable_count);
    }

        /* =========================================================
       CASE 3: FLOP COUNT VS ORDER
       ========================================================= */

    printf("\n\n");
    printf("========================================\n");
    printf("CASE 3: FLOP COUNT\n");
    printf("========================================\n");

    {
        int orders[] = {4, 8, 11};
        int num_orders = sizeof(orders) / sizeof(orders[0]);

        for(int t = 0; t < num_orders; ++t)
        {
            int p = orders[t];

            double a_test[MAX_ORDER + 1] = {0.0};

            levinson_durbin(&r[MAX_NOISE_SIZE - 1],
                            p,
                            a_test);

            printf("p = %2d --> flop_counter = %d\n",
                   p,
                   flop_counter);
        }
    }

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

double ld_stage(double *a, double *E, const double* r, int m) {
    
    double delta = r[m];
    double K     = 0.0;
    double a_temp[MAX_ORDER + 1] = {1.0};

    for(int k = 1; k < m ; ++k) {
        delta += (a[k] * r[m - k]);
        flop_counter += 1;
    };

    K = -delta / (*E);

    for(int k = 1; k < m; ++k) {
        a_temp[k] = a[k] + K*a[m - k];
    };

    for(int i = 0; i < m; ++i) {
        a[i] = a_temp[i];
    };

    a[m] = K;

    (*E) = (*E) * (1 - (K * K));

    return K;
};

void levinson_durbin(const double *r, int p, double *a) {
    flop_counter = 0;
    a[0] = 1.0;

    double E = r[0];
    for(int m = 1; m < p + 1; ++m) {
        k_arr[m - 1] = ld_stage(a, &E, r, m);
        //printf("\nFinal E = %.12lf\n", E);
    };
}

int k_stable(int m) {

    int k_stable = 0;

    for(int i = 0; i < m; ++i) {
        //printf("|k[%d]| = %4.2lf\n", i, ABS(k_arr[i]));
        k_stable += (ABS(k_arr[i]) > 1.0);
    };

    return k_stable;
};