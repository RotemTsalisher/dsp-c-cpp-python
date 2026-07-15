#include <stdio.h>
#include <stdlib.h>

#define SIZE 5
static double samples[SIZE] = { 
    -3.7,
     0.0,
     2.4,
    -0.1,
     5.9
};

int main() {

    for(int i = 0; i < SIZE; ++i) {
        printf("%d : %s\n", i, samples[i] >= 0.0 ? (samples[i] == 0.0 ? "Zero" : "Pos") : "Neg");
    };
    return 0;
}