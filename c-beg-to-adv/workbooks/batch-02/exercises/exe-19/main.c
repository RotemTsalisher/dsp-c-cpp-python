#include <stdio.h>
#include <stdlib.h>

#define SIZE 8

static double bin_powers[SIZE] = {
    0.125, 0.042, 0.278, 0.091,
    0.156, 0.334, 0.073, 0.210
};

int main() {

    double min = bin_powers[0], max = bin_powers[0], avg = 0.0;

    for (int i = 0; i < SIZE; ++i) {
        
        if(bin_powers[i] < min) {
            min = bin_powers[i];
        }

        if(bin_powers[i] > max) {
            max = bin_powers[i];
        }

        avg += bin_powers[i];
    }

    avg /= (double)SIZE;

    printf("min = %5.3lf || max = %5.3lf || avg = %5.3lf\n", min, max, avg);
    return 0;
}