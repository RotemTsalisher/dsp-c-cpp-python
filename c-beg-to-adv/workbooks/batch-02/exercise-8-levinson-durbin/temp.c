#include <stdio.h>

#define AUTOCORR_SIZE 5
#define ABS(x) ((x) > 0 ? (x) : -(x))

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
    double x[] = {
        1.0,
        2.0,
        3.0,
        4.0,
        5.0
    };

    int x_size = sizeof(x) / sizeof(x[0]);

    double rxx[2 * AUTOCORR_SIZE - 1] = {0.0};

    autocorr(x, x_size, rxx);

    vector_to_toeplitz(&rxx[x_size - 1],
                       AUTOCORR_SIZE,
                       p);

    printf("Input signal:\n");
    for (int i = 0; i < x_size; ++i) {
        printf("x[%d] = %.2f\n", i, x[i]);
    }

    printf("\nAutocorrelation:\n");
    for (int i = 0; i < (2 * x_size - 1); ++i) {
        printf("rxx[%d] = %.4f\n", i, rxx[i]);
    }

    printf("\nToeplitz matrix:\n");
    print_matrix(p, AUTOCORR_SIZE, AUTOCORR_SIZE);

    return 0;
}