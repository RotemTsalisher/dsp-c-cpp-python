#include <stdio.h>

#define AUTOCORR_SIZE 5
#define ABS(x) ((x) > 0 ? (x) : -(x))
#define MAX_ORDER     4
#define OFFSET        (int)(AUTOCORR_SIZE / 2)

static const double r[AUTOCORR_SIZE] = {
    1.00,
    0.80,
    0.50,
    0.25,
    0.10
};

static double p[AUTOCORR_SIZE][AUTOCORR_SIZE] = {0.0};

void vector_to_toeplitz(const double v[],
                        int size,
                        double p[][AUTOCORR_SIZE])
{
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            p[i][j] = v[ABS(i - j)];
        }
    }
}

void levinson_durbin_order_2(const double *rxx, double a[])
{
    double a_new[MAX_ORDER] = {0.0};
    double e_ = 0.0, k_ = 0.0;

    printf("\n=== ORDER 1 ===\n");

    a[0] = -(rxx[1] / rxx[0]);
    k_ = a[0];
    e_ = rxx[0] + a[0] * rxx[1];

    printf("K1      = %+.6f\n", k_);
    printf("a1(1)   = %+.6f\n", a[0]);
    printf("E1      = %.6f\n", e_);

    printf("\n=== ORDER 2 ===\n");

    a_new[1] = -(rxx[2] + a[0] * rxx[1]) / e_;
    k_ = a_new[1];

    a_new[0] = a[0] + k_ * a[0];

    e_ = e_ * (1.0 - (k_ * k_));

    printf("K2      = %+.6f\n", k_);
    printf("a2(1)   = %+.6f\n", a_new[0]);
    printf("a2(2)   = %+.6f\n", a_new[1]);
    printf("E2      = %.6f\n", e_);

    a[0] = a_new[0];
    a[1] = a_new[1];
}

void levinson_durbin_nth_order(const double *rxx, int order, double a[])
{
    double a_new[MAX_ORDER + 1] = {0.0};
    double e_ = 0.0, k_ = 0.0, delta = 0.0;

    /* init process : */
    e_= rxx[0];
    a[0] = 1; /* unused index to fit 1 based indexing */

    /* go to desired order */
    for(int m = 1; m < (order + 1); ++m) {

        printf("\n=== ORDER %d ===\n", m);

        /* compute forward residual correlation */
        delta = rxx[m];
        for(int k = 1; k < m; ++k) {
            delta += (a[k] * rxx[m - k]);
        };

        printf("delta   = %+.12f\n", delta);

        /* reflection coeff */
        k_ = -(delta / e_);

        printf("K%d      = %+.12f\n", m, k_);

        /* loop over new coeffs */
        for(int k = 1; k < m; ++k) {
            a_new[k] = a[k] + k_ * a[m - k];
        }

        a[m] = k_;

        e_ = e_ * (1 - (k_ * k_));

        printf("E%d      = %.12f\n", m, e_);

        for(int i = 1; i < m; ++i) {
            a[i] = a_new[i];
        };

        printf("COEFFS\n");

        for(int i = 0; i <= m; ++i) {
            printf("a[%d] = %+.12f\n", i, a[i]);
        }
    };
}

void autocorr(const double in[], int size, double out[])
{
    int n,k;
    int offset = size - 1;

    for(n = 0; n < size; ++n) {
        double tmp = 0.0;
        for(k = 0; k < size - n; ++k) {
            tmp += (in[k] * in[k + n]);
        };
        out[n + offset] = (tmp / ((double)size));
    };

    for(int i = 0; i < offset; ++i) {
        out[i] = out[(2*size - 1) - i - 1];
    };
};

void print_matrix(double p[][AUTOCORR_SIZE], int rows, int cols)
{
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            printf("%6.2f ", p[i][j]);
        }
        printf("\n");
    }
}

int main(void)
{
    for(int order = 1; order <= MAX_ORDER; ++order) {

        double a[MAX_ORDER + 1] = {0.0};

        printf("\n");
        printf("========================================\n");
        printf("TEST ORDER %d\n", order);
        printf("========================================\n");

        levinson_durbin_nth_order(r,
                                  order,
                                  a);

        printf("FINAL COEFFS\n");

        for(int i = 0; i <= order; ++i) {
            printf("a[%d] = %+.12f\n",
                   i,
                   a[i]);
        }
    }

    return 0;
}