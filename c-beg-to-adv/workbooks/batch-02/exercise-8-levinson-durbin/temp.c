#include <stdio.h>

#define AUTOCORR_SIZE 5
#define ABS(x) ((x) > 0 ? (x) : -(x))
#define MAX_ORDER     2
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

void autocorr(const double in[], int size, double out[]) {
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
    double a[MAX_ORDER] = {0.0};

    printf("Levinson-Durbin input:\n");

    for (int i = 0; i < AUTOCORR_SIZE; ++i) {
        printf("r[%d] = %.6f\n", i, r[i]);
    }

    levinson_durbin_order_2(r, a);

    printf("\nFinal AR(2) coefficients:\n");
    printf("a[0] = %+.6f\n", a[0]);
    printf("a[1] = %+.6f\n", a[1]);

    return 0;
}