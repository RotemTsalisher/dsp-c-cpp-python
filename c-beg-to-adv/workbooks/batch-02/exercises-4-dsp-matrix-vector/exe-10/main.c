#include <stdio.h>
#include <stdlib.h>

void axpy(double alpha, const double x[], int n, double y[]);

int main() {
    const int n = 6;
    const double alpha = 0.1;

    double x[6] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0};
    double y[6] = {10.0, 20.0, 30.0, 40.0, 50.0, 60.0};

    for (int i = 0; i < n; ++i) {
        printf("%.1f ", y[i]);
    }
    printf("\n");

    axpy(alpha, x, n, y);

    for (int i = 0; i < n; ++i) {
        printf("%.1f ", y[i]);
    }
    printf("\n");

    return 0;
}

void axpy(double alpha, const double x[], int n, double y[]) {
    for(int i = 0; i < n; ++i) {
        y[i] += alpha * x[i];
    };
};