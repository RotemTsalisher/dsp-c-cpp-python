#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static double G[3][4] = {
    {  1.25,  -2.50,   3.75,   4.10 },
    { -0.50,   8.20,  -1.75,   2.30 },
    {  9.90,  -4.40,   0.15,  -7.60 }
};

int main() {

    printf("====================\n");
    printf("DIMENTIONS : row = %d | cols = %d\n", 3, 4);

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 4; ++j) {
            printf("| %.3lf |", G[i][j]);
        };
        printf("\n");
    };

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 4; ++j) {
            printf("| linear storage : %d |\n", i*4 + j);
        };
    };


    return 0;
}
