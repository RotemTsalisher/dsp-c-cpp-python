#include <stdio.h>
#include <stdlib.h>

void zero_even_indices(double *begin, int length);

int main(void)
{
    double arr[] = {1.1, 2.2, 3.3, 4.4, 5.5, 6.6};
    int len = sizeof(arr) / sizeof(arr[0]);

    printf("Before:\n");
    for (int i = 0; i < len; ++i) {
        printf("%.1f ", arr[i]);
    }
    printf("\n");

    zero_even_indices(arr, len);

    printf("After:\n");
    for (int i = 0; i < len; ++i) {
        printf("%.1f ", arr[i]);
    }
    printf("\n");

    return 0;
}

void zero_even_indices(double *begin, int length) {
    double *tmp = begin;

    for(int i = 0; i < length; ++i, ++tmp) {
        if(!(i & 1u)) {
            *tmp = 0.0;
        };
    }
}
