#include <stdio.h>
#include <stdlib.h>
#include <math.h>


#define SIZE 4

double norm2(const double *x, int n);
int normalize(double *x, int n) ;

int main() {

    
    double x[SIZE] = {
        3.0, 4.0, 0.0, 12.0
    };

    normalize(x, SIZE);
    for(int i = 0; i < SIZE; ++i) {
        printf("x[%d] = %4.2lf\n", i, x[i]);
    };
    return 0;
}

double norm2(const double *x, int n) {
    
    double sum = 0.0;
    for(int i = 0; i < n;sum += (x[i] * x[i]), ++i);

    return sqrt(sum);
};

int normalize(double *x, int n) {
    double norm = norm2(x, n);
    double alpha = 1.0 / norm;

    if(!(norm)) {
        return 0;
    }

    for(int i = 0; i < n; ++i) {
        x[i] *= alpha;
    };
    return 1;
}