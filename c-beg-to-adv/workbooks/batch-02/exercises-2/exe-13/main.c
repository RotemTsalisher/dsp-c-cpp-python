#include <stdio.h>
#include <stdlib.h>

#define ROWS 3
#define COLS 4


static double gains[ROWS][COLS] = {
    {1.000, 0.500, 0.250, 0.125},
    {0.900, 0.450, 0.225, 0.112},
    {0.800, 0.400, 0.200, 0.100}
};


int main() {

    for(int i = 0; i < ROWS; ++i) {
        printf("| %6.3lf | %6.3lf | %6.3lf | %6.3lf |\n", gains[i][0], gains[i][1], gains[i][2], gains[i][3]);
    };

}