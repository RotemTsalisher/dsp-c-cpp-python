#include <stdio.h>

#define MAX_VEC_LEN 100
#define MAX_ORDER   10

void prediction_error(const double *x, int length, const double a[], int p, double *e);

int main() {

    double x[MAX_VEC_LEN] = {1, 0.9, 0.81}, e[MAX_VEC_LEN] = {0.0};
    double a[MAX_ORDER + 1] = {1, -0.9};
    
    int length = 3;
    int p = 1;

    prediction_error(x, length, a, p, e);
    return 0;
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