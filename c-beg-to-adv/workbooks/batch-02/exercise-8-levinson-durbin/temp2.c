#include <stdio.h>

#define MAX_VEC_LEN 100
#define MAX_ORDER   10
#define ABS(n)      (n) < 0 ? (-(n)) : (n)

void prediction_error(const double *x, int length, const double a[], int p, double *e);
void acf_biased(const double* x, int N, double* r, int p);
void toeplitz_from_r(const double *r, int p, double *G);

int main(void)
{
    double G[MAX_ORDER * MAX_ORDER];

    /* TEST 1 */
    {
        double r[] = {1.0, 0.5, 0.25};

        printf("\n=== TEST 1 ===\n");

        toeplitz_from_r(r, 3, G);

        for(int i = 0; i < 3; ++i) {
            for(int j = 0; j < 3; ++j) {
                printf("%8.3lf ", G[i + 3*j]);
            }
            printf("\n");
        }
    }

    /* TEST 2 */
    {
        double r[] = {7.5, 5.0, 2.75, 1.0};

        printf("\n=== TEST 2 ===\n");

        toeplitz_from_r(r, 4, G);

        for(int i = 0; i < 4; ++i) {
            for(int j = 0; j < 4; ++j) {
                printf("%8.3lf ", G[i + 4*j]);
            }
            printf("\n");
        }
    }

    /* TEST 3 */
    {
        double r[] = {1.0, -0.75, 0.5, -0.25};

        printf("\n=== TEST 3 ===\n");

        toeplitz_from_r(r, 4, G);

        for(int i = 0; i < 4; ++i) {
            for(int j = 0; j < 4; ++j) {
                printf("%8.3lf ", G[i + 4*j]);
            }
            printf("\n");
        }
    }

    /* TEST 4 */
    {
        double r[] = {25.0};

        printf("\n=== TEST 4 ===\n");

        toeplitz_from_r(r, 1, G);

        for(int i = 0; i < 1; ++i) {
            for(int j = 0; j < 1; ++j) {
                printf("%8.3lf ", G[i + 1*j]);
            }
            printf("\n");
        }
    }

    /* TEST 5 */
    {
        double r[] = {10.0, 0.0, 0.0};

        printf("\n=== TEST 5 ===\n");

        toeplitz_from_r(r, 3, G);

        for(int i = 0; i < 3; ++i) {
            for(int j = 0; j < 3; ++j) {
                printf("%8.3lf ", G[i + 3*j]);
            }
            printf("\n");
        }
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