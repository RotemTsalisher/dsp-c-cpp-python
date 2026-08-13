#include <stdio.h>

#define TINY       1e-8
#define MANY_TIMES 1000000

int main() {

    double sum_addition       = 0.0;
    double sum_multiplication = 0.0;

    for(int i = 0; i < MANY_TIMES; ++i) {
        sum_addition += TINY;
    };

    sum_multiplication = MANY_TIMES * TINY;

    printf("addition : %lf\nmultiplication : %lf\n", sum_addition, sum_multiplication);

    return 0;
}