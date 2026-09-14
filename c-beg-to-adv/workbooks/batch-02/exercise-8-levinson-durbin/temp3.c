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

int main() {
    
    double r[2*MAX_NOISE_SIZE -1] = {0.0};

    init_x();
    print_vector(x, MAX_NOISE_SIZE);
    acf(x, MAX_NOISE_SIZE, r);
    print_vector(r, 2*MAX_NOISE_SIZE -1);
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
