#include <stdio.h>
#include <stdlib.h>

#define SIZE 3

int main() {

    double gain[SIZE] = {0.0, 1.0, 2.5}, *gp[SIZE] = {gain, gain + 1, gain + 2};
    for(int i = 0; i < SIZE; ++i) {
        *(gp[i]) *= 0.5;
    };

    for(int i = 0; i < SIZE; ++i) {
        printf("GAIN [%d] : %4.2lf\n", i, gain[i]);
    };
    return 0;
}