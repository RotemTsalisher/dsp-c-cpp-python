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
    vector_to_toeplitz(r, AUTOCORR_SIZE, p);

    printf("Autocorrelation vector:\n");
    for (int i = 0; i < AUTOCORR_SIZE; ++i) {
        printf("r[%d] = %.2f\n", i, r[i]);
    }

    printf("\nToeplitz matrix:\n");
    print_matrix(p, AUTOCORR_SIZE, AUTOCORR_SIZE);

    return 0;
}