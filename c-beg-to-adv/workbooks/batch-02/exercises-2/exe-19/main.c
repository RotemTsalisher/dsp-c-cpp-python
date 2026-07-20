#include <stdio.h>
#include <stdlib.h>

void swap_ints(int *n, int *m) {
    int *tmp;
    *tmp = *n;
    *n = *m;
    *m = *tmp;
};

void increment_int(int *x) {
    (*x)++;
};

int main() {

    int a = 3, b = 2;
    swap_ints(&a, &b);
    printf("a = %d | b = %d \n", a, b);

    increment_int(&a);
    printf("a = %d\n", a);
    return 0;
}