#include <stdio.h>
#include <stdlib.h>

#define SIZE            5
#define SIZE_ARR(arr)   (sizeof(arr) / sizeof(arr[0]))


static double v1[SIZE] = {
    1.0, 2.0, 3.0, 4.0, 5.0
};

static double v2[SIZE] = {
    10.0, 20.0, 30.0, 40.0, 50.0
};
 
double dot_product(const double *v1, const double *v2, int size);

int main() {

    printf("v1 .* v2 = %4.2lf\n", dot_product(v1, v2, SIZE_ARR(v1)));
    
    return 0;
}

double dot_product(const double *v1, const double *v2, int size) {
    
    double res = 0.0;
    for(int i = 0; i < size; ++i) {
        res += (v1[i] * v2[i]);
    }

    return res;
};