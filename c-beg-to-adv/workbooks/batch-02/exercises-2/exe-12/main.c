#include <stdio.h>
#include <stdlib.h>

#define MAX_TAP_SIZE 8

int main() {

    double att = 0.0;
    double cumulative_sum = 0.0;
    for(int tap = 0; tap < MAX_TAP_SIZE; ++tap) {
        att = 1.0 / ((double)tap + 1);
        cumulative_sum += att;

        printf("Attenuation : %4.2lf | Cumulative Sum = %4.2lf |\n", att, cumulative_sum);
    };
    
    return 0;
}