#include <stdio.h>
#include <stdlib.h>


double mean_arr(const double *arr, int size) {
    double *begin = (double*)arr;
    double *end = begin + size;
    double mean = 0.0;
    for(begin; begin != end; ++begin) {
        printf("Val : %4.2lf\n", *begin);
        mean += (*begin);
    };

    return mean / (float)size;
};


int main(void) {
    double arr[] = { 1.0, 2.0, 3.0, 4.0, 5.0 };
    int size = sizeof(arr) / sizeof(arr[0]);

    printf("Mean = %.2lf\n", mean_arr(arr, size));

    return 0;
};
